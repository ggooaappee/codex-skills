#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill a Word lab-report template from a UTF-8 JSON job file (Windows + Word COM).

    python fill_report.py --job report.json

report.json:
{
  "template": "C:/.../学号-姓名-实验1 实验模版.doc",
  "out":      "C:/.../outputs/1123...-实验1.doc",
  "pdf":      "C:/.../work/preview.pdf",
  "student":  {"class": "252301", "id": "1123...", "name": "...", "date": "2026年10月19日"},
  "title":    "实验1  顺序表的基本操作及其应用算法",
  "blocks": [
    {"type": "h2",   "text": "一、实验内容"},
    {"type": "h3",   "text": "1．顺序表的基本操作算法（exp1.h、exp1.c）"},
    {"type": "body", "text": "……"},
    {"type": "img",  "path": "C:/.../shot.png", "caption": "图 1  exp1.c 的运行结果", "width": 290},
    {"type": "img-placeholder", "caption": "图 1  exp1.c 的运行结果", "hint": "（在此处粘贴 exp1.h 源代码截图）", "height": 180}
  ],
  "summary": ["……", "……"]
}

Block types: h2, h3, body, img, img-placeholder.
Requires Microsoft Word and pywin32 (pip install pywin32).
"""
import argparse
import json
import os
import shutil
import sys
import time

import win32com.client as win32

WD_ALIGN_LEFT = 0
WD_ALIGN_CENTER = 1
WD_ALIGN_JUSTIFY = 3
WD_ROW_AUTO = 0
WD_ROW_AT_LEAST = 2
WD_LINE_EXACT = 4


def setfont(f, name, size, east=None):
    f.Name = name
    f.NameAscii = name
    f.NameFarEast = east or name
    f.Size = size
    f.SizeFarEast = size


def set_cell_text(cell, lines, chunk=40):
    """Write many paragraphs into a cell without hitting COM string limits."""
    cell.Range.Text = lines[0]
    buf = []

    def flush():
        if not buf:
            return
        r = cell.Range
        r.End = r.End - 1          # keep the cell mark out of the range
        r.Collapse(0)
        r.InsertAfter("\r" + "\r".join(buf))
        del buf[:]

    for line in lines[1:]:
        buf.append(line)
        if len(buf) >= chunk:
            flush()
    flush()


def fmt_para(p, kind):
    pf = p.Format
    f = p.Range.Font
    pf.SpaceBefore = 0
    pf.SpaceAfter = 0
    pf.LineSpacingRule = 0
    pf.LeftIndent = 0
    pf.RightIndent = 0
    pf.FirstLineIndent = 0
    pf.Alignment = WD_ALIGN_JUSTIFY
    f.Bold = False
    f.Color = 0
    if kind == "h1":
        setfont(f, "黑体", 12); f.Bold = True
        pf.SpaceBefore = 10; pf.SpaceAfter = 4; pf.Alignment = WD_ALIGN_LEFT
    elif kind == "h2":
        setfont(f, "黑体", 11); f.Bold = True
        pf.SpaceBefore = 8; pf.SpaceAfter = 3; pf.Alignment = WD_ALIGN_LEFT
    elif kind == "h3":
        setfont(f, "黑体", 10.5); f.Bold = True
        pf.SpaceBefore = 8; pf.SpaceAfter = 3; pf.Alignment = WD_ALIGN_LEFT
    elif kind == "body":
        setfont(f, "仿宋", 10.5); pf.SpaceAfter = 4
    elif kind == "cap":
        setfont(f, "宋体", 9); pf.Alignment = WD_ALIGN_CENTER
        pf.SpaceBefore = 3; pf.SpaceAfter = 6
    else:
        setfont(f, "仿宋", 10.5); pf.SpaceAfter = 0


def clear_marker(cell, marker):
    for p in cell.Range.Paragraphs:
        if p.Range.Text.strip().strip("\x07").strip() == marker:
            r = p.Range
            r.MoveEnd(1, -1)
            pos = r.Start
            r.Delete()
            return pos
    raise RuntimeError("marker not found: " + marker)


def keep_with_next(doc, tbl):
    try:
        tbl.Rows(1).Cells(1).Range.ParagraphFormat.KeepWithNext = True
        nxt = doc.Range(tbl.Range.End, tbl.Range.End)
        pp = nxt.Paragraphs(1)
        pp.Format.KeepWithNext = True
        pp.Format.SpaceBefore = 0
        pp.Format.SpaceAfter = 0
        pp.Format.LineSpacingRule = WD_LINE_EXACT
        pp.Format.LineSpacing = 4
        pp.Range.Font.Size = 4
        pp.Range.Font.SizeFarEast = 4
    except Exception:
        pass


def add_box(doc, cell, marker, img=None, width=290.0, height=None, hint=None):
    pos = clear_marker(cell, marker)
    tbl = cell.Range.Tables.Add(doc.Range(pos, pos), 1, 1)
    tbl.PreferredWidthType = 2
    tbl.PreferredWidth = 100
    if height:
        tbl.Rows(1).HeightRule = WD_ROW_AT_LEAST
        tbl.Rows(1).Height = height
    else:
        tbl.Rows(1).HeightRule = WD_ROW_AUTO
    tbl.Borders.Enable = True
    for edge in (1, 2, 3, 4):
        b = tbl.Borders(edge)
        b.LineStyle = 1
        b.LineWidth = 2
        b.Color = 0x808080

    c = tbl.Rows(1).Cells(1)
    if img:
        c.Range.Text = ""
        r = c.Range
        r.SetRange(r.Start, r.Start)
        shp = doc.InlineShapes.AddPicture(FileName=img, LinkToFile=False,
                                          SaveWithDocument=True, Range=r)
        shp.LockAspectRatio = True
        shp.Width = width
        pf = c.Range.ParagraphFormat
        pf.Alignment = WD_ALIGN_CENTER
        pf.SpaceBefore = 0
        pf.SpaceAfter = 0
    else:
        c.Range.Text = hint or "（在此处粘贴截图）"
        pf = c.Range.ParagraphFormat
        pf.Alignment = WD_ALIGN_CENTER
        pf.SpaceBefore = 0
        pf.SpaceAfter = 0
        pf.LineSpacingRule = 0
        f = c.Range.Font
        setfont(f, "宋体", 8.5)
        f.Color = 0x808080
        f.Bold = False
    c.VerticalAlignment = 1
    keep_with_next(doc, tbl)


def build_flow(job):
    flow = []
    for b in job.get("blocks", []):
        kind = b.get("type", "body")
        if kind in ("img", "img-placeholder"):
            flow.append((kind, b))
            flow.append(("cap", {"text": b.get("caption", "")}))
        else:
            flow.append((kind, b))
    texts, seq = [], []
    n = 0
    for kind, val in flow:
        if kind in ("img", "img-placeholder"):
            n += 1
            seq.append((n, kind, val))
            texts.append("@IMG%d@" % n)
        else:
            texts.append(val.get("text", ""))
    return flow, texts, seq


def fill_document(doc, job, flow, texts, seq):
    t = doc.Tables(1)
    _ = t.Rows.Count                       # validates the COM connection
    t.Rows.AllowBreakAcrossPages = True
    for ri in range(1, t.Rows.Count + 1):
        try:
            t.Rows(ri).HeightRule = WD_ROW_AUTO
        except Exception:
            pass
    for ri in (6, 7, 8):
        try:
            t.Rows(ri).AllowBreakAcrossPages = False
        except Exception:
            pass

    st = job.get("student", {})
    for ci, key in ((1, "class"), (2, "id"), (3, "name"), (4, "date")):
        c = t.Cell(3, ci)
        c.Range.Text = str(st.get(key, ""))
        f = c.Range.Font
        setfont(f, "仿宋", 10.5)
        f.Bold = False
        c.Range.ParagraphFormat.Alignment = WD_ALIGN_CENTER

    t.Cell(4, 2).Range.Text = job.get("title", "")
    f = t.Cell(4, 2).Range.Font
    setfont(f, "仿宋", 10.5)
    f.Bold = False
    t.Cell(4, 2).Range.ParagraphFormat.Alignment = WD_ALIGN_CENTER

    try:
        t.Cell(5, 1).VerticalAlignment = 0
        t.Cell(5, 1).Range.ParagraphFormat.Alignment = WD_ALIGN_CENTER
        t.Cell(6, 1).Range.ParagraphFormat.Alignment = WD_ALIGN_CENTER
    except Exception:
        pass

    cell = t.Cell(5, 2)
    set_cell_text(cell, texts)
    paras = list(cell.Range.Paragraphs)
    if len(paras) != len(texts):
        raise RuntimeError("paragraph count mismatch: %d vs %d" % (len(paras), len(texts)))
    for i, p in enumerate(paras):
        fmt_para(p, flow[i][0])

    for idx, kind, b in seq:
        marker = "@IMG%d@" % idx
        if kind == "img":
            img = os.path.abspath(b.get("path", ""))
            if os.path.exists(img):
                add_box(doc, cell, marker, img=img, width=float(b.get("width", 290)))
            else:
                add_box(doc, cell, marker, height=float(b.get("height", 180)),
                        hint="（截图缺失：" + os.path.basename(img) + "）")
        else:
            add_box(doc, cell, marker,
                    height=float(b.get("height", 180)),
                    hint=b.get("hint", "（在此处粘贴截图）"))

    summary = job.get("summary") or []
    if summary:
        scell = t.Cell(6, 2)
        try:
            scell.VerticalAlignment = 0
        except Exception:
            pass
        set_cell_text(scell, summary, chunk=20)
        for p in list(scell.Range.Paragraphs):
            fmt_para(p, "body")


def new_word():
    try:
        w = win32.gencache.EnsureDispatch("Word.Application")
    except Exception:
        w = win32.Dispatch("Word.Application")
    w.Visible = False
    w.DisplayAlerts = 0
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    a = ap.parse_args()
    with open(a.job, encoding="utf-8") as fh:
        job = json.load(fh)

    template = os.path.abspath(job["template"])
    out = os.path.abspath(job["out"])
    pdf = os.path.abspath(job["pdf"]) if job.get("pdf") else None
    if not os.path.exists(template):
        sys.exit("template not found: " + template)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    flow, texts, seq = build_flow(job)

    last = None
    for attempt in range(1, 4):
        shutil.copyfile(template, out)
        word = doc = None
        try:
            word = new_word()
            doc = word.Documents.Open(out)
            fill_document(doc, job, flow, texts, seq)
            if out.lower().endswith(".docx"):
                doc.SaveAs2(out, FileFormat=16)
            else:
                doc.Save()
            if pdf:
                os.makedirs(os.path.dirname(pdf), exist_ok=True)
                doc.ExportAsFixedFormat(pdf, 17)
            print("report:", out)
            if pdf:
                print("preview:", pdf)
            return
        except Exception as exc:
            last = exc
            print("[retry %d] %s" % (attempt, exc), file=sys.stderr)
            time.sleep(3)
        finally:
            try:
                if doc is not None:
                    doc.Close(False)
            except Exception:
                pass
            try:
                if word is not None:
                    word.Quit()
            except Exception:
                pass
    sys.exit("Word COM failed after 3 attempts: %s" % last)


if __name__ == "__main__":
    main()

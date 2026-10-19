#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump a Word lab-report template's table/cell structure (Windows, Word COM).

    python inspect_doc.py --doc "C:/.../template.doc" [--json out.json]

Requires Microsoft Word and pywin32 (pip install pywin32).
"""
import argparse
import json
import os
import sys
import time

import win32com.client as win32


def row_cells(table, ri):
    try:
        return list(table.Rows(ri).Cells)
    except Exception:
        return [c for c in table.Range.Cells if c.RowIndex == ri]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()

    path = os.path.abspath(a.doc)
    if not os.path.exists(path):
        sys.exit("file not found: " + path)

    def new_word():
        try:
            w = win32.gencache.EnsureDispatch("Word.Application")
        except Exception:
            w = win32.Dispatch("Word.Application")
        w.Visible = False
        w.DisplayAlerts = 0
        return w

    info = {"doc": path, "tables": []}
    doc = None
    err = None
    for _ in range(3):
        try:
            word = new_word()
            doc = word.Documents.Open(path, ReadOnly=True)
            break
        except Exception as exc:
            err = exc
            time.sleep(3)
    if doc is None:
        sys.exit("Word COM failed: %s" % err)
    try:
        info["pages"] = doc.ComputeStatistics(2)
        ps = doc.Sections(1).PageSetup
        info["page"] = {
            "width": round(ps.PageWidth, 1), "height": round(ps.PageHeight, 1),
            "top": round(ps.TopMargin, 1), "bottom": round(ps.BottomMargin, 1),
            "left": round(ps.LeftMargin, 1), "right": round(ps.RightMargin, 1),
        }
        footers = []
        for fi in (1, 2, 3):
            try:
                f = doc.Sections(1).Footers(fi)
                txt = f.Range.Text.strip()
                if txt:
                    footers.append(txt)
            except Exception:
                pass
        info["footers"] = footers

        for ti in range(1, doc.Tables.Count + 1):
            t = doc.Tables(ti)
            tb = {"index": ti, "rows": t.Rows.Count, "cols": t.Columns.Count, "cells": []}
            widths = []
            for ci in range(1, t.Columns.Count + 1):
                try:
                    widths.append(round(t.Columns(ci).Width, 1))
                except Exception:
                    widths.append(None)
            tb["col_widths"] = widths
            for ri in range(1, t.Rows.Count + 1):
                for c in row_cells(t, ri):
                    rng = c.Range
                    txt = rng.Text.replace("\r\x07", "").replace("\x07", "").replace("\r", "")
                    tb["cells"].append({
                        "row": c.RowIndex,
                        "col": c.ColumnIndex,
                        "text": txt.strip(),
                        "font": str(rng.Font.Name),
                        "size": round(float(rng.Font.Size), 1),
                        "bold": int(rng.Font.Bold),
                        "align": int(rng.ParagraphFormat.Alignment),
                    })
            info["tables"].append(tb)
    finally:
        try:
            doc.Close(False)
        except Exception:
            pass
        try:
            word.Quit()
        except Exception:
            pass

    pretty = json.dumps(info, ensure_ascii=False, indent=2)
    print(json.dumps(info, ensure_ascii=True, indent=2))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            fh.write(pretty)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dump a lab instruction .docx and extract its embedded images.

Preferred invocation (paths inside a UTF-8 JSON file, avoids the Windows
console's non-ASCII argument mangling):

    # inspect.json  {"docx": "C:/.../实验3.docx", "outdir": "C:/.../_work/lab3"}
    python inspect_lab_doc.py --job inspect.json

Also accepts positional arguments when paths are ASCII:

    python inspect_lab_doc.py lab3.docx -o .\\lab3

Outputs:
    <outdir>/lab_dump.txt      paragraphs + tables, with <IMG> markers
    <outdir>/media/*           embedded images in document order
"""

import argparse
import json
import os
import re
import zipfile

import docx


def dump(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    document = docx.Document(path)
    lines = [f"FILE: {path}", ""]

    for index, para in enumerate(document.paragraphs):
        has_image = "graphic" in para._p.xml
        text = para.text.strip()
        if text or has_image:
            marker = " <IMG>" if has_image else ""
            lines.append(f"[{index}] {para.style.name}{marker} :: {text}")

    for table_index, table in enumerate(document.tables):
        lines.append("")
        lines.append(
            f"=== TABLE {table_index} rows={len(table.rows)} cols={len(table.columns)} ==="
        )
        for row_index, row in enumerate(table.rows):
            for cell_index, cell in enumerate(row.cells):
                text = " | ".join(
                    p.text.strip() for p in cell.paragraphs if p.text.strip()
                )
                if text:
                    lines.append(f"  r{row_index}c{cell_index}: {text}")

    dump_path = os.path.join(outdir, "lab_dump.txt")
    with open(dump_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    media_dir = os.path.join(outdir, "media")
    os.makedirs(media_dir, exist_ok=True)
    extracted = []
    with zipfile.ZipFile(path) as archive:
        media = [n for n in archive.namelist() if n.startswith("word/media/")]
        media.sort(key=_natural_key)
        for name in media:
            target = os.path.join(media_dir, os.path.basename(name))
            with archive.open(name) as src, open(target, "wb") as dst:
                dst.write(src.read())
            extracted.append(os.path.basename(name))

    print(f"paragraphs: {len(document.paragraphs)}")
    print(f"tables:     {len(document.tables)}")
    print(f"images:     {len(extracted)} -> {media_dir}")
    print(f"dump:       {dump_path}")


def _natural_key(name):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", name)
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", nargs="?", help="lab instruction .docx")
    parser.add_argument("-o", "--outdir", default=None, help="output directory")
    parser.add_argument("--job", help="UTF-8 JSON file with {docx, outdir}")
    args = parser.parse_args()

    outdir = args.outdir
    docx_path = args.docx
    if args.job:
        with open(args.job, encoding="utf-8") as handle:
            job = json.load(handle)
        docx_path = docx_path or job.get("docx")
        outdir = outdir or job.get("outdir")

    if not docx_path:
        parser.error("需要 docx 路径，或在 --job 文件中提供 docx")
    if not outdir:
        outdir = os.path.splitext(os.path.abspath(docx_path))[0] + "_inspect"

    dump(docx_path, outdir)


if __name__ == "__main__":
    main()

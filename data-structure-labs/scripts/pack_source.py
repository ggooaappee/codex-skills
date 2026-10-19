#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zip source files only (no report, no screenshots, no personal data).

    python pack_source.py --job pack.json

pack.json:
{
  "out":  "C:/.../outputs/112320250050-傅俊豪-实验1源代码.zip",
  "root": "112320250050-傅俊豪-实验1源代码",
  "src":  "C:/.../src",
  "files": ["exp1.h", "exp1.c", "exp2.1.h", "exp2.1.1.c", "exp2.1.2.c", "exp2.1.3.c", "exp2.1.4.c"]
}
"""
import argparse
import json
import os
import sys
import zipfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    a = ap.parse_args()
    with open(a.job, encoding="utf-8") as fh:
        job = json.load(fh)

    src = os.path.abspath(job["src"])
    out = os.path.abspath(job["out"])
    root = job.get("root") or os.path.splitext(os.path.basename(out))[0]
    files = job.get("files") or sorted(f for f in os.listdir(src)
                                       if f.endswith((".c", ".h")))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        os.remove(out)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in files:
            p = os.path.join(src, n)
            if not os.path.exists(p):
                sys.exit("missing source file: " + p)
            z.write(p, root + "/" + n)

    with zipfile.ZipFile(out) as z:
        bad = z.testzip()
    print("zip:", out, os.path.getsize(out), "bytes",
          "| integrity:", "OK" if bad is None else "BAD")


if __name__ == "__main__":
    main()

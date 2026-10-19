#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile and run C lab programs with GCC and print the real output.

    python run_c.py --dir "C:/.../src"
    python run_c.py --dir "C:/.../src" --files exp1.c exp2.1.1.c
    python run_c.py --dir "C:/.../src" --gcc "C:/w64devkit/bin/gcc.exe"

Each .c file is compiled on its own (they each carry their own main) and run
with empty stdin, so the printed output is exactly what the report may quote.
"""
import argparse
import os
import shutil
import subprocess
import sys


def find_gcc(explicit):
    if explicit:
        return explicit
    found = shutil.which("gcc")
    if found:
        return found
    for cand in (r"C:\w64devkit\bin\gcc.exe",
                 os.path.expanduser(r"~\w64devkit\bin\gcc.exe")):
        if os.path.exists(cand):
            return cand
    sys.exit("gcc not found; pass --gcc <path> or install a C toolchain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--gcc")
    a = ap.parse_args()

    src = os.path.abspath(a.dir)
    gcc = find_gcc(a.gcc)
    files = a.files or sorted(f for f in os.listdir(src) if f.endswith(".c"))
    if not files:
        sys.exit("no .c files in " + src)

    build = os.path.join(src, "_build")
    os.makedirs(build, exist_ok=True)
    failed = False
    for name in files:
        stem = os.path.splitext(name)[0]
        exe = os.path.join(build, stem + ".exe")
        print("=" * 60)
        print("[compile]", name)
        cp = subprocess.run([gcc, "-Wall", "-o", exe, name],
                            cwd=src, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        if cp.stdout.strip():
            print(cp.stdout.strip())
        if cp.stderr.strip():
            print(cp.stderr.strip())
        if cp.returncode != 0 or not os.path.exists(exe):
            print("[FAILED]", name)
            failed = True
            continue
        print("[run]", stem + ".exe")
        rp = subprocess.run([exe], cwd=src, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        print(rp.stdout, end="" if rp.stdout.endswith("\n") else "\n")
        if rp.stderr.strip():
            print("[stderr]", rp.stderr.strip())
        if rp.returncode != 0:
            print("[exit]", rp.returncode)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Search the course code-pattern library without loading every file into context."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def default_library() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "code-library" / "patterns"


def title_for(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def matching_lines(text: str, terms: list[str], radius: int = 3) -> str:
    lines = text.splitlines()
    selected: set[int] = set()
    lower_terms = [term.lower() for term in terms]

    for index, line in enumerate(lines):
        lower = line.lower()
        if any(term in lower for term in lower_terms):
            start = max(0, index - radius)
            stop = min(len(lines), index + radius + 1)
            selected.update(range(start, stop))

    chunks: list[list[str]] = []
    current: list[str] = []
    last_index = -2
    for index in sorted(selected):
        if index != last_index + 1 and current:
            chunks.append(current)
            current = []
        current.append(lines[index])
        last_index = index
    if current:
        chunks.append(current)

    return "\n...\n".join("\n".join(chunk) for chunk in chunks[:3])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("terms", nargs="*", help="Chinese or English search terms")
    parser.add_argument("--library", type=Path, default=default_library())
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--list", action="store_true", dest="list_files")
    args = parser.parse_args()

    library = args.library.resolve()
    if not library.is_dir():
        parser.error(f"Library directory not found: {library}")

    files = sorted(library.glob("*.md"))
    if args.list_files:
        for path in files:
            print(f"{path.name}\t{title_for(path)}")
        return 0

    if not args.terms:
        parser.error("Provide at least one search term, or use --list")

    scored: list[tuple[int, Path, str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        score = sum(lower.count(term.lower()) for term in args.terms)
        if score:
            scored.append((score, path, text))

    scored.sort(key=lambda item: (-item[0], item[1].name))
    if not scored:
        print("No matching pattern.")
        return 1

    for score, path, text in scored[: args.limit]:
        print(f"\n## {title_for(path)} ({path.name}, score={score})")
        print(matching_lines(text, args.terms))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

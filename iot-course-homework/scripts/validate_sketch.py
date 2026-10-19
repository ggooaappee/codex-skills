#!/usr/bin/env python3
"""Static checks for course-style Arduino sketches."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


PIN_NAME = re.compile(
    r"(PIN|^LED$|KEY|BUZZER|SDA|SCL|TRIG|ECHO|MOTOR|SERVO|SIC_|WATER|MIC|"
    r"STATUS|OUTPUT|TEMP|DATA|LS_)",
    re.IGNORECASE,
)

DEFINE_RE = re.compile(
    r"^\s*#define\s+([A-Za-z_]\w*)\s+([AD]?\d+)\s*(?://.*)?$",
    re.MULTILINE,
)
CONST_RE = re.compile(
    r"\b(?:const\s+)?(?:int|byte|uint8_t)\s+([A-Za-z_]\w*)\s*=\s*([AD]?\d+)\s*;",
    re.IGNORECASE,
)


def strip_comments_and_literals(text: str) -> str:
    result: list[str] = []
    index = 0
    state = "code"
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if state == "code":
            if char == "/" and next_char == "/":
                state = "line_comment"
                result.extend("  ")
                index += 2
                continue
            if char == "/" and next_char == "*":
                state = "block_comment"
                result.extend("  ")
                index += 2
                continue
            if char == '"':
                state = "string"
                result.append(" ")
                index += 1
                continue
            if char == "'":
                state = "char"
                result.append(" ")
                index += 1
                continue
            result.append(char)
            index += 1
            continue

        if state == "line_comment":
            result.append("\n" if char == "\n" else " ")
            if char == "\n":
                state = "code"
            index += 1
            continue

        if state == "block_comment":
            if char == "*" and next_char == "/":
                state = "code"
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if state in {"string", "char"}:
            if char == "\\":
                result.extend("  ")
                index += 2
                continue
            delimiter = '"' if state == "string" else "'"
            if char == delimiter:
                state = "code"
            result.append("\n" if char == "\n" else " ")
            index += 1

    return "".join(result)


def normalize_pin(value: str) -> str:
    upper = value.upper()
    if upper.startswith("D") and upper[1:].isdigit():
        return upper[1:]
    return upper


def collect_pins(text: str) -> dict[str, list[tuple[str, int]]]:
    pins: dict[str, list[tuple[str, int]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()

    for match in list(DEFINE_RE.finditer(text)) + list(CONST_RE.finditer(text)):
        name = match.group(1)
        if not PIN_NAME.search(name):
            continue
        if name.upper() in {"NUM_LEDS", "BRIGHTNESS"}:
            continue
        pair = (name, match.group(2))
        if pair in seen:
            continue
        seen.add(pair)
        pins[normalize_pin(match.group(2))].append((name, match.start()))
    return pins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sketch", type=Path)
    args = parser.parse_args()

    path = args.sketch
    if not path.is_file():
        parser.error(f"Sketch not found: {path}")

    raw = path.read_text(encoding="utf-8")
    code = strip_comments_and_literals(raw)
    errors: list[str] = []
    warnings: list[str] = []

    for opening, closing, label in [("{", "}", "braces"), ("(", ")", "parentheses"), ("[", "]", "brackets")]:
        if code.count(opening) != code.count(closing):
            errors.append(f"Unbalanced {label}: {code.count(opening)} opening, {code.count(closing)} closing")

    setup_count = len(re.findall(r"\bvoid\s+setup\s*\([^)]*\)\s*\{", code))
    loop_count = len(re.findall(r"\bvoid\s+loop\s*\([^)]*\)\s*\{", code))
    if setup_count != 1:
        errors.append(f"Expected one void setup(), found {setup_count}")
    if loop_count != 1:
        errors.append(f"Expected one void loop(), found {loop_count}")

    if re.search(r"[“”‘’]", code):
        errors.append("Curly quotation marks found; C++ requires straight quotes")

    if "IRremote.h" in raw:
        warnings.append("Old IRremote API detected; verify the installed IRremote version")
    for dependency in ("OLED.h", "DS18B20.h", "DHT12.h", "RFID_SIC.h", "SoftwareWire.h", "ADXL345.h"):
        if f"<{dependency}>" in raw or f'"{dependency}"' in raw:
            warnings.append(f"Course dependency required: {dependency}")

    pins = collect_pins(raw)
    for pin, declarations in sorted(pins.items()):
        if len(declarations) < 2:
            continue
        names = ", ".join(name for name, _ in declarations)
        warnings.append(f"{pin} is assigned to multiple names: {names}")

    if re.search(r"\bFastLED\b", raw) and "BUZZER" in raw and "A0" in raw:
        errors.append("RGB FastLED and BUZZER both appear with A0; check the course pin conflict")
    if re.search(r"\bServo\b", raw) and re.search(r"motorPin\s*=\s*10", raw):
        errors.append("Servo and DC motor both use D10")
    if "Servo2_PIN" in raw and "SIC_MOSI" in raw and "11" in raw:
        errors.append("Servo2 and RFID MOSI both appear to use D11")

    print(f"Checked: {path}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        return 1
    print("Static checks passed." if not warnings else "Static checks passed with warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

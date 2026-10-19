---
name: iot-fundamentals
description: Complete or troubleshoot Arduino-based 物联网基础作业 using the supplied course code library, including component selection, pin-conflict checks, sketch validation, wiring notes, and explicit GitHub publishing. Do not use for routing or switching lab reports.
---

# IoT Fundamentals

Use the course-derived code patterns as the primary source. Turn an assignment prompt and any attached code or screenshots into a runnable Arduino sketch, a short wiring note, and a test summary.

## Required Context

Read only the files needed for the current assignment:

- Pattern index: `assets/code-library/patterns/index.md`
- Pin and conflict table: `assets/code-library/patterns/pin-map.md`
- Matching module files in `assets/code-library/patterns/`
- Combined examples: `assets/code-library/patterns/integration-recipes.md`
- Detailed workflow: `references/assignment-workflow.md`
- Validation checklist: `references/validation-checklist.md`
- GitHub procedure, only when publishing was requested: `references/github-publishing.md`

Search without loading all patterns:

```bash
python scripts/find_pattern.py "温度 RGB"
python scripts/find_pattern.py --list
```

## Workflow

1. Read the assignment and distinguish requirements from explanatory or copied course text.
2. Translate the prompt into inputs, processing rules, outputs, timing, and constraints.
3. Identify the hardware modules and open the matching pattern files.
4. Check pin conflicts before writing code. Never silently combine modules that use the same pin.
5. Compose one sketch with one `setup()` and one `loop()`. Reuse course includes, APIs, thresholds, and helper functions.
6. Keep user-provided code and requested naming unless they prevent correct behavior.
7. Run `python scripts/validate_sketch.py <sketch.ino>`.
8. Compile with Arduino CLI when the board core and course libraries are available. Otherwise state that only static validation was possible.
9. Deliver the `.ino`, a concise `README.md`, and a `接线说明.md` when wiring matters.

## Non-Negotiable Checks

- Do not invent APIs for `OLED.h`, `DS18B20.h`, `DHT12.h`, `ADXL345.h`, `RFID_SIC.h`, or `SoftwareWire.h`.
- Do not claim hardware behavior was tested unless it actually was.
- Do not place two `setup()` or `loop()` functions in one sketch.
- Treat buttons as active-low when using the course `INPUT_PULLUP` patterns.
- Preserve sensor units and the distinction between ADC values, computed lux, temperature, and humidity.
- Flag `A3`, `A0`, `D10`, and `D11` reuse explicitly when modules are combined.
- Use course-faithful code first, then make clearly marked corrections for known typos or unsafe conflicts.

## Publishing

Upload only when the user explicitly asks. The known target repository is selected from the current thread or GitHub authentication, not guessed. Follow `references/github-publishing.md`, avoid committing course PPTX files or personal data, and report the commit and remote URL after a successful push.

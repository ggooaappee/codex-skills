# Validation Checklist

## Structure

- One `setup()` and one `loop()`
- Balanced braces, parentheses, and brackets
- Straight quotes in C++ strings
- All course and third-party dependencies declared

## Pins

- RGB data on the selected pin, normally `A0`
- Button and sensor logic match the actual active level
- No simultaneous use of one physical pin by incompatible modules
- PWM outputs use PWM-capable pins
- Motors and servos use suitable drivers and power

## Behavior

- Thresholds and comparison directions match the assignment
- Counts, intervals, and return-to-home behavior match the request
- OLED row/column positions fit an 8x16 font
- Sensor values are checked for warm-up, timeout, or invalid reads when relevant
- The loop does not block critical inputs for an excessive time

## Delivery

- Sketch filename matches its folder
- README states functional coverage and unverified risks
- Wiring note lists only the pin assignments needed by this assignment
- No personal data, secrets, or copyrighted course files are included

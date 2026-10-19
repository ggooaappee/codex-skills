# WS2812B RGB 彩灯

来源：第5次课件第7至14页。

## 依赖与初始化

```cpp
#include <FastLED.h>

#define NUM_LEDS 3
#define LED_PIN A0
#define BRIGHTNESS 64

CRGB leds[NUM_LEDS];

void setupRGB() {
  delay(100);
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}
```

## 设置单灯颜色

```cpp
void SET_RGB(int index, char color) {
  if (color == 'R') leds[index] = CRGB::Red;
  if (color == 'G') leds[index] = CRGB::Green;
  if (color == 'B') leds[index] = CRGB::Blue;
  if (color == 'Y') leds[index] = CRGB::Yellow;
  if (color == 'W') leds[index] = CRGB::White;
  if (color == 'D') leds[index] = CRGB::Black;
  FastLED.show();
}
```

## 闪烁

```cpp
void Flash_RGB(int index, char color, int times, int intervalMs) {
  leds[index] = CRGB::Black;
  for (int i = 0; i < times; i++) {
    if (color == 'R') leds[index] = CRGB::Red;
    if (color == 'G') leds[index] = CRGB::Green;
    if (color == 'B') leds[index] = CRGB::Blue;
    if (color == 'Y') leds[index] = CRGB::Yellow;
    FastLED.show();
    delay(intervalMs);
    leds[index] = CRGB::Black;
    FastLED.show();
    delay(intervalMs);
  }
}
```

## 常见作业映射

```cpp
if (conditionHigh) {
  SET_RGB(1, 'R');
} else if (conditionLow) {
  SET_RGB(1, 'B');
} else {
  SET_RGB(1, 'G');
}
```

## 作业复用要点

- 课件主要使用中间灯 `leds[1]`，也有综合页使用 `leds[0]`，按题目要求的灯位置选择。
- RGB 数据引脚为 `A0`。
- 只修改颜色而不调用 `FastLED.show()` 不会立即显示。
- 不要把蜂鸣器也分配到 `A0`。

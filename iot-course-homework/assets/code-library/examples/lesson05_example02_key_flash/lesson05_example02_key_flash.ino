#include <OLED.h>
#include "FastLED.h"

#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64

// 第5次课件第4页电路图：KEY1=D2，KEY2=D6。
#define KEY1 2
#define KEY2 6

OLED myOLED;
CRGB leds[NUM_LEDS];

void SET_RGB(int m, char c)
{
  if (c == 'R') leds[m] = CRGB::Red;
  if (c == 'G') leds[m] = CRGB::Green;
  if (c == 'B') leds[m] = CRGB::Blue;
  if (c == 'Y') leds[m] = CRGB::Yellow;
  if (c == 'W') leds[m] = CRGB::White;
  if (c == 'D') leds[m] = CRGB::Black;
  FastLED.show();
}

void Flash_RGB(int m, char c, int n, int finv)
{
  int i;
  leds[m] = CRGB::Black;
  for (i = 0; i < n; i++) {
    if (c == 'R') leds[m] = CRGB::Red;
    if (c == 'G') leds[m] = CRGB::Green;
    if (c == 'B') leds[m] = CRGB::Blue;
    if (c == 'Y') leds[m] = CRGB::Yellow;
    FastLED.show();
    delay(finv);
    leds[m] = CRGB::Black;
    FastLED.show();
    delay(finv);
  }
}

void setup()
{
  delay(100);
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  myOLED.begin(FONT_8x16);
  myOLED.clearScreen();
  myOLED.println("Ex2 RGB KEY");

  // 课件未展示按键初始化，这里按低电平有效按键补充上拉输入。
  pinMode(KEY1, INPUT_PULLUP);
  pinMode(KEY2, INPUT_PULLUP);
}

void loop()
{
  int BnState = digitalRead(KEY1);
  if (BnState == 0) {
    delay(500);
    Flash_RGB(1, 'R', 3, 1000);
  }

  BnState = digitalRead(KEY2);
  if (BnState == 0) {
    delay(500);
    Flash_RGB(2, 'B', 7, 200);
  }
}

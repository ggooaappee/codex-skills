#include <OLED.h>
#include "FastLED.h"

#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64

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
  myOLED.println("Ex3 Traffic Light");
}

void loop()
{
  SET_RGB(0, 'R');
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 1====");
  myOLED.println("1R");
  delay(3000);

  SET_RGB(0, 'D');
  Flash_RGB(1, 'Y', 7, 200);
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 2====");
  myOLED.println("Flash Y");
  delay(200);

  SET_RGB(2, 'G');
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 3====");
  myOLED.println("3G");
  delay(5000);

  SET_RGB(2, 'D');
}

#include <OLED.h>
#include "FastLED.h"

#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64

OLED myOLED;
CRGB leds[NUM_LEDS];

void setup()
{
  delay(100); // power-up safety delay
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  myOLED.begin(FONT_8x16);
  myOLED.clearScreen();
  myOLED.println("Ex1-4-0 RGB");
  myOLED.println("XXX");
}

void loop()
{
  leds[0] = CRGB::DarkRed;
  leds[1] = CRGB::DarkGreen;
  leds[2] = CRGB::DarkBlue;
  FastLED.show();
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 1====");
  myOLED.println("1DR;2DG;3DB");
  delay(1000);

  leds[0] = CRGB::Red;
  leds[1] = CRGB::Black;
  leds[2] = CRGB::Black;
  FastLED.show();
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 2====");
  myOLED.println("1R");
  delay(2000);

  leds[0] = CRGB::Black;
  leds[1] = CRGB::Green;
  leds[2] = CRGB::Black;
  FastLED.show();
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 3====");
  myOLED.println("2G");
  delay(1000);

  leds[0] = CRGB::Black;
  leds[1] = CRGB::Black;
  leds[2] = CRGB::Blue;
  FastLED.show();
  myOLED.setPosi(4,0);
  myOLED.println("====STEP 4====");
  myOLED.println("3B");
  delay(1000);
}

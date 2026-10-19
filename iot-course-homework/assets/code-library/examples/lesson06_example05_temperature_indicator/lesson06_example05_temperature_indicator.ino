#include <OneWire.h>
#include <DS18B20.h>
#include <OLED.h>
#include <FastLED.h>

#define Temp_PIN A3
#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64

DS18B20 ds;
OLED myOLED;
CRGB leds[NUM_LEDS];

float STempMax = 30; // 温度上限
float STempMin = 26; // 温度下限

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

void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);

  delay(100); // 上电稳定延时
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  myOLED.print("T1:");
  myOLED.print(STempMax);
  myOLED.print("T2:");
  myOLED.println(STempMin);
}

void loop()
{
  float temp = ds.readTemperature();
  myOLED.setPosi(2,0);
  myOLED.print("Temp.: ");
  myOLED.print(temp);
  myOLED.println(" *C");

  if (temp > STempMax)
    SET_RGB(1, 'R');
  else if (temp < STempMin)
    SET_RGB(1, 'B');
  else
    SET_RGB(1, 'G');
}

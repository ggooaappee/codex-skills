#include <OLED.h>
#include <OneWire.h>
#include <DS18B20.h>

#define Temp_PIN A3

OLED myOLED;
DS18B20 ds;

void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);
}

void loop()
{
  float temp = ds.readTemperature();
  if (temp < 125 && temp > 5)
  {
    myOLED.setPosi(4,0);
    myOLED.print("Temp.: ");
    myOLED.print(temp);
    myOLED.println(" *C");
  }
}

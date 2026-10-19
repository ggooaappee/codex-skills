#include <OLED.h>
#include <OneWire.h>
#include <DS18B20.h>

#define Temp_PIN A3
#define LED 3

OLED myOLED;
DS18B20 ds;
float Set_Temp = 29.5;

void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);

  pinMode(LED, OUTPUT);
  myOLED.print("Set_Temp:");
  myOLED.println(Set_Temp);
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

    myOLED.setPosi(6,0);

    //========Smart Processing=============
    if (temp > Set_Temp)
      digitalWrite(LED, HIGH);
    else
      digitalWrite(LED, LOW);
  }
}

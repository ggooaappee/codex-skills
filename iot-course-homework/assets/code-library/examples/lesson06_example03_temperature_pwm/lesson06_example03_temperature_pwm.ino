#include <OLED.h>
#include <OneWire.h>
#include <DS18B20.h>

#define Temp_PIN A3
#define LED 3

OLED myOLED;
DS18B20 ds;

float STempMax = 32; // 设置温度的上限
float STempMin = 29; // 根据环境需求可以调整

void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);

  pinMode(LED, OUTPUT);
  myOLED.print("T1:");
  myOLED.print(STempMax);
  myOLED.print("T2:");
  myOLED.println(STempMin);
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

    //========Smart Processing=============
    // map(value, fromLow, fromHigh, toLow, toHigh)
    int duty = map(temp, STempMin, STempMax, 0, 255);
    myOLED.setPosi(6,0);
    myOLED.print("Duty: ");

    if (temp > STempMax)
      digitalWrite(LED, HIGH);
    else if (temp < STempMin)
      digitalWrite(LED, LOW);
    else
      analogWrite(LED, duty);
  }
}

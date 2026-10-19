# 第6次 温度传感器：原始代码段

来源：`第6次 温度传感器.pptx`

## 第7页：DS18B20 声明、初始化和读取

```cpp
//-------Declare-Temp Sensor DS18B20-------------
#include <OneWire.h>
#include <DS18B20.h>
DS18B20 ds;
#define Temp_PIN A3

// setup()
ds.begin(Temp_PIN);

// 读取温度值
float temp = ds.readTemperature();
```

## 第8页：例1 温度显示器声明与初始化

```cpp
//-------Declare-OLED--------------------
#include <OLED.h>
OLED myOLED;

//-------Declare-Temp Sensor DS18B20-------------
#include <OneWire.h>
#include <DS18B20.h>
DS18B20 ds;
#define Temp_PIN A3

void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);
}
```

## 第9页：例1 温度显示

```cpp
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
```

## 第10页：例2 温度开关新增声明与初始化

```cpp
//-------Declare-LED1W-MD1----------------------
#define LED 3
float Set_Temp = 29.5;

void setup()
{
  pinMode(LED, OUTPUT);
  myOLED.print("Set_Temp:");
  myOLED.println(Set_Temp);
}
```

本页是在例1基础上增加，原页没有重复展示 `ds.begin()` 和 `myOLED.begin()`。

## 第11页：例2 温度开关处理

```cpp
void loop()
{
  myOLED.setPosi(6,0); // 修改显示位置

  //========Smart Processing=============
  if (temp > Set_Temp)
    digitalWrite(LED, HIGH);
  else
    digitalWrite(LED, LOW);
}
```

本页只展示新增处理。独立运行时要保留例1中的温度读取和显示。

## 第12页：例3 温度 PWM 控制器新增内容

```cpp
float STempMax = 32; // 设置温度的上限
float STempMin = 29; // 根据环境需求可以调整

void setup()
{
  myOLED.print("T1:");
  myOLED.print(STempMax);
  myOLED.print("T2:");
  myOLED.println(STempMin);
}
```

本页是在例2基础上增加。

## 第13页：例3 温度 PWM 控制

```cpp
void loop()
{
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
```

课件只输出 `"Duty: "` 标签，没有继续输出 `duty` 数值。原始提取保留这一写法，未擅自修改。

## 第14页：例4 温度报警器

课件没有提供完整代码，只给出以下任务：

```text
温度高于 30 度时蜂鸣器响。
提示：增加蜂鸣器的声明、初始化。
```

## 第16页：例5 温度指示器处理逻辑

```cpp
if (temp > STempMax)
  SET_RGB(1, 'R');
else if (temp < STempMin)
  SET_RGB(1, 'B');
else
  SET_RGB(1, 'G');
```

例5的文字要求为：

```text
高于 30 度：红色
低于 26 度：蓝色
26 到 30 度之间：绿色
```

因此例5应使用 `STempMax = 30`、`STempMin = 26`。

## 第18页：综合代码声明

```cpp
#include <OLED.h>
OLED myOLED;

#include <OneWire.h>
#include <DS18B20.h>
#define Temp_PIN A3
DS18B20 ds;

#define LED 3
float STempMin = 20;
float STempMax = 60;

#define BUZZER A0
void BEEP(int n, int finv);

#include <FastLED.h>
#define NUM_LEDS 3
#define LED_PIN A0
#define BRIGHTNESS 64
CRGB leds[NUM_LEDS];
void SET_RGB(int n, int c);
```

冲突提示：`BUZZER` 和 `LED_PIN` 都定义为 `A0`，不能按原样同时使用。

## 第19页：综合代码初始化

```cpp
void setup()
{
  ds.begin(Temp_PIN);
  myOLED.begin(FONT_8x16);
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}
```

## 第20页：综合代码主程序

```cpp
void loop()
{
  float temp = ds.readTemperature();
  myOLED.setPosi(2,0);
  myOLED.print(temp);

  if (temp > STempMax) {
    SET_RGB(0, 'R');
    BEEP(1, 300);
    delay(5000);
  }
  else if (temp < STempMin)
    SET_RGB(0, 'B');
  else
    SET_RGB(0, 'G');
}
```

本页的 `STempMin = 20`、`STempMax = 60` 是综合代码示例值，不是例5要求的 `26`、`30`。

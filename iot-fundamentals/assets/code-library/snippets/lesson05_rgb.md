# 第5次 RGB彩灯：原始代码段

来源：`第5次 RGB彩灯.pptx`

本文件按幻灯片顺序保存代码，不把不同页面的代码强行拼接。代码截图中的程序已转录为可复制文本。

## 第7页：RGB LED 声明与初始化

```cpp
//----------Declare-RGB LED WS2812Driver ------------
#include "FastLED.h"
#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64
CRGB leds[NUM_LEDS];

void setup()
{
  delay( 100 ); // power-up safety delay
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness( BRIGHTNESS );
}
```

## 第8页：例1 声明

```cpp
//-------Declare-OLED-------------------
#include <OLED.h>
OLED myOLED;

//----------Declare-RGB LED WS2812Driver ------------
#include "FastLED.h"
#define NUM_LEDS    3
#define LED_PIN     A0
#define BRIGHTNESS  64
CRGB leds[NUM_LEDS];
```

## 第9页：例1 初始化

```cpp
void setup()
{
  delay( 100 ); // power-up safety delay
  FastLED.addLeds<WS2812B, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness( BRIGHTNESS );

  myOLED.begin(FONT_8x16);
  myOLED.clearScreen();
  myOLED.println("Ex1-4-0 RGB");
  myOLED.println("XXX");
}
```

## 第10页：例1 设置灯的颜色

本页代码来自两张代码截图，按左到右顺序转录。

```cpp
// 截图 1
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

// 截图 2
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
```

## 第11页：SET_RGB() 函数

```cpp
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
```

课件中的弯引号已改为 C++ 可用的直引号。

## 第12页：Flash_RGB() 函数

```cpp
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
```

## 第13页：例2 按键控制闪灯

```cpp
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
```

课件写作 `Loop()`，C++ 标准入口应为 `void loop()`。

课件没有在此页定义 `KEY1`、`KEY2`。按第4页电路图，二者分别为 `D2`、`D6`。

## 第14页：例3 红绿灯

```cpp
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
```

本页代码来自代码截图。`delay(200)` 按截图原样保留。

# 雨滴传感器

来源：第15次课件第6至10页。

## 声明与初始化

```cpp
const int waterInPin = A3;
int waterState = 0;

void setupRainSensor() {
  pinMode(waterInPin, INPUT);
  digitalWrite(waterInPin, HIGH);
}
```

## 读取状态

```cpp
waterState = !digitalRead(waterInPin);
myOLED.setPosi(4, 0);
myOLED.print("Water = ");
myOLED.println(waterState);
```

## 模拟自动雨刮

```cpp
#include <Servo.h>
Servo myservo1;
#define Servo1_PIN 10

if (waterState == 1) {
  myservo1.write(90);
  delay(500);
  myservo1.write(0);
  delay(500);
} else {
  myservo1.write(0);
  delay(500);
}
```

## 作业复用要点

- 雨滴模块和浮球液位开关都使用“读取后取反”的课件写法。
- 第15次例2、例3为自由练习，可用 LED 或蜂鸣器替换舵机输出。
- 电位器可调节模块上的数字触发阈值。

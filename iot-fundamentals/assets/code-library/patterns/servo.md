# 舵机

来源：第10次课件第7至18页。

## 声明与初始化

```cpp
#include <Servo.h>

#define Servo1_PIN 10
#define Servo2_PIN 11

Servo myservo1;
Servo myservo2;

void setupServos() {
  myservo1.attach(Servo1_PIN);
  myservo2.attach(Servo2_PIN);
  myservo1.write(0);
  myservo2.write(0);
}
```

## 单舵机分步旋转

```cpp
myservo1.write(30);
delay(1000);
myservo1.write(60);
delay(1000);
myservo1.write(90);
delay(1000);
myservo1.write(180);
delay(1000);
myservo1.write(0);
```

## 平滑旋转函数

```cpp
void MoterMove(int motorNo, int startVal, int endVal, int intervalMs) {
  for (int value = startVal; value <= endVal; value++) {
    if (motorNo == 1) myservo1.write(value);
    if (motorNo == 2) myservo2.write(value);
    delay(intervalMs);
  }
}
```

函数名 `MoterMove` 是课件原拼写，保留以兼容课件。

## 多舵机协同

```cpp
void SetMTPos(int x, int y) {
  myservo1.write(x);
  myservo2.write(y);
}
```

## 作业复用要点

- 角度范围按 `0..180` 处理。
- `D10` 与直流电机共用，`D11` 与 RFID MOSI 共用，组合模块时必须检查冲突。
- 舵机供电不足会导致复位或抖动，代码正确不代表 USB 供电足够。

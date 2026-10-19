# 步进电机

来源：第11次课件第6至11页。

## 声明与初始化

```cpp
#include <Stepper.h>

const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 9, 10, 11, 12);

void setupStepper() {
  myStepper.setSpeed(80);
  Serial.begin(9600);
}
```

`1.8°` 步进电机通常每圈约 `200` 步。

## 正反转

```cpp
myStepper.step(stepsPerRevolution);   // 正转一圈
myStepper.step(-stepsPerRevolution);  // 反转一圈
```

## 模拟量调速

```cpp
int sensorReading = analogRead(A0);
int motorSpeed = map(sensorReading, 0, 1023, 0, 100);

if (motorSpeed > 0) {
  myStepper.setSpeed(motorSpeed);
  myStepper.step(stepsPerRevolution / 100);
}
```

## 作业复用要点

- 课件前页写 `9,10,11,12`，通用方法页写 `8,9,10,11`，必须按实际接线二选一。
- `setSpeed()` 只设速度，不产生转动，必须调用 `step()`。
- 步进电机需要驱动板，不能把线圈直接接到 Arduino 引脚。

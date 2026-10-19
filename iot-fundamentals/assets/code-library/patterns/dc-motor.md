# 直流电机

来源：第12次课件第6至8页。

## 声明与初始化

```cpp
const int motorPin = 10;

void setupDCMotor() {
  pinMode(motorPin, OUTPUT);
  analogWrite(motorPin, 0);
}
```

## 控制转速

```cpp
analogWrite(motorPin, 250);  // 开
analogWrite(motorPin, 0);    // 关
```

## 按键控制

```cpp
if (digitalRead(KEY1) == 0) {
  analogWrite(motorPin, 250);
  myOLED.print("state:ON");
}

if (digitalRead(KEY2) == 0) {
  analogWrite(motorPin, 0);
  myOLED.print("state:OFF");
}
```

## 作业复用要点

- `motorPin=10` 是 PWM 输出。
- 多数直流电机需要驱动模块，不能直接接 Arduino 引脚。
- 与舵机 1 共用 `D10`。

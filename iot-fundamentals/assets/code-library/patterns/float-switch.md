# 浮球液位开关

来源：第13次课件第5至10页。

## 声明与初始化

```cpp
const int waterInPin = 5;
int waterState = 0;

void setupFloatSwitch() {
  pinMode(waterInPin, INPUT);
  digitalWrite(waterInPin, HIGH);
}
```

## 读取状态

```cpp
waterState = !digitalRead(waterInPin);
myOLED.setPosi(2, 0);
myOLED.print("WATER = ");
myOLED.println(waterState);
```

## 水位控制电机或报警

```cpp
if (waterState == 1) {
  analogWrite(motorPin, 0);
} else {
  analogWrite(motorPin, 200);
}
```

## 作业复用要点

- 课件通过取反得到 `waterState`，不要再次反转，除非实际浮球方向相反。
- 水位报警器页要求自行补充蜂鸣器，可直接调用 `Beep(1, 300)`。
- 状态 `1` 与 `0` 对应“高/低”的实际方向取决于传感器安装朝向，应通过串口或 OLED 实测确认。

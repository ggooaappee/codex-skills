# 光照度传感器

来源：第8次课件第8至14页。

## 声明与初始化

```cpp
#define LS_PIN A3

void setupLightSensor() {
  pinMode(LS_PIN, INPUT);
}

int readLightLevel() {
  return analogRead(LS_PIN);
}
```

## 显示光照值

```cpp
int LSVal = analogRead(LS_PIN);
myOLED.setPosi(4, 0);
myOLED.print("LS:");
myOLED.println(LSVal);
delay(500);
```

## 光照开关

```cpp
#define LED 3
int Set_LS = 200;

if (LSVal > Set_LS) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}
```

## 光照 PWM

```cpp
int Set_LSMax = 400;
int Set_LSMin = 50;
int duty = map(LSVal, Set_LSMax, Set_LSMin, 0, 255);

if (LSVal < Set_LSMin) {
  digitalWrite(LED, HIGH);
  myOLED.print("255");
} else if (LSVal > Set_LSMax) {
  digitalWrite(LED, LOW);
  myOLED.print("0");
} else {
  analogWrite(LED, duty);
  myOLED.print(duty);
}
```

## 作业复用要点

- 返回值为 Arduino `0..1023` 的 ADC 值，不是标准 lux。
- 课件第14页使用反向映射 `Set_LSMax -> Set_LSMin`，按题目硬件亮暗方向决定是否反转。
- 光照模块代码引脚是 `A3`。

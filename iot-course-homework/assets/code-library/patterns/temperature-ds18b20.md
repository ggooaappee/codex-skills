# DS18B20 温度传感器

来源：第6次课件第7至20页。

## 依赖、声明与初始化

```cpp
#include <OneWire.h>
#include <DS18B20.h>

#define Temp_PIN A3
DS18B20 ds;

void setupTemperature() {
  ds.begin(Temp_PIN);
}

float readTemperatureC() {
  return ds.readTemperature();
}
```

## 显示温度

```cpp
float temp = ds.readTemperature();
if (temp > 5 && temp < 125) {
  myOLED.setPosi(4, 0);
  myOLED.print("Temp.: ");
  myOLED.print(temp);
  myOLED.println(" *C");
}
```

## 温度开关

```cpp
#define LED 3
float Set_Temp = 29.5;

if (temp > Set_Temp) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}
```

## 温度 PWM

```cpp
float STempMax = 32;
float STempMin = 29;
int duty = map(temp, STempMin, STempMax, 0, 255);

if (temp > STempMax) {
  digitalWrite(LED, HIGH);
} else if (temp < STempMin) {
  digitalWrite(LED, LOW);
} else {
  analogWrite(LED, duty);
}
```

## 温度指示器

```cpp
float STempMax = 30;
float STempMin = 26;

if (temp > STempMax) {
  SET_RGB(1, 'R');
} else if (temp < STempMin) {
  SET_RGB(1, 'B');
} else {
  SET_RGB(1, 'G');
}
```

## 温度报警

```cpp
if (temp > 30.0) {
  Beep(1, 300);
  delay(5000);
}
```

## 作业复用要点

- 课程温度范围写作 `-55` 至 `+125°C`，显示示例只接受 `5 < temp < 125`。
- `map()` 的输入是浮点数时会按整数规则截断，用于 PWM 通常可接受。
- 课件综合页的 `STempMin=20`、`STempMax=60` 与例5的 `26`、`30` 不同，以题目阈值为准。

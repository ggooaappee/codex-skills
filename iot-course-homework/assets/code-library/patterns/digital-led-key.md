# LED 与按键

来源：第2次课件第15至21页。

## 基础 Blink

```cpp
#define LED 3

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);
}
```

## 声明与初始化

```cpp
#define LED 3
#define KEY1 2
#define KEY2 6

void setupLEDAndKeys() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  pinMode(KEY1, INPUT_PULLUP);
  pinMode(KEY2, INPUT_PULLUP);
}
```

## 按键控制开和关

```cpp
int ledState = 0;

void updateLEDWithKeys() {
  if (digitalRead(KEY1) == 0) {
    delay(500);
    ledState = 1;
  }

  if (digitalRead(KEY2) == 0) {
    delay(500);
    ledState = 0;
  }

  digitalWrite(LED, ledState ? HIGH : LOW);
}
```

## 单键切换

```cpp
int ledState = 0;
int lastKeyState = HIGH;

void toggleLED() {
  int keyState = digitalRead(KEY1);
  if (lastKeyState == HIGH && keyState == LOW) {
    ledState = !ledState;
    digitalWrite(LED, ledState);
  }
  lastKeyState = keyState;
}
```

课件另有 `delay(500)` 版本，逻辑更简单，但长按会反复触发。

## 自定义闪灯

```cpp
void Flash_LED(int n, int intervalMs) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED, HIGH);
    delay(intervalMs);
    digitalWrite(LED, LOW);
    delay(intervalMs);
  }
}
```

## PWM 呼吸调光

```cpp
void fadeLED(int startValue, int endValue, int stepDelayMs) {
  int step = startValue <= endValue ? 1 : -1;
  for (int value = startValue; value != endValue + step; value += step) {
    analogWrite(LED, value);
    delay(stepDelayMs);
  }
}
```

## 作业复用要点

- 按键为低电平有效，因此判断 `digitalRead(KEYx) == LOW`。
- 使用 `INPUT_PULLUP` 时不要再外接下拉电阻。
- `Blink` 可改用 `millis()` 非阻塞方式，但课件示例使用 `delay()`。

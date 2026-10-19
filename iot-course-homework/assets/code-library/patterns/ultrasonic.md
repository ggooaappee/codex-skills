# 超声波测距

来源：第19次课件第7至9页。

## 声明与初始化

```cpp
int trigPin = A5;
int echoPin = A4;
long duration;
long cm;
long inches;

void setupUltrasonic() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}
```

## 测距

```cpp
digitalWrite(trigPin, LOW);
delayMicroseconds(5);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

duration = pulseIn(echoPin, HIGH);
cm = (duration / 2) / 29.1;
inches = (duration / 2) / 74;

myOLED.setPosi(0, 0);
myOLED.print("Distance: ");
myOLED.println(cm);

Serial.print("Distance: ");
Serial.print(inches);
Serial.print("in, ");
Serial.print(cm);
Serial.println("cm");
```

## 模拟倒车雷达

```cpp
if (cm > 0 && cm < 20) {
  Beep(1, 100);
} else if (cm < 50) {
  Beep(1, 300);
}
delay(250);
```

## 作业复用要点

- 没有回波时 `pulseIn()` 可能返回 0 或超时值，使用前应检查有效范围。
- 声速换算采用 `29.1us/cm`，结果是往返时间除以 2。
- `A4/A5` 与 I2C 传感器冲突。

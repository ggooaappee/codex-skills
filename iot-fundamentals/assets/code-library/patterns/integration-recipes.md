# 组合作业模式

## 温度指示器

使用 `temperature-ds18b20.md`、`oled.md`、`rgb-ws2812b.md`。

```cpp
float t = ds.readTemperature();
if (t > 30) SET_RGB(1, 'R');
else if (t < 26) SET_RGB(1, 'B');
else SET_RGB(1, 'G');
```

## 温度报警器

DS18B20 + OLED + 蜂鸣器：

```cpp
if (temp > 30.0) Beep(1, 300);
```

## 温湿度 RGB 指示

DHT12 + RGB：

```cpp
if (t > Set_temp && h < Set_h) SET_RGB(0, 'R');
else if (t > Set_temp && h > Set_h) SET_RGB(0, 'B');
else SET_RGB(0, 'G');
```

## 自动路灯

光照模块 + LED：

```cpp
int level = analogRead(LS_PIN);
int duty = map(level, Set_LSMax, Set_LSMin, 0, 255);
analogWrite(LED, constrain(duty, 0, 255));
```

## 自动雨刮

雨滴模块 + Servo：

```cpp
if (!digitalRead(waterInPin)) {
  myservo1.write(90);
} else {
  myservo1.write(0);
}
```

## 接近控制舵机

TMD27713 + Servo：

```cpp
ReadProx();
if (proximity > 100) MoterMove(2, 0, 120, 20);
else myservo2.write(0);
```

## 人体感应自动门

PIR + Stepper：

```cpp
if (digitalRead(outputPin) == HIGH) {
  myStepper.step(stepsPerRevolution / 4);
  delay(3000);
  myStepper.step(-stepsPerRevolution / 4);
}
```

## 倒车雷达

超声波 + 蜂鸣器，可再加 RGB：

```cpp
long distance = readDistanceCm();
if (distance < 20) Beep(2, 100);
else if (distance < 50) Beep(1, 150);
```

## ZigBee 温度遥测

发送端：DS18B20 + ZigBee。

```cpp
float temp = ds.readTemperature();
myZigBee.print("T:");
myZigBee.println(temp);
delay(1000);
```

接收端：ZigBee + OLED。

```cpp
if (myZigBee.available()) {
  String message = myZigBee.readStringUntil('\n');
  myOLED.println(message);
}
```

## 组合顺序

1. 列出所有输入、输出和通信模块。
2. 按 `pin-map.md` 检查引脚冲突。
3. 只保留一个 `setup()` 和一个 `loop()`。
4. 把每个模块的初始化放进 `setup()`。
5. 在 `loop()` 中先采集，再判断，再输出，最后设置合理延时。
6. 对需要响应按键的题目，避免被长时间 `delay()` 卡住。

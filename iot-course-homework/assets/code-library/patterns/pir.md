# 人体传感器

来源：第16次课件第6至9页。

## 声明与初始化

```cpp
const int statusPin = A4;
const int outputPin = A5;
#define LED 3

void setupPIR() {
  pinMode(LED, OUTPUT);
  pinMode(statusPin, INPUT);
  pinMode(outputPin, INPUT);
}
```

## 读取并控制 LED

```cpp
int state = digitalRead(statusPin);
int output = digitalRead(outputPin);

myOLED.setPosi(0, 0);
myOLED.print("PIR = ");
myOLED.println(state);

if (output == HIGH) {
  myOLED.println("Detecting");
  digitalWrite(LED, HIGH);
} else {
  myOLED.println("Warm-up");
  myOLED.print("OUT = ");
  myOLED.println(output);
  digitalWrite(LED, LOW);
}

delay(10);
```

## 模拟自动门

```cpp
if (output == HIGH) {
  myStepper.step(stepsPerRevolution / 4);
  delay(3000);
  myStepper.step(-stepsPerRevolution / 4);
}
```

PIR 上电后通常需要预热，刚启动时的检测结果不一定可靠。

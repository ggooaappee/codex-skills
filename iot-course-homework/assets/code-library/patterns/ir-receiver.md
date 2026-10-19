# 红外接收

来源：第20次课件第6至8页。

## 声明与初始化

```cpp
#include <IRremote.h>

const int irReceiverPin = A3;
#define LED 3

IRrecv irrecv(irReceiverPin);
decode_results results;

void setupIR() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  irrecv.enableIRIn();
}
```

## 接收编码并控制 LED

```cpp
if (irrecv.decode(&results)) {
  Serial.print("irCode: ");
  Serial.print(results.value, HEX);
  Serial.print(", bits: ");
  Serial.println(results.bits);
  irrecv.resume();
}

if (results.value == 0xADF3C46F) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}
delay(600);
```

## 作业复用要点

- 课件使用旧版 `IRremote` API。新版库可能改名为 `IRremote.hpp`，对象和中断 API 也不同。
- 遥控器编码因遥控器而异，先通过串口打印 `results.value`，再把实际编码写入判断。
- 接收脚为 `A3`。

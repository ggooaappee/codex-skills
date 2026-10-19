# ZigBee CC2530 透传模块

来源：第21次课件第7至13页。

## 声明与初始化

```cpp
#include <SoftwareSerial.h>

SoftwareSerial myZigBee(A1, A2);  // RX, TX
#define Kit1Channel 12
#define Kit1Panid 0xb217
#define Kit1Addr 0x2001

void setupZigBee() {
  myZigBee.begin(9600);
  Zigbee_setup(Kit1Channel, Kit1Panid, Kit1Addr);
  Serial.begin(9600);
}
```

## 课件配置函数

```cpp
void Zigbee_setup(uint8_t channel, uint16_t panid, uint16_t addr) {
  myZigBee.write(0xAA);
  myZigBee.write(0xC7);
  myZigBee.write(0xBB);
  delay(30);

  myZigBee.write(0xAA);
  myZigBee.write(0xC7);
  myZigBee.write(0x5A);
  myZigBee.write(channel);
  myZigBee.write(panid >> 8);
  myZigBee.write(panid & 0xff);
  myZigBee.write(addr >> 8);
  myZigBee.write(addr & 0xff);
  myZigBee.write(0xBB);
}
```

## 接收命令

```cpp
if (myZigBee.available()) {
  char command = myZigBee.read();
  if (command == '1') {
    digitalWrite(LED, HIGH);
  } else if (command == '2') {
    digitalWrite(LED, LOW);
  }
}
```

## 发送文本

```cpp
myZigBee.print("T:");
myZigBee.println(temp);
```

## 作业复用要点

- 需要两块 Arduino 和两块 ZigBee 模块，发送端和接收端配置必须一致。
- `SoftwareSerial(A1,A2)` 的顺序按课件写为 RX、TX。
- 第21次例2只给提示，可把 DS18B20 温度值用 `print()` 发送。

# RFID

来源：第18次课件第6至9页。

## 依赖、引脚与初始化

```cpp
#include <SPI.h>
#include <SoftwareSPI.h>
#include <RFID_SIC.h>

#define SIC_CS 10
#define SIC_SCK 13
#define SIC_MISO 12
#define SIC_MOSI 11

RFID_SIC sic;

void setupRFID() {
  sic.begin(SIC_CS, SIC_SCK, SIC_MISO, SIC_MOSI);
  sic.sicInit();
}
```

## 读取卡片 UID

```cpp
void readCardUID() {
  sic.sicInit();

  if (sic.ISO14443A_Request() == 1 &&
      sic.ISO14443A_Anticoll(0x93) == 1 &&
      sic.ISO14443A_Select(0x93) == 1) {

    String uid = "";
    for (int i = 0; i < 4; i++) {
      byte value = sic.sicUID[3 - i];
      if (value < 0x10) uid += "0";
      uid += String(value, HEX);
    }

    Serial.print("UID:[0x");
    Serial.print(uid);
    Serial.println("]");
    myOLED.print("UID:[0x");
    myOLED.print(uid);
    myOLED.println("]");
  }
}
```

## 作业复用要点

- 课程库为 `RFID_SIC.h`，API 与常见 MFRC522 库不同。
- 课件使用 10/13/12/11 作为 CS/SCK/MISO/MOSI。
- RFID 的 `D11` 与舵机 2 冲突。
- 课件截图中的 `RFIDCode` 拼接存在重复赋值，容易导致 UID 字符串异常；上例保持相同读取流程，但用 `String` 拼接避免该问题。

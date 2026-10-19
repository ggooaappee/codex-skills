# TMD27713 亮度与接近传感器

来源：第17次课件第6至14页。

## 依赖、声明与初始化

```cpp
#include <SoftwareWire.h>

SoftwareWire tmd;
#define TMD_ADDR 0x39
#define SDA_PIN A4
#define SCL_PIN A5

unsigned int data[6];
float luminance = 0.0;
double proximity = 0;

void setupTMD() {
  tmd.begin(SDA_PIN, SCL_PIN);
  InitProx();
}
```

## 初始化寄存器

```cpp
void InitProx() {
  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x00 | 0xA0);
  tmd.write(0x0F);
  tmd.endTransmission();

  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x01 | 0xA0);
  tmd.write(0xDB);
  tmd.endTransmission();

  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x02 | 0xA0);
  tmd.write(0xFF);
  tmd.endTransmission();

  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x03 | 0xA0);
  tmd.write(0xFF);
  tmd.endTransmission();

  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x0E | 0xA0);
  tmd.write(0x04);
  tmd.endTransmission();

  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x0F | 0xA0);
  tmd.write(0x20);
  tmd.endTransmission();
  delay(800);
}
```

## 读取亮度和接近值

```cpp
void ReadProx() {
  tmd.beginTransmission(TMD_ADDR);
  tmd.write(0x14 | 0xA0);
  tmd.endTransmission();
  tmd.requestFrom(TMD_ADDR, 6);

  if (tmd.available() == 6) {
    for (int i = 0; i < 6; i++) {
      data[i] = tmd.read();
    }
  }

  int c0Data = (data[1] * 256) + data[0];
  int c1Data = (data[3] * 256) + data[2];
  proximity = (data[5] * 256.0) + data[4];

  float CPL = 101.0 / 24.0;
  float luminance1 = (1 * c0Data - 2 * c1Data) / CPL;
  float luminance2 = (0.6 * c0Data - 1.00 * c1Data) / CPL;

  luminance = 0.0;
  if (luminance1 > 0 && luminance1 > luminance2) {
    luminance = luminance1;
  } else if (luminance2 > 0 && luminance2 > luminance1) {
    luminance = luminance2;
  }
}
```

## 显示与应用

```cpp
ReadProx();
myOLED.setPosi(4, 0);
myOLED.print("Lux");
myOLED.println(luminance);
myOLED.print("Prox");
myOLED.println(proximity);

if (luminance > 400) {
  myservo1.write(60);
} else {
  myservo1.write(30);
}

if (proximity > 100) {
  MoterMove(2, 0, 120, 20);
} else {
  myservo2.write(0);
}
```

## 作业复用要点

- 课件使用 `SoftwareWire`，不是普通 `Wire`。
- `luminance` 是课件公式计算结果，不是直接原始 ADC。
- `proximity` 范围在课件中写为约 `0..1023`。

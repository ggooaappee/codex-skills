# ADXL345 三轴加速度传感器

来源：第9次课件第8至17页。

## 声明与初始化

```cpp
#include <ADXL345.h>

#define SDA_PIN A4
#define SCL_PIN A5

ADXL345 adxl;
uint16_t iX, iY, iZ;
char sX, sY, sZ;

void setupADXL() {
  adxl.begin(SDA_PIN, SCL_PIN);
}
```

## 课件读取函数

```cpp
char ADXL_Data[18];

void Read_ADXL345() {
  uint16_t buf[3] = {0, 0, 0};
  uint16_t X0, X1, Y0, Y1, Z1, Z0;

  X0 = adxl.getData(0x32);
  X1 = adxl.getData(0x33);
  buf[0] = (X1 << 8) | X0;

  Y0 = adxl.getData(0x34);
  Y1 = adxl.getData(0x35);
  buf[1] = (Y1 << 8) | Y0;

  Z0 = adxl.getData(0x36);
  Z1 = adxl.getData(0x37);
  buf[2] = (Z1 << 8) | Z0;

  for (int i = 0; i < 3; i++) {
    if ((buf[i] & 0x8000) == 0x8000) {
      buf[i] = 65535 - buf[i];
      ADXL_Data[5 * i] = ' ';
      ADXL_Data[5 * i + 1] = '-';
    } else {
      ADXL_Data[5 * i] = ' ';
      ADXL_Data[5 * i + 1] = '+';
    }
    ADXL_Data[5 * i + 2] = (buf[i] / 100) + '0';
    ADXL_Data[5 * i + 3] = (buf[i] / 10 % 10) + '0';
    ADXL_Data[5 * i + 4] = (buf[i] % 10) + '0';
  }

  ADXL_Data[0] = 'X';
  ADXL_Data[5] = 'Y';
  ADXL_Data[10] = 'Z';

  iX = buf[0];
  iY = buf[1];
  iZ = buf[2];
  sX = ADXL_Data[1];
  sY = ADXL_Data[6];
  sZ = ADXL_Data[11];
}
```

## 显示三轴

```cpp
Read_ADXL345();
myOLED.setPosi(2, 0);
myOLED.print("X=");
myOLED.print(sX);
myOLED.println(iX);
myOLED.print("Y=");
myOLED.print(sY);
myOLED.println(iY);
myOLED.print("Z=");
myOLED.print(sZ);
myOLED.println(iZ);
```

## 手势动作开关 LED

```cpp
#define LED 3
int GXMax = 120;

if (iX > GXMax) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}
```

## 角度 PWM

```cpp
int GXMax = 240;
int GXMin = 30;
int duty = map(iX, GXMax, GXMin, 255, 0);

if (iX > GXMax) {
  digitalWrite(LED, HIGH);
} else if (iX < GXMin) {
  digitalWrite(LED, LOW);
} else {
  analogWrite(LED, duty);
}
```

## 作业复用要点

- I2C 引脚为 `A4=SDA`、`A5=SCL`。
- 课件中的 `iX/iY/iZ` 是处理后正值，符号单独保存在 `sX/sY/sZ`。
- 多个例4、例5只给任务提示，没有完整代码，可把 `SET_RGB()` 或 `Servo.write()` 接到同一个方向判断上。

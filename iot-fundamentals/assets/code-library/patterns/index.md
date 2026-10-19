# 物联网基础课程代码模式库

本库根据第1次至第21次课件整理。二次重复的“第9次 三轴加速度传感器”文件内容完全相同，只保留一份。

## 课程主题

| 次数 | 主题 | 主要硬件 | 代码模式 |
| --- | --- | --- | --- |
| 1 | 物联网概述、平台介绍 | Arduino Nano、课程模块 | 无程序代码 |
| 2 | LED、KEY | LED、按键、OLED | `digital-led-key.md` |
| 3 | 蜂鸣器 | 蜂鸣器、按键 | `buzzer.md` |
| 4 | OLED | OLED | `oled.md` |
| 5 | RGB彩灯 | WS2812B | `rgb-ws2812b.md` |
| 6 | 温度传感器 | DS18B20、OLED、RGB、蜂鸣器 | `temperature-ds18b20.md` |
| 7 | 温湿度传感器 | DHT12 | `temperature-humidity-dht12.md` |
| 8 | 照度传感器 | 模拟光照模块 | `light-sensor.md` |
| 9 | 三轴加速度传感器 | ADXL345 | `accelerometer-adxl345.md` |
| 10 | 舵机 | Servo | `servo.md` |
| 11 | 步进电机 | Stepper | `stepper.md` |
| 12 | 直流电机 | 直流电机模块 | `dc-motor.md` |
| 13 | 浮球液位开关 | 浮球开关 | `float-switch.md` |
| 14 | 麦克风 | 模拟声音模块 | `microphone.md` |
| 15 | 雨滴传感器 | 雨滴模块、Servo | `rain-sensor.md` |
| 16 | 人体传感器 | PIR | `pir.md` |
| 17 | 距离传感器 | TMD27713、Servo | `proximity-tmd27713.md` |
| 18 | RFID | RFID_SIC | `rfid.md` |
| 19 | 超声波测距 | HC-SR04 类模块 | `ultrasonic.md` |
| 20 | 红外接收模块 | IRremote | `ir-receiver.md` |
| 21 | ZigBee | CC2530、SoftwareSerial | `zigbee.md` |

## 使用顺序

1. 先读 `pin-map.md`，确认题目所需模块的课件引脚和冲突。
2. 打开对应模块文件，复制声明、初始化和读取/控制函数。
3. 在 `integration-recipes.md` 中查找相同或相近的组合。
4. 只写一个 `setup()` 和一个 `loop()`，把各模块初始化合并到 `setup()`。
5. 按题目阈值、输出方式和延时重写 `loop()`，不要直接拼接多个完整示例。

## 代码来源说明

- 标记为“课件代码”的片段来自幻灯片文本或代码截图。
- 对课件中的明显笔误，库中会保留“课件原样”提示，并给出可编译修正。
- 课程私有库 `OLED.h`、`DS18B20.h`、`DHT12.h`、`SoftwareSPI.h`、`RFID_SIC.h`、`ADXL345.h`、`SoftwareWire.h` 必须使用课程配套版本。

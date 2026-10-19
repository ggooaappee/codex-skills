# Arduino 物联网课程代码库

本代码库由第1次至第21次课件中的代码段和代码截图整理而成，供 `iot-course-homework` skill 完成课程作业时检索和组合。

## 结构

| 目录 | 内容 |
| --- | --- |
| `patterns/` | 按硬件模块整理的声明、初始化、读取、控制和组合模式 |
| `snippets/` | 已逐页转录的第5次 RGB、第6次温度传感器原始代码段 |
| `examples/` | 可直接放入 Arduino IDE 的拼装示例 |
| `manifest.json` | 课程、模块模式与示例索引 |

## 已覆盖课程

1. 物联网概述、平台介绍
2. LED、KEY
3. 蜂鸣器
4. OLED
5. RGB彩灯
6. 温度传感器 DS18B20
7. 温湿度传感器 DHT12
8. 照度传感器
9. 三轴加速度传感器 ADXL345
10. 舵机
11. 步进电机
12. 直流电机
13. 浮球液位开关
14. 麦克风
15. 雨滴传感器
16. 人体传感器
17. 距离与亮度传感器 TMD27713
18. RFID
19. 超声波测距
20. 红外接收
21. ZigBee

两份“第9次 三轴加速度传感器”课件内容完全相同，整理时只计算一次。

## 主要依赖

- `FastLED`
- `Servo`
- `Stepper`
- `OneWire`
- `DS18B20`
- `DHT12`
- `ADXL345`
- `SoftwareWire`
- `SoftwareSPI`
- `RFID_SIC`
- `IRremote`
- `OLED`

其中 `OLED.h`、`DS18B20.h`、`DHT12.h`、`ADXL345.h`、`SoftwareWire.h`、`SoftwareSPI.h`、`RFID_SIC.h` 通常来自课程配套环境。

## 使用顺序

1. 查 `patterns/index.md`。
2. 查对应模块文件。
3. 查 `patterns/pin-map.md` 检查引脚冲突。
4. 查 `patterns/integration-recipes.md` 找相近组合。
5. 用 `scripts/validate_sketch.py` 做静态校验。

## 内容边界

课件只提供任务提示、没有给出完整代码的练习不会被虚构为标准答案。代码截图转录会注明来源页，并对明显笔误单独标注。

# OLED

来源：第4次课件第7至11页。

## 声明与初始化

```cpp
#include <OLED.h>

OLED myOLED;

void setupOLED() {
  myOLED.begin(FONT_8x16);
  myOLED.clearScreen();
}
```

`FONT_8x16` 显示 8 行、每行约 16 个字符；`FONT_6x8` 可以显示更多字符。

## 输出

```cpp
myOLED.setPosi(2, 0);
myOLED.print("Temp.: ");
myOLED.print(25.6);
myOLED.println(" C");
```

`setPosi(row, column)` 的第一个参数是行，第二个参数是列。

## 绘图

```cpp
myOLED.circleDraw(64, 40, 10);
myOLED.boxDraw(30, 30, 96, 60);
myOLED.drawLine(1, 20, 127, 63);
```

## 作业复用要点

- `print()` 不换行，`println()` 换行。
- 每轮循环都从固定 `setPosi()` 位置开始覆盖输出，可避免内容乱跑。
- OLED 占用课程 SPI 接口 `D4,D7,D8,D9`。

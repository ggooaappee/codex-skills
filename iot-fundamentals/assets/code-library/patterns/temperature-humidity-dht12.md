# DHT12 温湿度传感器

来源：第7次课件第6至13页。

## 依赖、声明与初始化

```cpp
#include <DHT12.h>

#define DATA_PIN A3
DHT12 dht;

void setupDHT() {
  dht.begin(DATA_PIN);
}
```

课件注释说也可以替换为 `<DHT11.h>`，但给出的对象和 API 是 `DHT12 dht`。

## 读取并显示

```cpp
float h = dht.readHumidity();
float t = dht.readTemperature();

myOLED.setPosi(2, 0);
myOLED.print("Humidity:");
myOLED.println(h);
myOLED.print("Temp.:");
myOLED.println(t);
delay(1000);
```

## 温湿度阈值控制

```cpp
#define LED 3
#define BUZZER_PIN A3
int Set_temp = 30;
int Set_h = 70;

if (t > Set_temp) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}

if (h > Set_h) {
  digitalWrite(BUZZER_PIN, HIGH);
} else {
  digitalWrite(BUZZER_PIN, LOW);
}
```

课件该页写作 `#define BUZZER A0`，但按课程板引脚表蜂鸣器应为 `A3`；若同时使用 DHT12 的 `A3`，实际接线必须按实验板重新确认。

## 温湿度控制 RGB

```cpp
if (t > Set_temp && h < Set_h) {
  SET_RGB(0, 'R');
} else if (t > Set_temp && h > Set_h) {
  SET_RGB(0, 'B');
} else {
  SET_RGB(0, 'G');
}
```

RGB 的声明、初始化和 `SET_RGB()` 见 `rgb-ws2812b.md`。

## 作业复用要点

- 第7次课件标题页误写为“第6次”，文件名和课程进度是第7次。
- DHT12 与 DS18B20 不是同一种驱动，不能混用头文件。
- 温湿度读取后通常需要约 `1s` 的采样间隔。

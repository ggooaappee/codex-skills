# 麦克风

来源：第14次课件第5至8页。

## 声明与初始化

```cpp
#define MIC_PIN A3
const int sampleWindow = 50;
unsigned int sample;
float MIC_Val;

void setupMicrophone() {
  pinMode(MIC_PIN, INPUT);
}
```

## 读取峰值

```cpp
void Read_MIC() {
  unsigned int peakToPeak = 0;
  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;
  unsigned long startMillis = millis();

  while (millis() - startMillis < sampleWindow) {
    sample = analogRead(MIC_PIN);
    if (sample < 1024) {
      if (sample > signalMax) {
        signalMax = sample;
      } else if (sample < signalMin) {
        signalMin = sample;
      }
    }
  }

  peakToPeak = signalMax - signalMin;
  MIC_Val = peakToPeak / 10.0;
}
```

## 声控开关

```cpp
#define LED 3
float MIC_Min = 30;

Read_MIC();
if (MIC_Val > MIC_Min) {
  digitalWrite(LED, HIGH);
} else {
  digitalWrite(LED, LOW);
}
```

## 作业复用要点

- 输出是相对声音强度，不是经过校准的分贝值。
- `sampleWindow=50ms` 代表约 `20Hz` 的更新频率。
- 调试阈值时先通过 OLED 或串口观察安静环境和触发时的数值。

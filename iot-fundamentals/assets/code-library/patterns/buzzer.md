# 蜂鸣器

来源：第3次课件第6至15页。

## 初始化

```cpp
#define BUZZER_PIN A3

void setupBuzzer() {
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
}
```

## 按次数鸣叫

```cpp
void Beep(int n, int intervalMs) {
  for (int i = 0; i < n; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(intervalMs);
    digitalWrite(BUZZER_PIN, LOW);
    delay(intervalMs);
  }
}
```

## 播放指定频率

```cpp
void toneOnce(unsigned int frequency, unsigned long durationMs) {
  tone(BUZZER_PIN, frequency, durationMs);
}

void stopTone() {
  noTone(BUZZER_PIN);
}
```

常用频率来自课件第15页：

| 音名 | 频率 Hz |
| --- | --- |
| Do | 262 |
| Re | 294 |
| Mi | 330 |
| Fa | 349 |
| Sol | 392 |
| La | 440 |
| Si | 494 |

## 作业复用要点

- 无源蜂鸣器优先使用 `tone()`。
- 用 `Beep()` 时，`intervalMs` 同时决定亮/响和停顿。
- 第6次综合代码把 `BUZZER` 写成 `A0`，与 RGB 冲突；本库按第3次接线页使用 `A3`。

# Codex Skills

个人 Codex 技能集合。三个课程技能彼此独立，按任务领域分开安装和调用。

## 技能列表

| 技能 | 适用任务 | 不适用 |
| --- | --- | --- |
| [routing-switching-technology](routing-switching-technology/) | 路由与交换技术课程、eNSP 实验、VLAN/STP/MSTP 等配置与 Word 实验报告 | Arduino、传感器、IoT 作业 |
| [iot-fundamentals](iot-fundamentals/) | Arduino 物联网基础作业、课件代码、传感器/执行器组合、接线说明 | 路由交换命令、eNSP 拓扑、网络实验报告 |
| [data-structure-labs](data-structure-labs/) | 数据结构（C 语言）实验报告、顺序表/链表等算法、GCC 编译运行、套用 Word 模板 | 路由交换实验、Arduino 物联网作业 |

## routing-switching-technology

把「实验指导书 + 截图」生成格式统一的路由与交换技术实验报告。

主要内容：

- eNSP 拓扑、设备名、接口和 IP 一致性检查
- 按指导书原编号整理实验步骤
- 写入配置命令、截图、图注和结果分析
- docx → PDF → PNG 渲染检查

调用示例：

> 用 `$routing-switching-technology` 完成实验四的 STP/MSTP 报告，指导书和截图在桌面。

安装：

```powershell
Copy-Item -Recurse .\codex-skills\routing-switching-technology "$env:USERPROFILE\.codex\skills\"
```

## iot-fundamentals

根据第1至21次 Arduino 物联网课件代码库完成基础课程作业。

主要内容：

- LED、按键、OLED、RGB 和蜂鸣器
- 温度、湿度、光照、加速度、声音、雨滴、人体、距离和液位传感器
- 舵机、步进电机和直流电机
- RFID、红外和 ZigBee
- 引脚冲突检查、Sketch 静态检查和接线说明

调用示例：

> 用 `$iot-fundamentals` 完成“温度高于 30°C 红灯、低于 26°C 蓝灯、其余绿灯”的作业。

安装：

```powershell
Copy-Item -Recurse .\codex-skills\iot-fundamentals "$env:USERPROFILE\.codex\skills\"
```

## data-structure-labs

按教材与教师给定接口实现数据结构算法，编译运行后把运行截图填进课程 Word 模板，源代码单独打包。

主要内容：

- 读取 `.doc` 实验报告模板的表格、单元格与字体结构
- 顺序表基本操作，以及倒置、奇偶拆分、分类存储、有序归并（李云清《数据结构（C 语言版）》第 4 版口径）
- GCC 编译运行，报告只引用真实输出
- 报告以截图为主、文字从简；截图框与图注保持同页
- 源代码单独打 zip，报告另存 `.doc` 与预览 PDF

环境要求：Windows + Microsoft Word + `pywin32`，以及 PATH 中的 `gcc`（或 `--gcc` 指定）。

调用示例：

> 用 `$data-structure-labs` 完成实验1 的顺序表报告，模板、代码和截图都在附件里。

安装：

```powershell
Copy-Item -Recurse .\codex-skills\data-structure-labs "$env:USERPROFILE\.codex\skills\"
```

## 目录边界

```text
codex-skills/
├── routing-switching-technology/
│   ├── SKILL.md
│   ├── assets/实验报告模板.docx
│   ├── references/template-format.md
│   └── scripts/
├── iot-fundamentals/
│   ├── SKILL.md
│   ├── assets/code-library/
│   ├── references/
│   └── scripts/
└── data-structure-labs/
    ├── SKILL.md
    ├── assets/实验报告模板.doc
    ├── references/
    │   ├── template-format.md
    │   ├── algorithms-seqlist.md
    │   └── github-publishing.md
    └── scripts/
        ├── inspect_doc.py
        ├── fill_report.py
        ├── run_c.py
        └── pack_source.py
```

三个技能不共享入口文件、默认提示或输出模板。按课程选择对应 skill，避免生成错误类型的作业。

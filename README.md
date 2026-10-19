# Codex Skills

个人的 Codex 技能集合。每个技能是一个独立文件夹，按 Codex skill 规范组织（`SKILL.md` + 可选资源）。

## 技能列表

| 技能 | 说明 |
|---|---|
| [lab-report-builder](lab-report-builder/) | 实验报告生成：读取实验指导书与截图，套用既有报告模板，生成 Word 报告并转 PDF 校验排版 |
| [iot-course-homework](iot-course-homework/) | 物联网课程作业：基于第1至21次课件代码库完成 Arduino 程序、接线说明和静态校验 |

## lab-report-builder

把「实验指导书 + 截图」变成一份格式统一、可直接提交的 Word 实验报告，适用于 eNSP 网络实验（VLAN、STP、MSTP 等）及同类课程报告。

**工作流**

1. 拆解实验指导书：拓扑、需求、步骤编号、命令、要提交的截图
2. 清点截图：设备名、命令、关键输出、对应哪条需求
3. 一致性核对：`display` 回显是否支持正文结论，设备名/接口/IP 是否一致
4. 生成报告：克隆模板、按 `report.json` 重建正文、更新表头与总结
5. 渲染检查：docx → PDF → 逐页 PNG，检查分页、图注、字号
6. 交付：产物路径、待补项、做过的假设

**目录结构**

```text
lab-report-builder/
├── SKILL.md                        # 工作流与硬性要求
├── agents/openai.yaml              # UI 元数据
├── assets/
│   ├── 实验报告模板.docx            # 空白模板（已去掉个人信息）
│   └── 实验指导书/                  # 实验 2、实验 3 指导书原件
├── references/template-format.md   # 模板结构、字号、图宽、常见排版问题
└── scripts/
    ├── inspect_lab_doc.py          # 导出指导书段落与内嵌图片
    ├── build_report.py             # 克隆模板、重建正文（report.json）
    └── render_report.ps1           # docx → PDF → 逐页 PNG
```

## 给同学用

### iot-course-homework

根据课件中的 LED、按键、OLED、RGB、传感器、电机、RFID、红外和 ZigBee 代码，组合完成新的物联网课程作业。

```powershell
Copy-Item -Recurse .\codex-skills\iot-course-homework "$env:USERPROFILE\.codex\skills\"
```

用法示例：

> 用 `$iot-course-homework` 根据课件代码完成“温度高于 30°C 时红灯、低于 26°C 时蓝灯、其余时间绿灯”的作业，并把程序、接线说明和检查结果放到一个文件夹。

主要资源：

- `assets/code-library/patterns/`：按模块整理的代码模式
- `assets/code-library/patterns/pin-map.md`：课件引脚表与冲突
- `scripts/find_pattern.py`：按关键词检索代码模式
- `scripts/validate_sketch.py`：检查单 `setup/loop`、括号、弯引号和常见引脚冲突

### lab-report-builder

1. 克隆仓库并安装技能：

```powershell
git clone https://github.com/ggooaappee/codex-skills.git
Copy-Item -Recurse .\codex-skills\lab-report-builder "$env:USERPROFILE\.codex\skills\"
```

2. 用 `lab-report-builder\assets\实验报告模板.docx` 作为空白模板，不需要先做一份旧报告。
3. 在 `report.json` 里填自己的信息：

```json
"student": {"class": "网络工程1班", "id": "你的学号", "name": "你的姓名"},
"date": "2026.10.26"
```

4. 把指导书和截图给 Codex，说：用 `$lab-report-builder` 完成实验X报告。

> 仓库是私有的，克隆/下载需要仓库权限。

## 安装

把技能文件夹复制到 Codex 的 skills 目录：

```powershell
Copy-Item -Recurse .\lab-report-builder "$env:USERPROFILE\.codex\skills\"
```

之后即可用 `$lab-report-builder` 调用。

## 依赖

- Python 3 + `python-docx`
- Microsoft Word（docx → PDF）
- Poppler `pdftoppm`（PDF → PNG）

## 用法示例

> 用 `$lab-report-builder` 完成实验四的报告，指导书和截图在桌面。

## 说明

- 仓库为私有；`references/template-format.md` 中保留了带个人学号/姓名的模板示例。
- 每个技能文件夹可以独立复制使用。

---
name: lab-report-builder
description: 生成或补全课程实验报告 Word 文档：读取实验指导书与截图，套用已有实验报告模板，按实验步骤写入配置命令、截图、图注与结果分析，并转 PDF 渲染检查排版。用于 eNSP 网络实验报告（VLAN、STP、MSTP 等）及同类的课程报告。
---

# 实验报告生成工作流

把「实验指导书 + 截图」变成一份格式统一、图文对应、可直接提交的 Word 实验报告。

## 输入

1. 实验指导书（.docx，含拓扑、实验需求、步骤）
2. 截图（文件夹、剪贴板图片或微信图片）
3. 上一份实验报告 .docx 作为格式模板（同课程任意一份即可）
4. 学生信息与报告日期（写进 `report.json` 的 `student` / `date`）

没有模板时先向用户要；截图不全时只写能证实的部分，其余标注「待补充」，不要编造结果。
同学直接使用仓库自带的 `assets/实验报告模板.docx`（空白模板）即可，不需要先做一份旧报告。

## 工作流

### 1. 拆解实验文件

在工作目录写 `inspect.json`（UTF-8）：

```json
{"docx": "C:/Users/.../实验3 STP-MSTP.docx", "outdir": "C:/Users/.../_work/lab3"}
```

```bash
python scripts/inspect_lab_doc.py --job inspect.json
```

整理出：拓扑（设备、接口、IP、VLAN）、需求与步骤的**原始编号和措辞**、每一步要交的截图、指导书给出的命令。
指导书里的命令可以直接引用；**不要自创步骤或改动编号**。

### 2. 清点截图

用 `view_image` 逐张看，记录每张的：设备名、执行命令、关键输出、能证明哪条需求。
按文件名时间戳或用户说明判断拍摄顺序；归属不确定的图注要在交付时请用户确认。
缺图列成清单，不要用理论结果代替截图。

### 3. 一致性核对

- `display vlan` / `display mux-vlan` / `display stp brief` 等回显是否支持正文结论
- 设备名、IP、接口号是否与截图完全一致（注意 `fjh_sw1` 与 `fjh-sw1` 这类差异）
- 学生配置与指导书要求冲突时（例如要求 Hybrid、实际是 Trunk）先指出，不要默默写成符合要求

发现矛盾先告诉用户，再决定是改配置重截，还是如实说明。

### 4. 生成报告

1. 按 `references/template-format.md` 写 `report.json`：`template` 指向上一次报告或 `assets/实验报告模板.docx`，`out` 指向 `学号姓名实验X.题目.docx`，另含 `student`（班级/学号/姓名）、`date`、`title`、`summary` 和 `blocks`（h1 / head / body / cmd / img / cap 六种块）
3. 运行：

```bash
python scripts/build_report.py --job report.json
```

脚本会清空并重建正文单元格，同时更新报告日期、实验题目和实验总结。

### 5. 渲染检查

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/render_report.ps1 -Job render.json
```

`render.json`：`{"docx": "...", "outdir": "...", "pdftoppm": "..."}`。

逐页看 PNG，检查：分页是否合理（别让「成绩」单独占一页）、图注是否紧跟图片且编号连续、截图文字是否可读、命令块缩进是否正确、正文与截图结论是否一致。

必要时调图片宽度，或在 `report.json` 里加 `"row4_min_twips": 630` 压缩正文行高。

### 6. 交付

说明：产物路径与页数、已覆盖的步骤、待补项、做过的假设（日期、图注归属、拓扑图来源）。

## 硬性要求

- 步骤编号与指导书一致，不额外增加实验步骤。
- 不编造数据：时延、丢包率、序号只写截图里看得到的；丢包数用序号差算（seq 20 之后到 seq 38，即丢 17 个）。
- 每张图都有图注，正文按图号引用。
- 沿用模板的中文字体与页面设置：标题黑体、正文仿宋 10.5、命令 Consolas 8.5、图注仿宋 9 居中。

## 环境注意

- Python 优先用 `mcp__codex_app__load_workspace_dependencies` 返回的运行时；否则用 `$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`。
- 控制台默认按本地代码页解码，中文输出会显示成 `ʵ��3`。看输出前先执行 `$env:PYTHONIOENCODING='utf-8'` 或 `[Console]::OutputEncoding=[Text.Encoding]::UTF8`；路径参数本身是正常的。
- 路径统一写进 UTF-8 的 JSON 作业文件，命令行只传 `--job`，既避免引号转义问题，也方便下次复用。
- 含中文路径的 `.ps1` 必须保存为 **UTF-8 with BOM**，否则 Windows PowerShell 5.1 会按 ANSI 读取导致路径乱码。
- 不要对计算出来的路径做递归删除；渲染输出用新目录。
- 合并单元格：正文是 `tables[0].rows[4].cells[1]`，`cells[1..3]` 指向同一个 `tc`。

## 资源

- `references/template-format.md` — 模板结构、字号、图宽与常见排版问题
- `assets/实验报告模板.docx` — 空白实验报告模板（同学可直接使用）
- `assets/实验指导书/` — 实验 2、实验 3 的指导书原件（示例）
- `scripts/inspect_lab_doc.py` — 导出指导书段落与内嵌图片
- `scripts/build_report.py` — 克隆模板并重建正文
- `scripts/render_report.ps1` — docx → PDF → 逐页 PNG

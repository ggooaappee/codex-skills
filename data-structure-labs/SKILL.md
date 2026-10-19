---
name: data-structure-labs
description: 生成或补全数据结构（C 语言）课程实验报告：按教材与教师给定接口实现顺序表/链表等算法，用 GCC 编译运行真实程序，套用课程 Word 模板填入学号信息、运行截图与简要说明，并打包源代码。仅用于数据结构实验报告，不处理路由交换实验或 Arduino 物联网作业。
---

# 数据结构实验报告

把「作业要求 + 教师提供的模板与代码」变成一份可提交的实验报告：算法要能编译运行，报告要套用原模板，截图与结果一一对应。

## 输入

1. 作业要求：要实现的算法、测试程序、提交要求。
2. 教师文件：`.doc` 实验报告模板、`exp*.h`、`exp*.c`（接口和测试 `main()` 通常已给定）。
3. 学生信息：班级、学号、姓名、报告日期。
4. 截图：学生自己运行的代码/结果截图。没有截图时插入带提示文字的虚线框，并告诉学生怎么补拍。

缺信息先问。不要编造运行结果、测试数据或成绩。

## 依赖

- Windows + Microsoft Word（用 COM 读写 `.doc`）。
- Python 3.9+ 与 `pip install pywin32`。
- GCC 在 PATH 中，或用 `--gcc` 指定；没有时可解压便携版 w64devkit。

## 工作流

1. **拆解要求**：区分作业要求与模板里的说明文字，列出要实现的函数和要交的测试。
2. **读模板结构**：`python scripts/inspect_doc.py --doc <模板.doc>`，确认表格行数、单元格映射和字体。仰恩大学模板见 `references/template-format.md`。
3. **写代码**：按教材《数据结构（C 语言版）》（李云清，第 4 版，人民邮电出版社）的算法思路实现，保持教师给定接口不变。顺序表参考实现见 `references/algorithms-seqlist.md`。
4. **编译运行**：`python scripts/run_c.py --dir <源码目录>`。必须真实编译、真实运行、贴真实输出；禁止凭想象写结果。
5. **填报告**：写 `report.json`，运行 `python scripts/fill_report.py --job report.json`，生成 `.doc` 和预览 PDF。
6. **校验排版**：把 PDF 渲染成 PNG 逐页看：图片与图注是否同页、有无跨页大空白、表格是否被挤断。
7. **打包**：`python scripts/pack_source.py --job pack.json`，只打源代码。
8. **交付**：报告 `.doc` + 预览 `.pdf` + 源代码 `.zip` 放进 `outputs`。

## 硬性检查

- 教师提供的测试 `main()` 是评分依据，不要为了迁就头文件原型去改它；应调整头文件接口并在报告中说明。例：`exp1.c` 调用 `del(&L,i,&e)`，就把 `del` 写成带输出参数的三参函数，与 `exp2.1.h` 的 `delete` 一致。
- 源文件按 GBK（代码页 936）保存，中文注释在 Dev-C++/MSVC 下才不乱码。
- 模板里的 `int insert(SeqList *slt, int i, ElemType x,)` 多一个逗号，是待修正的语法错误。
- `if(ei%2) i++;` 后面不能再多写分号，否则后续 `else break;` 会报 "'else' without a previous 'if'"。
- 不要改动模板表格结构与字号，只在单元格里填内容。
- 报告从简：每个算法 1 行标题 + 截图 + 图注即可，不写大段算法说明。
- 运行结果必须来自真实执行；截图必须来自学生自己的运行环境。

## Word 操作要点

- 用 Word COM（pywin32）读写 `.doc`；给 `Cell.Range.Text` 赋值会替换内容但保留单元格。
- 单元格内的截图框用嵌套 1×1 表格：行高规则设为"最小值"，图片宽 290–316 pt，0.5 pt 灰边框。
- 嵌套表格不会出现在 `Document.Tables` 中，只能通过 `Cell.Range.Tables` 或按段落文本查找标记。
- 模板行高常是"最小值"，会给内容留出空白：先对整个表设置 `Row.HeightRule = 0`（自动）。
- 图片与图注用 `KeepWithNext` 链保持同页；单元格末尾的空段落设成 4–6 pt 行高可收紧间距。

## 发布

仅在用户明确要求时推送。目标仓库取当前线程指定或 `gh auth status` 的账号，不要猜。流程见 `references/github-publishing.md`；仓库只放技能与空白模板，不要放带学号姓名的成品报告。

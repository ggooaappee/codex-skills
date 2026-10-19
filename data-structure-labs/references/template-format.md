# 实验报告模板结构（仰恩大学 / 数据结构）

课程模板为 `.doc`（Word 97-2003 二进制），一张 8 行 4 列的表格，页面 A4，上下边距 72 pt、左右 90 pt，页脚居中「仰恩大学」。

## 单元格映射

| 行 | 列 | 内容 | 字体 |
| --- | --- | --- | --- |
| 1 | 合并 4 列 | 数据结构实验报告（标题） | 黑体 22 pt 加粗居中 |
| 2 | 1–4 | 班  级 / 学  号 / 姓  名 / 报告日期（标签） | 黑体 12 pt 居中 |
| 3 | 1–4 | 班级 / 学号 / 姓名 / 日期（填写值） | 仿宋 10.5 pt 居中 |
| 4 | 1 / 2–4 | 实验题目 / 题目内容 | 标签黑体 10.5，内容仿宋 10.5 |
| 5 | 1 / 2–4 | 实验步骤及结果 / 正文 | 标签黑体 10.5；正文仿宋 10.5 |
| 6 | 1 / 2–4 | 实验总结 / 总结 | 同上 |
| 7 | 1 / 2–4 | 教师评语 / 空白 | 黑体 10.5 |
| 8 | 1 / 2–4 | 成绩 / 空白 | 黑体 10.5 |

列宽：第 1 列约 75.7 pt，其余三列各约 113.2 pt；第 5、6 行的内容单元格横跨第 2–4 列，宽约 339.5 pt，正文可用宽度约 328 pt。

## 填写要点

- 第 5 行的内容会很长，整行必须允许跨页（`Row.AllowBreakAcrossPages = True`）；第 6–8 行建议不允许跨页，避免总结被拆成两页。
- 第 5 行第 1 列的标签默认垂直居中，跨页时标签会落在第一页中部；改 `Cell(5,1).VerticalAlignment = 0`（顶端）更自然。
- 表格行高常被模板设成"最小值"，给内容留出空白；先 `Row.HeightRule = 0` 全部改为自动，排版才紧凑。

## report.json 格式

`scripts/fill_report.py` 读取的作业文件（UTF-8）：

```json
{
  "template": "C:/.../学号-姓名-实验1 实验模版.doc",
  "out": "C:/.../outputs/112320250050-傅俊豪-实验1.doc",
  "pdf": "C:/.../work/preview.pdf",
  "student": {"class": "252301", "id": "112320250050", "name": "傅俊豪", "date": "2026年10月19日"},
  "title": "实验1  顺序表的基本操作及其应用算法",
  "blocks": [
    {"type": "h2", "text": "一、实验内容"},
    {"type": "body", "text": "顺序表的基本操作算法（exp1.h、exp1.c）；倒置存储（exp2.1.1.c）。"},
    {"type": "h3", "text": "1．顺序表的基本操作算法（exp1.h、exp1.c）"},
    {"type": "img", "path": "C:/.../shots/image1.png", "caption": "图 1  exp1.c 的运行结果", "width": 290},
    {"type": "body", "text": "6．5 个程序均编译通过，运行结果与算法要求一致。"}
  ],
  "summary": ["本次实验完成了……。", "5 个程序均编译通过，运行结果正确。"]
}
```

`blocks` 支持的 `type`：`h2`（二级标题）、`h3`（小节标题）、`body`（正文）、`img`（截图 + 图注）。

没有截图时把 `img` 换成占位框：`fill_report.py` 提供 `"placeholder": true` 与 `"hint"` 字段，生成灰框提示文字，学生点选提示文字后 `Ctrl+V` 覆盖即可。

## Word COM 常见坑

- `Cell.Range.Text = "..."` 替换内容但保留单元格；多段落用 `\r` 拼接后一次赋值即可。
- 往单元格末尾追加内容不能用 `Range.InsertAfter`（会报"此操作对行结尾无效"），要把 range 的 `End` 减 1 再 `Collapse(0)`。
- 单元格内插入嵌套表格：先删掉占位段的文字，记录其起始位置，再 `Cell.Range.Tables.Add(Doc.Range(pos,pos), rows, cols)`；插入后原段落变成表格后面的空段落。
- 嵌套表格不计入 `Document.Tables`，统计时要遍历单元格的 `Range.Tables`。
- 嵌套表格列宽：先 `AllowAutoFit = False`，再逐列设 `Columns(j).Width`，否则 Word 会重算。
- 表格/图片跨页：`Row.AllowBreakAcrossPages`；图文同页：给图片所在单元格段落和其后空段落设 `KeepWithNext = True`。
- 保存：`.doc` 用 `doc.Save()`（保持原格式）；`.docx` 用 `doc.SaveAs2(path, FileFormat=16)`。导出 PDF：`doc.ExportAsFixedFormat(pdf, 17)`。

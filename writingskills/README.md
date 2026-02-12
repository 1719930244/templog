# writingskills

本目录用于沉淀本轮对话产出的“写作 skill”与其可复现抓取脚本/输出索引。

## 内容

- `se-paper-writing/SKILL.md`：软件工程论文写作通用 skill（证据链、RQ 驱动评测、Threats to Validity 等）。
- `yg-paper-writing/SKILL.md`：杨光（Guang Yang）论文写作风格与技巧（标题/摘要信号 + 模板 + 清单）。
- `pipelines/`：抓取与信号提取脚本（Python；仅下载公开可访问 PDF，不绕过付费墙/反爬）。
- `outputs/`：最新一次运行的索引与汇总（JSON/Markdown）。
- `caches/`：抓取页面缓存（HTML）。

## 复现

在本仓库根目录运行（需要 Python + `pypdf`）：

```powershell
python templog/writingskills/pipelines/collect_xchencs_last5y_se.py --refresh-missing
python templog/writingskills/pipelines/collect_yg_publications.py --refresh-missing
python templog/writingskills/pipelines/collect_arxiv_csse.py --max-results 50 --since-year 2021
```

说明：
- `outputs/` 中的部分路径字段来自作者本机运行环境，跨机器使用建议重新跑脚本生成新索引。
- 本目录未同步 PDF 文件；如需 PDF，请在本机运行脚本自动下载（仅公开可获取的那部分）。

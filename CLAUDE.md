# 学者写作 SKILL 挖掘流程

目标：从某位学者的论文集中提炼出可复用的写作风格模板（SKILL.md）。

## 流程步骤

1. **收集论文列表**：从学者个人主页抓取论文列表 HTML，解析出标题、年份、会议/期刊、作者等元数据，按需过滤（如仅 CCF-A）
2. **获取 PDF**：依次尝试作者主页直链 → OpenAlex API → arXiv API → landing page 发现，下载公开可获取的 PDF
3. **提取文本**：用 pypdf 提取前 3 页文本，缓存到 `caches/extracted_<author>/` 目录
4. **信号提取**：对提取文本做正则匹配，统计写作信号（abstract 是否含数字、是否有 RQ、是否有 contributions 列表、是否有 threats to validity 等）
5. **汇总输出**：生成 `outputs/<author>_index.json`（全量元数据+信号）和 `outputs/<author>_summary.md`（统计摘要）
6. **人工+AI 深度分析**：基于汇总数据和 PDF 全文，由 AI 逐节分析（标题/摘要/引言/方法/实验/讨论/结论），提炼模式、占比、可复用句式模板，产出 `<author>-paper-writing/SKILL.md`

## 目录结构约定

```
writingskills/
├── pipelines/collect_<author>_publications.py   # 抓取+信号提取脚本
├── caches/                                       # HTML 缓存、PDF、提取文本
├── outputs/                                      # JSON 索引 + Markdown 汇总
└── <author>-paper-writing/SKILL.md              # 最终写作技巧文档
```

## 关键依赖

- Python + pypdf
- OpenAlex API（免费，无需 key）
- arXiv API（备选 PDF 来源）
- 学者个人主页（论文列表来源）

# templog 项目记忆

> **项目路径**: `/home/szw/github/templog/`
> **类型**: GitHub 项目
> **远程仓库**: `github.com/1719930244/templog`
> **用途**: 调研文档、写作技能分析、工作日志

## 文件命名规则

所有文件以 `YYMMDD-` 日期前缀开头，方便按时间排序和定位：
- 格式: `YYMMDD-描述.ext`，如 `260224-ai-code-eval-metrics-survey.md`
- 日期取文件最后更新日期

## 目录结构

```
templog/
├── YYMMDD-*.md/pdf/docx      # 调研文档、日志（按日期排序）
├── pdf_style.css              # PDF 导出样式
└── writingskills/             # 学者写作分析（独立模块）
    ├── pipelines/             # 数据采集脚本
    ├── caches/                # PDF/文本缓存
    ├── outputs/               # 分析结果
    └── <author>-paper-writing/SKILL.md
```

## PDF 导出

```bash
cd /home/szw/github/templog
npx md-to-pdf 260224-ai-code-eval-metrics-survey.md --stylesheet pdf_style.css
```

## 写作分析流程

流程: 收集论文列表 → 获取 PDF → 提取文本 → 信号提取 → 汇总输出 → AI 深度分析

依赖: Python + pypdf, OpenAlex API, arXiv API

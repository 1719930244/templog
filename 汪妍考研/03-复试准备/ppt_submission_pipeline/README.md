# 投稿论文PPT自动化流水线

这个目录用于把论文原稿（`docx/pdf`）自动转换为复试汇报PPT素材，覆盖：
- 结构化提纲（问题-方法-实验-结论-贡献-Q&A）
- Google Workspace MCP 批量建页参数（`create_presentation` + `batch_update_presentation`）
- 本地可直接打开的 `pptx` 学术版（含关键图表：VAS、满意度、依从性）

## 1. 生成产物（推荐学术风格版）

```bash
uv run --with python-pptx python3.10 ./build_submission_ppt_assets.py \
  --source "/home/szw/github/templog/汪妍考研/01-简历材料/原稿 _基于时效性激励理论的护理干预在经尿道前列腺热蒸汽消融术患者的应用效果研究.docx" \
  --output-dir "/home/szw/github/templog/汪妍考研/03-复试准备/ppt_submission_pipeline/generated" \
  --presenter "汪妍" \
  --affiliation "南京大学医学院附属鼓楼医院 泌尿外科"
```

## 2. 关键输出文件

- `generated/submission_outline.md`
- `generated/submission_slides.json`
- `generated/submission_local_academic.pptx`（优先使用）
- `generated/submission_local_styled.pptx`（同内容别名）
- `generated/submission_local_draft.pptx`（fallback）
- `generated/workspace_mcp_create_args.json`
- `generated/workspace_mcp_batch_update_args.template.json`

## 3. 用 Workspace MCP 生成 Google Slides

先创建演示文稿：

```bash
generated/workspace_mcp_payload.sh create your_email@example.com \
  | uvx workspace-mcp --cli create_presentation
```

拿到 `presentation_id` 后批量写入页面内容：

```bash
generated/workspace_mcp_payload.sh apply your_email@example.com PRESENTATION_ID \
  | uvx workspace-mcp --cli batch_update_presentation
```

## 4. 注意事项

- 该流水线会尽量抽取文中关键结果，但最终答辩前请用“最终投稿稿”复核所有数值。
- 如你更新论文，只需重新运行一次生成命令即可刷新全部产物。

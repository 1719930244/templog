# 投稿汇报PPT自动化产物

本目录由 `build_submission_ppt_assets.py` 自动生成，包含：
- `submission_outline.md`：论文汇报提纲（问题-方法-结果-结论-Q&A）
- `submission_slides.json`：结构化幻灯片数据（12页）
- `submission_slides.md`：Pandoc 幻灯片 Markdown
- `submission_local_academic.pptx`：本地学术风格PPT（优先使用）
- `submission_local_styled.pptx`：本地学术风格PPT（同内容别名）
- `submission_local_draft.pptx`：本地基础版PPT（fallback）
- `workspace_mcp_create_args.json`：`create_presentation` 参数模板
- `workspace_mcp_batch_update_args.template.json`：`batch_update_presentation` 参数模板
- `workspace_mcp_env.example`：Google OAuth 环境变量模板
- `workspace_mcp_payload.sh`：根据邮箱和 presentation_id 生成可直接 pipe 给 CLI 的 JSON

## 用 Google Workspace MCP 创建正式 Google Slides

0. 先配置 Google OAuth 环境变量（必需）：

```bash
export GOOGLE_OAUTH_CLIENT_ID="YOUR_CLIENT_ID"
export GOOGLE_OAUTH_CLIENT_SECRET="YOUR_CLIENT_SECRET"
```

1. 先创建演示文稿（得到 presentation_id）：

```bash
./workspace_mcp_payload.sh create your_email@example.com \
  | uvx workspace-mcp --cli create_presentation
```

2. 把第1步输出中的 `presentation_id` 复制出来后，批量写入全部页面：

```bash
./workspace_mcp_payload.sh apply your_email@example.com PRESENTATION_ID \
  | uvx workspace-mcp --cli batch_update_presentation
```

3. 如需二次修改页面内容，编辑 `submission_slides.json` 后重新运行生成脚本。

# Codex 任务总结回复（TraceGen：禁止 LLM 生成解释性注释）

时间：2026-02-10 10:53:48（本地）

目标：解决 TraceGen 合成阶段中，LLM 在 `code_after` / `injection_patch` 里夹带“解释性注释”（例如 `# to introduce a bug ...`）的问题。

---

## 一、解决方案（TraceGen 代码改动）

TraceGen 仓库：`/home/szw/Code_Projects/TraceGen/`  
本次改动 commit：`af503d1`（`synthesis: forbid explanatory comments in patches`）

### 1) Prompt 侧：显式禁止新增注释

文件：`src/modules/synthesis/prompts/synthesis_agent_prompts.py`

新增/强化约束：

- **NO NEW COMMENTS（STRICT）**：`code_after` 中禁止新增任何 `# ...` 注释（包含行尾 inline comment）
- 明确说明：解释必须写在 **Thought**，不能写进代码
- 在注入点约束（INJECTION_POINT_CONSTRAINT）中将“新增注释”列为 **Validation 会拒绝** 的条件之一

### 2) 代码侧：Patch 语义校验时拒绝“新引入的注释”

文件：`src/modules/synthesis/agent.py`

在 `_validate_patch_semantics()` 中加入严格校验：

- 对 `code_before` 与 `code_after` 做 Python tokenize（对缩进片段做 `dedent`）
- 若 `code_after` **比 `code_before` 多出任何 COMMENT token**（包含 inline comment），直接判定 **PATCH VALIDATION FAILED**
- 失败反馈会提示：禁止新注释，并给出一个 comment 示例，促使 LLM 下一轮重试时移除注释

效果：即使 LLM 仍尝试输出“解释性注释”，也会被合成阶段拦截并触发重试，从而保证落盘数据集不包含这类注释污染。

---

## 二、3 个 seeds 验证（确保输出不含解释性注释）

验证 seeds（同之前 3 个）：

- `django__django-11099`（Constant_Update）
- `django__django-12915`（Type_Cast_Fix）
- `django__django-13447`（Data_Initialization）

运行命令：

```bash
/home/szw/python_env/TraceGen/bin/python main.py \
  data.target_instances_path=configs/target_instances_prompt_mimic_3.json \
  runtime.enable_extraction=false \
  runtime.batch_size=0 \
  runtime.num_workers=1 \
  runtime.max_synthesis_instances=3 \
  method.synthesis.matcher.top_k_final=3 \
  +method.synthesis.agent.validate_during_synthesis=true \
  +method.synthesis.agent.max_attempts=3 \
  synthesis_llm.temperature=0.2 \
  runtime.enable_solving=false
```

输出目录：

- `/home/szw/Code_Projects/TraceGen_outputs/2026-02-10/10-42-32/`

每个 seed 至少获得 1 个 VALID（且其 `injection_patch` 中无新增注释行）：

- `django__django-11099` → VALID：`synthetic_django_django_20260210104435910483`
- `django__django-12915` → VALID：`synthetic_django_django_20260210104517094374`
- `django__django-13447` → VALID：`synthetic_django_django_20260210105155430530`

你可以在 `2_synthesis/final_dataset.json` 的每条 item 的 `metadata.injection_patch` 中检查 diff：已不再出现 `+ # ...` 或 `...  # ...` 这类解释性注释。

---

## 三、后续可选增强

当前规则仅禁止 **新增注释（# comment）**。若你希望进一步“只改可执行代码”，也可以继续强化：

- 禁止修改/新增 docstring（`""" ... """`）  
- 禁止改动纯文本行（例如只改注释、只改空白）之外，**更严格限制 diff 触及范围**


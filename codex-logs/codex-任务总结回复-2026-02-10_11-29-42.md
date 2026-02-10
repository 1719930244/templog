# Codex 任务总结回复（Fix Intent 映射 + 禁止 docstring/纯文本改动）

时间：2026-02-10 11:29:42（本地）

本轮完成两件事：
1) 给出 **Fix Intent → compatible_injections** 的映射位置与具体内容  
2) 在合成阶段加入 **禁止改 docstring / 纯文本行**（并额外禁止仅空白/格式改动）规则，避免 LLM 产生无意义文本噪声 diff

---

## 1) Fix Intent → compatible_injections 映射（具体内容）

代码位置：
- `src/modules/synthesis/heuristics/intent_rules.py` → `INTENT_INJECTION_RULES`

映射内容（source_intent → compatible_injections）：

- `Condition_Refinement` → [`Condition_Refinement`, `Guard_Clause_Addition`]
- `Guard_Clause_Addition` → [`Guard_Clause_Addition`, `Condition_Refinement`]
- `Exception_Fix` → [`Exception_Fix`, `Guard_Clause_Addition`]
- `Argument_Update` → [`Argument_Update`, `Constant_Update`, `Variable_Replacement`]
- `API_Replacement` → [`API_Replacement`, `Argument_Update`]
- `Variable_Replacement` → [`Variable_Replacement`, `Constant_Update`]
- `Constant_Update` → [`Constant_Update`, `Variable_Replacement`]
- `Type_Cast_Fix` → [`Type_Cast_Fix`, `Variable_Replacement`]
- `Data_Initialization` → [`Data_Initialization`, `Guard_Clause_Addition`]
- `Statement_Insertion` → [`Statement_Insertion`]
- `Complex_Logic_Rewrite` → [`Complex_Logic_Rewrite`, `Condition_Refinement`, `Statement_Insertion`]

使用点（提示词注入建议）：
- `src/modules/synthesis/agent.py`：`FixIntentTransformer.to_prompt_format()`

候选节点的 intent compatibility 过滤（不是上面这张映射，而是基于 seed pattern/关键词/兜底三层匹配）：
- `src/modules/synthesis/matcher.py`：`_filter_compatible_intents()`
- `src/modules/synthesis/pattern_matcher.py`：`check_intent_compatibility()`

---

## 2) 禁止改 docstring / 纯文本行（并禁止仅空白/格式改动）

目的：
- 防止 LLM “顺手改 docstring 文本”（如重复单词/拼写）污染 patch
- 防止产生仅空白/格式变化的噪声 diff

实现（双层约束）：

### Prompt 侧（明确禁令）

文件：`src/modules/synthesis/prompts/synthesis_agent_prompts.py`
- 在约束中新增/强化：
  - `NO DOCSTRING / PURE‑TEXT CHANGES`
  - 禁止触碰 triple‑quoted docstring 块

### 代码侧（硬拦截）

文件：`src/modules/synthesis/agent.py`

在 `SynthesisAgent._validate_patch_semantics()` 中新增两类拒绝条件：

1) **仅空白/格式改动**：若 `code_before` 与 `code_after` 去除空白后相同 → reject  
2) **docstring 改动**：使用 AST 对比 docstring（`ast.get_docstring`），若新增/删除/内容变化 → reject

TraceGen 本地 commit（已提交，未 push）：
- `f3d0df9` synthesis: forbid docstring and whitespace-only changes

---

## 3) 快速复验（3 seeds）

运行：

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
- `/home/szw/Code_Projects/TraceGen_outputs/2026-02-10/11-18-15/`

结论：
- 3 个 seed 均至少 1 个 VALID（且 `injection_patch` 中不再出现 docstring 文本改动 / 新增注释 / 纯空白噪声 diff）


# Codex 任务总结回复（TraceGen：Prompt 改造 + 3 seeds 验证）

时间：2026-02-10 10:27:03（本地）

目标：调整 TraceGen 的合成 Agent 提示词（prompt），让其**模仿 seed 的 pattern**进行 bug 合成，并**去掉“反转逻辑/逻辑反转（logic reversal）”倾向**；同时修正 `injection_strategy` 记录的默认值问题，并在 **3 个 Django seeds** 上完成验证。

---

## 一、改动内容（TraceGen 仓库）

TraceGen 仓库路径：`/home/szw/Code_Projects/TraceGen/`

### 1) Prompt：从“Reverse/通用翻转”改为“Seed Pattern Mimic”

文件：`/home/szw/Code_Projects/TraceGen/src/modules/synthesis/prompts/synthesis_agent_prompts.py`

主要改动：

- 将系统提示词中的 “Apply Reverse Transformation / Reverse Fix” 类表述改为 **Mimic Seed Pattern**（强调参考 seed BEFORE/AFTER 的 bug pattern，而不是默认做条件翻转/布尔反转）。
- 将 prompt 中的 “Common Bug Patterns (comparison flip / boolean inversion …)” 这类通用反转型策略降级/移除，改为 **Seed‑Pattern‑First**，避免 Agent 习惯性做逻辑翻转。
- 在 Action Input 的示例格式中补充 `injection_strategy` 字段（建议填 `{fix_intent}`），便于落盘统计不再缺失。
- 补充 `Type_Cast_Fix` 与 `Data_Initialization` 的 intent 示例（之前缺失，容易导致 Agent 漂移到通用策略或产生无语义改动）。

### 2) 记录字段：去掉 `logic_reversal` 默认占位

文件：`/home/szw/Code_Projects/TraceGen/src/modules/synthesis/agent.py`

- `injection_strategy` 的默认值从 `"logic_reversal"` 改为：`action_input.injection_strategy` → `action_input.injection_type` → `fix_intent` → `"unspecified"`  
  目的：避免 LLM 未输出该字段时，统计数据被“logic_reversal”默认值污染。
- `fix_intent_details` 中移除 “Reverse this …” 字样，改为强调 **模仿 seed 的 bug pattern**（避免 prompt 误导）。

### 3) 3-seed 验证用实例列表

文件：`/home/szw/Code_Projects/TraceGen/configs/target_instances_prompt_mimic_3.json`

包含 3 个 seeds：

- `django__django-11099`（Constant_Update）
- `django__django-12915`（Type_Cast_Fix）
- `django__django-13447`（Data_Initialization）

---

## 二、TraceGen 的 Git 中间节点（commit 记录）

以下 commit 已在 `TraceGen/` 中保存（未 push）：

- `f60b05d` docs: add git workflow note
- `c14532a` synthesis: mimic seed pattern prompt
- `8cdb7ac` prompts: prefer seed pattern over generic flips
- `e3c42fd` prompts: add examples for type cast and init

---

## 三、3 个实例验证（Stage2+Stage3，带合成阶段即时验证）

### 运行命令（Hydra overrides）

在 `TraceGen/` 下执行：

```bash
/home/szw/python_env/TraceGen/bin/python main.py \
  data.target_instances_path=configs/target_instances_prompt_mimic_3.json \
  runtime.enable_extraction=false \
  runtime.batch_size=0 \
  runtime.num_workers=1 \
  runtime.max_synthesis_instances=3 \
  method.synthesis.matcher.top_k_final=3 \
  +method.synthesis.agent.validate_during_synthesis=true \
  +method.synthesis.agent.max_attempts=2 \
  synthesis_llm.temperature=0.2 \
  runtime.enable_solving=false
```

说明：
- `validate_during_synthesis=true`：对每个候选点生成后立即跑一次验证，**一旦拿到 VALID 就停止继续尝试该 seed 的后续候选点**（更省时、也更容易保证每个 seed 至少有 1 个 valid）。
- `top_k_final=3`：每个 seed 最多尝试 3 个候选点（结合即时验证会提前停止）。

### 输出目录

本次验证输出目录：`/home/szw/Code_Projects/TraceGen_outputs/2026-02-10/10-15-26/`

### 验证结果概览

该轮对 3 个 seed 均获得了至少 1 个 `VALID` 的 synthetic bug：

- Seed `django__django-11099`（Constant_Update）
  - VALID：`synthetic_django_django_20260210101550062815`
  - `PASS_TO_FAIL`=1，`PASS_TO_PASS`=30
  - 注入补丁（摘要）：`django/contrib/sites/models.py` 中将 whitespace 检查改为**不检查换行符**（与 seed 的 newline 相关 bug pattern 一致）

- Seed `django__django-12915`（Type_Cast_Fix）
  - VALID：`synthetic_django_django_20260210101840646397`
  - `PASS_TO_FAIL`=3，`PASS_TO_PASS`=24
  - 注入补丁（摘要）：`django/core/handlers/base.py` 中对 `middleware_method(...)` 的返回值做 `str(...)` 转换，制造类型/返回值形态偏差（符合 Type_Cast_Fix 类 pattern）

- Seed `django__django-13447`（Data_Initialization）
  - VALID：`synthetic_django_django_20260210102450538538`
  - `PASS_TO_FAIL`=2，`PASS_TO_PASS`=638
  - 注入补丁（摘要）：`django/contrib/admin/options.py` 中 `get_model_perms()` 的返回 dict **缺失一个 key**（初始化缺失，符合 Data_Initialization 类 pattern）

对应文件：
- 合成数据集：`/home/szw/Code_Projects/TraceGen_outputs/2026-02-10/10-15-26/2_synthesis/final_dataset.json`
- 验证结果：`/home/szw/Code_Projects/TraceGen_outputs/2026-02-10/10-15-26/3_validation/*_validation.json`

---

## 四、补充说明 / 已知问题

1) **部分 LLM 输出仍会夹带“解释性注释”**（例如 `# Exclude newline …`）。目前 validator 不会因此失败，但从数据集质量角度，后续可进一步在 prompt 或代码侧强约束禁止此类“显式 bug 注释”。

2) `django__django-12915` 的 fix_intent 标注为 `Type_Cast_Fix`，但其原始 patch 更像 async handler 相关修复（存在 **intent 误标/弱标** 的可能）。本次通过加入 intent 示例 + seed-pattern-first 约束后，仍能稳定合成出可验证的 type-cast 风格 bug，但从“语义严格对齐 seed”角度，后续可考虑改进 seed intent 抽取/归类。


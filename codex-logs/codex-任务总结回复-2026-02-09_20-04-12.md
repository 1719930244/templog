# Codex 任务总结回复（TraceGen / Django 114 seeds）

时间：2026-02-09 20:04:12（本地）

本次围绕 TraceGen 的离线 Stage2（仅向量检索）可用性、向量生成完备性、以及历史日志中 `valid` bug 的汇总分析做了验证与整理。

---

## 关键路径（便于复现/查阅）

- TraceGen 代码仓库：`/home/szw/Code_Projects/TraceGen/`
- Python 环境：`/home/szw/python_env/TraceGen/bin/python`
- 输出根目录：`/home/szw/Code_Projects/TraceGen_outputs/`
- 记忆文档（SSOT）：`/home/szw/AGENT_MEMORY/TraceGen_master.md`

---

## 1) 确认 114 个 Django commits 向量是否生成完毕

结论：**已生成完毕（114/114）且索引文件齐全**。

- commits embedding JSON 数量：`data/assets/embeddings/django_django/commits/*.json` = **114**
- 统计文件：`data/assets/embeddings/django_django/stats.json`
  - `commits_processed` = **114**
  - `vector_pool.npy` 形状：`(63651, 1024)`
  - `hash_to_idx.json`：可用于向量池索引映射

---

## 2) Stage2 离线评测：仅向量检索能否找回正确候选节点（不使用 LLM）

目标：**不跑任何 LLM 的分析/提取**，仅基于缓存（extractions/graphs/embeddings）验证每个 seed 在第二阶段能否用向量检索到候选合成节点。

实现：

- 评测脚本：`/home/szw/Code_Projects/TraceGen/scripts/test_stage2_vector_retrieval.py`
- 评测报告：`/home/szw/Code_Projects/TraceGen_outputs/full_run/stage2_vector_retrieval_report.csv`

结果概览：

- **92/114** seeds：可在 Stage2 走到 “vector-used” 并找到 `>=1` candidate
- **22/114** seeds：失败，按原因统计：
  - `seed_anchor_not_in_commit_map`: **10**
    - seed 的 root_cause `node_id` 形态与 commit embedding map 的 `node_id` 形态不一致，导致无法定位 seed anchor
  - `seed_vector_norm_zero`: **10**
    - seed anchor 向量为全 0（余弦相似度不可用），通常意味着 embedding 写入了占位/失败向量
  - `no_candidates_after_intent_compatibility`: **2**
    - 向量检索能拉回候选，但在 intent 兼容过滤后全部被剔除

---

## 3) “只使用成功对象”：排除失败向量实例 + 写入 target instance 列表

已将 Stage2 向量检索评测结果转成 instance 列表，便于后续合成只跑 “可检索成功” 的子集：

- ✅ 成功列表（92）：`/home/szw/Code_Projects/TraceGen/configs/target_instances_stage2_vector_ok.json`
- ❌ 失败列表（22）：`/home/szw/Code_Projects/TraceGen/configs/target_instances_stage2_vector_fail.json`
- ❌ 失败子集：零向量（10）：`/home/szw/Code_Projects/TraceGen/configs/target_instances_seed_vector_norm_zero.json`

用法（示例）：运行时覆盖配置 `data.target_instances_path=...ok.json`，即可只对成功 seeds 做合成。

以上也已写入记忆文档：`/home/szw/AGENT_MEMORY/TraceGen_master.md`。

---

## 4) Git 工作流约束（已写入文档）

已在文档中记录并强调：

- TraceGen 项目已初始化 Git 且配置远程 `origin`
- **任何改动必须 commit**
- **仅在收到明确命令时 push**
- 严禁提交任何密钥/Token（尤其是 API Key / PAT）

落点：

- `~/AGENT_MEMORY/TraceGen_master.md`
- `~/Code_Projects/TraceGen/CLAUDE.md`

---

## 5) 汇总所有日志中 “已生成且通过 valid 验证” 的 bugs，并做初步分析

输出到临时汇总目录（便于你浏览/拷贝）：  
`/home/szw/Code_Projects/TraceGen_outputs/_tmp_valid_bugs_summary_2026-02-09_19-46-20/`

包含文件：

- `valid_bugs.csv`：**23** 个 unique valid bugs（**30** 次 valid occurrences）
- `valid_bug_occurrences.csv`：每次出现对应的 run 路径、日志路径
- `bugs/<instance_id>/`：按 bug 归档（`index.json`、可用时的 `synthesis.json`、`occurrences/*/validation_logs/`）
- `analysis.md`：统计汇总与失败总览

全局验证统计（来自本次扫描到的 validation JSON）：

- 总计：**810**
  - `error`: **522**
  - `invalid`: **233**
  - `valid`: **30**
  - `timeout`: **25**
- `error` 主要原因：patch apply 失败
- `invalid` 主要原因：`NO_FAIL`（预期 fail-to-pass 没能触发失败）

---

## 6) 关于 `logic_reversal`：它“在哪一步体现”？为什么看起来不对？

结论：你感觉是对的——`logic_reversal` 很多时候并不是实际判定出来的策略，而是**合成阶段写入的默认值**。

- 默认值来源：`/home/szw/Code_Projects/TraceGen/src/modules/synthesis/agent.py`
  - `_handle_generate_bug()` 中：
    - `injection_strategy = action_input.get("injection_strategy") or action_input.get("injection_type") or "logic_reversal"`
- 落盘：随后构造 `SynthesisResult(... injection_strategy=...)` 并保存到 `synthesis.json`

因此：当 LLM 没输出 `injection_strategy/injection_type` 字段时，记录会统一变成 `logic_reversal`，导致统计看起来“全是 logic_reversal”，但那很可能只是占位，而非真实注入策略分类。

改进建议（可选）：

1) 默认值改为 `unknown/unspecified`，避免误导统计  
2) 强制 LLM 必须输出该字段（缺失则判生成失败）  
3) 后验基于 `injection_patch` / AST diff 做注入策略分类（更可信，但工程量更大）

---

## 安全提醒（强烈建议）

请避免把任何 Token / PAT 明文写入：

- 代码仓库
- 配置文件
- 或 `git remote` URL

推荐改用 SSH 或 Git credential helper 管理凭据，并及时轮换已暴露的 Token。


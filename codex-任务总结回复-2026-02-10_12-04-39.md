# Stage2 向量检索离线评测结果（Django 114 seeds，top5 candidates）

时间：`2026-02-10_12-04-39`

## 本次运行

- 评测脚本：`Code_Projects/TraceGen/scripts/test_stage2_vector_retrieval.py`
- 运行命令：
  - `Code_Projects/TraceGen/.venv/bin/python Code_Projects/TraceGen/scripts/test_stage2_vector_retrieval.py --top-k-final 5`
- 说明：仅使用缓存的 `extractions/graphs/embeddings` 做 Stage2 检索与兼容性过滤，不调用 LLM。

## 总览

- 总 seeds：`114`
- 成功（`vector_used=1` 且 `candidates=5`）：`92`
- 失败：`22`

## 分数分布（成功 seeds 的 best candidate）

- best_final_score：min=0.627606, mean=0.826194, max=0.961178
- best_vector_score：min=0.310436, mean=0.704734, max=0.975237
- best_topology_score：min=0.670818, mean=0.907168, max=1.000000

## 失败原因统计

- `seed_anchor_not_in_commit_map`: `10`
- `seed_vector_norm_zero`: `10`
- `no_candidates_after_intent_compatibility`: `2`


## 失败 seeds 列表

| instance_id | commit_short | failure_reason |
|---|---|---|
| django__django-14730 | 4fe3774c | `no_candidates_after_intent_compatibility` |
| django__django-14667 | 6a970a8b | `no_candidates_after_intent_compatibility` |
| django__django-11283 | 08a4ee06 | `seed_anchor_not_in_commit_map` |
| django__django-14155 | 2f13c476 | `seed_anchor_not_in_commit_map` |
| django__django-13757 | 3f140dde | `seed_anchor_not_in_commit_map` |
| django__django-15738 | 6f73eb9d | `seed_anchor_not_in_commit_map` |
| django__django-13590 | 755dbf39 | `seed_anchor_not_in_commit_map` |
| django__django-14608 | 7f33c1e2 | `seed_anchor_not_in_commit_map` |
| django__django-15819 | 877c800f | `seed_anchor_not_in_commit_map` |
| django__django-12589 | 895f28f9 | `seed_anchor_not_in_commit_map` |
| django__django-15781 | 8d160f15 | `seed_anchor_not_in_commit_map` |
| django__django-14915 | 903aaa35 | `seed_anchor_not_in_commit_map` |
| django__django-16816 | 191f6a9a | `seed_vector_norm_zero` |
| django__django-14017 | 466920f6 | `seed_vector_norm_zero` |
| django__django-15400 | 4c76ffc2 | `seed_vector_norm_zero` |
| django__django-15814 | 5eb6a2b3 | `seed_vector_norm_zero` |
| django__django-11583 | 60dc957a | `seed_vector_norm_zero` |
| django__django-15695 | 64748016 | `seed_vector_norm_zero` |
| django__django-11019 | 93e892bb | `seed_vector_norm_zero` |
| django__django-12497 | a4881f5e | `seed_vector_norm_zero` |
| django__django-11001 | ef082ebb | `seed_vector_norm_zero` |
| django__django-16408 | ef85b6bf | `seed_vector_norm_zero` |


## 产物

- 报告 CSV（已同步到本仓库）：`TraceGen_reports/stage2_vector_retrieval_report_2026-02-10_12-04-39.csv`


## 备注（下一步可能的改进）

- `seed_anchor_not_in_commit_map`：Seed root-cause 节点无法在该 commit 的 `embeddings/.../commits/<hash>.json` 映射中找到（通常是节点 id 生成/映射不一致）。
- `seed_vector_norm_zero`：Seed 对应向量范数为 0，导致余弦相似度为空（需要排查 embedding 生成/写入）。
- `no_candidates_after_intent_compatibility`：向量+拓扑能找到候选，但意图兼容性过滤后为空（可能阈值/匹配规则过严或 seed intent 不可落地）。

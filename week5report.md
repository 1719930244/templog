# TraceGen Week5 Report（简版，用于组会）

> 截止：2026-02-10  
> 论文设计对照文档：`AGENT_MEMORY/Tracegen-paperdesign.md`

## Week5（02/02–02/06）我做了什么

- 跑通并稳定了全链路：提取 → 合成 → 容器验证 →（可选）求解评测
- 开始批量跑 Django 全量实例，并把每轮结果做成可复现实验产物与统计
- 把主要失败原因收敛到少数几类（便于后续专项提升有效样本）

## 周进度（从开始到现在）

| Week | 我做了什么（只写结果） | 规模/效果（可量化） |
|---|---|---:|
| Week1（01/05–01/09） | 环境与工程跑通，产物可落盘 | 形成可复现的 extraction 产物 |
| Week2（01/12–01/16） | 接入合成阶段，开始产出 synthetic 雏形 | 多次试跑产出 patch/元信息 |
| Week3（01/19–01/23） | 整理运行产物与统计口径，方便对比迭代 | 每次 run 都能快速定位瓶颈 |
| Week4（01/26–01/30） | 准备大规模跑数资产（图/提取缓存/向量库） | Django 图/提取缓存各 **114**；向量库覆盖 **114 commits**（约 **6.4 万**代码片段向量） |
| **Week5（02/02–02/06）** | **全链路批量跑数 + 稳定性/效率提升** | **Django seeds 114；候选 patch 检查 479 条；Stage4 seed 对比跑通（seed 6/8 resolved；synthetic 0/3 resolved）** |
| Week6（02/09–02/10） | 离线评测 Stage2 可用性 + 小规模回归提升有效样本 | Stage2 可用 **92/114（≈80.7%）**；代表性 seeds 回归：每个至少 1 个可验证样本 |

## 按论文结构对照解释（不讲实现细节）

论文（`AGENT_MEMORY/Tracegen-paperdesign.md`）的 Phase 与当前进度对照：

| 论文 Phase | 我现在做到什么程度（到 02/10） | 证据/指标 |
|---|---|---:|
| Phase 1：Defect Extraction | 已可批量产出并缓存（支撑全量实验） | Django 覆盖 **114 commits**（图+提取缓存齐全） |
| Phase 2：Agentic Data Synthesis | 已能稳定产出 synthetic；有效样本率仍需提升 | 已有批量生成与 patch 质量检查（**479** 条记录） |
| Phase 3：Validation | 已跑通容器验证并形成历史统计 | 累计验证 **1022** 条（valid 110 / invalid 361 / error 523 / timeout 28） |
| Evaluation（求解评测/对比） | seed 对比评测链路已稳定；synthetic solved 偏低 | Stage4：seed **6/8** resolved；synthetic **0/3** resolved |

## 本周结论 + 下周计划（两句话）

- Week5 结论：项目已从“能跑”进入“能批量验证/评测并出统计”，下一阶段核心是提高 valid synthetic 比例。  
- 下周计划：优先解决导致 invalid/error 的头部原因，扩大 synthetic 的可验证样本量，并用同一套指标持续对比（synthetic vs seed）。  

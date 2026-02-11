# Weekly Report — 2026-02-10

> 截止：2026-02-10
> 论文设计对照文档：`AGENT_MEMORY/Tracegen-paperdesign.md`

## 本周我做了什么

- 修复 Docker 基建问题（容器构建/部署流程稳定化）
- 完成首轮全量跑批（92 seeds × 5 candidates），产出可量化的合成基线
- 合成 Prompt 改造（Mimic Seed Pattern）+ 质量硬拦截（注释/docstring 过滤）
- 明确论文投稿计划与人工评估方案

## 周进度（从开始到现在）

| Week | 我做了什么（只写结果） | 规模/效果（可量化） |
|---|---|---:|
| Week1（01/05–01/09） | 环境与工程跑通，产物可落盘 | 形成可复现的 extraction 产物 |
| Week2（01/12–01/16） | 接入合成阶段，开始产出 synthetic 雏形 | 多次试跑产出 patch/元信息 |
| Week3（01/19–01/23） | 整理运行产物与统计口径，方便对比迭代 | 每次 run 都能快速定位瓶颈 |
| Week4（01/26–01/30） | 准备大规模跑数资产（图/提取缓存/向量库） | Django 图/提取缓存各 **114**；向量库覆盖 **114 commits**（约 **6.4 万**代码片段向量） |
| Week5（02/02–02/06） | 全链路批量跑数 + 稳定性/效率提升 | Django seeds 114；候选 patch 检查 479 条；Stage4 seed 对比跑通（seed 6/8 resolved；synthetic 0/3 resolved） |
| Week6（02/09–02/10） | 离线评测 Stage2 可用性 + Prompt 改造 + 质量硬拦截 | Stage2 可用 **92/114（≈80.7%）**；Mimic Seed Pattern prompt 上线；注释/docstring 硬拦截上线 |
| **Week7（02/10–02/11）** | **首轮 92×5 全量跑批完成 + Docker 基建修复** | **见下方详细结果** |

## 现有合成结果（首轮全量 92×5）

数据来源：SWE-bench Lite Django 子集（114 条原始 seed） → 经 Stage2 向量检索 + 链路深度筛选 → 92 条可用 seed

| | 输入 seeds | 目标合成 | 实际合成 | avg/seed | Stage3 valid | Stage3 invalid | timeout/error | Seed 覆盖率（≥1 valid） | 0-valid seeds | LLM 调用 | tokens | 费用 | 模型 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **92×5 全量** | 92 | 460 | 439 | 4.772 | **81 (18.5%)** | 351 (80.0%) | 6+1 | **53/92 (57.6%)** | 39 | 632 | 5.79M | ¥11.17 | qwen3-coder-plus |

## Stage4（求解评测）结果（synthetic vs seed）

> run: `Code_Projects/TraceGen_outputs/stage2_ok_92x5/latest/4_solving/summary.json`

| 指标 | 合成输入 | 已完成 | resolved | unresolved | LLM 调用 | tokens | 费用（¥） | timeout/error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| synthetic | 81 | 81 | 23 | 50 | 105 | 2.093M | ¥3.54 | 1/7 |
| seed | 53 | 53 | 4 | 42 | 87 | 1.702M | ¥2.80 | 0/7 |
| total | 134 | 134 | 27 | 92 | 192 | 3.795M | ¥6.34 | 1/14 |

### 历史结果对比

| 时间 | 规模 | Stage3 valid rate | Seed 覆盖率 | 备注 |
|------|------|-------------------|-------------|------|
| 02-05 | 1×3 smoke | 1/3 = 33% | 1/1 | 精选 seed |
| 02-10 (3-seed) | 3×3 | ~3/9 | 3/3 | prompt mimic 验证 |
| **02-10 (全量)** | **92×5** | **81/439 = 18.5%** | **53/92 = 57.6%** | **首轮全量基线** |

## 下一步规划

| 优先级 | 任务 | 说明 |
|--------|------|------|
| **P0** | 39 个 0-valid seed 失败分型 | 区分：注入太弱 / 测试不敏感 / 代码路径未执行 |
| **P0** | Stage4 求解评测已跑完 | synthetic **23/81** resolved；seed **4/53** resolved |
| **P1** | 论文撰写启动 | 动机（Motivation）+ 方法描述 + 实验设计框架 |
| **P1** | 人工评估实验（节后） | ~300 条 Opus 合成数据给业务同学评估逼真程度 |
| **P2** | 论文投稿 | 暂定 3 月底；核心方向：Scale 解决路径复杂度 |

---

*Updated: 2026-02-11*

# AI 代码生成评测 Benchmark 全景调研

> **版本**: v1.0 | **日期**: 2026-03-16
> **定位**: 独立全景预研——系统梳理现有公开 AI 代码评测 Benchmark 的特点、质量与生态缺陷
> **方法**: 文献调研 + 公开数据分析，参考 5 篇元综述/质量评估工作

---

## 目录

- [1. 调研目标与方法](#1-调研目标与方法)
- [2. 元综述与 Benchmark 质量评估方法论](#2-元综述与-benchmark-质量评估方法论)
- [3. Benchmark 全景图：按 SE 生命周期分类](#3-benchmark-全景图按-se-生命周期分类)
- [4. 重点 Benchmark 深度分析](#4-重点-benchmark-深度分析)
- [5. Benchmark 质量评估：多维度综合诊断](#5-benchmark-质量评估多维度综合诊断)
- [6. 关键发现与问题诊断](#6-关键发现与问题诊断)
- [7. 开放问题与研究机会](#7-开放问题与研究机会)
- [8. 参考文献](#8-参考文献)

---

## 1. 调研目标与方法

### 1.1 调研目标

本调研为独立全景预研，不预设特定评测框架，目标：

1. **全面盘点**现有公开 AI 代码评测 Benchmark，覆盖 SE 全生命周期各阶段
2. **建立质量评估方法论**，参考"Benchmark 的 Benchmark"工作，形成可操作的质量诊断体系
3. **识别评测生态的结构性缺陷**（覆盖盲区、数据污染、测试充分性等）
4. **梳理开放问题与研究机会**，为后续研究提供方向参考

### 1.2 参考的元综述工作

| 工作 | 覆盖范围 | 核心贡献 | 发表 |
|------|---------|---------|------|
| **Hu et al. (2025)** "Assessing and Advancing Benchmarks for Evaluating LLMs in SE Tasks" | 291 个 SE Benchmark | 按 6 大 SE 任务分类，5 维质量清单 | arXiv:2505.08903 |
| **Cao et al. (2025)** "Rigor, Reliability, and Reproducibility: A Decade-Scale Survey of 572 Code Benchmarks" | 572 个代码 Benchmark (2014-2025) | HOW2BENCH 55 条检查清单，5 阶段生命周期评估 | arXiv:2501.10711 |
| **Wang et al. (2025)** "SDLC Perspective: A Survey of Benchmarks for Code LLMs and Agents" | 178 个 Benchmark，461 篇论文 | SDLC 视角分层分析框架 | arXiv:2505.05283 |
| **Siddiq et al. (2024)** "The Fault in our Stars: Quality Assessment of Code Generation Benchmarks" | 9 个 Benchmark，3566 个 Prompt | Prompt 质量缺陷分析，记忆效应检测 | SCAM 2024 |
| **Zheng et al. (2025)** "Re-Evaluating Code LLM Benchmarks Under Semantic Mutation" | 8 个 Benchmark 任务，10 个 LLM | Prompt 敏感性框架，100 个语义等价变体 | arXiv:2506.17369 |

### 1.3 补充的质量诊断工作

| 工作 | 焦点 | 核心发现 |
|------|------|---------|
| **LessLeak-Bench** (Zhang et al., 2025) | 83 个 SE Benchmark 数据泄漏 | 平均泄漏率 Python 4.8%、Java 2.8%、C/C++ 0.7%；QuixBugs 100%、BigCloneBench 55.7% |
| **SWE-Bench+** (Aleithan et al., 2024) | SWE-Bench 解决方案泄漏 | 60.83% 存在解决方案泄漏，47.93% 通过弱测试 |
| **HOW2BENCH 人类研究** (Cao et al., 2025) | 49 人 Benchmark 开发者调查 | 70% 未做数据质量保证，80% 忽视数据污染威胁 |

---

## 2. 元综述与 Benchmark 质量评估方法论

### 2.1 Hu et al. 的五维质量清单

浙大胡星团队对 291 个 Benchmark 采用以下评估维度：

| 维度 | 评估内容 |
|------|---------|
| **描述清晰度** | 任务、数据集、评估指标的清晰表达 |
| **SE 相关性** | 与真实 SE 任务/挑战的对齐程度 |
| **方法论严谨性** | 构建过程是否有文档化、可追溯 |
| **可复现性与可用性** | 数据集、脚本是否公开可用 |
| **领域影响力** | 后续研究的引用和采纳频率 |

**关键发现**：
- 291 个 Benchmark 中，**Coding Assistant 占 124 个 (42.6%)**，Requirements & Design 仅 25 个 (8.6%)
- 近半数 Benchmark 在 2023 年前发布，面临数据过时和污染风险
- 需求工程数据极难获取（企业视为机密资产）

**分布统计**：
| SE 任务类别 | Benchmark 数量 | 占比 |
|------------|---------------|------|
| Coding Assistant | 124 | 42.6% |
| Quality Management | 111 | 38.1% |
| Requirements & Design | 25 | 8.6% |
| Software Testing | 25 | 8.6% |
| Maintenance | 13 | 4.5% |
| AIOps | 6 | 2.1% |

### 2.2 Cao et al. 的 HOW2BENCH 框架

Cao 团队的 572 个 Benchmark 十年回顾提出了迄今最系统的质量评估框架：

**5 阶段 × 55 条检查清单**：

| 阶段 | 检查项数 | 核心关注点 |
|------|---------|-----------|
| Phase 0: Design | 4 | 任务定义清晰度、评估目标明确性 |
| Phase 1: Construction | 19 | 数据采集、清洗、去重、质量保证 |
| Phase 2: Evaluation | 12 | 评估指标合理性、LLM 数量、重复实验 |
| Phase 3: Analysis | 10 | 结果分析深度、统计显著性、错误分析 |
| Phase 4: Release | 10 | 开源、许可证、文档完整性、可复现环境 |

**触目惊心的质量现状**：

| 质量问题 | 比例 | 影响 |
|---------|------|------|
| 未做数据质量保证 | **~70%** | 数据噪声传播 |
| 未做去重 | **62%** | 评估偏差 |
| 忽视数据污染 | **~80%** | 评测结果不可信 |
| 评估 LLM 不足 3 个 | **34%** | 结论泛化性差 |
| 实验未重复执行 | **60%+** | 结果稳定性未知 |
| 未提供完整实验环境 | **96.4%** | 无法复现 |
| 隐藏 Prompt | **52.6%** | 评估不透明 |
| 未开源或部分不可用 | **10.9%** | 无法验证 |

**传播效应（Propagation Effect）**：超过 18% 的 Benchmark 被后续 Benchmark 作为数据源复用，质量缺陷逐级放大。

### 2.3 Wang et al. 的 SDLC 覆盖分析

178 个 Benchmark 的 SDLC 阶段分布：

| SDLC 阶段 | 占比 | 评价 |
|-----------|------|------|
| 软件实现 (Implementation) | **~61%** | 严重过载 |
| 软件测试 (Testing) | ~15% | 相对充足 |
| 软件维护 (Maintenance) | ~16% | 有待加强 |
| 需求工程 (Requirements) | **~5%** | 严重不足 |
| 软件设计 (Design) | **~3%** | 几乎空白 |

### 2.4 综合质量评估方法论：整合框架

基于以上工作，我们提炼出一个 **8 维 Benchmark 质量评估框架**：

| 维度 ID | 维度名称 | 评估内容 | 信息来源 |
|---------|---------|---------|---------|
| Q1 | **学术严谨性** | 发表会议/期刊等级、同行评审、引用量 | Hu et al. "影响力"维度 |
| Q2 | **数据质量** | 去重、清洗、标注一致性、噪声控制 | HOW2BENCH Phase 1 |
| Q3 | **抗污染能力** | 防数据泄漏机制、时间截止策略、动态更新 | LessLeak-Bench + Wang et al. |
| Q4 | **测试充分性** | 测试用例数量和质量、是否有增强测试 | SWE-Bench+ 教训 |
| Q5 | **Prompt 鲁棒性** | 对 Prompt 变体的性能稳定性 | Zheng et al. 语义变异框架 |
| Q6 | **可复现性** | 环境、代码、数据完整公开程度 | HOW2BENCH Phase 4 |
| Q7 | **规模与多样性** | 样本量、语言覆盖、任务多样性 | 综合各调研 |
| Q8 | **工业对齐度** | 与真实开发场景的贴合度、工业采纳情况 | Hu et al. "SE 相关性" |

---

## 3. Benchmark 全景图：按 SE 生命周期分类

### 3.1 阶段 1：需求与设计

> **覆盖率**: ~8% | **质量**: 整体偏弱
| Benchmark | 规模 | 任务类型 | 评估维度 | 发表 | 质量评级 |
|-----------|------|---------|---------|------|---------|
| **DevBench** | 22 仓库，4 语言 | 需求→设计→实现全流程 | 软件设计文档质量、模块划分 | ACL 2024 | B |
| **ProjDevBench** | 2,690 样本 | 项目级多文件代码生成 | 架构合理性、多文件一致性 | arXiv | B- |
| **BigCodeBench** | 1,140 任务 | 复杂指令+139库约束 | 指令遵循率、API 组合 | ICLR 2025 | A- |
| **EvoCodeBench** | 275 任务，10 领域 | 仓库级代码生成 | 领域需求覆盖、依赖解析 | NeurIPS 2024 | A- |
| **NFR-Review** | — | 非功能需求识别 | 需求分类准确率 | 2018 | C |
| **SpecGenBench** | — | 规格说明生成 | 规格完整性 | 2024 | B- |

**关键缺口**：
- 无专门的需求歧义检测 Benchmark
- 架构设计评估完全依赖静态分析，无专用 Benchmark
- DevBench 规模太小（仅 22 仓库），统计效力不足

### 3.2 阶段 2：软件构造

> **覆盖率**: ~61% | **质量**: 最为成熟
#### 3.2.1 功能正确性

| Benchmark | 规模 | 粒度 | 语言 | 防污染 | 发表 | 质量评级 |
|-----------|------|------|------|--------|------|---------|
| **HumanEval** | 164 题 | 函数级 | Python | ✗ | OpenAI 2021 | B（已过时） |
| **MBPP** | 974 题 | 函数级 | Python | ✗ | Google 2021 | B（已过时） |
| **EvalPlus** (HE+/MBPP+) | 164+399 题 | 函数级 | Python | ✗ | NeurIPS 2023 | **A** |
| **LiveCodeBench** | 1,055+ 题 | 函数级 | Python | ✔ 时间截止 | ICLR 2025 | **A** |
| **BigCodeBench** | 1,140 任务 | 函数级 | Python | ✗ | ICLR 2025 | **A-** |
| **ClassEval** | 100 类 | 类级 | Python | ✗ | ICSE 2024 | B |
| **CoderEval** | 230+230 任务 | 函数级 | Python/Java | ✗ | ICSE 2024 | B |
| **CrossCodeEval** | — | 跨文件 | 4 语言 | ✗ | NeurIPS 2023 | B+ |
| **RepoBench** | — | 仓库级 | Python/Java | ✗ | ICLR 2024 | B+ |
| **DevEval** | — | 仓库级 | Python | ✗ | 2024 | B |
| **ExecRepoBench** | — | 仓库级 | — | ✗ | 2025 | B |
| **FeatBench** | — | 特性级 | — | ✗ | 2025 | B |
| **APPS** | 10,000 题 | 函数级 | Python | ✗ | NeurIPS 2021 | B（已过时） |
| **MERA Code** | 11 任务 | 多粒度 | 8 语言 | ✗ | 2025 | B |

**关键问题**：
- HumanEval/MBPP 被 LessLeak-Bench 检测到显著泄漏风险
- 语言严重偏向 Python（占 58%），Java 次之（39%），其他语言极度匮乏
- 函数级→类级→仓库级，粒度越大 Benchmark 越少，但工程实用性越强

#### 3.2.2 代码质量

| Benchmark | 规模 | 评估维度 | 发表 | 质量评级 |
|-----------|------|---------|------|---------|
| 静态分析直接度量 | — | CC、异味、重复率 | — | N/A |
| **CyberSecEval** (v1-v4) | 多维 | 安全漏洞生成倾向 | Meta 2024 | B+ |
| **SecurityEval** | — | CodeQL 安全扫描 | 2023 | B |
| **SVEN** | — | 安全代码生成 | 2023 | B- |
| **CWEval** | — | 功能+安全双维度 | 2025 | B+ |
| **SeCodePLT** | — | Agent 安全风险 | 2024 | B |
| **SecureAgentBench** | — | 真实漏洞场景 | 2025 | B |

**关键问题**：
- CyberSecEval 可复现率仅 29.4%（562/1916 漏洞样本可复现），因代码片段不完整
- 代码质量（非安全维度）缺乏专用 Benchmark，完全依赖静态分析工具链
- 工程质量评估（可维护性、可读性）尚无标准化 Benchmark

#### 3.2.3 执行效率

| Benchmark | 规模 | 评估维度 | 发表 | 质量评级 |
|-----------|------|---------|------|---------|
| **Mercury** | 1,889 任务 | 时间+内存效率 Beyond@K | NeurIPS 2024 | **A-** |
| **EffiBench** | 1,000 题 | 10 种算法类型效率 | 2024 | B+ |
| **EffiBench-X** | — | Mercury 多语言扩展 | NeurIPS 2025 | B+ |

**关键问题**：
- 效率评估高度依赖硬件环境标准化，跨平台可比性差
- 仅覆盖算法竞赛场景，缺乏工程代码效率评估

### 3.3 阶段 3：测试与验证

> **覆盖率**: ~15% | **质量**: 快速发展中
| Benchmark | 规模 | 任务类型 | 评估维度 | 发表 | 质量评级 |
|-----------|------|---------|---------|------|---------|
| **TestGenEval** | 68,647 测试，1,210 对 | 单元测试生成+补全 | 构建率、覆盖率、变异得分 | ICLR 2025 | **A-** |
| **EvalPlus** (测试维度) | 增强测试集 | 测试充分性标杆 | 测试覆盖率增益 | NeurIPS 2023 | **A** |
| **TestExplora** | — | 仓库级主动测试 | 缺陷发现率 | 2025 | B |
| **ULT Benchmark** | 3,909 函数 | 单元测试生成 | 变异得分 Mut@k | 2025 | B+ |
| **AgoneTest** | — | Java 测试自动评估 | 多维测试质量 | 2025 | B |
| **Defects4J** (测试维度) | 835 Java bugs | 回归测试验证 | P2P 回归安全性 | ISSTA 2014 | **A** |

**关键发现**：
- 最佳模型 GPT-4o 平均覆盖率仅 35.2%，变异得分 18.8%（TestGenEval）
- 大规模项目的测试生成远难于独立问题
- 测试预言质量（断言精确度）的自动化评估仍是开放问题

### 3.4 阶段 4：维护与演进

> **覆盖率**: ~16% | **质量**: 被 SWE-Bench 系列主导
#### 3.4.1 缺陷定位与修复 (APR)

| Benchmark | 规模 | 语言 | 粒度 | 发表 | 质量评级 |
|-----------|------|------|------|------|---------|
| **SWE-bench** | 2,294 issue-commit 对 | Python | 仓库级 | ICLR 2024 | B+（有严重质量问题） |
| **SWE-bench Verified** | 500 子集 | Python | 仓库级 | OpenAI 2024 | B+（仍有污染） |
| **SWE-Bench+** | 增强版 | Python | 仓库级 | 2024 | A-（修复了泄漏/弱测试） |
| **SWE-bench Pro** | — | Python | 仓库级（长期） | Scale AI 2025 | A- |
| **SWE-rebench** | 持续更新 | Python | 仓库级 | Nebius 2025 | B+ |
| **SWE-bench-C** | 179 PR | C | 仓库级 | 2025 | B |
| **SWE-bench Multilingual** | 300 任务 | 9 语言 | 仓库级 | 2025 | B+ |
| **Defects4J v2.0** | 835 bugs | Java | 方法级 | ISSTA 2014 | **A** |
| **Defects4C** | — | C/C++ | — | 2025 | B |
| **RepoFixEval** | 160 修复 | Python | 仓库级 | 2025 | B |

**SWE-bench 质量问题深度分析**：

| 问题类型 | 比例 | 具体表现 |
|---------|------|---------|
| 解决方案泄漏 | **60.83%** | Issue 描述直接/间接包含解决方案 |
| 弱测试通过 | **47.93%** | Patch 通过但并未真正修复 bug |
| 数据泄漏风险 | **>94%** | Issue 创建时间早于 LLM 知识截止日期 |
| 修复率虚高 | 12.47% → 3.97% | 过滤问题后，SWE-Agent+GPT-4 真实修复率骤降 |
| 验证器不足 | — | TestEnhancer 导致修复率下降 27~36 个百分点 |

**行业回应**：OpenAI 已宣布不再使用 SWE-bench Verified 评估前沿编码能力，转向 SWE-Bench Pro。

#### 3.4.2 程序理解

| Benchmark | 规模 | 任务类型 | 发表 | 质量评级 |
|-----------|------|---------|------|---------|
| **CRUXEval** | 800 函数 | I/O 预测 | ICML 2024 | B+ |
| **CRUXEval-X** | 19 语言 | 多语言推理 | ACL 2025 | B+ |

#### 3.4.3 代码审查

| Benchmark | 规模 | 任务类型 | 发表 | 质量评级 |
|-----------|------|---------|------|---------|
| **CodeReviewer** | 116K+ 样本，9 语言 | 审查评论生成/代码改进 | FSE 2022 | A- |
| CodeReviewer 数据质量问题 | — | "Too Noisy To Learn" | 2025 | 噪声较大 |

**关键发现**：CodeReviewer 数据集被发现存在显著噪声问题（Li et al. 2025 "Too Noisy To Learn"），审查意见与代码变更的对齐度不够精确。

### 3.5 跨阶段：Agent 与交互式开发

| Benchmark | 规模 | 评估维度 | 发表 | 质量评级 |
|-----------|------|---------|------|---------|
| **SWE-bench** 系列 | 见上 | 端到端 Issue 解决 | 见上 | B+~A- |
| **SWE-Agent** 评估 | — | Agent 架构评估 | 2024 | B+ |

---

## 4. 重点 Benchmark 深度分析

### 4.1 EvalPlus (HumanEval+/MBPP+)

**核心贡献**：通过自动生成测试输入将 HumanEval 测试扩充 80 倍、MBPP 扩充 35 倍，有效暴露 pass@k 虚高问题。

| 维度 | 评估 |
|------|------|
| Q1 学术严谨性 | **A** — NeurIPS 2023，~5000 引用 |
| Q2 数据质量 | **A** — 增强测试经人工验证 |
| Q3 抗污染 | **C** — 无防污染机制，HumanEval 已被广泛泄漏 |
| Q4 测试充分性 | **A** — 增强测试覆盖边界条件 |
| Q5 Prompt 鲁棒性 | **B-** — 单一 Prompt 模板 |
| Q6 可复现性 | **A** — 完整公开，有排行榜 |
| Q7 规模与多样性 | **C** — 仅 Python，规模偏小 |
| Q8 工业对齐度 | **C** — 算法题场景，与工业开发差距大 |

**综合评级**: **A** (功能正确性标杆，但存在明显局限)

### 4.2 LiveCodeBench

**核心贡献**：首个具备时间截止防污染机制的持续更新 Benchmark。

| 维度 | 评估 |
|------|------|
| Q1 学术严谨性 | **A** — ICLR 2025 |
| Q2 数据质量 | **A** — 来自 LeetCode/AtCoder/Codeforces |
| Q3 抗污染 | **A** — 时间截止机制，持续新增 |
| Q4 测试充分性 | **B+** — 竞赛题自带测试 |
| Q5 Prompt 鲁棒性 | **B** — 竞赛题描述相对标准化 |
| Q6 可复现性 | **A** — 公开排行榜 + 代码 |
| Q7 规模与多样性 | **B+** — 1055+ 题，仅 Python |
| Q8 工业对齐度 | **C** — 竞赛题场景 |

**综合评级**: **A** (防污染首选)

### 4.3 SWE-bench 系列

**核心贡献**：首个仓库级真实 Issue 修复 Benchmark，推动了 Agent 评估范式。

| 维度 | SWE-bench 原版 | SWE-bench Verified | SWE-Bench+ |
|------|---------------|-------------------|------------|
| Q1 学术 | A (ICLR 2024) | B+ (非正式) | B+ (OpenReview) |
| Q2 数据质量 | **D** (60.83% 解决方案泄漏) | **C** (仍有问题) | **B+** (修复泄漏) |
| Q3 抗污染 | **D** (>94% 可能泄漏) | **C** | **B** |
| Q4 测试充分性 | **D** (47.93% 弱测试) | **C+** | **A-** (TestEnhancer) |
| Q5 Prompt 鲁棒性 | B | B | B |
| Q6 可复现性 | A- | A- | A- |
| Q7 规模与多样性 | B (仅 Python) | C (500 子集) | B |
| Q8 工业对齐度 | **A** (真实 Issue) | **A** | **A** |

**综合评级**: 原版 **B+** → Verified **B+** → SWE-Bench+ **A-**

**教训**：SWE-bench 的质量问题是 Benchmark 评测领域最重要的警示案例——高影响力 Benchmark 并不等于高质量 Benchmark。

### 4.4 TestGenEval

**核心贡献**：最大规模文件级单元测试生成 Benchmark。

| 维度 | 评估 |
|------|------|
| Q1 学术严谨性 | **A** — ICLR 2025，CMU+Meta |
| Q2 数据质量 | **B+** — 来自真实开源项目 |
| Q3 抗污染 | **B** — 无主动防污染，但数据来源新 |
| Q4 测试充分性 | **A** — 含覆盖率和变异得分度量 |
| Q5 Prompt 鲁棒性 | **B** |
| Q6 可复现性 | **A** — Meta 开源 |
| Q7 规模与多样性 | **A** — 68,647 测试，11 仓库 |
| Q8 工业对齐度 | **A-** — 真实项目测试 |

**综合评级**: **A-** (测试生成评估首选)

### 4.5 Defects4J v2.0

| 维度 | 评估 |
|------|------|
| Q1 学术严谨性 | **A** — ~2500 引用，20 年社区验证 |
| Q2 数据质量 | **A** — 社区长期验证 |
| Q3 抗污染 | **C** — 历史悠久，高度泄漏风险 |
| Q4 测试充分性 | **A** — 配套完整测试套件 |
| Q5 Prompt 鲁棒性 | N/A |
| Q6 可复现性 | **A** — 标准化框架 |
| Q7 规模与多样性 | **B** — 835 bugs，仅 Java |
| Q8 工业对齐度 | **A-** — 真实项目 bug |

**综合评级**: **A** (Java APR 金标准，但污染风险高)

---

## 5. Benchmark 质量评估：多维度综合诊断

### 5.1 数据污染问题全景

数据污染是当前 Benchmark 评测生态最严重的威胁。

**LessLeak-Bench 泄漏率统计**：

| 语言 | 平均泄漏率 | 高泄漏 Benchmark 示例 |
|------|-----------|---------------------|
| Python | 4.8% | HumanEval, MBPP (来自 LeetCode 等公开平台) |
| Java | 2.8% | QuixBugs (100%), Defects4J (部分) |
| C/C++ | 0.7% | 相对安全 |

**泄漏根因分析**：
1. **预训练数据直接包含 Benchmark 数据**：GitHub 公开仓库、竞赛平台数据
2. **Benchmark 构建来源与训练数据重叠**：LeetCode、Stack Overflow 同时被用于 Benchmark 构建和 LLM 预训练
3. **时间失效**：>94% 的 SWE-bench Issue 创建于 LLM 知识截止日期之前

**防污染策略分类**：

| 策略 | 代表 Benchmark | 有效性 | 局限 |
|------|---------------|--------|------|
| 时间截止机制 | LiveCodeBench | 高 | 新数据最终也会泄漏 |
| 持续更新 | LiveCodeBench, SWE-rebench | 高 | 维护成本高 |
| 数据扰动/变换 | CodeCleaner | 中 | 可能改变任务语义 |
| 泄漏检测+清洗 | LessLeak-Bench | 中 | 事后补救，非预防 |
| 私有测试集 | SWE-bench Pro (商业集) | 高 | 不利于学术复现 |

### 5.2 Prompt 鲁棒性问题

Zheng et al. (2025) 的语义变异实验揭示了一个被严重低估的问题：

- 对 8 个 Benchmark 任务的 10 个 LLM 进行测试
- 每个任务生成 100 个语义等价的 Prompt 变体
- **微小的 Prompt 变化导致显著性能波动和排名不一致**
- 当前绝大多数 Benchmark 仅使用单一 Prompt 模板

**启示**：任何严肃的评测都应在多个 Prompt 变体上取均值或中位数。

### 5.3 测试充分性问题

SWE-Bench+ 的分析提供了最有力的证据：

- **47.93% 的"通过"实际上是假阳性**——Patch 通过了弱测试但未真正修复 Bug
- TestEnhancer 增强测试后，修复率平均下降 27~36 个百分点
- 这意味着当前 Agent 的真实修复能力被严重高估

**EvalPlus 的启示**：80x 测试增强使 pass@k 显著下降，证明"通过率"与"真实正确率"之间存在巨大鸿沟。

### 5.4 语言与任务多样性

**语言覆盖偏差**（HOW2BENCH 统计）：

| 语言 | Benchmark 覆盖率 | 问题 |
|------|----------------|------|
| Python | **58%** | 过度集中 |
| Java | **39%** | 相对充足 |
| JavaScript/TypeScript | ~10% | 不足 |
| C/C++ | ~8% | 不足 |
| Go/Rust/其他 | <5% | 严重缺乏 |

**任务类型偏差**：
- 代码生成占 **36.13%**，其次是程序修复 9.85%
- 需求工程、软件设计、代码审查等任务 Benchmark 极度匮乏

---

## 6. 关键发现与问题诊断

### 6.1 结构性问题

1. **SDLC 覆盖严重失衡**：实现阶段 ~61% vs 需求阶段 ~5% vs 设计阶段 ~3%
2. **语言严重偏科**：Python 58% + Java 39% = 97%，其他 49 种语言共享 3%
3. **粒度断层**：函数级 Benchmark 丰富，类级和仓库级稀缺
4. **评估维度单一**：超过 60% 的 Benchmark 仅评估功能正确性 (pass@k)

### 6.2 质量性问题

5. **数据污染普遍**：80% 的 Benchmark 忽视数据污染风险
6. **测试充分性不足**：SWE-bench 47.93% 假阳性是冰山一角
7. **可复现性危机**：96.4% 未提供完整实验环境
8. **Prompt 敏感性被忽视**：几乎所有 Benchmark 使用单一 Prompt

### 6.3 方法论问题

9. **缺乏 Benchmark 质量元评估标准**：HOW2BENCH 是首个尝试，但尚未被广泛采纳
10. **传播效应未被管控**：18% 的 Benchmark 被复用为下游数据源，缺陷放大
11. **静态vs动态评估**：绝大多数 Benchmark 是静态快照，缺乏持续更新机制

---

## 7. 开放问题与研究机会

### 7.1 Benchmark 覆盖盲区

基于本调研的全景扫描，以下 SE 任务在 Benchmark 层面存在显著空白：

| 空白领域 | 现状 | 研究机会 |
|---------|------|---------|
| **需求歧义检测** | 无专用 Benchmark | 构建含歧义需求的标注数据集，评估 LLM 识别并澄清歧义的能力 |
| **架构设计评估** | 仅 DevBench (22 仓库) 间接覆盖 | 需要专门评估模块划分、耦合内聚、设计模式选择的 Benchmark |
| **代码工程质量** | 完全依赖静态分析工具，无标准化 Benchmark | 可维护性、可读性、技术债务的评测数据集 |
| **跨语言评测** | Python 58% + Java 39% = 97% | Rust、Go、TypeScript 等现代语言的覆盖 |
| **代码审查** | CodeReviewer 存在噪声问题 | 高质量审查意见数据集，含可操作性标注 |
| **非功能属性** | 效率仅限算法题场景 | 工程代码的性能、可扩展性、资源消耗评估 |

### 7.2 Benchmark 质量方法论的前沿方向

| 方向 | 代表工作 | 开放挑战 |
|------|---------|---------|
| **Benchmark 质量元评估** | HOW2BENCH (55 条清单) | 尚未被社区广泛采纳，需要标准化推广 |
| **数据污染检测与缓解** | LessLeak-Bench, CodeCleaner | 预防优于检测，动态 Benchmark 维护成本高 |
| **Prompt 鲁棒性评估** | Zheng et al. 语义变异 | 如何在不改变任务语义的前提下系统化生成变体 |
| **测试充分性增强** | SWE-Bench+ TestEnhancer | 自动化测试增强的泛化性和成本问题 |
| **Benchmark 传播效应** | HOW2BENCH 发现 18% 级联复用 | 建立 Benchmark 谱系追踪机制 |

### 7.3 Benchmark 设计的新兴范式

**从静态到动态**：
- **持续更新型**：LiveCodeBench、SWE-rebench 代表了从"一次性快照"到"持续演进"的范式转变
- **对抗型**：EvoCodeBench 每半年更新以抵御数据污染，但维护成本可观
- **多层级型**：SWE-bench → SWE-bench Verified → SWE-Bench+ → SWE-bench Pro 的迭代修复链

**从单维到多维**：
- 当前 Benchmark 绝大多数仅评估单一维度（功能正确性），缺乏同时评估正确性+效率+安全+可维护性的综合型 Benchmark
- CWEval（功能+安全双维度）是一个初步尝试

**从函数到系统**：
- 粒度演进：函数级 → 类级 → 文件级 → 仓库级 → Agent 级
- 越高粒度的 Benchmark 越贴近工程实践，但构建难度和评估成本也指数级增长

### 7.4 尚未解决的根本性问题

1. **评测指标的信度 (Reliability)**：同一 Benchmark 上微小 Prompt 变化导致排名剧烈波动，如何定义可信的评测结论？
2. **评测指标的效度 (Validity)**：pass@k 在算法题上的表现与工程实践中的代码质量是否正相关？缺乏实证研究
3. **Benchmark 的半衰期**：数据污染使 Benchmark 的有效期越来越短，如何建立可持续的评测基础设施？
4. **评测公平性**：不同模型的训练数据不公开，无法确定哪些模型"见过"测试数据，如何保证公平比较？
5. **工业-学术鸿沟**：学术 Benchmark 侧重算法能力，工业需求侧重工程质量、团队协作、长期可维护性，两者差距如何弥合？

---

## 8. 参考文献

### 元综述与质量评估

1. Hu X, Niu F, Chen J, et al. **"Assessing and Advancing Benchmarks for Evaluating Large Language Models in Software Engineering Tasks"**. arXiv:2505.08903, 2025. [[Paper]](https://arxiv.org/abs/2505.08903)
2. Cao J, Chan Y-K, Ling Z, et al. **"Rigor, Reliability, and Reproducibility Matter: A Decade-Scale Survey of 572 Code Benchmarks"**. arXiv:2501.10711, 2025. [[Paper]](https://arxiv.org/abs/2501.10711)
3. Wang K, Li T, Zhang X, et al. **"Software Development Life Cycle Perspective: A Survey of Benchmarks for Code Large Language Models and Agents"**. arXiv:2505.05283, 2025. [[Paper]](https://arxiv.org/abs/2505.05283)
4. Siddiq ML, Dristi S, Saha J, Santos JCS. **"The Fault in our Stars: Quality Assessment of Code Generation Benchmarks"**. SCAM 2024. [[Paper]](https://arxiv.org/abs/2404.10155)
5. Zheng et al. **"Re-Evaluating Code LLM Benchmarks Under Semantic Mutation"**. arXiv:2506.17369, 2025. [[Paper]](https://arxiv.org/abs/2506.17369)

### 数据污染与泄漏

6. Zhang et al. **"LessLeak-Bench: A First Investigation of Data Leakage in LLMs Across 83 Software Engineering Benchmarks"**. arXiv:2502.06215, 2025. [[Paper]](https://arxiv.org/abs/2502.06215)
7. Aleithan et al. **"SWE-Bench+: Enhanced Coding Benchmark for LLMs"**. arXiv:2410.06992, 2024. [[Paper]](https://arxiv.org/abs/2410.06992)
8. **"Benchmarking Large Language Models Under Data Contamination: A Survey from Static to Dynamic Evaluation"**. arXiv:2502.17521, 2025. [[Paper]](https://arxiv.org/abs/2502.17521)

### 功能正确性 Benchmark

9. Liu J, et al. **"Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation"** (EvalPlus). NeurIPS 2023.
10. Jain N, et al. **"LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code"**. ICLR 2025. [[Site]](https://livecodebench.github.io/)
11. Zhuo T, et al. **"BigCodeBench: Benchmarking Code Generation with Diverse Function Calls"**. ICLR 2025.
12. Du M, et al. **"Mercury: A Code Efficiency Benchmark for Code Large Language Models"**. NeurIPS 2024. [[Paper]](https://arxiv.org/abs/2402.07844)

### 测试生成 Benchmark

13. Varshney N, et al. **"TestGenEval: A Real World Unit Test Generation and Test Completion Benchmark"**. ICLR 2025. [[Paper]](https://arxiv.org/abs/2410.00752)

### APR & 维护 Benchmark

14. Jimenez CE, et al. **"SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"**. ICLR 2024.
15. Just R, et al. **"Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs"**. ISSTA 2014.
16. **"SWE-rebench: A continuously updated benchmark for SWE LLMs"**. Nebius, 2025.

### 代码审查 & 安全

17. Li Z, et al. **"Automating Code Review Activities by Large-Scale Pre-training"** (CodeReviewer). FSE 2022.
18. Bhatt M, et al. **"Purple Llama CyberSecEval: A Benchmark for Evaluating the Cybersecurity Risks of Large Language Models"**. Meta 2024.

### 仓库级 & Agent Benchmark

19. Li X, et al. **"EvoCodeBench: An Evolving Code Generation Benchmark Aligned with Real-World Code Repositories"**. NeurIPS 2024. [[Paper]](https://arxiv.org/abs/2404.00599)
20. Li B, et al. **"DevBench: A Comprehensive Benchmark for Software Development"**. ACL 2024.
21. Liu X, et al. **"RepoBench: Benchmarking Repository-Level Code Auto-Completion Systems"**. ICLR 2024. [[Paper]](https://arxiv.org/abs/2306.03091)

### APR 综述

22. **"A Survey of LLM-based Automated Program Repair: Taxonomies, Design Paradigms, and Applications"**. arXiv:2506.23749, 2025. [[Paper]](https://arxiv.org/abs/2506.23749)
23. **"A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System"**. arXiv:2510.09721, 2025. [[Paper]](https://arxiv.org/abs/2510.09721)

---

*调研完成日期: 2026-03-16*
*版本: v1.0*
*调研范围: 覆盖 2014-2026 年公开 SE/代码 LLM 评测 Benchmark*

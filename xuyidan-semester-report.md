# 许一丹 2025-2026 上半学期工作汇报

## 概览

本学期工作分为两个部分：（1）辅助学长完成综述论文 Efficient LLM4SE Survey 的 Evaluation 章节；（2）独立开展低资源语言（Lua）代码生成增强实验。

---

## 第一部分：辅助完成综述 Evaluation 章节

### 1.1 综述背景

参与的综述论文题为 *Efficient Large Language Models for Software Engineering: A Survey on Models, Patterns, and Evaluation*，拟投稿至 TSE/TOSEM。论文系统梳理了 LLM 在软件工程中的效率优化技术，围绕三个研究问题展开：

- RQ1：LLM4SE 中使用了哪些效率技术？在模型生命周期中如何分布？
- RQ2：这些技术如何映射到不同 SE 工作负载？有哪些反复出现的效率模式？
- RQ3：评估效率的指标和报告实践有哪些？差距在哪里？

许一丹主要参与 RQ3（Evaluation）部分的撰写与数据整理工作。

### 1.2 RQ3 章节内容与贡献

RQ3 章节（Section: Evaluation of Efficiency in AI4SE）包含四个子节，具体工作如下：

#### (a) 过程效率指标梳理（Process Efficiency Metrics）

- 整理了判别式任务和生成式任务的效率指标体系
- 判别式任务：latency、throughput、peak memory，配合 accuracy/F1
- 生成式任务：TTFT（首 token 时间）、端到端延迟、tokens/s、资源利用率
- 特别关注了代码场景下的尾延迟（P95/P99）对 IDE 交互体验的影响
- 整理了能耗和碳排放作为新兴过程指标的相关文献

#### (b) 结果质量与效率指标（Result Quality and Efficiency Metrics）

- 整理了代码生成任务的功能正确性评估方式：pass@k、BLEU、CodeBLEU、ROUGE
- 梳理了效率感知评估的核心理念：明确质量-成本权衡（quality-cost trade-off）
- 例如：固定 token 预算下的 pass@k、accuracy-per-FLOP 曲线
- 补充了 energy-per-task 和 carbon-per-task 等新兴指标的文献调研

#### (c) 基准数据集整理（Tools and Benchmark Datasets）

- 构建了 Table: Representative Benchmarks for Efficiency Evaluation in AI4SE
- 区分了两类基准：
  - 效率导向型（efficiency-oriented）：EffiBench、PIE、SWE-Effi
  - 效率兼容型（efficiency-compatible）：HumanEval、MBPP、SWE-bench、Defects4J 等
- 整理了每个基准的规模、任务类型、效率指标和评估角度
- 分析了当前基准测试实践的异质性问题

#### (d) 报告检查清单与合规性分析（Reporting Checklist and Compliance）

- 协助设计了 Compact Reporting Checklist，涵盖 6 个维度：
  - Workload & Data、Model & Prompting、Decoding & Serving
  - Hardware & Software、Measurement Protocol、Reporting Format
- 对综述收录的全部主要研究进行了 checklist 合规性编码，生成合规率统计表
- 关键发现：
  - 92% 的研究报告了模型名称/版本
  - 85% 报告了硬件信息
  - 仅 39% 报告了 serving 配置（batch、concurrency、cache）
  - 仅 12% 报告了能耗/碳排放指标
- 这一分析揭示了当前 AI4SE 效率评估中报告实践的系统性缺失

### 1.3 工作总结

通过参与综述的 Evaluation 章节，系统学习了：
- AI4SE 领域效率评估的指标体系和方法论
- 学术论文中 benchmark 整理和 compliance analysis 的规范流程
- 综述写作中数据驱动论证的方法

---

## 第二部分：低资源语言代码生成增强实验（kNM-LM for CP-Lua）

### 2.1 研究目标

在不进行全量参数微调的前提下，通过 kNN-LM 技术构建解耦的算法逻辑纠错数据库（Datastore），在推理阶段实时修正大语言模型生成 Lua 算法代码时的逻辑偏差，提升 Pass@1 准确率。

选择 Lua 作为目标语言的原因：Lua 是典型的低资源编程语言，LLM 训练语料中 Lua 代码占比极低，模型在 Lua 代码生成上表现较差，适合验证 kNN-LM 纠错方案的有效性。

### 2.2 技术方案

- 基座模型：Qwen3-4B-Instruct（约 40 亿参数，hidden_size=2560）
- 核心方法：kNN-LM（k-Nearest Neighbor Language Model）
  - Mistake Mining：在训练数据上运行模型前向传播，捕获预测错误的 token 位置，将 Hidden State 作为 Key、正确 Token ID 作为 Value 存入 Faiss 向量数据库
  - kNN 推理：推理时检索最近邻，计算 kNN 概率分布并与模型原始概率插值融合
  - 动态 Lambda：λ = base_λ × (1 - confidence)，模型越自信 kNN 权重越低
- 评测方式：Ag-LiveCodeBench-X 数据集 + Agnostics Docker 沙箱端到端评测

### 2.3 实验迭代过程

共经历 4 个主要迭代阶段，完成 11 组对比实验：

| 阶段 | 方案 | Pass@1 | 关键发现 |
|------|------|--------|---------|
| v1 | 静态 λ=0.25, temp=1.0 | 9.0% | kNN 在模型自信位置大量引入噪声，低于基线 |
| v2 温度调优 | 提升 kNN 温度至 100.0 | - | kNN 概率分布更平滑，减少单个近邻过度影响 |
| v3 动态 λ | 置信度门控 | 13.0% | 追平 Baseline，消除高置信度干扰 |
| v4 性能优化 | λ<0.01 快速跳过 | 10.0% | 运行时错误下降但整体略降 |

Baseline（纯 Qwen3-4B）Pass@1 = 13.0%

### 2.4 关键发现

逐题分析（kNN v3 vs Baseline）显示 kNN 已具备纠错能力：

kNN 新增通过 3 题：
- 1899_A：修正条件判断逻辑错误
- abc305_a：修正数学计算逻辑
- abc320_a：修正 IO 解析类型错误

kNN 丢失 3 题：
- abc311_b：引入 for 循环边界类型错误
- abc307_d：导致括号不匹配
- 1899_D：引入 Python 风格的整除运算符（跨语言干扰）

核心结论：kNN 在修正 IO 格式和简单数学逻辑上有效，但在复杂语法结构上可能引入跨语言干扰。

### 2.5 瓶颈分析

1. 数据量不足：当前 Datastore 仅 24,245 条 key-value 对，远低于 kNN-LM 原论文的百万级规模（不足万分之一）
2. 领域偏移：训练数据主要来自 Neovim 插件和通用算法库，缺少竞赛场景特有的 IO 处理和边界条件模式，与评测集（算法竞赛题）存在明显差距

### 2.6 数据扩充计划

| 数据来源 | 预估数据量 | 获取难度 | 质量保障 |
|---------|-----------|---------|---------|
| Codeforces Lua AC 提交 | 500-2000 条 | 低 | 高（OJ 验证） |
| Python→Lua 跨语言翻译 | 10k-50k 条 | 中 | 中（需沙箱验证） |
| LeetCode Lua 题解 | 200-500 条 | 低 | 高 |
| Rosetta Code Lua 示例 | 300-800 条 | 低 | 高 |

### 2.7 下一步计划（4 周冲刺）

| 阶段 | 核心任务 | 交付物 |
|------|---------|--------|
| Week 1 数据周 | 爬取 Codeforces Lua AC 代码；跨语言翻译 Python→Lua 并沙箱验证 | Lua-CP-Dataset-v1 |
| Week 2 挖掘周 | 在扩充数据上重新跑 Mistake Mining | Mistake-Datastore-v2 |
| Week 3 系统周 | 系统性调参（λ, temp, k）；实现基于 token 类型的条件触发 | kNM-LM-Inference-v2 |
| Week 4 评测周 | 完整评测 + 撰写实验报告 | 最终实验报告 |

---

## 学期工作总结

| 维度 | 内容 |
|------|------|
| 综述协作 | 完成 RQ3 Evaluation 章节的数据整理、基准表格构建、checklist 合规性分析 |
| 独立实验 | 搭建 kNM-LM 实验框架，迭代 4 个版本，完成 11 组对比实验 |
| 技术积累 | 掌握 kNN-LM、Faiss 向量检索、Agnostics 沙箱评测等技术栈 |
| 学术训练 | 学习综述写作方法、benchmark 整理规范、实验设计与分析 |

### 已完成的里程碑

1. 综述 Evaluation 章节初稿完成，包含 3 张表格和合规性分析
2. kNM-LM 项目框架搭建完毕，端到端流程跑通
3. 动态 Lambda 机制验证有效，kNN 纠错能力得到逐题级别的验证
4. 明确了数据量不足是当前核心瓶颈，制定了可行的数据扩充方案

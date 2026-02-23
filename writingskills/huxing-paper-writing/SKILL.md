---
name: huxing-paper-writing
description: 基于胡星老师（Xing Hu）50篇 CCF-A 论文全文PDF深度分析的软件工程论文英文写作技巧指南。覆盖标题→摘要→引言→方法→实验→讨论→威胁→相关工作→结论全流程，含可复用句式模板库。仅收录 CCF-A 顶会顶刊：ICSE(17)/FSE(6)/ASE(10)/ISSTA(4)/TSE(3)/TOSEM(10)共50篇全文。4次 Distinguished Paper Award。
---

# 胡星老师论文英文写作技巧指南（Full-Text Analysis v2.0）

> 本指南基于胡星老师（浙江大学副教授）50 篇已下载全文 PDF 的逐节深度分析。
> 仅收录 CCF-A 顶会顶刊：ICSE(17)/FSE(6)/ASE(10)/ISSTA(4)/TSE(3)/TOSEM(10)。
> 胡星老师获得 4 次 Distinguished Paper Award（ICPC 2018, ICSE 2024×2, MSR 2024）。

---

## 0. 研究方向概览

胡星老师的研究聚焦于 **AI for SE（智能软件工程）**，主要涵盖五大方向：

| 方向 | 代表性工作 | 典型发表 |
|------|-----------|----------|
| **代码智能** | 代码注释生成(EditSum)、代码补全(SkCoder)、代码搜索、代码克隆检测(C3)、代码编辑(CodeEditor) | ICSE'22, ICSE'24, TOSEM'21, ASE'21 |
| **软件测试** | 单元测试生成/迁移/重构(MUT, CleanTest)、测试用例更新(CEPROT)、模糊测试(HFuzzer) | FSE'25×4, ASE'23, ASE'25, ISSTA'25 |
| **软件安全** | 漏洞检测(EPVD)、补丁存在性测试(PS3, PPT4J, REACT)、漏洞利用迁移(Diffploit)、静默修复识别(CoLeFunDa) | ICSE'24×3, ICSE'25, ICSE'26×2, TSE'23 |
| **LLM4SE** | LLM 鲁棒性(CREME, NLPerturbator)、代码推理(REval)、基准评估(RealisticCodeBench)、幻觉检测(HFuzzer) | ICSE'25, ICSE'26, ASE'25, TOSEM'25 |
| **经验研究** | 开发者期望(ICSE'22)、日志可读性(ASE'23)、漏洞披露管理(TOSEM'25)、LLM时代SE挑战(TOSEM'25) | ICSE'22, ASE'23, ISSTA'24, TOSEM'25 |

---

## 1. 标题（Title）写作模式

### 1.1 七种标题结构（按频率排序）

基于 50 篇全文分析的真实分布：

| 模式 | 占比 | 示例 | 适用场景 |
|------|------|------|----------|
| **工具名 + 冒号 + 功能描述** | 36% (18篇) | `PS3: Precise Patch Presence Test based on Semantic Symbolic Signature` | 提出新工具/方法（最常用） |
| **动名词/动作短语** | 18% (9篇) | `Automating User Notice Generation for Smart Contract Functions` | 自动化类工作 |
| **隐喻/格言/反直觉** | 10% (5篇) | `Less is More: On the Importance of Data Quality for Unit Test Generation` | 有反直觉发现 |
| **问句式** | 8% (4篇) | `Reasoning Runtime Behavior of a Program with LLM: How Far Are We?` | 探索性/评估性研究 |
| **经验研究/从业者视角** | 8% (4篇) | `Practitioners' Expectations on Automated Code Comment Generation` | 实证研究/调研 |
| **问题陈述/场景引入** | 8% (4篇) | `Similar but Patched Code Considered Harmful` | 揭示已知问题的新维度 |
| **描述性短语** | 12% (6篇) | `Vulnerability Detection via Multiple-Graph-Based Code Representation` | 方法描述型 |

### 1.2 标题写作规则（基于全文统计）

- 长度控制在 **8-18 个单词**
- 工具名用大驼峰或全大写缩写（PS3, PPT4J, CREME, HFuzzer, MUT, C4, Safe4U, DepRadar, CoLeFunDa）
- 工具名倾向于有含义的缩写或谐音（PPT4J = Patch Presence Test for Java, C4 = Contrastive Cross-language Code Clone, CREME = Code LLM Robustness Enhancement via Model Editing）
- 冒号后常用 **动名词短语** 或 **名词短语** 描述核心功能
- 问句式标题适合评估/探索类工作，常以 "How Far/How Much/Are They" 开头
- 反直觉标题（Less is More, Fight Fire with Fire, Easy over Hard）适合有意外发现的工作
- 经验研究标题常用 "Practitioners' Expectations on..." 或 "An Empirical Study on..."

### 1.3 可复用标题模板

```
[ToolName]: [Noun Phrase] for/via/based on [Key Technique]
[ToolName]: [Verb-ing] [Task] via/through/by [Key Technique]
[Verb-ing] [Target] [Preposition] [Technique/Approach]
[Concept/Proverb]: [Subtitle explaining the insight]
[Question]? [Subtitle with scope]
An Empirical Study on/of [Topic] in/for [Context]
[Practitioners'/Developers'] Expectations on [Topic]
```

---

## 2. 摘要（Abstract）写作模式

### 2.1 标准四段式结构

基于 50 篇全文分析，**94% 的摘要包含具体数字结果**：

| 句序 | 功能 | 典型长度 | 占比 |
|------|------|----------|------|
| S1 | **背景+重要性** | 1-2句 | 20% |
| S2 | **现有方法不足（Gap）** | 1-2句 | 20% |
| S3 | **本文方法概述** | 2-3句 | 30% |
| S4 | **实验结果+数字** | 2-3句 | 25% |
| S5 | **结论/启示（可选）** | 0-1句 | 5% |

### 2.2 各句位的句式模板库（从全文提取的真实句式）

**S1 背景句：**
```
[Task] is crucial/critical for [ensuring/improving] [Goal] in [Domain].
  → "Vulnerability disclosure is crucial for ensuring the security and reliability of OSS."
[Activity] has attracted increasing attention due to [Trend].
  → "Code generation with LLMs has attracted increasing attention."
With the rapid advancement of [Technology], [Task] has become increasingly important.
  → "With the increasing adoption of LLMs, testing their reliability has become pressing."
[Problem] poses significant challenges to [stakeholders].
  → "Package hallucinations pose significant security risks to developers."
```

**S2 Gap句（胡星老师特色——常从开发者实践角度切入）：**
```
However, existing approaches suffer from [Limitation], which limits their practical adoption.
  → "However, existing methods rely on syntax-level information, which may not hold across different compilation options."
Despite the progress, little is known about [specific aspect from practitioners' perspective].
  → "Despite the progress, little is known about practitioners' expectations on code comment generation."
Unfortunately, [existing method] may [fail/introduce/overlook] [specific problem] in practice.
  → "Unfortunately, existing tools may introduce false positives due to similar-but-patched code."
A key challenge is that [specific technical challenge], which existing methods fail to address.
  → "A key challenge is that partial code lacks definitions and dependencies, which existing tools fail to handle."
```

**S3 方法句：**
```
In this paper, we propose [ToolName], a [adjective] approach/framework to [Task] by [Mechanism].
  → "We propose PS3, which leverages symbolic emulation to extract semantic-level signatures."
To address this challenge, we design [ToolName], which [key mechanism].
  → "To address this, we design CREME, which identifies robustness-sensitive layers via causal intervention."
Specifically, [ToolName] first [Step1], then [Step2], and finally [Step3].
  → "Specifically, DepRadar first extracts defect semantics, then generates defect patterns, and finally analyzes downstream impact."
[ToolName] consists of [N] main components: (1) ..., (2) ..., and (3) ...
  → "CleanTest consists of three filters: (1) syntax filter, (2) relevance filter, and (3) coverage filter."
```

**S4 结果句（94% 的论文包含数字）：**
```
We evaluate [ToolName] on [N datasets/subjects]. Results show that [ToolName] outperforms [baseline] by [X%].
  → "On a dataset of 62 CVEs and 3,631 pairs, PS3 achieves F1 of 0.89, improving over SOTA by 33%."
Experimental results demonstrate that [ToolName] achieves [metric], improving over the state-of-the-art by [X%].
  → "Results show CleanTest improves branch coverage by 67% on average across four LLMs."
Our extensive experiments on [N subjects] show that [ToolName] can effectively [goal].
  → "Evaluation on 157 PRs shows DepRadar achieves 90% precision in defect identification."
```

**S5 结论句（可选，经验研究中常用）：**
```
Our findings provide practical guidelines/implications for [practitioners/researchers].
  → "Our findings reveal significant gaps between practitioners' preferences and actual practices."
We release our tool/dataset at [URL] to facilitate future research.
```

### 2.3 摘要写作检查清单

- [ ] 是否包含至少 1 个具体数字结果？（50 篇中 94% 包含）
- [ ] 是否有明确的 "we propose/present/design/conduct" 动作动词？
- [ ] Gap 句是否指向可测量的失败或实践中的具体痛点？
- [ ] 方法描述是否提到核心机制关键词？
- [ ] 总长度是否在 150-250 词之间？
- [ ] 经验研究是否在结尾提到 implications？

---

## 3. 引言（Introduction）写作模式

### 3.1 标准五段式结构

基于全文分析，引言通常为 **5-7 段**，**86% 包含 Motivating Example**：

| 段落 | 功能 | 内容要点 |
|------|------|----------|
| P1 | **任务背景+重要性** | 用实际开发场景或行业数据说明问题重要性 |
| P2 | **现有方法综述** | 简要介绍 2-3 类现有方法 |
| P3 | **现有方法的关键不足** | 指出具体失败模式，常配合 Motivating Example |
| P4 | **本文方法概述+核心 Insight** | 说清"做了什么、为什么有效" |
| P5 | **贡献点列表** | 3-4 条（48% 为 3 条，40% 为 4 条） |
| P6 | **论文组织（可选）** | "The rest of this paper is organized as follows..." |

### 3.2 各段的句式模板（从全文提取）

**P1 背景段开头（胡星老师特色——常从实践需求出发）：**
```
[Task/Activity] is a fundamental/critical task in modern software development.
  → "Unit testing is crucial for software development, but writing tests is time-consuming."
In practice, developers frequently need to [Activity], which is [important/challenging].
  → "In practice, developers frequently need to assess whether security patches are applied."
With the increasing adoption of [Technology], [Problem] has become a pressing concern.
  → "With the increasing adoption of LLMs for code generation, package hallucinations have become a pressing concern."
[Problem] is one of the most important challenges facing [the SE community].
  → "Vulnerability disclosure management is one of the most important challenges facing OSS maintainers."
```

**P3 不足段（Motivation 核心，86% 配合 Motivating Example）：**
```
However, these approaches have several limitations.
First, [Method] relies on [Assumption], which may not hold in real-world scenarios.
  → "First, existing methods rely on syntactic similarity, which fails when compilation options differ."
To illustrate this limitation, consider the example shown in Figure 1.
  → "Figure 1 shows a real CVE where existing tools fail to distinguish patched from vulnerable code."
Despite their effectiveness, existing methods still face challenges in [Aspect].
  → "Despite their effectiveness, existing LLMs are highly sensitive to prompt perturbations."
```

**P4 方法概述段：**
```
To address the above limitations, we propose [ToolName], a novel [type] approach that [key mechanism].
  → "To address these limitations, we propose CREME, which identifies robustness-sensitive layers via causal intervention and performs lightweight parameter editing."
The key insight behind [ToolName] is that [Observation from practice/data].
  → "The key insight is that semantic-level signatures remain stable across different compilation options."
Specifically, [ToolName] consists of [N] main phases: (1) ..., (2) ..., and (3) ...
Unlike existing methods that [limitation], [ToolName] [advantage] by leveraging [technique].
  → "Unlike Lexecutor that uses predefined dummy values, SelfPiCo dynamically learns from execution feedback."
```

**P5 贡献点列表（48% 为 3 条，40% 为 4 条，10% 为 2 条）：**
```
The main contributions of this paper are as follows:
• We propose [ToolName], a [adjective] approach to [Task]. To the best of our knowledge, this is the first work that [novelty claim].
• We design [specific component/technique] to [specific purpose].
• We conduct extensive experiments on [N] [subjects] and demonstrate that [ToolName] outperforms [N] state-of-the-art baselines.
• We release our code and data at [URL] to facilitate future research.
```

### 3.3 引言写作的关键技巧

1. **从实践者视角切入**——胡星老师的多篇论文（ICSE'22, ASE'23, ISSTA'24, ISSTA'25）以开发者调研/期望为出发点
2. **Motivating Example 是标配**——86% 的论文包含 Motivating Example，通常用 Figure 1 展示现有方法的具体失败案例
3. **Gap 必须可测量**——不是 "has not been studied"，而是具体的技术失败（如 "76.2% false positive rate"）或实践痛点
4. **Insight 来自观察**——常基于对真实数据/代码的观察得出核心洞察
5. **贡献点必须可验证**——每条贡献对应后文的一个章节或实验

---

## 4. 方法（Approach/Methodology）写作模式

### 4.1 标准结构

```
Section 3: [Approach Name]
  3.1 Overview (含 Overview Figure)
  3.2 Phase/Component 1: [Name]
  3.3 Phase/Component 2: [Name]
  3.4 Phase/Component 3: [Name]
```

### 4.2 Overview 段写法

**必须包含一张 Overview Figure**：

```
Figure 2 presents the overall framework/workflow of [ToolName].
[ToolName] takes [Input] as input and produces [Output].
The approach consists of [N] main phases/components:
(1) [Phase1], which [function];
(2) [Phase2], which [function]; and
(3) [Phase3], which [function].
```

### 4.3 子模块描述模板

```
[Phase Name]. Given [input], this phase aims to [goal].
The key challenge in this phase is [challenge].
To address this, we [technique/strategy].
Specifically, we first [Step1]. Then, we [Step2]. Finally, we [Step3].
```

### 4.4 方法章节的关键技巧（胡星老师特色）

1. **先给全景图再给细节**——Overview Figure 是必备项
2. **每个子模块开头说"为什么需要这一步"**——先 why 再 how
3. **善用 LLM/Agent 技术描述**——近年工作大量使用 LLM，描述时注重 prompt 设计和 chain-of-thought 的解释
4. **Design choice 要解释**——为什么选这个模型/技术？常用消融实验来支撑
5. **多 Agent 框架描述**——近期工作（如 DepRadar, IntentTester）采用多 Agent 架构，需清晰描述 Agent 间的协作机制
6. **LLM-in-the-loop 模式**——SelfPiCo 首创的交互式执行模式，LLM 从执行反馈中持续学习

---

## 5. 实验（Evaluation/Experiment）写作模式

### 5.1 RQ 驱动的实验设计

基于全文分析，**80% 的论文使用 RQ 驱动评测**。典型 RQ 套件：

| RQ类型 | 模板 | 出现频率 |
|--------|------|----------|
| **RQ1 有效性** | How effective is [ToolName] compared with state-of-the-art baselines? | 100% |
| **RQ2 消融** | How does each component of [ToolName] contribute to its effectiveness? | ~70% |
| **RQ3 泛化/效率** | How generalizable/efficient is [ToolName]? | ~50% |
| **RQ4 实用性** | Can [ToolName] help developers in practice? (case study/user study) | ~40% |
| **RQ5 参数敏感性** | How sensitive is [ToolName] to [hyperparameter]? | ~25% |

### 5.2 实验设置（Experimental Setup）模板

```
4.1 Research Questions
4.2 Datasets / Subjects / Benchmarks
4.3 Baselines / Compared Approaches
4.4 Evaluation Metrics
4.5 Implementation Details
```

**数据集描述模板：**
```
We conduct experiments on [N] widely-used/real-world datasets/benchmarks.
Table 1 summarizes the statistics of our experimental subjects.
[Dataset1] is collected from [Source] and contains [N] [items].
We choose these datasets because (1) they are widely used in prior studies [refs], and (2) they cover diverse [characteristics].
```

**基线选择模板：**
```
We compare [ToolName] with [N] state-of-the-art baselines:
(1) [Category1]-based: [Baseline1] [ref], [Baseline2] [ref];
(2) [Category2]-based: [Baseline3] [ref], [Baseline4] [ref].
We select these baselines because they represent the most recent and competitive approaches.
For fair comparison, we use the same [settings/data splits] for all approaches.
```

**评估指标模板：**
```
Following prior studies [refs], we adopt [Metric1], [Metric2], and [Metric3] as evaluation metrics.
[Metric1] measures [what it measures]. A higher/lower [Metric1] indicates better performance.
```

### 5.3 结果呈现模式

**表格设计规范：**
- 最优值用 **加粗**
- 次优值用 _下划线_（部分论文）
- 提升百分比用 `↑X%` 或 `(+X%)`
- 表格标题格式：`Table N: [Description]. The best results are highlighted in bold.`

**结果段落的标准写法（Answer to RQ 模式）：**
```
**Answer to RQ1:** Table 2 presents the comparison results.
We can observe that [ToolName] outperforms all baselines across [all/most] metrics.
Specifically, [ToolName] achieves [value] in [Metric], which improves over the best baseline [Name] by [X%].
The improvement is statistically significant (p-value < 0.05).
The reason is that [explanation of why our method works better].
```

**消融实验结果模板：**
```
**Answer to RQ2:** To evaluate the contribution of each component, we design [N] variants:
- [ToolName]-w/o-[Component1]: removing [Component1]
- [ToolName]-w/o-[Component2]: removing [Component2]
Table 3 shows the results. Removing [Component1] leads to a [X%] decrease in [Metric], indicating that [Component1] plays an important role.
```

### 5.4 统计检验使用

胡星老师的 TSE/TOSEM 论文中常用的统计方法：
- **Wilcoxon signed-rank test**：配对比较（最常用）
- **Cliff's delta (d)**：效应量
- **Mann-Whitney U test**：非配对比较
- **Cohen's kappa / Fleiss' kappa**：标注一致性（经验研究和人工评估中）

---

## 6. 讨论（Discussion）写作模式

### 6.1 是否需要单独 Discussion 节

| 论文类型 | 是否有 Discussion | 内容 |
|----------|-------------------|------|
| Empirical Study（TSE/TOSEM） | **必须有** | Implications, Lessons Learned |
| Technique（ICSE/FSE/ASE） | 约 50% 有 | 失败案例分析、实际应用讨论 |
| Tool（ISSTA） | 约 40% 有 | 工具局限性、开发者反馈 |

### 6.2 Discussion 句式模板

**Implications（胡星老师特色——常分 For Practitioners / For Researchers）：**
```
Our findings have several practical implications.
For practitioners: [Finding1] suggests that developers should [Action].
  → "Our findings suggest that OSS maintainers should establish security policies and provide private contact channels."
For researchers: [Finding2] indicates that [Direction] is a promising area for future work.
  → "The low IC scores indicate that improving logical consistency is a promising direction for code LLM research."
```

**失败案例分析：**
```
To better understand the limitations of [ToolName], we manually analyze the cases where it fails.
We find that [ToolName] tends to fail when [Condition], because [Reason].
This suggests that [Future Direction] could improve [ToolName].
```

---

## 7. 威胁有效性（Threats to Validity）写作模式

### 7.1 标准三维度结构

**Internal Validity：**
```
Threats to internal validity relate to [potential errors in implementation/setup].
To mitigate this, we [mitigation: e.g., carefully reviewed code, used established libraries].
We repeat each experiment [N] times and report the average results to reduce randomness.
```

**External Validity：**
```
Threats to external validity concern the generalizability of our findings.
Our experiments are conducted on [N] [subjects] from [Source].
To mitigate this, we select subjects that vary in [size/domain/language].
In the future, we plan to evaluate on more diverse subjects.
```

**Construct Validity：**
```
Threats to construct validity relate to the suitability of our evaluation metrics.
We adopt [Metrics] following prior studies [refs].
To complement quantitative results, we also conduct [case study/user study].
```

---

## 8. 相关工作（Related Work）写作模式

### 8.1 位置选择

| 位置 | 适用场景 | 比例 |
|------|----------|------|
| **Section 2（方法前）** | 需要先介绍背景知识 | ~40% |
| **倒数第二节（结论前）** | 方法独立性强 | ~60% |

### 8.2 每组的写法模板

```
[Topic] has been extensively studied in the literature.
[Author1] et al. [ref] proposed [Method1], which [brief description].
[Author2] et al. [ref] designed [Method2] to [goal] by [technique].
More recently, [Author3] et al. [ref] introduced [Method3] leveraging [LLMs/DL].

Different from these studies, our work focuses on [specific difference].
Unlike [closest work], we [key distinction].
```

### 8.3 关键技巧

- **每组最后必须有对比句**——`Unlike X, we...` / `Different from Y, our approach...`
- **不要变成综述**——每篇引用 1-2 句话足够
- **突出差异而非相似**
- **引用要新**——至少包含最近 2 年的工作

---

## 9. 结论（Conclusion）写作模式

### 9.1 句式模板

```
In this paper, we propose/present/conduct [ToolName/Study], a [adjective] approach/study to [Task].
[ToolName] [key mechanism in one sentence].
We evaluate [ToolName] on [N] [subjects] and compare it with [N] baselines.
Experimental results demonstrate that [ToolName] [key finding with number].
In the future, we plan to [Future Direction 1] and [Future Direction 2].
```

### 9.2 写作要点

- **不要引入新信息**——结论只总结已有内容
- **必须有数字**——至少重复一个关键结果数字
- **未来工作要具体**——不是 "improve our method"，而是 "extend to [specific scenario]"
- **长度控制在半页以内**

---

## 10. 跨章节的英文写作微技巧

### 10.1 过渡与衔接

**章节间过渡：**
```
In this section, we describe/present/introduce [content].
Having described [previous content], we now turn to [current content].
Based on the above analysis, we design [next step].
```

**段落间过渡：**
```
To address this issue, ...
Motivated by this observation, ...
Building upon [previous work/finding], ...
Furthermore, / More specifically, ...
```

### 10.2 精确动词选择

| 场景 | 推荐动词 | 避免动词 |
|------|----------|----------|
| 提出方法 | propose, design, develop, present | try, explore |
| 发现结果 | find, observe, demonstrate, reveal | think, believe |
| 比较 | outperform, surpass, improve over | is better than |
| 分析 | investigate, examine, analyze | look at, check |
| 解决问题 | address, tackle, mitigate | solve (太绝对) |
| 利用技术 | leverage, exploit, harness | use (太泛) |

### 10.3 避免的常见错误

1. **避免 "very/really/extremely"**——用数字代替程度副词
2. **避免 "we believe/think"**——用 "results show/indicate/suggest"
3. **避免 "obviously/clearly"**——如果真的 obvious，不需要说
4. **避免 "in order to"**——直接用 "to"
5. **避免被动语态过多**——主动语态更清晰
6. **"significant" 只在有统计检验时使用**——否则用 "substantial/considerable"

### 10.4 数字与量化表达

```
[ToolName] improves [Metric] by [X%] on average (ranging from [min%] to [max%]).
[ToolName] achieves [X%] [Metric], which is [Y%] higher than the best baseline.
On average, [ToolName] takes [N] seconds, which is [M]× faster than [Baseline].
Out of [N] cases, [ToolName] successfully [achieves goal] in [M] cases ([M/N × 100]%).
```

---

## 11. 图表设计规范

### 11.1 必备图表

| 图表 | 位置 | 功能 | 出现率 |
|------|------|------|--------|
| **Motivating Example (Fig 1)** | 引言 | 展示现有方法的失败案例 | 86% |
| **Overview Figure (Fig 2)** | 方法开头 | 展示整体框架/流程 | ~95% |
| **Results Table** | 实验 | 主要对比结果 | 100% |
| **Ablation Table** | 实验 | 消融实验结果 | ~70% |
| **Box Plot / Bar Chart** | 实验 | 分布/对比可视化 | ~50% |

### 11.2 表格/图标题规范

```
Table N. Comparison results of [ToolName] and baselines on [Dataset]. The best results are highlighted in bold.
Table N. Ablation study results. "-w/o X" means removing component X.
Fig. N. Overview of [ToolName]. [ToolName] consists of [N] phases: ...
Fig. N. A motivating example from [Project/CVE].
```

---

## 12. 论文类型特定写法

### 12.1 Technique Paper（工具/方法论文，占 ~70%）

- 引言必须有 Motivating Example（86% 包含）
- 方法必须有 Overview Figure + 流程描述
- 实验必须有 RQ1(有效性) + RQ2(消融) + 至少一个额外 RQ
- 必须讨论 Threats to Validity
- 胡星老师特色：近年 Technique Paper 大量融合 LLM，需描述 prompt 设计和 Agent 协作

### 12.2 Empirical Study（实证研究论文，占 ~20%）

- 标题用 "An Empirical Study on/of..." 或 "Practitioners' Expectations on..."
- 引言重点在 Research Gap 和 Study Design
- RQ 数量通常 3-5 个，每个 RQ 有独立的 Motivation
- 必须有 Implications（分 For Practitioners / For Researchers）
- Discussion 章节是核心
- 胡星老师特色：经验研究常包含开发者调研（survey/interview），如 ICSE'22 调查 720 名从业者

### 12.3 经验研究的 RQ 写法

```
RQ1: [Descriptive] — What are the characteristics of [phenomenon]?
RQ2: [Comparative] — How does [A] compare with [B]?
RQ3: [Causal] — What factors influence [outcome]?
RQ4: [Practical] — How can [finding] improve [practice]?
```

每个 RQ 的回答结构：
```
**Motivation.** We investigate this RQ because [reason].
**Approach.** To answer this RQ, we [methodology].
**Results.** [Key finding with numbers].
**Finding N.** [One-sentence takeaway].
```

---

## 13. 高频可复用句式速查表

### 13.1 Motivation 类
```
[Task] is important because [Reason].
However, [existing approach] suffers from [Limitation].
This motivates us to [Action].
To the best of our knowledge, this is the first work that [Novelty].
```

### 13.2 Method Description 类
```
Specifically, we first [Step1], then [Step2], and finally [Step3].
The intuition behind this design is that [Insight].
Given [Input], [ToolName] produces [Output] by [Mechanism].
```

### 13.3 Result Reporting 类
```
Table N presents the comparison results.
We can observe that [ToolName] consistently outperforms all baselines.
On average, [ToolName] achieves [X%] improvement over the best baseline.
The improvement is statistically significant (p < 0.05).
```

### 13.4 Analysis 类
```
To understand why [ToolName] performs better, we analyze [Aspect].
We find that [Observation], which explains [Result].
A possible reason is that [Explanation].
This finding suggests that [Implication].
```

### 13.5 Limitation 类
```
We acknowledge that our study has several limitations.
First, [Limitation1]. To mitigate this, we [Mitigation].
Despite these limitations, our findings provide [Value].
```

---

## 14. 写作流程建议（实操 Checklist）

### Phase 1: 骨架搭建
- [ ] 确定论文类型（Technique / Empirical / Tool）
- [ ] 写出一句话主张（Thesis Claim）
- [ ] 列出 3-4 个 RQ
- [ ] 画 Overview Figure 草图
- [ ] 确定数据集、基线、指标

### Phase 2: 核心章节
- [ ] 写方法章节（先 Overview 再细节）
- [ ] 写实验设置（数据集→基线→指标→实现细节）
- [ ] 跑实验，填表格
- [ ] 写每个 RQ 的 Answer 段落

### Phase 3: 首尾章节
- [ ] 写引言（从 P3 Gap 段开始写，再补 P1 P2）
- [ ] 写摘要（最后写，从结果倒推）
- [ ] 写相关工作
- [ ] 写 Threats to Validity
- [ ] 写结论

### Phase 4: 打磨
- [ ] 术语一致性检查
- [ ] RQ 与结论对齐检查
- [ ] 贡献点与实验对齐检查
- [ ] 数字一致性检查（摘要、引言、实验、结论中的数字）
- [ ] 图表标题完整性检查
- [ ] 参考文献格式检查

---

## 附录 A: 本指南数据来源

| 来源 | 全文数量 | 级别 |
|------|----------|------|
| ICSE 全文 | 17篇 | CCF-A 会议 |
| TOSEM 全文 | 10篇 | CCF-A 期刊 |
| ASE 全文 | 10篇 | CCF-A 会议 |
| FSE/ESEC 全文 | 6篇 | CCF-A 会议 |
| ISSTA 全文 | 4篇 | CCF-A 会议 |
| TSE 全文 | 3篇 | CCF-A 期刊 |
| **合计** | **50篇** | **全部 CCF-A** |

PDF 存储路径：`templog/writingskills/caches/pdfs_huxing/`
中文翻译路径：`templog/writingskills/caches/translations_cn/huxing_*.md`

## 附录 B: 写作特征统计汇总

| 特征 | 数值 | 说明 |
|------|------|------|
| 摘要含数字 | 94% (47/50) | 几乎所有论文摘要都有量化结果 |
| 有 RQ | 80% (40/50) | 含明确编号或隐含的研究问题 |
| 有 Motivating Example | 86% (43/50) | 多用 Figure 1 展示失败案例 |
| 贡献点 3 条 | 48% (24/50) | 最常见 |
| 贡献点 4 条 | 40% (20/50) | 次常见 |
| 贡献点 2 条 | 10% (5/50) | 较少 |
| 标题：工具名型 | 36% (18/50) | 最常见标题结构 |
| 标题：动名词型 | 18% (9/50) | 第二常见 |
| 标题：隐喻/格言型 | 10% (5/50) | 适合反直觉发现 |

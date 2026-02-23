---
name: xchencs-paper-writing
description: 基于陈翔老师（Xiang Chen）23篇全文PDF深度分析的软件工程论文英文写作技巧完整指南。覆盖标题→摘要→引言→方法→实验→讨论→威胁→相关工作→结论全流程，含可复用句式模板库。适用于 ICSE/FSE/ASE/ISSTA/TOSEM/TSE/EMSE/IST/JSS 等顶会顶刊投稿。v2.0，来源：TSE(4)/TOSEM(4)/ISSTA(1)/ASE(2)/EMSE(2)/ICSE(1)/IST(2)/ASEJ(3)/JSS(1)/ICPC(1)/COMPSAC(1)/SEKE(2)/EAAI(1)共23篇全文。
---

# 陈翔老师论文英文写作技巧完整指南（Full-Text Analysis v2.0）

> 本指南基于 23 篇已下载全文 PDF 的逐节深度分析，而非仅摘要。
> 涵盖 CCF-A（TSE/TOSEM/ICSE/FSE/ASE/ISSTA）到 CCF-B/C 各级别期刊会议。

---

## 1. 标题（Title）写作模式

### 1.1 五种常见标题结构

| 模式 | 示例 | 适用场景 |
|------|------|----------|
| **工具名 + 冒号 + 功能描述** | `DevMuT: Testing Deep Learning Framework via Developer Expertise-Based Mutation` | 提出新工具/方法 |
| **动名词开头 + 任务描述** | `Improving Deep Learning Framework Testing with Model-Level Metamorphic Testing` | 改进型工作 |
| **经验研究标题** | `An Empirical Study on Challenges for LLM Application Developers` | 实证研究 |
| **概念隐喻/对比** | `Less is More: DocString Compression in Code Generation` | 有反直觉发现 |
| **问句式** | `How Important are Good Method Names in Neural Code Generation?` | 探索性研究 |

### 1.2 标题写作规则

- 长度控制在 **10-16 个单词**
- 工具名用大驼峰或全大写缩写（DevMuT, SEthesaurus, CLACER）
- 冒号后的描述用 **动名词短语**（Improving/Detecting/Boosting）或 **介词短语**（via/through/based on）
- 关键技术词放在标题中（Mutation, Metamorphic Testing, Chain-of-Thought, Prompt Tuning）
- 避免 "A Novel..." / "A New..." 等空泛修饰

### 1.3 可复用标题模板

```
[ToolName]: [Verb-ing] [Task] via/through/by [Key Technique]
[Verb-ing] [Target] [Preposition] [Technique/Approach]
An Empirical Study on/of [Topic] in/for [Context]
[Concept]: From [Source] and For [Target] [Qualifier]
```

---

## 2. 摘要（Abstract）写作模式

### 2.1 标准四段式结构（逐句分析）

基于全文分析，陈翔老师的摘要严格遵循 **4-5 句式结构**：

| 句序 | 功能 | 典型长度 | 占比 |
|------|------|----------|------|
| S1 | **背景+重要性** | 1-2句 | 20% |
| S2 | **现有方法不足（Gap）** | 1-2句 | 20% |
| S3 | **本文方法概述** | 2-3句 | 30% |
| S4 | **实验结果+数字** | 2-3句 | 25% |
| S5 | **结论/启示（可选）** | 0-1句 | 5% |

### 2.2 各句位的句式模板库

**S1 背景句：**
```
[Task] plays a critical/important role in [Domain].
[Activity] has attracted increasing attention in [Field] due to [Reason].
With the rapid development of [Technology], [Task] has become increasingly important.
Recently, [Technique] has been widely adopted/applied to [Task].
```

**S2 Gap句（最关键——评审看这里判断novelty）：**
```
However, existing approaches/methods suffer from [Limitation].
Despite the progress, [specific challenge] remains under-explored.
Unfortunately, [existing method] may [fail/introduce/overlook] [specific problem].
Nevertheless, [current solutions] are limited in [aspect] because [reason].
Prior studies have not thoroughly investigated [specific gap].
```

**S3 方法句：**
```
In this paper, we propose [ToolName], a [adjective] approach/method to [Task] by [Mechanism].
To address this challenge, we design [ToolName], which [key mechanism].
Specifically, [ToolName] first [Step1], then [Step2], and finally [Step3].
The key insight behind our approach is that [Observation/Insight].
Our approach consists of three main components: (1) ..., (2) ..., and (3) ...
```

**S4 结果句（必须有数字）：**
```
We evaluate [ToolName] on [N datasets/projects/subjects]. Results show that [ToolName] outperforms [baseline] by [X%] in terms of [metric].
Experimental results on [N] [subjects] demonstrate that [ToolName] achieves [metric value], improving over the state-of-the-art by [X%].
Our extensive experiments on [N] [subjects] show that [ToolName] can effectively [achieve goal], with an average improvement of [X%] over [N] baselines.
```

**S5 结论句（可选）：**
```
Our findings provide practical guidelines for [practitioners/researchers].
These results suggest that [insight] is a promising direction for [future work].
```

### 2.3 摘要写作检查清单

- [ ] 是否包含至少 1 个具体数字结果？（约 80% 的论文包含）
- [ ] 是否有明确的 "we propose/present/design" 动作动词？
- [ ] Gap 句是否指向可测量的失败，而非泛泛的 "has not been studied"？
- [ ] 方法描述是否提到核心机制关键词？
- [ ] 总长度是否在 150-250 词之间？

---

## 3. 引言（Introduction）写作模式

### 3.1 标准五段式结构

基于 TSE/TOSEM/ASE 论文的全文分析，引言通常为 **5-7 段**，功能分布如下：

| 段落 | 功能 | 内容要点 |
|------|------|----------|
| P1 | **任务背景+重要性** | 用 1-2 个真实场景/数据说明为什么这个问题重要 |
| P2 | **现有方法综述** | 简要介绍 2-3 类现有方法（不展开细节） |
| P3 | **现有方法的关键不足** | 指出 1-2 个具体的失败模式（最好有例子或数据） |
| P4 | **本文方法概述+核心 Insight** | 用 1 段话说清楚"我们做了什么、为什么有效" |
| P5 | **贡献点列表** | 3-4 条，每条对应一个可交付物 |
| P6 | **论文组织（可选）** | "The rest of this paper is organized as follows..." |

### 3.2 各段的句式模板

**P1 背景段开头：**
```
[Task/Activity] is a fundamental/critical/essential task in software engineering.
In recent years, [Technology] has been increasingly adopted to [Task], achieving promising results.
[Problem] is one of the most [important/challenging] problems in [Domain].
```

**P2 现有方法段：**
```
To tackle this problem, researchers have proposed various approaches, which can be broadly categorized into [Category1]-based and [Category2]-based methods.
Existing approaches to [Task] can be divided into two main categories: [Cat1] and [Cat2].
Prior work on [Task] has explored [Approach1], [Approach2], and [Approach3].
```

**P3 不足段（Motivation 核心——评审最关注）：**
```
However, these approaches have several limitations.
First, [Method] relies on [Assumption], which may not hold in practice because [Reason].
Second, [Method] fails to consider [Factor], leading to [Consequence].
Despite their effectiveness, existing methods still face challenges in [Aspect].
A key limitation of prior work is that [specific limitation with evidence].
```

**P3 中的 Motivating Example 写法：**
```
To illustrate this limitation, consider the example shown in Figure 1.
Figure 1 shows a real-world example from [Project], where [existing method] fails because [reason].
As shown in Figure 1, [specific observation], which motivates our approach.
```

**P4 方法概述段：**
```
To address the above limitations, we propose [ToolName], a novel [type] approach that [key mechanism].
The key insight behind [ToolName] is that [Observation].
Specifically, [ToolName] consists of three main phases: (1) [Phase1], (2) [Phase2], and (3) [Phase3].
Unlike existing methods that [limitation], [ToolName] [advantage] by [mechanism].
```

**P5 贡献点列表：**
```
The main contributions of this paper are as follows:
• We propose [ToolName], a [adjective] approach to [Task]. To the best of our knowledge, this is the first work that [novelty claim].
• We design [specific component/technique] to [specific purpose].
• We conduct extensive experiments on [N] [subjects] and demonstrate that [ToolName] outperforms [N] state-of-the-art baselines.
• We release our code and data at [URL] to facilitate future research.
```

### 3.3 引言写作的关键技巧

1. **第一段不要写综述**——用一个具体场景或数据把读者拉进来
2. **Gap 必须可测量**——不是 "has not been studied"，而是 "causes X% false positives"
3. **Insight 必须可反驳**——不是 "we use deep learning"，而是 "we observe that [pattern]"
4. **贡献点必须可验证**——每条贡献对应后文的一个章节或实验
5. **Motivating Example 是加分项**——TSE/TOSEM 论文中约 60% 在引言中包含 Figure 1 作为 motivating example

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

**必须包含一张 Overview Figure**（全文分析中 100% 的 Technique 类论文都有）：

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
Algorithm 1 presents the detailed procedure of [Phase].
```

### 4.4 公式与算法写法

- 公式编号连续，首次出现时用 "as shown in Equation (1)"
- 算法伪代码用 `Algorithm` 环境，带行号
- 变量用斜体，函数名用正体
- 复杂公式后紧跟一句自然语言解释：`where [var] denotes [meaning]`

### 4.5 方法章节的关键技巧

1. **先给全景图再给细节**——读者需要先知道整体流程
2. **每个子模块开头说"为什么需要这一步"**——不要直接跳到 how
3. **用 running example 贯穿**——在每个子模块中用同一个例子演示
4. **Design choice 要解释**——为什么选 GNN 而不是 Transformer？为什么用 cosine similarity？

---

## 5. 实验（Evaluation/Experiment）写作模式

### 5.1 RQ 驱动的实验设计

陈翔老师的论文 **100% 使用 RQ 驱动评测**。典型 RQ 套件：

| RQ类型 | 模板 | 出现频率 |
|--------|------|----------|
| **RQ1 有效性** | How effective is [ToolName] compared with state-of-the-art baselines? | 100% |
| **RQ2 消融** | How does each component of [ToolName] contribute to its effectiveness? | ~80% |
| **RQ3 效率** | How efficient is [ToolName] in terms of time/memory cost? | ~50% |
| **RQ4 参数敏感性** | How sensitive is [ToolName] to the choice of [hyperparameter]? | ~40% |
| **RQ5 泛化性** | How does [ToolName] perform across different [settings/datasets]? | ~30% |
| **RQ6 实用性** | Can [ToolName] help developers in practice? (case study/user study) | ~20% |

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
We compare [ToolName] with [N] state-of-the-art baselines from [N] categories:
(1) [Category1]-based: [Baseline1] [ref], [Baseline2] [ref];
(2) [Category2]-based: [Baseline3] [ref], [Baseline4] [ref].
We select these baselines because they represent the most recent and competitive approaches.
For fair comparison, we use the same [settings/data splits/parameters] for all approaches.
```

**评估指标模板：**
```
Following prior studies [refs], we adopt [Metric1], [Metric2], and [Metric3] as evaluation metrics.
[Metric1] measures [what it measures]. A higher/lower [Metric1] indicates better performance.
```

### 5.3 结果呈现模式

**表格设计规范（从全文提取）：**
- 最优值用 **加粗**
- 次优值用 _下划线_（部分论文）
- 提升百分比用 `↑X%` 或 `(+X%)`
- 表格标题格式：`Table N: [Description]. The best results are highlighted in bold.`
- 每个 RQ 对应一个或多个表格/图

**结果段落的标准写法（Answer to RQ 模式）：**
```
**Answer to RQ1:** Table 2 presents the comparison results.
We can observe that [ToolName] outperforms all baselines across [all/most] metrics.
Specifically, [ToolName] achieves [value] in [Metric], which improves over the best baseline [Name] by [X%].
The improvement is statistically significant (p-value < 0.05, Wilcoxon signed-rank test).
The reason is that [explanation of why our method works better].
```

**消融实验结果模板：**
```
**Answer to RQ2:** To evaluate the contribution of each component, we design [N] variants:
- [ToolName]-w/o-[Component1]: removing [Component1]
- [ToolName]-w/o-[Component2]: removing [Component2]
Table 3 shows the results. We observe that removing [Component1] leads to a [X%] decrease in [Metric], indicating that [Component1] plays an important role in [function].
```

### 5.4 统计检验使用

陈翔老师的 TSE/TOSEM 论文中常用的统计方法：
- **Wilcoxon signed-rank test**：配对比较（最常用）
- **Cliff's delta (d)**：效应量（small/medium/large）
- **Scott-Knott ESD test**：多组比较排序
- **Mann-Whitney U test**：非配对比较

模板：
```
To verify the statistical significance, we perform the Wilcoxon signed-rank test at a significance level of 0.05.
We also compute Cliff's delta (d) to measure the effect size, where |d| < 0.147 is negligible, |d| < 0.33 is small, |d| < 0.474 is medium, and |d| ≥ 0.474 is large.
```

---

## 6. 讨论（Discussion）写作模式

### 6.1 是否需要单独 Discussion 节

| 论文类型 | 是否有 Discussion | 内容 |
|----------|-------------------|------|
| Empirical Study（TSE/TOSEM） | **必须有** | Implications, Lessons Learned |
| Technique（ASE/ISSTA） | 约 50% 有 | 失败案例分析、参数影响、实际应用讨论 |
| Tool（ICSE/FSE） | 约 40% 有 | 工具局限性、工业反馈 |

### 6.2 Discussion 常见子节

```
5. Discussion
  5.1 Implications / Practical Guidelines
  5.2 Failure Analysis / When Does It Fail?
  5.3 Generalizability
  5.4 Comparison with [Related Approach]
```

### 6.3 Discussion 句式模板

**Implications：**
```
Our findings have several practical implications for [practitioners/researchers].
First, [Finding1] suggests that [Implication1]. This means that developers should [Action].
Second, [Finding2] indicates that [Implication2], which can guide future research on [Topic].
```

**失败案例分析（加分项）：**
```
To better understand the limitations of [ToolName], we manually analyze the cases where it fails.
We find that [ToolName] tends to fail when [Condition], because [Reason].
Figure N shows a representative failure case, where [Description].
This suggests that [Future Direction] could be a promising direction to improve [ToolName].
```

---

## 7. 威胁有效性（Threats to Validity）写作模式

### 7.1 标准三维度结构

陈翔老师的 TSE/TOSEM 论文 **100% 包含 Threats to Validity**，且严格按三维度组织：

**Internal Validity（内部有效性）：**
```
Threats to internal validity relate to [potential errors in our implementation/experimental setup].
To mitigate this threat, we [mitigation strategy].
- 实现正确性：We carefully reviewed our code and used well-established libraries.
- 参数公平性：We use the default/recommended parameters for all baselines as reported in their original papers.
- 随机性：We repeat each experiment [N] times and report the average results.
```

**External Validity（外部有效性）：**
```
Threats to external validity concern the generalizability of our findings.
Our experiments are conducted on [N] [subjects] from [Source].
Although these subjects are widely used in prior studies, our findings may not generalize to [other contexts].
To mitigate this, we select subjects that vary in [size/domain/language/complexity].
In the future, we plan to evaluate [ToolName] on more diverse subjects.
```

**Construct Validity（构造有效性）：**
```
Threats to construct validity relate to the suitability of our evaluation metrics.
We adopt [Metrics] following prior studies [refs].
However, these metrics may not fully capture [aspect].
To complement, we also conduct [qualitative analysis/case study/user study].
```

### 7.2 写作要点

- **不要只说 "可能有威胁"**——必须说清楚威胁是什么、可能导致什么偏差、如何缓解
- **每个维度 2-3 条**，每条 2-3 句话
- **缓解措施要具体**——不是 "we will do more experiments"，而是 "we repeated N times with different seeds"

---

## 8. 相关工作（Related Work）写作模式

### 8.1 位置选择

| 位置 | 适用场景 | 陈翔老师论文中的比例 |
|------|----------|---------------------|
| **Section 2（方法前）** | 需要先介绍背景知识才能理解方法 | ~40% |
| **倒数第二节（结论前）** | 方法独立性强，不需要背景铺垫 | ~60% |

### 8.2 分组策略

按 **问题/技术** 分 2-4 个子节：

```
7. Related Work
  7.1 [Problem Domain] (e.g., Fault Localization)
  7.2 [Key Technique] (e.g., Mutation Testing)
  7.3 [Application Context] (e.g., Deep Learning Testing)
```

### 8.3 每组的写法模板

```
[Topic] has been extensively studied in the literature.
[Author1] et al. [ref] proposed [Method1], which [brief description].
[Author2] et al. [ref] designed [Method2] to [goal] by [technique].
More recently, [Author3] et al. [ref] introduced [Method3], achieving [result].

Different from these studies, our work focuses on [specific difference].
Unlike [closest work], we [key distinction].
```

### 8.4 关键技巧

- **每组最后必须有对比句**——`Unlike X, we...` / `Different from Y, our approach...`
- **不要变成综述**——每篇引用 1-2 句话足够
- **突出差异而非相似**——评审想知道你和别人有什么不同
- **引用要新**——至少包含最近 2 年的工作

---

## 9. 结论（Conclusion）写作模式

### 9.1 标准结构

```
8. Conclusion [and Future Work]
  - 1段：总结本文工作（2-3句）
  - 1段：主要发现/结果（2-3句）
  - 1段：未来工作（1-2句，可选）
```

### 9.2 句式模板

```
In this paper, we propose [ToolName], a [adjective] approach to [Task].
[ToolName] [key mechanism in one sentence].
We evaluate [ToolName] on [N] [subjects] and compare it with [N] baselines.
Experimental results demonstrate that [ToolName] [key finding with number].
In the future, we plan to [Future Direction 1] and [Future Direction 2].
```

### 9.3 写作要点

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
In addition to [previous point], ...
Furthermore, ...
More specifically, ...
```

**结果段落间过渡：**
```
We further investigate [next aspect].
To gain deeper insights, we analyze [specific aspect].
In addition to the quantitative results, we also conduct [qualitative analysis].
```

### 10.2 精确动词选择

| 场景 | 推荐动词 | 避免动词 |
|------|----------|----------|
| 提出方法 | propose, design, develop, present | try, explore, discuss |
| 发现结果 | find, observe, demonstrate, reveal | think, believe, feel |
| 比较 | outperform, surpass, improve over | is better than |
| 分析 | investigate, examine, analyze | look at, check |
| 解决问题 | address, tackle, mitigate | solve (太绝对) |

### 10.3 避免的常见错误

1. **避免 "very/really/extremely"**——用数字代替程度副词
2. **避免 "we believe/think"**——用 "results show/indicate/suggest"
3. **避免 "obviously/clearly"**——如果真的 obvious，不需要说
4. **避免 "in order to"**——直接用 "to"
5. **避免被动语态过多**——主动语态更清晰："We design X" > "X is designed"
6. **"significant" 只在有统计检验时使用**——否则用 "substantial/considerable"

### 10.4 数字与量化表达

```
[ToolName] improves [Metric] by [X%] on average (ranging from [min%] to [max%]).
[ToolName] achieves [X%] [Metric], which is [Y%] higher than the best baseline.
On average, [ToolName] takes [N] seconds to process [one subject], which is [M]× faster than [Baseline].
Out of [N] cases, [ToolName] successfully [achieves goal] in [M] cases ([M/N × 100]%).
```

---

## 11. 图表设计规范

### 11.1 必备图表

| 图表 | 位置 | 功能 |
|------|------|------|
| **Motivating Example (Fig 1)** | 引言 | 展示现有方法的失败案例 |
| **Overview Figure (Fig 2)** | 方法开头 | 展示整体框架/流程 |
| **Results Table** | 实验 | 主要对比结果 |
| **Ablation Table** | 实验 | 消融实验结果 |
| **Box Plot / Bar Chart** | 实验 | 分布/对比可视化 |

### 11.2 表格标题规范

```
Table N. Comparison results of [ToolName] and baselines on [Dataset]. The best results are highlighted in bold [and the second best are underlined].
Table N. Ablation study results. "-w/o X" means removing component X.
Table N. Statistics of experimental subjects.
```

### 11.3 图标题规范

```
Fig. N. Overview of [ToolName]. [ToolName] consists of three phases: ...
Fig. N. A motivating example from [Project]. [Description of what it shows].
Fig. N. Distribution of [Metric] across [subjects/settings].
```

---

## 12. 论文类型特定写法

### 12.1 Technique Paper（工具/方法论文）

- 引言必须有 Motivating Example
- 方法必须有 Overview Figure + 算法伪代码
- 实验必须有 RQ1(有效性) + RQ2(消融) + 至少一个额外 RQ
- 必须讨论 Threats to Validity

### 12.2 Empirical Study（实证研究论文）

- 标题用 "An Empirical Study on/of..."
- 引言重点在 Research Gap 和 Study Design
- 方法章节改为 Study Design / Methodology
- RQ 数量通常 3-5 个，每个 RQ 有独立的 Motivation
- 必须有 Implications / Lessons Learned
- Discussion 章节是核心（不是方法）

### 12.3 经验研究的 RQ 写法

```
RQ1: [Descriptive question] — What are the characteristics of [phenomenon]?
RQ2: [Comparative question] — How does [A] compare with [B] in terms of [aspect]?
RQ3: [Causal question] — What factors influence [outcome]?
RQ4: [Practical question] — How can [finding] be applied to improve [practice]?
```

每个 RQ 的回答结构：
```
**Motivation.** We investigate this RQ because [reason].
**Approach.** To answer this RQ, we [methodology].
**Results.** [Key finding with numbers]. Figure/Table N shows [visualization].
**Finding N.** [One-sentence takeaway in a box/highlight].
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
Algorithm 1 summarizes the overall procedure.
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
We leave [Extension] as future work.
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

| 来源 | 数量 | 级别 |
|------|------|------|
| TSE 全文 | 4篇 | CCF-A |
| TOSEM 全文 | 4篇 | CCF-A |
| ISSTA 全文 | 1篇 | CCF-A |
| ASE 全文 | 2篇 | CCF-A |
| ICSE 全文 | 1篇 | CCF-A |
| EMSE 全文 | 2篇 | CCF-B |
| IST 全文 | 2篇 | CCF-B |
| ASEJ 全文 | 3篇 | CCF-B |
| JSS 全文 | 1篇 | CCF-B |
| ICPC 全文 | 1篇 | CCF-B |
| COMPSAC 全文 | 1篇 | CCF-C |
| SEKE 全文 | 2篇 | CCF-C |
| EAAI 全文 | 1篇 | CCF-B |
| **合计** | **23篇** | |

PDF 存储路径：
- 旧版（9篇）：`Desktop/codes/写作参考/papers/pdfs/`
- 新版（14篇）：`templog/writingskills/caches/pdfs_xchencs_new/`

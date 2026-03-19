# ISSTA 2026 Paper #820 Review

## Paper: Narrowing the Complexity Gap in the Evaluation of Large Language Models

---

## Summary

This paper proposes GENEBENCH, an automated technique that increases the complexity of existing programming benchmarks while maintaining code readability. GENEBENCH formulates benchmark augmentation as a multi-objective optimization problem and employs NSGA-II to evolve programs through 22 semantic-preserving AST transformation operators. These operators introduce concurrency, decorators, API dependencies, and nested structures, among others. Complexity and readability thresholds are calibrated relative to real-world programs from SWE-Bench. The authors evaluate 13 LLMs, including two reasoning models, on four transformed benchmarks across four programming tasks: input prediction, output prediction, code translation, and program repair. Results show an average performance drop of 35.2%, ranging from 14.9% to 60.5%. The paper further demonstrates that neither few-shot learning nor fine-tuning can fully overcome the complexity gap, and that bug repair difficulty under GENEBENCH is comparable to SWE-Bench.

本文提出GENEBENCH，一种自动化benchmark增强技术，将benchmark增强建模为多目标优化问题，采用NSGA-II通过22种语义保持的AST变换算子进化程序。这些算子引入并发、装饰器、API依赖和嵌套结构等特征。复杂度和可读性阈值基于SWE-Bench中的真实项目进行校准。作者在4个变换后的benchmark上评估13个LLM（含两个推理模型），覆盖输入预测、输出预测、代码翻译和程序修复四个任务。结果显示平均35.2%的性能下降，范围为14.9%至60.5%。论文进一步证明few-shot学习和微调均无法完全弥补复杂度差距，且GENEBENCH下的bug修复难度与SWE-Bench相当。

---

## Strengths

**S1: Well-motivated and important problem.** The complexity gap between existing benchmarks and real-world code is a critical bottleneck in LLM evaluation. The paper convincingly demonstrates this gap through Figure 1, which quantifies seven complexity metrics across five benchmarks. The motivation is timely, as the community increasingly relies on benchmarks to claim LLM capabilities for real-world deployment.

**S1：问题动机充分且重要。** 现有benchmark与真实代码复杂度之间的差距是LLM评估领域的关键瓶颈。论文通过Figure 1用7个量化指标在5个benchmark上清晰展示了这一差距，说服力强。随着社区越来越依赖benchmark来声称LLM的真实世界部署能力，这一动机非常及时。

**S2: High practical value.** GENEBENCH is task-agnostic and can augment any existing Python benchmark without mining new repositories—a one-hour budget suffices. The non-deterministic combination of 22 operators can continuously produce new versions, naturally resisting data contamination and overfitting.

**S2：实用价值高。** GENEBENCH是任务无关的，可直接增强任何现有Python benchmark，无需挖掘新仓库，一小时预算即可生成结果。22个算子的非确定性组合可持续产生新版本，天然抵御数据污染和过拟合。

**S3: Artifact availability and transparency.** The implementation, original datasets, transformed problems, detailed transformation logs, prompts, and LLM responses are all publicly available at the artifact website, facilitating reproduction and future research.

**S3：工件公开透明。** 实现代码、原始数据集、变换后的问题、详细变换日志、prompt模板和LLM响应均已在artifact网站公开，便于复现和后续研究。

---

## Weaknesses

**W1: Python-only support limits generalizability.** All 22 transformation operators and the evolution pipeline are designed exclusively for Python. The authors claim extending to other languages "does not require changes in algorithms or analyses and is primarily an engineering effort" (p.18), but several operators (e.g., IntroduceDecorator, ReplaceNumPy) rely on Python-specific features with no direct counterparts in statically-typed languages like Java or C++. Single-language evaluation weakens the breadth of the contribution.

**W1：仅支持Python，泛化性未验证。** 全部22个变换算子和进化流程均针对Python设计。作者声称扩展到其他语言"不需要改变算法或分析，主要是工程工作"（第18页），但多个算子（如IntroduceDecorator、ReplaceNumPy）依赖Python特有特性，在Java或C++等静态类型语言中无直接对应物。单语言评估削弱了贡献的广度。

**W2: Operator design lacks completeness and representativeness validation.** The 22 operators are derived from manually analyzing 2,692 Python files from the top 100 PyPI projects over one month—a reasonable starting point. However, the paper provides no argument for why these 22 operators sufficiently cover the real-world complexity space: which code patterns are missing? How representative are they of the broader Python ecosystem beyond the top 100 projects? A completeness analysis or a mapping to an established code complexity taxonomy would strengthen the design.

**W2：变换算子缺乏完备性和代表性验证。** 22个算子来源于对PyPI排名前100项目的2,692个Python文件的人工分析，历时一个月——作为起点是合理的。但论文未论证这22个算子为何足以覆盖真实世界的复杂度空间：遗漏了哪些代码模式？它们对top 100以外的Python生态系统的代表性如何？完备性分析或与现有代码复杂度分类法的映射会增强设计的说服力。

**W3: Insufficient differentiation from adversarial/mutation testing.** The paper acknowledges in §6 that GENEBENCH is similar to programming adversarial attacks, and distinguishes itself by claiming "preserving the semantics is not essential to assess generalizability"—yet GENEBENCH chooses to preserve semantics as a design decision. While this is not a logical contradiction, the paper does not convincingly articulate what makes GENEBENCH fundamentally different from adversarial perturbation techniques beyond the optimization objective. The relationship with higher-order mutation testing also deserves deeper discussion—both apply multiple transformations to programs while maintaining test-passing behavior.

**W3：与对抗性测试/变异测试的区分不够充分。** 论文在§6承认GENEBENCH与编程对抗攻击相似，并通过声称"保持语义对于评估泛化能力并非必要"来区分自身——但GENEBENCH本身又将语义保持作为设计选择。这虽非逻辑矛盾，但论文未令人信服地阐明除优化目标外，GENEBENCH与对抗扰动技术的根本差异何在。与高阶变异测试的关系也需更深入讨论——二者都对程序施加多重变换同时保持测试通过行为。

**W4: Fitness calibration based on SWE-Bench creates potential circularity.** The RC and RR thresholds are computed from SWE-Bench's buggy classes, and RQ4 validates representativeness against SWE-Bench-Lite. Although different subsets are used, this "calibrate from SWE-Bench → validate with SWE-Bench" pipeline introduces potential bias.

**W4：基于SWE-Bench的适应度校准存在潜在循环论证风险。** RC和RR的阈值从SWE-Bench的buggy类中计算，而RQ4则用SWE-Bench-Lite验证代表性。虽然使用了不同子集，但这种"从SWE-Bench校准→用SWE-Bench验证"的流程引入了潜在偏差。

**W5: Lack of fine-grained analysis of individual complexity dimensions.** The paper reports overall performance drops but does not isolate which of the seven complexity dimensions are most challenging for LLMs. Figure 8 only shows operator frequency vs. complexity contribution. An ablation study—varying one complexity dimension while holding others constant—would provide much deeper insight into what makes code hard for LLMs.

**W5：缺乏对不同复杂度维度独立效果的细粒度分析。** 论文报告了整体性能下降，但未分离7个复杂度维度中哪些对LLM最具挑战性。Figure 8仅展示算子频率与复杂度贡献的相关性。控制变量的消融实验（仅改变一个复杂度维度，保持其他不变）将为"代码中什么使LLM困难"提供更深层的洞察。

---

## Importance

**High.** The accuracy of LLM code capability evaluation directly impacts academic research directions and industrial deployment decisions. The finding that "existing benchmarks severely underestimate LLM failure rates under real-world complexity" is an important wake-up call for the community. GENEBENCH as a general-purpose augmentation tool has broad applicability.

**高。** LLM代码能力评估的准确性直接影响学术研究方向和工业应用决策。"现有benchmark严重低估LLM在真实复杂度下的失败率"这一发现对社区具有重要警示意义。GENEBENCH作为通用增强工具具有广泛适用价值。

---

## Originality

**Medium-High.** Formulating benchmark augmentation as a multi-objective optimization problem with complexity and readability as competing objectives is novel. The direction of "increasing complexity of existing benchmarks" rather than "mining harder problems" is a fresh angle. However, the underlying technical components—genetic algorithms, AST transformations, NSGA-II—are mature techniques in established combination. Compared to prior benchmark generation work (PPM [27], EvoEval [76]), the innovation lies primarily in the optimization direction and the semantic-equivalence constraint, not in fundamental algorithmic breakthroughs.

**中高。** 将benchmark增强建模为以复杂度和可读性为竞争目标的多目标优化问题是新颖的。"增加现有benchmark复杂度"而非"挖掘更难问题"的方向提供了新视角。然而底层技术组件——遗传算法、AST变换、NSGA-II——均为成熟技术的组合应用。与PPM [27]、EvoEval [76]等先前benchmark生成工作相比，创新主要在优化方向和语义等价约束，而非底层算法突破。

---

## Soundness

**Medium.** The experimental scale is large, model diversity is good, and statistical tests are properly applied (Mann-Whitney U, Spearman correlation). However: (1) Semantic equivalence is only verified by tests, not formal proofs; thread-related transformations are particularly risky. (2) The paper does not control for the confound that readability degradation (12% on average) may independently explain part of the performance drop.

**中等。** 实验规模大、模型多样、统计检验完备（Mann-Whitney U、Spearman相关）。但存在以下问题：(1) 语义等价仅靠测试验证而非形式化证明，线程相关变换风险尤高。(2) 论文未控制可读性下降（平均12%）可能独立解释部分性能下降的混淆因素。

---

## Verifiability & Transparency

**High.** Source code, datasets, transformation logs, prompt templates, and LLM responses are all publicly available at the artifact website [15]. Algorithms 1 and 2 clearly describe the core procedures. Reproduction conditions (model versions, GPU configurations, hyperparameters) are thoroughly documented. The use of temperature=0 and specific model versions enhances reproducibility.

**高。** 代码、数据集、变换日志、prompt模板、LLM响应均在artifact网站[15]公开。Algorithm 1和Algorithm 2清晰描述了核心流程。复现条件（模型版本、GPU配置、超参数）均有详细说明。温度=0和具体模型版本的使用增强了可复现性。

---

## Presentation

**Medium-High.** The paper is well-structured with four RQs forming a logical progression. Figures and tables are abundant and informative. Figure 2's transformation example is intuitive, and Figure 5's Pareto front visualization is clear. However: (1) Table 5 is excessively dense (13 models × 8 tasks × before/after/delta)—consider splitting or moving parts to an appendix. (2) The RC/RR formulas in §3.2 could benefit from more intuitive explanation.

**中高。** 论文结构清晰，4个RQ逻辑递进。图表丰富且信息量大。Figure 2的变换示例直观易懂，Figure 5的Pareto前沿可视化清晰精炼。但：(1) Table 5过于密集（13模型×8任务×before/after/delta），建议拆分或将部分内容移至附录。(2) §3.2中RC/RR公式的表述可加更直觉的解释。

---

## Questions for the Authors

1. **Independent effect of complexity dimensions:** Among the seven complexity dimensions, which ones are most challenging for LLMs? Could you design an ablation study that increases only one dimension while holding others constant?

   **复杂度维度的独立效果：** 7个复杂度维度中，哪些对LLM性能影响最大？是否能设计消融实验——仅增加一个维度的复杂度，保持其他不变？

2. **Evolution budget sensitivity:** How was the one-hour evolution budget selected? Would extending to 4 or 8 hours further increase complexity? How does the Pareto front distribution change with longer budgets?

   **进化预算敏感性：** 1小时的进化预算如何选定？延长到4小时或8小时，复杂度能否进一步提升？Pareto前沿的分布随预算增加如何变化？

3. **Task selection justification and extensibility:** The paper claims GENEBENCH is "task-agnostic" but evaluates on only four tasks (input/output prediction, code translation, program repair). What criteria guided the selection of these four tasks? More importantly, can GENEBENCH extend to other code-to-code/text tasks such as code summarization, clone detection, or vulnerability detection? If so, what adaptations would be needed for the artifacts (e.g., ground-truth labels, evaluation metrics)?

   **任务选择依据与可扩展性：** 论文声称GENEBENCH是"任务无关的"，但仅在4个任务上验证。选择这4个任务的标准是什么？更重要的是，GENEBENCH能否扩展到其他code-to-code/text任务，如代码摘要、克隆检测或漏洞检测？如果可以，制品层面（如ground-truth标签、评估指标）需要哪些适配？

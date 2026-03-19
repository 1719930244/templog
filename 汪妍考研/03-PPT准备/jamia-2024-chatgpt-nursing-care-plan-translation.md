# JAMIA 论文中英对照翻译

> **论文**: An Example of Leveraging AI for Documentation: ChatGPT-Generated Nursing Care Plan for an Older Adult with Lung Cancer
> **期刊**: JAMIA, 2024, 31(9): 2089-2096 | IF ≈ 7.1
> **DOI**: 10.1093/jamia/ocae116 | **PMCID**: PMC11339505
> **用途**: 汪妍硕士复试文献汇报（备用2）准备材料

---

## Title / 标题

**An Example of Leveraging AI for Documentation: ChatGPT-Generated Nursing Care Plan for an Older Adult with Lung Cancer**

利用 AI 辅助文档编写的一个范例：ChatGPT 为老年肺癌患者生成的标准化护理计划

---

## Authors / 作者

- **Fabiana C Dos Santos** (PhD, MSN, RN) — School of Nursing, Columbia University, New York, NY
  哥伦比亚大学护理学院
- **Lisa G Johnson** (MSN, RN) — College of Nursing, University of Florida, Gainesville, FL
  佛罗里达大学护理学院
- **Olatunde O Madandola** (MPH, RN) — College of Nursing, University of Florida
  佛罗里达大学护理学院
- **Karen J B Priola** (MSCIS) — College of Nursing, University of Florida
  佛罗里达大学护理学院
- **Yingwei Yao** (PhD) — College of Nursing, University of Florida
  佛罗里达大学护理学院
- **Tamara G R Macieira** (PhD, RN) — College of Nursing, University of Florida
  佛罗里达大学护理学院
- **Gail M Keenan** (PhD, RN, FAAN) — College of Nursing, University of Florida
  佛罗里达大学护理学院

**通讯作者**: Fabiana C Dos Santos
**资助**: NIH/NINR (1R01NR018416-01) + NIA (R21AG072265/R33AG072265)

---

## Abstract / 摘要

### Objective / 目的

> This study demonstrates the effectiveness of using a validated framework to create a ChatGPT prompt that generates valid nursing care plan suggestions for one hypothetical older patient with lung cancer.

本研究展示了使用经过验证的框架创建 ChatGPT 提示词的有效性，该提示词能够为一名假设的老年肺癌患者生成有效的护理计划建议。

### Method / 方法

> The methodology describes creating ChatGPT prompts that generate consistent care plan suggestions and its application for a lung cancer case scenario. After entering a nursing assessment of the patient's condition into ChatGPT, the researchers asked it to generate care plan suggestions. Subsequently, they assessed the quality of the care plans produced by ChatGPT.

该方法描述了创建能够生成一致性护理计划建议的 ChatGPT 提示词及其在肺癌病例场景中的应用。研究人员将患者状况的护理评估输入 ChatGPT 后，要求其生成护理计划建议，随后评估了 ChatGPT 所生成护理计划的质量。

### Results / 结果

> While not all the suggested care plan terms (11 out of 16) utilized standardized nursing terminology, the ChatGPT-generated care plan closely matched the gold standard in scope and nature, correctly prioritizing oxygenation and ventilation needs.

虽然并非所有建议的护理计划术语（16 个中有 11 个）都使用了标准化护理术语，但 ChatGPT 生成的护理计划在范围和性质上与金标准高度一致，正确地将氧合和通气需求列为最高优先级。

### Conclusion / 结论

> Using a validated framework prompt to generate nursing care plan suggestions with ChatGPT demonstrates its potential value as a decision support tool for optimizing cancer care documentation.

使用经过验证的框架提示词通过 ChatGPT 生成护理计划建议，展示了其作为决策支持工具在优化癌症护理文档方面的潜在价值。

**Keywords / 关键词**: artificial intelligence（人工智能）, large language model（大语言模型）, cancer（癌症）, nursing（护理）, standardized nursing terminologies（标准化护理术语）

---

## Introduction / 引言

### 第1段：AI 在医学中的应用背景

> The integration of artificial intelligence (AI) in medical contexts is growing. A discussion of trust and comprehension behind an AI tool's recommendation is needed, especially in clinical settings, where decisions can have life-or-death consequences. Among the recent AI advances that have gained attention is ChatGPT, developed by OpenAI, known for generating nearly human-quality responses across various tasks through supervised and reinforcement learning. Nurses play a crucial role in ensuring that care decisions result in the delivery of high-quality care. Given the information constraints and complexity of real-time care, finding a valid use of ChatGPT to enhance care could be beneficial to nurses and patients.

人工智能（AI）在医学领域的整合正在不断发展。关于 AI 工具推荐背后的信任和理解的讨论是必要的，尤其是在临床环境中，因为决策可能涉及生死后果。近期受到关注的 AI 进展包括由 OpenAI 开发的 ChatGPT，它以通过监督学习和强化学习在各种任务中生成接近人类水平的回复而闻名。护士在确保护理决策带来高质量护理方面发挥着关键作用。鉴于实时护理中的信息限制和复杂性，找到 ChatGPT 提升护理的有效使用方式对护士和患者都可能有益。

### 第2段：大语言模型在医学文档中的应用

> The rise of large language models (LLMs), such as GPT, has caused a surge of interest in their application in various research and clinical environments. Researchers and practitioners have investigated how AI can improve documentation systems by interpreting EHR documentation and simplifying clinical notes. LLMs have been widely used for medical record and report generation, demonstrating the potential of these models to enhance the precision of medical documentation. For instance, LLMs have shown promise in summarizing clinical notes and assisting clinicians in extracting key information from radiology, pathology, and other medical reports when guided by appropriate prompts. The advancement of GPT-3.5 and GPT-4 suggested that LLMs can rapidly accommodate new tasks, resulting in better documentation.

大语言模型（LLMs）如 GPT 的兴起，引发了各研究和临床环境中对其应用的强烈兴趣。研究人员和从业者已经研究了 AI 如何通过解读电子健康记录（EHR）文档和简化临床笔记来改善文档系统。LLMs 已被广泛用于医疗记录和报告生成，展示了这些模型增强医学文档精确性的潜力。例如，在适当提示词的引导下，LLMs 在总结临床笔记和协助临床医生从放射学、病理学及其他医学报告中提取关键信息方面展现出了前景。GPT-3.5 和 GPT-4 的进步表明，LLMs 能够快速适应新任务，从而产生更好的文档。

### 第3段：AI 在护理中的应用现状

> The integration of AI in nursing care has been increasingly recognized for its potential to transform nursing care delivery and improve patient outcomes. Nurses are leveraging technologies such as AI-powered clinical decision support in clinical tasks, including fall-risk predictions and improved fall prevention in hospital settings. Two other studies suggested that ChatGPT has the potential to assist nurses in administrative work, such as documentation, due to its ability to quickly process large amounts of data, potentially generating accurate, standardized care plans for nurses and leading to better patient outcomes. Although studies have explored the use of ChatGPT as a resource for nurses and other clinicians, it is unclear how well ChatGPT handles creating care plans coded with standardized nursing terminologies (SNTs) based on structured assessments and targeted questions. AI tools, particularly those in the generative AI category, are susceptible to errors. A thoughtful process of designing, refining, validating, and implementing prompts or instructions that guide the output of LLMs, such as ChatGPT, is needed to improve the accuracy of data generated and enhance their utility across various tasks.

AI 在护理中的整合因其转变护理服务提供方式和改善患者结局的潜力而日益受到认可。护士正在利用 AI 驱动的临床决策支持等技术来执行临床任务，包括跌倒风险预测和医院环境中的跌倒预防改善。另外两项研究表明，ChatGPT 由于能够快速处理大量数据，有潜力协助护士完成行政工作（如文档记录），可能为护士生成准确、标准化的护理计划，从而带来更好的患者结局。尽管已有研究探索了将 ChatGPT 作为护士和其他临床医生资源的使用，但 ChatGPT 在基于结构化评估和针对性问题创建以标准化护理术语（SNTs）编码的护理计划方面的能力尚不明确。AI 工具，特别是生成式 AI 类别的工具，容易出错。需要一个精心设计、改进、验证和实施提示词或指令的过程来引导 LLMs（如 ChatGPT）的输出，以提高生成数据的准确性并增强其在各种任务中的实用性。

### 第4段：本研究的目标

> The research team recently created a framework for guiding the development of ChatGPT prompts that would consistently generate valid standardized care plan suggestions for diverse hospitalized patients. The article explains the framework and demonstrates its use with ChatGPT in generating valid nursing care plan suggestions for hospitalized older adults with lung cancer as an example.

研究团队最近创建了一个框架，用于指导开发 ChatGPT 提示词，使其能够持续地为不同住院患者生成有效的标准化护理计划建议。本文解释了该框架，并以住院老年肺癌患者为例，展示了其与 ChatGPT 配合使用生成有效护理计划建议的过程。

### 第5段：选择肺癌案例的原因

> The case exemplar was chosen for several reasons. Lung cancer is the second most common cancer in both men and women in the United States, with an overall five-year survival rate of less than 30% for non-small cell lung cancer. Patients often experience multiple symptoms, especially respiratory insufficiency, based on disease progression and treatment. Such complexities require nurses' increased presence in symptom management, supportive care, and care plan documentation. Consequently, nurses may face stressors accompanying these tasks, such as the distress of caring for seriously ill patients, long working hours, pressure to make critical decisions, and the burden of documentation.

选择该病例范例有以下几个原因。肺癌是美国男性和女性中第二常见的癌症，非小细胞肺癌的总体五年生存率低于 30%。患者通常会根据疾病进展和治疗经历多种症状，尤其是呼吸功能不全。这些复杂性要求护士在症状管理、支持性护理和护理计划文档记录中投入更多精力。因此，护士可能面临伴随这些任务的压力源，如照顾重症患者的困扰、长时间工作、做出关键决策的压力以及文档记录的负担。

---

## Methods / 方法

### 第1段：方法概述

> This section describes the methodology for developing ChatGPT prompts that produce consistent, high-quality care plan recommendations using the Patient's Needs Framework as a guide. The validated Patient's Needs Framework is used to guide the entry of assessment data into the prompt to which the validated question is added together, generating the desired care plan suggestions. The framework and method are demonstrated in generating ChatGPT care plan outputs for a lung cancer patient scenario.

本节描述了使用"患者需求框架"（Patient's Needs Framework）作为指导，开发能够产生一致、高质量护理计划建议的 ChatGPT 提示词的方法。经过验证的"患者需求框架"用于指导将评估数据输入提示词，并附加经验证的问题，从而生成期望的护理计划建议。该框架和方法通过生成肺癌患者场景的 ChatGPT 护理计划输出进行了演示。

### Creation of a Valid ChatGPT Prompt / 创建有效的 ChatGPT 提示词

#### 第2段：提示词的重要性

> The composition of the ChatGPT prompt is crucial to the output. The ChatGPT prompt is defined as the message (containing instructions) that, when submitted to ChatGPT, will return a response. Given the known variability and occasional incorrect response to prompts, the team set out to determine if they could create a prompt that would consistently generate accurate and useful nursing care plan suggestions for hospitalized patients. Ultimately, they created and iteratively validated their two-part prompt: (a) the Patient's Needs Framework to guide entering consistent patient assessment information and (b) question/s asked of ChatGPT that would generate high-quality care plans from the assessment data.

ChatGPT 提示词的组成对输出至关重要。ChatGPT 提示词被定义为提交给 ChatGPT 后会返回回复的消息（包含指令）。鉴于提示词已知的变异性和偶尔的错误回复，团队着手确定是否能创建一个能够持续为住院患者生成准确且有用的护理计划建议的提示词。最终，他们创建并迭代验证了由两部分组成的提示词：(a) 用于指导输入一致性患者评估信息的"患者需求框架"；(b) 向 ChatGPT 提出的问题，用于从评估数据生成高质量护理计划。

#### 第3段：理论基础

> The Basic Human Needs theory and the Situation-Background-Assessment-Recommendation (SBAR) principles were used to develop the initial Patient's Needs Framework. The Basic Human Needs theory emphasizes the importance of assessing the whole person's needs, while the SBAR model underscores identifying the health problem and the background information needed to understand the patient's current situation and medical history. Integrating these two theories, the framework contains six domains: (1) Situation/Background, (2) Physical, (3) Safety, (4) Psychosocial, (5) Spiritual/Culture, and (6) Nursing Recommendation. Each domain of the Patient's Needs Framework corresponds to a specific aspect of the patient's health situation that should be included in the ChatGPT prompt to ensure holistic representation of a patient's medical history and current needs.

基本人类需求理论和"情境-背景-评估-建议"（SBAR）原则被用于开发初始的"患者需求框架"。基本人类需求理论强调评估人的整体需求的重要性，而 SBAR 模型则强调识别健康问题和理解患者当前状况及病史所需的背景信息。整合这两种理论，该框架包含六个域：(1) 情境/背景、(2) 生理、(3) 安全、(4) 心理社会、(5) 灵性/文化、(6) 护理建议。"患者需求框架"的每个域对应患者健康状况的一个特定方面，应包含在 ChatGPT 提示词中，以确保全面呈现患者的病史和当前需求。

### Patient's Needs Framework: Six Domains / 患者需求框架：六大域

**域 1. 情境/背景 (Situation/Background)**
- 患者人口统计学信息（年龄、性别、种族、民族）
- 相关既往病史和用药
- 患者当前主要病症或并发症
- 入院时用药

**域 2. 生理 (Physical)**
- 气道、呼吸、循环-生命体征问题
- 神经系统状态：清醒，对人、地点、时间和情境的定向力
- 患者主观症状
- 头到脚评估异常/解剖部位
- 营养、水分、排泄或活动能力方面的问题
- 其他护理观察或相关实验室检查

**域 3. 安全 (Safety)**
- 哪些患者问题可能导致医院差错、事故或感染？

**域 4. 心理社会 (Psychosocial)**
- 异常行为状态或举止
- 护士能为患者的心理社会健康（如应对）提供哪些照护者/家属或患者支持（如会诊、咨询）？

**域 5. 灵性/文化 (Spiritual/Culture)**
- 需要护士立即处理的灵性支持或文化（饮食、信仰、价值观）或宗教关切

**域 6. 护理建议 (Nursing Recommendation)**
- 患者/护士的护理目标

### Iterative Design / 迭代设计过程

#### 第4段：以人为中心的迭代设计

> The team utilized the Iterative Human-Centered Design approach to ultimately ensure that the final Patient's Needs Framework and question/s requesting care plan suggestions consistently generate the desired output. The approach entailed three experts (FDS, LGJ, OOM) engaging in repeated rounds of entering the prompt content using 22 diverse hypothetical patient cases from the Simulation Learning System by Elsevier. The goal of the iterations was to continue rounds of fine-tuning the Framework and question/s until ChatGPT output care plan suggestions were consistent across independently entered expert prompts (for each case) and aligned with the gold standard care plan of the corresponding cases. The repeated rounds included (a) independent expert prompt entry; (b) comparison of the three experts' outputs and closeness to gold standard plans (for each hypothetical case); and (c) experts reaching a consensus on changes to be made for the next round. The final Patient's Needs Framework and question/s reached the desired goal after 10 rounds.

团队利用迭代式以人为中心的设计方法，最终确保最终的"患者需求框架"和请求护理计划建议的问题能持续生成期望的输出。该方法包括三名专家（FDS、LGJ、OOM）使用 Elsevier 模拟学习系统中的 22 个不同假设患者案例，进行多轮提示词内容输入。迭代的目标是持续微调框架和问题，直到 ChatGPT 输出的护理计划建议在三位专家独立输入的提示词（每个案例）之间保持一致，并与相应案例的金标准护理计划对齐。重复轮次包括：(a) 专家独立输入提示词；(b) 比较三位专家的输出及其与金标准计划的接近程度（每个假设案例）；(c) 专家就下一轮需要做出的更改达成共识。最终的"患者需求框架"和问题在 10 轮后达到了期望目标。

#### 第5段：三个迭代阶段

> **Initial Evaluation (Iteration 1):** The first iteration involved the analysis of a single case using the framework's initial five domains. At this stage, the framework included limited clinical information (such as demographics, current health condition).
>
> **Framework Expansion (Iterations 2-7):** During these iterations, the analysis was extended to 18 additional cases. The goal was to integrate more context and clinical information into each domain of the framework. This included past medical history, medication profiles, neurological status, and others. The updated framework enhanced its capacity to address the varied needs of individuals.
>
> **Refinement (Iterations 8-10):** In the final three iterations, the framework was further enriched by introducing a new domain focused on nursing recommendations and measurable patient goals.

**初始评估（第 1 轮）**：第一轮迭代涉及使用框架最初的五个域分析单个案例。在此阶段，框架包含有限的临床信息（如人口统计学信息、当前健康状况）。

**框架扩展（第 2-7 轮）**：在这些迭代中，分析扩展到另外 18 个案例。目标是将更多上下文和临床信息整合到框架的每个域中，包括既往病史、用药概况、神经系统状态等。更新后的框架增强了其应对个体多样化需求的能力。

**精炼（第 8-10 轮）**：在最后三轮迭代中，通过引入一个聚焦于护理建议和可测量患者目标的新域，进一步丰富了框架。

### Standardized Nursing Terminologies / 标准化护理术语

#### 第6段

> The use of SNTs to document nursing care provides consistency in communicating definitions and suggesting nursing practices. The researchers used SNTs recognized by the American Nurses Association, including: NANDA International (11th ed.) for nursing diagnoses; Nursing Outcomes Classification—NOC (7th ed.) for outcomes/goals; Nursing Interventions Classification—NIC (6th ed.) for interventions.

使用标准化护理术语（SNTs）记录护理提供了沟通定义和建议护理实践的一致性。研究人员使用了美国护士协会认可的 SNTs，包括：NANDA International（第 11 版）用于护理诊断；护理结局分类（NOC，第 7 版）用于结局/目标；护理干预分类（NIC，第 6 版）用于干预措施。

### ChatGPT 提问的演化 (Table 2)

| 阶段 | 英文 | 中文 |
|------|------|------|
| **V1（第1轮）** | "What would be the top three nursing care plans using NANDA diagnoses linked to the appropriate NOC and NIC for this patient?" | "针对该患者，使用 NANDA 诊断并关联相应 NOC 和 NIC 的前三个护理计划是什么？" |
| **V2（第2-7轮）** | "What would be the top nursing care plan using NANDA diagnosis linked to the appropriate NOC and NIC for this patient?" | "针对该患者，使用 NANDA 诊断并关联相应 NOC 和 NIC 的首要护理计划是什么？"（不限数量） |
| **V3（第8-10轮）** | "What would be the top FOUR nursing care plans using NANDA diagnoses linked to the appropriate NOC and NIC for this patient? Please select NANDA, NOC, and NIC labels by order of priority" | "针对该患者，使用 NANDA 诊断并关联相应 NOC 和 NIC 的前四个护理计划是什么？请按优先级顺序选择 NANDA、NOC 和 NIC 标签" |

### Gold Standard and Validation / 金标准与验证

#### 第7段

> To assess the quality and appropriateness of the care plans generated by ChatGPT, gold-standard nursing care plans were created for the 22 case scenarios and validated through consensus by three nurses (FDS, LGJ, OOM), against which ChatGPT responses were compared.

为了评估 ChatGPT 生成的护理计划的质量和适当性，研究人员为 22 个案例场景创建了金标准护理计划，并通过三名护士（FDS、LGJ、OOM）的共识进行验证，ChatGPT 的回复与之进行比较。

#### 第8段：ChatGPT 版本

> The researchers employed GPT-3.5 (released between January and April 2023) for the initial testing of the framework-guided prompt and GPT-4 (released between May and August 2023) for validation. In the context of the study, validation refers to the process of testing the accuracy of the prompts in different ChatGPT versions. Specifically, GPT-3.5 was initially employed to create nursing care plan suggestions. These initial tests helped refine the prompts to ensure they were generalizable and applicable to various medical conditions. GPT-4 was employed to confirm that the framework-generated prompts remain effective when interfaced with the latest AI advancements.

研究人员使用 GPT-3.5（2023 年 1 月至 4 月间发布）进行框架引导提示词的初始测试，使用 GPT-4（2023 年 5 月至 8 月间发布）进行验证。在本研究中，验证是指在不同 ChatGPT 版本中测试提示词准确性的过程。具体来说，GPT-3.5 最初被用于创建护理计划建议。这些初始测试帮助改进了提示词，确保它们具有通用性并适用于各种医学状况。GPT-4 被用于确认框架生成的提示词在与最新 AI 进展对接时仍然有效。

### Application to Lung Cancer / 应用于肺癌患者

#### 第9段

> The team employed the validated Patient's Needs Framework to guide the creation of specific ChatGPT prompts. They searched for demographic and clinical information that addresses the unique care needs of lung cancer patients.

团队使用经过验证的"患者需求框架"来指导创建特定的 ChatGPT 提示词。他们搜索了针对肺癌患者独特护理需求的人口统计学和临床信息。

> Items related to the physical domain included signs and symptoms (such as difficulty breathing) that the patient was experiencing from the obstructed chest tube and pneumothorax after the lobectomy procedure.

与生理域相关的条目包括患者在肺叶切除术后因胸管阻塞和气胸而出现的症状和体征（如呼吸困难）。

#### 第10段：评估标准

> To evaluate the quality of the nursing care plan suggested by ChatGPT, the researchers compared it with the nurse-created gold-standard care plan. This evaluation involved assessing the following criteria:
> 1. **Clarity of the content:** ChatGPT-generated nursing care plan that conveys a similar idea or meaning to the gold-standard care plan
> 2. **Priority of care:** ChatGPT generates the same hierarchical rank of priority as the gold-standard care plan
> 3. **Use of the SNTs:** Correct labels per NANDA, NOC, and NIC

为了评估 ChatGPT 建议的护理计划的质量，研究人员将其与护士创建的金标准护理计划进行了比较。该评估涉及以下标准：
1. **内容清晰度**：ChatGPT 生成的护理计划是否传达了与金标准护理计划相似的思想或含义
2. **护理优先级**：ChatGPT 是否生成了与金标准护理计划相同的优先级层次排序
3. **标准化术语使用**：NANDA、NOC 和 NIC 标签是否正确

---

## Results / 结果

### 第1段：总体比较

> In comparison with the gold standard care plan, the ChatGPT-generated care plan was similar in scope, emphasizing the importance of addressing oxygenation and inadequate ventilation, preventing post-surgical infections, mitigating the risk of falls, and fostering coping strategies to support the emotional well-being of the patient and family members.

与金标准护理计划相比，ChatGPT 生成的护理计划在范围上相似，强调了处理氧合不足和通气不当的重要性、预防术后感染、降低跌倒风险，以及培养应对策略以支持患者和家属的情感健康。

### Priority of Care Alignment / 护理优先级对齐

#### 第2段

> Compared to the priority of lung cancer care for older adults, ChatGPT accurately identified oxygenation issues as the highest priority in the nursing care plan. Similar to the gold standard nursing care plan, ChatGPT identified the risk of infection in surgical wounds as the second priority involving the patients' physical needs. ChatGPT's output and the gold standard also coincided in identifying the risk of falls as the third priority of care. While psychological distress was acknowledged in the care plan, it was ranked as the least urgent issue at admission. This finding suggests that the ChatGPT-generated nursing care plan provided a comprehensive list of appropriate interventions with properly ranked priorities for the patient's needs.

与老年肺癌患者的护理优先级相比，ChatGPT 准确地将氧合问题识别为护理计划中的最高优先级。与金标准护理计划类似，ChatGPT 将手术切口感染风险识别为涉及患者生理需求的第二优先级。ChatGPT 的输出与金标准在将跌倒风险识别为第三护理优先级方面也一致。虽然护理计划中承认了心理困扰，但它被排在入院时最不紧急的问题。这一发现表明，ChatGPT 生成的护理计划提供了一份全面的适当干预措施清单，并为患者的需求正确排列了优先级。

**护理优先级对照表**：

| 优先级 | ChatGPT 生成 | 金标准 | 是否一致 |
|--------|-------------|--------|---------|
| 1 | 氧合与通气不足 | 氧合与通气不足 | ✓ |
| 2 | 术后感染预防 | 术后感染预防 | ✓ |
| 3 | 跌倒风险管理 | 跌倒风险管理 | ✓ |
| 4 | 心理困扰/情感支持 | 心理困扰/情感支持 | ✓ |

### Use of Standardized Nursing Terminologies / 标准化护理术语使用

#### 第3段

> The researchers further assessed the use of SNTs by the ChatGPT-generated nursing care plan. Of 16 labels (NANDA: n = 4, NOC: n = 4, NIC: n = 8), 11 (69%) were standardized terms (NANDA: n = 1, NOC: n = 2, NIC: n = 8). The other terms generated by ChatGPT, though not from SNT, were appropriate for managing the lung cancer case and were close matches of SNT terms in the gold standard plan. However, further effort is needed to determine how LLMs might be used to generate care plans entirely coded in SNT.

研究人员进一步评估了 ChatGPT 生成的护理计划对标准化护理术语的使用情况。在 16 个标签中（NANDA: n=4, NOC: n=4, NIC: n=8），11 个（69%）是标准化术语（NANDA: n=1, NOC: n=2, NIC: n=8）。ChatGPT 生成的其他术语虽然不来自 SNT，但对于管理该肺癌病例是适当的，且与金标准计划中的 SNT 术语高度接近。然而，还需要进一步的努力来确定如何使用 LLMs 生成完全以 SNT 编码的护理计划。

**SNT 匹配率汇总**：

| 术语类型 | 匹配数 | 匹配率 |
|---------|--------|--------|
| NANDA 诊断 | 1/4 | 25% |
| NOC 结局 | 2/4 | 50% |
| NIC 干预 | **8/8** | **100%** |
| **总计** | **11/16** | **69%** |

### Additional Features / 额外特征

#### 第4段

> A distinct feature of ChatGPT-generated nursing care plan is the provision of explanations for each NIC intervention. For instance, Oxygen Therapy (NIC label) is accompanied by complementary information on administering supplemental oxygen to maintain normal saturation levels. Furthermore, ChatGPT suggested four additional NIC interventions, which were not present in the gold-standard care plan but aligned with the patient's needs. For enhancing respiratory status, Airway Management and Respiratory Monitoring interventions were recommended. To promote patient safety and prevent infection and falls, ChatGPT suggested incorporating Infection Protection and Mobility Assistance interventions, respectively. These recommendations further underscore the potential value of AI assistance in identifying comprehensive care needs for patients.

ChatGPT 生成的护理计划的一个显著特征是为每项 NIC 干预提供解释说明。例如，"氧疗"（NIC 标签）附带了关于给予补充氧气以维持正常血氧饱和度水平的补充信息。此外，ChatGPT 建议了四项额外的 NIC 干预措施，这些措施不在金标准护理计划中，但与患者的需求一致。为增强呼吸状态，推荐了"气道管理"和"呼吸监测"干预。为促进患者安全并预防感染和跌倒，ChatGPT 分别建议了"感染防护"和"活动辅助"干预。这些建议进一步强调了 AI 辅助识别患者综合护理需求的潜在价值。

**ChatGPT 额外建议的 4 项 NIC 干预**：

| 干预措施 | 目的 |
|---------|------|
| 气道管理 (Airway Management) | 增强呼吸状态 |
| 呼吸监测 (Respiratory Monitoring) | 增强呼吸状态 |
| 感染防护 (Infection Protection) | 预防感染 |
| 活动辅助 (Mobility Assistance) | 预防跌倒 |

---

## Discussion / 讨论

### 第1段：总体评价

> This article presented promising evidence of ChatGPT's feasibility in generating nursing care plans for a hypothetical older patient with lung cancer, demonstrating the potential of employing AI in nursing documentation systems. With prompts generated using the framework, ChatGPT produced high-quality nursing care plans for lung cancer patients that recognized and addressed the patient's needs. Similar to the gold standard nursing care plan, the ChatGPT-generated plan took into account the whole person's needs, emphasizing the importance of addressing the highest priority of care, such as oxygenation and ventilation, while also addressing other aspects of care, such as safety promotion and psychological well-being for both the patient and family members.

本文呈现了 ChatGPT 在为假设的老年肺癌患者生成护理计划方面可行性的有力证据，展示了在护理文档系统中使用 AI 的潜力。通过使用该框架生成的提示词，ChatGPT 为肺癌患者生成了高质量的护理计划，识别并满足了患者的需求。与金标准护理计划类似，ChatGPT 生成的计划考虑了全人需求，强调了处理最高优先级护理（如氧合和通气）的重要性，同时也关注了其他护理方面，如患者和家属的安全促进和心理健康。

### 第2段：ChatGPT 的独特贡献

> One notable feature of ChatGPT-generated plan was the provision of explanations for each NIC intervention, which provided a concise description of associated nursing activities applicable to the case. This is helpful for nurses unfamiliar with nursing terminology labels to better understand the actions that need to be performed. Additionally, ChatGPT suggested NIC interventions not included in the nurse-generated plan but aligned with the patient's needs. These recommendations underscore the potential value of AI assistance in improving nursing practice. ChatGPT did not always use labels from the NANDA, NOC, and NIC classifications as instructed, though the non-standardized terms were close equivalents of their SNT counterparts.

ChatGPT 生成计划的一个显著特征是为每项 NIC 干预提供了解释说明，简要描述了适用于该案例的相关护理活动。这有助于不熟悉护理术语标签的护士更好地理解需要执行的操作。此外，ChatGPT 还建议了护士生成的计划中未包含但与患者需求一致的 NIC 干预措施。这些建议强调了 AI 辅助改善护理实践的潜在价值。ChatGPT 并不总是按照指示使用 NANDA、NOC 和 NIC 分类中的标签，尽管非标准化术语是其 SNT 对应术语的接近等价物。

### 第3段：局限性

> The study presented a hypothetical case that demonstrated the promise of AI-based systems such as ChatGPT as supportive tools generating high-quality and comprehensive nursing care plans for older patients with lung cancer. However, it is essential for nurses to use their clinical expertise to evaluate AI recommendations critically before making clinical decisions, considering the patient's unique needs, clinical context, safety, and ethics. Further research for other simulated cases in oncology is needed.

该研究呈现了一个假设案例，展示了基于 AI 的系统（如 ChatGPT）作为支持工具为老年肺癌患者生成高质量、全面的护理计划的前景。然而，护士在做出临床决策之前，必须运用其临床专业知识批判性地评估 AI 推荐，考虑患者的独特需求、临床背景、安全性和伦理。需要针对肿瘤学中其他模拟案例进行进一步研究。

---

## Implications and Conclusions / 启示与结论

### 第1段

> This study demonstrates the potential of using AI-based systems such as ChatGPT to generate nursing care plan documentation aligned with lung cancer patients' needs. While the generated care plans show promise, nurses need to evaluate these plans critically in the context of the patient's unique needs. The field can expect to see more AI application in medical and nursing contexts with the potential to enhance the accuracy and precision of care. However, the nursing profession must remember that nurses' expertise, communication, and empathy with their patients remain irreplaceable. The development of a comprehensive Patient's Needs Framework for nursing assessment and targeted questions is crucial in guiding AI-assisted nursing care planning.

本研究展示了使用基于 AI 的系统（如 ChatGPT）生成与肺癌患者需求一致的护理计划文档的潜力。虽然生成的护理计划展现了前景，但护士需要在患者独特需求的背景下批判性地评估这些计划。该领域可以预期在医学和护理背景下看到更多 AI 应用，有潜力增强护理的准确性和精确性。然而，护理专业必须记住，护士的专业知识、沟通能力和对患者的同理心仍然是不可替代的。开发全面的"患者需求框架"用于护理评估和针对性问题对于指导 AI 辅助护理计划制定至关重要。

### 第2段：框架的兼容性

> The method for generating prompts was compatible with different versions of ChatGPT (GPT-4 and GPT-3.5) and is expected to achieve better outcomes with future more advanced versions.

生成提示词的方法与不同版本的 ChatGPT（GPT-4 和 GPT-3.5）兼容，预计随着未来更先进版本的出现将取得更好的结果。

### 第3段：未来研究方向

> Future research should consider scenarios not included in these initial evaluations. Testing with additional scenarios would be important for assessing the framework's adaptability and accuracy in different contexts. In addition, future studies should explore the potential utilization of AI in formulating nursing care plans coded with SNTs for other clinical conditions and investigate the feasibility and effectiveness of implementing AI systems in real-world scenarios. The article also extends new opportunities for the future development of software and tools capable of intermediating and facilitating the design of prompts, enabling more efficient use of LLMs in nursing care documentation.

未来的研究应考虑这些初始评估中未包含的场景。使用更多场景进行测试对于评估框架在不同背景下的适应性和准确性非常重要。此外，未来的研究应探索 AI 在为其他临床状况制定以 SNT 编码的护理计划方面的潜在应用，并调查在现实场景中实施 AI 系统的可行性和有效性。本文还为未来开发能够中介和促进提示词设计的软件和工具提供了新机遇，从而更高效地在护理文档中使用 LLMs。

---

## 核心术语速查

| 英文缩写 | 英文全称 | 中文 |
|---------|---------|------|
| AI | Artificial Intelligence | 人工智能 |
| LLM | Large Language Model | 大语言模型 |
| SNT | Standardized Nursing Terminology | 标准化护理术语 |
| NANDA | North American Nursing Diagnosis Association | 北美护理诊断协会 |
| NOC | Nursing Outcomes Classification | 护理结局分类 |
| NIC | Nursing Interventions Classification | 护理干预分类 |
| SBAR | Situation-Background-Assessment-Recommendation | 情境-背景-评估-建议 |
| EHR | Electronic Health Record | 电子健康记录 |
| BPH | Benign Prostatic Hyperplasia | 良性前列腺增生 |
| IPSS | International Prostate Symptom Score | 国际前列腺症状评分 |
| VAS | Visual Analog Scale | 视觉模拟评分法 |
| SAS | Self-Rating Anxiety Scale | 焦虑自评量表 |
| SDS | Self-Rating Depression Scale | 抑郁自评量表 |
| RCT | Randomized Controlled Trial | 随机对照试验 |

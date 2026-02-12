---
name: se-paper-writing
description: 面向软件工程（ICSE/FSE/ASE/ISSTA/ICPC/SANER、TOSEM/TSE/EMSE/IST/JSS 等）论文与申请书的写作工作流、结构模板与评审友好检查清单；特别强调“证据链（claim→method→evaluation）”“RQ 驱动评测”“Threats to Validity”“可复现与 artifact”。当需要把一个软工研究点写得更有依据、更像顶会/顶刊论文（而不是综述式堆砌）时使用。
---

# 软件工程论文写作（SE Paper Writing）Skill

本 Skill 目标：把“研究想法”转成“评审可读、可验证、可复现”的软工论文叙事与结构。

本 Skill 的写作习惯总结来源于：
- 陈翔老师（Xiang Chen）近五年公开可获取的论文 PDF（当前自动抓到 `9` 篇）+ OpenAlex 可获得摘要（当前 `64` 条）。索引与下载状态见 `templog/writingskills/outputs/xchencs_last5y_se_index.json` 与 `templog/writingskills/outputs/xchencs_last5y_se_summary.md`。
- arXiv `cs.SE`（可批量下载、便于扩充样本）。索引与汇总见 `templog/writingskills/outputs/arxiv_csse_index.json` 与 `templog/writingskills/outputs/arxiv_csse_summary.md`。

---

## 0) 开写前先要齐的输入（不要直接开写）

先把下面信息要全（缺一就先补齐或显式写“假设/占位”）：
- **论文类型**：Technique / Empirical Study / System&Tool / Benchmark&Dataset / Survey（不同类型的“贡献点”与“评测设计”写法不同）
- **一句话主张（Thesis Claim）**：`我们提出 X，用 Y 机制解决 Z 问题，在 W 场景上相对 baseline 提升/降低 …`
- **对象与场景**：系统/语言/框架/数据来源（工业 or 开源；版本范围；约束）
- **对照基线（Baselines）**：至少 2-3 个强 baseline（同类方法 + 最常用传统/商业工具）
- **评测资产**：数据集（规模、来源、清洗、标签）、指标（Precision/Recall/MRR、时间/内存、人工评估一致性等）、统计方法（效应量/显著性）
- **可复现计划**：代码/数据/脚本/seed/环境（哪怕先写“我们将开源 …”）

> 写作原则：软工论文不是“观点文”，而是“证据文”。先把证据链拼起来，再写漂亮话。

---

## 1) 软工论文的“证据链”叙事骨架（最重要）

把整篇论文写成一条可追踪的链：
1. **Problem**：为什么现有方法不行（不是“有缺点”，而是“会导致可测的失败/成本”）
2. **Insight**：你观察到的结构性规律/机会（可复现、可被反驳）
3. **Method**：基于该 insight 的机制（可实现、可解释）
4. **Evaluation**：围绕 claim 设计的 RQ 与对照实验（可重复、可消融）
5. **Result**：用数字与误差条回答 RQ，说明适用边界与失败案例

写作时，每一节都要能回答：**“这段文字对应证据链的哪一环？”**

---

## 2) 摘要（Abstract）写法：四段式 + 数字化

软工摘要建议按 4 句/4 段写（句子可拆分，但信息顺序保持）：
1. **Context + Pain**：在什么任务/场景下，痛点是什么（量化/例子）
2. **Gap**：现有方法为什么做不到（具体到“会错在哪里/慢在哪里”）
3. **Approach**：我们提出什么（1 句话概述核心机制；不展开细节）
4. **Evaluation + Results**：在什么数据/基准上，和谁比，提升多少；再补一句结论（泛化/效率/可用性）

可直接套用的句模版（按需改写）：
- *We study … and find that … causes … in …*  
- *To address this, we propose …, which … by …*  
- *We evaluate … on … (N projects / M issues / K models). Results show … (↑x% / ↓y% / speedup z×).*  
- *Our findings suggest … and …*

经验信号（来自本次样本统计）：OpenAlex 可拿到的摘要中，约 **76.6%** 包含数字结果，约 **68.8%** 明确出现 “we propose/present/introduce/develop” 这类动作动词。  
=> **不要写“泛泛背景 + 一句话方法 + 空泛结论”，要写“可测结果”。**

摘要里常见的“软工句式组件”（对齐评审预期，但不要空喊）：
- **Gap 句**：`... has not been thoroughly investigated.` / `... remains under-explored.`  
  - 用法：紧跟具体场景与失败模式，不要单独成段。
- **行动句**：`We propose a novel approach/technique to ...`  
  - 用法：后面必须跟 1 个机制关键词（e.g., graph-based / mutation-based / prompt-based）。
- **结果句**：`Experimental results show that ...` / `Results show that ...`  
  - 用法：至少带 1 个数字 + 1 个对照对象（baseline/setting）。

---

## 3) 引言（Introduction）写法：三段 + 贡献点（不堆 Related Work）

推荐结构（ICSE/FSE/ASE 常见）：
1. **第一段：任务重要性 + 真实困难（可用一个短例子）**  
   - 把读者拉进“真实工程痛点”，别上来就综述。
2. **第二段：现有方法的关键失败模式（1-2 条）**  
   - 用“会导致什么后果”写缺点；最好能对应后面的 RQ/实验。
3. **第三段：你的方法概述 + 为什么有效（1 个 insight）**  
   - 讲机制，不讲模块清单。
4. **贡献点列表（Contributions）**（建议 3 条，最多 4 条）  
   - 每条必须能落到“一个可交付物/一个评测问题/一个可复现实证”。

贡献点写法建议（从“主张”出发）：
- **C1（Method）**：提出 X（关键机制一句话，避免 marketing 词）
- **C2（System/Tool）**：实现原型/工具，支持 …（给出范围与限制）
- **C3（Evaluation）**：在 … 上与 … 对比，得到 …（数字化）
- **C4（Dataset/Benchmark，可选）**：构建/公开 …（若真有）

避免的坏写法：
- “我们提出一个新框架/新方法/新系统”但不说新在哪里，也不说怎么验证
- “贡献点=本文结构复述”（比如“我们做了实验/我们写了系统”）

---

## 4) RQ 驱动评测：把“实验”写成“回答问题”

软工论文的评测部分，最评审友好的写法是 **Research Questions (RQs)**。

常用 RQ 套件（按论文类型选 2-4 个）：
- **RQ1 Effectiveness**：方法能否更准/更好？（主指标 + 强 baseline）
- **RQ2 Efficiency/Scalability**：成本如何？（时间/内存/吞吐；随规模曲线）
- **RQ3 Ablation/Component**：哪个机制带来收益？（消融 + 误差条）
- **RQ4 Generality/Transferability**：跨项目/跨语言/跨版本是否成立？
- **RQ5 Practicality**：开发者可用吗？（用户研究/问卷/案例/工业反馈）

经验信号（来自可下载的 9 篇 PDF 全文粗检）：约 **6/9** 明确出现 `RQ1`（说明这种写法在该研究群体里很常见）。  
=> **把实验标题从“Experiment Setup / Results”改成 RQ，是最便宜的“学术化升级”。**

RQ 写作注意：
- RQ 必须对应“论文主张”的一个维度；每个 RQ 都要能在结论中被一句话回答。
- 每个 RQ 的结果段落按同一结构写：**结论句（带数字）→ 解释原因 → 失败案例/边界**。

---

## 5) Threats to Validity（软工特有的“自证清醒”）

Threats 不是“例行公事”，写好会显著提升可信度。

建议按三类写（每类 2-4 条，带对策）：
- **Construct validity**：指标是否代表你想测的东西？（标签质量、代理指标偏差）
- **Internal validity**：因果是否站得住？（实现 bug、参数调优不公平、数据泄漏）
- **External validity**：能否泛化？（数据集偏、语言/框架偏、版本偏）

经验信号（来自可下载的 9 篇 PDF 全文粗检）：约 **4/9** 出现 Threats to Validity。  
=> 在 ICSE/FSE/ASE/EMSE/IST/JSS 写作里，这一节通常是“加分项”，尤其对实证/工具类工作。

写法要点：
- 不要只写“可能有威胁”。要写“威胁是什么→可能导致什么偏差→我们怎么缓解→剩余风险是什么”。

---

## 6) Related Work：按“问题/机制”分组，用对比句收尾

Related Work 的目标不是“引用尽可能多”，而是让评审相信：
- 你知道最相关的工作；
- 你的差异点是明确且必要的；
- 你没有把已有方法换皮重写。

推荐写法：
- 以 2-4 个小节分组：`Problem-based grouping`（比如 “fault localization / LLM for SE / graph-based …”）
- 每组最后用 1-2 句“对比句”收束：`Unlike X, we …` / `Different from Y, our method …`

禁忌：
- 变成综述；把引言第二段的“失败模式”搬过来重复。

---

## 7) 软工论文语言与排版的微习惯（可直接执行）

- **动词优先**：用 propose / design / implement / evaluate / find / observe，不用“discuss / explore / try”做主陈述
- **避免夸张副词**：significantly / dramatically 等只在有统计/数字时用
- **同一概念同一叫法**：术语表（Terminology）统一大小写、缩写首次展开
- **图表先行**：复杂方法先给 1 张 overview figure；实验结果尽量图（曲线/箱线/散点）而不是大表格堆数字
- **把“失败案例/误用场景”写出来**：一段 “When it fails …” 往往比再多 5 个 baseline 更加分
- **复现实用信息**：数据集版本、采样标准、过滤规则、seed、硬件、运行时环境（最好集中在 Evaluation Setup）

---

## 8) 交付给 Codex 的写作任务拆分（让它真的能帮你写）

把大任务拆成小任务，效果最好：
1. 让 Codex 先生成 **证据链**（Problem→Insight→Method→Evaluation→Result）的一页提纲
2. 再分别生成：Abstract / Intro / RQs&Setup / Threats / Related Work
3. 最后做 **一致性检查**：术语统一、RQ 与结论对齐、贡献点与实验对齐、claim 不超出证据

---

## 9) 本次可获取 PDF 列表（用于“细读对齐”）

本地路径见 `caches/pdfs_*`；索引 JSON 里也记录了 URL 与下载状态。

建议细读顺序（更偏软工写作范式）：
1. ICSE/ASE/TOSEM/EMSE/JSS（结构更标准，Threats/RQ 更典型）
2. ICPC（工程叙事与评测写法）
3. SEKE/COMPSAC/EAAI（相对更“工程/应用”，可对比写作差异）

---
name: yg-paper-writing
description: 总结杨光（Guang Yang）在软工/代码智能方向论文中常用的标题与摘要写法、叙事节奏与证据表达；用“可复用模板 + 可量化检查清单”帮助你把研究点写得更像 TOSEM/TSE/EMSE/ICSE/ASE/ACL 等风格（强调 action verb + baseline + results）。
---

# 杨光论文写作风格与技巧（Guang Yang Writing Style）

本 Skill 的目标：把你的研究内容写成“评审一眼能读懂、能抓到贡献、能看见证据链”的软工论文叙事。

本 Skill 的信号来源（可复现）：
- 解析 `https://ntdxyg.github.io/publications/` 得到 `39` 条论文条目；
- 公开可下载 PDF `6` 篇（仅做首 1–3 页结构信号提取；不做付费墙/反爬绕过）；
- 摘要来自网页嵌入数据（已在索引里落盘）。

索引与汇总见：
- `templog/writingskills/outputs/yg_publications_index.json`
- `templog/writingskills/outputs/yg_publications_summary.md`

---

## 1) “可观察的风格签名”（用数据约束写作）

### 1.1 标题（Title）

从全量 39 条标题统计（见 `yg_publications_summary.md`）：
- **冒号结构**（`A: B`）出现 `56.4%`：标题更倾向“先给任务/立场，再给方法/机制/角度”。
- **缩写/方法名**（全大写 Acronym）出现 `17.9%`：常把方法名做成可引用的“术语锚点”（便于评审记住）。
- “**Less is More**”作为修辞标题出现 `5.1%`：用强立场句式吸引注意，但后文必须用实验把立场“兑现”。

可直接套用的标题范式：
- `Claim/Goal: Mechanism`：*Less is More: … via …* / *X: … with …*
- `Task: Data/Signal/Structure-aware Method`：*…: Syntax-Aware …* / *…: Retrieval-Augmented …*

### 1.2 摘要（Abstract）

英文摘要（38 条）的典型信号（见 `yg_publications_summary.md`）：
- **动作动词**（`we propose/present/introduce/develop...`）`86.8%`
- **数字**（规模/提升/开销等）`65.8%`
- **结果句**（`results show/suggest/indicate...` 或等价表达）`65.8%`
- **baseline** 在摘要中被点名 `60.5%`
- 连接词 “**However**” 出现 `52.6%`（常用于“从背景→痛点→缺口”的转折）
- “**novel**” 出现 `47.4%`（但通常伴随机制关键词，而不是空喊）

摘要长度（英文 38 条）：
- 平均 `~206` 词，中位数 `204`；平均 `~9.2` 句（更偏“信息密度型”，不是 3 句短摘要）。

结论：杨光风格的摘要更像一条“证据链速览”，而不是“背景+一句方法+空泛结论”。

---

## 2) 他的摘要写法：强转折 + 强动作 + 强对照 + 强数字

建议你按下面顺序写（句子可多，但信息顺序别乱）：

1. **Context（背景/任务）**：一句话交代任务与价值（别综述）。
2. **However（缺口/痛点）**：用 *However* 把失败模式说具体（会导致什么可测后果）。
3. **Action（我们做了什么）**：*We propose …*，紧跟 1 个“机制关键词”（graph / retrieval / prompt / mutation / pruning / robustness…）。
4. **Evaluation（怎么证）**：数据/对象/基线/指标至少点 2 个（让评审知道你“会做实验”）。
5. **Results（结论数字化）**：最少 1 个数字 + 1 个对照对象（baseline / SOTA / ablation）。

可复用句模版（按需替换括号）：
- *However, existing approaches (fail because …), leading to (measurable cost/error) in (scenario).*
- *We propose **METHOD**, which (core mechanism) by (key insight/signal/structure).*
- *We evaluate **METHOD** on (dataset/benchmarks) against (baselines) using (metrics).*
- *Results show that **METHOD** (improves/reduces/speeds up) (X%) over (baseline) while (tradeoff).*

---

## 3) 证据链写作技巧：把“主张”写成可检验命题

把论文主张写成一行（写作时反复对齐）：

`我们提出 METHOD，用 MECHANISM 解决 TASK/PROBLEM，在 DATA/SCENARIO 上相对 BASELINE 带来 RESULT（并给出边界/代价）。`

对应地，把评审最在意的 4 个槽位写齐：
- **Method**：新在哪里（不是“用了 Transformer”，而是“引入了 X 结构/约束/信号来解决 Y 失败模式”）
- **Baselines**：比谁强（同类 SOTA + 常用强基线）
- **Datasets/Subjects**：在哪些对象上成立（规模、来源、过滤规则）
- **Results**：提升多少、成本多少、什么时候不行（边界条件）

---

## 4) 写作落地：一套“评审友好”的结构清单

### 4.1 Introduction（建议 3 段 + 贡献点 3 条）
- 段 1：任务重要性 + 一个具体工程困难（别上来 related work）
- 段 2：However + 现有方法关键失败模式（1–2 条，能映射到 RQ/实验）
- 段 3：We propose + 核心机制（1 个 insight）+ 你如何验证
- Contributions（3 条足够）：
  1) **Technique**：方法/机制（可实现、可解释）
  2) **Evaluation**：评测设计（RQ + baselines + datasets + metrics）
  3) **Artifact/Insight**：可复现资产/发现（数据、工具、分析）

### 4.2 Evaluation（围绕 claim 设计，而不是“跑一堆实验”）
按 RQ 组织（每个 RQ 只回答一个命题）：
- RQ1：有效性（相对 baselines 的提升）
- RQ2：效率/成本（时间/显存/能耗/训练开销）
- RQ3：消融与原因（哪个机制贡献最大，失败案例是什么）
- RQ4（可选）：泛化/迁移（不同项目/语言/场景）

在每个结果段落结尾写“判决句”：
- *Takeaway:* 用一句话把数字翻译成结论（并点出适用条件）。

---

## 5) 复现与脚本（如何更新这份风格总结）

在 `C:\\Users\\daoge\\Desktop\\codes` 下运行：

```powershell
python templog/writingskills/pipelines/collect_yg_publications.py --no-resume
python templog/writingskills/pipelines/collect_yg_publications.py --refresh-missing
```

说明：
- 脚本只下载公开可访问 PDF，不会尝试绕过付费墙/反爬；因此 PDF 下载率可能长期偏低。
- 若你能在校内/机构网络手动补齐 PDF，再运行 `--refresh-missing` 可把写作信号统计变得更可靠。

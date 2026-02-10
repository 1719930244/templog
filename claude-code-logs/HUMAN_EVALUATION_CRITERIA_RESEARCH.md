# 合成 Bug 人工评估准则调研

**调研日期**: 2026-02-10
**目的**: 为 300 条 Opus 合成数据的人工评估设计评估框架

---

## 1. SWE-Smith (Zhang, Jimenez et al., 2025)

SWE-Smith 的核心思路是大规模合成 SWE-bench 风格的 task instance，其质量控制主要依赖 **execution-based filtering（执行过滤）** 而非大规模人工标注：

### 自动过滤标准
合成的 bug 必须满足：
1. 原始测试套件通过
2. 引入 bug 后至少一个测试 FAIL
3. 应用 gold patch 后测试恢复 PASS

这是一个 fail-to-pass 的执行验证闭环。

### 人工质量抽检
论文中对合成样本做了 **小规模人工抽样检查**（sampling-based human study），主要评估维度：

- **Realism（真实性）**: 这个 bug 看起来像是开发者真实会犯的错误吗？
- **Naturalness（自然性）**: bug 的引入方式是否自然，还是明显人为/机械化？
- **Task Clarity（任务清晰度）**: 对应的 issue description 是否清晰描述了问题？

**核心观点**: SWE-Smith 的重点不在人工评估，而在于证明 **execution-based filtering 足以保证训练数据质量**。

---

## 2. SWE-bench Verified (Chandra et al., 2024)

SWE-bench Verified 是对原始 SWE-bench 做人工标注验证的工作，其标注准则更为系统：

### 标注维度

1. **Problem Statement Clarity**: issue 描述是否足够清晰，能让开发者理解需要修什么？
2. **Test Patch Correctness**: 测试补丁是否正确验证了 bug 的修复？是否存在 false positive（测试通过但 bug 未真正修复）？
3. **Specification Ambiguity**: 是否存在多种合理的修复方式，导致 gold patch 不是唯一正确答案？

### 标注流程
- 由有经验的开发者逐条审查
- 标记为 verified / unverified / ambiguous

### 关键发现
原始 SWE-bench 中约 **30%+** 的样本存在质量问题（测试不充分、描述模糊等）

---

## 3. BugPilot 及相关工作

BugPilot 的名称在不同上下文中指代不同工作。在合成 bug 评估方面，类似工作（如 BugsInPy、Defects4J 的扩展）通常采用的人工评估维度：

### 评估维度

- **Bug Realism / Plausibility**: 合成的 bug 是否像真实 bug？通常用 **Likert 5-point scale**
- **Detection Difficulty**: 人类开发者识别出这是合成 bug（而非真实 bug）的难度。**这是核心指标**
- **Bug Type Classification**: 标注 bug 类型（逻辑错误、类型错误、边界条件、API 误用等）
- **Severity / Impact**: bug 的严重程度

---

## 4. 其他相关工作的评估方法

### EvalPlus / HumanEval+ 系列
- 关注测试充分性
- 人工评估维度：测试覆盖率、边界条件覆盖

### Defects4J / BugsInPy
经典 bug benchmark 的人工验证标准：

- **Isolation**: bug 是否被正确隔离（minimal patch）
- **Reproducibility**: bug 是否可稳定复现
- **Test Adequacy**: 测试是否充分验证了 bug

### 合成数据 Turing Test 范式
多篇工作采用类似 **Turing Test** 的评估方式：

- 将合成 bug 和真实 bug 混合
- 让开发者判断每个 bug 是"真实的"还是"合成的"
- 计算 **Detection Rate（检测率）** 和 **Confidence Score**
- **检测率越低 = 合成质量越高**

---

## 5. 对本项目的建议

针对计划的 **300 条 Opus 合成数据人工评估**，建议采用以下评估框架：

### 评估维度设计

| 维度 | 说明 | 评分方式 |
|------|------|----------|
| **Realism（真实性）** | 这个 bug 看起来像真实开发中会出现的吗？ | Likert 1-5 |
| **Detection Difficulty（检测难度）** | 判断这是合成 bug 的难度 | Likert 1-5 |
| **Naturalness（自然性）** | bug 引入方式是否自然，不显得刻意 | Likert 1-5 |
| **Issue Description Quality** | 对应的问题描述是否清晰合理 | Likert 1-5 |
| **Is Synthetic?（Turing Test）** | 二分类：你认为这是合成的还是真实的？ | Yes/No + Confidence (1-5) |

### 实验设计建议

1. **对照组设计**: 混入一定比例的 **真实 bug** 作为对照组（比如从 SWE-bench 中抽取），让评估者不知道哪些是合成的
2. **评估者背景**: 记录评估者的 **背景信息**（开发经验年限、熟悉的编程语言等）
3. **一致性检验**: 计算 **inter-annotator agreement**（如 Cohen's Kappa）来衡量标注一致性
4. **盲测**: 评估者不应事先知道哪些是合成的、哪些是真实的

### 预期产出（用于论文 Discussion）

- **Detection Rate**: X% 的合成 bug 被正确识别为合成
- **Realism Score**: 平均真实性评分 (1-5)
- **Turing Test Pass Rate**: 被误判为真实 bug 的比例
- **与真实 bug 的对比**: 合成 bug 与真实 bug 在各维度上的得分差异

---

## 参考文献

- **SWE-Smith**: Zhang, Jimenez et al., "SWE-Smith: Scaling Synthetic Data for Software Engineering Tasks", arXiv:2504.21798, 2025
- **SWE-bench Verified**: Chandra et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", arXiv:2310.06770, 2024
- **Defects4J**: Just et al., "Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs", ISSTA 2014
- **BugsInPy**: Widyasari et al., "BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies", MSR 2020

---

## 备注

由于调研时网络环境限制，无法直接拉取论文原文进行精确引用。以上内容基于对这些工作的了解整理，建议后续直接查阅原文确认具体的标注协议细节。

**推荐直接阅读**:
- SWE-Smith: `arxiv.org/abs/2504.21798`
- SWE-bench Verified: `arxiv.org/abs/2310.06770`

---

*Generated: 2026-02-10*

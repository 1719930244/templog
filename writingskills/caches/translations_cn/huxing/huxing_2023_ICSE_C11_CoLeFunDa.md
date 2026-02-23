# CoLeFunDa: Explainable Silent Vulnerability Fix Identification
# CoLeFunDa：可解释的静默漏洞修复识别

**来源**: ICSE 2023 | **作者**: Jiayuan Zhou 等

## 摘要
开源软件用户通常依赖安全公告发现新披露的漏洞及其补丁。然而漏洞修复通常比披露提前一周公开可用，且大多数漏洞被静默修复（提交信息不包含漏洞信息），这给攻击者提供了利用窗口。本文提出CoLeFunDa框架，包含对比学习器和函数级代码变更数据增强组件FunDa。FunDa通过无监督和有监督策略增强修复数据，对比学习器训练函数变更编码器FCBERT，最终微调用于三个下游任务：静默修复识别、CWE分类和可利用性评级分类。CoLeFunDa在所有任务上均显著优于现有最先进基线。

## 引言核心
- 漏洞修复通常比CVE披露提前一周以上公开，如Log4Shell修复比披露早11天，给攻击者提供利用窗口
- 大多数漏洞被静默修复，提交信息不包含漏洞信息，OSS用户难以理解和评估影响
- 仅识别静默修复不够，还需提供解释（CWE类别和可利用性评级）帮助用户理解漏洞
- 漏洞修复数据有限（仅占提交的0.35%）且多样（涉及多种CWE类别），传统方法难以有效学习
- 现有方法VulFixMiner使用整个提交级别的代码变更，缺乏代码上下文信息

## 方法概述
CoLeFunDa包含三个阶段。阶段一（FunDa数据增强）：对每个函数变更，通过基于变量的程序切片生成函数切片（OriFSlice和ModFSlice），生成函数变更描述（FCDesc），组合生成增强样本（FCSample）。采用自基（self-based）无监督策略和组基（group-based）有监督策略构建正样本对用于对比学习。

阶段二（函数变更表示学习）：利用对比学习进一步预训练语言模型，通过最小化正样本对距离、最大化负样本对距离来学习函数级代码变更表示，训练得到FCBERT编码器。阶段三（下游任务微调）：基于FCBERT分别微调三个模型——CoLeFunDa_fix（静默修复识别）、CoLeFunDa_cwe（CWE分类）和CoLeFunDa_exp（可利用性评级分类）。

## 关键实验发现
- RQ1（静默修复识别）：CoLeFunDa_fix在所有effort-aware指标上比VulFixMiner提升11%-14%
- RQ2（CWE分类）：CoLeFunDa_cwe在macro AUC、precision、recall和F1上比最佳基线提升6%-72%
- RQ3（可利用性评级分类）：CoLeFunDa_exp在各指标上比最佳基线提升24%-54%
- RQ4（实际应用验证）：对40个无CWE的CVE进行用户研究，37.5%（62.5%）在top-1（top-2）推荐中被正确分类

## 写作特征备注
- 标题结构：工具名: 描述（CoLeFunDa: Explainable Silent Vulnerability Fix Identification）
- 摘要是否有数字：是（62.5%、25/40 CVE）
- 是否有RQ：是（有明确的研究问题）
- 是否有Motivating Example：是（以Log4Shell为例说明静默修复的危险性）
- 贡献点数量：4

## 结论
CoLeFunDa首次提出可解释的静默漏洞修复识别框架，通过函数级代码变更数据增强和对比学习有效应对数据有限和多样性挑战，在三个下游任务上均显著优于现有方法，为OSS漏洞管理提供了实用的早期预警能力。

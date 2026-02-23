# Diffploit: Facilitating Cross-Version Exploit Migration for Open Source Library Vulnerabilities
# Diffploit：促进开源库漏洞跨版本漏洞利用迁移

**来源**: ICSE 2026 | **作者**: Zirui Chen 等

## 摘要
漏洞利用（exploit）常用于验证库漏洞的存在及其在不同版本中的影响。然而，由于版本演化中引入的破坏性变更，直接将exploit应用于其他版本往往会失败。这些失败源于触发条件的变化（如API重构）和动态环境的破坏（如构建或运行时错误）。本文提出Diffploit，一种迭代式、差异驱动的exploit迁移方法，包含上下文模块和迁移模块两个核心组件。在包含102个Java CVE和689个版本迁移任务的大规模数据集上，Diffploit成功迁移了84.2%的exploit，分别比TaRGET和IDEA高出52.0%和61.6%。此外，Diffploit发现了5个CVE报告中不准确的受影响版本范围（3个已确认），以及GitHub Advisory Database中111个未报告的版本。

## 引言核心
- 开源库漏洞可从上游传播到下游项目，评估漏洞在不同版本中的影响至关重要
- 公开的exploit通常仅适用于特定版本，直接复用到其他版本常因环境变化和触发条件演化而失败
- 现有方法主要依赖模糊测试进行执行轨迹对齐，耗时且无法处理环境级故障
- 两大核心挑战：动态环境破坏（依赖升级、运行时配置不兼容）和复杂触发条件演化（API重构、删除）
- Diffploit通过差异驱动的LLM框架，迭代利用Causing Diff和Supporting Diff实现exploit迁移

## 方法概述
Diffploit采用迭代式差异驱动方法，包含两个核心模块。上下文模块（Context Module）通过比较目标版本和参考版本的行为差异，构建迁移上下文，包括导致失败的Causing Diff（如API重命名、包结构变更）和辅助解决问题的Supporting Diff（如库内部对变更的适配代码）。迁移模块（Migration Module）利用LLM基于构建的上下文进行exploit适配，采用模拟退火策略在多次迭代中探索diff候选并逐步精化。

整个过程遵循差异驱动的闭环：每次迭代中比较目标版本和参考版本的执行输出以识别失败指标，构建迁移上下文，由LLM进行适配，然后重新执行并收集新反馈以指导下一轮迭代，逐步消除差异实现有效迁移。

## 关键实验发现
- RQ1（有效性）：Diffploit在689个版本迁移任务中成功迁移580个（84.2%），比TaRGET高52.0%，比IDEA高61.6%
- RQ2（消融研究）：各组件设计合理，完整方法比基础模型提升46.1%
- RQ3（实际应用）：发现5个CVE报告中不准确的受影响版本范围（3个已被CNA确认），向GitHub Advisory Database提交了111个缺失版本（82个已被接受）

## 写作特征备注
- 标题结构：工具命名型（Diffploit: Facilitating...）
- 摘要是否有数字：是（102个CVE、689个任务、84.2%、52.0%、61.6%、111个版本）
- 是否有RQ：是
- 是否有Motivating Example：是（CVE-2024-22257的spring-security-core示例）
- 贡献点数量：3

## 结论
Diffploit通过差异驱动的迭代迁移策略，有效解决了跨版本exploit迁移中的环境破坏和触发条件演化问题，并在实际应用中发现了多个CVE报告的不准确之处。

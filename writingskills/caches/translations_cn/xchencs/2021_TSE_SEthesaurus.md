# SEthesaurus: WordNet in Software Engineering
# SEthesaurus：软件工程领域的WordNet

**来源**: TSE 2021 | **作者**: Xiang Chen 等

## 摘要
软件工程中的自然语言处理任务（如bug报告分析、代码搜索）需要理解领域特定的词汇语义关系。通用词典（如WordNet）无法覆盖软件工程术语。本文构建了SEthesaurus，一个面向软件工程领域的同义词词典。SEthesaurus通过从Stack Overflow、GitHub等平台挖掘词汇关系，建立了包含同义词、上下位词、相关词等关系的词汇网络。

## 引言核心
- 软件工程中的NLP任务依赖词汇语义理解
- 通用WordNet缺少SE领域术语（如"commit"、"pull request"、"refactor"的领域含义）
- 现有SE词典规模小、覆盖面窄
- 核心insight：大规模SE社区数据（SO/GitHub）中蕴含丰富的词汇语义关系

## 方法概述
1. **数据收集**：从Stack Overflow标签系统、GitHub README、API文档中收集SE术语
2. **关系抽取**：使用分布式语义模型和模式匹配方法抽取词汇关系
3. **词典构建**：整合多源关系，构建结构化词汇网络
4. **质量评估**：通过人工评估和下游任务评估验证词典质量

## 关键实验发现
- SEthesaurus包含数万个SE术语和语义关系
- 在bug报告去重、代码搜索等下游任务上，使用SEthesaurus比通用WordNet效果更好
- 人工评估显示词汇关系的准确率达到较高水平

## 结论
SEthesaurus填补了SE领域词汇资源的空白，为SE中的NLP任务提供了有价值的基础设施。

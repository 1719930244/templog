# ProRLearn: Boosting Prompt Tuning-based Vulnerability Detection by Reinforcement Learning
# ProRLearn：基于强化学习增强Prompt调优的漏洞检测

**来源**: ASEJ 2024 | **作者**: Xiang Chen 等

## 摘要
软件漏洞检测是安全领域的关键任务。近年来，基于预训练模型的Prompt Tuning方法在漏洞检测中展现出潜力。然而，现有Prompt Tuning方法的prompt模板设计依赖人工经验，且难以适应不同类型的漏洞。本文提出ProRLearn，利用强化学习自动优化prompt模板，提升漏洞检测效果。

## 引言核心
- 软件漏洞每年造成巨大经济损失，自动化检测需求迫切
- Prompt Tuning将漏洞检测转化为填空任务，避免了全参数微调的高成本
- 现有方法的prompt模板固定，无法适应漏洞的多样性
- 核心insight：强化学习可以根据检测反馈动态调整prompt策略

## 方法概述
1. **Prompt空间定义**：定义prompt模板的搜索空间（模板结构、关键词、位置等）
2. **强化学习优化**：将prompt选择建模为序列决策问题，使用PPO算法优化
3. **奖励设计**：基于漏洞检测的F1分数设计奖励函数
4. **多轮迭代**：通过多轮交互逐步优化prompt策略

## 关键实验发现
- ProRLearn在多个漏洞检测数据集上优于手工设计的prompt和AutoPrompt
- 强化学习找到的prompt模板具有可解释性
- 在不同预训练模型（CodeBERT、UniXcoder）上均有效

## 结论
ProRLearn通过强化学习自动化prompt优化，有效提升了基于Prompt Tuning的漏洞检测性能。

# Automating TODO-missed Methods Detection and Patching
# 自动化检测和修补TODO遗漏方法

**来源**: TOSEM 2024 | **作者**: Zhipeng Gao 等

## 摘要
TODO注释被开发者广泛用于提醒未完成的任务，通常关联临时或次优的实现方案。理想情况下，所有等价的次优实现都应同步更新（如添加TODO注释），但开发者可能因时间限制或疏忽而遗漏，导致TODO遗漏方法的产生。本文提出TDPatcher框架，自动检测TODO遗漏方法并将TODO注释修补到正确位置。TDPatcher包含离线学习和在线推理两个阶段：离线阶段使用GraphCodeBERT和对比学习将TODO注释与次优实现编码为向量表示；在线阶段利用训练好的模型识别遗漏方法并确定修补位置。在Top-10,000 Python GitHub仓库上的评估表明TDPatcher性能优异，并在50个GitHub仓库中成功检测到26个TODO遗漏方法。

## 引言核心
- TODO注释标记当前次优方案，帮助开发者在未来开发中关注需改进之处
- 当一个方法添加了TODO注释，所有具有等价次优实现的方法都应同步更新，但实际中常被遗漏
- TODO遗漏方法中"隐藏"的次优实现可能长期损害软件质量和可维护性
- 检测TODO遗漏方法面临两个关键挑战：理解TODO注释与次优实现之间的语义映射（自然语言vs编程语言的鸿沟）；定位遗漏方法中的精确修补位置
- 手动检查大型项目中的所有方法极其耗时且易出错

## 方法概述
TDPatcher的核心思想基于两点：(1) 代码模式和文档可通过预训练模型自动编码为语义向量；(2) 对比学习可以探索TODO引入方法和TODO遗漏方法之间的关联和差异。

离线学习阶段，从Top-10,000 Python GitHub仓库收集TODO引入方法，自动构建⟨anchor, positive, negative⟩三元组训练样本。使用GraphCodeBERT将样本编码为上下文化向量，然后应用对比学习策略拉近正样本（具有等价次优实现的方法）并推远负样本（无关方法）。在线推理阶段，当新的TODO注释被添加时，利用离线训练的模型在项目中搜索可能的TODO遗漏方法，并通过成对比较确定精确的修补位置。

## 关键实验发现
- RQ1（检测有效性）：TDPatcher在TODO遗漏方法检测任务上显著优于多个基准方法
- RQ2（修补有效性）：TDPatcher能准确定位TODO注释应被修补的具体代码位置
- RQ3（实际应用）：在50个GitHub仓库的真实场景评估中，成功检测到26个TODO遗漏方法
- 对比学习策略对提升检测性能有显著贡献

## 写作特征备注
- 标题结构：动作+任务描述（Automating TODO-missed Methods Detection and Patching）
- 摘要是否有数字：是（Top-10,000仓库，26个遗漏方法，50个仓库）
- 是否有RQ：是（通过实验部分的研究问题组织）
- 是否有Motivating Example：是（Figure 1通过save_workbook和get_fullname方法展示TODO遗漏场景）
- 贡献点数量：3（新任务定义、TDPatcher框架、大规模评估）

## 结论
TDPatcher首次提出并解决了TODO遗漏方法的自动检测和修补问题，通过GraphCodeBERT和对比学习有效桥接了自然语言注释与代码实现之间的语义鸿沟，在真实项目中验证了实用价值。

# QTC4SO: Automatic Question Title Completion for Stack Overflow
# QTC4SO：Stack Overflow问题标题自动补全

**来源**: ICPC 2023 | **作者**: Xiang Chen 等

## 摘要
SO上许多问题标题不完整或不够描述性。本文提出QTC4SO，自动补全和改进SO问题标题。通过分析问题正文和代码片段，生成更完整、更具描述性的标题。

## 方法概述
1. 分析问题正文和代码片段提取关键信息
2. 基于序列到序列模型生成补全后的标题
3. 融合代码和文本的双模态信息

## 关键发现
- 自动补全的标题在信息完整性和可读性上优于原始标题
- 代码信息对标题补全有重要贡献

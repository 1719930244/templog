# SVA-ICL: Improving LLM-based Software Vulnerability Assessment via In-Context Learning and Information Fusion
# SVA-ICL：基于上下文学习和信息融合改进LLM软件漏洞评估

**来源**: IST 2025 | **作者**: Xiang Chen 等

## 摘要
软件漏洞评估旨在对已发现的漏洞进行严重性评级。本文提出SVA-ICL，利用LLM的上下文学习（In-Context Learning）能力，结合多源信息融合，提升漏洞评估的准确性。通过精心设计的示例选择策略和信息融合机制，SVA-ICL在无需微调的情况下实现了有竞争力的评估效果。

## 方法概述
1. **示例选择**：基于漏洞相似度选择最相关的上下文示例
2. **信息融合**：融合代码特征、漏洞描述、CWE分类等多源信息
3. **Prompt构建**：将融合信息组织为结构化prompt
4. **LLM推理**：利用LLM的ICL能力进行漏洞严重性评估

## 关键发现
- ICL方法在漏洞评估上接近甚至超过微调方法
- 示例选择策略对ICL效果影响显著
- 多源信息融合比单一信息源效果更好

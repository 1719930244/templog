# DeepSCC: Source Code Classification Based on Fine-Tuned RoBERTa
# DeepSCC：基于微调RoBERTa的源代码分类

**来源**: SEKE 2021 | **作者**: Xiang Chen 等

## 摘要
源代码分类是代码理解的基础任务。本文提出DeepSCC，基于微调RoBERTa预训练模型进行源代码编程语言分类。通过将源代码视为自然语言序列，利用RoBERTa的强大文本理解能力进行分类。

## 方法概述
1. 将源代码tokenize为子词序列
2. 在RoBERTa基础上添加分类头
3. 使用标注的代码-语言对进行微调
4. 支持多种编程语言的分类

## 关键发现
- 预训练模型在代码分类上显著优于传统特征工程方法
- RoBERTa的子词分词策略对代码token有良好的覆盖
- 在多语言分类基准上达到较高准确率

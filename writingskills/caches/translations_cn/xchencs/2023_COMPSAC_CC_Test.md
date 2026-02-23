# Identifying CC Test Cases with Multiple Features Extraction for Better Fault Localization
# 基于多特征提取识别CC测试用例以改进故障定位

**来源**: COMPSAC 2023 | **作者**: Xiang Chen 等

## 摘要
故障定位是调试过程中的关键步骤。CC（Coincidentally Correct）测试用例是指执行了缺陷代码但仍然通过的测试，它们会干扰基于频谱的故障定位方法。本文提出基于多特征提取的CC测试用例识别方法，通过识别并排除CC测试用例来提升故障定位精度。

## 方法概述
1. 提取测试用例的多维特征（覆盖信息、执行路径、输入特征等）
2. 训练分类器识别CC测试用例
3. 在故障定位前排除识别出的CC测试用例
4. 评估排除CC后的故障定位效果提升

## 关键发现
- CC测试用例的存在显著降低了故障定位精度
- 多特征融合比单一特征的CC识别效果更好
- 排除CC测试用例后，SBFL方法的定位精度显著提升

# DevMuT: Testing Deep Learning Framework via Developer Expertise-Based Mutation
# DevMuT：基于开发者经验的变异测试深度学习框架

**来源**: ASE 2024 | **作者**: Xiang Chen 等

## 摘要
深度学习框架的质量保障至关重要。本文提出DevMuT，一种基于开发者经验的DL框架变异测试方法。DevMuT从历史bug修复中学习开发者的修复模式，将其逆向转化为变异算子，用于生成更真实的测试用例。实验在TensorFlow和PyTorch上进行，DevMuT检测到多个之前未知的bug。

## 引言核心
- DL框架bug的检测是软件测试领域的重要挑战
- 现有变异测试方法使用通用变异算子，生成的变异体与真实bug差异大
- 核心insight：开发者修复bug的逆过程可以作为更有效的变异算子

## 方法概述
1. **Bug修复模式挖掘**：从DL框架的commit历史中提取bug修复模式
2. **变异算子生成**：将修复模式逆向转化为变异算子
3. **变异体生成与筛选**：应用变异算子生成变异体，通过等价变异体检测进行筛选
4. **差异测试**：在多个框架版本间进行差异测试

## 关键实验发现
- RQ1：DevMuT在TensorFlow和PyTorch上检测到多个confirmed bugs
- RQ2：基于开发者经验的变异算子比通用算子更有效
- RQ3：DevMuT生成的变异体与真实bug的相似度更高

## 结论
DevMuT通过挖掘开发者经验来指导变异测试，有效提升了DL框架测试的bug检测能力。

# RealisticCodeBench: Towards More Realistic Evaluation of Large Language Models for Code Generation
# RealisticCodeBench：面向更真实的大语言模型代码生成评估

**来源**: ASE 2025 | **作者**: Xiao Yu 等

## 摘要
评估大语言模型的代码生成能力仍是开放问题。现有高级基准测试（如CoderEval、ClassEval）评估LLM在复杂实际编码任务上的表现，但即使最先进的LLM在这些任务上也表现不佳（如GPT-4在ClassEval上仅37.0% pass@1）。研究表明开发者在LLM输出不正确时往往放弃使用。本文提出RealisticCodeBench，通过挖掘GitHub上标注为ChatGPT或Copilot生成的代码样本，收集反映开发者实际使用LLM场景的编码任务。最终构建376个编程问题，跨5种编程语言（Python 361、JavaScript 346、TypeScript 343、Java 307、C++ 323），每个问题配有参考解决方案和测试用例。对12个LLM的评估显示GPT-4.1以60.65%平均pass@1领先，DeepSeek-V3-671B以58.86%紧随其后。

## 引言核心
- 现有基准（HumanEval、MBPP）主要包含算法和基础编程问题，不能完全反映真实编码挑战
- 复杂基准（CoderEval、ClassEval等）上LLM表现不佳，开发者实际上不会用LLM处理过于复杂的任务
- 开发者更倾向于使用LLM处理高性能模型能可靠完成的可管理编码任务
- 通过挖掘GitHub上标注为ChatGPT/Copilot生成的代码，捕捉开发者实际使用LLM的场景
- 部分LLM在HumanEval和RealisticCodeBench之间存在显著性能差异，暗示过度专门化问题

## 方法概述
RealisticCodeBench的构建流程如下：首先通过GitHub REST API搜索高星项目中标注为ChatGPT或Copilot生成的Python、Java、JavaScript、TypeScript和C++代码样本。过滤掉过于简单、重复或难以测试的代码后，对每个样本的需求进行修改（保留原始意图和复杂度），并调整输入输出参数以降低数据泄露风险。使用ChatGPT-4o生成参考解决方案和测试用例，经人工修正确保准确性和覆盖率。随后生成多语言版本并人工验证。

最终邀请13位经验丰富的工程师评估编程问题是否代表真实开发场景，仅保留获得至少10/13工程师认可的问题。基准涵盖9个不同领域（数据结构与算法、文本处理、文件处理、数据可视化、网络编程、前端开发等）。

## 关键实验发现
- RQ1（模型排名）：GPT-4.1以60.65%平均pass@1领先，DeepSeek-V3-671B（58.86%）为可行的开源替代方案
- RQ2（成本效益）：CodeGeeX4-9B（45.75%）与GPT-4o-mini（53.11%）差距适中，可作为个人开发者的经济替代
- RQ3（基准差异）：CodeGeeX4-9B在HumanEval上82.3%但在RealisticCodeBench Python子集上仅54.02%，暴露过度专门化问题
- RQ4（失败分析）：识别了LLM在实际编码任务中的关键不足领域

## 写作特征备注
- 标题结构：工具命名型（"RealisticCodeBench" + "Towards" 目标导向副标题）
- 摘要是否有数字：是（376、361、346、343、307、323、60.65%、58.86%、37.0%等）
- 是否有RQ：是（通过实验设计隐含多个RQ）
- 是否有Motivating Example：否（通过文献综述和基准对比引出动机）
- 贡献点数量：2

## 结论
RealisticCodeBench通过挖掘开发者实际使用LLM的编码场景构建了更贴近现实的评估基准，揭示了现有LLM在HumanEval上的高分可能不代表实际编码能力，为研究者和从业者提供了更有价值的评估参考。

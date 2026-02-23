# DepRadar: Agentic Coordination for Context-Aware Defect Impact Analysis in Deep Learning Libraries
# DepRadar：面向深度学习库的上下文感知缺陷影响分析智能体协调框架

**来源**: ICSE 2026 | **作者**: Yi Gao 等

## 摘要
深度学习（DL）库（如Transformers和Megatron）在现代AI程序中被广泛采用。然而，当这些库引入缺陷时——从静默计算错误到微妙的性能退化——下游用户往往难以评估自己的程序是否受到影响。本文提出DepRadar，一个用于DL库更新中细粒度缺陷和影响分析的智能体协调框架。DepRadar协调四个专门化智能体完成三个步骤：(1) PR Miner和Code Diff Analyzer提取结构化缺陷语义；(2) Orchestrator Agent综合生成统一的缺陷模式和触发条件；(3) Impact Analyzer检查下游程序是否满足触发条件。在157个PR和70个commit上的评估中，DepRadar在缺陷识别上达到90%精确率，在122个客户端程序的影响分析中达到90%召回率和80%精确率。

## 引言核心
- DL库的缺陷往往不会导致程序崩溃，而是静默地降低数值精度或运行效率，难以被下游用户察觉
- PR和commit中的缺陷描述通常非结构化、含噪声，根因和触发条件很少被形式化
- 库内部修复（如CUDA图、通信缓冲区）与用户高层API之间存在深层语义鸿沟
- 判断客户端程序是否满足缺陷触发条件需要理解配置、函数调用等使用上下文
- DepRadar通过多智能体协调、静态分析和领域特定规则，实现从库端到客户端的端到端缺陷影响分析

## 方法概述
DepRadar基于AutoGen构建，包含三个步骤和四个智能体。第一步，缺陷语义提取：Commit/PR Miner Agent从PR标题、正文、issue引用和开发者评论中提取结构化缺陷表示（bug背景、影响范围、触发条件），同时实现两步过滤机制排除非缺陷PR；Code Diff Analyzer Agent分析补丁语义，定位修改的方法并总结修复逻辑。第二步，缺陷模式生成：Orchestrator Agent综合上游智能体的结果，生成包含风险相关方法调用和参数组合的缺陷模式，并生成最小触发代码。第三步，缺陷影响分析：Impact Analyzer Agent对客户端代码进行上下文分析，通过版本感知文件匹配、AST静态分析和条件匹配，判断客户端是否满足触发条件。

框架还引入了渐进式上下文增强机制以应对LLM的长上下文限制，以及基于AST的后处理验证模块以缓解LLM幻觉。

## 关键实验发现
- RQ1（缺陷识别）：DepRadar在PR数据集上达到95%的缺陷分类F1分数，超过70%的提取字段被领域专家评为完全准确
- RQ2（影响分析）：在122个真实客户端程序上达到85%的F1分数，显著优于三个强基线
- RQ3（实际验证）：在Megatron内部commit上成功识别了12个受静默缺陷影响的真实客户端程序，已被开发者确认

## 写作特征备注
- 标题结构：工具命名型（DepRadar: Agentic Coordination for...）
- 摘要是否有数字：是（90%精确率、157个PR、70个commit、122个客户端、80%精确率）
- 是否有RQ：是
- 是否有Motivating Example：是（Transformers库Flash Attention相关的两个PR示例）
- 贡献点数量：3

## 结论
DepRadar通过多智能体协调框架，实现了从DL库缺陷语义提取到下游客户端影响分析的自动化流程，有效帮助开发者识别静默缺陷对其程序的潜在影响。

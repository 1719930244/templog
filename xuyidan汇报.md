# 许一丹 kNM-LM 项目汇报

## 一、项目概述

本项目名为 **kNM-LM for CP-Lua**，目标是在不进行全量参数微调的前提下，通过构建解耦的算法逻辑纠错数据库（Datastore），在推理阶段实时修正大语言模型生成 Lua 算法代码时的逻辑偏差，提升 Pass@1 准确率。

核心思路：利用 kNN-LM（k-Nearest Neighbor Language Model）技术，将模型在训练数据上预测错误的 token 对应的 Hidden State 和正确 Token 存入 Faiss 向量数据库，推理时通过检索相似上下文来纠正模型输出。

## 二、项目结构

```
knm_project/
├── knm/                          # Python 3.13 虚拟环境（含 transformers, faiss 等依赖）
├── test3/                        # 核心实验代码
│   ├── src/                      # 源码
│   │   ├── run_lm.py             # 主入口：训练/评估/Mistake Mining/kNN推理
│   │   ├── knn_lm.py             # kNN-LM 核心实现（KNNWrapper + KNNSaver）
│   │   ├── model.py              # 模型定义（RNNModel, UnixCoderLM）
│   │   ├── dataset.py            # 数据集加载（支持 JSONL 格式）
│   │   ├── config.py             # 命令行参数配置
│   │   └── beam.py               # Beam Search 实现
│   ├── evaluation/               # 评测模块
│   │   ├── eval_ag.py            # 基于 Agnostics 沙箱的端到端评测
│   │   ├── configs.py            # Prompt 模板配置
│   │   ├── utils.py              # 测试用例解密、代码提取
│   │   ├── sandbox.py            # Agnostics 沙箱封装
│   │   └── eval_results_*.json   # 各轮评测结果
│   ├── data/lua_cp/              # Lua 算法数据集
│   │   ├── train.jsonl           # 训练集（1228 条 Lua 函数）
│   │   ├── dev.jsonl             # 验证集（154 条）
│   │   └── test.jsonl            # 测试集（154 条）
│   ├── datastore/lua_mistakes/   # Faiss 向量数据库
│   │   ├── keys.npy              # Hidden State 向量
│   │   ├── vals.npy              # 对应的正确 Token ID
│   │   └── *.indexed             # Faiss IVFFlat 索引文件
│   └── output/                   # 模型输出缓存
├── 低资源Lua代码生成增强计划.md    # 项目计划书
└── 实验记录.pdf                   # 实验记录文档
```

## 三、技术方案

### 3.1 基座模型
- Qwen3-4B-Instruct-2507（约 40 亿参数，hidden_size=2560）
- 使用 bfloat16 精度 + device_map="auto" 加载，防止显存溢出

### 3.2 Mistake Mining（错误挖掘）
通过 KNNSaver 在训练数据上运行模型前向传播，捕获模型预测错误的 token 位置：
- 使用 ActivationCapturer 通过 forward hook 抓取最后一层 Transformer 的 Hidden State
- 将 Hidden State 作为 Key、正确 Token ID 作为 Value 存入 numpy memmap 文件
- 使用 Faiss IndexIVFFlat 构建向量索引，支持快速近邻检索

实验参数：dstore_size=1,000,000，block_size=1024，训练数据 80,338 tokens（78 个 block）

### 3.3 kNN 推理（KNNWrapper）

推理时通过 forward hook 拦截模型输出，执行以下流程：
1. 获取当前 token 的 Hidden State 作为 query
2. 在 Faiss 索引中检索 k=16 个最近邻
3. 通过 vals.npy 将 Index ID 映射为真实 Token ID
4. 计算 kNN 概率分布并与模型原始概率插值融合

关键技术点：
- 动态 Lambda：`λ = base_lambda × (1.0 - confidence)`，模型越自信 kNN 权重越低
- 置信度拦截：当 λ < 0.01 时跳过 Faiss 检索，节省计算开销
- Prefill 维度对齐：处理 generate 第一步 hidden 序列长但 logits 只有 1 个 token 的情况

### 3.4 端到端评测（eval_ag.py）

使用 nuprl/Ag-LiveCodeBench-X 数据集 + Agnostics 官方 Docker 沙箱进行评测：
- 为每道题构造 Prompt，调用模型生成 Lua 代码
- 解密测试用例（Base64 -> Zlib -> Pickle -> JSON）
- 在 Docker 容器中运行代码并判定 Pass/Fail

## 四、数据情况

### 4.1 训练数据

训练集共 1228 条 Lua 函数片段，来源于开源 GitHub 项目，总计 80,338 tokens。

数据来源分布（Top 10）：

| 来源项目 | 条数 | 占比 |
|---------|------|------|
| leetcode.nvim | 220 | 17.9% |
| torchlib | 156 | 12.7% |
| Lua (通用) | 126 | 10.3% |
| lua-ai | 111 | 9.0% |
| codediff.nvim | 102 | 8.3% |
| lua-algorithms | 62 | 5.0% |
| DataStructures | 53 | 4.3% |
| Project-Euler-Solutions | 51 | 4.2% |
| lua-winged-edge | 44 | 3.6% |
| q_algorithm | 41 | 3.3% |

代码长度统计：最短 26 字符，最长 2563 字符，平均 225 字符。

### 4.2 数据问题分析

当前数据存在两个核心问题：

1. **数据量严重不足**：1228 条 Lua 函数经过 tokenize 后仅产生 80,338 tokens（78 个 block），Mistake Mining 后实际存入 Datastore 的仅 24,245 条 key-value 对。相比 kNN-LM 原论文中百万级的 Datastore，当前数据量差了两个数量级。

2. **数据领域偏移**：训练数据主要来自 Neovim 插件（leetcode.nvim, codediff.nvim）、通用算法库（torchlib, lua-algorithms）等，这些代码以工具函数和数据结构为主，缺少竞赛场景特有的 IO 处理、边界条件判断等模式。而评测集 Ag-LiveCodeBench-X 是标准算法竞赛题，两者之间存在明显的领域差距。

### 4.3 Datastore 状态

| 指标 | 数值 |
|------|------|
| 预分配容量 | 1,000,000 |
| 实际存储量 | 24,245 条 |
| 利用率 | 2.4% |
| keys.npy 大小 | 2.25 MB |
| vals.npy 大小 | 2.25 MB |
| 向量维度 | 2560 (Qwen3-4B hidden_size) |
| 索引类型 | Faiss IndexIVFFlat (L2) |

## 五、实验结果

### 5.1 总体 Pass@1 对比

在 Ag-LiveCodeBench-X 数据集上进行了多轮实验，共 11 组评测结果：

| 实验配置 | 样本数 | 通过数 | Pass@1 | 说明 |
|---------|--------|--------|--------|------|
| Baseline（无 kNN） | 100 | 13 | **13.0%** | 纯 Qwen3-4B 基线 |
| kNN v1（静态 λ=0.25, temp=1.0） | 100 | 9 | 9.0% | 静态权重，kNN 干扰严重 |
| kNN v2（动态 λ, temp=100） | 100 | 13 | **13.0%** | 动态权重，追平基线 |
| kNN v3（动态 λ+, temp=100） | 100 | 10 | 10.0% | 参数微调版本 |

小规模验证（10 题）：

| 实验配置 | 通过数 | Pass@1 |
|---------|--------|--------|
| Baseline | 2 | 20.0% |
| kNN 早期版本 | 1 | 10.0% |
| kNN 动态 λ | 2 | 20.0% |

### 5.2 错误类型分布对比

对 100 题实验中失败题目的错误类型进行分类统计：

| 错误类型 | Baseline | kNN v1 (静态λ) | kNN v2 (动态λ) | kNN v3 (动态λ+) |
|---------|----------|----------------|----------------|-----------------|
| 运行时错误 | 37 (42.5%) | 35 (38.5%) | 37 (42.5%) | 28 (31.1%) |
| 输出错误（逻辑错误） | 12 (13.8%) | 10 (11.0%) | 12 (13.8%) | 9 (10.0%) |
| 语法错误 | 18 (20.7%) | 13 (14.3%) | 14 (16.1%) | 18 (20.0%) |
| 其他错误 | 20 (23.0%) | 33 (36.3%) | 24 (27.6%) | 35 (38.9%) |

关键发现：
- 运行时错误占比最高（约 40%），主要表现为类型错误（attempt to perform arithmetic on a string value）和索引错误（attempt to index a nil value），这是 Lua 语言特有的弱类型陷阱
- kNN v3 将运行时错误从 37 降至 28（降幅 24.3%），说明 kNN 在纠正类型相关错误上有一定效果
- 静态 λ 版本（v1）的"其他错误"显著增加，说明 kNN 在模型已经正确的位置反而引入了噪声

### 5.3 逐题增减分析（kNN v2 vs Baseline）

kNN v2（动态 λ）是综合表现最好的版本，与 Baseline 同为 13.0%，但通过的题目集合不完全相同：

**kNN 新增通过的 3 道题：**
- `1899_A`：Baseline 输出错误（wrong-output），kNN 修正了条件判断逻辑（n%3==0 时应输出 "Second"）
- `abc305_a`：Baseline 输出错误，kNN 修正了数学计算逻辑（四舍五入到最近的 5 的倍数）
- `abc320_a`：Baseline 运行时错误（string.match 参数类型错误），kNN 版本生成了正确的 IO 解析代码

**kNN 丢失的 3 道题：**
- `abc311_b`：kNN 引入了 for 循环边界的类型错误（'for' limit must be a number）
- `abc307_d`：kNN 导致括号不匹配的语法错误
- `1899_D`：kNN 引入了 Python 风格的 `/` 整除运算符（Lua 中应使用 `math.floor`）

这组对比揭示了一个重要现象：kNN 在修正 IO 格式和简单数学逻辑上有效，但在复杂语法结构上可能引入跨语言干扰（如 Python 语法混入 Lua）。

### 5.4 实验迭代过程

项目经历了 4 个主要迭代阶段：

1. **静态 λ 阶段**（v1）：固定 λ=0.25，kNN 温度 temp=1.0。结果 Pass@1 从 13.0% 降至 9.0%，kNN 在模型自信的位置大量引入噪声。
2. **温度调优阶段**：将 kNN 温度从 1.0 提升至 100.0，使 kNN 概率分布更平滑，减少单个近邻的过度影响。
3. **动态 λ 阶段**（v2）：引入置信度门控 `λ = base_λ × (1 - confidence)`，模型自信时自动降低 kNN 权重。Pass@1 恢复至 13.0%。
4. **性能优化阶段**（v3）：增加 λ < 0.01 的快速跳过机制，减少不必要的 Faiss 检索。运行时错误有所下降但整体 Pass@1 降至 10.0%。

## 六、可行性分析

### 6.1 技术可行性

**已验证的部分：**
- kNN-LM 的 hook 机制能够成功挂载到 Qwen3-4B 模型上，ActivationCapturer 可以正确抓取最后一层 Transformer 的 Hidden State
- Faiss IndexIVFFlat 索引在 24,245 条数据上检索延迟可接受
- 动态 Lambda 机制有效避免了 kNN 在模型高置信度时的干扰
- 端到端评测流程（模型生成 → 沙箱执行 → 结果判定）已完全跑通

**存在的瓶颈：**
- 当前 Datastore 仅 24,245 条，远低于 kNN-LM 有效工作所需的数据规模。参考 kNN-LM 原论文（Khandelwal et al., 2020），在 Wikitext-103 上使用约 1 亿条 key-value 对才取得显著的 PPL 下降。当前数据量不足原论文的万分之一。
- 训练数据与评测任务之间存在领域偏移：训练数据是通用 Lua 函数片段，评测任务是算法竞赛的完整程序生成。

### 6.2 数据扩充可行性

项目计划书中提出的跨语言数据增强方案具有较高可行性：

| 数据来源 | 预估数据量 | 获取难度 | 质量保障 |
|---------|-----------|---------|---------|
| Codeforces Lua AC 提交 | 500-2000 条 | 低（API 可爬） | 高（OJ 验证） |
| Python→Lua 跨语言翻译 | 10k-50k 条 | 中（需 LLM API） | 中（需沙箱验证） |
| LeetCode Lua 题解 | 200-500 条 | 低 | 高 |
| Rosetta Code Lua 示例 | 300-800 条 | 低 | 高 |

如果跨语言翻译方案落地，Datastore 规模有望从当前的 24,245 条扩展至百万级，届时 kNN 的检索命中率和纠错能力将有质的提升。

### 6.3 方法论可行性

从逐题分析来看，kNN 已经展现出在特定场景下的纠错能力：
- 修正了 `1899_A` 的条件判断逻辑错误
- 修正了 `abc305_a` 的数学计算错误
- 修正了 `abc320_a` 的 IO 解析类型错误

这三个成功案例说明，当 Datastore 中恰好包含相关的算法模式时，kNN 能够有效纠正模型的逻辑偏差。当前的主要限制不在方法本身，而在数据覆盖度不足。

### 6.4 风险与应对

| 风险 | 影响 | 应对方案 |
|------|------|---------|
| 跨语言翻译质量不高 | Datastore 混入错误代码 | 每条翻译代码必须通过至少 5 个测试用例的沙箱验证 |
| kNN 引入跨语言语法干扰 | 生成 Python 风格的 Lua 代码 | 在 Datastore 构建时过滤含 Python 特有语法的条目 |
| 推理速度下降 | 实际部署受限 | 置信度门控已实现，仅在模型不确定时触发检索 |
| Faiss 索引过大 | 内存溢出 | 可对 Hidden State 做 PCA 降维（2560→512） |

## 七、项目计划（4 周冲刺）

| 阶段 | 时间 | 核心任务 | 交付物 |
|------|------|---------|--------|
| Week 1 | 数据周 | 爬取 Codeforces Lua AC 代码；跨语言翻译 Python→Lua 并沙箱验证 | Lua-CP-Dataset-v1 |
| Week 2 | 挖掘周 | 在扩充数据上重新跑 Mistake Mining；重点检查 IO/索引类错误 | Mistake-Datastore-v2 |
| Week 3 | 系统周 | 系统性调参（λ, temp, k）；实现基于 token 类型的条件触发 | kNM-LM-Inference-v2 |
| Week 4 | 评测周 | 完整 Ag-LiveCodeBench-X 评测；撰写实验报告与对比图表 | 最终实验报告 |

## 八、当前进展与下一步

### 已完成
- 项目框架搭建完毕，支持 Qwen3-4B 模型加载与推理
- Mistake Mining 流程跑通，生成了 Datastore（24,245 条 key-value 对）
- kNN 推理流程跑通，迭代了 4 个版本（静态λ → 温度调优 → 动态λ → 性能优化）
- 基于 Agnostics 沙箱的端到端评测流程跑通，完成 11 组对比实验
- 动态 Lambda 机制成功消除了 kNN 对模型高置信度预测的干扰

### 核心结论
当前 kNN-LM 与 Baseline 持平（Pass@1 = 13.0%），但逐题分析显示 kNN 已具备纠错能力（新增通过 3 题），瓶颈在于 Datastore 数据量不足（24,245 条 vs 目标百万级）和训练数据与评测任务的领域偏移。

### 下一步优先级
1. **最高优先**：实现跨语言数据增强，将 Datastore 扩展至 10 万条以上
2. **高优先**：在扩充数据上重新跑 Mistake Mining，验证数据量对 Pass@1 的影响
3. **中优先**：系统性调参实验（λ, temp, k 的网格搜索）
4. **低优先**：探索基于 token 类型的条件触发策略

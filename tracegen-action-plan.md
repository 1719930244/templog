# TraceGen 行动方案 - ASE 2026 投稿准备

**制定日期**: 2026-03-03
**投稿截止**: 假设 2026-04-15 (ASE 通常 4 月截止)
**剩余时间**: ~6 周

---

## 📅 时间线规划

### 第 1 周 (3.3 - 3.9): 🔴 紧急修复 + 数据补全

**目标**: 让论文具备可投稿的基本条件

#### Day 1-2: 修复关键 Bug
- [ ] **修复 main.py 异常处理** (2 小时)
  ```bash
  cd /home/szw/github/tracegen
  # 修改 main.py Line 247-255
  ```

- [ ] **添加图缓存版本检查** (3 小时)
  ```bash
  # 创建 src/core/graph_cache.py
  # 实现版本化缓存逻辑
  ```

- [ ] **实现 num_workers 并发** (4 小时)
  ```bash
  # 修改 src/pipeline/runner.py
  # 在 Stage 3 验证阶段使用 ThreadPoolExecutor
  ```

#### Day 3-5: 运行完整实验
- [ ] **运行 92 个实例** (预计 2.5 小时)
  ```bash
  cd /home/szw/github/tracegen
  python main.py \
    runtime.batch_size=0 \
    runtime.enable_validation=true \
    runtime.enable_solving=true \
    runtime.num_workers=4
  ```

- [ ] **收集实验指标** (2 小时)
  ```bash
  # 创建 scripts/collect_metrics.py
  python scripts/collect_metrics.py \
    --output_dir ../tracegen-outputs/latest \
    --save_to results/full_run_metrics.json
  ```

- [ ] **填充论文数据** (3 小时)
  - 更新 Table 2 (对比实验)
  - 更新 Table 3 (消融实验 - 先填充 Full 数据)
  - 更新 Table 4 (成本分析)

#### Day 6-7: 案例研究
- [ ] **选择 3 个代表性案例** (4 小时)
  ```bash
  python scripts/select_case_studies.py \
    --validation_results ../tracegen-outputs/latest/3_validation/ \
    --output cases/
  ```

- [ ] **编写案例分析** (6 小时)
  - Case 1: Over-Fixing Pattern
  - Case 2: BM25 Retrieval Gap
  - Case 3: Cross-Subsystem Transfer
  - 更新 sections/experiment.tex Line 268-288

---

### 第 2 周 (3.10 - 3.16): 🟡 有效率提升 + 图表制作

**目标**: 提升核心指标，完善论文视觉呈现

#### Day 8-10: 提升有效率
- [ ] **实现方案 A: 扩展排除列表** (4 小时)
  ```python
  # 修改 src/pipeline/runner.py
  EXCLUDED_INTENT_TYPES = {
      "Complex_Logic_Rewrite",
      "Statement_Insertion",
      "Other"
  }
  MIN_CHAIN_LENGTH = 3
  ```

- [ ] **运行对比实验** (2 小时)
  ```bash
  # 基线
  python main.py runtime.batch_size=20 --config baseline

  # 方案 A
  python main.py runtime.batch_size=20 --config improved_filtering
  ```

- [ ] **分析结果并选择最佳方案** (2 小时)
  - 如果提升明显 (>3%)，应用到全量实验
  - 否则保持当前配置

#### Day 11-12: 绘制论文图表
- [ ] **Figure 1: Motivating Example** (4 小时)
  - 使用 draw.io 或 TikZ
  - 展示 Seed Bug → DefectChain → Synthetic Bug
  - 保存为 figures/motivating_example.pdf

- [ ] **Figure 2: Pipeline Overview** (3 小时)
  - 四阶段流程图
  - 保存为 figures/pipeline_overview.pdf

- [ ] **Fix Intent 分布图** (2 小时)
  ```python
  python scripts/plot_intent_distribution.py \
    --data results/full_run_metrics.json \
    --output figures/intent_distribution.pdf
  ```

#### Day 13-14: 配置优化
- [ ] **重构测试选择模式配置** (3 小时)
  ```yaml
  # 创建 configs/validation_modes.yaml
  # 分离 fast_mode, module_suite_mode, full_mode
  ```

- [ ] **使用 Hydra 配置继承** (2 小时)
  ```yaml
  # 创建 configs/llm/qwen3_base.yaml
  # 减少 synthesis_llm 和 analyzer_llm 的重复
  ```

---

### 第 3 周 (3.17 - 3.23): 🟢 消融实验 + 基线对比

**目标**: 完成消融实验，处理基线对比

#### Day 15-17: 消融实验
- [ ] **创建 5 个消融配置** (4 小时)
  ```bash
  mkdir -p configs/ablation
  # 创建 no_graph_matching.yaml
  # 创建 no_intent_taxonomy.yaml
  # 创建 no_chain_alignment.yaml
  # 创建 no_quality_controls.yaml
  # 创建 no_candidate_filtering.yaml
  ```

- [ ] **运行消融实验** (每个 2 小时，共 10 小时)
  ```bash
  bash scripts/run_ablation_study.sh
  ```

- [ ] **生成对比表格** (2 小时)
  ```bash
  python scripts/generate_ablation_table.py \
    --results_dir results/ablation/ \
    --output tables/ablation_table.tex
  ```

#### Day 18-19: 基线对比
- [ ] **联系 SWE-Smith 和 BugPilot 作者** (1 小时)
  - 发送邮件请求 Django 子集数据
  - 或请求代码复现

- [ ] **方案 B: 引用论文数据** (4 小时)
  - 从 SWE-Smith 论文中提取可比数据
  - 在论文中添加说明差异的段落
  - 更新 sections/experiment.tex

- [ ] **方案 C: 实现简化版基线** (如果时间允许，8 小时)
  ```bash
  # 创建 scripts/baselines/swe_smith_baseline.py
  # 实现随机变异逻辑
  ```

#### Day 20-21: 统计分析
- [ ] **添加置信区间** (2 小时)
  ```python
  python scripts/statistical_analysis.py \
    --results results/full_run_metrics.json \
    --output results/statistics.json
  ```

- [ ] **更新论文中的统计数据** (2 小时)
  - 添加 95% CI
  - 如果有基线数据，添加卡方检验

---

### 第 4 周 (3.24 - 3.30): 🔧 性能优化 + 代码清理

**目标**: 提升系统性能，确保代码质量

#### Day 22-24: 性能优化
- [ ] **实现 LazyVectorPool** (4 小时)
  ```python
  # 创建 src/core/lazy_vector_pool.py
  # 使用内存映射替代全量加载
  ```

- [ ] **实现全局缓存管理器** (3 小时)
  ```python
  # 创建 src/core/cache_manager.py
  # 缓存图、向量池、BM25 索引
  ```

- [ ] **测试性能提升** (2 小时)
  ```bash
  # 运行 10 个实例对比
  python main.py runtime.batch_size=10 --profile
  ```

#### Day 25-26: 代码清理
- [ ] **添加错误处理日志** (3 小时)
  ```python
  # 修改 src/modules/extraction/extractor.py
  # 添加 _save_failure_log 方法
  ```

- [ ] **创建配置文档** (3 小时)
  ```bash
  # 创建 configs/CONFIG_GUIDE.md
  # 说明每个参数的作用和取值范围
  ```

- [ ] **运行代码检查** (2 小时)
  ```bash
  # 格式化代码
  black src/ scripts/

  # 类型检查
  mypy src/

  # Lint 检查
  pylint src/
  ```

#### Day 27-28: 文档完善
- [ ] **更新 README.md** (2 小时)
  - 添加最新的实验结果
  - 更新配置说明
  - 添加故障排除指南

- [ ] **创建 EXPERIMENTS.md** (3 小时)
  - 记录所有实验配置
  - 记录实验结果
  - 提供复现步骤

---

### 第 5 周 (3.31 - 4.6): 📝 论文润色 + 最终验证

**目标**: 完善论文写作，准备投稿

#### Day 29-31: 论文润色
- [ ] **完善 Introduction** (4 小时)
  - 强化动机
  - 明确贡献
  - 添加论文结构说明

- [ ] **完善 Method** (4 小时)
  - 补充算法伪代码
  - 添加更多实现细节
  - 确保可复现性

- [ ] **完善 Experiments** (4 小时)
  - 确保所有 TODO 已填充
  - 添加更多分析
  - 强化结论

#### Day 32-33: Related Work
- [ ] **补充相关工作** (6 小时)
  - 数据泄露相关工作
  - Bug 生成相关工作
  - 代码 LLM 评测相关工作
  - 对比 TraceGen 的优势

#### Day 34-35: 论文检查
- [ ] **语法和拼写检查** (2 小时)
  ```bash
  # 使用 Grammarly 或 LanguageTool
  ```

- [ ] **格式检查** (2 小时)
  - 检查引用格式
  - 检查图表编号
  - 检查页数限制

- [ ] **内部审阅** (4 小时)
  - 请导师或同事审阅
  - 收集反馈
  - 修改论文

---

### 第 6 周 (4.7 - 4.13): 🚀 最终准备 + 投稿

**目标**: 最后检查，提交论文

#### Day 36-38: 最终实验
- [ ] **运行最终完整实验** (3 小时)
  ```bash
  # 使用最优配置运行全量实验
  python main.py \
    runtime.batch_size=0 \
    runtime.enable_validation=true \
    runtime.enable_solving=true \
    --config final
  ```

- [ ] **更新论文中的所有数字** (3 小时)
  - 确保所有表格数据一致
  - 确保文本中的数字与表格匹配

- [ ] **生成补充材料** (4 小时)
  - 创建 supplementary.pdf
  - 包含详细的实验配置
  - 包含额外的案例研究

#### Day 39-40: 代码发布准备
- [ ] **清理代码仓库** (3 小时)
  ```bash
  # 移除敏感信息
  # 添加 LICENSE
  # 完善 README
  ```

- [ ] **创建 Docker 镜像** (如果需要，4 小时)
  ```bash
  # 创建 Dockerfile
  # 构建镜像
  # 测试可复现性
  ```

- [ ] **准备代码发布** (2 小时)
  - 创建 GitHub Release
  - 添加 DOI (Zenodo)
  - 在论文中引用

#### Day 41-42: 投稿
- [ ] **最终检查清单** (2 小时)
  - [ ] 所有作者信息正确
  - [ ] 摘要在 150-250 词之间
  - [ ] 所有图表清晰可读
  - [ ] 所有引用格式正确
  - [ ] 页数符合要求 (通常 10-12 页)
  - [ ] 补充材料已准备
  - [ ] 代码仓库已公开

- [ ] **提交论文** (1 小时)
  - 上传 PDF
  - 上传补充材料
  - 填写元数据
  - 确认提交

- [ ] **庆祝！** 🎉

---

## 🎯 关键里程碑

| 日期 | 里程碑 | 验收标准 |
|------|--------|----------|
| 3.9 | 论文数据完整 | 所有 TODO 已填充 |
| 3.16 | 有效率提升 | 有效率 ≥ 22% |
| 3.23 | 消融实验完成 | 5 个变体数据齐全 |
| 3.30 | 性能优化完成 | 运行时间减少 30% |
| 4.6 | 论文初稿完成 | 无 TODO 标记 |
| 4.13 | 论文投稿 | 成功提交 |

---

## ⚠️ 风险管理

### 高风险项及应对

1. **实验运行失败**
   - 风险: Docker 环境问题、API 限流
   - 应对: 提前测试小规模实验，准备备用 API key

2. **有效率提升不明显**
   - 风险: 方案 A 提升 < 3%
   - 应对: 强调当前 18.5% 的质量（高解决率 28.4%）

3. **基线数据无法获取**
   - 风险: 作者不回复邮件
   - 应对: 使用方案 C（引用论文数据 + 说明差异）

4. **时间不足**
   - 风险: 某些任务超时
   - 应对: 优先完成 🔴 和 🟡 任务，🟢 任务可选

---

## 💰 预算估算

### API 调用成本

**当前已知**:
- 81 个实例: $1.55

**预计额外成本**:
- 完整 92 实例: $1.70
- 消融实验 (5 × 20 实例): $1.70
- 有效率提升实验 (20 实例): $0.35
- 重跑和调试: $1.00

**总计**: ~$6.30

### 时间成本

- 总工作时间: ~160 小时
- 按每天 4 小时: 40 天
- 按每天 8 小时: 20 天

---

## 📋 每日检查清单

### 每天开始前
- [ ] 查看 TODO 列表
- [ ] 确认今天的目标
- [ ] 准备所需资源（API key, 数据等）

### 每天结束后
- [ ] 更新 TODO 状态
- [ ] 提交代码到 Git
- [ ] 记录遇到的问题
- [ ] 规划明天的任务

---

## 🔧 快速命令参考

### 运行实验
```bash
# 完整实验
python main.py runtime.batch_size=0 runtime.enable_validation=true

# 小规模测试
python main.py runtime.batch_size=5 runtime.enable_validation=false

# 消融实验
python main.py --config-name ablation/no_graph_matching runtime.batch_size=20
```

### 收集指标
```bash
python scripts/collect_metrics.py \
  --output_dir ../tracegen-outputs/latest \
  --save_to results/metrics.json
```

### 生成表格
```bash
python scripts/generate_tables.py \
  --metrics results/metrics.json \
  --output tables/
```

---

## 📞 紧急联系

如果遇到阻塞问题：
1. 检查 `/home/szw/github/templog/tracegen-comprehensive-analysis.md`
2. 查看错误日志 `data/assets/logs/`
3. 搜索 GitHub Issues
4. 联系导师或同事

---

**文档版本**: v1.0
**最后更新**: 2026-03-03
**负责人**: 汪妍


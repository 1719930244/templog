# TraceGen 紧急 20 天投稿计划

**当前日期**: 2026-03-03
**投稿截止**: 2026-03-23 (假设)
**剩余时间**: 20 天
**状态**: 🔥 紧急模式

---

## ⚠️ 现实评估

### 当前状况
- ✅ 已有 81 个验证通过的实例
- ✅ 基础实验数据已收集
- ❌ 论文有大量 TODO 标记
- ❌ 缺少基线对比数据
- ❌ 消融实验未完成
- ❌ 图表缺失

### 2月份 API 费用
- **总费用**: $14.65 (¥105.44)
- **调用次数**: 2,352 次
- **Token 消耗**: 3000 万 tokens
- **说明**: 这是 2 月份的累计费用，3 月刚开始

### 时间压力
- **每天可用时间**: 假设 6-8 小时
- **总可用时间**: 120-160 小时
- **必须取舍**: 无法完成所有优化，只做核心任务

---

## 🎯 20 天核心任务（极简版）

### Week 1: 数据补全 (Day 1-7)

#### Day 1-2: 🔴 修复 Bug + 运行实验 (16 小时)

**Day 1 (3.3 周一)**
- [ ] **上午 (4h)**: 修复关键 Bug
  ```bash
  # 1. 修复 main.py 异常处理 (1h)
  cd /home/szw/github/tracegen
  # 修改 Line 247-255

  # 2. 测试修复 (1h)
  python main.py runtime.batch_size=5

  # 3. 提交代码 (0.5h)
  git add main.py
  git commit -m "fix: 修复 batch_size 异常处理逻辑"
  ```

- [ ] **下午 (4h)**: 运行完整实验
  ```bash
  # 运行 92 个实例（预计 2.5 小时）
  python main.py \
    runtime.batch_size=0 \
    runtime.enable_validation=true \
    runtime.enable_solving=false \
    runtime.num_workers=4 \
    > run_full_92.log 2>&1 &

  # 监控进度
  tail -f run_full_92.log
  ```

**Day 2 (3.4 周二)**
- [ ] **上午 (4h)**: 收集实验指标
  ```bash
  # 1. 检查实验结果
  cd ../tracegen-outputs/latest

  # 2. 统计指标
  python -c "
  import json
  from pathlib import Path

  # 读取验证结果
  validation_dir = Path('3_validation')
  valid_count = 0
  total_count = 0

  for f in validation_dir.glob('*_validation.json'):
      with open(f) as fp:
          data = json.load(fp)
          total_count += 1
          if data.get('status') == 'VALID':
              valid_count += 1

  print(f'Valid: {valid_count}/{total_count} ({valid_count/total_count*100:.1f}%)')
  "
  ```

- [ ] **下午 (4h)**: 填充论文数据
  - 更新 Table 2 (对比实验 - 先填 TraceGen 数据)
  - 更新 Table 3 (消融实验 - 先填 Full 数据)
  - 更新 Table 4 (成本分析)

---

#### Day 3-4: 🔴 案例研究 + 图表 (16 小时)

**Day 3 (3.5 周三)**
- [ ] **全天 (8h)**: 选择并编写 3 个案例
  ```bash
  # 1. 从 81 个实例中筛选 (2h)
  # - Over-Fixing: patch_lines > 15
  # - BM25 Gap: bm25_hit_rate = 0
  # - Cross-Subsystem: 不同模块

  # 2. 编写案例分析 (6h)
  # 每个案例 2 小时
  ```

**Day 4 (3.6 周四)**
- [ ] **全天 (8h)**: 绘制论文图表
  - Figure 1: Motivating Example (3h)
  - Figure 2: Pipeline Overview (3h)
  - Fix Intent 分布图 (2h)

---

#### Day 5-7: 🟡 有效率提升（可选）(24 小时)

**策略**: 如果当前 18.5% 可接受，跳过此步骤

**Day 5 (3.7 周五)**
- [ ] **上午 (4h)**: 实现扩展排除列表
  ```python
  # src/pipeline/runner.py
  EXCLUDED_INTENT_TYPES = {
      "Complex_Logic_Rewrite",
      "Statement_Insertion",
      "Other"
  }
  MIN_CHAIN_LENGTH = 3
  ```

- [ ] **下午 (4h)**: 运行对比实验
  ```bash
  # 小规模测试 (20 个实例)
  python main.py runtime.batch_size=20 --config improved
  ```

**Day 6-7 (3.8-3.9 周末)**
- **如果提升明显 (>3%)**:
  - [ ] 运行完整实验 (8h)
  - [ ] 更新论文数据 (4h)
- **如果提升不明显**:
  - [ ] 跳过，保持当前配置
  - [ ] 开始准备消融实验

---

### Week 2: 实验补充 (Day 8-14)

#### Day 8-10: 🟡 消融实验 (24 小时)

**简化策略**: 只做 3 个最重要的消融

**Day 8 (3.10 周一)**
- [ ] **全天 (8h)**: 创建消融配置
  ```yaml
  # 只做 3 个消融:
  # 1. no_graph_matching (最重要)
  # 2. no_intent_taxonomy (次重要)
  # 3. no_quality_controls (第三)
  ```

**Day 9-10 (3.11-3.12 周二-周三)**
- [ ] **每个消融 8 小时**
  ```bash
  # 每个消融运行 20 个实例（不是 92 个）
  python main.py --config-name ablation/no_graph_matching \
    runtime.batch_size=20
  ```

---

#### Day 11-12: 🟢 基线对比（简化）(16 小时)

**现实方案**: 引用论文数据 + 说明差异

**Day 11 (3.13 周四)**
- [ ] **全天 (8h)**: 从论文中提取数据
  - 阅读 SWE-Smith 论文
  - 阅读 BugPilot 论文
  - 提取可比数据

**Day 12 (3.14 周五)**
- [ ] **全天 (8h)**: 编写对比说明
  ```latex
  \paragraph{Baseline Comparison.}
  We compare against SWE-Smith and BugPilot.
  Since neither provides Django-specific data, we report
  their published metrics and note differences in setup.
  ```

---

#### Day 13-14: 📝 论文润色 (16 小时)

**Day 13 (3.15 周六)**
- [ ] **全天 (8h)**: 完善核心章节
  - Introduction (2h)
  - Method (3h)
  - Experiments (3h)

**Day 14 (3.16 周日)**
- [ ] **全天 (8h)**: Related Work
  - 数据泄露相关工作 (2h)
  - Bug 生成相关工作 (3h)
  - 对比 TraceGen 优势 (3h)

---

### Week 3: 最终冲刺 (Day 15-20)

#### Day 15-17: 🚀 最终实验 + 代码发布 (24 小时)

**Day 15 (3.17 周一)**
- [ ] **全天 (8h)**: 运行最终实验
  ```bash
  # 使用最优配置
  python main.py runtime.batch_size=0 --config final
  ```

**Day 16 (3.18 周二)**
- [ ] **全天 (8h)**: 更新所有数字
  - 检查所有表格
  - 检查所有文本中的数字
  - 确保一致性

**Day 17 (3.19 周三)**
- [ ] **全天 (8h)**: 代码发布准备
  ```bash
  # 1. 清理代码 (2h)
  # 2. 完善 README (3h)
  # 3. 创建 Release (3h)
  ```

---

#### Day 18-20: ✅ 最终检查 + 投稿 (24 小时)

**Day 18 (3.20 周四)**
- [ ] **全天 (8h)**: 论文检查
  - 语法检查 (Grammarly)
  - 格式检查
  - 引用检查
  - 页数检查

**Day 19 (3.21 周五)**
- [ ] **全天 (8h)**: 内部审阅
  - 请导师审阅
  - 收集反馈
  - 修改论文

**Day 20 (3.22 周六)**
- [ ] **全天 (8h)**: 准备投稿
  - 生成 PDF
  - 准备补充材料
  - 填写元数据
  - **提交！**

---

## 💰 预算估算（20 天）

### API 费用
- **已花费 (2月)**: $14.65
- **预计额外**:
  - 完整实验 (92 实例): $1.70
  - 消融实验 (3 × 20 实例): $1.00
  - 有效率实验 (20 实例): $0.35
  - 重跑和调试: $0.50
- **总预计**: ~$18.20 (¥131)

### 时间成本
- **总工作时间**: 160 小时
- **每天**: 8 小时
- **工作日**: 20 天

---

## ⚠️ 必须取舍的内容

### ❌ 放弃的任务
1. **性能优化**: 内存映射、FAISS、并行化
   - 理由: 不影响论文结果

2. **完整消融实验**: 只做 3 个最重要的
   - 理由: 时间不够

3. **实现基线**: 只引用论文数据
   - 理由: 实现成本太高

4. **统计显著性检验**: 可选
   - 理由: 不是必需的

### ✅ 必须完成的任务
1. **补全论文数据**: 所有 TODO 必须填充
2. **案例研究**: 3 个具体案例
3. **图表**: Figure 1, 2 必须有
4. **消融实验**: 至少 3 个变体
5. **Related Work**: 必须完整

---

## 🎯 每日检查清单

### 每天早上
- [ ] 查看 TODO 列表
- [ ] 确认今天的 3 个核心目标
- [ ] 准备所需资源

### 每天晚上
- [ ] 更新 TODO 状态
- [ ] 提交代码到 Git
- [ ] 记录明天的任务

---

## 🚨 风险应对

### 高风险
1. **实验运行失败**
   - 应对: 提前小规模测试
   - 备用: 使用已有的 81 个实例数据

2. **时间不足**
   - 应对: 严格按优先级执行
   - 备用: 放弃消融实验

3. **数据不理想**
   - 应对: 强调质量而非数量
   - 备用: 调整论文叙述角度

---

## 📞 紧急联系

如果遇到阻塞:
1. 跳过当前任务，继续下一个
2. 记录问题，晚上统一处理
3. 不要在单个问题上卡超过 2 小时

---

## 🎉 成功标准

### 最低标准（必须达到）
- [ ] 论文无 TODO 标记
- [ ] 所有表格有数据
- [ ] 有 3 个案例研究
- [ ] 有 2 个图表
- [ ] 有 Related Work

### 理想标准（尽力而为）
- [ ] 有效率 > 20%
- [ ] 有 3 个消融实验
- [ ] 有基线对比数据
- [ ] 代码已发布

---

**最后提醒**:
- **不要追求完美，追求完成！**
- **20 天后必须投稿，不管结果如何！**
- **每天工作 8 小时，不要熬夜！**

---

**文档版本**: v2.0 (紧急版)
**最后更新**: 2026-03-03
**负责人**: 汪妍
**截止日期**: 2026-03-23


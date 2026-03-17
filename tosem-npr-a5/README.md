# A5: Negative-Filtered 反向实验

> TOSEM-2025-0185 | Reviewer 3 Evaluation #6
> "A similar 'sanity check' would be to show that training on a negative-template-filtered dataset results in worse performance overall."

## 目标

在 SequenceR 上训练 Version-N（仅负向模板匹配的训练数据），证明 precision 显著下降。

## 预期结果

| 模型 | Correct/Plausible | Precision |
|------|------------------|-----------|
| SequenceR_o | 14/19 | 74% |
| SequenceR_vp | 11/12 | 92% |
| SequenceR_vpm | 12/14 | 86% |
| **SequenceR_N** | **?/?** | **?%** (预期 30-50%) |

## 在 217 上执行

### 前置条件

- 账号: `liq@172.29.7.217` / `lq123456`
- SequenceR 代码: `/home/dxx/sequencer/`
- 训练数据: `/home/dxx/sequencer/data/src-train.txt` (需确认)
- 模板过滤结果: `/home/dxx/TowardsHP/filtered_dataset/`

### 操作流程

```bash
# 0. 把 a5_experiment 整个目录传到 217
scp -r a5_experiment/ liq@172.29.7.217:~/a5_experiment/
ssh liq@172.29.7.217
cd ~/a5_experiment

# 1. 探查环境（5分钟，确认路径）
bash scripts/00_check_env.sh
# → 根据输出确认 SEQUENCER_DIR 路径是否正确

# 2. 构造 Version-N 数据集（1-5分钟）
#    方案 text: 文本模式匹配 N1-N5（推荐，不依赖 AST）
python3 scripts/01_create_version_n.py --mode text \
    --sequencer-dir /home/dxx/sequencer
#    → 输出: ./data/version_n/src-train.txt, tgt-train.txt
#    → 预期: ~5,000-6,000 行（约15%原始数据）
#    → 如果数量偏差太大（<3000 或 >8000），检查 SequenceR 数据格式

# 3. 训练 SequenceR_N（4-8小时 V100）
bash scripts/02_train.sh
#    → 模型保存在 ./models/sequencer_N/

# 4. 推理 + Defects4J 验证（3-4小时）
bash scripts/03_infer_and_eval.sh
#    → 需要手动完成 Defects4J 补丁验证部分

# 5. 收集结果
python3 scripts/04_collect_results.py --correct X --plausible Y
#    → 输出: results/a5_summary.json + results/latex_snippet.tex
#    → 把 results/ 传回来更新论文
```

### 常见问题

1. **SequenceR 数据格式不确定**: 先 `head -3 /home/dxx/sequencer/data/src-train.txt` 看格式
   - 如果有 `<START_BUG>` / `<END_BUG>` 标记 → 脚本可直接用
   - 如果是纯 token 序列 → 脚本也可处理（会用整行做匹配）

2. **构造出的数据量不对**:
   - 太多（>10000）: N4 匹配过宽，调高 overlap 阈值
   - 太少（<2000）: 放宽匹配条件，或改用差集法（去掉 v2 匹配的 ID）

3. **OpenNMT 路径问题**: `00_check_env.sh` 会搜索，根据输出修改 `SEQUENCER_DIR`

4. **训练发散**: 如果 loss 不收敛，检查数据量是否足够（至少需要 ~2000 条）

## 论文需填充

TOSEM.tex L1037 的三个占位符:
- `XXX_N_PLAUS` → plausible patches 数
- `XXX_N_CORRECT` → correct patches 数
- `XXX_N_PREC` → precision 百分比

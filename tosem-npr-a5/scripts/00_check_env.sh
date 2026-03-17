#!/bin/bash
# Step 0: 探查服务器环境，确认所有路径和数据
set -e

echo "=========================================="
echo "A5 环境检查"
echo "=========================================="

# 1. SequenceR 代码
echo ""
echo "[1] SequenceR 代码"
for d in /home/dxx/sequencer /home/dxx/TowardsHP/sequencer; do
    if [ -d "$d" ]; then
        echo "  FOUND: $d"
        echo "  内容: $(ls $d | head -10)"
        # 找 OpenNMT
        if [ -d "$d/OpenNMT-py" ]; then
            echo "  OpenNMT: $d/OpenNMT-py/ ✓"
        fi
        # 找训练脚本
        for f in train.sh run_train.sh train_sequencer.sh; do
            [ -f "$d/$f" ] && echo "  训练脚本: $d/$f ✓" && cat "$d/$f" | head -20 && echo "  ..."
        done
    fi
done

# 2. 训练数据
echo ""
echo "[2] SequenceR 训练数据"
for d in /home/dxx/sequencer/data /home/dxx/sequencer/dataset /home/dxx/TowardsHP/sequencer/data; do
    if [ -d "$d" ]; then
        echo "  FOUND: $d"
        ls -lh "$d"/ | head -20
        # 行数
        for f in src-train.txt tgt-train.txt src-val.txt tgt-val.txt; do
            [ -f "$d/$f" ] && echo "  $f: $(wc -l < "$d/$f") 行"
        done
    fi
done

# 3. 模板过滤结果
echo ""
echo "[3] 模板过滤结果"
for d in /home/dxx/TowardsHP/filtered_dataset /home/dxx/TowardsHP/filtered_dataset/filter-dataset-v1 /home/dxx/TowardsHP/filtered_dataset/filter-dataset-v2; do
    if [ -d "$d" ]; then
        echo "  FOUND: $d"
        ls "$d"/ | head -20
    fi
done
# 找 negative 相关文件
echo "  搜索 negative 相关文件:"
find /home/dxx/TowardsHP/ -maxdepth 4 -name "*negative*" -o -name "*neg*" -o -name "*N1*" -o -name "*N2*" 2>/dev/null | head -20

# 4. 已训练好的 SequenceR 模型（用于对比验证流程）
echo ""
echo "[4] 已训练模型"
find /home/dxx/sequencer/ -name "*.pt" -o -name "*.bin" 2>/dev/null | head -10
find /home/dxx/TowardsHP/ -name "*sequencer*" -name "*.pt" 2>/dev/null | head -10

# 5. Defects4J
echo ""
echo "[5] Defects4J"
which defects4j 2>/dev/null && echo "  defects4j: $(which defects4j) ✓" || echo "  defects4j: NOT FOUND"
for d in /home/dxx/defects4j /opt/defects4j /usr/local/defects4j ~/defects4j; do
    [ -d "$d" ] && echo "  D4J目录: $d"
done

# 6. GPU
echo ""
echo "[6] GPU"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "  nvidia-smi 不可用"

# 7. Python
echo ""
echo "[7] Python 环境"
python3 --version 2>/dev/null
python3 -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')" 2>/dev/null || echo "  PyTorch 未安装"
python3 -c "import onmt; print(f'OpenNMT-py {onmt.__version__}')" 2>/dev/null || echo "  OpenNMT 未安装（需要从 SequenceR 目录安装）"

echo ""
echo "=========================================="
echo "检查完毕。请根据上面的输出修改 01_create_version_n.py 中的路径。"
echo "=========================================="

#!/bin/bash
# Step 3: 推理 + Defects4J 验证
set -e

SEQUENCER_DIR="${SEQUENCER_DIR:-/home/dxx/sequencer}"
MODEL_DIR="./models/sequencer_N"
RESULTS_DIR="./results"
LOG_DIR="./logs"
OPENNMT="$SEQUENCER_DIR/OpenNMT-py"

mkdir -p "$RESULTS_DIR" "$LOG_DIR"

# ============================================================
# 1. 找模型和测试数据
# ============================================================
BEST_MODEL=$(ls -t "$MODEL_DIR"/model_step_*.pt 2>/dev/null | head -1)
[ -z "$BEST_MODEL" ] && echo "ERROR: 没找到模型文件" && exit 1
echo "模型: $BEST_MODEL"

# 找测试数据（Defects4J bug）
TEST_SRC=""
for f in "$SEQUENCER_DIR/data/src1klim-test.txt" \
         "$SEQUENCER_DIR/data/src-test.txt" \
         "$SEQUENCER_DIR/dataset/src1klim-test.txt"; do
    if [ -f "$f" ]; then
        TEST_SRC="$f"
        break
    fi
done
[ -z "$TEST_SRC" ] && echo "ERROR: 找不到测试数据" && exit 1
echo "测试数据: $TEST_SRC ($(wc -l < "$TEST_SRC") 行)"

# ============================================================
# 2. 推理
# ============================================================
echo ""
echo "=== Inference (beam=50) ==="

python3 "$OPENNMT/translate.py" \
    -model "$BEST_MODEL" \
    -src "$TEST_SRC" \
    -output "$RESULTS_DIR/raw_output.txt" \
    -beam_size 50 \
    -n_best 50 \
    -max_length 100 \
    -gpu 0 \
    2>&1 | tee "$LOG_DIR/infer.log"

echo "推理输出: $RESULTS_DIR/raw_output.txt"

# ============================================================
# 3. 后处理 (还原为 Java 代码)
# ============================================================
echo ""
echo "=== Post-processing ==="

# 找 SequenceR 的后处理脚本
POST_SCRIPT=""
for f in "$SEQUENCER_DIR/postprocess.py" \
         "$SEQUENCER_DIR/scripts/postprocess.py" \
         "$SEQUENCER_DIR/post_process.py" \
         "$SEQUENCER_DIR/tokenization/detokenize.py"; do
    if [ -f "$f" ]; then
        POST_SCRIPT="$f"
        break
    fi
done

if [ -n "$POST_SCRIPT" ]; then
    echo "后处理脚本: $POST_SCRIPT"
    python3 "$POST_SCRIPT" "$RESULTS_DIR/raw_output.txt" "$RESULTS_DIR/patches/" 2>&1 || {
        echo "[WARN] 后处理脚本执行失败，可能需要不同的参数。"
        echo "请手动运行后处理，然后执行 04_collect_results.py"
    }
else
    echo "[WARN] 没找到后处理脚本。"
    echo "请检查 $SEQUENCER_DIR 中的后处理逻辑。"
    echo ""
    echo "通常 SequenceR 的后处理包括:"
    echo "  1. 将 token 还原为 Java 代码"
    echo "  2. 替换 <seq2seq4repair_space> 等占位符"
    echo "  3. 按 bug 分组输出 50 个候选"
    echo ""
    echo "你也可以直接参考 SequenceR_o 的验证流程:"
    echo "  ls $SEQUENCER_DIR/scripts/"
    echo "  ls $SEQUENCER_DIR/*.sh"
fi

# ============================================================
# 4. Defects4J 验证
# ============================================================
echo ""
echo "=== Defects4J 验证 ==="
echo ""
echo "如果后处理成功，补丁应在 $RESULTS_DIR/patches/ 中。"
echo ""
echo "验证方法 1: 参考 SequenceR_o 的验证脚本"
echo "  通常在 $SEQUENCER_DIR 中有 validate.sh 或 evaluate.sh"
echo ""
echo "验证方法 2: 使用本包的 validatePatch.py"
echo "  python3 scripts/validatePatch.py <patches_dir> <checkout_dir> <buggy_file>"
echo ""
echo "验证方法 3: 直接参考 SequenceR_o 验证的完整流程"
echo "  看之前跑 SequenceR_o 时用的命令/日志"
echo ""
echo "验证完成后运行: python3 scripts/04_collect_results.py"

#!/bin/bash
# Step 2: 训练 SequenceR_N
# 超参数与论文 SequenceR_o 完全一致
set -e

# ============================================================
# 配置（根据 00_check_env.sh 的输出修改）
# ============================================================
SEQUENCER_DIR="${SEQUENCER_DIR:-/home/dxx/sequencer}"
DATA_DIR="${DATA_DIR:-./data/version_n}"
MODEL_DIR="./models/sequencer_N"
LOG_DIR="./logs"
OPENNMT="$SEQUENCER_DIR/OpenNMT-py"

# ============================================================
# 检查
# ============================================================
echo "=== A5: Training SequenceR_N ==="
echo "OpenNMT: $OPENNMT"
echo "Data: $DATA_DIR"

for f in "$DATA_DIR/src-train.txt" "$DATA_DIR/tgt-train.txt"; do
    [ ! -f "$f" ] && echo "ERROR: $f 不存在。先运行 01_create_version_n.py" && exit 1
done

TRAIN_SIZE=$(wc -l < "$DATA_DIR/src-train.txt")
echo "训练集: $TRAIN_SIZE 行"

[ ! -d "$OPENNMT" ] && echo "ERROR: OpenNMT 目录不存在: $OPENNMT" && exit 1

mkdir -p "$MODEL_DIR" "$LOG_DIR"

# ============================================================
# 重要: 先看 SequenceR_o 原始训练参数
# ============================================================
echo ""
echo "=== 检查原始训练参数 ==="
for f in "$SEQUENCER_DIR/train.sh" "$SEQUENCER_DIR/run_train.sh" "$SEQUENCER_DIR/scripts/train.sh"; do
    if [ -f "$f" ]; then
        echo "找到训练脚本: $f"
        echo "--- 内容 ---"
        cat "$f"
        echo "--- END ---"
        echo ""
        echo "!! 请确认下面的超参数与上面一致 !!"
        echo "!! 如果不一致，请修改下面的参数后重新运行 !!"
        echo ""
        break
    fi
done

# ============================================================
# 预处理
# ============================================================
echo "=== Preprocessing ==="
PREP_DIR="$DATA_DIR/preprocessed"
mkdir -p "$PREP_DIR"

# 处理 validation 文件（可能不存在）
VAL_ARGS=""
if [ -f "$DATA_DIR/src-val.txt" ] && [ -f "$DATA_DIR/tgt-val.txt" ]; then
    VAL_ARGS="-valid_src $DATA_DIR/src-val.txt -valid_tgt $DATA_DIR/tgt-val.txt"
fi

python3 "$OPENNMT/preprocess.py" \
    -train_src "$DATA_DIR/src-train.txt" \
    -train_tgt "$DATA_DIR/tgt-train.txt" \
    $VAL_ARGS \
    -src_seq_length 1000 \
    -tgt_seq_length 100 \
    -src_vocab_size 1000 \
    -tgt_vocab_size 1000 \
    -save_data "$PREP_DIR/version_n" \
    2>&1 | tee "$LOG_DIR/preprocess.log"

# ============================================================
# 训练
# ============================================================
echo ""
echo "=== Training ==="

# 自适应 steps
if [ "$TRAIN_SIZE" -lt 1000 ]; then
    STEPS=10000
    echo "[WARN] 数据量少 ($TRAIN_SIZE)，使用 $STEPS steps"
elif [ "$TRAIN_SIZE" -lt 5000 ]; then
    STEPS=20000
else
    STEPS=30000
fi

# 论文参数: 30000 steps, batch 64, lr 0.001, Adam, 2-layer BiRNN 256
python3 "$OPENNMT/train.py" \
    -data "$PREP_DIR/version_n" \
    -save_model "$MODEL_DIR/model" \
    -layers 2 \
    -rnn_size 256 \
    -word_vec_size 256 \
    -encoder_type brnn \
    -decoder_type rnn \
    -train_steps $STEPS \
    -max_grad_norm 5 \
    -batch_size 64 \
    -optim adam \
    -learning_rate 0.001 \
    -dropout 0.3 \
    -gpu_ranks 0 \
    -seed 42 \
    -save_checkpoint_steps 5000 \
    -valid_steps 2500 \
    -log_file "$LOG_DIR/train.log" \
    2>&1 | tee -a "$LOG_DIR/train.log"

echo ""
echo "训练完成。模型: $MODEL_DIR/"
echo "下一步: bash scripts/03_infer_and_eval.sh"

#!/usr/bin/env python3
"""
构造 Version-N 数据集: 从 SequenceR 训练数据中仅保留匹配负向模板的样本。

方案 A (--mode ids): 使用服务器上已有的 AST 过滤结果
方案 B (--mode text): 使用文本模式匹配（近似，不需要 AST）

用法:
    # 方案 A: 服务器上有过滤结果
    python3 01_create_version_n.py --mode ids \
        --filter-dir /home/dxx/TowardsHP/filtered_dataset/filter-dataset-v1/ \
        --sequencer-dir /home/dxx/sequencer/

    # 方案 B: 用文本匹配
    python3 01_create_version_n.py --mode text \
        --sequencer-dir /home/dxx/sequencer/

输出: ./data/version_n/{src,tgt}-{train,val}.txt
"""
import argparse
import os
import re
import sys
import json
import glob
from pathlib import Path


# ============================================================
# 方案 A: 从 AST 过滤结果中提取 negative IDs
# ============================================================

def find_negative_ids_from_filter_dir(filter_dir):
    """
    尝试从 TowardsHP 的过滤结果中找到匹配负向模板的样本 ID。

    可能的文件结构（需要根据实际情况调整）:
    - filter-dataset-v1/negative_matched.json
    - filter-dataset-v1/results/negative/*.csv
    - filter-dataset-v1/统计.xlsx 旁边的数据文件
    """
    filter_dir = Path(filter_dir)
    neg_ids = set()

    print(f"搜索 negative 过滤结果: {filter_dir}")

    # 策略 1: 找 json/csv 文件中的 negative 匹配
    for pattern in ["*negative*", "*neg*", "*N1*", "*N2*", "*N3*", "*N4*", "*N5*"]:
        for f in filter_dir.rglob(pattern):
            print(f"  找到: {f}")
            if f.suffix == '.json':
                try:
                    data = json.load(open(f))
                    if isinstance(data, list):
                        neg_ids.update(data)
                    elif isinstance(data, dict):
                        for v in data.values():
                            if isinstance(v, list):
                                neg_ids.update(v)
                except:
                    pass
            elif f.suffix == '.csv' or f.suffix == '.txt':
                try:
                    with open(f) as fh:
                        for line in fh:
                            line = line.strip()
                            if line.isdigit():
                                neg_ids.add(int(line))
                except:
                    pass

    # 策略 2: 如果有 template_id 列的 CSV，提取 template 为 negative 的行
    for f in filter_dir.rglob("*.csv"):
        try:
            with open(f) as fh:
                header = fh.readline()
                if 'template' in header.lower() or 'negative' in header.lower():
                    print(f"  解析模板CSV: {f}")
                    # TODO: 根据实际格式调整
        except:
            pass

    # 策略 3: 找统计文件旁边的数据
    for f in filter_dir.rglob("统计*"):
        parent = f.parent
        print(f"  统计文件所在目录: {parent}")
        for sub in parent.iterdir():
            print(f"    - {sub.name}")

    return neg_ids


def create_version_n_from_ids(neg_ids, sequencer_dir, output_dir):
    """用样本 ID 过滤训练数据。"""
    sequencer_dir = Path(sequencer_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for split in ["train", "val"]:
        src_file = sequencer_dir / "data" / f"src-{split}.txt"
        tgt_file = sequencer_dir / "data" / f"tgt-{split}.txt"

        if not src_file.exists():
            # 尝试其他路径
            for alt in [sequencer_dir / "dataset", sequencer_dir]:
                if (alt / f"src-{split}.txt").exists():
                    src_file = alt / f"src-{split}.txt"
                    tgt_file = alt / f"tgt-{split}.txt"
                    break

        if not src_file.exists():
            print(f"[WARN] 找不到 {src_file}，跳过 {split}")
            continue

        with open(src_file) as sf, open(tgt_file) as tf:
            src_lines = sf.readlines()
            tgt_lines = tf.readlines()

        out_src = open(output_dir / f"src-{split}.txt", "w")
        out_tgt = open(output_dir / f"tgt-{split}.txt", "w")

        count = 0
        for i in range(len(src_lines)):
            if i in neg_ids:
                out_src.write(src_lines[i])
                out_tgt.write(tgt_lines[i])
                count += 1

        out_src.close()
        out_tgt.close()
        print(f"  {split}: {count}/{len(src_lines)} 样本保留")

    return True


# ============================================================
# 方案 B: 文本模式匹配（不需要 AST）
# ============================================================

def is_negative_by_text(src, tgt):
    """
    用文本模式近似匹配 5 个负向模板。
    注意: SequenceR 格式是 token 化的（空格分隔）。
    """
    src_tokens = src.strip().split()
    tgt_tokens = tgt.strip().split()

    # 找到 bug 区域
    bug_start = -1
    bug_end = -1
    for i, t in enumerate(src_tokens):
        if t == "<START_BUG>":
            bug_start = i
        elif t == "<END_BUG>":
            bug_end = i

    if bug_start >= 0 and bug_end >= 0:
        bug_region = src_tokens[bug_start+1:bug_end]
    else:
        bug_region = src_tokens

    bug_len = len(bug_region)

    # N1: 纯删除 — tgt 为空或几乎为空
    if len(tgt_tokens) <= 1:
        return True, "N1"

    # N2: 删除代码块 — tgt 比 bug 区域短很多
    if bug_len > 10 and len(tgt_tokens) < bug_len * 0.2:
        return True, "N2"

    # N3: 删除 final
    if "final" in " ".join(bug_region) and "final" not in " ".join(tgt_tokens):
        # 确认其余部分基本相同
        bug_no_final = [t for t in bug_region if t != "final"]
        if len(bug_no_final) > 0 and len(tgt_tokens) > 0:
            overlap = len(set(bug_no_final) & set(tgt_tokens))
            if overlap > len(bug_no_final) * 0.7:
                return True, "N3"

    # N4: 删除函数参数 — tgt 中逗号更少
    src_commas = " ".join(bug_region).count(",")
    tgt_commas = " ".join(tgt_tokens).count(",")
    if src_commas > 0 and tgt_commas < src_commas:
        overlap = len(set(bug_region) & set(tgt_tokens))
        if overlap > min(len(bug_region), len(tgt_tokens)) * 0.5:
            return True, "N4"

    # N5: 简化 if 条件 — tgt 中的逻辑运算符更少
    src_logic = " ".join(bug_region).count("&&") + " ".join(bug_region).count("||")
    tgt_logic = " ".join(tgt_tokens).count("&&") + " ".join(tgt_tokens).count("||")
    if "if" in " ".join(bug_region) and src_logic > 0 and tgt_logic < src_logic:
        return True, "N5"

    return False, None


def create_version_n_from_text(sequencer_dir, output_dir):
    """用文本匹配过滤训练数据。"""
    sequencer_dir = Path(sequencer_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for split in ["train", "val"]:
        src_file = sequencer_dir / "data" / f"src-{split}.txt"
        tgt_file = sequencer_dir / "data" / f"tgt-{split}.txt"

        if not src_file.exists():
            for alt in [sequencer_dir / "dataset", sequencer_dir]:
                if (alt / f"src-{split}.txt").exists():
                    src_file = alt / f"src-{split}.txt"
                    tgt_file = alt / f"tgt-{split}.txt"
                    break

        if not src_file.exists():
            print(f"[WARN] 找不到 {src_file}，跳过 {split}")
            continue

        with open(src_file) as sf, open(tgt_file) as tf:
            src_lines = sf.readlines()
            tgt_lines = tf.readlines()

        assert len(src_lines) == len(tgt_lines), \
            f"行数不匹配: src={len(src_lines)}, tgt={len(tgt_lines)}"

        out_src = open(output_dir / f"src-{split}.txt", "w")
        out_tgt = open(output_dir / f"tgt-{split}.txt", "w")

        count = 0
        template_hits = {"N1": 0, "N2": 0, "N3": 0, "N4": 0, "N5": 0}

        for i in range(len(src_lines)):
            matched, template = is_negative_by_text(src_lines[i], tgt_lines[i])
            if matched:
                out_src.write(src_lines[i])
                out_tgt.write(tgt_lines[i])
                count += 1
                template_hits[template] += 1

        out_src.close()
        out_tgt.close()

        rate = count / len(src_lines) * 100
        print(f"  {split}: {count}/{len(src_lines)} ({rate:.1f}%) 匹配负向模板")
        print(f"    模板分布: {template_hits}")

    return True


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ids", "text"], default="text",
                        help="ids=用已有过滤结果, text=文本匹配")
    parser.add_argument("--sequencer-dir", default="/home/dxx/sequencer",
                        help="SequenceR 代码目录")
    parser.add_argument("--filter-dir", default="/home/dxx/TowardsHP/filtered_dataset/filter-dataset-v1/",
                        help="模板过滤结果目录 (仅 --mode ids)")
    parser.add_argument("--output-dir", default="./data/version_n",
                        help="输出目录")
    args = parser.parse_args()

    print("=" * 60)
    print("A5: 构造 Version-N 数据集")
    print(f"模式: {args.mode}")
    print(f"SequenceR: {args.sequencer_dir}")
    print(f"输出: {args.output_dir}")
    print("=" * 60)

    if args.mode == "ids":
        neg_ids = find_negative_ids_from_filter_dir(args.filter_dir)
        if not neg_ids:
            print("\n[WARN] 未找到 negative ID。尝试文本匹配方案...")
            print("如果服务器上确实有过滤结果，请手动检查目录结构并调整代码。")
            print("现在回退到文本匹配...\n")
            create_version_n_from_text(args.sequencer_dir, args.output_dir)
        else:
            print(f"\n找到 {len(neg_ids)} 个 negative 样本 ID")
            create_version_n_from_ids(neg_ids, args.sequencer_dir, args.output_dir)
    else:
        create_version_n_from_text(args.sequencer_dir, args.output_dir)

    # 验证输出
    output_dir = Path(args.output_dir)
    for split in ["train", "val"]:
        f = output_dir / f"src-{split}.txt"
        if f.exists():
            n = sum(1 for _ in open(f))
            print(f"\nVersion-N {split}: {n} 行 -> {f}")

    print("\n下一步: bash scripts/02_train.sh")


if __name__ == "__main__":
    main()

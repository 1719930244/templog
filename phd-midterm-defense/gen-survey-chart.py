#!/usr/bin/env python3.10
"""生成文献调研柱状图：JIT缺陷预测领域论文发表趋势（基于DBLP数据）"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

font_path = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
fp_title = fm.FontProperties(fname=font_path, size=14, weight='bold')
fp_label = fm.FontProperties(fname=font_path, size=12)
fp_legend = fm.FontProperties(fname=font_path, size=11)
fp_small = fm.FontProperties(fname=font_path, size=9)
fp_anno = fm.FontProperties(fname=font_path, size=10)

plt.rcParams['axes.unicode_minus'] = False

out_dir = "/home/szw/github/templog/phd-midterm-defense/figs"

# ============================================================
# DBLP 真实数据（2025-02-25 检索）
# 多关键词去重合并后 149 篇
# ============================================================
years = list(range(2014, 2026))
counts = [1, 1, 2, 3, 7, 10, 10, 21, 22, 22, 28, 22]

# 配色：渐变蓝色，越近年份越深
base_color = np.array([0.267, 0.447, 0.769])  # #4472C4
colors = []
for i, c in enumerate(counts):
    ratio = 0.4 + 0.6 * (i / (len(counts) - 1))
    colors.append(base_color * ratio + np.array([1, 1, 1]) * (1 - ratio))

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
width = 0.65

bars = ax.bar(x, counts, width, color=colors, edgecolor='white', linewidth=0.8,
              zorder=3)

# 网格线
ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)

ax.set_xlabel('年份', fontproperties=fp_label)
ax.set_ylabel('论文数量', fontproperties=fp_label)
ax.set_title('DBLP收录JIT缺陷预测相关论文数量趋势（2014-2025）',
             fontproperties=fp_title, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(years, rotation=45, fontsize=10)
ax.set_ylim(0, max(counts) + 6)

# 柱子上方标注数值
for bar in bars:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, str(int(h)),
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color='#333333')

# 阶段标注
phases = [
    (0, 2, '萌芽期', '#E8F0FE'),
    (3, 5, '起步期', '#D2E3FC'),
    (5, 7, '加速期', '#A8C7FA'),
    (7, 11, '爆发期', '#7BAAF7'),
]
for start, end, label, bg_color in phases:
    mid = (start + end) / 2
    ax.axvspan(start - 0.4, end + 0.4, alpha=0.12, color=bg_color, zorder=0)
    y_pos = max(counts[start:end+1]) + 3.5 if end < len(counts) else max(counts[start:]) + 3.5
    ax.text(mid, y_pos, label, ha='center', va='center',
            fontproperties=fp_anno, color='#555555',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#CCCCCC', alpha=0.9))

# 总数
ax.text(0.98, 0.92, f'总计: {sum(counts)} 篇',
        transform=ax.transAxes, ha='right', va='top',
        fontproperties=fm.FontProperties(fname=font_path, size=12, weight='bold'),
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9C4', edgecolor='#F9A825'))

# 数据来源
ax.text(0.98, 0.02,
        '数据来源: DBLP (dblp.org), 检索日期: 2025-02-25\n'
        '检索词: just-in-time defect prediction/localization 等5组关键词去重',
        transform=ax.transAxes, ha='right', va='bottom',
        fontproperties=fp_small, color='#888888')

# 去掉上边框和右边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f"{out_dir}/survey-chart.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"图表已保存: {out_dir}/survey-chart.png")

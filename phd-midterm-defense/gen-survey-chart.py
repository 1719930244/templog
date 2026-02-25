#!/usr/bin/env python3.10
"""生成文献调研柱状图：JIT缺陷预测领域论文发表趋势（DBLP + OpenAlex 双数据源）"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

font_path = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
font_prop_title = fm.FontProperties(fname=font_path, size=13)
font_prop_label = fm.FontProperties(fname=font_path, size=12)
font_prop_legend = fm.FontProperties(fname=font_path, size=11)
font_prop_small = fm.FontProperties(fname=font_path, size=9)

plt.rcParams['axes.unicode_minus'] = False

out_dir = "/home/szw/github/templog/phd-midterm-defense/figs"

# ============================================================
# 真实数据（2025-02-25 检索）
# DBLP: 去重后 149 篇
# OpenAlex: "just-in-time defect prediction" 458 篇
# ============================================================
years = list(range(2014, 2026))

# DBLP 数据（去重合并多个检索词）
dblp = [1, 1, 2, 3, 7, 10, 10, 21, 22, 22, 28, 22]

# OpenAlex 数据（覆盖更广，含 arXiv 预印本等）
openalex = [1, 6, 2, 10, 22, 32, 49, 61, 100, 76, 66, 27]

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
width = 0.35

bars1 = ax.bar(x - width/2, openalex, width, label='OpenAlex（全部学术文献）',
               color='#4472C4', edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, dblp, width, label='DBLP（计算机科学文献）',
               color='#ED7D31', edgecolor='white', linewidth=0.5)

ax.set_xlabel('年份', fontproperties=font_prop_label)
ax.set_ylabel('论文数量', fontproperties=font_prop_label)
ax.set_title('JIT缺陷预测相关论文发表数量趋势（2014-2025）', fontproperties=font_prop_title)
ax.set_xticks(x)
ax.set_xticklabels(years, rotation=45)
ax.legend(prop=font_prop_legend, loc='upper left')
ax.set_ylim(0, max(openalex) + 15)

for bar in bars1:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.8, str(int(h)),
                ha='center', va='bottom', fontsize=8, color='#4472C4')
for bar in bars2:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.8, str(int(h)),
                ha='center', va='bottom', fontsize=8, color='#ED7D31')

ax.text(0.98, 0.95, f'OpenAlex: {sum(openalex)} 篇\nDBLP: {sum(dblp)} 篇',
        transform=ax.transAxes, ha='right', va='top',
        fontproperties=font_prop_label,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

ax.text(0.98, 0.02, '数据来源: DBLP (dblp.org) & OpenAlex (openalex.org)\n检索日期: 2025-02-25, 2025年数据截至2月',
        transform=ax.transAxes, ha='right', va='bottom',
        fontproperties=font_prop_small, color='gray')

plt.tight_layout()
plt.savefig(f"{out_dir}/survey-chart.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"图表已保存: {out_dir}/survey-chart.png")

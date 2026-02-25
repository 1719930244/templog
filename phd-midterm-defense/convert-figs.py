#!/usr/bin/env python3.10
"""将论文 PDF 图片转换为 PNG"""

import fitz  # PyMuPDF
import os

src_dir = "/home/szw/overleaf/jit-mtl/source/figs"
out_dir = "/home/szw/github/templog/phd-midterm-defense/figs"
os.makedirs(out_dir, exist_ok=True)

# 需要的图片：figs1(示例), figs2(概览), figs3(多任务学习), figs4(不同粒度)
for pdf_name in ["figs1.pdf", "figs2.pdf", "figs3.pdf", "figs4.pdf"]:
    pdf_path = os.path.join(src_dir, pdf_name)
    png_name = pdf_name.replace(".pdf", ".png")
    png_path = os.path.join(out_dir, png_name)

    doc = fitz.open(pdf_path)
    page = doc[0]
    # 高分辨率渲染
    mat = fitz.Matrix(3, 3)  # 3x zoom
    pix = page.get_pixmap(matrix=mat)
    pix.save(png_path)
    doc.close()
    print(f"转换完成: {pdf_name} -> {png_name} ({pix.width}x{pix.height})")

print("所有图片转换完毕！")

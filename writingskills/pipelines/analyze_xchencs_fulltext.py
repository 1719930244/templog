#!/usr/bin/env python3
"""
Download available CCF-A paper PDFs and analyze full-text writing structure.

Reads: outputs/xchencs_ccfa_index.json
Outputs:
  - pipelines/pdfs/*.pdf
  - outputs/xchencs_ccfa_fulltext_analysis.json
  - outputs/xchencs_ccfa_fulltext_analysis.md
"""

import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("Missing dependency: pip install pypdf")

PROXY = "http://30.164.192.185:7890"
CTX = ssl.create_default_context()

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pipelines" / "pdfs"
INDEX_JSON = ROOT / "outputs" / "xchencs_ccfa_index.json"
OUT_JSON = ROOT / "outputs" / "xchencs_ccfa_fulltext_analysis.json"
OUT_MD = ROOT / "outputs" / "xchencs_ccfa_fulltext_analysis.md"

# Extra PDF sources found via Semantic Scholar (not in OpenAlex OA)
EXTRA_PDFS: Dict[str, str] = {
    "Improving Deep Learning Framework Testing with Model-Level Metamorphic Testing":
        "https://arxiv.org/pdf/2507.04354.pdf",
    "An Empirical Study on Challenges for LLM Application Developers":
        "https://arxiv.org/pdf/2408.05002.pdf",
    "Automated Question Title Reformulation by Mining Modification Logs From Stack Overflow":
        "https://ink.library.smu.edu.sg/context/sis_research/article/9228/viewcontent/Automated_question_title_reformulation_by_mining_modifcation_logs_av.pdf",
    "Achieving High MAP-Coverage through Pattern Constraint Reduction":
        "https://ink.library.smu.edu.sg/context/sis_research/article/7943/viewcontent/PatternConstraint_av.pdf",
}


# ── HTTP ─────────────────────────────────────────────────────

def _http_get(url: str, *, timeout: int = 60, use_proxy: bool = False) -> bytes:
    handlers = []
    if use_proxy:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "application/pdf,*/*",
    })
    with opener.open(req, timeout=timeout) as resp:
        return resp.read()

def download_pdf(url: str, dest: Path) -> bool:
    """Download PDF, try direct then proxy. Returns True on success."""
    for use_proxy in [False, True]:
        try:
            data = _http_get(url, use_proxy=use_proxy)
            if data[:5] == b"%PDF-":
                dest.write_bytes(data)
                return True
        except Exception:
            continue
    return False

# ── PDF text extraction ──────────────────────────────────────

def extract_full_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        pages.append(t)
    return "\n".join(pages)


def safe_filename(title: str, year: int, venue: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title)[:60].strip().replace(" ", "_")
    return f"{year}_{venue}_{slug}.pdf"


# ── Structure analysis ───────────────────────────────────────

SECTION_PATTERNS = {
    "abstract": r"\babstract\b",
    "introduction": r"\b(1\.?\s+)?introduction\b",
    "related_work": r"\brelated\s+work\b",
    "background": r"\bbackground\b|\bpreliminaries?\b",
    "approach": r"\b(approach|method(ology)?|technique|framework|proposed)\b",
    "evaluation": r"\b(evaluation|experiment(s|al)?)\b",
    "setup": r"\b(experimental\s+)?setup\b|\bsettings?\b",
    "results": r"\bresults?\b",
    "discussion": r"\bdiscussion\b",
    "threats": r"\bthreats?\s+to\s+validity\b",
    "conclusion": r"\bconclusion(s)?\b",
    "references": r"\breferences\b",
    "rq": r"\bRQ\s*\d",
    "data_availability": r"\bdata\s+availability\b|\breplication\s+package\b|\bartifact\b",
}

RQ_PATTERN = re.compile(r"\bRQ\s*(\d+)\b", re.I)

def analyze_structure(text: str) -> Dict[str, Any]:
    low = text.lower()
    sections_found = {}
    for name, pat in SECTION_PATTERNS.items():
        if re.search(pat, low if name != "rq" else text):
            sections_found[name] = True

    # Count RQs
    rqs = sorted(set(RQ_PATTERN.findall(text)))
    rq_count = len(rqs)

    # Detect specific writing patterns
    signals = {
        "has_rq": rq_count > 0,
        "rq_count": rq_count,
        "rq_ids": rqs,
        "has_threats_to_validity": "threats" in sections_found,
        "has_related_work": "related_work" in sections_found,
        "has_evaluation": "evaluation" in sections_found,
        "has_discussion": "discussion" in sections_found,
        "has_data_availability": "data_availability" in sections_found,
        "sections_found": list(sections_found.keys()),
    }

    # Writing style signals from full text
    signals["has_contributions_list"] = bool(
        re.search(r"(contributions?\s+(are|include)|we\s+make\s+the\s+following\s+contributions)", low))
    signals["has_finding_pattern"] = bool(
        re.search(r"\bfinding\s*\d|\bfinding\s*[:.]", low))
    signals["finding_count"] = len(re.findall(r"\bfinding\s*\d", low))
    signals["has_implication"] = bool(re.search(r"\bimplication", low))
    signals["has_takeaway"] = bool(re.search(r"\btakeaway|take-away|key\s+insight", low))
    signals["has_answer_to_rq"] = bool(
        re.search(r"(answer\s+to\s+rq|summary\s+(of|for)\s+rq)", low))
    signals["has_statistical_test"] = bool(
        re.search(r"(wilcoxon|mann.whitney|cliff.s\s+delta|p.value|cohen.s\s+d|effect\s+size|statistical(ly)?\s+significant)", low))
    signals["has_replication_package"] = bool(
        re.search(r"(replication\s+package|github\.com|zenodo|figshare|available\s+at|open.source)", low))
    signals["mentions_baseline_count"] = len(
        set(re.findall(r"\bbaseline[s]?\b", low)))
    signals["has_ablation"] = bool(re.search(r"\bablation\b", low))
    signals["has_case_study"] = bool(re.search(r"\bcase\s+stud", low))
    signals["has_user_study"] = bool(re.search(r"\buser\s+stud|\bhuman\s+(evaluation|study|judge)", low))

    # Estimate page count (rough: ~3000 chars per page for two-column)
    signals["approx_pages"] = max(1, len(text) // 3000)
    signals["total_chars"] = len(text)

    return signals

# ── Output ───────────────────────────────────────────────────

def write_analysis_md(results: List[Dict[str, Any]]) -> None:
    analyzed = [r for r in results if r.get("analysis")]
    if not analyzed:
        return

    n = len(analyzed)
    # Aggregate signals
    agg = Counter()
    total_rqs = []
    for r in analyzed:
        a = r["analysis"]
        for key in ["has_rq", "has_threats_to_validity", "has_related_work",
                     "has_evaluation", "has_discussion", "has_contributions_list",
                     "has_finding_pattern", "has_implication", "has_statistical_test",
                     "has_replication_package", "has_ablation", "has_case_study",
                     "has_user_study", "has_data_availability", "has_answer_to_rq",
                     "has_takeaway"]:
            if a.get(key):
                agg[key] += 1
        total_rqs.append(a.get("rq_count", 0))

    def pct(v: int) -> str:
        return f"{v}/{n} ({100*v/n:.0f}%)"

    lines = [
        "# 陈翔老师 CCF-A 论文正文写作结构分析",
        "",
        f"- 成功下载并分析 PDF: `{n}` 篇",
        f"- 分析来源: OA 论文 + arXiv 预印本",
        "",
        "## 正文结构信号汇总",
        "",
        "| 信号 | 命中 | 说明 |",
        "|------|------|------|",
        f"| RQ 驱动评测 | {pct(agg['has_rq'])} | 使用 RQ1/RQ2/... 组织实验 |",
        f"| Threats to Validity | {pct(agg['has_threats_to_validity'])} | 包含有效性威胁讨论 |",
        f"| 贡献点列表 | {pct(agg['has_contributions_list'])} | 明确列出 contributions |",
        f"| 统计检验 | {pct(agg['has_statistical_test'])} | Wilcoxon/Cliff's delta/p-value 等 |",
        f"| 消融实验 | {pct(agg['has_ablation'])} | Ablation study |",
        f"| Findings 模式 | {pct(agg['has_finding_pattern'])} | Finding 1/2/3... 结构 |",
        f"| Implications | {pct(agg['has_implication'])} | 对实践者/研究者的启示 |",
        f"| 复现包/开源 | {pct(agg['has_replication_package'])} | GitHub/Zenodo/开源声明 |",
        f"| Case Study | {pct(agg['has_case_study'])} | 案例分析 |",
        f"| Discussion 节 | {pct(agg['has_discussion'])} | 独立的讨论章节 |",
        f"| Data Availability | {pct(agg['has_data_availability'])} | 数据可用性声明 |",
        f"| Answer to RQ | {pct(agg['has_answer_to_rq'])} | 显式回答 RQ |",
        "",
        f"RQ 数量分布: 平均 {sum(total_rqs)/n:.1f} 个, "
        f"范围 {min(total_rqs)}–{max(total_rqs)}",
        "",
        "## 各论文详细分析",
        "",
    ]
    for r in analyzed:
        a = r["analysis"]
        lines.append(f"### [{r['year']}] {r['venue']} — {r['title'][:70]}")
        lines.append(f"- 章节: {', '.join(a.get('sections_found', []))}")
        lines.append(f"- RQ 数量: {a.get('rq_count', 0)} ({', '.join('RQ'+x for x in a.get('rq_ids', []))})")
        flags = []
        for k in ["has_threats_to_validity", "has_statistical_test", "has_ablation",
                   "has_finding_pattern", "has_implication", "has_replication_package",
                   "has_case_study", "has_contributions_list"]:
            if a.get(k):
                flags.append(k.replace("has_", "").replace("_", " "))
        lines.append(f"- 特征: {', '.join(flags) if flags else '无特殊标记'}")
        lines.append(f"- 估计页数: ~{a.get('approx_pages', '?')} 页")
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────

def main() -> int:
    if not INDEX_JSON.exists():
        sys.exit(f"Index not found: {INDEX_JSON}\nRun collect_xchencs_ccfa.py first.")

    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    papers = data["papers"]
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    # Collect PDF URLs: OA URLs + source PDF links
    results = []
    for p in papers:
        pdf_url = None
        source = None

        # Priority 1: source_links with .pdf or arxiv
        for link in p.get("source_links", []):
            if ".pdf" in link.lower() or "arxiv.org/pdf" in link.lower():
                pdf_url = link
                source = "homepage"
                break

        # Priority 2: extra PDFs from Semantic Scholar (fuzzy match)
        if not pdf_url:
            t_norm = re.sub(r"[^a-z0-9]+", " ", p["title"].lower()).strip()
            for et, eu in EXTRA_PDFS.items():
                en = re.sub(r"[^a-z0-9]+", " ", et.lower()).strip()
                if SequenceMatcher(None, t_norm, en).ratio() > 0.85:
                    pdf_url = eu
                    source = "semantic_scholar"
                    break

        # Priority 3: OA URL (only arxiv ones, ACM/IEEE OA URLs are 403)
        if not pdf_url and p.get("oa_url"):
            oa = p["oa_url"]
            if "arxiv.org" in oa:
                pdf_url = oa
                source = "openalex_oa"

        results.append({
            "title": p["title"],
            "year": p["year"],
            "venue": p["venue"],
            "pdf_url": pdf_url,
            "pdf_source": source,
            "pdf_downloaded": False,
            "pdf_path": None,
            "analysis": None,
        })

    # Download and analyze
    downloadable = [(i, r) for i, r in enumerate(results) if r["pdf_url"]]
    print(f"[info] {len(downloadable)} papers have potential PDF URLs")

    for idx, (i, r) in enumerate(downloadable, 1):
        fname = safe_filename(r["title"], r["year"], r["venue"])
        dest = PDF_DIR / fname
        print(f"  [{idx}/{len(downloadable)}] {r['year']} {r['venue']}: {r['title'][:50]}...")

        if dest.exists() and dest.stat().st_size > 1000:
            print(f"    [cache] already downloaded")
            r["pdf_downloaded"] = True
            r["pdf_path"] = str(dest)
        else:
            time.sleep(0.5)
            ok = download_pdf(r["pdf_url"], dest)
            if ok:
                print(f"    ✓ downloaded ({dest.stat().st_size // 1024} KB)")
                r["pdf_downloaded"] = True
                r["pdf_path"] = str(dest)
            else:
                print(f"    ✗ download failed")
                continue

        # Extract and analyze
        try:
            text = extract_full_text(dest)
            if len(text) < 500:
                print(f"    ⚠ extracted text too short ({len(text)} chars)")
                continue
            r["analysis"] = analyze_structure(text)
            rqc = r["analysis"]["rq_count"]
            ttv = "✓" if r["analysis"]["has_threats_to_validity"] else "✗"
            stat = "✓" if r["analysis"]["has_statistical_test"] else "✗"
            print(f"    analyzed: RQs={rqc} threats={ttv} stats={stat}")
        except Exception as e:
            print(f"    ⚠ analysis error: {e}")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    write_analysis_md(results)

    analyzed = sum(1 for r in results if r.get("analysis"))
    print(f"\n[done] {analyzed} papers analyzed")
    print(f"  → {OUT_JSON}")
    print(f"  → {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

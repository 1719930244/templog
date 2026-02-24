#!/usr/bin/env python3
"""
Collect CCF-A papers by Xiang Chen from xchencs.github.io,
then enrich metadata via OpenAlex API.

Outputs:
  - outputs/xchencs_ccfa_index.json
  - outputs/xchencs_ccfa_summary.md
"""

import html as html_lib
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PUB_URL = "https://xchencs.github.io/publications.html"
OPENALEX_SEARCH = "https://api.openalex.org/works"
PROXY = "http://30.164.192.185:7890"

ROOT = Path(__file__).resolve().parent.parent
CACHE_HTML = ROOT / "caches" / "xchencs_publications.html"
OUT_JSON = ROOT / "outputs" / "xchencs_ccfa_index.json"
OUT_MD = ROOT / "outputs" / "xchencs_ccfa_summary.md"

CTX = ssl.create_default_context()


# ── HTTP helpers ──────────────────────────────────────────────

def _http_get(url: str, *, timeout: int = 30, use_proxy: bool = False) -> bytes:
    handlers = []
    if use_proxy:
        handlers.append(urllib.request.ProxyHandler({
            "http": PROXY, "https": PROXY,
        }))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; PaperCollector/1.0)",
        "Accept": "*/*",
    })
    with opener.open(req, timeout=timeout) as resp:
        return resp.read()


def http_get_with_fallback(url: str, **kw) -> bytes:
    """Try direct first, fall back to proxy on failure."""
    try:
        return _http_get(url, use_proxy=False, **kw)
    except Exception:
        return _http_get(url, use_proxy=True, **kw)

# ── HTML parsing ─────────────────────────────────────────────

def _strip_tags(s: str) -> str:
    return html_lib.unescape(re.sub(r"(?is)<.*?>", "", s)).strip()


def _looks_like_title(s: str) -> bool:
    s = s.strip().replace("*", "")
    if re.fullmatch(r"[A-Z][a-z]+(\s+[A-Z][a-z]+){1,2}", s):
        return False  # looks like a person name
    words = s.split()
    return len(words) >= 3 or len(s) >= 20


def fetch_html() -> str:
    if CACHE_HTML.exists():
        print(f"[cache] using {CACHE_HTML}")
        return CACHE_HTML.read_text(encoding="utf-8", errors="replace")
    print(f"[fetch] {PUB_URL}")
    data = http_get_with_fallback(PUB_URL)
    CACHE_HTML.parent.mkdir(parents=True, exist_ok=True)
    CACHE_HTML.write_bytes(data)
    return data.decode("utf-8", errors="replace")


def _short_venue(venue_full: str) -> str:
    """Extract short venue name like TSE, TOSEM, ICSE, ASE, etc."""
    mapping = {
        "IEEE Transactions on Software Engineering": "TSE",
        "ACM Transactions on Software Engineering and Methodology": "TOSEM",
        "International Conference on Software Engineering": "ICSE",
        "Automated Software Engineering": "ASE",
        "Foundations of Software Engineering": "FSE",
        "ESEC/FSE": "FSE",
        "Software Testing and Analysis": "ISSTA",
    }
    for key, short in mapping.items():
        if key.lower() in venue_full.lower():
            return short
    # fallback: try to find acronym in parentheses
    m = re.search(r"\((\w{2,10})\s*\d{4}\)", venue_full)
    return m.group(1) if m else venue_full[:30]


def parse_ccfa_papers(html: str) -> List[Dict[str, Any]]:
    blocks = re.findall(r"(?is)<li\b[^>]*>.*?</li>", html)
    papers = []
    for blk in blocks:
        if "CCF A" not in blk:
            continue
        # title
        strongs = re.findall(r"(?is)<strong>\s*(.*?)\s*</strong>", blk)
        title = ""
        for s in strongs:
            clean = _strip_tags(s)
            if _looks_like_title(clean):
                title = clean
                break
        if not title:
            bm = re.search(r"(?is)<b>\s*(.*?)\s*</b>", blk)
            if bm:
                title = _strip_tags(bm.group(1))
        if not title:
            continue
        # year
        ym = re.search(r"(20\d{2})", blk)
        year = int(ym.group(1)) if ym else None
        if not year:
            continue
        # venue
        vm = re.search(r"(?is)<em>\s*(.*?)\s*</em>", blk)
        venue_full = _strip_tags(vm.group(1)) if vm else ""
        venue_short = _short_venue(venue_full)
        # links
        hrefs = [urllib.parse.urljoin(PUB_URL, h)
                 for h in re.findall(r'href="([^"]+)"', blk)]
        papers.append({
            "title": title,
            "year": year,
            "venue": venue_short,
            "venue_full": venue_full,
            "ccf": "A",
            "source_links": hrefs,
        })
    # deduplicate by title similarity
    seen: List[str] = []
    unique = []
    for p in papers:
        norm = re.sub(r"[^a-z0-9]+", " ", p["title"].lower()).strip()
        if any(SequenceMatcher(None, norm, s).ratio() > 0.9 for s in seen):
            continue
        seen.append(norm)
        unique.append(p)
    unique.sort(key=lambda x: (-x["year"], x["venue"], x["title"]))
    return unique

# ── OpenAlex enrichment ──────────────────────────────────────

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _reconstruct_abstract(inv_index: Optional[Dict]) -> Optional[str]:
    if not inv_index:
        return None
    try:
        size = max(i for idxs in inv_index.values() for i in idxs) + 1
        words = [""] * size
        for token, idxs in inv_index.items():
            for i in idxs:
                if 0 <= i < size:
                    words[i] = token
        return " ".join(w for w in words if w).strip() or None
    except Exception:
        return None


def enrich_with_openalex(paper: Dict[str, Any]) -> Dict[str, Any]:
    """Search OpenAlex by title, pick best match, merge metadata."""
    title = paper["title"]
    url = f"{OPENALEX_SEARCH}?search={urllib.parse.quote(title)}&per_page=5"
    try:
        data = json.loads(http_get_with_fallback(url, timeout=20))
    except Exception as e:
        paper["openalex_error"] = str(e)
        return paper

    best, best_score = None, -1.0
    for w in data.get("results", []):
        cand = w.get("display_name", "")
        score = SequenceMatcher(None, _norm(title), _norm(cand)).ratio()
        pub_year = w.get("publication_year")
        if pub_year and abs(int(pub_year) - paper["year"]) <= 1:
            score += 0.03
        if score > best_score:
            best_score, best = score, w

    if not best or best_score < 0.75:
        paper["openalex_error"] = f"no_match (best_score={best_score:.2f})"
        return paper

    paper["doi"] = best.get("doi")
    paper["cited_by_count"] = best.get("cited_by_count", 0)
    paper["abstract"] = _reconstruct_abstract(best.get("abstract_inverted_index"))
    oa = best.get("open_access", {})
    paper["is_oa"] = oa.get("is_oa", False)
    paper["oa_url"] = oa.get("oa_url")
    paper["openalex_id"] = best.get("id")
    paper["openalex_score"] = round(best_score, 3)
    return paper

# ── Output generation ────────────────────────────────────────

def write_summary_md(papers: List[Dict[str, Any]]) -> None:
    lines = [
        "# 陈翔老师 CCF-A 论文列表",
        "",
        f"- 生成时间: `{datetime.now(timezone.utc).isoformat()}`",
        f"- 数据来源: `{PUB_URL}`",
        f"- CCF-A 论文总数: `{len(papers)}`",
        f"- 有摘要: `{sum(1 for p in papers if p.get('abstract'))}`",
        f"- 有 DOI: `{sum(1 for p in papers if p.get('doi'))}`",
        "",
        "## 论文列表",
        "",
        "| # | Year | Venue | Title | Cited | DOI |",
        "|---|------|-------|-------|------:|-----|",
    ]
    for i, p in enumerate(papers, 1):
        doi_link = f"[link]({p['doi']})" if p.get("doi") else "-"
        cited = p.get("cited_by_count", "-")
        title_short = p["title"][:70] + ("..." if len(p["title"]) > 70 else "")
        lines.append(f"| {i} | {p['year']} | {p['venue']} | {title_short} | {cited} | {doi_link} |")

    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    for i, p in enumerate(papers, 1):
        abstract = p.get("abstract", "（未获取到摘要）")
        lines.append(f"### {i}. [{p['year']}] {p['title']}")
        lines.append(f"**{p['venue']}** | Cited: {p.get('cited_by_count', '?')}")
        lines.append("")
        lines.append(abstract or "（未获取到摘要）")
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────

def main() -> int:
    html = fetch_html()
    papers = parse_ccfa_papers(html)
    print(f"[parse] found {len(papers)} CCF-A papers")

    for i, p in enumerate(papers, 1):
        if i > 1:
            time.sleep(0.3)
        print(f"  [{i}/{len(papers)}] {p['year']} {p['venue']}: {p['title'][:60]}...")
        enrich_with_openalex(p)
        err = p.get("openalex_error")
        if err:
            print(f"    ⚠ {err}")
        else:
            cited = p.get("cited_by_count", "?")
            has_abs = "✓" if p.get("abstract") else "✗"
            print(f"    cited={cited} abstract={has_abs}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_url": PUB_URL,
        "total_ccfa_papers": len(papers),
        "papers": papers,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(papers)

    enriched = sum(1 for p in papers if not p.get("openalex_error"))
    print(f"\n[done] {len(papers)} papers, {enriched} enriched with OpenAlex")
    print(f"  → {OUT_JSON}")
    print(f"  → {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

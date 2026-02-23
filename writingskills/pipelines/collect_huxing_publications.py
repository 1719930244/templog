#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collect (publicly accessible) PDFs for Xing Hu's CCF-A software-engineering papers,
then extract lightweight writing-style signals.

Inputs:
  - Optionally uses ../caches/huxing_publications.html (cached). If missing, downloads it.

Outputs (under ../outputs and ../caches):
  - outputs/huxing_ccfa_index.json: paper list, metadata, PDF status, extracted signals
  - outputs/huxing_ccfa_summary.md: aggregated signals + missing PDF list
  - caches/pdfs_huxing/*.pdf: downloaded PDFs (best-effort, only if publicly accessible)
  - caches/extracted_huxing/*.txt: extracted first-page text

Notes:
  - Only collects CCF-A papers (ICSE/FSE/ASE/ISSTA/TSE/TOSEM).
  - This script does NOT bypass paywalls or anti-bot protections.
"""

from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

try:
    from pypdf import PdfReader  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency pypdf: {exc}")


PUB_URL = "https://xing-hu.github.io/publications/"
BASE_URL = "https://xing-hu.github.io/"
OPENALEX_WORKS_SEARCH = "https://api.openalex.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"

# CCF-A venue keywords for filtering
CCF_A_VENUES = [
    "ICSE", "FSE", "ESEC/FSE", "ESEC", "ASE", "ISSTA",
    "TSE", "IEEE Transactions on Software Engineering",
    "TOSEM", "ACM Transactions on Software Engineering and Methodology",
]

ROOT = Path(__file__).resolve().parent
WS_ROOT = ROOT.parent
CACHE_DIR = WS_ROOT / "caches"
OUT_DIR = WS_ROOT / "outputs"
PDF_DIR = CACHE_DIR / "pdfs_huxing"
EXTRACT_DIR = CACHE_DIR / "extracted_huxing"
INDEX_JSON = OUT_DIR / "huxing_ccfa_index.json"
SUMMARY_MD = OUT_DIR / "huxing_ccfa_summary.md"
PUBLICATIONS_HTML_CACHE = (CACHE_DIR / "huxing_publications.html").resolve()

CTX = ssl.create_default_context()


# ---------------------------------------------------------------------------
# HTTP helpers (reused from xchencs pipeline)
# ---------------------------------------------------------------------------

def _http_get(
    url: str,
    *,
    timeout_s: int = 45,
    headers: dict[str, str] | None = None,
    attempts: int = 3,
) -> bytes:
    last_exc: Exception | None = None
    for attempt in range(1, max(1, attempts) + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; CodexCLI/1.0)",
                    "Accept": "*/*",
                    **(headers or {}),
                },
            )
            with urllib.request.urlopen(req, context=CTX, timeout=timeout_s) as resp:
                return resp.read()
        except Exception as exc:
            last_exc = exc
            if attempt >= attempts:
                break
            time.sleep(0.8 * attempt)
    raise last_exc or RuntimeError("http_get_failed")


def fetch_publications_html() -> str:
    if PUBLICATIONS_HTML_CACHE.exists():
        return PUBLICATIONS_HTML_CACHE.read_text(encoding="utf-8", errors="replace")
    data = _http_get(PUB_URL)
    PUBLICATIONS_HTML_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PUBLICATIONS_HTML_CACHE.write_bytes(data)
    return data.decode("utf-8", errors="replace")


def _strip_tags(s: str) -> str:
    return html_lib.unescape(re.sub(r"(?is)<.*?>", "", s)).strip()


# ---------------------------------------------------------------------------
# HTML parsing for xing-hu.github.io/publications/
# ---------------------------------------------------------------------------

@dataclass
class PubItem:
    label: str       # e.g. "C61", "J27"
    title: str
    year: int
    venue: str
    authors: str
    ccf_a: bool
    pdf_links: list[str] = field(default_factory=list)
    is_award: bool = False


def is_ccf_a_venue(venue: str) -> bool:
    """Check if venue string matches a CCF-A venue."""
    v = venue.lower()
    checks = [
        "icse" in v or "international conference on software engineering" in v,
        "foundations of software engineering" in v or "fse" in v or "esec" in v,
        ("automated software engineering" in v or " ase " in v or v.endswith("ase") or "(ase" in v),
        "issta" in v or "software testing and analysis" in v,
        "ieee transactions on software engineering" in v or ("(tse)" in v),
        "transactions on software engineering and methodology" in v or "(tosem)" in v,
    ]
    return any(checks)


def parse_publications(html: str) -> list[PubItem]:
    """Parse Xing Hu's publications page HTML.

    The page structure is:
      <div class="intro"><p class="section-title">2025</p></div>
      <div class="item">...</div>
      <div class="item">...</div>
      <div class="intro"><p class="section-title">2024</p></div>
      ...
    We need to track the current year section to assign years to J-papers
    whose venue strings don't contain a year.
    """
    items: list[PubItem] = []

    # Build a list of (position, type, content) tuples for year headers and items
    year_pattern = re.compile(r'(?is)<p\s+class="section-title">\s*(\d{4})\s*</p>')
    item_pattern = re.compile(r'(?is)<div\s+class="item">\s*(.*?)\s*</div>')

    # Find all year headers with their positions
    year_positions = [(m.start(), int(m.group(1))) for m in year_pattern.finditer(html)]
    # Find all item blocks with their positions
    item_positions = [(m.start(), m.group(1)) for m in item_pattern.finditer(html)]

    def get_year_for_position(pos: int) -> int:
        """Find the most recent year header before this position."""
        current = 0
        for ypos, year in year_positions:
            if ypos < pos:
                current = year
            else:
                break
        return current

    for pos, block in item_positions:
        section_year = get_year_for_position(pos)

        # Extract label like [C61], [J27]
        label_m = re.search(r'\[([CJ]\d+)\]', block)
        label = label_m.group(1) if label_m else ""

        # Extract the main text content
        tagline_m = re.search(r'(?is)<span\s+class="project-tagline">(.*?)</span>', block)
        if not tagline_m:
            continue
        tagline = tagline_m.group(1)

        # Extract title (in quotes)
        title_m = re.search(r'"([^"]+)"', tagline)
        if not title_m:
            title_m = re.search(r'\u201c([^\u201d]+)\u201d', tagline)  # smart quotes
        title = title_m.group(1).strip() if title_m else ""
        if not title:
            continue

        # Extract venue (in <em> tags)
        venue_m = re.search(r'(?is)<em>(.*?)</em>', tagline)
        venue = _strip_tags(venue_m.group(1)).strip() if venue_m else ""

        # Extract year from venue or use section year as fallback
        year = 0
        year_m = re.search(r'\b(20\d{2})\b', venue)
        if year_m:
            year = int(year_m.group(1))
        elif section_year > 0:
            year = section_year

        # Extract authors (text before the title quote)
        authors_text = tagline.split('"')[0] if '"' in tagline else ""
        authors = _strip_tags(authors_text).strip().rstrip('.')

        # Check for award
        is_award = "Distinguished Paper Award" in block

        # Extract PDF links
        pdf_links = []
        pdf_hrefs = re.findall(r'(?is)href="([^"]*\.pdf[^"]*)"', block)
        for href in pdf_hrefs:
            pdf_links.append(urllib.parse.urljoin(BASE_URL, href))

        # Check if CCF-A
        ccf_a = is_ccf_a_venue(venue)

        if year == 0:
            continue

        items.append(PubItem(
            label=label,
            title=title,
            year=year,
            venue=venue,
            authors=authors,
            ccf_a=ccf_a,
            pdf_links=pdf_links,
            is_award=is_award,
        ))

    return items


# ---------------------------------------------------------------------------
# OpenAlex / arXiv helpers (reused from xchencs pipeline)
# ---------------------------------------------------------------------------

def _norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm_title(a), _norm_title(b)).ratio()


def openalex_search(title: str, *, per_page: int = 5) -> list[dict[str, Any]]:
    url = f"{OPENALEX_WORKS_SEARCH}?search={urllib.parse.quote(title)}&per_page={per_page}"
    data = _http_get(url, timeout_s=45)
    payload = json.loads(data)
    return payload.get("results") or []


def pick_best_openalex_match(
    title: str, expected_year: int | None
) -> tuple[dict[str, Any] | None, float]:
    results = openalex_search(title, per_page=5)
    best = None
    best_score = -1.0
    for w in results:
        cand_title = w.get("display_name") or ""
        score = _title_similarity(title, cand_title)
        pub_year = w.get("publication_year")
        if expected_year is not None and pub_year is not None:
            if abs(int(pub_year) - int(expected_year)) <= 1:
                score += 0.03
            elif abs(int(pub_year) - int(expected_year)) <= 3:
                score -= 0.03
        if score > best_score:
            best_score = score
            best = w
    return best, best_score


def reconstruct_openalex_abstract(w: dict[str, Any] | None) -> str | None:
    if not w:
        return None
    inv = w.get("abstract_inverted_index")
    if not inv:
        return None
    try:
        size = max(i for idxs in inv.values() for i in idxs) + 1
        words = [""] * size
        for token, idxs in inv.items():
            for i in idxs:
                if 0 <= i < size:
                    words[i] = token
        abstract = " ".join(w for w in words if w).strip()
        return abstract or None
    except Exception:
        return None


def openalex_pdf_candidate(w: dict[str, Any] | None) -> str | None:
    if not w:
        return None

    def iter_locations() -> Iterable[dict[str, Any]]:
        loc = w.get("best_oa_location") or None
        if isinstance(loc, dict) and loc:
            yield loc
        for loc2 in w.get("locations") or []:
            if isinstance(loc2, dict) and loc2:
                yield loc2

    for loc in iter_locations():
        for key in ("pdf_url", "url", "landing_page_url"):
            u = loc.get(key)
            if not u or not isinstance(u, str):
                continue
            ul = u.lower()
            if key == "pdf_url":
                return u
            if ul.endswith(".pdf") or "arxiv.org/pdf" in ul:
                return u

    oa = w.get("open_access") or {}
    u = oa.get("oa_url")
    if isinstance(u, str):
        ul = u.lower()
        if ul.endswith(".pdf") or "arxiv.org/pdf" in ul:
            return u
    return None


def discover_pdf_from_landing(landing_url: str) -> str | None:
    try:
        data = _http_get(landing_url, timeout_s=60, attempts=2, headers={"Accept": "text/html,*/*"})
    except Exception:
        return None
    if data.startswith(b"%PDF"):
        return landing_url
    html = data.decode("utf-8", errors="replace")
    m = re.search(
        r'(?is)<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        html,
    )
    if m:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m.group(1).strip()))
    m2 = re.search(r'(?is)href=["\']([^"\']+\.pdf[^"\']*)["\']', html)
    if m2:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m2.group(1).strip()))
    return None


def arxiv_pdf_by_title(title: str) -> str | None:
    query = f'ti:"{title}"'
    url = f"{ARXIV_API}?search_query={urllib.parse.quote(query)}&start=0&max_results=5"
    try:
        feed = _http_get(url, timeout_s=45).decode("utf-8", errors="replace")
    except Exception:
        return None
    entries = re.findall(r"(?is)<entry>.*?</entry>", feed)
    best_abs = None
    best_score = 0.0
    for ent in entries:
        tid = re.search(r"(?is)<title>\s*(.*?)\s*</title>", ent)
        if not tid:
            continue
        cand_title = _strip_tags(tid.group(1)).replace("\n", " ").strip()
        if cand_title.lower() == "arxiv.org e-print archive":
            continue
        score = _title_similarity(title, cand_title)
        if score < 0.85:
            continue
        iid = re.search(r"(?is)<id>\s*(https?://arxiv\.org/abs/[^<]+)\s*</id>", ent)
        if not iid:
            continue
        if score > best_score:
            best_score = score
            best_abs = iid.group(1).strip()
    if not best_abs:
        return None
    return best_abs.replace("/abs/", "/pdf/") + ".pdf"


# ---------------------------------------------------------------------------
# PDF download & text extraction
# ---------------------------------------------------------------------------

def safe_slug(s: str, *, max_len: int = 80) -> str:
    s = s.strip().strip(".")
    s = re.sub(r"[\\/:*?\"<>|]+", "_", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def stable_id(item: PubItem) -> str:
    h = hashlib.sha1(f"{item.year}|{item.title}|{item.venue}|{item.label}".encode("utf-8")).hexdigest()
    return h[:12]


def download_pdf(url: str, dest: Path) -> tuple[bool, str | None]:
    try:
        data = _http_get(url, timeout_s=90, headers={"Accept": "application/pdf"})
        if not data.startswith(b"%PDF"):
            return False, "not_a_pdf"
        dest.write_bytes(data)
        return True, None
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def extract_pdf_text_first_pages(pdf_path: Path, *, max_pages: int = 3) -> str:
    reader = PdfReader(str(pdf_path))
    out: list[str] = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t:
            out.append(t)
    return "\n".join(out).strip()


def extract_writing_signals(full_text: str) -> dict[str, Any]:
    low = full_text.lower()
    return {
        "has_abstract_heading": bool(re.search(r"\babstract\b", low)),
        "has_introduction_heading": bool(
            re.search(r"(\b1\s+introduction\b|\bi\.\s+introduction\b)", low)
        ),
        "has_contributions_phrase": bool(
            re.search(
                r"(we\s+make\s+the\s+following\s+contributions|our\s+contributions?\s+(are|include)|in\s+summary,\s+we\s+)",
                low,
            )
        ),
        "has_rq": bool(re.search(r"\brq\s*1\b", low)),
        "has_threats_to_validity": bool(re.search(r"threats?\s+to\s+validity", low)),
        "has_evaluation_section": bool(re.search(r"\bevaluation\b|\bexperiment(s)?\b", low)),
        "mentions_tool_or_implementation": bool(
            re.search(r"\bwe\s+implemented\b|\bprototype\b|\btool\b|\bimplementation\b", low)
        ),
        "abstract_has_numbers": bool(re.search(r"\babstract\b.*?\d", low, flags=re.S)),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("[1/4] Fetching publications HTML...")
    html = fetch_publications_html()
    all_pubs = parse_publications(html)
    print(f"  Parsed {len(all_pubs)} total publications")

    # Filter: CCF-A only
    pubs = [p for p in all_pubs if p.ccf_a]
    print(f"  CCF-A papers: {len(pubs)}")

    # Deduplicate by stable id
    uniq: dict[str, PubItem] = {}
    for p in pubs:
        uniq[stable_id(p)] = p
    pubs = list(uniq.values())
    pubs.sort(key=lambda x: (x.year, x.label, x.title))
    print(f"  After dedup: {len(pubs)}")

    results: list[dict[str, Any]] = []
    processed_ids: set[str] = set()

    resume_disabled = "--no-resume" in sys.argv
    refresh_missing = "--refresh-missing" in sys.argv
    enable_arxiv_fallback = "--arxiv-fallback" in sys.argv

    # Resume from previous checkpoint
    if INDEX_JSON.exists() and not resume_disabled:
        try:
            existing = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
            existing_papers = existing.get("papers") or []
            if isinstance(existing_papers, list) and existing_papers:
                kept = []
                for p in existing_papers:
                    pid = p.get("id")
                    if not (isinstance(pid, str) and pid):
                        continue
                    pdf = p.get("pdf") or {}
                    downloaded = bool(pdf.get("downloaded"))
                    if refresh_missing:
                        if downloaded:
                            processed_ids.add(pid)
                            kept.append(p)
                    else:
                        processed_ids.add(pid)
                        kept.append(p)
                results = kept
                mode = "downloaded-only" if refresh_missing else "all"
                print(f"  [resume:{mode}] loaded {len(results)} from existing index")
        except Exception:
            pass

    print(f"\n[2/4] Processing {len(pubs) - len(processed_ids)} new papers...")

    for idx, item in enumerate(pubs, start=1):
        pid = stable_id(item)
        if pid in processed_ids:
            continue
        if idx > 1:
            time.sleep(0.2)

        print(f"  [{idx}/{len(pubs)}] {item.year} {item.label} {item.title[:60]}...")

        oa_error = None
        try:
            oa_best, oa_score = pick_best_openalex_match(item.title, item.year)
        except Exception as exc:
            oa_best, oa_score = None, -1.0
            oa_error = f"{type(exc).__name__}: {exc}"

        oa_abstract = reconstruct_openalex_abstract(oa_best)
        oa_pdf = openalex_pdf_candidate(oa_best)
        oa_is_oa = ((oa_best or {}).get("open_access") or {}).get("is_oa") is True

        pdf_url = None
        source = None
        if item.pdf_links:
            pdf_url = item.pdf_links[0]
            source = "author_page"
        elif oa_pdf:
            pdf_url = oa_pdf
            source = "openalex"
        elif oa_is_oa:
            bol = (oa_best or {}).get("best_oa_location") or {}
            landing = bol.get("landing_page_url") or bol.get("url")
            if isinstance(landing, str) and landing:
                discovered = discover_pdf_from_landing(landing)
                if discovered:
                    pdf_url = discovered
                    source = "openalex_discovered"
        elif enable_arxiv_fallback:
            arxiv_pdf = arxiv_pdf_by_title(item.title)
            if arxiv_pdf:
                pdf_url = arxiv_pdf
                source = "arxiv"

        pdf_record: dict[str, Any] = {"url": pdf_url, "source": source, "downloaded": False}

        local_pdf = None
        existing_files = list(PDF_DIR.glob(f"*_{pid}.pdf"))
        if existing_files:
            local_pdf = sorted(existing_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            pdf_record["downloaded"] = True
            if pdf_record.get("source") is None:
                pdf_record["source"] = "local_cache"

        if pdf_url and local_pdf is None:
            slug = safe_slug(item.title)
            venue_short = ""
            vl = item.venue.lower()
            for tag in ["ICSE", "FSE", "ASE", "ISSTA", "TSE", "TOSEM"]:
                if tag.lower() in vl:
                    venue_short = tag
                    break
            filename = f"{item.year}_{venue_short}_{slug}_{pid}.pdf"
            local_pdf = PDF_DIR / filename
            if not local_pdf.exists():
                ok, err = download_pdf(pdf_url, local_pdf)
                pdf_record["downloaded"] = ok
                if err:
                    pdf_record["error"] = err
                    if local_pdf.exists():
                        try:
                            local_pdf.unlink()
                        except Exception:
                            pass
                else:
                    print(f"    -> Downloaded ({source})")
            else:
                pdf_record["downloaded"] = True

        features = None
        extracted_preview_path = None
        if local_pdf and local_pdf.exists() and pdf_record.get("downloaded"):
            try:
                preview = extract_pdf_text_first_pages(local_pdf, max_pages=3)
                extracted_preview_path = str((EXTRACT_DIR / (local_pdf.stem + ".txt")).resolve())
                (EXTRACT_DIR / (local_pdf.stem + ".txt")).write_text(preview[:20000], encoding="utf-8")
                features = extract_writing_signals(preview)
            except Exception as exc:
                pdf_record["extract_error"] = f"{type(exc).__name__}: {exc}"

        results.append({
            "id": pid,
            "label": item.label,
            "title": item.title,
            "year": item.year,
            "venue": item.venue,
            "authors": item.authors,
            "is_award": item.is_award,
            "openalex": {
                "score": oa_score,
                "id": (oa_best or {}).get("id"),
                "doi": (oa_best or {}).get("doi"),
                "display_name": (oa_best or {}).get("display_name"),
                "publication_year": (oa_best or {}).get("publication_year"),
                "is_oa": ((oa_best or {}).get("open_access") or {}).get("is_oa"),
                "abstract": oa_abstract,
                "error": oa_error,
            },
            "pdf": {
                **pdf_record,
                "path": (str(local_pdf.resolve()) if local_pdf and local_pdf.exists() else None),
                "preview_text_path": extracted_preview_path,
            },
            "signals": features,
        })

        # Checkpoint every 10 items
        if idx % 10 == 0:
            checkpoint = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source_publications_url": PUB_URL,
                "paper_count": len(results),
                "papers": results,
                "note": "checkpoint (partial)",
            }
            INDEX_JSON.write_text(
                json.dumps(checkpoint, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            dl_count = sum(1 for p in results if p.get("pdf", {}).get("downloaded"))
            print(f"  [checkpoint] {idx}/{len(pubs)}; downloaded {dl_count}")

    # Final output
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_publications_url": PUB_URL,
        "paper_count": len(results),
        "papers": results,
    }
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Summary markdown
    downloaded = [p for p in results if p.get("pdf", {}).get("downloaded")]
    missing = [p for p in results if not p.get("pdf", {}).get("downloaded")]

    def pct(n: int, d: int) -> str:
        return f"{(100.0 * n / d):.1f}%" if d else "n/a"

    sig_keys = [
        "has_abstract_heading", "has_introduction_heading", "has_contributions_phrase",
        "has_rq", "has_threats_to_validity", "has_evaluation_section",
        "mentions_tool_or_implementation", "abstract_has_numbers",
    ]
    agg = {k: 0 for k in sig_keys}
    for p in downloaded:
        sig = p.get("signals") or {}
        for k in sig_keys:
            if sig.get(k):
                agg[k] += 1

    lines = []
    lines.append("# 胡星老师（Xing Hu）CCF-A 论文：PDF 可得性与写作信号汇总")
    lines.append("")
    lines.append(f"- 生成时间（UTC）：`{payload['generated_at']}`")
    lines.append(f"- 条目数：`{len(results)}`（CCF-A only，已去重）")
    lines.append(f"- 成功下载 PDF：`{len(downloaded)}` / `{len(results)}`（{pct(len(downloaded), len(results))}）")
    lines.append(f"- 获奖论文：`{sum(1 for p in results if p.get('is_award'))}`")
    lines.append("")
    lines.append("## 下载到的 PDF")
    for p in downloaded:
        award = " 🏅" if p.get("is_award") else ""
        lines.append(f"- {p['year']} {p.get('label','')} {p['title']}{award}")
    lines.append("")
    lines.append("## 写作信号统计（下载成功子集）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in sig_keys:
        lines.append(f"| `{k}` | {agg[k]} | {pct(agg[k], len(downloaded))} |")
    lines.append("")
    lines.append("## 未能获取公开 PDF 的条目")
    for p in missing:
        pdf = p.get("pdf") or {}
        err = pdf.get("error") or ""
        src = pdf.get("source") or "none"
        lines.append(f"- {p['year']} {p.get('label','')} {p['title']}（source={src} {err}）")
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n[3/4] Results:")
    print(f"  Index: {INDEX_JSON}")
    print(f"  Summary: {SUMMARY_MD}")
    print(f"  PDFs downloaded: {len(downloaded)} / {len(results)}")
    print(f"\n[4/4] Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

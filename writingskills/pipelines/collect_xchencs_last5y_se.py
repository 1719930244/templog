#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collect (publicly accessible) PDFs for Xiang Chen's software-engineering papers
from the last ~5 years, then extract lightweight writing-style signals.

Inputs:
  - Optionally uses ../xchencs_publications.html (cached). If missing, it will download it.

Outputs (in this folder):
  - xchencs_last5y_se_index.json: paper list, metadata, PDF status, extracted signals
  - xchencs_last5y_se_summary.md: aggregated signals + missing PDF list
  - pdfs/*.pdf: downloaded PDFs (best-effort, only if publicly accessible)
  - extracted/*.txt: extracted first-page text (debug, small)

Notes:
  - This script does NOT bypass paywalls or anti-bot protections.
  - Many publisher PDFs are not accessible; for those, the index will mark as missing.
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
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

try:
    from pypdf import PdfReader  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency pypdf: {exc}")


PUB_URL = "https://xchencs.github.io/publications.html"
BASE_URL = "https://xchencs.github.io/"
OPENALEX_WORKS_SEARCH = "https://api.openalex.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"

# Interpreting "近五年" at 2026-02-09: sliding window since 2021.
WINDOW_START_YEAR = 2021

ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / "pdfs"
EXTRACT_DIR = ROOT / "extracted"
INDEX_JSON = ROOT / "xchencs_last5y_se_index.json"
SUMMARY_MD = ROOT / "xchencs_last5y_se_summary.md"

PUBLICATIONS_HTML_CACHE = (ROOT / ".." / "xchencs_publications.html").resolve()

CTX = ssl.create_default_context()


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


def _is_probably_name(s: str) -> bool:
    s = s.strip().replace("*", "")
    return bool(re.fullmatch(r"[A-Z][a-z]+(\s+[A-Z][a-z]+){1,2}", s))


def _looks_like_title(s: str) -> bool:
    if not s or _is_probably_name(s):
        return False
    words = [w for w in re.split(r"\s+", s) if w]
    if len(words) >= 4:
        return True
    if len(s) >= 20 and any(ch in s for ch in [" ", ":", "?", "-", "：", "—"]):
        return True
    if any(ch in s for ch in [":", "?", "：", "—"]):
        return True
    return False


@dataclass
class PubItem:
    section: str
    title: str
    year: int
    venue: str
    label: str
    ccf: str | None
    links: list[str]
    pdf_links: list[str]


def parse_publications(html: str) -> list[PubItem]:
    def section_slice(name: str) -> str:
        m = re.search(rf"(?is)<h2>\s*{re.escape(name)}\s*</h2>", html)
        if not m:
            return ""
        start = m.end()
        # end at next h2
        m2 = re.search(r"(?is)<h2>\s*[^<]+?\s*</h2>", html[start:])
        end = start + (m2.start() if m2 else len(html))
        return html[start:end]

    sections = [
        "International Journal",
        "International Conference",
        "Top Journals in China（国内一级学报）",
    ]

    items: list[PubItem] = []
    for sec in sections:
        content = section_slice(sec)
        if not content:
            continue
        # jemdoc HTML is mostly well-formed for these sections
        for blk in re.findall(r"(?is)<li\b[^>]*>\s*.*?</li>", content):
            strongs = [_strip_tags(s) for s in re.findall(r"(?is)<strong>\s*(.*?)\s*</strong>", blk)]
            title = ""
            for s in strongs:
                if _looks_like_title(s):
                    title = s
                    break
            if not title:
                bm = re.search(r"(?is)<b>\s*(.*?)\s*</b>", blk)
                if bm:
                    title = _strip_tags(bm.group(1))

            ym = re.search(r"(?is)</em>\.?\s*(20\d{2})", blk)
            year = int(ym.group(1)) if ym else None
            if year is None:
                ym2 = re.search(r"\b(20\d{2})\b", blk)
                year = int(ym2.group(1)) if ym2 else None
            if not (title and year):
                continue

            vm = re.search(r"(?is)<em>\s*(.*?)\s*</em>", blk)
            venue = _strip_tags(vm.group(1)) if vm else ""

            lm = re.search(r"(?is)<span[^>]*>\s*\[([^\]]+)\]\s*</span>", blk)
            label = _strip_tags(lm.group(1)) if lm else ""

            ccf = None
            ccfm = re.search(r"\(\s*CCF\s*([ABC])\s*\)", _strip_tags(blk))
            if ccfm:
                ccf = ccfm.group(1)

            hrefs = re.findall(r'(?is)<a\s+href="([^"]+)"', blk)
            links = [urllib.parse.urljoin(BASE_URL, h) for h in hrefs]
            pdf_links = [
                u
                for u in links
                if re.search(r"(?i)\.pdf($|[?#])", u) or "arxiv.org/pdf" in u.lower()
            ]

            items.append(
                PubItem(
                    section=sec,
                    title=title,
                    year=year,
                    venue=venue,
                    label=label,
                    ccf=ccf,
                    links=links,
                    pdf_links=pdf_links,
                )
            )

    return items


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
                # OpenAlex marks this as a PDF URL even if it doesn't end with ".pdf".
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

    # Common scholarly metadata tags
    m = re.search(
        r'(?is)<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        html,
    )
    if m:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m.group(1).strip()))

    # Any direct .pdf href
    m2 = re.search(r'(?is)href=["\']([^"\']+\.pdf[^"\']*)["\']', html)
    if m2:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m2.group(1).strip()))

    # Some sites use meta content without citation_pdf_url
    m3 = re.search(r'(?is)content=["\']([^"\']+\.pdf[^"\']*)["\']', html)
    if m3:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m3.group(1).strip()))

    # Fall back: try a few links that *look* like PDF endpoints (no extension).
    hrefs = re.findall(r'(?is)href=["\']([^"\']+)["\']', html)
    pdfish = []
    for h in hrefs:
        hl = h.lower()
        if "pdf" in hl or "viewcontent.cgi" in hl or "download" in hl:
            pdfish.append(h)
    for h in pdfish[:6]:
        u = urllib.parse.urljoin(landing_url, html_lib.unescape(h.strip()))
        try:
            head = _http_get(u, timeout_s=20, attempts=1, headers={"Range": "bytes=0-4095"})
        except Exception:
            continue
        if head.startswith(b"%PDF"):
            return u

    return None


def arxiv_pdf_by_title(title: str) -> str | None:
    # Best-effort: try an exact-ish title query.
    query = f'ti:"{title}"'
    url = f"{ARXIV_API}?search_query={urllib.parse.quote(query)}&start=0&max_results=5"
    try:
        feed = _http_get(url, timeout_s=45).decode("utf-8", errors="replace")
    except Exception:
        return None

    # Extract abs ids and pick by title similarity
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
            # some endpoints return HTML or redirects
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
    t = full_text
    low = t.lower()
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


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    html = fetch_publications_html()
    pubs = parse_publications(html)

    # Filter: last 5-year sliding window; and SE-ish (exclude clearly unrelated venue)
    pubs = [p for p in pubs if p.year >= WINDOW_START_YEAR and p.venue.strip() != "Energy"]

    # Deduplicate by stable id
    uniq: dict[str, PubItem] = {}
    for p in pubs:
        uniq[stable_id(p)] = p
    pubs = list(uniq.values())
    pubs.sort(key=lambda x: (x.year, x.label, x.title))

    results: list[dict[str, Any]] = []
    processed_ids: set[str] = set()

    resume_disabled = "--no-resume" in sys.argv
    refresh_missing = "--refresh-missing" in sys.argv

    # Resume from a previous checkpoint if present.
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
                print(
                    f"[resume:{mode}] loaded {len(results)} papers from existing index; will skip {len(processed_ids)} ids"
                )
        except Exception:
            pass

    # Toggle expensive fallbacks: OpenAlex already surfaces many arXiv PDFs.
    enable_arxiv_fallback = "--arxiv-fallback" in sys.argv

    for idx, item in enumerate(pubs, start=1):
        pid = stable_id(item)
        if pid in processed_ids:
            continue
        # polite pacing (OpenAlex is fast, but don't spam)
        if idx > 1:
            time.sleep(0.2)

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
            source = "xchencs_page"
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

        # If we already have a PDF downloaded from a previous run, reuse it even if
        # metadata sources fluctuate.
        local_pdf = None
        existing = list(PDF_DIR.glob(f"*_{pid}.pdf"))
        if existing:
            local_pdf = sorted(existing, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            pdf_record["downloaded"] = True
            if pdf_record.get("source") is None:
                pdf_record["source"] = "local_cache"

        if pdf_url and local_pdf is None:
            sid = pid
            slug = safe_slug(item.title)
            filename = f"{item.year}_{item.label or 'paper'}_{slug}_{sid}.pdf"
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

        results.append(
            {
                "id": pid,
                "section": item.section,
                "title": item.title,
                "year": item.year,
                "venue": item.venue,
                "label": item.label,
                "ccf": item.ccf,
                "source_links": {"links": item.links, "pdf_links": item.pdf_links},
                "openalex": {
                    "score": oa_score,
                    "id": (oa_best or {}).get("id"),
                    "doi": (oa_best or {}).get("doi"),
                    "display_name": (oa_best or {}).get("display_name"),
                    "publication_year": (oa_best or {}).get("publication_year"),
                    "host_venue": ((oa_best or {}).get("host_venue") or {}).get("display_name"),
                    "is_oa": ((oa_best or {}).get("open_access") or {}).get("is_oa"),
                    "oa_url": ((oa_best or {}).get("open_access") or {}).get("oa_url"),
                    "best_oa_location": (oa_best or {}).get("best_oa_location"),
                    "abstract": oa_abstract,
                    "error": oa_error,
                },
                "pdf": {
                    **pdf_record,
                    "path": (str(local_pdf.resolve()) if local_pdf and local_pdf.exists() else None),
                    "preview_text_path": extracted_preview_path,
                },
                "signals": features,
            }
        )

        # Checkpoint every 10 items so long runs don't lose progress.
        if idx % 10 == 0:
            checkpoint = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source_publications_url": PUB_URL,
                "window_start_year": WINDOW_START_YEAR,
                "paper_count": len(results),
                "papers": results,
                "note": "checkpoint (partial; run script again to complete)",
            }
            INDEX_JSON.write_text(
                json.dumps(checkpoint, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"[checkpoint] processed {idx}/{len(pubs)}; downloaded {sum(1 for p in results if p.get('pdf', {}).get('downloaded'))}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_publications_url": PUB_URL,
        "window_start_year": WINDOW_START_YEAR,
        "paper_count": len(results),
        "papers": results,
    }
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Summary markdown
    downloaded = [p for p in results if p.get("pdf", {}).get("downloaded")]
    missing = [p for p in results if not p.get("pdf", {}).get("downloaded")]

    def pct(n: int, d: int) -> str:
        return f"{(100.0 * n / d):.1f}%" if d else "n/a"

    # aggregate signals on downloaded subset
    sig_keys = [
        "has_abstract_heading",
        "has_introduction_heading",
        "has_contributions_phrase",
        "has_rq",
        "has_threats_to_validity",
        "has_evaluation_section",
        "mentions_tool_or_implementation",
        "abstract_has_numbers",
    ]
    agg = {k: 0 for k in sig_keys}
    for p in downloaded:
        sig = p.get("signals") or {}
        for k in sig_keys:
            if sig.get(k):
                agg[k] += 1

    lines = []
    lines.append("# 陈翔老师（Xiang Chen）近五年软工论文：PDF 可得性与写作信号汇总")
    lines.append("")
    lines.append(f"- 生成时间（UTC）：`{payload['generated_at']}`")
    lines.append(f"- 统计窗口：`{WINDOW_START_YEAR}`–`{datetime.now().year}`（按 publications.html 年份字段）")
    lines.append(f"- 条目数：`{len(results)}`（已去重）")
    lines.append(f"- 成功下载 PDF：`{len(downloaded)}` / `{len(results)}`（{pct(len(downloaded), len(results))}）")
    lines.append("")
    lines.append("## 下载到的 PDF（可用于细读）")
    for p in downloaded[:50]:
        lines.append(f"- {p['year']} {p.get('label','')} {p['title']} (`{p['pdf']['path']}`)")
    if len(downloaded) > 50:
        lines.append(f"- ...（其余 {len(downloaded)-50} 篇见 `{INDEX_JSON.name}`）")
    lines.append("")
    lines.append("## 从 PDF 预览页提取到的写作信号（下载成功子集）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in sig_keys:
        lines.append(f"| `{k}` | {agg[k]} | {pct(agg[k], len(downloaded))} |")
    lines.append("")
    lines.append("## 未能获取公开 PDF 的条目（需要你手动或校内/机构访问下载）")
    for p in missing[:80]:
        pdf = p.get("pdf") or {}
        err = pdf.get("error") or pdf.get("extract_error") or ""
        src = pdf.get("source") or "none"
        lines.append(f"- {p['year']} {p.get('label','')} {p['title']}（pdf_source={src} {err}）")
    if len(missing) > 80:
        lines.append(f"- ...（其余 {len(missing)-80} 条见 `{INDEX_JSON.name}`）")
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote index: {INDEX_JSON}")
    print(f"Wrote summary: {SUMMARY_MD}")
    print(f"PDFs downloaded: {len(downloaded)} / {len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

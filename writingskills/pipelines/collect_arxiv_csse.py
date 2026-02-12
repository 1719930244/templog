#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collect open-access software-engineering papers from arXiv (default: cs.SE),
download PDFs, and extract lightweight writing-style signals.

Why this exists:
  - Publisher PDFs are often paywalled; arXiv provides a reliable OA corpus.
  - This script adds more "paper" samples to writingskills with reproducible fetch.

Outputs (under ../outputs and ../caches):
  - outputs/arxiv_csse_index.json
  - outputs/arxiv_csse_summary.md
  - caches/arxiv_csse_feed.xml
  - caches/pdfs_arxiv_csse/*.pdf
  - caches/extracted_arxiv_csse/*.txt

Notes:
  - No paywall/anti-bot bypass.
  - Uses only stdlib + pypdf.
"""

from __future__ import annotations

import hashlib
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from pypdf import PdfReader  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency pypdf: {exc}")


ARXIV_API = "https://export.arxiv.org/api/query"

ROOT = Path(__file__).resolve().parent
WS_ROOT = ROOT.parent
CACHE_DIR = WS_ROOT / "caches"
OUT_DIR = WS_ROOT / "outputs"

FEED_CACHE = CACHE_DIR / "arxiv_csse_feed.xml"
PDF_DIR = CACHE_DIR / "pdfs_arxiv_csse"
EXTRACT_DIR = CACHE_DIR / "extracted_arxiv_csse"
INDEX_JSON = OUT_DIR / "arxiv_csse_index.json"
SUMMARY_MD = OUT_DIR / "arxiv_csse_summary.md"

CTX = ssl.create_default_context()


def _http_get(
    url: str,
    *,
    timeout_s: int = 60,
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
            time.sleep(0.9 * attempt)
    raise last_exc or RuntimeError("http_get_failed")


def _arg_value(flag: str, default: str | None = None) -> str | None:
    if flag not in sys.argv:
        return default
    i = sys.argv.index(flag)
    if i + 1 >= len(sys.argv):
        return default
    return sys.argv[i + 1]


def _arg_int(flag: str, default: int) -> int:
    v = _arg_value(flag)
    if v is None:
        return default
    try:
        return int(v)
    except Exception:
        return default


def safe_slug(s: str, *, max_len: int = 90) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    s = re.sub(r"[\\/:*?\"<>|]+", "_", s)
    s = s.strip().strip(".")
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s or "untitled"


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


def extract_pdf_writing_signals(full_text: str) -> dict[str, Any]:
    t = full_text or ""
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


def extract_title_signals(title: str) -> dict[str, Any]:
    t = (title or "").strip()
    return {
        "has_colon": (":" in t) or ("：" in t),
        "has_question": "?" in t or "？" in t,
        "has_towards": bool(re.search(r"\btowards?\b", t, flags=re.I)),
        "has_less_is_more": bool(re.search(r"\bless\s+is\s+more\b", t, flags=re.I)),
        "has_acronym": bool(re.search(r"\b[A-Z]{2,}\b", t)),
    }


def extract_abstract_signals(abstract: str) -> dict[str, Any]:
    a = (abstract or "").strip()
    low = a.lower()
    return {
        "has_numbers": bool(re.search(r"\d", a)),
        "has_action_verb": bool(
            re.search(r"\bwe\s+(propose|present|introduce|develop|design|build)\b", low)
        ),
        "has_gap_phrase": bool(
            re.search(
                r"(however|remains\s+challenging|has\s+not\s+been\s+(well|thoroughly)\s+studied|under-explored|lack\s+of)",
                low,
            )
        ),
        "has_results": bool(re.search(r"(results?\s+(show|demonstrate|indicate)|we\s+find)", low)),
    }


@dataclass
class ArxivEntry:
    arxiv_id: str
    title: str
    authors: list[str]
    published: str
    updated: str
    categories: list[str]
    summary: str
    abs_url: str
    pdf_url: str | None


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return (el.text or "").strip()


def _clean_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _arxiv_id_from_abs(abs_url: str) -> str:
    m = re.search(r"/abs/([^?#/]+)", abs_url)
    return m.group(1) if m else abs_url.rsplit("/", 1)[-1]


def parse_arxiv_feed(xml_bytes: bytes) -> list[ArxivEntry]:
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml_bytes)
    out: list[ArxivEntry] = []

    for entry in root.findall("atom:entry", ns):
        abs_url = _text(entry.find("atom:id", ns))
        arxiv_id = _arxiv_id_from_abs(abs_url)
        title = _clean_ws(_text(entry.find("atom:title", ns)))
        summary = _clean_ws(_text(entry.find("atom:summary", ns)))
        published = _text(entry.find("atom:published", ns))
        updated = _text(entry.find("atom:updated", ns))

        authors: list[str] = []
        for a in entry.findall("atom:author", ns):
            authors.append(_clean_ws(_text(a.find("atom:name", ns))))
        authors = [x for x in authors if x]

        categories = [c.get("term", "").strip() for c in entry.findall("atom:category", ns)]
        categories = [c for c in categories if c]

        pdf_url = None
        for link in entry.findall("atom:link", ns):
            href = link.get("href") or ""
            title_attr = (link.get("title") or "").lower()
            type_attr = (link.get("type") or "").lower()
            if title_attr == "pdf" or type_attr == "application/pdf":
                pdf_url = href
                break
        if not pdf_url:
            # fallback: arXiv convention
            pdf_url = abs_url.replace("/abs/", "/pdf/") + ".pdf" if "/abs/" in abs_url else None

        out.append(
            ArxivEntry(
                arxiv_id=arxiv_id,
                title=title,
                authors=authors,
                published=published,
                updated=updated,
                categories=categories,
                summary=summary,
                abs_url=abs_url,
                pdf_url=pdf_url,
            )
        )
    return out


def fetch_feed(
    *,
    query: str,
    start: int,
    max_results: int,
    refresh: bool,
) -> bytes:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if FEED_CACHE.exists() and not refresh:
        return FEED_CACHE.read_bytes()

    url = (
        f"{ARXIV_API}?search_query={urllib.parse.quote(query)}"
        f"&start={start}&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    data = _http_get(url, timeout_s=90, headers={"Accept": "application/atom+xml"})
    FEED_CACHE.write_bytes(data)
    return data


def download_pdf(url: str, dest: Path) -> tuple[bool, str | None]:
    try:
        data = _http_get(url, timeout_s=120, headers={"Accept": "application/pdf"})
        if not data.startswith(b"%PDF"):
            return False, "not_a_pdf"
        dest.write_bytes(data)
        return True, None
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def _load_existing_index() -> dict[str, Any] | None:
    if not INDEX_JSON.exists():
        return None
    try:
        return json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    query = _arg_value("--query", "cat:cs.SE") or "cat:cs.SE"
    start = _arg_int("--start", 0)
    max_results = _arg_int("--max-results", 50)
    since_year = _arg_int("--since-year", 2021)
    refresh_feed = "--refresh-feed" in sys.argv
    refresh_missing = "--refresh-missing" in sys.argv
    no_resume = "--no-resume" in sys.argv
    no_download = "--no-download" in sys.argv

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    existing = None if no_resume else _load_existing_index()
    existing_items: dict[str, dict[str, Any]] = {}
    if existing and isinstance(existing.get("papers"), list):
        for p in existing["papers"]:
            if isinstance(p, dict) and isinstance(p.get("arxiv_id"), str):
                existing_items[p["arxiv_id"]] = p

    feed = fetch_feed(query=query, start=start, max_results=max_results, refresh=refresh_feed)
    entries = parse_arxiv_feed(feed)

    def year_of(published: str) -> int | None:
        m = re.match(r"(\d{4})-", (published or "").strip())
        return int(m.group(1)) if m else None

    entries = [e for e in entries if (year_of(e.published) or 0) >= since_year]

    results: list[dict[str, Any]] = []
    for e in entries:
        prev = existing_items.get(e.arxiv_id)
        if prev and not refresh_missing:
            # If we already have a successful PDF download, keep it.
            pdf_prev = (prev.get("pdf") or {}) if isinstance(prev.get("pdf"), dict) else {}
            if pdf_prev.get("downloaded"):
                results.append(prev)
                continue

        year = year_of(e.published) or 0
        h = hashlib.sha1(f"{e.arxiv_id}|{e.title}".encode("utf-8")).hexdigest()[:10]
        pdf_name = f"{year}_arxiv_{safe_slug(e.arxiv_id)}_{h}.pdf"
        local_pdf = PDF_DIR / pdf_name
        extracted_path = EXTRACT_DIR / (local_pdf.stem + ".txt")

        pdf_record: dict[str, Any] = {
            "source": "arxiv",
            "url": e.pdf_url,
            "downloaded": False,
            "error": None,
            "extract_error": None,
            "path": None,
            "preview_text_path": None,
        }

        signals: dict[str, Any] = {}
        if no_download:
            pdf_record["error"] = "skipped (--no-download)"
        elif not e.pdf_url:
            pdf_record["error"] = "missing_pdf_url"
        else:
            if not local_pdf.exists() or refresh_missing:
                ok, err = download_pdf(e.pdf_url, local_pdf)
                pdf_record["downloaded"] = ok
                pdf_record["error"] = err
            else:
                pdf_record["downloaded"] = True

            if pdf_record["downloaded"]:
                try:
                    preview_text = extract_pdf_text_first_pages(local_pdf, max_pages=3)
                    extracted_path.write_text(preview_text, encoding="utf-8")
                    signals = extract_pdf_writing_signals(preview_text)
                    pdf_record["path"] = str(local_pdf.resolve())
                    pdf_record["preview_text_path"] = str(extracted_path.resolve())
                except Exception as exc:
                    pdf_record["extract_error"] = f"{type(exc).__name__}: {exc}"

        paper = {
            "arxiv_id": e.arxiv_id,
            "title": e.title,
            "authors": e.authors,
            "published": e.published,
            "updated": e.updated,
            "year": year,
            "categories": e.categories,
            "abs_url": e.abs_url,
            "pdf_url": e.pdf_url,
            "abstract": e.summary,
            "title_signals": extract_title_signals(e.title),
            "abstract_signals": extract_abstract_signals(e.summary),
            "pdf": pdf_record,
            "signals": signals,
        }
        results.append(paper)

        # Gentle rate limiting (arXiv is friendly, but be polite)
        time.sleep(0.25)

    results.sort(key=lambda x: (x.get("year", 0), x.get("arxiv_id", "")), reverse=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "arXiv API",
        "query": query,
        "since_year": since_year,
        "start": start,
        "max_results": max_results,
        "paper_count": len(results),
        "papers": results,
    }
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    downloaded = [p for p in results if (p.get("pdf") or {}).get("downloaded")]
    missing = [p for p in results if not (p.get("pdf") or {}).get("downloaded")]

    def pct(n: int, d: int) -> str:
        return f"{(100.0 * n / d):.1f}%" if d else "n/a"

    title_keys = ["has_colon", "has_question", "has_towards", "has_less_is_more", "has_acronym"]
    title_agg = {k: 0 for k in title_keys}
    for p in results:
        ts = p.get("title_signals") or {}
        for k in title_keys:
            if ts.get(k):
                title_agg[k] += 1

    abs_keys = ["has_numbers", "has_action_verb", "has_gap_phrase", "has_results"]
    abs_agg = {k: 0 for k in abs_keys}
    for p in results:
        sig = p.get("abstract_signals") or {}
        for k in abs_keys:
            if sig.get(k):
                abs_agg[k] += 1

    pdf_sig_keys = [
        "has_abstract_heading",
        "has_introduction_heading",
        "has_contributions_phrase",
        "has_rq",
        "has_threats_to_validity",
        "has_evaluation_section",
        "mentions_tool_or_implementation",
        "abstract_has_numbers",
    ]
    pdf_agg = {k: 0 for k in pdf_sig_keys}
    for p in downloaded:
        sig = p.get("signals") or {}
        for k in pdf_sig_keys:
            if sig.get(k):
                pdf_agg[k] += 1

    lines: list[str] = []
    lines.append("# arXiv cs.SE：PDF 可得性与写作信号汇总")
    lines.append("")
    lines.append(f"- 生成时间（UTC）：`{payload['generated_at']}`")
    lines.append(f"- 查询：`{query}`；窗口：`>= {since_year}`；返回：`{len(entries)}` 条（过滤后写入 `{len(results)}` 条）")
    lines.append(f"- 成功下载 PDF：`{len(downloaded)}` / `{len(results)}`（{pct(len(downloaded), len(results))}）")
    lines.append("")

    lines.append("## 下载到的 PDF（可用于细读）")
    for p in downloaded[:80]:
        pdf = p.get("pdf") or {}
        lines.append(f"- {p.get('year')} arXiv {p.get('arxiv_id')} {p.get('title')} (`{pdf.get('path')}`)")
    if len(downloaded) > 80:
        lines.append(f"- ...（其余 {len(downloaded)-80} 篇见 `{INDEX_JSON.name}`）")
    lines.append("")

    lines.append("## 标题风格信号（全量条目）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in title_keys:
        lines.append(f"| `{k}` | {title_agg[k]} | {pct(title_agg[k], len(results))} |")
    lines.append("")

    lines.append("## 摘要信号（全量条目）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in abs_keys:
        lines.append(f"| `{k}` | {abs_agg[k]} | {pct(abs_agg[k], len(results))} |")
    lines.append("")

    lines.append("## PDF 结构信号（下载成功子集）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in pdf_sig_keys:
        lines.append(f"| `{k}` | {pdf_agg[k]} | {pct(pdf_agg[k], len(downloaded))} |")
    lines.append("")

    lines.append("## 未能获取/未下载 PDF 的条目（可用 --refresh-missing 重试）")
    for p in missing[:120]:
        pdf = p.get("pdf") or {}
        err = pdf.get("error") or pdf.get("extract_error") or ""
        lines.append(f"- {p.get('year')} arXiv {p.get('arxiv_id')} {p.get('title')}（{err}）")
    if len(missing) > 120:
        lines.append(f"- ...（其余 {len(missing)-120} 条见 `{INDEX_JSON.name}`）")
    lines.append("")

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote index: {INDEX_JSON}")
    print(f"Wrote summary: {SUMMARY_MD}")
    print(f"PDFs downloaded: {len(downloaded)} / {len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


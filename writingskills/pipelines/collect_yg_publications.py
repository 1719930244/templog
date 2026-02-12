#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collect (publicly accessible) PDFs for Guang Yang's publications, then extract
lightweight writing-style signals.

Source:
  - https://ntdxyg.github.io/publications/

What this script does:
  - Parses the publications list embedded in the page (Next.js RSC payload)
  - Best-effort finds publicly accessible PDFs (NO paywall/anti-bot bypass)
  - Downloads PDFs and extracts text from first pages
  - Emits an index JSON + a summary markdown with aggregated signals

Outputs (under ../outputs and ../caches):
  - outputs/yg_publications_index.json
  - outputs/yg_publications_summary.md
  - caches/pdfs_yg_publications/*.pdf
  - caches/extracted_yg_publications/*.txt

Notes:
  - Many publisher PDFs are not publicly accessible; those will be marked missing.
  - This script relies only on stdlib + pypdf (already used in this repo).
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


PUB_URL = "https://ntdxyg.github.io/publications/"
OPENALEX_WORKS_SEARCH = "https://api.openalex.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"

ROOT = Path(__file__).resolve().parent
WS_ROOT = ROOT.parent
CACHE_DIR = WS_ROOT / "caches"
OUT_DIR = WS_ROOT / "outputs"
PDF_DIR = CACHE_DIR / "pdfs_yg_publications"
EXTRACT_DIR = CACHE_DIR / "extracted_yg_publications"
INDEX_JSON = OUT_DIR / "yg_publications_index.json"
SUMMARY_MD = OUT_DIR / "yg_publications_summary.md"

PUBLICATIONS_HTML_CACHE = (CACHE_DIR / "yg_publications.html").resolve()

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
            time.sleep(0.9 * attempt)
    raise last_exc or RuntimeError("http_get_failed")


def fetch_publications_html() -> str:
    if PUBLICATIONS_HTML_CACHE.exists():
        return PUBLICATIONS_HTML_CACHE.read_text(encoding="utf-8", errors="replace")
    data = _http_get(PUB_URL)
    PUBLICATIONS_HTML_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PUBLICATIONS_HTML_CACHE.write_bytes(data)
    return data.decode("utf-8", errors="replace")


def _json_unescape(js_string_literal_content: str) -> str:
    # The Next.js payload stores chunks as JS string literals; JSON string escape
    # rules are compatible for our needs.
    return json.loads(f"\"{js_string_literal_content}\"")

def _extract_rsc_text_records(html: str) -> dict[str, str]:
    """
    Extract Next.js RSC `T` records into a map: hex_id -> utf-8 string.

    The App Router Flight stream stores text records as:
      <id>:T<hex_len>,<utf8_bytes...>

    `hex_len` is byte length, so we MUST parse on bytes to stay aligned.
    """
    chunks = re.findall(
        r'self\.__next_f\.push\(\[1,"(.*?)"\]\)\s*</script>',
        html,
        flags=re.S,
    )
    if not chunks:
        return {}

    stream = b"".join(_json_unescape(ch).encode("utf-8") for ch in chunks)
    pat = re.compile(rb"([0-9a-f]+):T([0-9a-f]+),")

    pos = 0
    out: dict[str, str] = {}
    while True:
        m = pat.search(stream, pos)
        if not m:
            break
        rid = m.group(1).decode("ascii", errors="ignore")
        length = int(m.group(2), 16)
        data_start = m.end()
        data_end = data_start + length
        data = stream[data_start:data_end]
        out[rid] = data.decode("utf-8", errors="replace")
        pos = data_end

    return out


def parse_publications_from_html(html: str) -> list[dict[str, Any]]:
    """
    The page is a Next.js App Router site which embeds its data in:
      self.__next_f.push([1,"..."])

    One of the chunks contains: \"publications\":[{...}, ...]
    We locate that chunk, unescape it, then extract and parse the JSON array.
    """
    chunks = re.findall(
        r'self\.__next_f\.push\(\[1,"(.*?)"\]\)\s*</script>',
        html,
        flags=re.S,
    )
    pub_chunk = None
    for ch in chunks:
        if '\\"publications\\":' in ch:
            pub_chunk = ch
            break
    if not pub_chunk:
        raise RuntimeError("Could not find publications payload in page HTML.")

    payload = _json_unescape(pub_chunk)
    key = '"publications":'
    idx = payload.find(key)
    if idx < 0:
        raise RuntimeError("Publications key not found after unescape.")
    start = payload.find("[", idx)
    if start < 0:
        raise RuntimeError("Publications array start not found.")

    level = 0
    end = None
    for i, ch in enumerate(payload[start:], start=start):
        if ch == "[":
            level += 1
        elif ch == "]":
            level -= 1
            if level == 0:
                end = i + 1
                break
    if end is None:
        raise RuntimeError("Failed to bracket-match publications array.")

    arr_text = payload[start:end]
    pubs = json.loads(arr_text)
    if not isinstance(pubs, list):
        raise RuntimeError("Parsed publications is not a list.")

    # Resolve `$xx` references for large fields (abstract/bibtex) via RSC T-records.
    text_map = _extract_rsc_text_records(html)
    if text_map:
        for p in pubs:
            if not isinstance(p, dict):
                continue
            for key in ("abstract", "bibtex"):
                v = p.get(key)
                if isinstance(v, str) and re.fullmatch(r"\$[0-9a-f]+", v):
                    p[key] = text_map.get(v[1:], v)

    return pubs


def _norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm_title(a), _norm_title(b)).ratio()


def openalex_search(title: str, *, per_page: int = 5) -> list[dict[str, Any]]:
    url = f"{OPENALEX_WORKS_SEARCH}?search={urllib.parse.quote(title)}&per_page={per_page}"
    data = _http_get(url, timeout_s=60)
    payload = json.loads(data)
    return payload.get("results") or []


def openalex_get_by_doi(doi: str) -> dict[str, Any] | None:
    doi = (doi or "").strip()
    if not doi:
        return None
    doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    url = f"{OPENALEX_WORKS_SEARCH}/{doi_url}"
    try:
        data = _http_get(url, timeout_s=60, attempts=2)
    except Exception:
        return None
    try:
        w = json.loads(data)
    except Exception:
        return None
    return w if isinstance(w, dict) else None


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
        data = _http_get(
            landing_url,
            timeout_s=75,
            attempts=2,
            headers={"Accept": "text/html,*/*"},
        )
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

    m3 = re.search(r'(?is)content=["\']([^"\']+\.pdf[^"\']*)["\']', html)
    if m3:
        return urllib.parse.urljoin(landing_url, html_lib.unescape(m3.group(1).strip()))

    hrefs = re.findall(r'(?is)href=["\']([^"\']+)["\']', html)
    pdfish: list[str] = []
    for h in hrefs:
        hl = h.lower()
        if "pdf" in hl or "viewcontent.cgi" in hl or "download" in hl:
            pdfish.append(h)
    for h in pdfish[:6]:
        u = urllib.parse.urljoin(landing_url, html_lib.unescape(h.strip()))
        try:
            head = _http_get(
                u, timeout_s=20, attempts=1, headers={"Range": "bytes=0-4095"}
            )
        except Exception:
            continue
        if head.startswith(b"%PDF"):
            return u

    return None


def arxiv_pdf_by_title(title: str) -> str | None:
    query = f'ti:"{title}"'
    url = f"{ARXIV_API}?search_query={urllib.parse.quote(query)}&start=0&max_results=5"
    try:
        feed = _http_get(url, timeout_s=60).decode("utf-8", errors="replace")
    except Exception:
        return None

    entries = re.findall(r"(?is)<entry>.*?</entry>", feed)
    best_abs = None
    best_score = 0.0
    for ent in entries:
        tid = re.search(r"(?is)<title>\s*(.*?)\s*</title>", ent)
        if not tid:
            continue
        cand_title = re.sub(r"(?is)<.*?>", "", tid.group(1)).replace("\n", " ").strip()
        if cand_title.lower() == "arxiv.org e-print archive":
            continue
        score = _title_similarity(title, cand_title)
        if score < 0.86:
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
    s = (s or "").strip().strip(".")
    s = re.sub(r"[\\/:*?\"<>|]+", "_", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def stable_id(*parts: str) -> str:
    h = hashlib.sha1("|".join(p.strip() for p in parts if p).encode("utf-8")).hexdigest()
    return h[:12]


def download_pdf(url: str, dest: Path) -> tuple[bool, str | None]:
    try:
        data = _http_get(url, timeout_s=120, headers={"Accept": "application/pdf"})
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


def extract_pdf_signals(full_text: str) -> dict[str, Any]:
    low = (full_text or "").lower()
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


def extract_abstract_signals(abstract: str) -> dict[str, Any]:
    a = (abstract or "").strip()
    low = a.lower()
    is_zh = bool(re.search(r"[\u4e00-\u9fff]", a))
    if is_zh:
        return {
            "lang": "zh",
            "has_numbers": bool(re.search(r"\d", a)),
            "has_propose": bool(re.search(r"(提出|设计|构建|我们提出|本文提出)", a)),
            "has_results": bool(re.search(r"(结果(表明|显示)|实验(结果)?表明|实验结果显示)", a)),
        }
    return {
        "lang": "en",
        "has_numbers": bool(re.search(r"\d", a)),
        "has_action_verb": bool(
            re.search(
                r"\b((we|this\s+paper|this\s+study)\s+(propose|present|introduce|develop|design|build|conduct|investigate))\b",
                low,
            )
        ),
        "has_gap_phrase": bool(re.search(r"\b(remains?|has\s+not\s+been)\b", low)),
        "has_results": bool(
            re.search(
                r"\b(results?\s+(show|suggest|indicate)|experimental\s+results|our\s+(experiments?|evaluation)\s+(show|suggest|indicate)|we\s+(show|demonstrate))\b",
                low,
            )
        ),
    }


def title_style_signals(title: str) -> dict[str, Any]:
    t = (title or "").strip()
    return {
        "has_colon": ":" in t,
        "has_question": "?" in t,
        "has_towards": bool(re.search(r"\bTowards\b", t)),
        "has_less_is_more": bool(re.search(r"\bLess\s+is\s+More\b", t)),
        "has_acronym": bool(re.search(r"\b[A-Z]{3,}\b", t)),
    }


@dataclass
class PubItem:
    paper_id: str
    page_id: str
    title: str
    year: int
    abbr: str
    venue: str
    typ: str
    doi: str | None
    url: str | None
    code: str | None
    tags: list[str]
    abstract: str | None


def to_pub_items(raw: list[dict[str, Any]]) -> list[PubItem]:
    items: list[PubItem] = []
    for p in raw:
        page_id = str(p.get("id") or "").strip()
        title = (p.get("title") or "").strip()
        year = p.get("year")
        if not title or not isinstance(year, int):
            continue
        doi = (p.get("doi") or "").strip() or None
        abbr = (p.get("abbr") or "").strip()
        typ = (p.get("type") or "").strip()
        venue = (p.get("conference") or p.get("journal") or "").strip()
        url = (p.get("url") or "").strip() or None
        code = (p.get("code") or "").strip() or None
        tags = p.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        abstract = (p.get("abstract") or "").strip() or None

        pid = stable_id(str(year), title, doi or "", p.get("id") or "")
        items.append(
            PubItem(
                paper_id=pid,
                page_id=page_id,
                title=title,
                year=year,
                abbr=abbr,
                venue=venue,
                typ=typ,
                doi=doi,
                url=url,
                code=code,
                tags=[str(t) for t in tags if t],
                abstract=abstract,
            )
        )
    items.sort(key=lambda x: (x.year, x.abbr, x.title))
    return items


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    html = fetch_publications_html()
    raw = parse_publications_from_html(html)
    pubs = to_pub_items(raw)

    results: list[dict[str, Any]] = []
    processed_ids: set[str] = set()

    resume_disabled = "--no-resume" in sys.argv
    refresh_missing = "--refresh-missing" in sys.argv
    enable_arxiv_fallback = "--arxiv-fallback" in sys.argv

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
                    f"[resume:{mode}] loaded {len(results)} papers; will skip {len(processed_ids)} ids"
                )
        except Exception:
            pass

    for idx, item in enumerate(pubs, start=1):
        pid = item.paper_id
        if pid in processed_ids:
            continue
        if idx > 1:
            time.sleep(0.2)

        oa_error = None
        oa_best = None
        oa_score = -1.0
        try:
            if item.doi:
                oa_best = openalex_get_by_doi(item.doi)
                oa_score = 2.0 if oa_best else -1.0
            if not oa_best:
                oa_best, oa_score = pick_best_openalex_match(item.title, item.year)
        except Exception as exc:
            oa_best, oa_score = None, -1.0
            oa_error = f"{type(exc).__name__}: {exc}"

        oa_abstract = reconstruct_openalex_abstract(oa_best)
        oa_pdf = openalex_pdf_candidate(oa_best)
        oa_is_oa = ((oa_best or {}).get("open_access") or {}).get("is_oa") is True

        pdf_url = None
        source = None

        # 1) direct url from page (if PDF)
        if item.url:
            ul = item.url.lower()
            if ul.endswith(".pdf") or "arxiv.org/pdf" in ul:
                pdf_url = item.url
                source = "yg_page_url"

        # 2) OpenAlex surfaced OA PDF
        if not pdf_url and oa_pdf:
            pdf_url = oa_pdf
            source = "openalex"

        # 3) If OpenAlex says OA, try landing page discovery
        if not pdf_url and oa_is_oa:
            bol = (oa_best or {}).get("best_oa_location") or {}
            landing = bol.get("landing_page_url") or bol.get("url")
            if isinstance(landing, str) and landing:
                discovered = discover_pdf_from_landing(landing)
                if discovered:
                    pdf_url = discovered
                    source = "openalex_discovered"

        # 4) Try discover PDF from the page URL (publisher/ACL/etc)
        if not pdf_url and item.url:
            discovered = discover_pdf_from_landing(item.url)
            if discovered:
                pdf_url = discovered
                source = "yg_url_discovered"

        # 5) Optional: arXiv title fallback
        if not pdf_url and enable_arxiv_fallback:
            arxiv_pdf = arxiv_pdf_by_title(item.title)
            if arxiv_pdf:
                pdf_url = arxiv_pdf
                source = "arxiv"

        pdf_record: dict[str, Any] = {
            "url": pdf_url,
            "source": source,
            "downloaded": False,
        }

        local_pdf = None
        extracted_preview_path = None
        features = None
        pdf_error = None

        # Reuse a previously downloaded PDF if exists.
        pattern = f"{item.year}_*_{pid}.pdf"
        matches = sorted(PDF_DIR.glob(pattern))
        if matches:
            local_pdf = matches[0]
            pdf_record["downloaded"] = True
            pdf_record["path"] = str(local_pdf.resolve())
        elif pdf_url:
            label = item.abbr or item.venue or item.typ or "paper"
            fname = f"{item.year}_{safe_slug(label)}_{safe_slug(item.title, max_len=90)}_{pid}.pdf"
            local_pdf = PDF_DIR / fname
            ok, err = download_pdf(pdf_url, local_pdf)
            if ok:
                pdf_record["downloaded"] = True
                pdf_record["path"] = str(local_pdf.resolve())
            else:
                pdf_error = err
                pdf_record["error"] = err
                if local_pdf.exists():
                    try:
                        local_pdf.unlink()
                    except Exception:
                        pass
                local_pdf = None

        if local_pdf and local_pdf.exists():
            try:
                preview = extract_pdf_text_first_pages(local_pdf, max_pages=3)
                extracted_preview_path = str((EXTRACT_DIR / (local_pdf.stem + ".txt")).resolve())
                (EXTRACT_DIR / (local_pdf.stem + ".txt")).write_text(
                    preview, encoding="utf-8", errors="replace"
                )
                features = extract_pdf_signals(preview)
            except Exception as exc:
                pdf_error = f"{type(exc).__name__}: {exc}"
                pdf_record["extract_error"] = pdf_error

        abs_signals = extract_abstract_signals(item.abstract or oa_abstract or "")
        title_signals = title_style_signals(item.title)

        results.append(
            {
                "id": pid,
                "page_id": item.page_id,
                "title": item.title,
                "year": item.year,
                "abbr": item.abbr,
                "venue": item.venue,
                "type": item.typ,
                "tags": item.tags,
                "doi": item.doi,
                "url": item.url,
                "code": item.code,
                "abstract": item.abstract,
                "abstract_signals": abs_signals,
                "title_signals": title_signals,
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

        if idx % 10 == 0:
            checkpoint = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source_publications_url": PUB_URL,
                "paper_count": len(results),
                "papers": results,
                "note": "checkpoint (partial; run script again to complete)",
            }
            INDEX_JSON.write_text(
                json.dumps(checkpoint, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            dl = sum(1 for p in results if p.get("pdf", {}).get("downloaded"))
            print(f"[checkpoint] processed {idx}/{len(pubs)}; downloaded {dl}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_publications_url": PUB_URL,
        "paper_count": len(results),
        "papers": results,
    }
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    downloaded = [p for p in results if p.get("pdf", {}).get("downloaded")]
    missing = [p for p in results if not p.get("pdf", {}).get("downloaded")]

    def pct(n: int, d: int) -> str:
        return f"{(100.0 * n / d):.1f}%" if d else "n/a"

    # Abstract-level signals (all items)
    abs_keys_en = ["has_numbers", "has_action_verb", "has_gap_phrase", "has_results"]
    abs_keys_zh = ["has_numbers", "has_propose", "has_results"]
    abs_agg_en = {k: 0 for k in abs_keys_en}
    abs_agg_zh = {k: 0 for k in abs_keys_zh}
    abs_cnt_en = 0
    abs_cnt_zh = 0
    for p in results:
        sig = (p.get("abstract_signals") or {}) if isinstance(p.get("abstract_signals"), dict) else {}
        lang = sig.get("lang")
        if lang == "en":
            abs_cnt_en += 1
            for k in abs_keys_en:
                if sig.get(k):
                    abs_agg_en[k] += 1
        elif lang == "zh":
            abs_cnt_zh += 1
            for k in abs_keys_zh:
                if sig.get(k):
                    abs_agg_zh[k] += 1

    # Title style signals (all items)
    title_keys = ["has_colon", "has_question", "has_towards", "has_less_is_more", "has_acronym"]
    title_agg = {k: 0 for k in title_keys}
    for p in results:
        ts = p.get("title_signals") or {}
        for k in title_keys:
            if ts.get(k):
                title_agg[k] += 1

    # PDF signals (downloaded subset)
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
    lines.append("# 杨光（Guang Yang）论文：PDF 可得性与写作信号汇总")
    lines.append("")
    lines.append(f"- 生成时间（UTC）：`{payload['generated_at']}`")
    lines.append(f"- 条目数：`{len(results)}`（按 publications 页解析）")
    lines.append(f"- 成功下载 PDF：`{len(downloaded)}` / `{len(results)}`（{pct(len(downloaded), len(results))}）")
    lines.append("")

    lines.append("## 下载到的 PDF（可用于细读）")
    for p in downloaded[:80]:
        lines.append(f"- {p['year']} {p.get('abbr','')} {p['title']} (`{p['pdf']['path']}`)")
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

    lines.append("## 摘要信号（全量条目；按语言分组）")
    lines.append("")
    if abs_cnt_en:
        lines.append(f"### English abstracts (`{abs_cnt_en}`)")
        lines.append("")
        lines.append("| 信号 | 命中数 | 占比 |")
        lines.append("|---|---:|---:|")
        for k in abs_keys_en:
            lines.append(f"| `{k}` | {abs_agg_en[k]} | {pct(abs_agg_en[k], abs_cnt_en)} |")
        lines.append("")
    if abs_cnt_zh:
        lines.append(f"### 中文摘要 (`{abs_cnt_zh}`)")
        lines.append("")
        lines.append("| 信号 | 命中数 | 占比 |")
        lines.append("|---|---:|---:|")
        for k in abs_keys_zh:
            lines.append(f"| `{k}` | {abs_agg_zh[k]} | {pct(abs_agg_zh[k], abs_cnt_zh)} |")
        lines.append("")

    lines.append("## PDF 结构信号（下载成功子集）")
    lines.append("")
    lines.append("| 信号 | 命中数 | 占比 |")
    lines.append("|---|---:|---:|")
    for k in pdf_sig_keys:
        lines.append(f"| `{k}` | {pdf_agg[k]} | {pct(pdf_agg[k], len(downloaded))} |")
    lines.append("")

    lines.append("## 未能获取公开 PDF 的条目（需要你手动或校内/机构访问下载）")
    for p in missing[:120]:
        pdf = p.get("pdf") or {}
        err = pdf.get("error") or pdf.get("extract_error") or ""
        src = pdf.get("source") or "none"
        lines.append(f"- {p['year']} {p.get('abbr','')} {p['title']}（pdf_source={src} {err}）")
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

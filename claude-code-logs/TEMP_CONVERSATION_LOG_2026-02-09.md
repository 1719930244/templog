# TEMP Conversation Log — 2026-02-09

## Task (user request)
- Expand the survey’s **primary studies** using a “multi-agent” (parallel) search, and **strictly screen** candidates per the methodology; then report results.
- After results: save this conversation into a temporary log for later summarization.

## Ground truth constraints (from the manuscript)
- Inclusion/Exclusion criteria are defined in `overleaf_project/sample.tex` (Table `tab:inclusion_exclusion`, IC1–IC6 / EC1–EC5).
- Primary-study time window: **2018–2025** (IC2). A small number of **2026** preprints are allowed only as *forward-looking references*.
- Screening/coding is **single-coder**, but must be **logged** with exclusion reasons (auditable decision log).
- The manuscript states the core synthesis size is **71 primary studies**.

## What was implemented
- Implemented a reproducible OpenAlex pipeline that:
  1) Runs query templates Q1–Q10 (from `overleaf_project/awesome/METHODOLOGY.md`) **in parallel threads** (“agents”).
  2) Uses OpenAlex Works API cursor pagination, filters by concepts:
     - Software engineering: `C115903868`
     - Machine learning: `C119857082`
  3) Deduplicates candidates by DOI → OpenAlex ID → normalized title+year.
  4) Performs **stage-1 title+abstract screening** with explicit EC mapping + reasons.
  5) Emits **stage-2 template** for manual full-text verification (IC6/EC2 edge cases).
- Baseline “already covered” is approximated by DOI overlap with `overleaf_project/software.bib` (this is *not* guaranteed to equal the manuscript’s 71 primary studies set).

## Outputs (all generated under Overleaf repo, not yet committed)
Folder: `overleaf_project/awesome/primary_study_expansion/`
- `run_openalex_pipeline.py` — the pipeline script
- `openalex_queries.json` — exact query strings, per-agent counts, run date, screening tallies
- `candidates_dedup.csv` — deduplicated candidates
- `screening_stage1.csv` — stage-1 decision log (include/uncertain/exclude + EC reason + flags)
- `screening_stage2_template.csv` — stage-2 manual full-text template for include/uncertain
- `PRIMARY_STUDY_EXPANSION_REPORT.md` — human-readable report (queries + counts + top “new include” list)

## Latest run results (2026-02-09)
- Raw hits (sum over agents, before dedup): **4028**
- Deduplicated candidates: **3571**
- Stage-1 (title+abstract) decisions:
  - include: **145**
  - uncertain: **35**
  - exclude: **3391**
- Exclusion breakdown: recorded in `openalex_queries.json` / `PRIMARY_STUDY_EXPANSION_REPORT.md`

## Key caveats (important for next conversation)
- **Stage-1 is only title+abstract**: it cannot fully validate IC6 (empirical efficiency metrics) or EC2 (insufficient technical detail). Items marked `uncertain` require full-text screening.
- **False positives can still exist** even with SE/ML concept filters; OpenAlex concept assignment may include borderline CS/ML papers that mention “code/coding” without being AI4SE primary studies.
- “Already in our synthesis” is currently approximated via DOI overlap with `software.bib`, not a verified 71-primary list.

## How to reproduce
From `C:\\Users\\daoge\\Desktop\\codes\\overleaf_project`:
`python awesome/primary_study_expansion/run_openalex_pipeline.py`

## Repo state
- `overleaf_project` git has **untracked** folder: `awesome/primary_study_expansion/`
- No commit/push was performed in this turn.

---

## Additional task (2026-02-10) — 陈翔老师近五年软工论文写作参考（Skill 沉淀）

### Task (user request)
- Create a local folder `写作参考/`.
- From `https://xchencs.github.io/publications.html`, collect Xiang Chen’s software-engineering papers in the last ~5 years (window start: 2021), best-effort download **publicly accessible** PDFs (no paywall bypass), extract lightweight writing signals, and distill them into a writing Skill doc (SE-oriented).

### Outputs (local workspace)
Folder: `写作参考/`
- `写作参考/README.md` — folder guide
- `写作参考/xchencs_publications.html` — cached publications page

Folder: `写作参考/papers/`
- `写作参考/papers/collect_xchencs_last5y_se.py` — collector (OpenAlex + landing-page PDF discovery; optional arXiv fallback; resume + checkpoints)
- `写作参考/papers/xchencs_last5y_se_index.json` — paper index (OpenAlex metadata + PDF status + extracted signals)
- `写作参考/papers/xchencs_last5y_se_summary.md` — aggregated signals + missing-PDF list
- `写作参考/papers/pdfs/` — downloaded PDFs (publicly accessible only)
- `写作参考/papers/extracted/` — extracted first-page text previews

Folder: `写作参考/skill-se-paper-writing/`
- `写作参考/skill-se-paper-writing/SKILL.md` — SE paper writing workflow/templates/checklist (evidence-backed where possible)

### Latest run results (2026-02-10)
- Run time (UTC): `2026-02-10T01:20:51.729883+00:00`
- Window: `2021`–`2026`; items: `139` (deduped); PDFs downloaded: `9` / `139` (6.5%)
- Note: script does **NOT** bypass paywalls/anti-bot; many publisher PDFs are not publicly accessible.

#### Downloaded PDFs (for close reading)
- 2021 ICSE-2021 Automated Query Reformulation for Efficient Search Based on Query Logs from Stack Overflow. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2021_ICSE-2021_Automated Query Reformulation for Efficient Search Based on Query Logs from Stac_6ed25061f59c.pdf`)
- 2021 SEKE-2021 DeepSCC: Source Code Classification Based on Fine-Tuned RoBERTa (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2021_SEKE-2021_DeepSCC_ Source Code Classification Based on Fine-Tuned RoBERTa_ae11ba95328d.pdf`)
- 2023 COMPSAC-2023 Identifying CC Test Cases with Multiple Features Extraction for Better Fault Localization. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2023_COMPSAC-2023_Identifying CC Test Cases with Multiple Features Extraction for Better Fault Loc_5c8ff1a089ea.pdf`)
- 2023 ICPC-2023 QTC4SO: Automatic Question Title Completion for Stack Overflow. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2023_ICPC-2023_QTC4SO_ Automatic Question Title Completion for Stack Overflow_dc05dee162f4.pdf`)
- 2023 SEKE-2023 An Empirical Study of Adversarial Training in Code Comment Generation. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2023_SEKE-2023_An Empirical Study of Adversarial Training in Code Comment Generation_0f45d0e98b4c.pdf`)
- 2025 EAAI Resource-Efficient Automatic Software Vulnerability Assessment via Knowledge Distillation and Particle Swarm Optimization. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2025_EAAI_Resource-Efficient Automatic Software Vulnerability Assessment via Knowledge Dis_760a3e9c40f9.pdf`)
- 2025 TOSEM Defending Code Language Models against Backdoor Attacks with Deceptive Cross-Entropy Loss. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2025_TOSEM_Defending Code Language Models against Backdoor Attacks with Deceptive Cross-Ent_38194b8ac5ae.pdf`)
- 2026 EMSE Detecting API Compatibility Issues of Android Applications based on Screen Transition Graphs. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2026_EMSE_Detecting API Compatibility Issues of Android Applications based on Screen Trans_cd68fa65540d.pdf`)
- 2026 JSS Exploring the Potential and Limitations of Large Language Models for Novice Program Fault Localization. (`C:\Users\daoge\Desktop\codes\写作参考\papers\pdfs\2026_JSS_Exploring the Potential and Limitations of Large Language Models for Novice Prog_77cee9875d8c.pdf`)

#### Writing signals (downloaded subset)
| Signal | Hits | Rate |
|---|---:|---:|
| `has_abstract_heading` | 8 | 88.9% |
| `has_introduction_heading` | 2 | 22.2% |
| `has_contributions_phrase` | 1 | 11.1% |
| `has_rq` | 2 | 22.2% |
| `has_threats_to_validity` | 1 | 11.1% |
| `has_evaluation_section` | 7 | 77.8% |
| `mentions_tool_or_implementation` | 7 | 77.8% |
| `abstract_has_numbers` | 8 | 88.9% |

### How to reproduce
From `C:\\Users\\daoge\\Desktop\\codes`:
`python 写作参考/papers/collect_xchencs_last5y_se.py --refresh-missing`

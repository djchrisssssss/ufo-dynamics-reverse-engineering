# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.2.6] — 2026-06-12

### Fixed
- **CNT/graphene citation integrity (§6.2)**: `latex/references.bib` entries `Bai2018` and `Zhang2019` carried metadata from unrelated metamaterial/metasurface papers. `Bai2018` corrected to the actual CNT-bundle paper (DOI 10.1038/s41565-018-0141-z); the graphene 130 GPa claim re-cited to a new `Lee2008` entry (Lee et al., *Science* 321, 385–388, 2008, DOI 10.1126/science.1157996), which also replaces the mismatched `src-028` in `bibliography.json`, the canonical full-text reference list, and `per-section/s06`. The defect-strength claim (`ref-111` / `s06-009`) is remapped to the auxiliary source Takakura et al. (*Nature Communications* 10, 3040, 2019) after the previously recorded DOI (10.1038/s41467-019-11760-8) was found to be non-resolving; the `s06-008` source URL carried the same non-resolving DOI and is corrected to the Bai 2018 DOI. Total source count remains 61 (+37 auxiliary)
- **Nimitz acceleration kinematics (§2.2–2.3)**: the sensitivity analysis previously described the descent as "constant acceleration", which is inconsistent with the quoted magnitude. Text now states the Knuth et al. (2019) model explicitly — the object starts and ends approximately at rest (accelerate-then-decelerate profile, mean |a| = 4d/t², peak speed ≈ 46,000 mph = 2× path average) — and quotes the published estimate of ~5,370 g (previously loosely rounded to ~5,300 g), noting that a non-arresting uniform descent would imply roughly half that value. Sensitivity table rescaled (~820–5,370 g) and synced across EN/ZH Markdown, LaTeX, `s02-001`/`s02-013` statistics, per-section references, and both verification reports
- **Alcubierre energy figure (§7.2)**: replaced the self-inconsistent "~10⁶⁴ J for a 200-meter bubble — more than the mass-energy of the observable universe" (10⁶⁴ J is ~6 orders of magnitude *below* the universe's mass-energy) with the Pfenning–Ford result: total negative energy of order −10⁶² kg in mass-equivalent terms (|E| ~ 10⁷⁹ J) for a 100 m-radius bubble, roughly ten orders of magnitude above the observable universe's mass-energy (~10⁵³ kg). Synced in EN/ZH Markdown and LaTeX
- **Unruh temperature (§5.1)**: corrected from ~4×10⁻¹⁶ K to ~2×10⁻¹⁶ K. T = ħa/(2πck_B) at a = 5,370 g ≈ 5.3×10⁴ m/s² evaluates to 2.1×10⁻¹⁶ K (the prior figure was ~2× too high). Synced in EN Markdown, LaTeX, and per-section/s05. Conclusion ("utterly undetectable") unaffected
- **Transmedium dynamic-pressure ratio (§2.7)**: corrected "nearly 1,000 times greater" to "approximately 830 times greater", since q = ½ρv² makes the water/air pressure ratio equal to the density ratio (~830×) already stated in the same paragraph — not ~1,000×. Synced in EN/ZH Markdown and LaTeX

### Changed
- **Version metadata** bumped to 1.2.6 across `CITATION.cff`, `.zenodo.json`, README citation examples, and LaTeX acknowledgments

## [1.2.5] — 2026-03-27

### Added
- **Section 9.8–9.10** in the canonical English Markdown, Traditional Chinese Markdown, and LaTeX paper: phenomenology-constrained oblate shell geometry, tidal/EM constraints, and a missing-time decomposition
- **2 new peer-reviewed sources** on abduction-memory distortion and sleep paralysis in `references/bibliography.json`, `latex/references.bib`, and `references/source-registry.json`
- **Section 9 note map expansion** via canonical note IDs `ref-132` through `ref-136` and the auxiliary phenomenology source `abduction-schema-corpus-2026`

### Changed
- **Section 9 scope** tightened so the deeper theory now explicitly separates low proper acceleration, low tidal stress, electromagnetic boundary-layer effects, and non-geometric missing-time terms
- **Visible bibliography metadata** updated across README, canonical full-text documents, LaTeX acknowledgments, and repo docs to reflect 61 sources and 37 tracked URLs
- **Version metadata** bumped to 1.2.5 across `CITATION.cff`, `.zenodo.json`, README citation examples, and LaTeX acknowledgments

### Removed
- **Legacy root-level reports** `report-en.md` and `report-zh-TW.md` — superseded by canonical `docs/en/full-text.md` and `docs/zh-TW/full-text.md`; legacy copies lacked Section 9 and used outdated superscript citation format

## [1.2.4] — 2026-03-27

### Added
- **Section 9.7 — Layered Field-Shell Transport as a Conservative Particular Case** in the canonical English Markdown, Traditional Chinese Markdown, and LaTeX paper
- **Section 9 note map expansion** via new canonical note IDs `ref-128` through `ref-131` and the auxiliary phenomenology source `watchers-ii-1995`

### Changed
- **Section 9 reference coverage** expanded to include NASA's 2023 UAP study and Green's DIRD on reported biological field effects
- **Section 9 scope summary** in `README.md` updated to reflect the new layered field-shell transport case
- **Version metadata** bumped to 1.2.4 across `CITATION.cff`, `.zenodo.json`, LaTeX acknowledgments, and README citation examples

## [1.2.3] — 2026-03-26

### Added
- **Section 9 — Mathematical and Relativistic Foundations for Anomalous Flight** in the canonical English Markdown, Traditional Chinese Markdown, and LaTeX paper
- **Section 9 reference map** via `references/per-section/s09-references.md` and new canonical note IDs `ref-122` through `ref-127`
- **Section 9 statistics placeholder**: `data/statistics/s09-theoretical-foundations-stats.json` reserved for future empirical constraints while keeping the current section formula-centric

### Changed
- **Repository structure documentation** updated to reflect the new `s09` section in `README.md` and `CLAUDE.md`
- **Bibliography cross-references** expanded so core GR / warp-drive sources now register `s09` in `sections_cited`
- **Version metadata** bumped to 1.2.3 across `CITATION.cff`, `.zenodo.json`, LaTeX acknowledgments, and README citation examples

## [1.2.2] — 2026-03-22

### Changed
- **Citation metadata** realigned to version 1.2.2 and the Zenodo concept DOI (`10.5281/zenodo.19138270`) so repository citations no longer point at an outdated version-specific archive
- **AARO source links** regularized to direct official PDF endpoints for the ORNL metallic specimen synopsis and parallax/forced perspective information paper
- **Compiled PDF delivery** moved to the GitHub Actions `ufo-dynamics-paper` artifact; the committed binary PDF was removed to avoid stale release snapshots

### Fixed
- **Source registry duplication**: validator now fails on duplicate tracked URLs, preventing repeated endpoint entries from silently inflating audit counts
- **Version drift** across `CITATION.cff`, `.zenodo.json`, LaTeX acknowledgments, and citation examples

## [1.2.1] — 2026-03-21

### Added
- **Section 2.2 — Observational Data Quality Assessment**: Data provenance table grading Nimitz (B), Gimbal (C), GoFast (C−); sensitivity analysis on 5,300 g estimate (800–5,300 g range); conditional analytical framing
- **Section 2.8 — Alternative and Competing Explanatory Frameworks**: Systematic evaluation of four competing hypotheses (atmospheric plasma, sensor artifacts, adversarial technology, cognitive bias) with framework selection rationale
- **Key Judgment #11**: Energy-to-curvature transduction gap assessed at very low confidence as missing-physics problem
- **Appendix E — Falsification Criteria**: Six testable conditions for weakening or falsifying the warp bubble framework
- **DIRD evidence weighting** paragraph in Methodology section
- **Transduction gap** paragraph in Section 7.1
- **5 new bibliography entries**: Knuth2019, NASA UAP 2023, Project Condign, AARO Parallax 2024, LLNL NIF 2025
- **Statistics data point s02-013**: Sensitivity analysis range for USS Nimitz acceleration estimate
- **5 new URLs** in source registry (total: 34)

### Changed
- **Abstract** amended: added transduction gap as "missing physics, not missing engineering"
- **Key Judgment #1** amended: added conditional qualifier referencing data quality (§2.2) and alternative frameworks (§2.8)
- **Section numbering** in §2: renumbered 2.2–2.6 → 2.3–2.7 to accommodate new §2.2
- **Bibliography metadata**: total_sources updated from 54 to 59; categories updated
- **NIF April 2025 data** (s04-009): URL updated to specific LLNL ignition page, verification note enriched
- **LaTeX version** bumped to 1.2.1

### Fixed
- **5,300 g attribution**: corrected from ODNI2021 to Knuth et al. 2019 throughout §2 and statistics

## [1.1.1] — 2026-03-21

### Added
- **DOI**: [10.5281/zenodo.19138271](https://doi.org/10.5281/zenodo.19138271) — Zenodo archive with persistent identifier
- **DOI badge** on README
- **AI Collaboration & Data Verification** section in all reports, LaTeX, and README — specifying Claude Opus 4 and Claude Sonnet 4 as collaborating models
- **Compiled PDF** (`latex/ufo_dynamics_RV.pdf`) from Overleaf

### Changed
- **Abstract** refined: near-term barriers are engineering/materials constraints; controlled energy-to-curvature transduction is an unresolved physics gap
- **Data verification** updated to 43/44 cross-checked data points (one contested estimate retained as low-confidence)
- **Document ID removed**: `IRD-UAP-2026-001` replaced by DOI as sole persistent identifier
- **ZH-TW readability**: replaced formal 係 with 是 (4 instances)

### Fixed
- **LaTeX citation keys**: renamed to consistent `AuthorYear` format; DIRD keys to `DIRD_` prefix; fixed `\orcid{}`, `\SIrange`, and confidence table
- **Inline math rendering**: `\text{}` → `\mathrm{}` in subscripts for GitHub compatibility (`\mathcal{E}_\mathrm{shell}`, `\gamma_\mathrm{eff}`)

## [1.1.0] — 2026-03-21

### Added
- **Section 1.1 — Background and Motivation**: Origin story referencing Luis Elizondo's *Imminent: Inside the Pentagon's Hunt for UFOs* (2024), explaining how the Five Observables and DIRD physics motivated this assessment
- **Section 1.2 — Terminology**: Formal definitions of UFO and UAP with set-theoretic relationship (UFO ⊂ UAP); usage convention for the document
- **Section 3.x — Warp Bubble Morphology**: New subsection on warp bubble intensity profiles, observed shape paradox, and morphology classification matrix
- **Bibliography entry #53/54**: Elizondo's *Imminent* added to all reference lists and BibTeX
- **Background section in README**: Bilingual (EN/ZH-TW) origin story
- **Certificate of Authorship**: Five-point declaration in report footers
- **`.zenodo.json`**: Zenodo metadata for automated DOI minting

### Changed
- **Document headers**: Reformatted from intelligence-report style to academic paper style (title, author with ORCID, abstract, methodology & scope)
- **Titles**: Changed from "UAP" to "UFO" in main titles for precision and recognizability
- **Section numbering**: Renumbered §1 subsections (Background → 1.1, Terminology → 1.2, Blue Book → 1.3, AAWSAP → 1.4, Scope → 1.5)
- **CITATION.cff**: Updated with full author metadata (name, email, ORCID, affiliation)
- **README.md**: Academic format with author section, documents table, BibTeX citation

### Fixed
- **Transformation optics formula** (§6.1): Empty `\frac{}{}`  denominator replaced with correct flat notation
- **Inline math rendering** (§2–§6): Added spaces between CJK punctuation and `$` delimiters to fix GitHub math parser failures (10 instances)

## [1.0.0] — 2026-03-20

### Added
- **Project restructuring** following academic repository best practices
  - `data/` directory with JSON Schema validation, per-section statistics, timelines, and comparisons
  - `references/` directory with master bibliography (53 sources), URL registry, and per-section reference files
  - `latex/` directory with REVTeX 4-2 formatted paper and BibTeX bibliography
  - `docs/` directory with bilingual (EN/ZH-TW) full texts and verification reports
- **Data infrastructure**
  - `data/schemas/statistics-schema.json` — JSON Schema v2020-12 for data validation
  - `data/statistics/s02-observables-stats.json` — 12 data points on observable characteristics
  - `data/statistics/s03-propulsion-stats.json` — 4 data points on spacetime engineering constraints
  - `data/statistics/s04-energy-stats.json` — 16 data points on energy sources and fusion progress
  - `data/statistics/s06-materials-stats.json` — 12 data points on advanced materials
  - `data/timelines/uap-investigation-history.csv` — 23 events from 1947 to 2025
  - `data/timelines/dird-publications.csv` — Complete 38 DIRD catalog
  - `data/comparisons/energy-density-comparison.csv` — 8 energy source comparisons
  - `data/comparisons/materials-gap-analysis.csv` — 7 theoretical-vs-practical gap analyses
- **Reference management**
  - `references/bibliography.json` — Master bibliography with 53 sources, DOIs, URLs
  - `references/source-registry.json` — 29 tracked URLs with verification status
  - `references/per-section/s01-references.md` through `s08-references.md` — Per-section source documentation
- **LaTeX academic paper**
  - `latex/main.tex` — REVTeX 4-2 two-column paper (~1400 lines) with full content
  - `latex/references.bib` — 53 BibTeX entries (30 peer-reviewed, 5 government, 12 DIRD, 5 books, 1 preprint)
- **Verification reports** in English and Traditional Chinese
- **Project metadata**: `CLAUDE.md`, `CITATION.cff`, `CHANGELOG.md`, `README.md`

### Changed
- Reports reorganized from root to `docs/en/` and `docs/zh-TW/` bilingual structure
- Original `report-en.md`, `report-zh-TW.md`, `transcription.md` retained at root for backwards compatibility

## [0.1.0] — 2026-03-19

### Added
- Initial assessment report (English) — `report-en.md`
- Traditional Chinese translation — `report-zh-TW.md`
- Source book transcription — `transcription.md`
- 10 JPEG photographs of source material

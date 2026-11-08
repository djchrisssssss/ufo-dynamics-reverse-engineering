# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Scientific-validation audit (five referee-style reviews of physics, numbers, citations, metadata and validation). Release metadata (`CITATION.cff`, `.zenodo.json`, README citation examples, LaTeX acknowledgments) still says 1.2.7 and will be bumped when this is released.

### Fixed — physics and numbers
- **Section 3 (s03-001…004)**: Pfenning–Ford's model-dependent wall bound (~1.6 × 10⁻³³ m for v_b ~ c) replaces the "Planck-length" wall; ideal-plate Casimir density at 100 nm corrected to −4.33 J/m³; the 100 m example is −6.2 × 10⁶² kg mass-equivalent per unit v_b; the 10⁶⁸ Casimir-to-warp ratio is withdrawn (s03-004 "not defined", `verified: false`); P&F dates set to 1997-07.
- **Nimitz acceleration (s02-001, s02-013)**: modal 5,370 (+1,430/−820) g restated as a model output from witness-reported inputs; the former "820–5,370 g" range withdrawn (−820 g is an uncertainty; 2.0 s is a hypothetical ≈ 870 g).
- **Energy (s04)**: D–T 3.37 × 10¹⁴ J/kg; p-¹¹B 7.0 × 10¹³ J/kg and "aneutronic" qualified; deuterium ~34 g/m³ of seawater; antimatter value defined per kg of total annihilated mass; H₂–O₂ no longer called the highest chemical energy density; cosmological-constant ratio marked cutoff-dependent; NIF target gain distinguished from wall-plug gain.
- **Materials (s06)**: s06-009 "up to 85%" defect reduction (not in the cited paper) replaced by Takakura et al.'s 25–66 GPa; E/10 restated as an order-of-magnitude ideal-strength estimate (source corrected from an unrelated 1921 DOI to Orowan 1949); CNT modulus ~1 TPa; specific strength made convention-dependent; CNT 80 GPa identified as a bundle, wall-area value.
- **Comparison and timeline data**: unsupported universal gap factors removed from `materials-gap-analysis.csv`; `energy-density-comparison.csv` p-¹¹B row corrected; `uap-investigation-history.csv` separates the Condon report (Jan 1969) from the Blue Book termination (Dec 1969), dates AAWSAP to 2009, re-sources the Nimitz row to Knuth et al., removes a duplicate ODNI row and the "no verifiable evidence" paraphrase; `dird-publications.csv` records the DIRDs as FOIA-released UNCLASSIFIED//FOUO documents dated 2009–2011, entry 38 as the SECRET/NOFORN version of #23, and DIRD #30 as V. Teofilo.

### Fixed — citations
- **Bibliography metadata**: author lists for MICROSCOPE (src-013) and Bai et al. (src-027) replaced with the Crossref lists; Fell (src-007) is Shaun D. B. Fell; DOIs added for src-003/007/009; AARO/ORNL specimen synopsis (src-034) dated 2024; AARO parallax paper (src-058) given its real title, "Effect of Forced Perspective and Parallax View on UAP Observations" (May 2024); LLNL page (src-059) titled "Achieving Fusion Ignition"; one URL per source for src-033, src-057 and src-058.
- **BibTeX**: DIRD titles match the released documents (#07, #19, #24, #26) and carry DIA numbers for #13/#15; Elizondo ISBN corrected (invalid check digit) and Kaku ISBN reverted to the 2008 Doubleday edition; Knuth, Elizondo, Condign and parallax notes corrected; keys renamed `Kennefick2020` → `GilmoreTauschPebody2022` and `AARO_ORNL2022` → `AARO_ORNL2024`.
- **New sources**: 10 sources cited in the corrected text added as src-062…src-071 (Fuchs et al. 2024; Everett & Roman 1997; Hiscock 1997; Finazzi, Liberati & Barceló 2009; Clark, Hiscock & Larson 1999; Müller & Weiskopf 2012; Olum 1998; Schurig et al. 2006; Monticone & Alù 2016; Fowler 1995). The bibliography now has 71 sources (42 peer-reviewed, 9 government, 12 DIRD, 7 books, 1 preprint).
- **Note map**: GoFast analysis attributed to NASA's UAP Independent Study Team (ref-045c) rather than AARO; ODNI 2022 health statement mapped to src-032 (ref-099, KJ-7); 1919 eclipse note adds Gilmore & Tausch-Pebody; Pfenning–Ford numbers (ref-119) and energy-condition notes (ref-120a) mapped to the papers that contain them; new notes ref-048a, ref-055a, ref-056a and key judgment KJ-10c; unlinked DIRDs and analog-gravity papers linked; Betterton–Kroll auxiliary renamed (no "1938 patent"); further-reading sources (src-012, src-035, src-052) documented in `bibliography.json` metadata. `sections_cited` is now the union of per-section listings and note-map sections.
- **Source registry**: the orphan `ndaa-2023` entry (it pointed at an unrelated bill) removed; ODNI/ICD 203 and FAS URLs recorded as access-restricted after the 2026-11-07 audit (34 URLs: 19 reachable, 15 restricted).

### Fixed — attribution
- Elizondo's memoir treated as a participant account (README zh-TW background, per-section notes, BibTeX note); the AARO/ORNL specimen is no longer described as Betterton–Krohl "slag"; the AARO parallax paper no longer carries the GoFast analysis.

### Changed
- **Data verification**: 42/45 (93.3%) records marked source-cross-checked in metadata (was 43/45); the remaining three are two low-confidence model estimates and one withdrawn ratio. Wording now says provenance review, not empirical confirmation.
- **zh-TW / LaTeX resync**: README zh-TW background, the zh-TW verification report, the zh-TW full text (note IDs, counts, references 1–71 at parity with English) and `latex/main.tex` (which had drifted from v1.2.7 and still carried the withdrawn 10⁶⁸ gap, Planck-length wall and "energy-to-curvature transduction" framing; now includes a Key Judgments section) resynced with the corrected English text.
- **Validator**: header-aware per-section table parsing (no false positives from "Gap" columns); count, book and NIF snippets follow the audit wording; new checks for uncited BibTeX keys, BibTeX ↔ `bibliography.json` DOI/title/year agreement, unmapped sources, `sections_cited` in both directions, non-canonical note IDs, withdrawn-claim tokens in either full text, and unverified records that are neither low-confidence nor withdrawn; an empty HTTP 202 counts as access-restricted. Unit tests cover these paths and add a whole-repository smoke test.
- **Statistics schema**: closed objects (`additionalProperties: false`); `confidence`, `verification_status`, `verification_note` required; ID pattern `^(s0[1-9]|sA[1-4])`.
- **CI**: actions pinned by SHA; the required job runs unit tests plus offline validation; live URL audit moved to the weekly `url-audit.yml`; `requirements.txt` pins `jsonschema==4.25.1`; the LaTeX job fails on undefined citations or references.
- **Docs**: README and CLAUDE.md project structure, validation commands and section table updated; Zenodo keyword "warp bubble morphology" removed, and removed from `CITATION.cff`.

## [1.2.7] — 2026-06-13

### Fixed
- **Bilingual parity in §5.1 (Electromagnetic Signatures)**: the Traditional Chinese full-text had condensed three explanatory passages out of the Dynamical Casimir / Unruh subsection. Restored to match the English canonical text — the boundary-velocity and photon-frequency variable definitions (`[ref-088]`), the warp-bubble-wall broadband-emission description spanning microwave through terahertz to X-ray (`[ref-089]`), and the Unruh-temperature evaluation (~2×10⁻¹⁶ K at 5,370 g, with the Planck-scale caveat, `[ref-091]`). English text, data, statistics, and references are unchanged.

### Changed
- **Version metadata** bumped to 1.2.7 across `CITATION.cff`, `.zenodo.json`, README citation examples, and LaTeX acknowledgments

## [1.2.6] — 2026-06-13

### Fixed
- **CNT/graphene citation integrity (§6.2)**: `latex/references.bib` entries `Bai2018` and `Zhang2019` carried metadata from unrelated metamaterial/metasurface papers. `Bai2018` corrected to the actual CNT-bundle paper (DOI 10.1038/s41565-018-0141-z); the graphene 130 GPa claim re-cited to a new `Lee2008` entry (Lee et al., *Science* 321, 385–388, 2008, DOI 10.1126/science.1157996), which also replaces the mismatched `src-028` in `bibliography.json`, the canonical full-text reference list, and `per-section/s06`. The defect-strength claim (`ref-111` / `s06-009`) is remapped to the auxiliary source Takakura et al. (*Nature Communications* 10, 3040, 2019) after the previously recorded DOI (10.1038/s41467-019-11760-8) was found to be non-resolving; the `s06-008` source URL carried the same non-resolving DOI and is corrected to the Bai 2018 DOI. Total source count remains 61 (+37 auxiliary)
- **Nimitz acceleration kinematics (§2.2–2.3)**: the sensitivity analysis previously described the descent as "constant acceleration", which is inconsistent with the quoted magnitude. Text now states the Knuth et al. (2019) model explicitly — the object starts and ends approximately at rest (accelerate-then-decelerate profile, mean |a| = 4d/t², peak speed ≈ 46,000 mph = 2× path average) — and quotes the published estimate of ~5,370 g (previously loosely rounded to ~5,300 g), noting that a non-arresting uniform descent would imply roughly half that value. Sensitivity table rescaled (~820–5,370 g) and synced across EN/ZH Markdown, LaTeX, `s02-001`/`s02-013` statistics, per-section references, and both verification reports
- **Alcubierre energy figure (§7.2)**: replaced the self-inconsistent "~10⁶⁴ J for a 200-meter bubble — more than the mass-energy of the observable universe" (10⁶⁴ J is ~6 orders of magnitude *below* the universe's mass-energy) with the Pfenning–Ford result: total negative energy of order −10⁶² kg in mass-equivalent terms (|E| ~ 10⁷⁹ J) for a 100 m-radius bubble, roughly ten orders of magnitude above the observable universe's mass-energy (~10⁵³ kg). Synced in EN/ZH Markdown and LaTeX
- **Unruh temperature (§5.1)**: corrected from ~4×10⁻¹⁶ K to ~2×10⁻¹⁶ K. T = ħa/(2πck_B) at a = 5,370 g ≈ 5.3×10⁴ m/s² evaluates to 2.1×10⁻¹⁶ K (the prior figure was ~2× too high). Synced in EN Markdown, LaTeX, and per-section/s05. Conclusion ("utterly undetectable") unaffected
- **Transmedium dynamic-pressure ratio (§2.7)**: corrected "nearly 1,000 times greater" to "approximately 830 times greater", since q = ½ρv² makes the water/air pressure ratio equal to the density ratio (~830×) already stated in the same paragraph — not ~1,000×. Synced in EN/ZH Markdown and LaTeX

### Changed
- **URL spot-check registry (CI hardening)**: removed two entries from `references/source-registry.json` — `nasa-ntrs` (an orphan landing-page URL referenced by no citation) and `src-057` (the UK National Archives webarchive URL for Project Condign, which now returns HTTP 405/404 to automated checks). The Project Condign source is retained in the bibliography and inline notes; only its dead URL leaves the automated spot-check. `total_urls` 37 → 35, `last_audit` refreshed to 2026-06-13, and the HTTP-status counts in both verification reports updated to 23/35 reachable + 12/35 restricted
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

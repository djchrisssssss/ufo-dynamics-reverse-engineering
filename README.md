# Reverse Engineering the Dynamics of UFOs

**UFO 動力學之逆向工程**

*— A Physics-Based Assessment of Unidentified Aerial Phenomena*

---

## Author / 作者

**Kris Lai**
- Email: kriss@scallop.io
- ORCID: [0009-0000-2223-4826](https://orcid.org/0009-0000-2223-4826)
- Affiliation: [Scallop Labs](https://www.scallop.io/)

---

## Documents / 文件

| Document | Language | Description |
|----------|----------|-------------|
| [`docs/en/full-text.md`](docs/en/full-text.md) | English | Full assessment in Markdown |
| [`docs/zh-TW/full-text.md`](docs/zh-TW/full-text.md) | 繁體中文 | 完整評估報告 |
| [`docs/en/verification-report.md`](docs/en/verification-report.md) | English | Data verification report |
| [`docs/zh-TW/verification-report.md`](docs/zh-TW/verification-report.md) | 繁體中文 | 資料驗證報告 |
| [`latex/main.tex`](latex/main.tex) | English | REVTeX 4-2 academic paper |

---

## Abstract / 摘要

A systematic physics-based assessment of reported UFO/UAP flight characteristics. Evaluates whether known or theoretically plausible physical mechanisms — including Alcubierre warp metrics, nuclear fusion, dynamical Casimir effect, and metamaterials — could account for the "Five Observables" taxonomy. Concludes that barriers are primarily **materials science maturity**, not fundamental physics violations.

以物理學為基礎，系統性評估已報告之 UFO/UAP 飛行特徵。評估已知或理論上合理之物理機制——包括阿乎庫比耶曲速度規、核融合、動態卡西米爾效應及超穎材料——能否解釋「五大可觀測特徵」分類法。結論為障礙主要在於**材料科學成熟度**，而非基礎物理學之違反。

> This is an independent scientific assessment. No classified information was used. All sources are publicly available.

---

## Sections / 章節概覽

| # | Section | 節標題 | Key Topics |
|---|---------|--------|------------|
| 1 | Introduction & Historical Context | 導論與歷史脈絡 | Terminology (UFO ⊂ UAP); Blue Book → AATIP → AARO; 38 DIRDs |
| 2 | Observable Characteristics | 可觀測特徵 | Five Observables; geodesic equation; equivalence principle |
| 3 | Propulsion Mechanisms | 推進機制 | Alcubierre metric; warp bubble morphology; exotic matter; wormholes |
| 4 | Energy Sources | 能量來源 | DT/DD fusion; NIF ignition; heavy water; vacuum energy |
| 5 | Electromagnetic Signatures | 電磁特徵 | Dynamical Casimir; Unruh; Hawking; THz gap; biological effects |
| 6 | Advanced Materials | 先進材料 | Metamaterials; CNT; graphene; Bi-Mg analysis; QCD bonding |
| 7 | Integrated Model | 整合模型 | Single-mechanism synthesis; materials gap analysis |
| 8 | Intelligence Gaps | 情報缺口 | Research priorities; definitive evidence criteria |
| A | Appendices | 附錄 | Glossary; equations; DIRD list; confidence definitions |

---

## Data & References / 資料與參考文獻

| Directory | Contents | 內容 |
|-----------|----------|------|
| `data/schemas/` | JSON Schema for statistics validation | 資料驗證 Schema |
| `data/statistics/` | Per-section quantitative data (56 data points) | 各節定量資料 |
| `data/timelines/` | UAP investigation history; DIRD catalog (CSV) | 調查歷程時間軸 |
| `data/comparisons/` | Energy density; materials gap analysis (CSV) | 能量密度與材料差距比較 |
| `references/bibliography.json` | Master bibliography (53 sources) | 主參考書目 |
| `references/source-registry.json` | URL verification registry (29 URLs) | URL 驗證登錄 |
| `references/per-section/` | Per-section reference documentation | 各節參考文獻 |

### Source Breakdown / 來源分布

| Type / 類型 | Count | % |
|-------------|-------|---|
| Peer-reviewed / 同儕審查 | 30 | 56.6% |
| Government / 政府文件 | 5 | 9.4% |
| DIRD / 國防情報參考文件 | 12 | 22.6% |
| Books / 學術專書 | 5 | 9.4% |
| Preprints / 預印本 | 1 | 1.9% |

### Key Government Sources / 主要政府來源

- [ODNI Preliminary Assessment (2021)](https://www.dni.gov/files/ODNI/documents/assessments/Prelimary-Assessment-UAP-20210625.pdf)
- [ODNI 2022 Annual Report](https://www.dni.gov/files/ODNI/documents/assessments/Unclassified-2022-Annual-Report-UAP.pdf)
- [AARO Historical Record Vol I (2024)](https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-2024-0175-HISTORICAL-RECORD-REPORT-VOLUME-I-2024.PDF)
- [ICD 203 Analytic Standards](https://www.dni.gov/files/ODNI/documents/ICD/ICD%20203%20Analytic%20Standards.pdf)
- [DIRD Collection (Black Vault FOIA)](https://documents2.theblackvault.com/documents/dia/AAWSAP-DIRDs/)
- [DIRD Master List (FAS)](https://irp.fas.org/dia/aatip-list.pdf)

---

## LaTeX Paper / 學術論文

The assessment is also available as a two-column academic paper formatted with REVTeX 4-2 (APS Physical Review D style):

```bash
cd latex/
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## Project Structure / 專案結構

```text
UFO-dynamics-reverse-engineering/
├── docs/
│   ├── en/                          # English documents
│   │   ├── full-text.md
│   │   └── verification-report.md
│   └── zh-TW/                      # Traditional Chinese documents
│       ├── full-text.md
│       ├── transcription.md
│       └── verification-report.md
├── data/
│   ├── schemas/                     # JSON Schema validation
│   ├── statistics/                  # Per-section data (4 JSON files)
│   ├── timelines/                   # Historical events (2 CSVs)
│   └── comparisons/                 # Cross-domain analysis (2 CSVs)
├── references/
│   ├── bibliography.json            # 53 sources
│   ├── source-registry.json         # URL verification
│   └── per-section/                 # 8 reference files
├── latex/
│   ├── main.tex                     # REVTeX 4-2 paper
│   ├── references.bib               # 53 BibTeX entries
│   └── figures/
├── CLAUDE.md
├── CITATION.cff
├── CHANGELOG.md
└── README.md
```

---

## How to Cite / 引用方式

### APA

Lai, K. (2026). *Reverse Engineering the Dynamics of UFOs: A Physics-Based Assessment of Unidentified Aerial Phenomena* (IRD-UAP-2026-001). DOI: pending.

### BibTeX

```bibtex
@misc{Lai_UFO_2026,
  title     = {Reverse Engineering the Dynamics of UFOs: A Physics-Based Assessment of Unidentified Aerial Phenomena},
  author    = {Lai, Kris},
  year      = {2026},
  note      = {Document ID: IRD-UAP-2026-001. UNCLASSIFIED --- Open Source Analysis},
  url       = {https://github.com/djchrisssssss/ufo-dynamics-reverse-engineering}
}
```

See also: [CITATION.cff](CITATION.cff)

---

## License / 授權

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

本著作以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19138271.svg)](https://doi.org/10.5281/zenodo.19138271)

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

## Background / 背景

This work originated from a close reading of ***Imminent: Inside the Pentagon's Hunt for UFOs*** (William Morrow, 2024) by **Luis Elizondo** — the former U.S. Army counterintelligence officer who directed the Pentagon's Advanced Aerospace Threat Identification Program (AATIP) from 2008 to 2017. Elizondo's book is the first insider account from the person who actually ran the U.S. government's modern UFO investigation program. It documents how the "Five Observables" taxonomy was created, the commissioning of 38 classified Defense Intelligence Reference Documents (DIRDs) by world-class physicists, the specific radar and sensor cases that defied conventional explanation, and the internal political battles that led to his resignation in protest.

After reading the book, we realized that the physical claims described — instantaneous acceleration, transmedium travel, absence of sonic booms — are not vague anecdotes but structured, sensor-corroborated observations that can be rigorously evaluated against known physics. This assessment was born from that realization: taking Elizondo's observational framework and the DIRD physics as a starting point, then systematically mapping each claimed observable onto established general relativity, quantum field theory, nuclear physics, and materials science to determine what is physically possible, what is theoretically plausible, and where the true engineering gaps lie.

本作品起源於對 **Luis Elizondo** 所著 ***《Imminent: Inside the Pentagon's Hunt for UFOs》***（William Morrow, 2024）的深入研讀。Elizondo 曾任美國陸軍反情報特別探員，於 2008 至 2017 年間主持五角大廈「先進航太威脅識別計畫」（AATIP），是美國政府現代 UFO 調查計畫的實際負責人。本書是首部由計畫主持人以第一手視角撰寫的內部紀實，記錄了「五大可觀測特徵」分類法的建立過程、38 份由頂尖物理學家撰寫之國防情報參考文件（DIRD）的委託始末、挑戰傳統解釋的具體雷達與感測器案例，以及最終促使他辭職抗議的國防部內部政治角力。

閱讀本書後我們意識到，書中所描述的物理特徵——瞬間加速、跨介質飛行、無音爆——並非模糊的軼事傳聞，而是結構化的、有感測器佐證的觀測紀錄，完全可以用已知物理學進行嚴謹檢驗。本評估即誕生於此認知：以 Elizondo 的觀測框架與 DIRD 物理學為起點，系統性地將每項聲稱之可觀測特徵對應至已建立之廣義相對論、量子場論、核物理學及材料科學，判定何者在物理上可能、何者在理論上合理、以及真正的工程差距究竟在何處。

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

## AI Collaboration & Data Verification / AI 協作與資料驗證

This project was produced through a structured collaboration between the human author and **Claude** (Anthropic), using the **Claude Opus 4** and **Claude Sonnet 4** models. AI contributions included:

本專案係由人類作者與 **Claude**（Anthropic）進行結構化協作所產出，使用 **Claude Opus 4** 及 **Claude Sonnet 4** 模型。AI 之貢獻包括：

| Contribution / 貢獻 | Description / 說明 |
|---------------------|--------------------|
| Literature synthesis / 文獻綜整 | Cross-referencing 54 sources / 交叉比對 54 筆來源 |
| Equation typesetting / 公式排版 | Markdown + LaTeX (REVTeX 4-2) formatting / 格式化 |
| Structural organization / 結構組織 | 8-section architecture, bilingual parity / 八章節架構、雙語對照 |
| Data infrastructure / 資料基礎設施 | JSON Schema, statistics, timelines, source registry / 驗證架構 |
| Translation / 翻譯 | Full Traditional Chinese parallel text / 繁體中文全文翻譯 |

**All scientific judgments, assessments, and conclusions are solely those of the human author.**

**所有科學判斷、評估及結論均為人類作者之獨立意見。**

All 56 quantitative data points have been verified against original sources. See the [verification reports](docs/en/verification-report.md) for full audit details.

全部 56 個定量資料點均已對照原始來源進行驗證。完整審核詳見[驗證報告](docs/zh-TW/verification-report.md)。

---

## How to Cite / 引用方式

### APA

Lai, K. (2026). *Reverse Engineering the Dynamics of UFOs: A Physics-Based Assessment of Unidentified Aerial Phenomena* (IRD-UAP-2026-001). DOI: [10.5281/zenodo.19138271](https://doi.org/10.5281/zenodo.19138271).

### BibTeX

```bibtex
@misc{Lai_UFO_2026,
  title     = {Reverse Engineering the Dynamics of UFOs: A Physics-Based Assessment of Unidentified Aerial Phenomena},
  author    = {Lai, Kris},
  year      = {2026},
  note      = {Document ID: IRD-UAP-2026-001. UNCLASSIFIED --- Open Source Analysis},
  doi       = {10.5281/zenodo.19138271},
  url       = {https://github.com/djchrisssssss/ufo-dynamics-reverse-engineering}
}
```

See also: [CITATION.cff](CITATION.cff)

---

## License / 授權

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

本著作以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

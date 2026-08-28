# Hyderabad Electoral Analysis, 1999–2023

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: Election Commission](https://img.shields.io/badge/Data-Election%20Commission-blue.svg)](https://eci.gov.in/)

Vote-share trends across five old-city assembly constituencies in Hyderabad district, over six election cycles.

**[Open the interactive report →](https://varnasr.github.io/Hyderabad-Electoral-Analysis/)** · [The data](Data/HYD-DIST-RESULTS.csv) · [Methodology and limits](METHODOLOGY.md)

---

## What this is

A single dataset and a single-page interactive report tracking party vote share in **Bahadurpura, Chandrayangutta, Charminar, Malakpet and Yakutpura** across the assembly elections of **1999, 2004, 2009, 2014, 2018 and 2023**.

Parties tracked: **AIMIM, TDP, MBT, INC, BJP, and TRS/BRS**.

That is the whole scope. It is a descriptive vote-share series — useful for seeing how competition in these seats has changed, and for pointing at a specific number in an argument.

## What this is *not*

**There is no infrastructure data in this repository.** Earlier metadata described it as a "voting patterns and public infrastructure analysis." That was never accurate: the dataset holds vote shares only, and the report does not mention infrastructure anywhere. The description has been corrected rather than left to mislead. If a vote-share-against-service-delivery comparison is wanted, that is a new data-collection project — see [Open questions](#open-questions).

It is also **not a causal analysis**. It shows what vote shares were, not why. Nothing here identifies the effect of representation on anything. [METHODOLOGY.md](METHODOLOGY.md) sets out exactly what the comparison can and cannot support, and is worth reading before quoting any of it.

## What the data shows

Read alongside the [limits](METHODOLOGY.md#what-this-cannot-establish).

**AIMIM's dominance is real but has been narrowing.** The party holds all five seats, but its share has fallen in four of them since 2014. The clearest movement is in **Yakutpura**, from 45.8% (2014) to **32.9%** (2023) — its weakest recorded position in the series, on the district's lowest turnout that year (39.6%).

**BJP has grown from nothing to second place in parts of the old city.** Absent or marginal in 1999–2009, it reached **26.8% in Charminar** and 18.0% in Malakpet by 2023. In Charminar its rise tracks AIMIM's decline from 73.5% (2004) to 50.1% (2023) almost step for step.

**The old regional players collapsed.** TDP fielded candidates in most of these seats through 2009 and has essentially vanished from the series by 2023. MBT persists only in pockets — though notably it returned to **32.2% in Yakutpura in 2023**, which is most of the explanation for AIMIM's drop there.

**BRS peaked and receded.** Effectively absent before 2009, it climbed to double digits across the district by 2018, then fell back in 2023 — consistent with the statewide swing that year.

**Malakpet is the outlier throughout.** It is the only seat where AIMIM has never crossed 50%, and the only one with a genuine four-way contest. The 1999 and 2004 rows are unusual and should not be read as trend points — see the data notes below.

## The data

[`Data/HYD-DIST-RESULTS.csv`](Data/HYD-DIST-RESULTS.csv) — 27 constituency-year rows, one column per party, values as vote-share percentages. Full dictionary and provenance in [`Data/README.md`](Data/README.md).

Three things to know before using it:

1. **Bahadurpura is missing for 2009.** The seat was created in the 2008 delimitation and *was* contested in 2009 — AIMIM's Mohammad Moazam Khan won it. The row is absent from this dataset, so any 2009 district total understates AIMIM. This is a known gap, not a zero. See [`Data/README.md`](Data/README.md#known-gaps).
2. **Rows do not sum to 100%.** There is no "Others"/independents/NOTA column. A gap of 10–20 points is normal and does not indicate missing party data.
3. **Blank ≠ zero.** A blank cell means the party did not contest that seat that year.

## Open questions

Things this repository does not answer and could:

- **The infrastructure comparison.** Sourcing constituency-level service-delivery data (ward-level GHMC works, water and sanitation coverage, school and PHC provision) for 1999–2023 is the substantial piece of work implied by the old name. It is tractable via GHMC ward records and Census/NFHS ward-level data, but it is a collection project, not a re-labelling.
- **Turnout as a variable.** 2023 turnout is known per seat (Yakutpura 39.6%, Malakpet 41.3%, Charminar 43.3%, Chandrayangutta 45.3%, Bahadurpura 45.5%) but is not in the dataset. Vote share moves differently from votes cast, and the Yakutpura result in particular is hard to read without it.
- **Absolute vote counts.** Shares alone hide whether a party's base grew or the electorate shrank around it.
- **Delimitation discontinuity.** The 2008 boundary redraw means pre-2009 and post-2009 rows are not strictly the same geographies. Treated properly this needs a caveat on every cross-period comparison.

## Using the report

`index.html` is self-contained apart from three CDN libraries (Chart.js, html2canvas, jsPDF) loaded at runtime, so it needs a network connection on first load.

```bash
git clone https://github.com/Varnasr/Hyderabad-Electoral-Analysis.git
cd Hyderabad-Electoral-Analysis
open index.html          # or: python3 -m http.server 8000
```

Every section is deep-linkable — `index.html#constituency-analysis`, `#statistical-analysis`, `#interpretation` and so on — so a specific finding can be sent to someone directly.

Charts export to PNG individually; tables export to CSV; the whole report prints to PDF.

## Sources

- Election Commission of India — constituency-level results, [eci.gov.in](https://eci.gov.in/)
- [`Docs/`](Docs/) — the compiled analysis PDF
- Cross-checks against Wikipedia constituency pages and IndiaVotes are recorded in [`Data/README.md`](Data/README.md)

## Contributing

Corrections to the data are the most valuable contribution — particularly the missing 2009 Bahadurpura row, sourced to an ECI record. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

See [CITATION.cff](CITATION.cff).

## License

MIT — see [LICENSE](LICENSE).

---

**Note:** An independent analysis using official Election Commission results. Interpretations are the author's. Where a claim rests on a single secondary source rather than an ECI record, the data documentation says so.

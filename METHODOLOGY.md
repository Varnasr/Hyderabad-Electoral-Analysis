# Methodology

What was compared, how, and — most importantly — what the comparison can and cannot establish.

---

## The unit of analysis

One row per **constituency-year**: five seats across six assembly elections, 27 rows in total (28 expected; see [known gaps](Data/README.md#known-gaps)).

The measure throughout is **vote share as a percentage**, not absolute votes. That choice is worth being explicit about, because it determines what the series can show:

- Vote share answers *how the contest was divided*.
- It does not answer *how many people voted*, or whether a party's base grew or shrank.

A party can lose vote share while gaining votes if turnout rises around it. Nothing in this dataset distinguishes those two cases. Where a movement looks dramatic — Yakutpura 2023 is the obvious one — the absence of turnout and count data is a real limit on interpretation, not a detail.

## What was computed

| Measure | How | What it means |
|---|---|---|
| **Trend** | Vote share plotted by year, per party per seat | Direction of travel, nothing more |
| **Volatility** | Standard deviation of a party's vote share across the six cycles | How stable a party's support has been. High SD = swings, not necessarily weakness |
| **Growth** | 2023 share minus 1999 share | Net change across the period. Says nothing about the path taken between |
| **Comparative** | Cross-sectional ranking within a year | Who led where, in that cycle |

These are descriptive statistics. There is no regression, no control for any covariate, and no significance testing — because with six time points and five units, none of those would be meaningful.

## What this cannot establish

This section exists because the repository's earlier framing invited claims it cannot support.

**No causal claims.** Nothing here identifies the effect of anything on anything. If a seat has both long AIMIM incumbency and poor service delivery, this dataset cannot tell you whether one caused the other, whether a third factor drove both, or whether the association is coincidental. It contains no service-delivery data at all.

**No inference about voters.** Constituency-level results are aggregates. Reading individual or community-level voting behaviour off them is the [ecological fallacy](https://en.wikipedia.org/wiki/Ecological_fallacy), and it is a live risk in a district where constituency and community composition correlate. A seat's result tells you how that seat voted in aggregate. It does not tell you how any group within it voted.

**No pre/post-2009 continuity.** The 2008 delimitation redrew these boundaries. Bahadurpura did not exist before 2009. Comparing a 2004 result to a 2023 result in the "same" seat compares two different geographies wearing one name. Every cross-period claim in this repository carries that caveat implicitly; treat it as explicit.

**No statistical power.** Six observations per seat. Any apparent pattern is descriptive. Trends here are things to investigate, not findings to rest on.

**Not a complete account of the contest.** Rows sum to 80–90%, not 100%. Independents, smaller parties and NOTA are not captured. In close comparisons that residual can matter more than the gap being discussed.

## Data provenance and its limits

Primary source is the Election Commission of India. Figures have been spot-checked against Wikipedia constituency pages and IndiaVotes; those checks and their outcomes are recorded in [`Data/README.md`](Data/README.md).

Those cross-checks turned up **small discrepancies of well under a percentage point** — for example Bahadurpura 2014 records 78.46% here against 79.19% on Wikipedia. The most likely explanation is a different denominator (valid votes versus total votes polled, with or without postal ballots and NOTA). The dataset does not currently record which denominator it uses. Until it does, treat figures as accurate to roughly ±1 point and do not build an argument on a sub-1-point difference.

## How to use this responsibly

Defensible with this data:

- "AIMIM's vote share in Yakutpura fell from 45.8% in 2014 to 32.9% in 2023."
- "BJP went from not contesting Charminar in 2004 to 26.8% there in 2023."
- "Malakpet is the only one of these five seats where AIMIM has never exceeded 50%."

Not defensible with this data:

- Any statement about why a share moved.
- Any statement about how a community voted.
- Any statement connecting representation to service delivery or infrastructure outcomes.
- Any claim resting on a difference smaller than about a percentage point.

## Reproducing the figures

The dataset is a plain CSV and the report computes everything client-side in `index.html`. To recompute independently:

```bash
python3 -c "
import csv, statistics
rows = list(csv.DictReader(open('Data/HYD-DIST-RESULTS.csv')))
vals = [float(r['AIMIM_VoteShare']) for r in rows
        if r['ACNAME']=='YAKUTPURA' and r['AIMIM_VoteShare']]
print('Yakutpura AIMIM:', vals)
print('mean %.2f  sd %.2f' % (statistics.mean(vals), statistics.stdev(vals)))
"
```

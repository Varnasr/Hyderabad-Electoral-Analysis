# Data documentation

`HYD-DIST-RESULTS.csv` — party vote share by constituency and assembly election year, Hyderabad district.

## Dictionary

| Column | Type | Description |
|---|---|---|
| `YEAR` | integer | Assembly election year: 1999, 2004, 2009, 2014, 2018, 2023 |
| `ACNAME` | string | Assembly constituency, uppercase: BAHADURPURA, CHANDRAYANGUTTA, CHARMINAR, MALAKPET, YAKUTPURA |
| `AIMIM_VoteShare` | float | All India Majlis-e-Ittehadul Muslimeen, % |
| `TDP_VoteShare` | float | Telugu Desam Party, % |
| `MBT_VoteShare` | float | Majlis Bachao Tehreek, % |
| `INC_VoteShare` | float | Indian National Congress, % |
| `BJP_VoteShare` | float | Bharatiya Janata Party, % |
| `TRS_VoteShare` | float | Telangana Rashtra Samithi, renamed Bharat Rashtra Samithi (BRS) in 2022, % |

**Rows:** 27. **Coverage:** 1999–2023, six cycles.

## Reading the file correctly

**A blank cell means the party did not contest that seat that year. It does not mean zero.** Treating blanks as zeros will drag every average down and invent declines that did not happen. In Python: `pandas.read_csv(...)` gives `NaN`, which is correct — do not `fillna(0)`.

**Rows do not sum to 100%.** There is no column for independents, smaller parties, or NOTA. Totals typically land between 80% and 95%. The residual is real votes, not missing data.

**TRS and BRS are the same party.** Renamed in 2022. The column keeps the `TRS_` name across the whole series for continuity.

## Known gaps

### Bahadurpura, 2009 — missing row

The dataset jumps from no Bahadurpura rows (1999–2009) to a 2014 row. That is misleading. Bahadurpura was created in the **2008 delimitation and was contested in 2009**, won by **Mohammad Moazam Khan (AIMIM)**.

Consequence: any district-level aggregate for 2009 omits what is consistently AIMIM's strongest seat, and therefore **understates AIMIM in 2009**. Cross-cycle comparisons involving 2009 are affected.

**What has been recovered so far** (August 2026, secondary sources, two independent
results agreeing — not yet confirmed against an ECI record):

| Candidate | Party | Votes | Share |
|---|---|---|---|
| Mohammad Moazam Khan | AIMIM | 65,453 | 70.80% |
| Mir Ahmed Ali | **CPI** | 8,718 | 9.43% |

**Why the row is still not in the CSV.** The runner-up was **CPI**, which has no column in
this dataset. The schema carries AIMIM, TDP, MBT, INC, BJP and TRS only. Adding a row with
AIMIM at 70.80 and every other column blank would assert, under this file's own convention,
that INC, BJP, TDP and MBT *did not contest* Bahadurpura in 2009 — which is not established
and is probably false. A partial row would therefore corrupt the dataset rather than complete
it, and would do so silently.

This is itself a finding about the schema: the six tracked parties do not cover every serious
contender in these seats. In 2009 Bahadurpura the second-placed party is not represented at
all.

**To close this properly**, the row needs the full candidate list with each party's share,
from the ECI's *Statistical Report on the 2009 General Election to the Andhra Pradesh
Legislative Assembly* (constituency-wise detail, or the Form 20 for AC-69). Sources tried and
exhausted without success: Wikipedia (constituency and candidate pages — no 2009 table),
IndiaVotes, ElectionPandit (503), ResultUniversity (520), and the Indiastat constituency
factbook (a scanned PDF with no extractable text).

The pre-2009 absence of Bahadurpura is correct and expected — the seat did not exist.

### Turnout and absolute votes — not collected

The dataset holds shares only. Known 2023 turnout, for reference, not currently in the file:

| Constituency | 2023 turnout |
|---|---|
| Yakutpura | 39.64% |
| Malakpet | 41.32% |
| Charminar | 43.27% |
| Chandrayangutta | 45.26% |
| Bahadurpura | 45.50% |

These were the lowest in the state that cycle, which bears directly on how the 2023 shifts should be read.

## Cross-checks performed

Spot-checked August 2026 against Wikipedia constituency pages.

| Row | This dataset | Cross-check | Delta |
|---|---|---|---|
| Bahadurpura 2014, AIMIM | 78.46 | 79.19 | −0.73 |
| Bahadurpura 2018, AIMIM | 74.26 | 74.96 | −0.70 |
| Bahadurpura 2023, AIMIM | 62.02 | 62.24 | −0.22 |
| Bahadurpura 2023, TRS/BRS | 15.60 | 15.60 | 0.00 |

The consistent small negative delta points to a **denominator difference** — valid votes versus total votes polled — rather than transcription error. The dataset does not currently record which denominator was used. Until it does, treat values as accurate to about ±1 percentage point.

## Anomalies worth knowing

- **Malakpet 1999** — AIMIM blank, BJP 53.24%, INC 31.16%. The only cycle in the series where BJP led one of these seats outright.
- **Malakpet 2004** — INC 52.12%, its highest anywhere in the series. AIMIM did not field a candidate. Not a Congress surge; an uncontested lane.
- **Yakutpura 2023** — AIMIM 32.9%, MBT 32.2%. Effectively a tie, and the closest contest in the dataset. Reading AIMIM's fall here without MBT's rise misses the mechanism.

## Provenance

- **Primary:** Election Commission of India, constituency-level results — [eci.gov.in](https://eci.gov.in/)
- **Cross-check:** Wikipedia constituency pages; IndiaVotes
- **Compiled:** see [`../Docs/`](../Docs/)

## Contributing corrections

Cite an ECI record, note the denominator used, and say which row changes. Corrections to the 2009 Bahadurpura gap are especially welcome.

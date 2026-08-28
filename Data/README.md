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

**Rows do not sum to 100%.** There is no column for independents, smaller parties, or NOTA. The residual runs from 0 to 15.6 points with a median of 3.5; 21 of the 27 rows fall under 6 points, so totals typically land between 94% and 98%. The six largest residuals are Malakpet 1999 (15.6), Yakutpura 2023 (14.0), Yakutpura 2009 (13.6), Malakpet 2009 (12.6), Malakpet 2014 (8.4) and Chandrayangutta 2009 (7.8). The residual is real votes, not missing data.

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

---

# GHMC-WARD-AMENITIES-2011.csv

Census 2011 household amenities and assets for **108 GHMC wards** in Hyderabad
district. Used in [`../ANALYSIS.md`](../ANALYSIS.md).

## Dictionary

| Column | Description |
|---|---|
| `mandal` | Sub-district (tehsil) the ward sits in |
| `ward_no` | GHMC ward number |
| `old_city` | `yes` for the six old-city mandals — Bahadurpura, Charminar, Bandlaguda, Saidabad, Asifnagar, Golconda |
| `tap_water_treated` | % households, main drinking-water source is treated tap water |
| `water_within_premises` | % households, water source within premises |
| `closed_drainage` | % households, waste water to closed drainage |
| `bathroom_within_premises` | % households with a bathroom within premises |
| `lpg_png_cooking` | % households cooking on LPG/PNG |
| `avails_banking` | % households availing banking services |
| `computer_internet` | % households with a computer/laptop **with** internet |
| `car_jeep_van` | % households owning a car, jeep or van |
| `no_listed_assets` | % households with none of the listed assets |

All values are percentages of households in that ward.

## Provenance

Census of India 2011, **Houselisting & Housing Census, table HH-14** —
"Percentage of households to total households by amenities and assets", district
536 (Hyderabad), Andhra Pradesh as then constituted. Retrieved from the Census
release republished by [OpenCity](https://data.opencity.in/dataset/hyderabad-census-2011-data)
in August 2026 and reduced to the columns above; no values were altered.

## Reading it correctly

**Mandals are not assembly constituencies.** `old_city` marks the six mandals that
contain the five seats in `HYD-DIST-RESULTS.csv`, but the boundaries are not
identical. Any comparison using this flag is between parts of a city, not between
electorates.

**One time point.** Census 2011 pre-dates most of the 2014–2023 electoral period,
so this supports statements about *levels*, not about change over the period of
representation.

**Complete enumeration, not a sample.** There are no sampling errors on these
figures. Significance tests in `ANALYSIS.md` compare ward distributions between two
groups of wards, which is a different question from sampling uncertainty.

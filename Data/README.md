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
| `TURNOUT_PCT` | float | Share of registered electors who voted, %. 1999–2018 from the TCPD results file via SHRUG v2; 2023 from ECI figures as press-reported |
| `ELECTORS` | integer | Registered electors. 1999–2018 only (TCPD); blank for 2023, which TCPD has not yet published |
| `VALID_VOTES` | integer | Valid votes counted. 1999–2018 only (TCPD); blank for 2023 |

**Rows:** 28. **Coverage:** 1999–2023, six cycles.

Absolute votes for any party-row through 2018 can be recovered as
`VALID_VOTES × VoteShare / 100`, to within rounding of the published share.

## Reading the file correctly

**A blank cell means the party did not contest that seat that year. It does not mean zero.** Treating blanks as zeros will drag every average down and invent declines that did not happen. In Python: `pandas.read_csv(...)` gives `NaN`, which is correct — do not `fillna(0)`.

**Rows do not sum to 100%.** There is no column for independents, smaller parties, or NOTA. The residual runs from 0 to 15.9 points with a median of 3.6; 21 of the 28 rows fall under 6 points, so totals typically land between 94% and 98%. The six largest residuals are Bahadurpura 2009 (15.9, runner-up CPI), Malakpet 1999 (15.6), Yakutpura 2023 (14.0), Yakutpura 2009 (13.6), Malakpet 2009 (12.6) and Malakpet 2014 (8.4). The residual is real votes, not missing data.

**TRS and BRS are the same party.** Renamed in 2022. The column keeps the `TRS_` name across the whole series for continuity.

## Gaps closed in August 2026

### Bahadurpura, 2009 — recovered from TCPD

Earlier versions of this file had no 2009 Bahadurpura row, and refused to add a
partial one: the seat's runner-up was CPI, which has no column here, and it could
not be established which of the six tracked parties actually contested. Both
problems are resolved by the **TCPD candidates file (via SHRUG v2)**, which carries
the full field of 11 candidates for AC-69 in 2009 and matches the two secondary
sources recovered earlier to the vote:

| Candidate | Party | Votes | Share |
|---|---|---|---|
| Mohammad Moazam Khan | **AIMIM** | 65,453 | 70.80% |
| Mir Ahmed Ali | CPI | 8,718 | 9.43% |
| Syed Raza Hussain Azad | INC | 7,246 | 7.84% |
| Mohd Sirajuddin | BJP | 5,067 | 5.48% |
| (PRAP, SP, BSP, four independents) | | 5,970 | 6.45% |

TDP, MBT and TRS did **not** field candidates, so their blanks in the 2009
Bahadurpura row mean exactly what blanks mean everywhere else in the file. The
row's tracked shares sum to 84.1% — the largest residual in the dataset, because
the second-placed party sits outside the schema. That remains a finding about the
schema worth knowing when averaging.

The pre-2009 absence of Bahadurpura is correct and expected — the seat did not exist.

### Turnout and electorate — now collected

`TURNOUT_PCT`, `ELECTORS` and `VALID_VOTES` were added in August 2026. 1999–2018
come from the TCPD results file via SHRUG v2 (turnout there is total votes over
registered electors). The 2023 turnout figures are ECI numbers as press-reported —
39.64% (Yakutpura) to 45.50% (Bahadurpura), the five lowest in the state that
cycle, which bears directly on how the 2023 shifts should be read. TCPD has not
yet published the 2023 Telangana election, so 2023 `ELECTORS` and `VALID_VOTES`
are blank; they should be filled from the same file when a new TCPD vintage ships.

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
- **2009 Bahadurpura row, turnout, electors, valid votes:** TCPD candidates file via SHRUG v2 (Development Data Lab), Harvard Dataverse doi:10.7910/DVN/DPESAK
- **Cross-check:** Wikipedia constituency pages; IndiaVotes
- **Compiled:** see [`../Docs/`](../Docs/)

## Contributing corrections

Cite an ECI record, note the denominator used, and say which row changes.

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

---

# GHMC-WARD-PCA-2011.csv

Census 2011 ward-level Primary Census Abstract, reduced to literacy and
work-participation indicators for the same **108 GHMC wards** as the amenities file.
Used in the "Schooling and work" section of [`../ANALYSIS.md`](../ANALYSIS.md).

## Dictionary

| Column | Description |
|---|---|
| `mandal`, `ward_no`, `old_city` | As in `GHMC-WARD-AMENITIES-2011.csv` |
| `population` | Total ward population |
| `literacy_rate_7plus` | Literates as % of the age-7+ population |
| `female_literacy_rate_7plus` | Female literates as % of age-7+ females |
| `male_female_literacy_gap` | Male literacy rate minus female, percentage points |
| `wpr_all_ages` | Total workers as % of total population |
| `wpr_7plus` | Total workers as % of the age-7+ population |
| `female_wpr_all_ages` | Female workers as % of total females |
| `female_wpr_7plus` | Female workers as % of age-7+ females |
| `main_worker_share` | Main (non-marginal) workers as % of all workers |
| `child_share_0_6` | Age 0–6 population as % of total |
| `sc_share` | Scheduled Caste population as % of total |

## Derivation and provenance

Derived from the ward-level Primary Census Abstract for Hyderabad district
(Census of India 2011), republished by
[OpenCity](https://data.opencity.in/dataset/hyderabad-census-2011-data). Rates are
computed from the PCA counts (`P_LIT`, `TOT_WORK_P`, `P_06` and so on); no values
were taken from secondary tabulations. Mandal spellings were normalised to match
the amenities file (Ammerpet→ameerpet, Tirumalgiri→tirumalagiri,
Maredpally→maredpalle, Himayatnagar→himayathnagar, Golkonda→golconda); all 108
wards joined exactly.

The 7-plus denominators use the PCA's age-0–6 counts. Census convention computes
literacy over the age-7+ population; the same denominator is offered for work
participation because the old city's higher child share (13.0% vs 10.7%) would
otherwise depress its whole-population rate mechanically. Both variants are in the
file.

---

# GHMC-WARD-SLUMS.csv

GHMC slum-survey population aggregated to ward level, for the tenure-proxy
comparison in [`../ANALYSIS.md`](../ANALYSIS.md). **99 wards**, not 108: the eight
Tirumalagiri (Secunderabad Cantonment) wards and the Osmania University census-town
ward are outside GHMC's slum survey and outside its ward-numbering scheme, so they
are excluded rather than mis-joined.

## Dictionary

| Column | Description |
|---|---|
| `ward_no`, `mandal`, `old_city` | As in the other ward files |
| `n_slums` | GHMC-listed slums with this ward number |
| `slum_population` | Sum of surveyed slum population |
| `slum_households` | Sum of surveyed slum households |
| `ward_population_2011` | Census 2011 ward population (from the PCA file) |
| `slum_pop_share_pct` | slum_population / ward_population_2011 × 100 |
| `notified_pop_share_pct` | % of the ward's slum population in Notified (vs Non-Notified) slums |

## Provenance and join validation

Source: "Hyderabad - Slums" KML republished by
[OpenCity](https://data.opencity.in/dataset/hyderabad-slums) from GHMC — 1,351
polygons carrying slum name, notified status, ward number, households and
population; 1,268 have non-zero population. Survey year is not stated in the file;
GHMC's slum surveys date from the early 2010s.

The KML's ward numbers are GHMC's 150-ward scheme. Ward numbers 1–12 in that
scheme are north-eastern wards (Kapra–Uppal belt) outside Hyderabad district,
while the census files use Cantonment and census-town numbering for nine
low-numbered wards — a collision. The join was therefore validated by computing
each ward number's slum-polygon centroids: wards 18–19 land in Saidabad and match
the census rows; wards 1–8 land in the north-east and do not. Only the 99
unambiguous wards are included.

## Reading it correctly

**Mixed vintages.** Administrative survey population over 2011 Census
denominators; Yousufguda (ward 108) exceeds 100% as a result. Ward medians and
rank tests are robust to this; individual ward values are indicative.

**"Slum" is an administrative category.** GHMC listing reflects official
recognition as much as housing conditions. Under-notification in any area,
including the old city, cannot be ruled out from this data.

---

# AIMIM-CONTESTS-1999-2022.csv and AIMIM-CLOSE-CONTESTS-LIGHTS.csv

The close-election test described in `../ANALYSIS.md`, run in August 2026.

`AIMIM-CONTESTS-1999-2022.csv` — every general assembly election AIMIM contested
in the TCPD data (324 rows): state, constituency, year, whether AIMIM led, its
vote share, and its margin against the winner (negative) or runner-up (positive).
Bye-elections excluded. The similarly-abbreviated "All India
Majlis-E-Inquilab-E-Millat" is excluded as a different party.

`AIMIM-CLOSE-CONTESTS-LIGHTS.csv` — the 2014–2019 contests joined to VIIRS night
lights by post-2008 assembly constituency: `dlog` is the change in log annual
lights (mean of up to three post-election years minus mean of pre-years from 2012).

## Provenance

Election results: Trivedi Centre for Political Data (Lok Dhaba), as distributed in
**SHRUG v2** (Development Data Lab; Asher, Lunt, Matsuura and Novosad), Harvard
Dataverse doi:10.7910/DVN/DPESAK, files `trivedi_elections_clean` and
`trivedi_candidates_clean`; coverage ends 2022. Night lights: VIIRS annual
composites aggregated to `ac08_id` constituencies, same source, `viirs_annual_con08`
("average-masked" series), 2012–2021.

## Reading it correctly

The test's own diagnostics (in `../ANALYSIS.md`) matter more than its point
estimate: three treated constituencies, all high-baseline urban cores, permutation
p = 0.12, and a −0.40 correlation between baseline brightness and growth. It is
reported as an uninformative result, not as evidence in either direction.

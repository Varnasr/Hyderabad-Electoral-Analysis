# Hyderabad-Electoral-Analysis

Electoral and ward-level analysis of Hyderabad district, 1999 to 2023. Static
HTML pages plus the CSVs they describe, deployed to GitHub Pages.

## Commands

```bash
python3 tools/check_data.py     # data integrity, run by CI
python3 -m http.server 8000     # then open http://localhost:8000
```

## This repository is carefully documented. Read before changing data.

`data-notes.html` and `METHODOLOGY.md` are unusually good: they record
provenance, vintage mismatches and the reasoning behind each join, including one
the analysis had to resolve geometrically. Do not edit a CSV without checking
whether the prose describes it, and do not "fix" an anomaly the prose already
explains.

Two that look like errors and are not:

- **The slums file covers 99 wards, not 108.** GHMC's 150-ward KML numbers wards
  1 to 12 in the north-eastern Kapra and Uppal belt, outside Hyderabad district,
  while the census files use Cantonment and census-town numbering for nine
  low-numbered wards. The join was validated by computing slum-polygon
  centroids: wards 18 and 19 land in Saidabad and match, wards 1 to 8 land in
  the north-east and do not. The ambiguous wards are excluded rather than
  mis-joined. A check fails if that count moves.
- **Yousufguda (ward 108) exceeds a 100% slum share.** Administrative survey
  population over 2011 Census denominators. Ward medians and rank tests survive
  it; single ward values are indicative. A check fails if a second ward joins it.

## The key nobody wrote down

`ward_no` **alone is not unique.** Ward 1 appears twice: Musheerabad with a
population of 6,762, and Tirumalagiri with 28,700. Join the PCA and amenities
files on `ward_no` and those two rows pair silently, while 107 of 108 wards join
correctly, so the output looks right.

**The key is `(mandal, ward_no)`**, which is unique in all three ward files.

This is a different collision from the KML one above, which is between numbering
schemes rather than within a file. Both are live. Only the first was documented
before 2026-09-22, and `tools/check_data.py` now pins the second: one check
asserts the composite key is unique, and another asserts `ward_no` alone is
*still* ambiguous, so the warning cannot outlive the hazard.

## Watch out for

- **TURNOUT_PCT is `VALID_VOTES / ELECTORS`**, checked to within 0.05 points in
  every row. Strictly that is the valid-vote rate rather than turnout: for the
  1999 paper-ballot contests, rejected votes are excluded from the numerator.
  Worth stating if the figure is quoted outside this repository.
- **Bahadurpura was created in the 2008 delimitation** and correctly has no rows
  before 2009. A check fails if results appear for a constituency before it
  existed.
- **`won` and `margin` must agree in sign** in the AIMIM contest files. A win
  with a negative margin is a data entry error, and 324 contests are too many to
  eyeball.

## Testing

`.github/workflows/ci.yml` runs `tools/check_data.py` and a shape check over
every CSV. `static.yml` deploys to Pages and does not validate anything.

All eleven checks passed on first run. The ward-key and slums-coverage checks
were both fault-injected against real failures to confirm they bite.

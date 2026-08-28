# Sustained representation, sustained poverty

Hyderabad's old city has returned the same party for a generation. It is also
markedly poorer than the rest of its own district. This note sets out that
coincidence, and is careful about what it does and does not establish.

The finding that makes it worth writing down is **negative**: the old city is not
under-served. On every measure of municipal service delivery it is level with the
rest of Hyderabad district, and on two it is marginally ahead. The gap is
somewhere else entirely.

---

## The two facts

**Representation has been stable and one-sided.** AIMIM holds all five old-city
seats in this dataset and has held them across every cycle in which they existed —
1999 to 2023, six assembly elections. Vote shares run from 30% to 78%. No other
party has won one of these seats in the period covered.

**Household economic status is far below the rest of the district.** Census 2011
enumerated 108 GHMC wards in Hyderabad district. Comparing the 52 wards in the six
old-city mandals against the 56 elsewhere:

| Indicator | Old city | Rest of district | Gap | p |
|---|---|---|---|---|
| LPG/PNG for cooking | 55.9% | 77.1% | **−21.2** | <0.0001 |
| Household avails banking | 51.4% | 68.7% | **−17.3** | <0.0001 |
| Computer/laptop with internet | 9.1% | 20.0% | **−10.9** | <0.0001 |
| Car / jeep / van | 5.9% | 15.7% | **−9.8** | <0.0001 |

Ward medians; two-sided Mann–Whitney. Half the cooking-gas penetration, half the
internet, a third of the car ownership.

## The fact that reframes the argument

Set those against what a municipal corporation actually builds:

| Indicator | Old city | Rest of district | Gap | p |
|---|---|---|---|---|
| Tap water, treated source | 97.1% | 97.4% | −0.3 | 0.50 |
| Water source within premises | 94.8% | 94.5% | +0.3 | 0.10 |
| Waste water to closed drainage | 98.4% | 97.5% | **+0.9** | 0.07 |
| Bathroom within premises | 98.9% | 99.0% | −0.0 | 0.90 |

**Not one is significant. Two favour the old city.** The single worst-served ward in
the district on treated water (49.1%) and on closed drainage (49.8%) is *not* in the
old city.

Ward 43 in Bahadurpura is the clearest illustration: **22.0%** LPG — the lowest in
the district — alongside **92.9%** treated tap water and **95.6%** closed drainage.
Poor households on a well-served network.

So the pipes went in. What did not follow was income.

## What this supports, and what it does not

**Supported:** the old city has been represented by one party throughout, and is
substantially poorer than the rest of its district on every household economic
measure available. Those two things are true at once.

**Not supported — and the distinction is the whole point:**

*That AIMIM caused the poverty.* This is a coincidence of two long-run facts, not an
identified effect. Causal inference would need variation in representation, and there
is none — the party has won every one of these seats, every cycle.

*That the old city was denied infrastructure.* The data says the opposite. Anyone
arguing under-provision of municipal services will be refuted by the Census.

*That an MLA could have changed either.* Urban infrastructure in India runs through
the municipal corporation, state departments and centrally sponsored schemes. MLA-LADS
is around ₹3 crore a year — small against municipal capital budgets. Across this whole
period GHMC and the state were held by TDP, Congress, then TRS/BRS. **AIMIM has not
controlled the machinery that builds or funds any of this.** That cuts both ways: it
weakens a blame argument and it weakens a credit argument.

*That the direction runs one way.* Poor, dense, historically under-invested
neighbourhoods produce distinctive political attachments. Representation may be as much
consequence as cause. Nothing here separates the two.

## Why the reframing is the stronger argument

"The old city has no development" is refutable in one afternoon with this Census
table, and it aims at the one thing an MLA has least control over.

"A generation of unbroken representation has coincided with a generation of
unchanged relative poverty, in a place where the pipes and drains were built"
is a harder claim to dismiss, and a more interesting one. It moves the question from
civic works — where the old city is doing fine — to economic mobility, where the
gap is large, consistent across four independent indicators, and statistically
unambiguous.

It also raises the question worth actually asking: **what would have had to be
different?** If service delivery is level and outcomes are not, the binding
constraint is somewhere other than pipes — land title, credit access, formal
employment, education. Those are answerable questions, and none of them is settled
by a vote-share chart.

## Limits of this analysis

**Census 2011 is one time point, now fifteen years old.** It pre-dates most of the
2014–2023 period. The word "sustained" on the poverty side is doing more work than
one census can carry; establishing it properly needs Census 2001 ward tables, or
Census 2027 when it lands.

**Mandals are not constituencies.** The six old-city mandals approximate the five
assembly seats; the boundaries are not identical. The comparison is between parts
of a city, not between electorates.

**These are levels, not change.** Levels largely record history. A poor area in 2011
may have been poor in 1951. Detecting whether representation changed a trajectory
needs at least two time points, which this does not have.

**No controls.** Old-city wards differ from the rest in density, housing-stock age,
unauthorised construction and land-title status — all of which predict economic
outcomes independently of who represents them.

## Reproducing it

Data: [`Data/GHMC-WARD-AMENITIES-2011.csv`](Data/GHMC-WARD-AMENITIES-2011.csv) — 108
GHMC wards, Census 2011 table HH-14 (Houselisting & Housing Census), percentage of
households by amenity and asset. Extracted from the Census of India release
republished by [OpenCity](https://data.opencity.in/dataset/hyderabad-census-2011-data).

`old_city = yes` marks wards in the Bahadurpura, Charminar, Bandlaguda, Saidabad,
Asifnagar and Golconda mandals.

```bash
python3 - <<'EOF'
import csv, statistics as st
rows=list(csv.DictReader(open('Data/GHMC-WARD-AMENITIES-2011.csv')))
old =[r for r in rows if r['old_city']=='yes']
rest=[r for r in rows if r['old_city']=='no']
for k in ['tap_water_treated','closed_drainage','lpg_png_cooking','avails_banking']:
    a=st.median(float(r[k]) for r in old); b=st.median(float(r[k]) for r in rest)
    print(f"{k:26} old {a:5.1f}   rest {b:5.1f}   gap {a-b:+5.1f}")
EOF
```

Significance is a two-sided Mann–Whitney U on the ward distributions — a rank test,
chosen because ward percentages are bounded and skewed rather than normal.

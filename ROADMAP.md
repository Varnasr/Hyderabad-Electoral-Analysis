# Open questions, and what would close them

This site has taken the question — a generation of AIMIM wins, a generation of
old-city poverty, does one explain the other? — as far as public data currently
allows. The record is established, the poverty is measured at ward level, the
easy explanations are eliminated, and the one formal causal test that could be
run came back uninformative. What follows is the work that would move the
argument further, in rough order of how much each item would add, and what each
one is waiting on.

If you can supply any of the missing pieces, open an issue or a pull request on
[GitHub](https://github.com/Varnasr/Hyderabad-Electoral-Analysis).

## 1. The delimitation experiment — the one that matters

The 2008 boundary redraw moved wards between assembly constituencies without
anyone in those wards changing how they voted. Wards that moved into or out of
AIMIM-held seats, compared before and after on the 2001 and 2011 censuses, would
be the cleanest test of representation effects available for this question —
far stronger than the national close-contest design, which had only three
usable bare wins.

**Blocked on:** a ward-boundary crosswalk between the 2001 and 2011 census
wards for Hyderabad. None is public. The pieces that would unblock it are the
2001 municipal ward maps (on paper in MCH/GHMC records) and the delimitation
notification assigning localities to the new constituencies. Digitising the two
and matching them is a bounded project — GIS skills and a focused week — and it
would be a genuine contribution to the literature, not just to this site. The
design is set out in [the full analysis](ANALYSIS.md).

## 2. Refresh the causal test when the data catches up

The close-contest test used TCPD election results through 2022 and VIIRS night
lights through 2021. The 2023 Telangana and 2024 Maharashtra elections both had
AIMIM contesting widely and would add contests — possibly new near-ties, which
is what the design is starved of.

**Waiting on:** the next TCPD/SHRUG data release. Nothing to do until it ships;
worth checking the Harvard Dataverse a couple of times a year. The same release
would fill the blank 2023 `ELECTORS` and `VALID_VOTES` cells in the election
file.

## 3. What the corporators actually spent

MP and MLA funds are small — roughly ₹250 a head over a full term. The money
that builds a neighbourhood is the GHMC ward budget, and ward-wise capital
works and spending are not published anywhere. A decade of ward-wise works data
would answer a question nothing public can touch: are old-city wards underfunded
per head, or funded and still poor?

**Needs:** an RTI to GHMC (works and town-planning wings) from an applicant in
Telangana, asking for ward-wise capital expenditure, ideally 2016 onwards.

## 4. MPLADS by party, as a series

The MPLADS portal publishes MP-wise detail only from 2023–24; before that, the
public record is aggregate. MP-wise utilisation for earlier terms exists in
annexures to Lok Sabha questions. Assembling those would turn the funds section
from a handful of press-reported figures into a proper by-party series.

**Needs:** patience with the Lok Sabha question archive, or an RTI to the
Ministry of Statistics, which administers the scheme.

## 5. Date the slum survey

The GHMC slum list used for the ward-level slum shares carries no survey year;
this site calls it "early 2010s" and treats it as a single time point. A records
request to GHMC's Urban Community Development wing would pin the year down and
say whether a newer round exists.

## 6. A second post-2011 anchor

The updated ward estimates rest on NFHS-5 (2019–21) plus one stated assumption
about banking. NFHS-6, whenever fieldwork happens, would add measured anchors
for more indicators. And the next census — expected around 2027 — will replace
the 2011 ward base entirely; when its ward tables publish, every level on this
site can be re-estimated rather than projected.

---

**Closed since launch** (August 2026): the missing Bahadurpura 2009 row,
recovered in full from the TCPD candidates file, and turnout, electorate and
valid-vote columns for 1999–2023 — details in [the data notes](Data/README.md).

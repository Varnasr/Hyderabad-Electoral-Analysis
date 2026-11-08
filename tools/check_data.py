#!/usr/bin/env python3
"""Integrity checks for the Hyderabad electoral and ward datasets.

The repository had no CI beyond the Pages deploy, so nothing held the data to
the claims `data-notes.html` and `METHODOLOGY.md` make about it. Everything here
passes today. The point is the ones that would break quietly.

The sharpest is the ward key. `ward_no` alone is **not unique**: ward 1 appears
twice, once in Musheerabad with 6,762 people and once in Tirumalagiri with
28,700. A join on `ward_no` between the PCA and amenities files silently pairs
those two rows, and 107 of 108 wards join correctly, so the result looks right.
The key is `(mandal, ward_no)`.

That is a different collision from the one `data-notes.html` already documents,
which is between GHMC's 150-ward KML scheme and the Cantonment and census-town
numbering used for nine low-numbered wards, and which the slums join resolves
with polygon centroids. Both are live; only one was written down.

Run:  python3 tools/check_data.py
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "Data"

failures = []


def check(name, fn):
    try:
        note = fn()
        print(f"  ok    {name}" + (f" ({note})" if note else ""))
    except AssertionError as e:
        failures.append(name)
        print(f"  FAIL  {name}\n        {e}")


def load(name):
    with open(D / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


results = load("HYD-DIST-RESULTS.csv")
pca = load("GHMC-WARD-PCA-2011.csv")
amen = load("GHMC-WARD-AMENITIES-2011.csv")
slums = load("GHMC-WARD-SLUMS.csv")

wkey = lambda r: (r["mandal"].strip().lower(), r["ward_no"].strip())

# ---------------------------------------------------------------- results

def _shares():
    over = []
    for r in results:
        s = sum(float(r[c]) for c in r if c.endswith("VoteShare") and r[c].strip())
        if s > 100.01:
            over.append(f"{r['YEAR']} {r['ACNAME']} = {s:.2f}")
    assert not over, "vote shares exceed 100: " + "; ".join(over)
    return f"{len(results)} contests, all under 100 with the remainder as others and NOTA"
check("constituency vote shares are internally possible", _shares)


def _turnout():
    bad = []
    for r in results:
        if r["ELECTORS"].strip() and r["VALID_VOTES"].strip():
            calc = 100 * float(r["VALID_VOTES"]) / float(r["ELECTORS"])
            if abs(calc - float(r["TURNOUT_PCT"])) > 0.05:
                bad.append(f"{r['YEAR']} {r['ACNAME']}: stated {r['TURNOUT_PCT']}, computes {calc:.2f}")
    assert not bad, "; ".join(bad)
    return "TURNOUT_PCT equals VALID_VOTES / ELECTORS in every row"
check("turnout recomputes from its own columns", _turnout)


def _delimitation():
    """Bahadurpura was created in the 2008 delimitation and cannot appear before 2009."""
    early = [r for r in results if r["ACNAME"] == "BAHADURPURA" and int(r["YEAR"]) < 2009]
    assert not early, f"Bahadurpura has rows before 2009: {[r['YEAR'] for r in early]}"
    years = sorted({r["YEAR"] for r in results})
    return f"{len(set(r['ACNAME'] for r in results))} constituencies across {', '.join(years)}"
check("no constituency has results before it existed", _delimitation)

# ---------------------------------------------------------------- wards

def _composite_key():
    for name, rows in (("PCA", pca), ("amenities", amen), ("slums", slums)):
        c = Counter(wkey(r) for r in rows)
        dupes = [k for k, v in c.items() if v > 1]
        assert not dupes, f"{name}: (mandal, ward_no) repeats for {dupes}"
    return "(mandal, ward_no) is unique in all three ward files"
check("the ward key is the mandal and the number together", _composite_key)


def _ward_no_is_not_a_key():
    """Pinned deliberately. If this ever passes, the hazard is gone and the
    warning in CLAUDE.md and the module docstring should go with it."""
    by_num = {}
    for r in pca:
        by_num.setdefault(r["ward_no"].strip(), set()).add(r["mandal"].strip().lower())
    clashes = {n: sorted(m) for n, m in by_num.items() if len(m) > 1}
    assert clashes, ("ward_no is now unique across mandals. Remove this check and "
                     "the warnings that depend on it.")
    return f"ward_no {list(clashes)[0]} still spans {clashes[list(clashes)[0]]}, so joins need the mandal"
check("ward_no alone remains ambiguous, as documented", _ward_no_is_not_a_key)


def _pca_amenities_align():
    kp, ka = {wkey(r) for r in pca}, {wkey(r) for r in amen}
    assert kp == ka, f"PCA and amenities disagree on {sorted(kp ^ ka)}"
    return f"{len(kp)} wards, identical in both"
check("PCA and amenities cover exactly the same wards", _pca_amenities_align)


def _slums_subset():
    kp, ks = {wkey(r) for r in pca}, {wkey(r) for r in slums}
    extra = ks - kp
    assert not extra, f"slums rows with no census ward: {sorted(extra)}"
    assert len(ks) == 99, (
        f"the slums file now covers {len(ks)} wards, not the 99 data-notes.html "
        f"describes as unambiguous after the centroid validation. Update the prose "
        f"if this was deliberate."
    )
    return f"{len(ks)} of {len(kp)} wards, the rest excluded rather than mis-joined"
check("slums coverage matches the documented 99 unambiguous wards", _slums_subset)


def _old_city_consistent():
    flags = {}
    for rows in (pca, amen, slums):
        for r in rows:
            k = wkey(r)
            v = r["old_city"].strip().lower()
            if k in flags and flags[k] != v:
                raise AssertionError(f"{k} is old_city={flags[k]} in one file and {v} in another")
            flags[k] = v
    return f"{sum(1 for v in flags.values() if v == 'yes')} old-city wards, agreeing across files"
check("the old_city flag agrees across all three ward files", _old_city_consistent)


def _shares_are_percentages():
    bad = []
    for r in pca:
        for c in ("literacy_rate_7plus", "female_literacy_rate_7plus", "sc_share",
                  "child_share_0_6", "main_worker_share"):
            if r[c].strip() and not (0 <= float(r[c]) <= 100):
                bad.append(f"{wkey(r)} {c}={r[c]}")
    assert not bad, "; ".join(bad[:6])
check("census percentage columns stay within 0 to 100", _shares_are_percentages)


def _slum_share_note():
    """Yousufguda exceeds 100% because administrative slum counts sit over 2011
    Census denominators. data-notes.html says so; this keeps the exception from
    quietly spreading."""
    over = [(wkey(r), float(r["slum_pop_share_pct"])) for r in slums
            if r["slum_pop_share_pct"].strip() and float(r["slum_pop_share_pct"]) > 100]
    assert len(over) <= 1, (
        f"{len(over)} wards now exceed 100% slum share, not the single documented "
        f"case: {over}"
    )
    return (f"{len(over)} ward over 100%, the documented mixed-vintage case"
            if over else "no ward over 100%")
check("the mixed-vintage overflow stays confined to its documented case", _slum_share_note)

# ---------------------------------------------------------------- AIMIM

def _aimim():
    contests = load("AIMIM-CONTESTS-1999-2022.csv")
    lights = load("AIMIM-CLOSE-CONTESTS-LIGHTS.csv")
    bad = [r for r in contests if r["won"].strip() not in ("0", "1")]
    assert not bad, f"won is not a 0/1 flag in {len(bad)} rows"
    wins = [r for r in contests if r["won"] == "1"]
    neg = [r for r in wins if r["margin"].strip() and float(r["margin"]) < 0]
    assert not neg, f"{len(neg)} contests marked won with a negative margin"
    losses = [r for r in contests if r["won"] == "0" and r["margin"].strip()]
    pos = [r for r in losses if float(r["margin"]) > 0]
    assert not pos, f"{len(pos)} contests marked lost with a positive margin"
    return f"{len(contests)} contests, {len(wins)} won, {len(lights)} in the close-contest subset"
check("AIMIM win flags and margins agree in sign", _aimim)

# ---------------------------------------------------------------- page head

def _page_heads():
    import re
    base = "https://varnasr.github.io/Hyderabad-Electoral-Analysis/"
    pages = sorted(ROOT.glob("*.html"))
    assert pages, "no pages found"
    for f in pages:
        s = f.read_text(encoding="utf-8")
        url = base + ("" if f.name == "index.html" else f.name)
        canon = re.findall(r'<link rel="canonical" href="([^"]*)"', s)
        assert canon == [url], f"{f.name}: canonical is {canon}, expected {[url]}"
        for prop, want in (("og:url", url), ("og:type", "website")):
            got = re.findall(r'<meta property="%s" content="([^"]*)"' % prop, s)
            assert got == [want], f"{f.name}: {prop} is {got}"
        title = re.search(r"<title>(.*?)</title>", s).group(1)
        got = re.findall(r'<meta property="og:title" content="([^"]*)"', s)
        assert got == [title], f"{f.name}: og:title does not match the title"
        desc = re.search(r'<meta name="description" content="([^"]*)"', s)
        got = re.findall(r'<meta property="og:description" content="([^"]*)"', s)
        assert got == ([desc.group(1)] if desc else []), f"{f.name}: og:description does not match the description"
        assert 'name="twitter:card" content="summary_large_image"' in s, f"{f.name}: twitter:card is not summary_large_image"
    return f"{len(pages)} pages carry a canonical and Open Graph tags that match their own title and description"
check("every page names its own address and previews as its own title", _page_heads)

# ---------------------------------------------------------------- share card

def _jpeg_or_png_size(data):
    """Width and height of a JPEG or PNG from its own bytes, or None."""
    import struct
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:3] == b"\xff\xd8\xff":
        i = 2
        while i + 9 < len(data):
            assert data[i] == 0xFF, "damaged JPEG"
            marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + length
    return None


def _share_card():
    import re
    base = "https://varnasr.github.io/Hyderabad-Electoral-Analysis/"
    pages = sorted(ROOT.glob("*.html"))
    for f in pages:
        s = f.read_text(encoding="utf-8")
        got = re.findall(r'<meta property="og:image" content="([^"]*)"', s)
        assert len(got) == 1 and got[0].startswith(base), f"{f.name}: og:image is {got}, expected one address under {base}"
        assert re.findall(r'<meta name="twitter:image" content="([^"]*)"', s) == got, f"{f.name}: twitter:image differs from og:image"
        assert re.findall(r'<meta property="og:image:width" content="([^"]*)"', s) == ["1200"], f"{f.name}: og:image:width is not 1200"
        assert re.findall(r'<meta property="og:image:height" content="([^"]*)"', s) == ["630"], f"{f.name}: og:image:height is not 630"
        assert re.search(r'<meta property="og:image:alt" content="[^"]+"', s), f"{f.name}: no og:image:alt"
    path = ROOT / got[0][len(base):]
    assert path.is_file(), f"{got[0]} has no file at {path.relative_to(ROOT)}"
    data = path.read_bytes()
    assert len(data) <= 250_000, f"{path.name} is {len(data)} bytes; WhatsApp drops previews over about 250 KB"
    size = _jpeg_or_png_size(data)
    assert size, f"{path.name} is not a JPEG or PNG (LinkedIn does not read WebP)"
    assert size == (1200, 630), f"{path.name} is {size[0]}x{size[1]}, the tags say 1200x630"
    return f"{len(pages)} pages point at {path.name}, {len(data)} bytes, {size[0]}x{size[1]}"
check("every page previews with a JPEG or PNG card that exists, within 250 KB", _share_card)

print()
if failures:
    print(f"FAIL - {len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("PASS - all checks passed")

#!/usr/bin/env python3
"""Regenerate analysis.html, methodology.html and data-notes.html from the
markdown sources, styled like the main report. Run from the repo root:
    python3 tools/build_docs.py
"""
import markdown, io, re, sys, os

PAGES = [
    ("ANALYSIS.md",    "analysis.html",    "The full analysis"),
    ("METHODOLOGY.md", "methodology.html", "Methodology and limits"),
    ("Data/README.md", "data-notes.html",  "Data notes and dictionaries"),
    ("ROADMAP.md",     "roadmap.html",     "What comes next"),
]

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Hyderabad's old city, 1999–2023</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; }}
:root {{
    --paper:#f7f3ec; --surface:#fdfbf7; --ink:#211d16; --muted:#6e675a;
    --rule:#ddd5c6; --rule-strong:#b8ae9a; --accent:#a84b2f;
}}
@media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
        --paper:#151310; --surface:#1d1a16; --ink:#ece6d9; --muted:#a09786;
        --rule:#3a352c; --rule-strong:#554e40; --accent:#e08a5f;
    }}
}}
:root[data-theme="dark"] {{
    --paper:#151310; --surface:#1d1a16; --ink:#ece6d9; --muted:#a09786;
    --rule:#3a352c; --rule-strong:#554e40; --accent:#e08a5f;
}}
body {{
    margin:0; background:var(--paper); color:var(--ink);
    font-family:'Newsreader','Iowan Old Style',Georgia,serif;
    font-size:18px; line-height:1.65; -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:860px; margin:0 auto; padding:0 24px 80px; }}
.top {{
    position:sticky; top:0; background:var(--paper); border-bottom:1px solid var(--rule);
    font-family:'IBM Plex Sans',system-ui,sans-serif; font-size:13px; z-index:10;
}}
.top-in {{ max-width:860px; margin:0 auto; padding:14px 24px; }}
.top a {{ color:var(--muted); text-decoration:none; }}
.top a:hover {{ color:var(--ink); }}
h1 {{ font-size:clamp(1.9rem,5vw,2.7rem); font-weight:500; line-height:1.1;
     letter-spacing:-.015em; margin:44px 0 8px; }}
.subtitle {{ font-family:'IBM Plex Sans',system-ui,sans-serif; font-size:13px;
     color:var(--muted); margin-bottom:36px; }}
h2 {{ font-size:1.45rem; font-weight:500; letter-spacing:-.01em; margin:44px 0 12px;
     padding-top:26px; border-top:1px solid var(--rule); }}
h3 {{ font-size:1.1rem; font-weight:500; margin:30px 0 8px; }}
p, li {{ max-width:70ch; }}
a {{ color:var(--accent); }}
strong {{ font-weight:600; }}
blockquote {{ margin:20px 0; padding:2px 22px; border-left:3px solid var(--accent);
     color:var(--muted); font-style:italic; }}
table {{ border-collapse:collapse; width:100%; margin:20px 0;
     font-family:'IBM Plex Sans',system-ui,sans-serif; font-size:13.5px;
     font-feature-settings:"tnum" 1; background:var(--surface); }}
th, td {{ padding:8px 12px; border-bottom:1px solid var(--rule); text-align:left; }}
thead th {{ font-size:10.5px; text-transform:uppercase; letter-spacing:.07em;
     color:var(--muted); border-bottom:1px solid var(--rule-strong); }}
.table-scroll {{ overflow-x:auto; border:1px solid var(--rule); border-radius:10px; }}
.table-scroll table {{ margin:0; }}
code {{ font-family:ui-monospace,'SF Mono',Menlo,monospace; font-size:.85em;
     background:var(--surface); border:1px solid var(--rule); border-radius:4px;
     padding:1px 5px; }}
pre {{ background:var(--surface); border:1px solid var(--rule); border-radius:10px;
     padding:16px 18px; overflow-x:auto; font-size:13px; line-height:1.5; }}
pre code {{ border:none; background:none; padding:0; }}
hr {{ border:none; border-top:1px solid var(--rule); margin:40px 0; }}
.footer {{
    margin-top: 76px; border-top: 1px solid var(--rule); padding: 26px 0 60px;
    font-size: 13px; color: var(--muted); line-height: 1.65;
    font-family:'IBM Plex Sans',system-ui,sans-serif;
}}
.footer p {{ margin: 0 0 .6em; max-width: 74ch; }}
.footer a {{ color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }}
</style>
</head>
<body>
<div class="top"><div class="top-in"><a href="index.html{backhash}">&larr; Back to the report</a></div></div>
<div class="wrap">
<h1>{title}</h1>
<p class="subtitle">Part of <a href="index.html">Hyderabad&rsquo;s old city, 1999&ndash;2023</a> &middot; source file: <a href="{src}">{src}</a></p>
{body}
<footer class="footer">
    <p>Need help setting out your story, what sets your work apart, the context, the return on investment and the projections? Pinpoint Ventures can help. Write to <a href="mailto:hello@pinpointventures.in?subject=Enquiry%20from%20varnasr.github.io/Hyderabad-Electoral-Analysis">hello@pinpointventures.in</a> or message on <a href="https://wa.me/919871777110?text=Hi%20Pinpoint%20Ventures%2C%20I%20found%20you%20through%20varnasr.github.io/Hyderabad-Electoral-Analysis.%20I%27d%20like%20to%20discuss%20a%20research%20or%20advisory%20engagement." target="_blank" rel="noopener">WhatsApp</a>.</p>
</footer>
</div>
</body>
</html>
"""

def fix_links(html, src):
    # md cross-links -> the generated pages; keep CSVs and PDFs as-is
    repl = {
        "ANALYSIS.md": "analysis.html", "METHODOLOGY.md": "methodology.html",
        "ROADMAP.md": "roadmap.html",
        "Data/README.md": "data-notes.html", "../ANALYSIS.md": "analysis.html",
        "README.md": "data-notes.html" if src.startswith("Data/") else "README.md",
    }
    for a, b in repl.items():
        html = html.replace('href="%s' % a, 'href="%s' % b)
    if src.startswith("Data/"):
        # paths inside Data/README.md are relative to Data/
        html = re.sub(r'href="(?!https?://|#|[a-z-]+\.html)([A-Za-z0-9_.-]+\.(?:csv|pdf))"',
                      r'href="Data/\1"', html)
        html = html.replace('href="../Docs/', 'href="Docs/')
        html = html.replace('href="analysis.html#', 'href="analysis.html#')
    return html

def wrap_tables(html):
    return html.replace(
        "<table>",
        '<div class="table-scroll" tabindex="0" role="region" aria-label="Table, scrolls horizontally"><table>'
    ).replace("</table>", "</table></div>")

def scroll_code(html):
    return html.replace("<pre><code", '<pre tabindex="0" role="region" aria-label="Code, scrolls horizontally"><code')

def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    for src, out, title in PAGES:
        md = io.open(src, encoding="utf-8").read()
        body = markdown.markdown(md, extensions=["tables", "fenced_code", "toc"])
        body = scroll_code(wrap_tables(fix_links(body, src)))
        io.open(out, "w", encoding="utf-8").write(
            SHELL.format(title=title, body=body, src=src, backhash=""))
        print("built", out, len(body), "bytes")

if __name__ == "__main__":
    main()

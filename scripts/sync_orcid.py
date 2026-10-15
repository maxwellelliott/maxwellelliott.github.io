"""Add new papers from Maxwell Elliott's ORCID record to publications/index.html.

Run weekly by .github/workflows/orcid-sync.yml, or by hand from the repo root:

    python3 scripts/sync_orcid.py

It only ever adds papers (or swaps a preprint for its published version); it never deletes
anything, because the page also lists papers that aren't in ORCID. ORCID entries that should
stay off the page go in scripts/orcid-skip.txt, one DOI per line.
"""

import html
import json
import os
import re
import sys
import urllib.request

ORCID_ID = "0000-0003-1083-6277"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "publications", "index.html")
HOME = os.path.join(ROOT, "index.html")
SKIP = os.path.join(ROOT, "scripts", "orcid-skip.txt")

# Preprint servers by DOI prefix, for the "Preprint, <server>" venue label.
PREPRINT_SERVERS = {
    "10.1101/": None,  # bioRxiv or medRxiv: ORCID's journal title says which
    "10.21203/": "Research Square",
    "10.31234/": "PsyArXiv",
    "10.2139/": "SSRN",
    "10.64898/": "medRxiv",
}
NAMED_SERVERS = {"biorxiv": "bioRxiv", "medrxiv": "medRxiv"}


def fetch_works():
    req = urllib.request.Request(
        f"https://pub.orcid.org/v3.0/{ORCID_ID}/works", headers={"Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    works = []
    for group in data["group"]:
        s = group["work-summary"][0]
        ids = {e["external-id-type"]: e["external-id-value"] for e in group["external-ids"]["external-id"]}
        year = ((s.get("publication-date") or {}).get("year") or {}).get("value")
        journal = ((s.get("journal-title") or {}) or {}).get("value")
        works.append({
            "doi": ids.get("doi"),
            "title": s["title"]["title"]["value"],
            "journal": journal,
            "type": s["type"],
            "year": int(year) if year else None,
        })
    return works


def norm(title):
    """Compare titles ignoring case, punctuation and markup."""
    text = html.unescape(re.sub(r"<[^>]+>", "", title))
    return re.sub(r"[^a-z0-9]", "", text.lower())


def preprint_server(work):
    doi = work["doi"].lower()
    for prefix, name in PREPRINT_SERVERS.items():
        if doi.startswith(prefix):
            return name or NAMED_SERVERS.get((work["journal"] or "").lower(), "bioRxiv")
    return None


def venue(work):
    server = preprint_server(work)
    if work["type"] != "journal-article" and server:
        return f"Preprint, {server}"
    return work["journal"] or ("Preprint" if work["type"] == "preprint" else "")


def entry(work):
    doi = html.escape(work["doi"])
    title = html.escape(html.unescape(re.sub(r"<[^>]+>", "", work["title"])).strip())
    return (
        '          <li class="paper">\n'
        f'            <p class="paper__title"><a href="https://doi.org/{doi}">{title}</a></p>\n'
        f'            <p class="paper__venue"><i>{html.escape(venue(work))}</i><span class="mono">doi:{doi}</span></p>\n'
        "          </li>\n"
    )


def page_entries(page):
    """Each paper on the page: its full <li> text, DOI (lowercase, or None) and normalized title."""
    out = []
    for m in re.finditer(r'^[ \t]*<li class="paper">.*?</li>\n', page, re.S | re.M):
        block = m.group(0)
        doi = re.search(r'href="https://doi.org/([^"]+)"', block)
        title = re.search(r'<p class="paper__title">(.*?)</p>', block, re.S)
        venue_text = re.search(r'<p class="paper__venue"><i>([^<]*)', block)
        out.append({
            "block": block,
            "doi": doi.group(1).lower() if doi else None,
            "title": norm(title.group(1)) if title else "",
            "preprint": bool(venue_text and venue_text.group(1).startswith("Preprint")),
        })
    return out


def insert(page, work):
    """Put the paper at the top of its year, adding the year section if it's new."""
    year = work["year"]
    opening = re.search(rf'<section class="year-group" id="y{year}".*?<ol class="paper-list">\n', page, re.S)
    if opening:
        return page[: opening.end()] + entry(work) + page[opening.end():]
    section = (
        f'      <section class="year-group" id="y{year}" data-year="{year}" aria-labelledby="y{year}-h">\n'
        f'        <h2 id="y{year}-h">{year}</h2>\n'
        '        <ol class="paper-list">\n'
        f"{entry(work)}"
        "        </ol>\n"
        "      </section>\n"
    )
    # Before the first existing year that is older than this one, else after the last.
    for m in re.finditer(r'[ \t]*<section class="year-group" id="y(\d+)"', page):
        if int(m.group(1)) < year:
            return page[: m.start()] + section + page[m.start():]
    last = [m.end() for m in re.finditer(r"</section>\n", page)][-1]
    return page[:last] + section + page[last:]


def main():
    works = fetch_works()
    page = open(PAPERS, encoding="utf-8").read()
    skip = set()
    if os.path.exists(SKIP):
        for line in open(SKIP, encoding="utf-8"):
            line = line.split("#", 1)[0].strip().lower()
            if line:
                skip.add(line)

    report = []
    # Published versions first, so a paper whose preprint and article both appear lands as the article.
    for work in sorted(works, key=lambda w: w["type"] != "journal-article"):
        if not work["doi"] or not work["year"]:
            continue
        doi = work["doi"].lower()
        entries = page_entries(page)
        if doi in skip or any(e["doi"] == doi for e in entries):
            continue
        same = [e for e in entries if e["title"] and e["title"] == norm(work["title"])]
        if same:
            old = same[0]
            if work["type"] == "journal-article" and old["preprint"]:
                page = page.replace(old["block"], "", 1)
                page = insert(page, work)
                report.append(f"Replaced preprint with published version: {work['title']} ({work['doi']})")
            # Otherwise it's another version of a paper already listed; leave the page alone.
            continue
        page = insert(page, work)
        report.append(f"Added: {work['title']} ({work['year']}, {work['doi']})")

    # Keep the paper counts in the page intro and on the home page in step with the list.
    total = len(page_entries(page))
    page = re.sub(r"<p>\d+ journal articles and recent preprints", f"<p>{total} journal articles and recent preprints", page)
    open(PAPERS, "w", encoding="utf-8").write(page)
    home = open(HOME, encoding="utf-8").read()
    open(HOME, "w", encoding="utf-8").write(re.sub(r"All \d+ papers", f"All {total} papers", home))

    on_page = {e["doi"] for e in page_entries(page) if e["doi"]}
    in_orcid = {w["doi"].lower() for w in works if w["doi"]}
    missing = sorted(on_page - in_orcid)

    lines = ["## ORCID sync", ""]
    lines += [f"- {r}" for r in report] or ["- No new papers."]
    if missing:
        lines += ["", "On the website but not in ORCID (left as is; add them to ORCID if they belong there):", ""]
        lines += [f"- {d}" for d in missing]
    text = "\n".join(lines) + "\n"
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    sys.exit(main())

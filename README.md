# maxwellelliott.github.io

Source for Maxwell Elliott's academic website, live at **https://maxwellelliott.github.io**.

It's a plain static site: hand-written HTML, one stylesheet, one script. There is no build
step, no framework, and nothing to install. Whatever is on the `master` branch is what
GitHub Pages serves, usually within a minute or two of a push.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Home page (research, recent papers, contact) |
| `publications/index.html` | Full publication list |
| `about/index.html` | About me (bio) |
| `news/index.html` | Lab news |
| `join/index.html` | Recruiting / how to join the lab |
| `assets/site.css` | All styles, including dark mode |
| `assets/site.js` | Dark-mode switch, phone menu, papers chart, Altmetric scores |
| `images/` | Images hosted on this site (e.g. `headshot.jpeg`) |
| `files/` | PDFs (old CV links point here, so keep these paths stable) |
| `favicon.svg` | Browser tab icon |
| `scripts/sync_orcid.py` | Adds new ORCID papers to the Papers page (run weekly) |
| `scripts/orcid-skip.txt` | ORCID entries the sync should never add |
| `.github/workflows/orcid-sync.yml` | The weekly job that runs the sync |
| `.nojekyll` | Tells GitHub Pages to serve files as-is instead of running Jekyll |

Each page is a folder with an `index.html`, so `about/index.html` is served at `/about/`.
To add a page, copy an existing folder (e.g. `news/`), edit it, and add a link to it in the
header nav of every page.

The header, nav and footer are repeated in each page's HTML, so a nav change has to be
made in all five files.

## Papers page: ORCID sync and Altmetric

**New papers arrive automatically.** Every Monday a GitHub Actions job reads Max's public
[ORCID record](https://orcid.org/0000-0003-1083-6277), adds any paper whose DOI isn't on the
Papers page yet, updates the paper counts (Papers page intro and "All N papers" on the home
page), and publishes. To run it right away: repo **Actions** tab → **Update papers from
ORCID** → **Run workflow**. Each run's summary lists what it added.

How it decides:

- It only adds; it never deletes. Some papers on the page aren't in ORCID, and that's fine
  (the run summary lists them).
- A paper whose title matches one already on the page is treated as another version and
  skipped, except that a published article replaces its listed preprint.
- DOIs in `scripts/orcid-skip.txt` are never added. Use it for preprints whose published
  title differs, or anything else that shouldn't be on the site.
- Titles and journal names come straight from ORCID, so a new entry may need its
  capitalization tidied by hand. Edits like that are kept; the sync matches on DOI.

The sync is only as current as ORCID. To keep ORCID current, accept Crossref's
"auto-update" permission request when it shows up in your ORCID inbox; after that, new
papers that list your ORCID iD are added to your record automatically.

Run it locally with `python3 scripts/sync_orcid.py`.

**Altmetric scores** are added in the browser by `assets/site.js`: every paper with a
`doi.org` link gets Altmetric's small donut and an "Altmetric N" label under its venue.
Papers with no online mentions show nothing. There's nothing to maintain per paper. The
look is set in `assets/site.css` under "Altmetric score".

## Preview locally

From this folder:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Refresh after editing; no restart needed.

## Making changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for the edit → review → publish workflow.

## History

- Until October 2026 the site was built with the academicpages Jekyll template. That
  version is preserved on the `legacy-site` branch if anything needs to be recovered.
- The current design was built by GitHub user `MantisTMD1` in
  `MantisTMD1/maxwell-elliott-site` and merged in with its commit history intact. This repo
  is now the single place the site lives; make new changes here.

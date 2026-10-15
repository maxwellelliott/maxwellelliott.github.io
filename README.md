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
| `assets/site.js` | Dark-mode switch and phone menu |
| `images/` | Images hosted on this site (e.g. `headshot.jpeg`) |
| `files/` | PDFs (old CV links point here, so keep these paths stable) |
| `favicon.svg` | Browser tab icon |
| `.nojekyll` | Tells GitHub Pages to serve files as-is instead of running Jekyll |

Each page is a folder with an `index.html`, so `about/index.html` is served at `/about/`.
To add a page, copy an existing folder (e.g. `news/`), edit it, and add a link to it in the
header nav of every page.

The header, nav and footer are repeated in each page's HTML, so a nav change has to be
made in all five files.

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

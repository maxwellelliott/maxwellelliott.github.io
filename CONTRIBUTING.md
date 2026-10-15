# Working on the site together

Anyone listed as a collaborator on this repo (repo **Settings → Collaborators**) can push.
The rule of thumb: **`master` is live**, so anything you push there is public within a minute
or two.

## Small fixes (typo, new paper, news item)

Editing directly on `master` is fine:

1. Edit the file, either on github.com (open the file and click the pencil icon) or locally.
2. If editing locally, preview it (see README), then:

   ```bash
   git pull
   git add -A
   git commit -m "Add 2026 Neuron paper"
   git push
   ```

## Bigger changes (redesigns, new pages, anything you want a second opinion on)

Use a branch and a pull request so the other person can look before it goes live:

```bash
git pull
git checkout -b people-page-photos
# ...edit and preview...
git add -A
git commit -m "Add photos to People page"
git push -u origin people-page-photos
```

Then open the pull request on GitHub (it offers a "Compare & pull request" button after the
push), ask the other person to review it, and merge it when you're both happy. Merging is
what publishes it.

## Adding a paper

Usually you don't need to: the weekly ORCID sync (see README) adds it. To add one by hand,
copy a `<li class="paper">` block into the right year on `publications/index.html`. Use the
paper's `https://doi.org/...` link so the sync recognizes it and Altmetric can find it.

## Before you push

- Preview locally and click through every page you touched, in light and dark mode and at
  phone width.
- If you changed the header or footer, make the same change in all five pages.
- Keep existing file paths in `files/` and `images/` stable; other sites may link to them.

## Undoing a change

Every change is a commit, so nothing is lost. `git revert <commit>` undoes one cleanly, and
the pre-2026 Jekyll site is on the `legacy-site` branch.

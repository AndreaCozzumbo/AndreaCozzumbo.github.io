# How this website works

Jekyll site on the [al-folio](https://github.com/alshedivat/al-folio) theme (MIT).

## What to edit

| I want to change... | Edit |
| --- | --- |
| Home page text, role, affiliation, research topics | `_pages/about.md` |
| Plots, video and title band of the research topics | files in `assets/research/`, named in `_pages/about.md` |
| Description at the top of a page | `description` at the top of its file in `_pages/` (publications: in the text) |
| Portrait / home photograph | `assets/img/profile_pic.jpeg` / `assets/img/background.jpg` |
| Education and theses | `_data/curriculum/education.yml` |
| Visits and jobs | `_data/curriculum/experience.yml` |
| Supervision, outreach, organization, schools attended | `_data/curriculum/{supervision,outreach,organization,participation}.yml` |
| Skills, languages | `_data/curriculum/skills.yml` |
| Talks and seminars | `_data/talks.yml` |
| Name, email, ORCID (CV) / icons | `_data/curriculum/profile.yml` / `_data/socials.yml` |
| Publications | nothing: they come from INSPIRE every Monday |
| Fix a title that is wrong on INSPIRE | `_data/publication_overrides.yml` |
| Colours, fonts, spacing | `_sass/_custom.scss` (colours at the top) |
| Menu | `nav`, `nav_order`, `nav_title` at the top of each file in `_pages/` |
| Photos | `scripts/prepare_photos.py` (see below) |

The CV page and the CV PDFs are made from the same files, so each thing is written once.

## What each folder does

| Path | Role |
| --- | --- |
| `_config.yml` | site settings, plugins |
| `_pages/` | one file per page |
| `_data/` | content: CV, talks, badge colours |
| `_bibliography/papers.bib` | publications, written by `scripts/update_publications.py` |
| `_layouts/` | page skeletons: `default` (all), `about` (home), `page`, `bib` (one publication) |
| `_includes/` | pieces: menu (`header`), `footer`, `cv_entry`, `photo_grid` |
| `_sass/_custom.scss`, `assets/css/main.scss` | look of the site |
| `assets/` | images, photos, PDFs, `js/copy-bibtex.js` |
| `cv-latex/` | LaTeX style of the CV and of the publication list |
| `scripts/` | `update_publications.py` (INSPIRE), `build_cv.py` (LaTeX), `prepare_photos.py` |
| `.github/workflows/` | automation: `update-publications`, `build-cv`, `deploy` |
| `.devcontainer/` | lets GitHub Codespaces run the site (private preview) |
| `Gemfile*`, `package*.json`, `purgecss.config.js`, `Dockerfile`, `docker-compose*.yml`, `bin/` | build tools of al-folio |
| `docs/`, `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.codex/`, `.gemini/` | al-folio documentation; not published |

## Changes from this computer, and private test

1. Settings > Actions > General > Workflow permissions: *Read and write permissions*.
2. Preview: **Code > Codespaces > Create codespace on main**, wait for the build, then open port
   **8080** in the *Ports* tab. Keep its visibility on *Private*: only you can open it.
   If nothing starts, type `bash .devcontainer/start.sh` in the terminal.
   Alternatively download `site` from the latest *Build site* run in the **Actions** tab.
3. To send changes (published in a few minutes once the site is public): `git pull`, then `git add -A && git commit -m "..." && git push`.

## Publishing

The site is served at `https://andreacozzumbo.github.io`, so the repository must be called `AndreaCozzumbo.github.io`.

1. Settings > Secrets and variables > Actions > Variables: `PUBLISH_SITE` = `true`.
2. Actions > *Build site* > Run workflow (later, every push does it).
3. Settings > Pages > Deploy from a branch > `gh-pages` / `(root)`.

## Preview on this computer

Needs Ruby 3 and ImageMagick, e.g. `conda create -n website -c conda-forge ruby=3.3 imagemagick compilers make`
and `conda activate website`, then:

```bash
gem install bundler && bundle install       # once
bundle exec jekyll serve                    # http://localhost:4000
```

## Photographs

1. Put the photos in `photos/BnW` or `photos/Color`, next to `AC_web` (outside the repository: originals are never uploaded).
   JPEG, PNG, TIFF, HEIC. Number them (`0001.jpg`, `0002.jpg`...): in the catalogue the highest
   number comes first; the gallery with the arrows is in random order; each sub-folder makes a section with its name.
2. From `AC_web`:

```bash
python3 -m pip install pillow pyyaml        # once
python3 scripts/prepare_photos.py
```

It writes web copies without any metadata (EXIF, GPS) in `assets/photos/` and the list `_data/photos.yml`.
Number of columns: `.photo-grid` in `_sass/_custom.scss`.

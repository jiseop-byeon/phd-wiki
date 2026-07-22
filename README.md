# Physical AI Notes

Personal research wiki covering deep learning, robotics, control, and construction robotics.
Maintained as an Obsidian vault (`content/`); published online via Quartz + GitHub Pages at
https://jiseop-byeon.github.io/phd-wiki/.

## Structure (under `content/`)

- `01-canonical-papers/` — the curated paper list and one study note per paper,
  grouped by section (`notes/1-foundations/` … `notes/8-construction/`)
- `02-foundations/` — course-depth foundations, numbered in study order:
  0. Overview · 0.5 Engineering Math · 1. Linear Algebra · 2. Calculus & Backprop ·
  3. Probability · 4. Optimization · 5. Information Theory · 6. Signal Processing ·
  7. RL Basics · 8. 3D Geometry & SE(3) · 9. ML Practice & Evaluation
- `03-deep-learning/` — paper lineage diagrams and the physical-AI ecosystem map
- `04-robotics/` — Modern Robotics book guide + chapter summaries (ch. 2–6, 8–13),
  control theory, LQR/LQG, MPC, convex MPC for legged robots
- `05-construction-robotics/` — research lineage (four eras + current streams) and labs map
- `glossary.md` / `study-log.md` — term lookup and reading log
- `templates/` — note templates (not published)

## Conventions

- **Language**: each page has an `English` section first, then a `한국어` section.
- **Paper notes**: open with `**Author et al., VENUE YEAR** — [arXiv] · [PDF] · [Code]`,
  then context → method → results → limitations → impact → connections.
- **Links**: `[[wikilinks]]` connect papers, foundations, and domain pages; every claim of
  lineage is a link.
- **Explorer ordering**: numeric title prefixes (`1.`, `2.`, …) define study order;
  the sort override lives in `quartz.ts`.
- Display math must stay on a single line (`$$...$$`), and mermaid node labels must not
  start with `N.` — both break rendering otherwise.

## Workflow

1. Edit notes locally in Obsidian (open `content/` as vault) or via Claude Code.
2. Commit and push to `v5` — GitHub Actions builds and deploys the site automatically.
3. Local preview: `npx quartz build --serve` (requires `npx quartz plugin install` once).

The local `reference/` folder holds copyrighted course materials and is gitignored —
only original distilled notes are published.

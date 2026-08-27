# Physical AI Notes

Personal research wiki covering deep learning, robotics, control, and construction robotics.
Maintained as an Obsidian vault (`content/`); published online via Quartz + GitHub Pages at
https://jiseop-byeon.github.io/phd-wiki/.

## Structure (under `content/`)

- `00-study-depth-guide.md` — global Literacy / Working / Mastery targets; each
  substantive page also displays its target and Mastery promotion condition
- `01-canonical-papers/` — the curated paper list and one study note per paper,
  grouped by section (`notes/1-foundations/` … `notes/8-construction/`)
- `02-foundations/` — course-depth foundations, numbered in study order:
  0. Overview · 0.5 Engineering Math · 1. Linear Algebra · 2. Calculus & Backprop ·
  3. Probability · 4. Optimization · 5. Information Theory · 6. Signal Processing ·
  7. RL Basics · 8. 3D Geometry & SE(3) · 9. ML Practice & Evaluation
- `03-deep-learning/` — paper lineage diagrams and the physical-AI ecosystem map
- `04-robotics/` — Modern Robotics (ch. 2–6, 8–13), estimation/SLAM, planning,
  control, contact/tactile interaction, robot systems/deployment, HRI and safety
- `05-construction-robotics/` — research lineage (four eras + current streams) and labs map
- `06-research-practice/` — research questions, experimental design, failure analysis,
  scientific writing and peer review
- `08-research-radar/` — interactive, conservative trend map built from published
  proceedings and journal metadata using a multi-scope ontology
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
3. Use Node 24 (`nvm use`; see `.nvmrc`). Local preview: `npm run preview`; one-off build:
   `npm run site` (requires `npx quartz plugin install` once).
   Local builds need a larger Node heap as the site grows — these scripts set
   `NODE_OPTIONS=--max-old-space-size=8192` and single-worker mode; if calling `npx quartz build` directly, use both settings yourself.
   (Do not use Node 26 or `npm run build` — the current Quartz/plugin combination is
   verified on Node 24 and can hang or exhaust memory on Node 26.)

Content QA: `python3 scripts/verify_content.py` (run it from the repo root). Besides the
rendering and link rules, it enforces two classes of consistency that a page-by-page read
does not reliably catch:

- **self-counts** — every number the wiki states about its own contents (notes, sections,
  ★/◐/○ marks, the reading-load table) is derived from the files, so the files are the
  authority. A claim whose wording changes also fails, so a check cannot be lost by accident.
- **bilingual parity** — the `## English` and `## 한국어` halves of a page must cite the same
  sections (`scripts/audit_parity.py`, also runnable alone for a readable report). This
  exists because a correction can reach one language and leave the other asserting the
  superseded claim.

Rebuild the global page-depth profile
with `npm run depths`. Refresh the Radar dataset with `npm run radar`; its taxonomy lives
in `scripts/research_radar_taxonomy.json` and permits one topic to belong to multiple
research scopes.

The local `reference/` folder holds copyrighted course materials and is gitignored —
only original distilled notes are published.

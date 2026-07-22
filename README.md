# Physical AI Notes

Personal research wiki covering deep learning, robotics, control, and construction robotics.
Maintained as an Obsidian vault (`content/`); published online via Quartz + GitHub Pages.

## Structure (under `content/`)

- `01-canonical-papers/` — the curated paper list and one study note per paper
- `02-foundations/` — course-depth math & systems foundations (linear algebra → RL basics)
- `03-deep-learning/` — maps of content: CV, VLM, VLA, world models, diffusion; paper lineage diagrams
- `04-robotics/` — Modern Robotics (Lynch & Park) notes, control theory (state-space → LQR → MPC)
- `05-construction-robotics/` — construction/manufacturing robotics literature (CEE, CS, ME, EE venues)
- `templates/` — note templates (paper note, concept note)

## Conventions

- **Language**: each note has an `English` section first, then a `한국어` section.
- **Links**: use `[[wikilinks]]` liberally to connect concepts and papers.
- **Paper notes**: one file per paper in `40-papers/notes/`, created from `templates/paper-note.md`.
- **Status tags**: `to-read` → `reading` → `done` in paper note frontmatter.

## Workflow

1. Edit notes locally in Obsidian (or ask Claude Code to draft/refactor).
2. Commit and push to GitHub.
3. GitHub Actions builds the Quartz site and deploys to GitHub Pages automatically.

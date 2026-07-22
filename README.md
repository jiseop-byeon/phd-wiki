# PhD Knowledge Wiki

Personal research wiki covering deep learning, robotics, control, and construction robotics.
Maintained as an Obsidian vault; published online via Quartz + GitHub Pages.

## Structure

- `00-index/` — home page and maps of content (MOC)
- `10-deep-learning/` — foundations, computer vision, VLM, VLA, world models, diffusion
- `20-robotics/` — Modern Robotics (Lynch & Park) notes, control theory (state-space → LQR → MPC)
- `30-construction-robotics/` — construction/manufacturing robotics literature (CEE, CS, ME, EE venues)
- `40-papers/` — canonical paper list and individual paper notes
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

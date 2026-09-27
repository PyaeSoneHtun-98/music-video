# Music video production guide

## Goal

Build an original 6:50 anime music video featuring **Zin Zin** and **Pyae Sone**, planned as 28 segments. Keep the film visually consistent across separately generated Seedance shots.

## Sources of truth

1. `production/shot-list.csv` — segment IDs, timing and progress.
2. `production/continuity.md` — character identity, wardrobe, prop state and framing.
3. `production/world-bible.md` — location geography and master reference images.
4. `story-outline.md` — overall narrative.
5. `prompts/Sxx.md` — exact shot instructions for each segment.

If any sources disagree, fix the inconsistency before generating more assets.

## Asset workflow

- Plan a review sheet either from independent **16:9 landscape** frames or from one combined image with four equal 16:9 quadrants, as approved for S04. Never use a multi-panel contact sheet directly as a video input; prepare one separate 16:9 input per video shot after sheet approval.
- Give every frame a stable ID and path: `frames/S01-01-coastal-town.png`, `frames/S01-02-rail-drops.png`, and so on.
- Reuse the source character sheets, appropriate location masters and prop master as image references. Prompt for only the people and objects the shot needs.
- Pyae Sone wears the white short-sleeve shirt and dark trousers; his hands are empty unless a story action explicitly uses the charm. Do not add a carried jacket or extra shirt.
- Use character names in production text only. No on-screen name cards, captions or title cards.
- Record the reference images and final generation prompt in the matching `prompts/Sxx.md`.
- Build presentation sheets from the individual frames while preserving each panel's 16:9 aspect ratio.
- Present each completed sheet for the user's visual review. Keep its tracker status `in_review` and do not begin the next sheet until the user explicitly approves it. Fix any malformed frame or continuity problem before approval.
- Run `python scripts/validate_project.py` before committing a milestone.

## Repository hygiene

- `sparkle.m4a` is a local working track and is ignored by Git. Do not add it to the repository.
- Keep renders and exports outside Git unless the project deliberately selects a small review artifact.
- Preserve source images and earlier approved assets. Make a versioned file for a revision rather than silently overwriting one.
- Keep `README.md` and the shot tracker current. Commit meaningful milestones and push after verification, as requested for this project.

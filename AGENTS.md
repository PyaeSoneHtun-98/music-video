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

- Plan a review sheet either from independent **16:9 landscape** frames or from one combined image with four equal 16:9 quadrants, as approved for S04. For video generation, use each approved storyboard sheet as the visual reference for one complete 15-second segment (S28 is 5 seconds). Prompt sequential shots in panel order; the generated video must not show the contact-sheet grid. An intentional split-screen within a single approved shot is allowed.
- Give every frame a stable ID and path: `frames/S01-01-coastal-town.png`, `frames/S01-02-rail-drops.png`, and so on.
- Reuse the source character sheets, appropriate location masters and prop master as image references. Prompt for only the people and objects the shot needs.
- Pyae Sone wears the white short-sleeve shirt and dark trousers; his hands are empty unless a story action explicitly uses the charm. Do not add a carried jacket or extra shirt.
- Use character names in production text only. No on-screen name cards, captions or title cards.
- Record the reference images and final generation prompt in the matching `prompts/Sxx.md`.
- Before generating each segment video, add one timed multi-shot video prompt to its `prompts/Sxx.md`.
- Keep the extracted individual frames and `production/video-inputs.csv` as a timing and fallback library. They are not the primary one-prompt-per-shot production workflow. S01–S03 use approved individual frames in one segment generation until clean image sheets are prepared; their HTML review layouts are not uploadable images.
- Build presentation sheets from the individual frames while preserving each panel's 16:9 aspect ratio.
- Present future combined review sheets as clean images without shot numbers, timestamps or captions. Do not make new labeled HTML or screenshot previews. Keep timing and shot descriptions in `prompts/Sxx.md` and `production/shot-list.csv`; those production notes are not video inputs. Existing labeled preview files are archival review aids only.
- Present each completed sheet for the user's visual review. Keep its tracker status `in_review` until the user explicitly approves it. Fix any malformed frame or continuity problem before approval. When the user approves a sheet, mark it ready, validate, commit and push the milestone, then continue with the next sheet.
- Run `python scripts/validate_project.py` before committing a milestone.

## Repository hygiene

- `sparkle.m4a` is a local working track and is ignored by Git. Do not add it to the repository.
- Keep renders and exports outside Git unless the project deliberately selects a small review artifact.
- Preserve source images and earlier approved assets. Make a versioned file for a revision rather than silently overwriting one.
- Keep `README.md` and the shot tracker current. Commit meaningful milestones and push after verification, as requested for this project.

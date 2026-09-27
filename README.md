# Zin Zin × Pyae Sone — music video

An original anime romance music video planned around a local 6:50 edit of RADWIMPS’ *Sparkle*. The story follows Zin Zin and Pyae Sone through a rainlit coastal town toward a lighthouse reunion.

## Current state

- Story outline and 28-sheet production grid: [story-outline.md](story-outline.md)
- Master schedule and progress: [production/shot-list.csv](production/shot-list.csv)
- Identity and framing rules: [production/continuity.md](production/continuity.md)
- Town geography and reusable references: [production/world-bible.md](production/world-bible.md)
- First sheet’s shot instructions: [prompts/S01.md](prompts/S01.md)
- First full-frame visual: [frames/S01-01-coastal-town.png](frames/S01-01-coastal-town.png)
- Reusable [location references](locations/) and [prop reference](props/P01-reunion-props.png)
- Reproducible [reference asset prompts](prompts/reference-assets.md)
- S01 contact sheet: [storyboards/S01-the-town-after-rain-v2.png](storyboards/S01-the-town-after-rain-v2.png) (planning only; its cells are not 16:9 video inputs)

## Format

- Master video: **16:9 landscape**, export at **1920 × 1080**.
- Song length from local file metadata: **410.018 seconds**, approximately **6:50**.
- Plan: 27 intervals of 15 seconds and a final interval of 5 seconds.
- No on-screen names, titles, captions, or dialogue text unless intentionally added later.
- Keep generated images and clips for each sheet in `frames/` and `renders/` with stable IDs such as `S01-01`.

## Workflow

1. Use the character sheets `zinzin.png` and `pyaesone.png` as identity references.
2. Write a prompt for each shot in `prompts/Sxx.md` and keep timing in `production/shot-list.csv`.
3. Generate each opening frame as its own near-16:9 image. A multi-panel contact sheet is a visual plan, not a Seedance input.
4. Generate the video shots at the platform’s **16:9 setting**; keep characters, wardrobe and town geography consistent.
5. Assemble and trim the videos to the local audio in an editor, then export the master at 1920 × 1080.
6. Run `python scripts/validate_project.py` after adding or changing still frames or the schedule.

The local working audio `sparkle.m4a` is intentionally excluded from Git. Keep it in the project folder for editing. The source character sheets and approved visual references are versioned.

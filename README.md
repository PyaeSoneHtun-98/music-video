# Zin Zin × Pyae Sone — music video

An original anime romance music video planned around a local 6:50 edit of RADWIMPS’ *Sparkle*. The story follows Zin Zin and Pyae Sone through a rainlit coastal town toward a lighthouse reunion.

## Current state

- Story outline and 28-sheet production grid: [story-outline.md](story-outline.md)
- Production instructions for future agents: [AGENTS.md](AGENTS.md)
- Master schedule and progress: [production/shot-list.csv](production/shot-list.csv)
- Identity and framing rules: [production/continuity.md](production/continuity.md)
- Town geography and reusable references: [production/world-bible.md](production/world-bible.md)
- First sheet’s shot instructions: [prompts/S01.md](prompts/S01.md)
- First full-frame visual: [frames/S01-01-coastal-town.png](frames/S01-01-coastal-town.png)
- Reusable [location references](locations/) and [prop reference](props/P01-reunion-props.png)
- Reproducible [reference asset prompts](prompts/reference-assets.md)
- S01 production sheet: [storyboards/S01.html](storyboards/S01.html) (six true 16:9 picture windows)
- S02 production sheet: [storyboards/S02.html](storyboards/S02.html) (approved)
- S03 production sheet: [storyboards/S03.html](storyboards/S03.html) (approved)
- S04 production sheet: [storyboards/S04.html](storyboards/S04.html) (approved one-generation combined image)
- S05 production sheet: [storyboards/S05.html](storyboards/S05.html) (approved combined image with one route correction)
- S06 production sheet: [storyboards/S06-combined.png](storyboards/S06-combined.png) (approved clean combined image with one prop correction)
- S08 production sheet: [storyboards/S08-combined-v2.png](storyboards/S08-combined-v2.png) (approved glass-window revision)
- S09 production sheet: [storyboards/S09-combined-v2.png](storyboards/S09-combined-v2.png) (approved open-street revision)
- S10 production sheet: [storyboards/S10-combined-v2.png](storyboards/S10-combined-v2.png) (approved free-falling charm revision)
- S11 production sheet: [storyboards/S11-combined.png](storyboards/S11-combined.png) (approved original version)
- S12 production sheet: [storyboards/S12-combined.png](storyboards/S12-combined.png) (approved)
- S13 production sheet: [storyboards/S13-combined-v2.png](storyboards/S13-combined-v2.png) (approved)
- S14 production sheet: [storyboards/S14-combined.png](storyboards/S14-combined.png) (approved)
- S15 production sheet: [storyboards/S15-combined.png](storyboards/S15-combined.png) (approved)
- S16 production sheet: [storyboards/S16-combined.png](storyboards/S16-combined.png) (approved)
- S17 production sheet: [storyboards/S17-combined.png](storyboards/S17-combined.png) (approved)
- S18 production sheet: [storyboards/S18-combined.png](storyboards/S18-combined.png) (approved)
- S19 production sheet: [storyboards/S19-combined-v3.png](storyboards/S19-combined-v3.png) (approved)
- S20 production sheet: [storyboards/S20-combined-v3.png](storyboards/S20-combined-v3.png) (approved)
- Early S01 concept: [storyboards/S01-the-town-after-rain-v2.png](storyboards/S01-the-town-after-rain-v2.png) (planning only; its cells are not 16:9 video inputs)

## Format

- Master video: **16:9 landscape**, export at **1920 × 1080**.
- Song length from local file metadata: **410.018 seconds**, approximately **6:50**.
- Plan: 27 intervals of 15 seconds and a final interval of 5 seconds.
- No on-screen names, titles, captions, or dialogue text unless intentionally added later.
- Keep generated images and clips for each sheet in `frames/` and `renders/` with stable IDs such as `S01-01`.

## Workflow

1. Use the character sheets `zinzin.png` and `pyaesone.png` as identity references.
2. Write a prompt for each shot in `prompts/Sxx.md` and keep timing in `production/shot-list.csv`.
3. For review, generate either independent near-16:9 frames or one combined sheet with equal 16:9 quadrants. Prepare one separate 16:9 image per shot before using it as a Seedance input; the full contact sheet is a visual plan.
4. Present each completed sheet for visual approval before starting the next one. Fix any malformed image or continuity issue first.
   Future combined-sheet reviews show the clean unlabeled image; timestamps live in the prompt and schedule files, not on the image.
5. Generate the video shots at the platform’s **16:9 setting**; keep characters, wardrobe and town geography consistent.
6. Assemble and trim the videos to the local audio in an editor, then export the master at 1920 × 1080.
7. Run `python scripts/validate_project.py` after adding or changing still frames or the schedule.

The local working audio `sparkle.m4a` is intentionally excluded from Git. Keep it in the project folder for editing. The source character sheets and approved visual references are versioned.

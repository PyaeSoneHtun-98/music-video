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
- S02 production sheet: [storyboards/S02-combined.png](storyboards/S02-combined.png) (approved frames assembled as one clean uploadable image; [archival layout](storyboards/S02.html))
- S03 production sheet: [storyboards/S03-combined.png](storyboards/S03-combined.png) (approved frames assembled as one clean uploadable image; [archival layout](storyboards/S03.html))
- S04 production sheet: [storyboards/S04-combined.png](storyboards/S04-combined.png) (approved one-generation combined image; [archival layout](storyboards/S04.html))
- S05 production sheet: [storyboards/S05-combined.png](storyboards/S05-combined.png) (approved combined image with one route correction; [archival layout](storyboards/S05.html))
- S06 production sheet: [storyboards/S06-combined.png](storyboards/S06-combined.png) (approved clean combined image with one prop correction)
- S07 production sheet: [storyboards/S07-combined.png](storyboards/S07-combined.png) (approved; four matched 16:9 frames)
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
- S21 production sheet: [storyboards/S21-combined-v3.png](storyboards/S21-combined-v3.png) (approved)
- S22 production sheet: [storyboards/S22-combined-v2.png](storyboards/S22-combined-v2.png) (approved)
- S23 production sheet: [storyboards/S23-combined.png](storyboards/S23-combined.png) (approved clean review image)
- S24 first-sight frame: [frames/S24-01-first-sight.png](frames/S24-01-first-sight.png) (approved clean 16:9 image)
- S25 reunion sheet: [storyboards/S25-combined.png](storyboards/S25-combined.png) (approved clean four-panel image)
- S26 charm-return sheet: [storyboards/S26-combined.png](storyboards/S26-combined.png) (approved clean four-panel image)
- S27 new-morning sheet: [storyboards/S27-combined-v3.png](storyboards/S27-combined-v3.png) (approved clean four-panel image; couple beside the plush at the right-hand rail)
- S28 final frame: [frames/S28-01-final-image-v2.png](frames/S28-01-final-image-v2.png) (approved clean 16:9 image; couple at the rail, shirt matched to character sheet)
- Early S01 concept: [storyboards/S01-the-town-after-rain-v2.png](storyboards/S01-the-town-after-rain-v2.png) (planning only; its cells are not 16:9 video inputs)

## Seedance segment workflow

- All 28 story segments are approved. Generate **one 15-second Seedance clip per segment**, including S28. Select the best five seconds of S28 for the final 06:45–06:50 edit. Attach the approved storyboard image as a visual reference, set Seedance to **16:9 landscape**, and prepare one timed segment prompt in `prompts/Sxx.md` before generation. Each panel becomes a sequential shot; the video must not display the storyboard grid. An intentional split-screen within a shot is retained.
- S02 and S03 use their clean combined storyboard images as single uploads. S01 still needs an uploadable combined image; its approved individual frames can guide a single segment generation until that sheet is prepared. S24 and S28 use their approved single-frame images.
- [production/video-inputs.csv](production/video-inputs.csv) remains a **108-shot timing and fallback library**. Its 88 extracted 832 × 468 panels and 20 original standalone frames can support retries or individual-shot repairs; they are no longer the primary generation sequence.
- The fallback extraction remains reproducible with `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prepare_video_inputs.ps1`. Rebuild its timing map with `python scripts/build_video_input_manifest.py`, then run `python scripts/validate_project.py`.

## Format

- Master video: **16:9 landscape**, export at **1920 × 1080**.
- Song length from local file metadata: **410.018 seconds**, approximately **6:50**.
- Plan: 27 intervals of 15 seconds and a final interval of 5 seconds.
- No on-screen names, titles, captions, or dialogue text unless intentionally added later.
- Keep generated images and clips for each sheet in `frames/` and `renders/` with stable IDs such as `S01-01`.

## Workflow

1. Use the character sheets `zinzin.png` and `pyaesone.png` as identity references.
2. Write one timed multi-shot video prompt per segment in `prompts/Sxx.md` and keep segment timing in `production/shot-list.csv`.
3. Use approved sheets as visual references for whole-segment generation. The separate approved frames in `production/video-inputs.csv` remain available for retries and repair shots.
4. Present each completed sheet for visual approval before starting the next one. Fix any malformed image or continuity issue first.
   Future combined-sheet reviews show the clean unlabeled image; timestamps live in the prompt and schedule files, not on the image.
5. Generate one 16:9 video clip per segment, translating storyboard panels into sequential full-screen shots while keeping characters, wardrobe and town geography consistent.
6. Assemble and trim the videos to the local audio in an editor, then export the master at 1920 × 1080.
7. Run `python scripts/validate_project.py` after adding or changing still frames or the schedule.

The local working audio `sparkle.m4a` is intentionally excluded from Git. Keep it in the project folder for editing. The source character sheets and approved visual references are versioned.

# Downloaded video audit — 2026-10-04

## Result

41 MP4 downloads were inspected and renamed in the local `videos/` directory across two audit passes. All 41 decode without reported errors. Their bytes were preserved and SHA256 verified after renaming. No clips were deleted, trimmed, re-encoded or marked visually approved.

- 36 unique files: 34 music-video takes and 2 unrelated office clips.
- 5 exact duplicate downloads, retained with `duplicate-01` suffixes.
- Coverage for 26 of the 28 segments. S01 coverage consists of six individual raw clips, not an assembled 15-second segment.
- **Missing: S13 and S16** — 30 seconds of planned story coverage.
- Present does not mean approved: several clips need continuity repairs or editing.

The source-to-final filename map, hashes, technical metadata and individual findings are in [video-audit.csv](video-audit.csv). The separate [video-status.csv](video-status.csv) tracks downloaded video coverage. `shot-list.csv` continues to track storyboard progress; its `ready` state is not approval of these generated videos.

## Missing segments

| Segment | Film time | Required action |
|---|---|---|
| S13 — Different stairways | 03:00–03:15 | Separate storm routes: Zin Zin on west stairs, Pyae Sone on east route holding charm. |
| S16 — The clue | 03:45–04:00 | Pyae Sone recognizes the wordless ceramic lighthouse mural and chooses upper east stairs. |

The two similar moonlit staircase videos are **both S21 takes**, not S21 and S23. Both start with a harbor view, then Zin Zin climbing, Pyae Sone climbing and a wider stair view. Neither contains S23's charm insert and threshold sequence.

## Visible repair findings

Times below are approximate source-clip times. Findings are based on sampled frames, including one-second contact sheets for the relevant clips.

| Segment | Finding | Action |
|---|---|---|
| S06 | Source four-panel grid appears during roughly first 1–2 seconds. | Replace opening shot or regenerate segment. Simply trimming loses the planned opening beat. |
| S07 take-01 | Source grid occupies opening roughly 0–3 seconds; previously rejected by user. | Preserve as rejected take. Prefer take-02 for review. |
| S07 take-02 | Intended two-panel split-screen appears at opening; subsequent wide/window/departure sequence is present. | Better candidate. Check exact shot durations; transitions include dissolves. |
| S10 | Charm chain appears caught on the rail around 0–7 seconds. | Retry the fall action so charm detaches from bag and falls freely. |
| S14 | Spotted charm reappears on Zin Zin's bag during early stair/gust shots. | Remove premature charm return; she lost it in S10. |
| S19 | Charm is visible on Zin Zin's bag while Pyae Sone holds recovered charm later. | Repair duplicated prop state. |
| S20 | Charm is again visible on her bag around 5–10 seconds. Storm looks weaker than requested. | Repair bag state and review storm continuity. |
| S21 both takes | Charm remains on her bag around 4–7 seconds. | Repair bag state before selecting a take. |
| S23 | Around 5–8 seconds Zin Zin holds the plush again and the spotted charm is already on her bag while Pyae Sone carries it. | Keep plush on paving beside right shoe and bag without charm until S26. |
| S24 | Held wide cuts to close portrait around 9 seconds. She holds plush again and charm is already attached to bag. | Retry uninterrupted wide; plush stays on ground and charm stays with Pyae Sone. |
| S25 | Charm is already on her bag while Pyae Sone carries it. | Repair before S26 returns charm. |
| S27 | Pair stops away from fixed plush and rail in several wide shots. | Restore approved placement immediately beside rail and toy. |
| S28 | Source has wide/close/wide cuts instead of the requested continuous waist-level hold. Its 15-second generation length matches the latest remote instructions. | Regenerate approved held composition or deliberately select an alternate five-second edit after review. |

S26's return and handhold are present, but the toy's distance from the pair and close hand/clasp motion need review. S01-05 has a tram-like arrival background instead of a clear ferry arrival, and S01-06's adjacent backgrounds make the intended separate locations ambiguous. These are recorded as review items rather than certified passes.

## Technical checks and edit requirements

- 39 files are 1280 × 720 (16:9), HEVC, 24 fps. The 2 portrait files are the unrelated office-chair clip and its duplicate, at 720 × 1280.
- Each download has approximately **15.104 seconds container duration**, **15.041667 seconds video duration** (361 frames), and an audio stream. The small overrun is export padding, not evidence of a missing shot.
- S01's six raw clips require selections of 2, 3, 2, 3, 2 and 3 seconds to assemble its planned 15 seconds. Do not concatenate all six at full length.
- S02–S27 need exact 15-second timeline boundaries; generate S28 for 15 seconds and select five seconds for the final edit, as specified by remote commit `1f66d25`. Final sequence is 410 seconds against the local working music track.
- Sampled music-video frames show a **Dola AI watermark**. The downloads do not satisfy the intended no-watermark delivery yet.
- Generated audio is present; replace/mute it when assembling against the local `sparkle.m4a` track. Audio content and music synchronization were not auditioned in this audit.
- The 720p source clips can be placed in the planned 1920 × 1080 edit, but upscaling does not add genuine source detail.

## Review scope

All 41 files received metadata, full decode and SHA256 checks. Six distributed frames per file were visually checked for identity and segment mapping. One-second contact sheets were checked for selected narrative/continuity issues, including all four downloads in the second pass. This is a sampled visual audit, not a guarantee that every intermediate frame has correct fingers, motion or geometry. A continuous playback review is still needed before final video approval.

Audit previews are local ignored files under `tmp/video-audit/`; overview row indices match `audit_index` in the CSV. They are analysis aids, not new storyboard/video inputs. Videos remain ignored by Git.

## Reproducibility and recovery

- `python scripts/apply_video_names.py` checks all mapped hashes and previews pending renames; `--apply` performs them. It is safe to rerun after completion.
- `python scripts/apply_video_names.py --undo --apply` restores original download names with collision and hash checks when those names are unique. The second download batch reuses the original lighthouse filenames; full undo now refuses before any mutation because of those repeated historical names. Use the manifest to restore separate batches to separate directories if needed.
- `scripts/audit_video_files.py` requires FFmpeg/ffprobe on PATH and Pillow. Run it with the bundled workspace Python if the default Python lacks Pillow. It reads local videos and writes ignored previews; rerunning after renaming creates a fresh inventory using current names.
- Add `--new-only` to audit only names absent from the saved manifest. New previews go in `tmp/video-audit-recheck/`, preserving the first pass. Its preview indices 1–4 correspond to CSV audit indices 38–41 for this second pass.
- Preserve alternate S05, S07 and S21 takes until edit selection. `take-01` is a stable identifier, not a quality ranking.

## Completion checks

41 filename changes applied across both passes, all hashes verified unchanged, 41 files retained. Project validation passed before committing each audit milestone. Storyboard approval and previously pending project changes are separate from this video audit.

## Second pass — 2026-10-04, after additional downloads

- `Rainy Market Video (12).mp4` is now `S12-summer-memory-take-01.mp4`. All four planned memory scenes are present; no grid appears in sampled frames. Remains awaiting video review, with dissolves rather than hard cuts.
- `Rainy Market Video (13).mp4` is now `S23-the-final-steps-take-01.mp4`. All four planned actions are identifiable, but plush and charm continuity need repairs as above.
- The two newly present `Zin Zin's Lighthouse` downloads are exact SHA256 duplicates of existing S27 and S22 takes, not repaired versions. Both are retained with duplicate suffixes.
- Rechecked all 37 earlier files against the saved hashes; contents are unchanged, so earlier findings still apply.

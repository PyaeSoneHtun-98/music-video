# First music-video cut — v02

**Review status:** in review; generated footage and this assembly are not final approvals.

**Local output:** `exports/Zin-Zin-Pyae-Sone-review-v02.mp4` (1920 × 1080, 24 fps, 6:50).

Revision v02 replaces v01's static S10 falling-charm insert with selected generated footage. Both local exports and their edit manifests are preserved.

## Edit decisions

- Follow the 28-segment schedule from 0 to 410 seconds, retaining all narrative beats and S07's intentional opening split-screen.
- Use `sparkle.m4a` from time zero as the sole soundtrack. Discard every generated clip's audio. Preserve the song's level; add only a one-second end fade and trim the approximately 18 ms audio tail beyond 410 seconds.
- Assemble S01's six raw downloads into the planned 2/3/2/3/2/3-second opening.
- Select S05 take 01, S07 take 02, S21 take 01 and S23 take 02. Exclude exact duplicates and rejected S07 take 01.
- Keep 332 seconds of generated moving footage. Use 78 seconds of approved standalone illustrations with a restrained 2.5% centered camera push, including the planned 15-second S24 hold and five-second closing image. The remaining 58 seconds replace grid flashes, duplicated props or incorrect rail placement.
- Use hard cuts at the saved edit-event boundaries. Existing dissolves within intact generated takes remain. Source intervals are retimed where needed to reach exact event durations. Opening fade is half a second; closing fade is one second.
- Upscale the 720p moving footage with Lanczos. This produces a 1080p delivery file but cannot restore detail absent from the source.

The exact selected sources, source intervals, final timeline intervals and replacement reasons are in [edit-v02.csv](edit-v02.csv). The source videos and approved illustrations remain unchanged.

## Approved-frame replacements

| Segment | Replacement |
|---|---|
| S06 | Opening tram wide; prevents contact-sheet grid. |
| S10 | Bag illustration replaces the rail snag; a clean 0.9-second detached fall and landing from the generated clip is slowed to four seconds. |
| S14 | Gust shot; prevents premature charm return. |
| S19 | Bridge and stair shots; keeps bag without charm. |
| S20 | Wide, stair-edge reaction and continuing climb; fixes missing distant figure and bag prop state. |
| S21 | Zin Zin stair shot; fixes recovered charm reappearing on bag. |
| S23 | Head-turn shot; prevents the second teal plush appearing in her arms. |
| S24 | Whole continuous wide; preserves the approved single-shot composition and ground plush. |
| S25 | Approach and two-shot; fixes charm duplicated on bag before return. |
| S27 | Approach, rail hold and closing wide; preserves proximity to plush and rail. |
| S28 | Approved linked-hands image held for five seconds. |

The illustrated replacements animate the camera, not character actions. Regenerated shots can replace those events later without rebuilding the rest of the edit. Approach actions and some walking shots remain illustrated in this review version. The S10 fall uses generated motion; its short source interval is slowed by repeating frames, which may appear stepped.

## Remaining review limits

- Dola AI watermarks remain on the moving source footage. No names, captions, timestamps or title cards are added to the film.
- Subtle source motion, wardrobe, geography and hand defects may remain. See [video-audit.md](video-audit.md).
- This first cut uses the existing story schedule against the track from time zero. Fine adjustment of cuts to musical accents remains a review decision; it is not described as a finished beat-by-beat edit.
- Source video tracker repair states are retained even where the review assembly uses a temporary illustrated replacement. Storyboard approvals are unchanged.

## Export checks

The [verification record](edit-v02-verification.json) confirms 9,840 frames, exactly 410 seconds, clean full decoding, and soundtrack alignment (correlation 0.9991). All 60 event midpoints were sampled; the revised fall insert and export fades received additional checks. Continuous playback and creative timing review are still pending.

## Rebuild

The saved CSV is the source of truth for this version. `python scripts/render_review_cut.py --manifest production/edit-v02.csv --version v02` renders cached events and exports the film. Existing exported versions are protected from overwriting; use a new version for a revision. FFmpeg/ffprobe must be on PATH.

`scripts/build_review_edit.py` documents how the initial CSV was built and refuses to overwrite it. To validate the actual export, run `scripts/verify_review_cut.py --manifest production/edit-v02.csv --version v02` with the bundled workspace Python (requires NumPy and Pillow). It checks full decoding, exact frame count and soundtrack signal alignment, and makes ignored technical review previews.

Only edit scripts and production records are committed. The music, MP4 export, temporary previews, cache and local video ZIP remain ignored.

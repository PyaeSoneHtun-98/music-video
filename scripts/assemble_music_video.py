"""Assemble the Sparkle review cut from the downloaded Seedance clips.

The edit follows the 28-segment schedule in production/shot-list.csv. Segment
boundaries are snapped to the nearest strong onset in sparkle.m4a so cuts land
on the music, every piece is retimed or trimmed to fill its slot exactly, and a
light anime grade (highlight bloom, vignette, grain) is applied at 1920 x 1080.

    python scripts/assemble_music_video.py                 # full review cut
    python scripts/assemble_music_video.py --plan-only     # write the EDL only
    python scripts/assemble_music_video.py --segments S11,S12,S13 --out renders/proof.mp4
    python scripts/assemble_music_video.py --final-start 405 --no-snap --no-crop

The resulting edit decision list is written to production/edit-decision-list.csv.
Requires FFmpeg/ffprobe and numpy. Renders go to renders/ (ignored by Git).
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"
SONG = ROOT / "sparkle.m4a"
SCHEDULE = ROOT / "production" / "shot-list.csv"
EDL_PATH = ROOT / "production" / "edit-decision-list.csv"
WORK = ROOT / "tmp" / "assembly"

FPS = 24
CLIP_END = 15.0417  # 361 frames; the container's last 0.06 s is padding
FIRST = 1 / FPS  # skip each clip's first frame, which is often a flash frame

# The final chord of the working track lands at about 399 s and decays by
# ~404 s; the remaining seconds are silence. Starting S28 on that chord is an
# editorial choice. Pass --final-start 405 to restore the scheduled 405-410 s.
DEFAULT_FINAL_START = 399.0

# 1.11x crop-zoom that keeps the generator watermark (y 664-689 of 720) out of
# frame. Disable with --no-crop once watermark-free downloads are available.
WATERMARK_CROP = "crop=1152:648:64:6"


@dataclass
class Piece:
    file: str
    src_in: float
    src_out: float


@dataclass
class Segment:
    sid: str
    pieces: list[Piece]
    fade_in: tuple[str, float] | None = None  # (colour, seconds)
    fade_out: tuple[str, float] | None = None
    note: str = ""
    start: float = 0.0
    end: float = 0.0
    plan: list[dict] = field(default_factory=list)


def whole(name: str) -> list[Piece]:
    return [Piece(name, FIRST, CLIP_END)]


def build_segments(final_start: float) -> list[Segment]:
    s01 = [
        Piece("S01-01-coastal-town-take-01.mp4", 0.0417, 2.0417),
        Piece("S01-02-rail-drops-take-01.mp4", 6.0, 9.0),
        Piece("S01-03-lighthouse-take-01.mp4", 4.0, 6.0),
        Piece("S01-04-zinzin-tram-take-01.mp4", 9.0, 12.0),
        Piece("S01-05-pyaesone-arrival-take-01.mp4", 0.0417, 2.0417),
        Piece("S01-06-separate-gazes-take-01.mp4", 5.0, 8.0),
    ]
    early_final = final_start < 405
    segs = [
        Segment("S01", s01, fade_in=("black", 1.5), note="six raw clips cut 2/3/2/3/2/3 s"),
        Segment("S02", whole("S02-two-journeys-begin-take-01.mp4")),
        Segment("S03", whole("S03-the-promise-take-01.mp4")),
        Segment("S04", whole("S04-almost-on-time-take-01.mp4")),
        Segment("S05", whole("S05-first-downpour-take-02.mp4"), note="take-02 selected"),
        Segment("S06", [Piece("S06-closed-route-take-01.mp4", 2.5, CLIP_END)],
                note="starts after the storyboard grid that ends at 2.46 s"),
        Segment("S07", whole("S07-passing-shadows-take-02.mp4"), note="take-02; take-01 rejected"),
        Segment("S08", whole("S08-warm-window-take-01.mp4")),
        Segment("S09", whole("S09-his-route-take-01.mp4")),
        Segment("S10", whole("S10-the-charm-falls-take-01.mp4"), note="charm still snags on rail"),
        Segment("S11", whole("S11-recognition-take-01.mp4"), fade_out=("white", 0.25)),
        Segment("S12", whole("S12-summer-memory-take-01.mp4"), fade_in=("white", 0.6),
                fade_out=("white", 0.25), note="memory framed by white dips"),
        Segment("S13", whole("S13-different-stairways-take-01.mp4"), fade_in=("white", 0.5)),
        Segment("S14", whole("S14-wind-and-water-take-01.mp4"), note="charm-on-bag error remains"),
        Segment("S15", whole("S15-doubt-take-01.mp4")),
        Segment("S16", whole("S16-the-clue-take-01.mp4")),
        Segment("S17", whole("S17-town-of-reflections-take-01.mp4")),
        Segment("S18", whole("S18-the-bell-take-01.mp4")),
        Segment("S19", whole("S19-last-crossing-take-01.mp4"), note="charm-on-bag error remains"),
        Segment("S20", whole("S20-he-calls-out-take-01.mp4"), note="charm-on-bag error remains"),
        Segment("S21", whole("S21-storm-breaks-take-01.mp4"), fade_in=("white", 0.35),
                note="take-01; white flash on the climax entry; charm-on-bag error remains"),
        Segment("S22", whole("S22-where-they-began-take-01.mp4")),
        Segment("S23", [Piece("S23-the-final-steps-take-02.mp4", FIRST, 7.5),
                        Piece("S23-the-final-steps-take-02.mp4", 9.75, CLIP_END)],
                note="take-02 with the duplicated-plush turn (7.5-9.7 s) cut out"),
        Segment("S24", [Piece("S24-first-sight-take-01.mp4", FIRST, 8.4)],
                note="held wide only; close-up with plush/charm errors cut out"),
        Segment("S25", whole("S25-reunion-take-01.mp4"), note="charm-on-bag error remains"),
        Segment("S26", whole("S26-the-little-promise-take-01.mp4")),
    ]
    if early_final:
        segs.append(Segment("S27", [Piece("S27-new-morning-take-01.mp4", FIRST, 4.0),
                                    Piece("S27-new-morning-take-01.mp4", 4.0833, 7.8333),
                                    Piece("S27-new-morning-take-01.mp4", 7.9167, 11.3333)],
                            note="shortened so S28 lands on the final chord; placement error remains"))
        segs.append(Segment("S28", [Piece("S28-final-image-take-01.mp4", 3.5, CLIP_END)],
                            fade_out=("black", 3.0),
                            note="hands close-up, dissolve to the held wide, fade to black"))
    else:
        segs.append(Segment("S27", whole("S27-new-morning-take-01.mp4"), note="placement error remains"))
        segs.append(Segment("S28", [Piece("S28-final-image-take-01.mp4", 9.0, CLIP_END)],
                            fade_out=("black", 2.5), note="five seconds of the held wide"))
    return segs


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kw)


def song_duration() -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(SONG)], capture_output=True, text=True)
    return float(out.stdout.strip())


def onset_envelope() -> tuple[np.ndarray, float]:
    sr, hop, n = 22050, 256, 1024
    raw = run(["ffmpeg", "-v", "error", "-i", str(SONG), "-ac", "1", "-ar", str(sr),
               "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
    spec = np.log1p(10 * np.abs(np.fft.rfft(frames, axis=1)))
    flux = np.maximum(0, np.diff(spec, axis=0)).sum(1)
    # Loudness rise catches soft piano/chord attacks that spectral flux underrates.
    loud = np.log10((frames ** 2).mean(1) + 1e-10)
    rise = np.maximum(0, loud[1:] - loud[:-1])
    z = lambda v: (v - v.mean()) / v.std()
    # A short moving sum favours full attacks over single-hop clicks.
    onset = np.convolve(z(flux) + z(rise), np.ones(3), mode="same")
    # Index i compares frames i and i + 1; an attack peaks there when it sits
    # at the centre of frame i + 1.
    lead = (hop + n / 2) / hop - 1
    return onset, sr / hop, lead


def snap(t: float, env: tuple, window: float = 0.4) -> float:
    onset, rate, lead = env
    a, b = int((t - window) * rate), int((t + window) * rate)
    local = onset[a:b] - onset[a:b].min()
    # Prefer the strongest onset, lightly weighted towards the scheduled time.
    weights = 1 - 0.3 * np.abs(np.arange(a, b) / rate - t) / window
    best = a + int(np.argmax(local * weights))
    return (best + 1 + lead) / rate


def frame(t: float) -> float:
    return round(t * FPS) / FPS


def place(segs: list[Segment], final_start: float, use_snap: bool) -> float:
    with SCHEDULE.open(newline="", encoding="utf-8") as fh:
        starts = {r["sheet_id"]: float(r["start_seconds"]) for r in csv.DictReader(fh)}
    starts["S28"] = final_start
    total = frame(song_duration())
    env = onset_envelope() if use_snap else None
    bounds = []
    for seg in segs:
        t = starts[seg.sid]
        if use_snap and t > 0:
            t = snap(t, env)
        bounds.append(frame(t))
    bounds.append(total)
    for seg, a, b in zip(segs, bounds, bounds[1:]):
        seg.start, seg.end = a, b
        plan_pieces(seg)
    return total


def plan_pieces(seg: Segment) -> None:
    target = seg.end - seg.start
    pieces = [Piece(p.file, p.src_in, p.src_out) for p in seg.pieces]
    source = sum(p.src_out - p.src_in for p in pieces)
    speed = target / source  # >1 slows the footage down
    if speed < 0.97:
        # Too much footage: trim the tail instead of visibly speeding it up.
        excess = source - target
        while excess > 1e-6:
            last = pieces[-1]
            length = last.src_out - last.src_in
            if length <= excess + 0.5:
                pieces.pop()
                excess -= length
            else:
                last.src_out -= excess
                excess = 0
        speed = target / sum(p.src_out - p.src_in for p in pieces)
    t = seg.start
    seg.plan = []
    for i, p in enumerate(pieces, 1):
        dur = (p.src_out - p.src_in) * speed
        seg.plan.append({
            "segment_id": seg.sid, "piece": i, "source_file": p.file,
            "src_in": f"{p.src_in:.3f}", "src_out": f"{p.src_out:.3f}",
            "speed_factor": f"{speed:.4f}",
            "timeline_start": f"{t:.3f}", "timeline_end": f"{t + dur:.3f}",
            "fade_in": f"{seg.fade_in[0]} {seg.fade_in[1]}s" if seg.fade_in and i == 1 else "",
            "fade_out": f"{seg.fade_out[0]} {seg.fade_out[1]}s" if seg.fade_out and i == len(pieces) else "",
            "note": seg.note if i == 1 else "",
        })
        t += dur


def write_edl(segs: list[Segment], final_start: float, use_snap: bool, crop: bool) -> None:
    rows = [row for seg in segs for row in seg.plan]
    with EDL_PATH.open("w", newline="", encoding="utf-8") as fh:
        fh.write(f"# review cut: final_start={final_start:g} snapped={use_snap} watermark_crop={crop} "
                 f"fps={FPS}; generated by scripts/assemble_music_video.py\n")
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def grade_chain(src: str, crop: bool) -> str:
    """Filtergraph from label src to an unterminated graded chain."""
    pre = ([WATERMARK_CROP] if crop else []) + [
        "scale=1920:1080:flags=lanczos",
        "eq=contrast=1.03:saturation=1.08",
        "format=gbrp",  # blend in RGB; screening YUV chroma tints the frame
    ]
    return (f"{src}{','.join(pre)},split[base][hi];"
            # Bloom: blur only the highlights and screen them back over the frame.
            "[hi]curves=all='0/0 0.62/0 1/1',gblur=sigma=28[glow];"
            "[base][glow]blend=all_mode=screen:all_opacity=0.25,format=yuv420p,"
            "vignette=angle=PI/7,unsharp=5:5:0.35,noise=alls=3:allf=t")


def render_segment(seg: Segment, crop: bool) -> Path:
    out = WORK / f"{seg.sid}.mkv"
    frames = round((seg.end - seg.start) * FPS)
    inputs, chains, labels = [], [], []
    for i, row in enumerate(seg.plan):
        inputs += ["-i", str(VIDEOS / row["source_file"])]
        speed = float(row["speed_factor"])
        retime = f"setpts=(PTS-STARTPTS)*{speed:.6f}"
        rate = (f"framerate=fps={FPS}" if speed > 1.2 else f"fps={FPS}")
        chains.append(f"[{i}:v]trim={row['src_in']}:{row['src_out']},{retime},{rate},"
                      f"setsar=1,format=yuv420p[p{i}]")
        labels.append(f"[p{i}]")
    graph = ";".join(chains)
    graph += f";{''.join(labels)}concat=n={len(labels)}:v=1:a=0[cat]"
    graph += ";" + grade_chain("[cat]", crop)
    fades = []
    dur = seg.end - seg.start
    if seg.fade_in:
        fades.append(f"fade=t=in:st=0:d={seg.fade_in[1]}:color={seg.fade_in[0]}")
    if seg.fade_out:
        fades.append(f"fade=t=out:st={dur - seg.fade_out[1]:.4f}:d={seg.fade_out[1]}:color={seg.fade_out[0]}")
    tail = ",".join(["tpad=stop_mode=clone:stop_duration=1"] + fades + ["format=yuv420p"])
    graph += f",{tail}[v]"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[v]",
         "-frames:v", str(frames), "-r", str(FPS), "-c:v", "libx264", "-preset", "fast",
         "-crf", "10", "-bf", "0", str(out)])
    return out


def assemble(parts: list[Path], start: float, end: float, out: Path) -> None:
    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    dur = end - start
    afade = f"afade=t=in:st=0:d=0.05,afade=t=out:st={max(dur - 1.5, 0):.3f}:d=1.5"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(SONG),
         "-map", "0:v:0", "-map", "1:a:0", "-af", afade,
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
         "-profile:v", "high", "-tune", "animation", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart",
         "-frames:v", str(round(dur * FPS)), str(out)])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="renders/sparkle-review-cut-v1.mp4")
    ap.add_argument("--segments", help="comma-separated subset for a proof render, e.g. S11,S12,S13")
    ap.add_argument("--final-start", type=float, default=DEFAULT_FINAL_START)
    ap.add_argument("--no-snap", action="store_true", help="keep the exact 15-second grid")
    ap.add_argument("--no-crop", action="store_true", help="keep the full frame, watermark included")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print(f"{tool} is required on PATH", file=sys.stderr)
            return 1
    if not SONG.exists():
        print("sparkle.m4a is missing", file=sys.stderr)
        return 1

    segs = build_segments(args.final_start)
    total = place(segs, args.final_start, not args.no_snap)
    missing = sorted({r["source_file"] for s in segs for r in s.plan if not (VIDEOS / r["source_file"]).exists()})
    if missing:
        print("missing clips: " + ", ".join(missing), file=sys.stderr)
        return 1

    chosen = segs
    if args.segments:
        wanted = args.segments.upper().split(",")
        chosen = [s for s in segs if s.sid in wanted]
    else:
        write_edl(segs, args.final_start, not args.no_snap, not args.no_crop)
        print(f"edit decision list: {EDL_PATH.relative_to(ROOT)} ({total:.3f} s)")
    for s in chosen:
        print(f"{s.sid}  {s.start:8.3f} - {s.end:8.3f}  speed {s.plan[0]['speed_factor']}  {s.note}")
    if args.plan_only:
        return 0

    WORK.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        parts = list(pool.map(lambda s: render_segment(s, not args.no_crop), chosen))
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    assemble(parts, chosen[0].start, chosen[-1].end, out)
    print(f"rendered {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

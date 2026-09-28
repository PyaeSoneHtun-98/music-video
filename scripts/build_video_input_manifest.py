"""Map every approved edit shot to one standalone Seedance input frame."""

from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "production" / "shot-list.csv"
OUTPUT = ROOT / "production" / "video-inputs.csv"
SHOT_ROW = re.compile(r"^\|\s*(S\d{2}-\d{2})\s*\|\s*(\d+)[–-](\d+)s\s*\|")
PANELS = {"01": "top_left", "02": "top_right", "03": "bottom_left", "04": "bottom_right"}
STANDALONE_SHEETS = {"S01", "S02", "S03", "S07", "S24", "S28"}


def main() -> None:
    with TRACKER.open(newline="", encoding="utf-8") as file:
        tracker = list(csv.DictReader(file))

    manifest: list[dict[str, str | int]] = []
    next_start = 0
    for sheet in tracker:
        sheet_id = sheet["sheet_id"]
        prompt = ROOT / "prompts" / f"{sheet_id}.md"
        shots: list[tuple[str, int, int]] = []
        for line in prompt.read_text(encoding="utf-8").splitlines():
            if match := SHOT_ROW.match(line):
                shots.append((match.group(1), int(match.group(2)), int(match.group(3))))

        if sheet_id in {"S24", "S28"}:
            shots = [
                (
                    f"{sheet_id}-01",
                    int(sheet["start_seconds"]),
                    int(sheet["end_seconds"]),
                )
            ]
        if not shots:
            raise ValueError(f"{sheet_id}: no shot timing found in {prompt}")

        for shot_id, start, end in shots:
            if start != next_start or end <= start:
                raise ValueError(f"{shot_id}: noncontiguous or invalid timing {start}-{end}")
            next_start = end

            if sheet_id in {"S24", "S28"}:
                input_path = sheet["first_frame"]
                panel = "standalone"
            elif sheet_id in STANDALONE_SHEETS:
                matches = sorted((ROOT / "frames").glob(f"{shot_id}-*.png"))
                if len(matches) != 1:
                    raise ValueError(f"{shot_id}: expected one independent frame, found {matches}")
                input_path = matches[0].relative_to(ROOT).as_posix()
                panel = "standalone"
            else:
                input_path = f"frames/{shot_id}-input.png"
                panel = PANELS[shot_id[-2:]]

            if not (ROOT / input_path).is_file():
                raise ValueError(f"{shot_id}: missing input frame {input_path}")

            manifest.append(
                {
                    "shot_id": shot_id,
                    "start_seconds": start,
                    "end_seconds": end,
                    "input_frame": input_path,
                    "review_source": sheet["storyboard"],
                    "panel": panel,
                }
            )

        if next_start != int(sheet["end_seconds"]):
            raise ValueError(f"{sheet_id}: final shot ends at {next_start}, expected {sheet['end_seconds']}")

    if next_start != 410 or len(manifest) != 108:
        raise ValueError(f"Expected 108 shots spanning 0-410s, found {len(manifest)} to {next_start}s")

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["shot_id", "start_seconds", "end_seconds", "input_frame", "review_source", "panel"],
        )
        writer.writeheader()
        writer.writerows(manifest)
    print(f"Mapped {len(manifest)} standalone shot inputs to 0-{next_start}s in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""Check schedule continuity and framing of generated PNG keyframes."""

from __future__ import annotations

import csv
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "production" / "shot-list.csv"
EXPECTED_END = 410
ALLOWED_STATUS = {"planned", "in_progress", "ready", "rendered", "edited"}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as file:
        header = file.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    errors: list[str] = []
    with MANIFEST.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != 28:
        errors.append(f"expected 28 sheets, found {len(rows)}")

    next_start = 0
    for number, row in enumerate(rows, 1):
        sheet = row["sheet_id"]
        start = int(row["start_seconds"])
        end = int(row["end_seconds"])
        if sheet != f"S{number:02d}":
            errors.append(f"sheet order: expected S{number:02d}, found {sheet}")
        if start != next_start or end <= start:
            errors.append(f"{sheet}: non-contiguous or invalid time {start}–{end}")
        if end - start > 15:
            errors.append(f"{sheet}: exceeds 15 seconds")
        if row["status"] not in ALLOWED_STATUS:
            errors.append(f"{sheet}: unknown status {row['status']}")
        next_start = end

        for column in ("storyboard", "first_frame"):
            relative = row[column]
            if relative and not (ROOT / relative).is_file():
                errors.append(f"{sheet}: missing {column}: {relative}")

        relative = row["first_frame"]
        if relative:
            path = ROOT / relative
            if path.is_file():
                try:
                    width, height = png_size(path)
                    ratio = width / height
                    if abs(ratio - 16 / 9) > 0.002:
                        errors.append(f"{sheet}: {relative} is {width}x{height}, ratio {ratio:.4f}; expected near 16:9")
                except ValueError as exc:
                    errors.append(str(exc))

    if next_start != EXPECTED_END:
        errors.append(f"schedule ends at {next_start}s, expected {EXPECTED_END}s")

    reference_paths = [
        *sorted((ROOT / "frames").glob("*.png")),
        *sorted((ROOT / "locations").glob("*.png")),
        ROOT / "props" / "P01-reunion-props.png",
    ]
    for path in reference_paths:
        if not path.is_file():
            errors.append(f"missing reusable reference: {path.relative_to(ROOT)}")
            continue
        try:
            width, height = png_size(path)
            if abs(width / height - 16 / 9) > 0.002:
                errors.append(f"{path.relative_to(ROOT)} is {width}x{height}; expected near 16:9")
        except ValueError as exc:
            errors.append(str(exc))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(rows)} sheets covering 0-{EXPECTED_END}s and {len(reference_paths)} near-16:9 references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

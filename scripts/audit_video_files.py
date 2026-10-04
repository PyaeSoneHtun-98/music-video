"""Inspect local videos without modifying their contents; write ignored audit previews."""
import concurrent.futures
import argparse
import csv
import hashlib
import json
import pathlib
import subprocess
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--new-only', action='store_true', help='Inspect filenames absent from the saved rename manifest.')
args = parser.parse_args()
OUT = ROOT / 'tmp' / ('video-audit-recheck' if args.new_only else 'video-audit')
OUT.mkdir(parents=True, exist_ok=True)

def inspect(item):
    index, path = item
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True)
    metadata = json.loads(probe.stdout)
    stream = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
    duration = float(metadata['format']['duration'])
    decode = subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True, text=True)
    row = {'index': index, 'original': path.name, 'sha256': digest, 'duration': duration, 'width': stream['width'], 'height': stream['height'], 'fps': stream['r_frame_rate'], 'video_codec': stream['codec_name'], 'audio': any(s['codec_type'] == 'audio' for s in metadata['streams']), 'decode_ok': decode.returncode == 0 and not decode.stderr.strip(), 'decode_errors': decode.stderr.strip()}
    thumbs = []
    for k, fraction in enumerate([0.02, 0.2, 0.4, 0.6, 0.8, 0.96]):
        thumb = OUT / f'{index:02d}-{k}.jpg'
        time = min(duration - 0.1, duration * fraction)
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(time), '-i', str(path), '-vf', 'scale=240:135', '-frames:v', '1', str(thumb)], check=True, capture_output=True)
        thumbs.append(str(thumb))
    row['thumbnails'] = thumbs
    contact = OUT / f'{index:02d}-detail.jpg'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(path), '-vf', 'fps=1,scale=640:360,tile=4x4', '-frames:v', '1', str(contact)], check=True, capture_output=True)
    row['detail'] = str(contact)
    return row

paths = sorted((ROOT / 'videos').glob('*.mp4'), key=lambda p: p.name.lower())
if args.new_only:
    with (ROOT / 'production/video-audit.csv').open(encoding='utf-8', newline='') as manifest:
        known_names = {row['renamed_name'].lower() for row in csv.DictReader(manifest)}
    paths = [path for path in paths if path.name.lower() not in known_names]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(inspect, enumerate(paths, 1)))
(OUT / 'inventory.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
for page, start in enumerate(range(0, len(rows), 5), 1):
    batch = rows[start:start+5]
    canvas = Image.new('RGB', (1440, len(batch)*160), '#111111')
    draw = ImageDraw.Draw(canvas)
    for j, row in enumerate(batch):
        draw.text((5, j*160+4), f"{row['index']:02d} | {row['original']} | {row['duration']:.3f}s | {row['width']}x{row['height']}", fill='white')
        for k, thumb in enumerate(row['thumbnails']):
            with Image.open(thumb) as im:
                canvas.paste(im, (k*240, j*160+25))
    canvas.save(OUT / f'overview-{page:02d}.jpg', quality=92)
groups = {}
for row in rows:
    groups.setdefault(row['sha256'], []).append(row['index'])
print(json.dumps({'count': len(rows), 'unique': len(groups), 'duplicates': [v for v in groups.values() if len(v)>1], 'metadata': [{k:v for k,v in row.items() if k not in ['thumbnails','detail','sha256']} for row in rows]}, indent=2))

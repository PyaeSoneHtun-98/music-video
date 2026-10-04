"""Check the actual first-cut export: decode, frames, soundtrack alignment and review previews."""
import argparse
import csv
import json
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--version',default='v01')
parser.add_argument('--manifest',default='production/edit-v01.csv')
args=parser.parse_args()
if not args.version.replace('-','').isalnum():
    raise ValueError('Version must be a simple identifier.')
TARGET=ROOT/'exports'/f'Zin-Zin-Pyae-Sone-review-{args.version}.mp4'
OUT=ROOT/'tmp'/f'review-{args.version}'
OUT.mkdir(parents=True,exist_ok=True)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

meta=probe(TARGET)
video=[s for s in meta['streams'] if s['codec_type']=='video']
audio=[s for s in meta['streams'] if s['codec_type']=='audio']
assert len(video)==len(audio)==1, 'Expected exactly one video and one audio stream.'
v=video[0]
assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'24/1')
assert int(v['nb_frames'])==9840 and abs(float(v['duration'])-410)<0.001
decoded=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(TARGET),'-f','null','-'],capture_output=True,text=True)
assert decoded.returncode==0 and not decoded.stderr.strip(),decoded.stderr

def pcm(path):
    data=subprocess.check_output(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-map','0:a:0','-t','408','-ac','1','-ar','11025','-f','f32le','-'])
    return np.frombuffer(data,dtype='<f4').astype(np.float64)

song,export=pcm(ROOT/'sparkle.m4a'),pcm(TARGET)
n=min(len(song),len(export));song=song[:n];export=export[:n]
corr=float(np.dot(song,export)/np.sqrt(np.dot(song,song)*np.dot(export,export)))
rms_ratio=float(np.sqrt(np.mean(export**2)/np.mean(song**2)))
assert corr>0.99, f'Soundtrack mismatch or timing shift: correlation {corr}'
assert 0.95<rms_ratio<1.05, f'Unexpected music volume change: {rms_ratio}'

with (ROOT/args.manifest).open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
for i,row in enumerate(rows):
    moment=(float(row['timeline_in'])+float(row['timeline_out']))/2
    path=OUT/f'{row["edit_id"]}.jpg'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(moment),'-i',str(TARGET),'-vf','scale=320:180','-frames:v','1',str(path)],check=True,capture_output=True)
for page,start in enumerate(range(0,len(rows),12),1):
    canvas=Image.new('RGB',(1280,600),'#111111'); draw=ImageDraw.Draw(canvas)
    for j,row in enumerate(rows[start:start+12]):
        x=(j%4)*320;y=(j//4)*200
        with Image.open(OUT/f'{row["edit_id"]}.jpg') as im: canvas.paste(im,(x,y+20))
        draw.text((x+4,y+3),f'{row["edit_id"]} {row["segment_id"]} {row["timeline_in"]}-{row["timeline_out"]}s {row["mode"]}',fill='white')
    canvas.save(OUT/f'overview-{page:02d}.jpg',quality=92)
result={'export':str(TARGET),'duration_seconds':float(v['duration']),'frame_count':int(v['nb_frames']),
        'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'video_codec':v['codec_name'],
        'audio_codec':audio[0]['codec_name'],'decode_ok':True,'music_correlation_first_408_seconds':corr,
        'music_rms_ratio_first_408_seconds':rms_ratio,'edit_events':len(rows),'approval':'in_review',
        'visual_review':'Previews generated; human/agent review must be completed separately.'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))

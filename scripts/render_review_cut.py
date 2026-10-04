"""Render a versioned review edit with the local song as its sole audio stream."""
import argparse
import concurrent.futures
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FPS = 24

def run(command):
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode:
        raise RuntimeError(process.stderr[-6000:])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',default='production/edit-v01.csv')
    parser.add_argument('--version',default='v01')
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    if not args.version.replace('-','').isalnum():
        raise ValueError('Version must be a simple identifier.')
    with (ROOT/args.manifest).open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    cursor=0
    for row in rows:
        start,end=float(row['timeline_in']),float(row['timeline_out'])
        if abs(start-cursor)>1e-6 or end<=start or abs((end-start)*FPS-round((end-start)*FPS))>1e-6:
            raise ValueError(f'Invalid timeline: {row}')
        if not (ROOT/row['source']).is_file(): raise FileNotFoundError(row['source'])
        cursor=end
    if cursor!=410: raise ValueError('Expected 410-second film.')
    cache=ROOT/'renders'/f'review-{args.version}'
    cache.mkdir(parents=True,exist_ok=True)
    target=ROOT/'exports'/f'Zin-Zin-Pyae-Sone-review-{args.version}.mp4'
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): raise FileExistsError(f'Preserve existing export: {target}')
    common=['ffmpeg','-hide_banner','-loglevel','error','-y']
    def encode(row):
        source=ROOT/row['source']; duration=float(row['timeline_out'])-float(row['timeline_in'])
        count=round(duration*FPS)
        key=hashlib.sha256((json.dumps(row,sort_keys=True)+str(source.stat().st_mtime_ns)+'1080p24-crf18-fast-zoom-v1').encode()).hexdigest()
        output=cache/f'{row["edit_id"]}.mp4'; stamp=cache/f'{row["edit_id"]}.sha256'
        if not (output.exists() and stamp.exists() and stamp.read_text()==key):
            if row['mode']=='video':
                begin,end=float(row['source_in']),float(row['source_out'])
                if end<=begin: raise ValueError(row)
                inputs=['-ss',str(begin),'-t',str(end-begin),'-i',str(source)]
                filters=f'setpts={duration/(end-begin):.12f}*(PTS-STARTPTS),fps={FPS},scale=1920:1080:flags=lanczos:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,tpad=stop_mode=clone:stop_duration=1,trim=end_frame={count},setpts=N/({FPS}*TB)'
            elif row['mode']=='still':
                inputs=['-loop','1','-framerate',str(FPS),'-i',str(source)]
                # A restrained centered push animates the camera only, never character limbs.
                filters=f"scale=2560:1440:flags=lanczos:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='1+0.025*on/{max(count-1,1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={count}:s=1920x1080:fps={FPS},setsar=1,trim=end_frame={count},setpts=N/({FPS}*TB)"
            else: raise ValueError(row['mode'])
            if row is rows[0]: filters+=',fade=t=in:st=0:d=0.5'
            if row is rows[-1]: filters+=f',fade=t=out:st={duration-1}:d=1'
            run(common+inputs+['-map','0:v:0','-an','-vf',filters,'-frames:v',str(count),'-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-video_track_timescale','12288','-map_metadata','-1',str(output)])
            stamp.write_text(key)
        print(f'{row["edit_id"]} {row["segment_id"]} {duration:g}s {row["mode"]}',flush=True)
        return output
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        pieces=list(pool.map(encode,rows))
    concat=cache/'concat.txt'
    concat.write_text('\n'.join(f"file '{p.name}'" for p in pieces)+'\n',encoding='utf-8')
    run(common+['-f','concat','-safe','0','-i',str(concat),'-i',str(ROOT/'sparkle.m4a'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','atrim=duration=410,asetpts=PTS-STARTPTS,afade=t=out:st=409:d=1','-c:a','aac','-b:a','192k','-t','410','-map_metadata','-1','-movflags','+faststart',str(target)])
    print(f'Export: {target}',flush=True)

if __name__=='__main__': main()

"""Write a reproducible 410-second first-cut decision list from the approved schedule."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT/'production/shot-list.csv').open(encoding='utf-8', newline='') as f:
    schedule = list(csv.DictReader(f))
with (ROOT/'production/video-inputs.csv').open(encoding='utf-8', newline='') as f:
    frames = {r['shot_id']: r['input_frame'] for r in csv.DictReader(f)}
with (ROOT/'production/video-status.csv').open(encoding='utf-8', newline='') as f:
    available = {r['segment_id']: r['files'].split('; ') for r in csv.DictReader(f)}
preferred = {'S05':'S05-first-downpour-take-01.mp4', 'S07':'S07-passing-shadows-take-02.mp4',
             'S21':'S21-storm-breaks-take-01.mp4', 'S23':'S23-the-final-steps-take-02.mp4'}
rows = []
cursor = 0

def add(segment, duration, mode='video', source=None, begin=0, end=None, reason=''):
    global cursor
    source = source or 'videos/'+preferred.get(segment, available[segment][0])
    if not (ROOT/source).is_file():
        raise FileNotFoundError(source)
    rows.append(dict(edit_id=f'E{len(rows)+1:03d}', segment_id=segment,
        timeline_in=cursor, timeline_out=cursor+duration, mode=mode, source=source,
        source_in=begin if mode=='video' else '', source_out=end if end is not None else duration if mode=='video' else '',
        note=reason or 'Selected generated footage; exact segment duration; source audio discarded.'))
    cursor += duration

def still(segment, shot, duration, reason):
    add(segment, duration, 'still', frames[f'{segment}-{shot:02d}'], reason=reason)

for s in schedule:
    segment = s['sheet_id']
    assert cursor == int(s['start_seconds'])
    if segment == 'S01':
        for i, duration in enumerate([2,3,2,3,2,3], 1):
            source = available[segment][i-1]
            add(segment,duration,source='videos/'+source,begin=2,end=2+duration,
                reason='Select stable motion from individual raw clip; preserve opening six-shot plan.')
    elif segment == 'S06':
        still(segment,1,4,'Approved frame with gentle push replaces source-grid opening.')
        add(segment,3,begin=2.1,end=7.8,reason='Passengers exit; retime clean full-screen passage.')
        add(segment,4,begin=8.1,end=11.35,reason='Bridge route; trim transition overlap.')
        add(segment,4,begin=11.55,end=15,reason='Pyae bakery search; fit planned ending.')
    elif segment == 'S10':
        still(segment,1,4,'Approved bag frame replaces charm caught on rail.')
        still(segment,2,4,'Approved free-fall illustration with gentle push; actual fall animation still needs regeneration.')
        add(segment,3,begin=8.1,end=10.9,reason='Dropped charm in puddle.')
        add(segment,4,begin=11.2,end=15,reason='Zin continues unaware.')
    elif segment == 'S14':
        still(segment,1,4,'Approved gust frame avoids charm reappearing on bag.')
        add(segment,4,begin=4.1,end=6.8)
        add(segment,4,begin=7.1,end=10.8)
        add(segment,3,begin=11.1,end=15)
    elif segment == 'S19':
        still(segment,1,4,'Approved bridge frame preserves bag without recovered charm.')
        still(segment,2,4,'Approved stair frame replaces premature charm return.')
        add(segment,3,begin=8.1,end=10.8)
        add(segment,4,begin=11.2,end=15)
    elif segment == 'S20':
        still(segment,1,4,'Approved wide includes distant Zin on same stairs.')
        add(segment,4,begin=2.1,end=4.9,reason='Pyae calls while holding charm; retimed portrait.')
        still(segment,3,4,'Approved stair-edge reaction avoids duplicated bag charm.')
        still(segment,4,3,'Approved rear climb keeps charm absent and storm continuity.')
    elif segment == 'S21':
        add(segment,4,begin=0,end=3.9)
        still(segment,2,4,'Approved moonlit climb replaces charm on Zin bag.')
        add(segment,4,begin=8.1,end=11.8)
        add(segment,3,begin=12.1,end=15)
    elif segment == 'S23':
        add(segment,4,begin=0,end=2.9)
        add(segment,4,begin=3.1,end=4.9,reason='Single recovered charm insert; slow to planned duration.')
        still(segment,3,4,'Approved head-turn frame replaces duplicated plush in take 02.')
        add(segment,3,begin=10.2,end=13.2,reason='Threshold pause; end before shared sight line.')
    elif segment == 'S24':
        still(segment,1,15,'Approved continuous two-person hold replaces unwanted cut and incorrect props.')
    elif segment == 'S25':
        add(segment,4,begin=0,end=2.85,reason='Zin recognition portrait.')
        add(segment,4,begin=3.1,end=6.8,reason='Pyae recognition portrait.')
        still(segment,3,4,'Approved approach frame avoids charm duplication on bag.')
        still(segment,4,3,'Approved arm-length two-shot; charm remains with Pyae.')
    elif segment == 'S27':
        still(segment,1,4,'Approved linked-hands approach toward plush by rail.')
        still(segment,2,4,'Approved pair standing directly beside rail and toy.')
        add(segment,3,begin=8.1,end=10.8,reason='Warm dawn side portrait.')
        still(segment,4,4,'Approved wide preserves nearby plush and rail placement.')
    elif segment == 'S28':
        still(segment,1,5,'Approved waist-level linked-hands hold; final one-second fade.')
    else:
        add(segment,15,begin=0,end=15)
    assert cursor == int(s['end_seconds'])
assert cursor == 410
target = ROOT/'production/edit-v01.csv'
if target.exists():
    raise FileExistsError('Versioned edit list already exists; use a new version rather than overwrite.')
with target.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f'{len(rows)} edit events, {cursor}s; {sum(float(r["timeline_out"])-float(r["timeline_in"]) for r in rows if r["mode"]=="still")}s of approved-frame repair/held shots.')

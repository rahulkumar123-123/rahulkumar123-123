from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/contributions.json').read_text())
days=data['days'][-371:]
palette=['#161b22','#0e4429','#006d32','#26a641','#39d353','#69f0a0']
cell=13; gap=3; left=44; top=34
cols=53; rows=7
width=left+cols*(cell+gap)+150; height=190
# Pad at front so the final 371 days occupy complete columns.
while len(days)<371: days.insert(0,{'date':'','level':0,'count':0})
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<style>.t{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}@keyframes pop{from{opacity:0;transform:translate(-4px,-4px)}to{opacity:1;transform:translate(0,0)}}</style>', '<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d"/>']
svg.append('<text x="18" y="23" class="t" fill="#7ee787" font-size="13">rahul@github:~$ ./contributions.sh</text>')
for i,d in enumerate(days):
    col=i//7; row=i%7
    x=left+col*(cell+gap); y=top+row*(cell+gap)
    delay=(col*0.018+row*0.025)
    svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{palette[d.get("level",0)]}" style="animation:pop .35s ease-out {delay:.3f}s both"/>')
# Month labels: approximate from actual dates.
seen=set()
for i,d in enumerate(days):
    if not d['date']: continue
    month=d['date'][:7]
    if month not in seen and i%7==0:
        col=i//7; svg.append(f'<text x="{left+col*(cell+gap)}" y="{top-9}" class="t" fill="#8b949e" font-size="11">{month[5:]}/{month[:4]}</text>'); seen.add(month)
svg.append(f'<text x="18" y="{height-34}" class="t" fill="#8b949e" font-size="11">Less</text>')
for j,c in enumerate(palette): svg.append(f'<rect x="54" y="{height-44}" width="12" height="12" rx="3" fill="{c}"/>')
svg.append(f'<text x="{width-74}" y="{height-34}" class="t" fill="#8b949e" font-size="11">More</text>')
svg.append(f'<text x="{width-260}" y="{height-34}" class="t" fill="#c9d1d9" font-size="11">{data["stats"]["contributions"]:,} contributions · streak {data["stats"]["current_streak"]}d</text>')
svg.append('</svg>')
(ROOT/'contrib-heatmap.svg').write_text('\n'.join(svg),encoding='utf-8')
print(ROOT/'contrib-heatmap.svg')

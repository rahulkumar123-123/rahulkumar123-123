from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'info-card.svg'
static=os.getenv('STATIC')=='1'
rows=[
('Education','4th Year B.Tech · Electronics & Communication','BIT Mesra, Ranchi'),
('Focus','Machine Learning · GenAI · Data Science','Full-stack development'),
('Research','Illinois Tech · Bioinformatics + ML','HPA · TCGA · LINCS L1000'),
('Experience','Analytics Intern · MMM Amsterdam','Power BI · US market analytics'),
('Role','Student Placement Coordinator','BIT Mesra'),
('Projects','Parkinson’s speech detection','Wav2Vec2 · WavLM · GRU · LSTM · SVM'),
]
w,h=570,360
s=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
.t{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.k{{fill:#7ee787;font-weight:700}} .v{{fill:#c9d1d9}} .sub{{fill:#8b949e;font-size:13px}}
.row{{opacity:{1 if static else 0}}}
@keyframes in{{from{{opacity:0;transform:translateX(12px)}}to{{opacity:1;transform:translateX(0)}}}}
</style>
<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d"/>
<rect x="0" y="0" width="100%" height="42" rx="10" fill="#161b22"/>
<circle cx="18" cy="21" r="5" fill="#ff7b72"/><circle cx="36" cy="21" r="5" fill="#d29922"/><circle cx="54" cy="21" r="5" fill="#3fb950"/>
<text x="72" y="27" class="t" fill="#8b949e" font-size="14">rahul@github:~$ whoami</text>
<text x="22" y="76" class="t" fill="#58a6ff" font-size="22" font-weight="700">Rahul Kumar</text>
<text x="22" y="97" class="t sub">machine learning · genai · data · web</text>
<line x1="22" y1="112" x2="548" y2="112" stroke="#30363d"/>''']
for i,(k,v,sub) in enumerate(rows):
    y=140+i*35
    dur=0 if static else 0.35
    begin=0 if static else i*0.12
    op='' if static else f' style="animation:in .35s ease-out {begin:.2f}s forwards"'
    s.append(f'<g class="row"{op}><text x="22" y="{y}" class="t k" font-size="13">{k}</text><text x="115" y="{y}" class="t v" font-size="13">{v}</text><text x="115" y="{y+15}" class="t sub">{sub}</text></g>')
s.append('</svg>')
out.write_text('\n'.join(s),encoding='utf-8')
print(out)

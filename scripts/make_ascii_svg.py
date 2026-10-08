from pathlib import Path
import cv2, html

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'source-prepped.png'
out = ROOT / 'avi-ascii.svg'
RAMP = ' .`:-=+*cs#%@'
COLS, ROWS = 92, 48
img = cv2.imread(str(src), cv2.IMREAD_GRAYSCALE)
if img is None:
    raise SystemExit('Run prep_photo.py first.')
img = cv2.resize(img, (COLS, ROWS), interpolation=cv2.INTER_AREA)

# Slightly bias toward darker glyphs for a stronger portrait.
lines=[]
for y in range(ROWS):
    s=''
    for x in range(COLS):
        v=int(img[y,x])
        idx=round((255-v)/255*(len(RAMP)-1))
        s += RAMP[max(0,min(len(RAMP)-1,idx))]
    lines.append(s.rstrip())

font=8.5
line_h=10.2
pad=10
width=COLS*font+pad*2
height=ROWS*line_h+pad*2
parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">
<rect width="100%" height="100%" rx="8" fill="#0d1117"/>
<defs><clipPath id="wipe">''']
for y in range(ROWS):
    yy=pad+y*line_h-7.5
    parts.append(f'<rect x="{pad}" y="{yy:.1f}" width="0" height="{line_h+2:.1f}"><animate attributeName="width" from="0" to="{COLS*font:.1f}" dur="0.55s" begin="{y*0.035:.3f}s" fill="freeze"/></rect>')
parts.append('</clipPath></defs>')
parts.append(f'<g clip-path="url(#wipe)" fill="#c9d1d9" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{font}px" xml:space="preserve">')
for y,line in enumerate(lines):
    parts.append(f'<text x="{pad}" y="{pad+(y+1)*line_h:.1f}">{html.escape(line)}</text>')
parts.append('</g></svg>')
out.write_text('\n'.join(parts), encoding='utf-8')
print(out)

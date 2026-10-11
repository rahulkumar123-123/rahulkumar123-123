from pathlib import Path
import json, html
from datetime import date
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
days = data["days"][-371:]
while len(days) < 371:
    days.insert(0, {"date": "", "level": 0, "count": 0})
palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
cell, gap, left, top, cols, rows = 13, 3, 36, 36, 53, 7
width, height = left + cols * (cell + gap) + 28, 160
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
       '<style>.t{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}</style>',
       '<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>']
# Month labels based on the actual first day in each week.
last_month = None
for col in range(cols):
    week = days[col * 7:(col + 1) * 7]
    dates = [item["date"] for item in week if item.get("date")]
    if not dates:
        continue
    dt = date.fromisoformat(min(dates))
    month_key = (dt.year, dt.month)
    if month_key != last_month:
        svg.append(f'<text x="{left + col * (cell + gap)}" y="24" class="t" fill="#94a3b8" font-size="11">{dt.strftime("%b")}</text>')
        last_month = month_key
for i, item in enumerate(days):
    col, row = i // 7, i % 7
    level = max(0, min(4, int(item.get("level", 0))))
    x, y = left + col * (cell + gap), top + row * (cell + gap)
    delay = col * 0.012 + row * 0.018
    svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{palette[level]}" style="opacity:0;animation:pop .28s ease-out {delay:.3f}s forwards"><title>{html.escape(item.get("date", ""))}: {int(item.get("count", 0))} contributions</title></rect>')
# Keyframes are in the SVG so no JavaScript is needed.
svg.insert(1, '<style>@keyframes pop{from{opacity:0;transform:translate(-2px,-2px)}to{opacity:1;transform:translate(0,0)}} .t{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}</style>')
contrib = int(data.get("stats", {}).get("contributions", sum(int(x.get("count", 0)) for x in days)))
streak = int(data.get("stats", {}).get("current_streak", 0))
legend_y = height - 17
svg.append(f'<text x="18" y="{legend_y + 3}" class="t" fill="#94a3b8" font-size="10">Less</text>')
for j, color in enumerate(palette):
    svg.append(f'<rect x="{49 + j * 15}" y="{legend_y - 9}" width="11" height="11" rx="3" fill="{color}"/>')
svg.append(f'<text x="{width - 215}" y="{legend_y + 3}" class="t" fill="#c9d1d9" font-size="11">{contrib:,} contributions in the last year · streak {streak}d</text>')
svg.append('</svg>')
(ROOT / "contrib-heatmap.svg").write_text("\n".join(svg), encoding="utf-8")
print(ROOT / "contrib-heatmap.svg")

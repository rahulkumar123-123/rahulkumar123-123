from pathlib import Path
from bs4 import BeautifulSoup
import requests, json, re
from datetime import datetime, date, timedelta

ROOT = Path(__file__).resolve().parents[1]
USER = "rahulkumar123-123"
URL = f"https://github.com/users/{USER}/contributions"
OUT = ROOT / "data" / "contributions.json"
response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 profile-art-refresh"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
days = []
for cell in soup.select("[data-date]"):
    raw_date = cell.get("data-date", "")
    if not raw_date:
        continue
    label = cell.get("aria-label", "")
    count_attr = cell.get("data-count")
    match = re.search(r"(\d+) contributions? on", label, re.I)
    if count_attr is not None:
        count = int(count_attr)
    elif match:
        count = int(match.group(1))
    elif label.lower().startswith("no contributions"):
        count = 0
    else:
        count = 0
    try:
        level = int(cell.get("data-level", "0"))
    except ValueError:
        level = 0
    days.append({"date": raw_date, "level": max(0, min(4, level)), "count": count})
if len(days) < 300:
    raise RuntimeError(f"Expected about 365 contribution days, found {len(days)}; refusing to overwrite valid data.")
days = sorted(days, key=lambda item: item["date"])[-371:]
counts = [item["count"] for item in days]
longest = run = 0
for item in days:
    run = run + 1 if item["count"] > 0 else 0
    longest = max(longest, run)
current = 0
for item in reversed(days):
    if item["count"] > 0:
        current += 1
    else:
        break
best_day = max(days, key=lambda item: item["count"])
payload = {"username": USER, "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z", "days": days, "stats": {"contributions": sum(counts), "current_streak": current, "longest_streak": longest, "best_day": best_day}}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"Updated {len(days)} days; {payload['stats']['contributions']} contributions in the last year.")

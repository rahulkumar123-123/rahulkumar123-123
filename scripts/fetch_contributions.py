from pathlib import Path
from bs4 import BeautifulSoup
import requests, json, re
from datetime import datetime

ROOT=Path(__file__).resolve().parents[1]
USER='rahulkumar123-123'
URL=f'https://github.com/users/{USER}/contributions'
out=ROOT/'data/contributions.json'
r=requests.get(URL,headers={'User-Agent':'rahulkumar123-123-profile-art/1.0'},timeout=30)
r.raise_for_status()
soup=BeautifulSoup(r.text,'html.parser')
days=[]
for cell in soup.select('[data-date][data-level]'):
    try:
        days.append({'date':cell.get('data-date'),'level':int(cell.get('data-level','0')),'count':int(re.sub(r'[^0-9]','',cell.get('aria-label','0')) or 0)})
    except ValueError:
        continue
if not days:
    raise RuntimeError('GitHub returned no contribution cells; page structure may have changed.')
# Normalize to the most recent 371 days / 53 weeks.
days=sorted(days,key=lambda x:x['date'])[-371:]
counts=[d['count'] for d in days]
streak=best=cur=0
for d in reversed(days):
    if d['count']>0: cur+=1
    else: break
for d in days:
    if d['count']>0: best=max(best,cur:=cur+1)
    else: cur=0
payload={'username':USER,'generated_at':datetime.utcnow().isoformat(timespec='seconds')+'Z','days':days,'stats':{'contributions':sum(counts),'current_streak':streak,'longest_streak':best,'best_day':max(days,key=lambda x:x['count'])}}
out.write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(f'Wrote {len(days)} contribution days to {out}')

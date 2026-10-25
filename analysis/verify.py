"""Independent numerical checks, including JS vs SciPy and SQL vs raw records."""
import json
import math
import re
import sqlite3
import subprocess
from pathlib import Path
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'dist/data.json').read_text())
code="""
const fs=require('fs'),a=require('./dist/analytics.js'),d=JSON.parse(fs.readFileSync('./dist/data.json'));
const e=a.experiment(d),s=a.summary(d.rows,d.costs),r=a.compare(e[0].act,e[0].n,e[1].act,e[1].n);
const scenarios=[];
for(const fraction of [0,.05,.1,.2,.3])for(const saturation of [.6,1,1.8]){
 const o=a.optimise(a.channels(d),fraction,saturation);
 scenarios.push({fraction,saturation,total:o.total,allocated:o.allocated,base:o.base,expected:o.expected,remaining:o.remaining,
 rows:o.rows.map(c=>({baseline:c.spend,allocation:c.allocated,change:c.change}))});
}
console.log(JSON.stringify({summary:s,experiment:r,arms:e,sampleSize:a.sampleSize(.4,.1),scenarios,
 edges:[a.compare(0,0,2,10),a.compare(0,10,0,10),a.compare(10,10,10,10)]}));
"""
js=json.loads(subprocess.check_output(['node','-e',code],cwd=ROOT,text=True))
rows=data['rows'];arms=[[r for r in rows if r[7]==a] for a in [1,2]]
n1,n2=map(len,arms);x1,x2=[sum(r[4] for r in a) for a in arms]
p1,p2=x1/n1,x2/n2;pool=(x1+x2)/(n1+n2)
z=(p2-p1)/math.sqrt(pool*(1-pool)*(1/n1+1/n2))
assert abs(js['experiment']['p']-2*norm.sf(abs(z)))<2e-7
assert abs(js['experiment']['diff']-(p2-p1))<1e-12
assert abs(js['summary']['rate']-sum(r[4] for r in rows)/len(rows))<1e-12
assert js['sampleSize'] == math.ceil((norm.ppf(.975)*math.sqrt(2*.42*.58)+norm.ppf(.8)*math.sqrt(.4*.6+.44*.56))**2/.04**2)
assert js['edges'][0] is None
assert all(e['p']==1 and all(math.isfinite(v) for v in e['ci']) for e in js['edges'][1:])
for scenario in js['scenarios']:
    assert abs(scenario['total']-scenario['allocated'])<.001
    assert scenario['remaining']<.001
    assert scenario['expected']>=scenario['base']-.001
    for c in scenario['rows']:
        assert abs(c['change'])<=scenario['fraction']+1e-9

db=sqlite3.connect(':memory:')
db.execute('CREATE TABLE users('+','.join(f+' INTEGER' for f in data['fields'])+')')
db.executemany('INSERT INTO users VALUES('+','.join('?' for _ in data['fields'])+')',rows)
db.execute('CREATE TABLE channel_costs(signup_week INTEGER,channel_id INTEGER,acquisition_cost_gbp REAL)')
db.executemany('INSERT INTO channel_costs VALUES(?,?,?)',data['costs'])
sql=re.sub(r'^\s*--[^\n]*', '', (ROOT/'analysis/metrics.sql').read_text(),flags=re.MULTILINE)
statements=[s.strip() for s in sql.split(';') if s.strip()]
results=[]
for statement in statements:
    # All explanatory comments use full stops, avoiding statement delimiters.
    results.append(db.execute(statement).fetchall())
assert len(results[0])==12
assert len(results[1])==43
assert len(results[2])==2
assert len(results[3])==8
assert all(r[1]==0 for r in results[4])
assert sum(r[1] for r in results[0])==len(rows)
assert abs(sum(r[5] for r in results[1])-sum(c[2] for c in data['costs']))<1e-7
print(json.dumps({'status':'passed','checks':['JavaScript p-value matches SciPy','Sample-size formula matches SciPy quantiles','All metric numerators reconcile to raw users','15 budget scenarios preserve total and channel bounds','Zero-denominator and degenerate-rate cases handled','All five SQL queries run and reconcile','All four SQL data-quality checks have zero failures'],'primary_effect_pp':100*(p2-p1),'two_sided_p':2*norm.sf(abs(z)),'planned_sample_per_arm':js['sampleSize']},indent=2))

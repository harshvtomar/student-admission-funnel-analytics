"""Run: python -m src.pipeline. Regenerates only this project's derived outputs."""
import hashlib
import json
from pathlib import Path
import pandas as pd
from .generate import generate, SEED, AS_OF
from .validate import validate
from .database import build_database, ROOT
from .metrics import select,kpis,segment_performance
from .recommendations import recommendations

def run():
    t=generate(); result=validate(t)
    if not result['passed']: raise ValueError(result)
    data=ROOT/'data'; reports=ROOT/'reports'
    data.mkdir(exist_ok=True); reports.mkdir(exist_ok=True)
    hashes={}
    for name,df in t.items():
        path=data/f'{name}.csv.gz'
        df.to_csv(path,index=False,compression={'method':'gzip','mtime':0})
        hashes[name]=hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()
    db=data/'admissions.sqlite'
    if db.exists(): db.unlink()
    con=build_database(t,db)
    for path in sorted((ROOT/'sql').glob('[0-9]*.sql')):
        pd.read_sql_query(path.read_text(),con).to_csv(reports/f'{path.stem}.csv',index=False)
    con.close()
    c,l=select(t)
    (reports/'validation.json').write_text(json.dumps(result,indent=2))
    (reports/'kpis.json').write_text(json.dumps(kpis(c,l),indent=2,allow_nan=False))
    recommendations(c,l).to_csv(reports/'recommendations.csv',index=False)
    (data/'manifest.json').write_text(json.dumps(dict(seed=SEED,as_of=str(AS_OF),counts=result['counts'],canonical_csv_sha256=hashes),indent=2))
    print(json.dumps(result,indent=2)); print(json.dumps(kpis(c,l),indent=2))
if __name__=='__main__': run()

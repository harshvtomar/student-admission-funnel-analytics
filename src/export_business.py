"""Regenerate authoritative reporting inputs and all institutional report packs."""
import json
from pathlib import Path
from .generate import generate
from .metrics import select, kpis, campaign_performance, segment_performance
from .budget import historical_inputs, allocate, scenario_outputs, SCENARIOS
from .client_reports import report_bundle

def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'reports/session2'; out.mkdir(parents=True,exist_ok=True)
    clients=out/'institutions'; clients.mkdir(exist_ok=True)
    t=generate(); c,l=select(t)
    h=historical_inputs(c,l); allocation=allocate(h)
    frames={'campaigns':campaign_performance(c,l), 'channels':segment_performance(c,l,'acquisition_channel'),
        'institutions':segment_performance(c,l,'institution_id'), 'geography':segment_performance(c,l,'geographic_market'),
        'history':h,'allocation':allocation}
    for name,df in frames.items(): df.to_csv(out/(name+'.csv'),index=False)
    payload={name:json.loads(df.to_json(orient='records')) for name,df in frames.items()}
    payload['kpis']=kpis(c,l)
    payload['names']=t['institutions'].set_index('institution_id').institution_name.to_dict()
    payload['scenarios']=[{'scenario':name,'factor':factor,'modeled_enrollments':scenario_outputs(allocation,factor).modeled_enrollments.sum()} for name,factor in SCENARIOS.items()]
    (out/'business_inputs.json').write_text(json.dumps(payload,indent=2))
    for iid in t['institutions'].institution_id:
        (clients/(iid+'_report.zip')).write_bytes(report_bundle(t,c,l,iid))
    print(json.dumps(payload['scenarios'],indent=2))

if __name__=='__main__': main()

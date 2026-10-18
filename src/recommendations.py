"""Deterministic diagnostics, never causal budget prescriptions."""
import pandas as pd
from .metrics import campaign_performance, kpis

def recommendations(c,l):
    if c.empty or l.empty: return pd.DataFrame(columns=['segment','evidence','action'])
    # Eligible campaign-months: every acquired lead has at least 90 days follow-up.
    from .generate import AS_OF
    mc=c[pd.to_datetime(c.end_date)+pd.Timedelta(days=91)<=AS_OF]
    ml=l[l.campaign_id.isin(mc.campaign_id)]
    p=campaign_performance(mc,ml)
    if p.empty: return pd.DataFrame(columns=['segment','evidence','action'])
    base=kpis(mc,ml); rows=[]
    for r in p.sort_values('actual_spend',ascending=False).itertuples():
        if r.leads<100: continue
        if r.lead_to_application<base['lead_to_application']*.8 and r.actual_spend>=p.actual_spend.median():
            rows.append(dict(segment=r.campaign_id,evidence=f'{r.leads} leads; completed application rate {r.lead_to_application:.1%} versus pooled {base["lead_to_application"]:.1%}; spend INR {r.actual_spend:,.0f}',action='Audit targeting and landing-page qualification; test a revised message with a randomized control.'))
        if r.enrolled==0 or r.cpe>base['cpe']*1.5:
            rows.append(dict(segment=r.campaign_id,evidence=f'{r.enrolled} enrollments; spend INR {r.actual_spend:,.0f}; CPE '+('undefined (zero enrollments)' if r.enrolled==0 else f'INR {r.cpe:,.0f} versus pooled INR {base["cpe"]:,.0f}'),action='Review cost and lead quality before considering a controlled budget test.'))
        gap=r.qualified-r.application_started
        if r.qualified and gap/r.qualified>.35:
            rows.append(dict(segment=r.campaign_id,evidence=f'{int(gap)} / {r.qualified} qualified leads have no application start ({gap/r.qualified:.1%})',action='Investigate follow-up delays; test an opt-in counseling reminder.'))
        abandon=r.application_started-r.application_completed
        if r.application_started and abandon/r.application_started>.35:
            rows.append(dict(segment=r.campaign_id,evidence=f'{int(abandon)} / {r.application_started} started applications are incomplete ({abandon/r.application_started:.1%})',action='Inspect application friction and document-upload failures with the institution.'))
    return pd.DataFrame(rows,columns=['segment','evidence','action'])

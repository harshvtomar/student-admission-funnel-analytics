"""Non-mutating diagnostics; exact duplicate repair is explicit and opt-in."""
import pandas as pd
from .generate import AS_OF, STAGES

def deduplicate_exact(df, key):
    clean=df.drop_duplicates().copy()
    if clean[key].duplicated().any(): raise ValueError(f'Conflicting duplicate {key}; manual resolution required')
    return clean

def dates(values):
    return pd.to_datetime(values, format="mixed", errors="coerce")

def validate(t):
    errors=[]
    def check(ok,message):
        if not bool(ok): errors.append(message)
    ids={'institutions':'institution_id','campaigns':'campaign_id','leads':'lead_id','events':'event_id','enrollments':'enrollment_id'}
    for name,key in ids.items():
        check(not t[name][key].duplicated().any(),f'{name}: duplicate identifiers')
        check(not t[name].isna().any().any(),f'{name}: missing data')
    if any('duplicate identifiers' in error for error in errors):
        return {'passed':False,'errors':errors,'counts':{k:len(v) for k,v in t.items()}}
    i,c,l,e,n=[t[k] for k in ids]
    for frame,cols in [(c,['start_date','end_date']),(l,['created_at']),(e,['event_timestamp']),(n,['admission_decision_date','confirmation_date'])]:
        for col in cols: check(dates(frame[col]).notna().all(),f'invalid timestamp {col}')
    for frame,col,parent in [(c,'institution_id',i.institution_id),(l,'campaign_id',c.campaign_id),(l,'institution_id',i.institution_id),(e,'lead_id',l.lead_id),(n,'lead_id',l.lead_id),(n,'institution_id',i.institution_id)]:
        check(frame[col].isin(parent).all(),f'unmatched {col}')
    check(not n.lead_id.duplicated().any(),'duplicated enrollment attribution')
    check(not e.duplicated(['lead_id','event_type']).any(),'duplicated funnel stages')
    check(e.event_type.isin(STAGES).all(),'unknown stage')
    check(e.event_status.eq('achieved').all(),'invalid event status')
    check(n.enrollment_outcome.eq('confirmed').all(),'invalid enrollment outcome')
    joined=l.merge(c,on='campaign_id',suffixes=('_lead','_campaign'))
    check(joined.institution_id_lead.eq(joined.institution_id_campaign).all(),'inconsistent institution attribution')
    check(joined.acquisition_source.eq(joined.acquisition_channel).all(),'inconsistent channel attribution')
    created=dates(joined.created_at)
    check(((created>=dates(joined.start_date))&(created<dates(joined.end_date)+pd.Timedelta(days=1))).all(),'lead outside campaign period')
    check((dates(c.start_date)<=dates(c.end_date)).all(),'invalid campaign period')
    check((c[['budget','actual_spend','impressions','clicks']]>=0).all().all(),'negative campaign quantities')
    check(c.clicks.le(c.impressions).all(),'clicks exceed impressions')
    check(l.groupby('campaign_id').size().reindex(c.campaign_id,fill_value=0).to_numpy().astype(int).__le__(c.clicks.to_numpy()).all(),'leads exceed clicks')
    if not e.empty:
        p=e.pivot_table(index='lead_id',columns='event_type',values='event_timestamp',aggfunc='first').reindex(columns=STAGES)
        times=p.apply(dates)
        for prev,nxt in zip(STAGES,STAGES[1:]):
            check((times[nxt].isna() | (times[prev].notna() & (times[nxt]>times[prev]))).all(),f'invalid transition {prev}->{nxt}')
        base=l.set_index('lead_id').created_at.reindex(times.index)
        check((times.qualified>dates(base)).all(),'events precede lead creation')
        check((dates(e.event_timestamp)<=AS_OF).all(),'future event')
        qualified=set(e.loc[e.event_type=='qualified','lead_id'])
        check(set(l.loc[l.qualification_status=='qualified','lead_id'])==qualified,'qualification status mismatch')
        enrolled=set(e.loc[e.event_type=='enrolled','lead_id'])
        check(set(n.lead_id)==enrolled,'enrollment event mismatch')
        if not n.empty:
            nn=n.merge(l[['lead_id','institution_id']],on='lead_id',suffixes=('','_lead')).set_index('lead_id')
            check(nn.institution_id.eq(nn.institution_id_lead).all(),'enrollment institution mismatch')
            check(dates(nn.confirmation_date).eq(times.enrolled.reindex(nn.index)).all(),'enrollment timestamp mismatch')
            check(dates(nn.admission_decision_date).eq(times.offer.reindex(nn.index)).all(),'offer timestamp mismatch')
    allocated=c.groupby('institution_id').budget.sum().reindex(i.institution_id,fill_value=0)
    check((allocated.to_numpy()==i.campaign_budget_allocation.to_numpy()).all(),'institution budget mismatch')
    return {'passed':not errors,'errors':errors,'counts':{k:len(v) for k,v in t.items()}}

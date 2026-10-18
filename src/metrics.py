"""Explicit grain separation. No allocation of spend to geographic slices."""
import numpy as np
import pandas as pd
from .generate import AS_OF, STAGES

def ratio(n, d):
    return float(n/d) if pd.notna(n) and pd.notna(d) and d else np.nan

def lead_facts(tables):
    l=tables['leads'].copy()
    e=tables['events']
    for stage in STAGES:
        l[stage]=l.lead_id.isin(e.loc[(e.event_type==stage)&(e.event_status=='achieved'),'lead_id']).astype(int)
    l['month']=l.created_at.str[:7]
    l['mature']=(AS_OF-pd.to_datetime(l.created_at)).dt.total_seconds()>=90*86400
    return l

def select(tables, institutions=None, channels=None, campaigns=None, months=None, geography=None, mature_only=False):
    """Filter complete campaign-months; maturity option keeps fully mature campaigns."""
    c=tables['campaigns'].copy()
    for col,values in [('institution_id',institutions),('acquisition_channel',channels),('campaign_id',campaigns)]:
        if values is not None: c=c[c[col].isin(values)]
    if months is not None: c=c[c.start_date.str[:7].isin(months)]
    if mature_only: c=c[pd.to_datetime(c.end_date)+pd.Timedelta(days=91)<=AS_OF]
    l=lead_facts(tables)
    l=l[l.campaign_id.isin(c.campaign_id)]
    if geography is not None: l=l[l.geographic_market.isin(geography)]
    return c,l

def kpis(c,l, costs_available=True):
    out={'leads':int(l.lead_id.nunique())}
    out.update({s:int(l[s].sum()) for s in STAGES})
    for name,num,den in [('qualified_rate','qualified','leads'),('application_start_rate','application_started','qualified'),('application_completion_rate','application_completed','application_started'),('lead_to_application','application_completed','leads'),('application_to_enrollment','enrolled','application_completed'),('lead_to_enrollment','enrolled','leads')]:
        out[name]=ratio(out[num],out[den])
    for col in ['actual_spend','budget','impressions','clicks']:
        out[col]=float(c[col].sum()) if costs_available else np.nan
    for name,num,den in [('ctr','clicks','impressions'),('cpc','actual_spend','clicks'),('cpl','actual_spend','leads'),('cost_per_application','actual_spend','application_completed'),('cpe','actual_spend','enrolled'),('budget_utilization','actual_spend','budget')]:
        out[name]=ratio(out[num],out[den])
    return out

def campaign_performance(c,l):
    grouped={key:g for key,g in l.groupby('campaign_id')}
    return pd.DataFrame([dict(campaign_id=row.campaign_id,institution_id=row.institution_id,acquisition_channel=row.acquisition_channel,month=row.start_date[:7],**kpis(c[c.campaign_id==row.campaign_id],grouped.get(row.campaign_id,l.iloc[:0]))) for row in c.itertuples()])

def segment_performance(c,l,dimension):
    if dimension in ['geographic_market','month','mature']:
        return pd.DataFrame([dict(segment=str(key),**kpis(c,g,False)) for key,g in l.groupby(dimension)])
    lead_dim='acquisition_source' if dimension=='acquisition_channel' else dimension
    return pd.DataFrame([dict(segment=key,**kpis(g,l[l[lead_dim]==key])) for key,g in c.groupby(dimension)])

def funnel(k):
    labels=['Leads','Qualified leads','Applications started','Applications completed','Admission offers','Enrollments']
    counts=[k['leads']]+[k[s] for s in STAGES]
    result=pd.DataFrame({'stage':labels,'students':counts})
    result['conversion_from_previous']=result.students/result.students.shift(1).replace(0,np.nan)
    result['drop_off']=result.students.shift(1)-result.students
    result['drop_off_pct']=1-result.conversion_from_previous
    return result

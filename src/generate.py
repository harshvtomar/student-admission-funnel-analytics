"""Deterministic portfolio simulation; no empirical calibration or personal data."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20261018
AS_OF = pd.Timestamp('2025-12-31 23:59:59')
STAGES = ['qualified', 'application_started', 'application_completed', 'offer', 'enrolled']
CHANNELS = ['Google Search', 'Meta Ads', 'Organic Search', 'Referral', 'Email', 'Education webinars', 'Display Ads']
MARKETS = ['Delhi NCR','Maharashtra','Karnataka','Tamil Nadu','Uttar Pradesh','Rajasthan','West Bengal','Telangana']
LOCATIONS = [('Delhi','New Delhi'),('Maharashtra','Pune'),('Karnataka','Bengaluru'),('Tamil Nadu','Chennai'),('Uttar Pradesh','Lucknow'),('Rajasthan','Jaipur'),('West Bengal','Kolkata'),('Telangana','Hyderabad')]

def generate(n_leads=50000, seed=SEED):
    r = np.random.default_rng(seed)
    institutions = pd.DataFrame([dict(institution_id=f'I{i+1:03}', institution_name=f'CampusGrowth Demo Institute {i+1:02}', state=LOCATIONS[i%8][0],city=LOCATIONS[i%8][1], institution_category=['Private university','Autonomous college','Specialist institute'][i%3],course_segment=['Engineering','Management','Multidisciplinary'][i%3]) for i in range(24)])
    campaigns=[]
    for i in range(120):
        start=pd.Timestamp(2025, i//10+1, 1)
        end=start+pd.offsets.MonthEnd(0)
        budget=int(r.integers(80000,250001))
        campaigns.append(dict(campaign_id=f'C{i+1:03}',institution_id=f'I{i%24+1:03}', acquisition_channel=CHANNELS[i%7],campaign_objective=['Lead acquisition','Application completion','Enrollment consideration'][i%3],start_date=str(start.date()),end_date=str(end.date()),budget=budget,actual_spend=round(budget*r.uniform(.65,1.12),2)))
    campaigns=pd.DataFrame(campaigns)
    sizes=r.multinomial(n_leads, r.dirichlet(np.ones(120)*12))
    leads=[]; events=[]; enrollments=[]
    for c,count in zip(campaigns.to_dict('records'),sizes):
        channel=CHANNELS.index(c['acquisition_channel'])
        quality=[.66,.49,.65,.73,.58,.71,.43][channel] * r.uniform(.88,1.1)
        completion=r.uniform(.60,.82)
        for _ in range(count):
            lid=f'L{len(leads)+1:06}'
            start=pd.Timestamp(c['start_date'])
            created=start+pd.Timedelta(seconds=int(r.integers(0,(pd.Timestamp(c['end_date']).day)*86400)))
            record=dict(lead_id=lid,created_at=str(created),acquisition_source=c['acquisition_channel'],campaign_id=c['campaign_id'],institution_id=c['institution_id'],geographic_market=MARKETS[int(r.integers(8))],course_preference=['Engineering','MBA','Arts & Science','Commerce'][int(r.integers(4))],qualification_status='not_qualified')
            t=created; offer_date=None
            for stage,prob in zip(STAGES,[quality,.69,completion,.76,.56]):
                if r.random()>prob: break
                t+=pd.Timedelta(days=int(r.integers(1,15)),hours=int(r.integers(0,12)))
                if t>AS_OF: break
                events.append(dict(event_id=f'E{len(events)+1:07}',lead_id=lid,event_type=stage,event_timestamp=str(t),event_status='achieved'))
                if stage=='qualified': record['qualification_status']='qualified'
                if stage=='offer': offer_date=t
                if stage=='enrolled':
                    enrollments.append(dict(enrollment_id=f'N{len(enrollments)+1:06}',lead_id=lid,institution_id=c['institution_id'],admission_decision_date=str(offer_date),confirmation_date=str(t),enrollment_outcome='confirmed'))
            leads.append(record)
    campaigns['clicks']=[int(n*r.uniform(5,12)) for n in sizes]
    campaigns['impressions']=[int(n/r.uniform(.015,.06)) for n in campaigns.clicks]
    institutions['campaign_budget_allocation']=institutions.institution_id.map(campaigns.groupby('institution_id').budget.sum())
    return dict(institutions=institutions,campaigns=campaigns,leads=pd.DataFrame(leads),events=pd.DataFrame(events,columns=['event_id','lead_id','event_type','event_timestamp','event_status']),enrollments=pd.DataFrame(enrollments,columns=['enrollment_id','lead_id','institution_id','admission_decision_date','confirmation_date','enrollment_outcome']))

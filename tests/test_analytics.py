from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd
import pytest
from src.generate import generate, STAGES
from src.validate import validate,deduplicate_exact
from src.metrics import select,kpis,ratio,lead_facts,campaign_performance
from src.database import build_database,ROOT
from src.recommendations import recommendations

@pytest.fixture(scope='session')
def t(): return generate()
@pytest.fixture(scope='session')
def db(t):
    con=build_database(t); yield con; con.close()

def test_reproducibility():
    a,b=generate(600),generate(600)
    for name in a: pd.testing.assert_frame_equal(a[name],b[name])

def test_seed_changes_population():
    assert not generate(500,1)['leads'].equals(generate(500,2)['leads'])

def test_full_validation(t): assert validate(t)['passed']

@pytest.mark.parametrize('name,key',[('institutions','institution_id'),('campaigns','campaign_id'),('leads','lead_id'),('events','event_id'),('enrollments','enrollment_id')])
def test_unique_ids(t,name,key): assert t[name][key].is_unique

def test_foreign_keys(db): assert db.execute('PRAGMA foreign_key_check').fetchall()==[]

def test_sql_constraints(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO events VALUES ('BAD','nonexistent','qualified','2025-01-01','achieved')")
    db.rollback()

def test_chronology_detects_mutation(t):
    bad={k:v.copy() for k,v in t.items()}; bad['events'].loc[0,'event_timestamp']='2024-01-01'
    assert not validate(bad)['passed']

def test_missing_detected(t):
    bad={k:v.copy() for k,v in t.items()}; bad['leads'].loc[0,'geographic_market']=None
    assert 'leads: missing data' in validate(bad)['errors']

def test_unmatched_detected(t):
    bad={k:v.copy() for k,v in t.items()}; bad['leads'].loc[0,'campaign_id']='UNKNOWN'
    assert 'unmatched campaign_id' in validate(bad)['errors']

def test_invalid_transition(t):
    bad={k:v.copy() for k,v in t.items()}
    lead=bad['events'].loc[bad['events'].event_type=='enrolled','lead_id'].iloc[0]
    bad['events']=bad['events'][~((bad['events'].lead_id==lead)&(bad['events'].event_type=='application_completed'))]
    assert not validate(bad)['passed']

def test_conflicting_duplicates():
    with pytest.raises(ValueError): deduplicate_exact(pd.DataFrame({'id':[1,1],'x':[1,2]}),'id')

def test_exact_duplicates():
    assert len(deduplicate_exact(pd.DataFrame({'id':[1,1],'x':[2,2]}),'id'))==1

def test_attribution(t):
    l=lead_facts(t)
    assert l.lead_id.is_unique and len(l)==50000
    assert l.enrolled.sum()==len(t['enrollments'])

@pytest.mark.parametrize('n,d',[(5,0),(0,0),(np.nan,2),(2,np.nan)])
def test_undefined_ratios(n,d): assert np.isnan(ratio(n,d))

def test_independent_fixture():
    # Four unique students, two completed applications, one enrollment; spend 1200.
    c=pd.DataFrame({'actual_spend':[1000,200],'budget':[1000,400],'impressions':[10000,2000],'clicks':[1000,200]})
    l=pd.DataFrame({'lead_id':['A','B','C','D'],'qualified':[1,1,1,0],'application_started':[1,1,0,0],'application_completed':[1,1,0,0],'offer':[1,0,0,0],'enrolled':[1,0,0,0]})
    k=kpis(c,l)
    assert k['cpe']==1200 and k['cpl']==300 and k['cost_per_application']==600
    assert k['lead_to_enrollment']==.25 and k['application_to_enrollment']==.5
    assert k['application_start_rate']==pytest.approx(2/3)
    assert k['application_completion_rate']==1 and k['ctr']==.1
    assert np.isnan(kpis(c,l,False)['cpe'])

def test_zero_enrollment_fixture():
    c=pd.DataFrame({'actual_spend':[200],'budget':[300],'impressions':[1000],'clicks':[50]})
    l=pd.DataFrame({'lead_id':['A'],**{s:[0] for s in STAGES}})
    k=kpis(c,l)
    assert np.isnan(k['cpe']) and k['lead_to_enrollment']==0

def test_spend_not_multiplied(t):
    c,l=select(t); p=campaign_performance(c,l)
    assert p.actual_spend.sum()==pytest.approx(t['campaigns'].actual_spend.sum())
    assert p.leads.sum()==len(t['leads'])

def test_filters(t):
    c,l=select(t,institutions=['I001'],channels=['Google Search'])
    assert c.institution_id.eq('I001').all() and c.acquisition_channel.eq('Google Search').all()
    assert l.campaign_id.isin(c.campaign_id).all()
    c,l=select(t,campaigns=['C001'],geography=['Delhi NCR'])
    assert not l.empty and l.geographic_market.eq('Delhi NCR').all()

def test_maturity_filter(t):
    c,l=select(t,mature_only=True)
    assert l.mature.all() and set(c.start_date.str[:7])=={f'2025-{i:02}' for i in range(1,10)}

def test_empty_selection(t):
    c,l=select(t,months=[]); k=kpis(c,l)
    assert c.empty and l.empty and k['leads']==0 and np.isnan(k['cpe'])
    assert recommendations(c,l).empty

def test_recent_no_recommendations(t):
    c,l=select(t,months=['2025-12']); assert recommendations(c,l).empty

def test_sql_python_campaign_reconciliation(t,db):
    c,l=select(t); py=campaign_performance(c,l).set_index('campaign_id').sort_index()
    sql=pd.read_sql_query('SELECT * FROM campaign_performance',db).set_index('campaign_id').sort_index()
    for col in ['actual_spend','leads','qualified','application_started','application_completed','offer','enrolled','cpl','cpe','lead_to_enrollment']:
        np.testing.assert_allclose(py[col],sql[col],equal_nan=True)

@pytest.mark.parametrize('query',sorted((ROOT/'sql').glob('[0-9]*.sql')),ids=lambda p:p.stem)
def test_queries_execute(db,query):
    assert not pd.read_sql_query(query.read_text(),db).empty

def test_cohort_reconciliation(t,db):
    py=lead_facts(t).groupby(['month','mature']).agg(leads=('lead_id','size'),enrollments=('enrolled','sum')).reset_index()
    sql=pd.read_sql_query((ROOT/'sql/10_cohort_conversion.sql').read_text(),db)
    assert py.leads.tolist()==sql.leads.tolist() and py.enrollments.tolist()==sql.enrollments.tolist()

def test_channel_reconciliation(t,db):
    c,l=select(t)
    for dimension in ['acquisition_channel','institution_id']:
        from src.metrics import segment_performance
        py=segment_performance(c,l,dimension).set_index('segment').sort_index()
        sql=pd.read_sql_query(f'SELECT {dimension} segment,SUM(actual_spend) actual_spend,SUM(enrolled) enrolled,SUM(leads) leads FROM campaign_performance GROUP BY {dimension}',db).set_index('segment').sort_index()
        np.testing.assert_allclose(py[sql.columns],sql)

def test_recommendations_deterministic(t):
    c,l=select(t)
    a,b=recommendations(c,l),recommendations(c,l)
    pd.testing.assert_frame_equal(a,b)
    assert not a.empty and a.evidence.str.len().min()>10

def test_invalid_timestamp_diagnostic(t):
    bad={k:v.copy() for k,v in t.items()}; bad['events'].loc[0,'event_timestamp']='not-a-date'
    assert 'invalid timestamp event_timestamp' in validate(bad)['errors']

def test_manifest_matches(t):
    import json,hashlib
    manifest=json.loads((ROOT/'data/manifest.json').read_text())
    for name,df in t.items():
        assert hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()==manifest['canonical_csv_sha256'][name]

def test_remaining_sql_reports_reconcile(t,db):
    c,l=select(t); p=campaign_performance(c,l); k=kpis(c,l)
    def query(n): return pd.read_sql_query(next((ROOT/'sql').glob(f'{n:02}_*.sql')).read_text(),db)
    monthly=p.groupby('month')[['actual_spend','leads','application_completed','enrolled']].sum()
    np.testing.assert_allclose(monthly.to_numpy(),query(2).set_index('month')[['spend','leads','applications','enrollments']].to_numpy())
    unique=query(3).iloc[0]
    assert unique['leads']==k['leads'] and unique.enrollments==k['enrolled']
    assert unique.conversion==pytest.approx(k['lead_to_enrollment'])
    for n,den,col in [(5,'leads','cpl'),(6,'enrolled','cpe')]:
        expected=p.groupby('acquisition_channel').apply(lambda g:g.actual_spend.sum()/g[den].sum(),include_groups=False)
        np.testing.assert_allclose(query(n).set_index('acquisition_channel')[col],expected)
    abandonment=l.groupby('institution_id')[['application_started','application_completed']].sum()
    sql=query(7).set_index('institution_id')
    np.testing.assert_allclose(sql.incomplete,abandonment.application_started-abandonment.application_completed)
    geo=l.groupby('geographic_market').enrolled.agg(['size','sum'])
    np.testing.assert_allclose(query(8)[['leads','enrollments']],geo[['size','sum']])
    np.testing.assert_allclose(query(9).utilization,c.actual_spend/c.budget)
    mc,ml=select(t,mature_only=True); mp=campaign_performance(mc,ml); mk=kpis(mc,ml)
    expected=set(mp.loc[(mp.leads>=100)&((mp.enrolled==0)|(mp.cpe>mk['cpe']*1.5)),'campaign_id'])
    assert set(query(11).campaign_id)==expected
    summary=query(12).iloc[0]
    for sql_key,py_key in [('spend','actual_spend'),('budget','budget'),('impressions','impressions'),('clicks','clicks'),('leads','leads'),('applications','application_completed'),('enrollments','enrolled'),('cpe','cpe'),('conversion','lead_to_enrollment')]:
        assert summary[sql_key]==pytest.approx(k[py_key])

def test_duplicate_lead_diagnostic(t):
    bad={k:v.copy() for k,v in t.items()}
    bad['leads']=pd.concat([bad['leads'],bad['leads'].iloc[:1]],ignore_index=True)
    assert 'leads: duplicate identifiers' in validate(bad)['errors']

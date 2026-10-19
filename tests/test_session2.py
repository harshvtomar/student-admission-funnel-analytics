import io
from zipfile import ZipFile
import pandas as pd
import pytest
from src.budget import allocate, scenario_outputs, historical_inputs
from src.client_reports import institution_report, report_bundle
from src.generate import generate
from src.metrics import select

@pytest.fixture
def history():
    return pd.DataFrame({'segment':['A','B','C'], 'eligible':[True]*3,
        'cpe':[100.,200.,400.], 'cost_per_qualified_lead':[10.,20.,40.],
        'cost_per_application':[50.,100.,200.]})

def test_exact_bounded_optimum(history):
    p=allocate(history,1000,.1,.6)
    assert p.recommended_budget.tolist()==[600,300,100]
    assert p.recommended_budget.sum()==1000
    assert scenario_outputs(p).modeled_enrollments.sum()==7.75

def test_paise_preserved(history):
    p=allocate(history,1234.57,.05,.7)
    assert round(p.recommended_budget.sum()*100)==123457
    assert p.recommended_share.between(.05,.7).all()

@pytest.mark.parametrize('budget,lo,hi',[(0,0,1),(100,.4,.5),(100,0,.3),(100,-.1,1),(float('nan'),0,1),(100,.5,.2)])
def test_invalid_constraints(history,budget,lo,hi):
    with pytest.raises(ValueError): allocate(history,budget,lo,hi)

def test_scenarios_are_assumptions(history):
    p=allocate(history,1000,.1,.6)
    assert scenario_outputs(p,1.25).modeled_enrollments.sum()==pytest.approx(7.75/1.25)
    assert scenario_outputs(p,.85).modeled_enrollments.sum()==pytest.approx(7.75/.85)
    with pytest.raises(ValueError): scenario_outputs(p,0)

def test_ineligible_excluded(history):
    history.loc[0,'eligible']=False
    assert allocate(history,1000,0,1).segment.tolist()==['B','C']
    with pytest.raises(ValueError): allocate(pd.DataFrame())

def test_maturity_and_report_scope():
    t=generate(); c,l=select(t)
    h=historical_inputs(c,l)
    mc,ml=select(t,mature_only=True)
    assert h.leads.sum()==len(ml)
    iid=c.institution_id.iloc[0]
    html,p=institution_report(t,c,l,iid)
    assert p.institution_id.eq(iid).all()
    assert p.leads.sum()==len(l[l.institution_id==iid])
    assert 'Portfolio simulation' in html
    with ZipFile(io.BytesIO(report_bundle(t,c,l,iid))) as z:
        assert z.read('report.html').decode()==html
        assert len(pd.read_csv(z.open('campaign_scorecard.csv')))==len(p)
    with pytest.raises(ValueError): institution_report(t,c,l,'INVALID')

def test_dashboard_budget_constraints_and_client_export():
    from streamlit.testing.v1 import AppTest
    from pathlib import Path
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=30).run()
    app.radio[0].set_value('Growth Recommendations').run()
    assert not app.exception
    app.number_input[2].set_value(10.0).run()
    assert any('Infeasible' in w.value for w in app.warning)
    app.radio[0].set_value('University Client Performance').run()
    assert not app.exception
    assert len(app.selectbox[0].options)==24
    assert len(app.get('download_button'))>=3

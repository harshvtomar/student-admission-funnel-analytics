import pytest
from streamlit.testing.v1 import AppTest
from src.database import ROOT
PAGES=['Executive Overview','Student Admission Funnel','Campaign Performance','Marketing Channel Analytics','University Client Performance','Geographic & Cohort Analytics','Growth Recommendations']
@pytest.mark.parametrize('page',PAGES)
def test_page_renders(page):
    at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=60).run()
    at.sidebar.radio[0].set_value(page).run()
    assert not at.exception
    assert at.title[0].value=='AdmissionFlow Intelligence'

def test_dashboard_empty_state():
    at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=60).run()
    at.sidebar.multiselect[0].set_value([]).run()
    assert not at.exception and 'No campaigns' in at.warning[0].value

def test_dashboard_filters():
    at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=60).run()
    original=at.metric[1].value
    at.sidebar.multiselect[0].set_value(['2025-01']).run()
    assert not at.exception and at.metric[1].value!=original
    at.sidebar.checkbox[0].check().run()
    assert not at.exception

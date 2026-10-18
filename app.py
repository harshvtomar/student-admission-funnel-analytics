"""AdmissionFlow Intelligence — CampusGrowth Analytics portfolio simulation."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.database import load_tables
from src.generate import generate
from src.metrics import select,kpis,campaign_performance,segment_performance,funnel
from src.recommendations import recommendations

st.set_page_config(page_title='AdmissionFlow Intelligence',page_icon='🎓',layout='wide')
st.markdown('''<style>
.stApp {background:#f6f8fc;color:#182b49} [data-testid="stSidebar"]{background:#eaf0f8}
[data-testid="stMetric"]{background:white;padding:18px;border-radius:12px;border:1px solid #dfe7f1}
[data-testid="stMetricValue"]{color:#135cc5} h1,h2,h3{letter-spacing:-.03em}
</style>''',unsafe_allow_html=True)
@st.cache_data
def data():
    path=Path(__file__).parent/'data/admissions.sqlite'
    return load_tables(path) if path.exists() else generate()

def money(v):
    if pd.isna(v): return 'N/A'
    if abs(v)>=100000: return f'₹{v/100000:,.2f} L'
    return f'₹{v:,.0f}'

def chart(fig):
    fig.update_layout(template='plotly_white',font=dict(family='Arial',color='#182b49'),margin=dict(l=10,r=10,t=40,b=20),colorway=['#2563eb','#0caa91','#ffb547','#875ce5'])
    st.plotly_chart(fig,width='stretch')

def table(df,name):
    st.dataframe(df,width='stretch',hide_index=True)
    st.download_button('Download CSV',df.to_csv(index=False).encode(),name+'.csv','text/csv',key=name)

t=data()
st.sidebar.markdown('### 🎓 AdmissionFlow\nCampusGrowth Analytics')
PAGES=['Executive Overview','Student Admission Funnel','Campaign Performance','Marketing Channel Analytics','University Client Performance','Geographic & Cohort Analytics','Growth Recommendations']
page=st.sidebar.radio('Workspace',PAGES)
st.sidebar.divider()
months=st.sidebar.multiselect('Campaign months',sorted(t['campaigns'].start_date.str[:7].unique()),default=sorted(t['campaigns'].start_date.str[:7].unique()))
inst=st.sidebar.multiselect('Institutions',t['institutions'].institution_id.tolist(),format_func=lambda x: t['institutions'].set_index('institution_id').loc[x,'institution_name'])
channels=st.sidebar.multiselect('Channels',sorted(t['campaigns'].acquisition_channel.unique()))
cids=st.sidebar.multiselect('Campaigns',t['campaigns'].campaign_id.tolist())
mature=st.sidebar.checkbox('Fully mature campaign cohorts only',value=False,help='Keeps campaign-months ending at least 91 days before the snapshot. Every lead then has at least 90 days follow-up.')
st.sidebar.caption('Empty institution/channel/campaign choices = all. Empty month choice = no data.')
c,l=select(t,institutions=inst or None,channels=channels or None,campaigns=cids or None,months=months,mature_only=mature)
k=kpis(c,l)
st.caption('CAMPUSGROWTH ANALYTICS  /  PORTFOLIO SIMULATION')
st.title('AdmissionFlow Intelligence')
st.markdown('**Student Acquisition · Campaign Performance · Enrollment Analytics**')
st.info('Synthetic data • Fictional institutions and students • Jan–Dec 2025 activity • Outcomes observed through 31 Dec 2025 • No affiliation with KollegeApply')
st.header(page)
st.caption(f'{len(c):,} campaign-months · {len(l):,} unique leads · Primary acquisition campaign attribution · '+('Fully mature campaign cohorts' if mature else 'Includes incomplete recent cohorts; observed-to-date outcomes'))
if c.empty:
    st.warning('No campaigns match these filters. Select at least one month or broaden the filters.')
    st.stop()
if page=='Executive Overview':
    metrics=[('Marketing spend',money(k['actual_spend'])),('Unique leads',f"{k['leads']:,}"),('Completed applications',f"{k['application_completed']:,}"),('Confirmed enrollments',f"{k['enrolled']:,}"),('Cost per enrollment',money(k['cpe'])),('Lead → enrollment','N/A' if pd.isna(k['lead_to_enrollment']) else f"{k['lead_to_enrollment']:.1%}")]
    for cols,chunk in [(st.columns(3),metrics[:3]),(st.columns(3),metrics[3:])]:
        for col,(label,value) in zip(cols,chunk): col.metric(label,value)
    p=campaign_performance(c,l)
    monthly=p.groupby('month',as_index=False)[['leads','application_completed','enrolled','actual_spend']].sum()
    left,right=st.columns([2,1])
    with left: chart(px.line(monthly,x='month',y=['leads','application_completed','enrolled'],markers=True,title='Acquisition cohorts · outcomes to snapshot'))
    with right: chart(px.bar(monthly,x='month',y='actual_spend',title='Campaign spend · INR'))
    st.subheader('Management review')
    st.write(f"{k['qualified']:,} leads qualified; {k['application_started']-k['application_completed']:,} started applications remain incomplete at the snapshot.")
    st.write(f"Budget utilization is {k['budget_utilization']:.1%}. These are cost-efficiency measures; tuition revenue and ROI are not modeled.")
    rec=recommendations(c,l)
    for r in rec.head(3).itertuples(): st.markdown(f'**{r.segment}** — {r.evidence}. {r.action}')
    table(monthly,'monthly_overview')
elif page=='Student Admission Funnel':
    geo=st.multiselect('Student geography (conversion only)',sorted(l.geographic_market.unique()))
    fl=l[l.geographic_market.isin(geo)] if geo else l
    if fl.empty: st.warning('No students in this selection.'); st.stop()
    if not geo:
        st.write(f"**Aggregate reach:** {int(k['impressions']):,} impressions → {int(k['clicks']):,} clicks · CTR {k['ctr']:.2%} · click-to-lead ratio {k['leads']/k['clicks']:.2%}")
        st.caption('Impressions and clicks are campaign-level interactions, not distinct people. Student funnel below counts unique leads; click-to-lead is a cross-grain ratio, not a person conversion probability.')
    else: st.caption('Campaign reach and cost metrics suppressed: geographic delivery allocation is unavailable.')
    f=funnel(kpis(c,fl,not bool(geo)))
    chart(go.Figure(go.Funnel(y=f.stage,x=f.students,textinfo='value+percent initial',marker_color='#2563eb')))
    worst=f.dropna(subset=['drop_off_pct']).sort_values('drop_off_pct',ascending=False).iloc[0]
    st.warning(f"Largest proportional stage gap: {worst.stage} · {worst.drop_off_pct:.1%} not yet progressed. Recent leads may still convert.")
    table(f,'funnel')
elif page=='Campaign Performance':
    p=campaign_performance(c,l)
    chart(px.scatter(p,x='lead_to_enrollment',y='cpe',size='actual_spend',color='acquisition_channel',hover_name='campaign_id',hover_data=['leads','enrolled'],labels={'cpe':'Cost per enrollment (INR)','lead_to_enrollment':'Lead-to-enrollment rate'},title='Cost and conversion · undefined CPE excluded from chart'))
    st.caption('Use the mature-cohort filter for comparisons. Zero-enrollment campaigns remain visible in the table with undefined CPE.')
    table(p,'campaign_scorecards')
elif page=='Marketing Channel Analytics':
    p=segment_performance(c,l,'acquisition_channel')
    chart(px.bar(p,x='segment',y='cpe',color='segment',title='Channel cost per enrollment · INR'))
    chart(px.bar(p,x='segment',y='lead_to_enrollment',title='Observed student conversion'))
    st.caption('Organic, referral, email and webinar spend includes simulated content, incentives and operating costs. Channel differences are generator assumptions, not real-world effectiveness.')
    table(p,'channel_performance')
elif page=='University Client Performance':
    p=segment_performance(c,l,'institution_id').merge(t['institutions'][['institution_id','institution_name']],left_on='segment',right_on='institution_id')
    chart(px.bar(p.sort_values('enrolled'),x='enrolled',y='institution_name',orientation='h',title='Institution enrollments',height=700))
    table(p,'institution_performance')
elif page=='Geographic & Cohort Analytics':
    g=segment_performance(c,l,'geographic_market')
    chart(px.bar(g,x='segment',y='lead_to_enrollment',hover_data=['leads','enrolled'],title='Territory conversion · fictional population'))
    table(g.drop(columns=['actual_spend','budget','impressions','clicks','ctr','cpc','cpl','cost_per_application','cpe','budget_utilization']),'territories')
    cohort=l.groupby(['month','mature'],as_index=False).agg(leads=('lead_id','nunique'),enrollments=('enrolled','sum'))
    cohort['conversion']=cohort.enrollments/cohort.leads
    cohort['follow_up']=cohort.mature.map({True:'At least 90 days',False:'Under 90 days — incomplete'})
    chart(px.bar(cohort,x='month',y='conversion',color='follow_up',barmode='group',hover_data=['leads','enrollments'],title='Cohort conversion and follow-up maturity'))
    st.caption('Month is lead acquisition month. Comparisons are observed-to-date, not standardized 90-day survival estimates; no real market demand can be inferred.')
    table(cohort,'cohorts')
else:
    st.write('Evidence-backed investigation queue · fully mature campaign-months · minimum 100 leads per campaign')
    rec=recommendations(c,l)
    if rec.empty: st.info('No eligible recommendations for the current selection. Broaden filters to include mature campaigns.')
    else:
        for r in rec.head(12).itertuples():
            with st.container(border=True):
                st.markdown(f'**{r.segment} · Investigate**')
                st.write(r.evidence); st.caption(r.action)
        table(rec,'growth_recommendations')
    st.warning('Associations do not establish causal impact. Validate any change through controlled testing; this is not an automatic budget optimizer.')
with st.expander('Metric definitions and reporting rules'):
    st.markdown('''All filters select complete campaign-months. Spend, impressions and clicks are summed once per campaign. Leads have a single primary campaign. Applications mean **completed applications** unless marked started. Outcomes include events up to 31 Dec 2025 for the selected acquired leads, including events after campaign end. Zero denominators display N/A. Maturity means at least 90 days since acquisition; complete-campaign maturity uses a conservative 91-day end-date rule. Application-start rate = starts / qualified; completion rate = completed / started; lead-to-application = completed / leads; application-to-enrollment = enrollments / completed. No tuition ROI is calculated.''')

"""Portable, escaped HTML client reports; no browser or PDF dependency."""
from html import escape
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from .metrics import kpis, campaign_performance, funnel
from .recommendations import recommendations

def institution_report(tables, c, l, institution_id):
    names = tables['institutions'].set_index('institution_id').institution_name
    if institution_id not in names.index:
        raise ValueError('Unknown institution.')
    c = c[c.institution_id == institution_id]
    l = l[l.campaign_id.isin(c.campaign_id)]
    if c.empty:
        raise ValueError('No campaigns for this institution in the selected scope.')
    k = kpis(c, l)
    p = campaign_performance(c, l)
    rec = recommendations(c, l)
    scope = ', '.join(sorted(c.start_date.str[:7].unique()))
    actions = ''.join('<li>' + escape(str(r.evidence)) + ' — ' + escape(str(r.action)) + '</li>' for r in rec.itertuples())
    if not actions:
        actions = '<li>No mature campaign flags meet the investigation rules. Review follow-up and recent cohorts before changing budgets.</li>'
    summary = f"Spend INR {k['actual_spend']:,.2f} · {k['leads']:,} leads · {k['application_completed']:,} completed applications · {k['enrolled']:,} enrollments"
    html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(names[institution_id])} | AdmissionFlow</title><style>body{{font:16px Arial;max-width:1100px;margin:40px auto;padding:0 20px;color:#182b49}}h1,h2{{color:#135cc5}}table{{border-collapse:collapse;font-size:13px}}th,td{{padding:9px;border-bottom:1px solid #ddd;text-align:left}}.scroll{{overflow:auto}}@media print{{body{{margin:0}}}}</style>
<h1>{escape(names[institution_id])}</h1><p>CampusGrowth Analytics · Portfolio simulation · Fictional data · No affiliation with KollegeApply.</p>
<h2>Performance at 31 December 2025</h2><p>{summary}</p>
<p>Lead-to-enrollment: {k['lead_to_enrollment']:.2%} · Cost per completed application: INR {k['cost_per_application']:,.2f} · Cost per enrollment: INR {k['cpe']:,.2f}</p>
<p>Campaign months: {escape(scope)}. Channels: {escape(', '.join(sorted(c.acquisition_channel.unique())))}. Campaigns: {escape(', '.join(c.campaign_id))}.</p>
<p>Primary acquisition attribution; costs summed once per campaign. Outcomes through the snapshot; recent cohorts may still convert. Undefined ratios appear as NaN. These associations do not establish causal impact.</p>
<h2>Student funnel</h2>{funnel(k).to_html(index=False, float_format=lambda v: f'{v:,.3f}')}
<h2>Campaign scorecard</h2><div class="scroll">{p[['campaign_id','acquisition_channel','actual_spend','leads','qualified','application_completed','enrolled','cpe']].to_html(index=False,float_format=lambda v:f'{v:,.2f}')}</div>
<h2>Issues and recommended actions</h2><p>Investigation rules use fully mature campaign-months and at least 100 leads.</p><ul>{actions}</ul>
<p>Before implementation, validate CRM follow-up, lead quality and attribution. Test changes with a controlled experiment; no tuition ROI or future improvement is claimed.</p></html>'''
    return html, p

def report_bundle(tables, c, l, institution_id):
    html, scorecard = institution_report(tables, c, l, institution_id)
    buffer = BytesIO()
    with ZipFile(buffer, 'w', ZIP_DEFLATED) as z:
        z.writestr('report.html', html)
        z.writestr('campaign_scorecard.csv', scorecard.to_csv(index=False))
        z.writestr('README.txt', 'Portfolio simulation. Open report.html in a browser; Print > Save as PDF for a portable copy. CSV contains the same filtered campaign scope. INR costs; snapshot 2025-12-31.')
    return buffer.getvalue()

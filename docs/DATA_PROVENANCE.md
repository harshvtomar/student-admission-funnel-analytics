# Data provenance and research decision
Research date: 18 October 2026. All project data is generated locally by `src/generate.py`.

| Public source reviewed | Observed scope | Suitability and reuse decision |
|---|---|---|
| https://aishe.gov.in/ and https://aishe.gov.in/document-category/aishe-final-reports/ | Official higher-education institutional and enrollment statistics | Useful domain context, but no linked campaign spend, clicks and individual admission-event history. No rows imported; no reuse-license assumption required. |
| https://www.data.gov.in/resource/state-and-ugc-faculty-group-wise-student-enrollment-universities-and-colleges-2012-2013 | State/faculty enrollment aggregates | Wrong grain and period for a marketing CRM; not joined to synthetic leads. |
| https://archive.ics.uci.edu/dataset/856/higher%2Beducation%2Bstudents%2B | Student academic/performance attributes; source lists CC BY 4.0 | Not an Indian admissions marketing CRM. Not imported despite a stated reusable license. |

No suitable complete public Indian spend-to-enrollment CRM was identified in this focused investigation; this is not a claim that no such dataset exists. No scraping, personal student data or unverified tuition-revenue estimates are used.

## Generator assumptions
Seed 20261018; NumPy's default random generator; pinned NumPy/pandas versions. There are 10 campaign-months per month over calendar 2025 and 24 institutions rotated across 120 campaigns. Channels rotate across seven categories. Campaign budgets are uniform INR 80,000–250,000; spend is 65–112% of budget. Lead volume is a multinomial allocation with Dirichlet weights (concentration 12). Clicks are 5–12 times leads; impressions imply a synthetic 1.5–6% CTR. These are illustrative assumptions, not benchmark estimates.

Per-channel qualification probabilities are [0.66, 0.49, 0.65, 0.73, 0.58, 0.71, 0.43] in the channel order in `generate.py`, perturbed by campaign factors 0.88–1.10. Conditional stage probabilities are 0.69 for application starts, 0.60–0.82 for completion, 0.76 for offers and 0.56 for enrollment. Each progression adds 1–14 days plus 0–11 hours; events after the snapshot are censored. Markets/course preferences are random and are not demographic predictions. Maximum modeled progression lag is below 90 days, so fully mature cohorts have complete modeled follow-up.

Manifest hashes refer to canonical uncompressed CSV bytes, not platform-dependent ZIP or SQLite bytes. `python -m src.pipeline` recreates data and reports. The checked-in manifest contains exact table counts and hashes for detecting unintended generator drift.

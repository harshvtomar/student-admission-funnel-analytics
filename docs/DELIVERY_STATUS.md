# Delivery status — Session 2

Verified 19 October 2026. Repository branch: main.
Application/report build commit: `a9c04d2b6b1a778af8d9338af47fe0dccad294ec`.
Final handoff is a documentation and evidence descendant; use `git rev-parse HEAD` for its own SHA.

Live app: https://student-admission-funnel-analytics.streamlit.app/
Hosting: Streamlit Community Cloud, Python 3.12, existing repository main, app.py. The application loaded in the connected Chrome browser, including the new planner and institution exports.

## Delivered

- Seven-page Streamlit application; existing analytics and filters preserved.
- Mature-cohort fixed-budget allocation with editable total, lower/upper channel shares, three named cost scenarios and an editable active multiplier.
- Historical CPQL, CPA, CPE and allocation comparisons; exact paise allocation; explicit hypothetical-volume explanations and infeasible-input warnings.
- Institution selector and filtered HTML / ZIP-with-CSV downloads; 24 full-snapshot institution packs.
- Eight-tab XLSX: seven requested business views plus Guide. 904 formulas and six editable charts, filters, conditional formatting and scenario input controls.
- Ten-slide editable PPTX with five native charts, PDF, executive report and reproducible reporting inputs/builders.
- Interview guide with two resume bullets, 60–90-second explanation and ten Q&A.
- Genuine desktop, planner and narrow-screen screenshots.

## Verification evidence

| Check | Result |
|---|---|
| Previous baseline | Initial 48 pass / 9 fail due to damaged derived SQLite file; rebuilt, then 57 pass / 0 fail |
| Final local Python suite | 69 passed, 0 failed in 20.69 seconds; reports/session2/test_output.txt and pytest.xml |
| SQL/Python reconciliation | Passed within the suite; original 12 SQL analyses retained |
| Data pipeline | Regenerated successfully, validation passed without diagnostic errors |
| GitHub Actions build | Run 39182948308 completed successfully for application commit a9c04d2 |
| Seven app pages | AppTest renders all seven; corresponding public page content inspected in Chrome |
| Planner | Base result reconciled with Python/Excel; live 10% maximum cap produces infeasible-constraint warning; 25% restored |
| Institution export | Live I001 ZIP download completed; all 24 generated ZIP structures checked; scoped counts covered by tests |
| Excel | Seven headline controls reconcile; conservative multiplier and infeasible-cap checks pass; 904 formulas, six charts, zero cached formula errors |
| Presentation | Ten slides and five charts; package, layout, font and re-import checks pass; all ten slide previews and PDF pages inspected |
| Live maturity filter | 90 campaigns, 37,372 leads and 4,653 enrollments shown; defaults restored |
| Narrow screen | 390×844 Chrome viewport checked; text reflows, sidebar collapses, wide tables remain horizontally scrollable |

## Honest limits

Synthetic data cannot establish real-world effectiveness, market demand or causal uplift. Planner assumes constant efficiency and no saturation; scope/eligibility constraints are documented in BUDGET_METHODOLOGY.md. Excel is a fixed 120-campaign/seven-channel export and its historical ranking must be rebuilt when inputs change. Its table filters do not alter executive SUM formulas.

Native Microsoft Excel and PowerPoint editing were not available for direct testing. Workbook calculations were verified in the authoring runtime and exported cache; PDF was rendered via LibreOffice. One failed PDF export in the artifact runtime was resolved with LibreOffice. Structural/visual checks are not full cross-suite or accessibility certification. Narrow-screen coverage is a responsive spot check, not an exhaustive device matrix. All seven pages have automated rendering coverage, but every possible filter combination and download has not been exercised in-browser.

The optional Excel/deck builders require the documented ChatGPT Work artifact-authoring runtime; the app, analytics and institution-report generator require only requirements.txt. Free hosting availability and cold starts are outside this project's control. Real CRM integration, consent governance, refunds/withdrawals, multi-touch attribution, delivery-level geographic costs and controlled response experiments remain future work. No authentication or permission action is currently required from the user.

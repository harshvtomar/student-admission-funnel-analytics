# Project state — Session 1

Repository: https://github.com/harshvtomar/student-admission-funnel-analytics
Branch: `main`
Validated application commit: `2fefaa4587174192fa53efc5c5b6be1e6d44f311`
This checkpoint is a documentation-only descendant of that commit. Obtain its exact current SHA with `git rev-parse HEAD` or the GitHub branch reference; a commit cannot contain its own hash.

## Completed
- Deterministic five-table simulation, constrained SQLite schema, two analytical views and 12 documented SQL queries.
- Separate generator, validation, database, KPI, recommendations and presentation modules.
- Seven functional Streamlit workspaces, filters, Plotly charts, INR cards, CSV downloads and empty states.
- Single primary campaign attribution; explicit grain separation; mature-cohort controls; deterministic evidence-backed recommendations.
- Complete README, provenance, data dictionary, analytical methodology, SQL guide and management review.
- Public GitHub repository, compressed CSV tables and manifest, test/validation reports, GitHub Actions workflow.

## Dataset
Seed 20261018. Calendar 2025 campaigns; as-of 2025-12-31 23:59:59.
24 institutions; 120 campaigns; 50,000 leads; 79,321 achieved events; 5,627 enrollment confirmations; eight markets; seven channels.

## Verified locally
`python -m src.pipeline`: passed, no diagnostic errors.
`python -m pytest -q --junitxml=reports/pytest.xml`: **57 passed, 0 failed**, 16.89 seconds.
Includes all seven pages via Streamlit AppTest and arithmetic/SQL reconciliation.
Real Streamlit HTTP health endpoint: **200 / ok**.
GitHub Actions workflow is committed; inspect the live run for hosted status, which may finish after this checkpoint.

## Known limitations
Fully synthetic data; no empirical effectiveness/market-demand/ROI claims. Observed-to-date recent cohorts are incomplete. No multi-touch attribution, geographic cost allocation, real CRM ingestion, withdrawals or rejected-outcome modeling. INR uses floating-point values with testing tolerance. Complete browser visual/mobile/accessibility QA is not done. No public app deployment yet. The repository screenshot documents creation, not dashboard visual QA.

## Remaining work
Session 2: deploy the current app, verify seven pages in a browser, capture genuine dashboard screenshots, produce a formula-backed Excel workbook, institutional CSV/Excel reporting packs and concise leadership presentation. Explore budget scenarios only with explicit hypothetical assumptions and no causal uplift claims. Preserve this repository and do not touch the user's other repositories.

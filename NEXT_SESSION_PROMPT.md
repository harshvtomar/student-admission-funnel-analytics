# PROJECT 2 — WORK SESSION 2
## AdmissionFlow Intelligence: deployment, reporting and visual QA

Continue the existing Student Admission Funnel & Marketing Campaign Optimization project. Do not restart or replace it.

Repository: https://github.com/harshvtomar/student-admission-funnel-analytics
Branch: main
Verified Session 1 application commit: 2fefaa4587174192fa53efc5c5b6be1e6d44f311
Read PROJECT_STATE.md, SESSION_LOG.md, README.md, docs/METHODOLOGY.md and the latest GitHub main commit before changing anything. Work from the current branch head, which includes later checkpoint documentation.

Act as a senior marketing analyst, Streamlit developer and reporting specialist. Preferred model: GPT-6 Astra with Medium Reasoning if available. Work autonomously for one focused Work session. Ask only for necessary authentication or external approvals. Preserve all unrelated repositories, particularly university-partnership-sales-analytics, retail-growth-profitability and customer-retention-analytics.

## Existing verified foundation
50,000 synthetic leads, 24 fictional institutions, 120 campaigns, eight markets, seven channels, 79,321 funnel events and 5,627 confirmations. Seed 20261018; snapshot 2025-12-31. Seven functional Streamlit pages, 12 SQL queries, complete KPI/attribution/maturity rules and 57 passing local tests. HTTP startup was verified. All data is explicitly a CampusGrowth Analytics portfolio simulation, not KollegeApply data.

## Ordered work
1. Pull current main; inspect GitHub Actions. Install pinned dependencies with Python 3.12. Run pipeline and tests. Verify canonical hashes match data/manifest.json before accepting any dataset changes.
2. Deploy app.py from this repository using a free Streamlit hosting option. First inspect the connected account and existing deployments; create a new app without changing other apps. Do not buy services. Request user action only if sign-in or approval is required.
3. Perform genuine browser QA of all seven pages: default view, month/institution/channel/campaign filters, maturity checkbox, funnel geography, CSV downloads and empty state. Check desktop/mobile layout and chart labels. Capture real screenshots in screenshots/; do not substitute mockups. Fix concrete issues and regression-test the affected behavior.
4. Create an Excel management workbook with source/report sheets, formula-linked KPI summary, channel/campaign/institution comparisons, cohort definitions and a recommendations sheet. Reconcile Excel results against Python/SQL. Use blanks/N/A for undefined denominators. Include simulation labels and as-of date.
5. Create downloadable institutional reporting packs from filtered calculations, with attribution and maturity explanations. Avoid allocations of marketing spend to geography without new documented data.
6. Create a concise leadership presentation: business question, data and grain, funnel bottlenecks, mature campaign diagnostics, controlled-test proposals, limitations and next actions. Every number must reconcile to the dataset; no invented ROI or causal lift.
7. Optional only after the above: scenario-based budget planning with explicitly hypothetical constraints and conversion assumptions. Do not present a historical ranking as causal optimization. Keep scenario values separate from observed simulation results.
8. Update README with the verified live link, genuine screenshots, exact test counts and deliverable links. Commit tested work and update PROJECT_STATE.md and SESSION_LOG.md. Write NEXT_SESSION_PROMPT.md only if material work remains.

## Final response
Provide repository/live URLs, final commit SHA, actual local and hosted CI results, screenshot/Excel/presentation/report links, completed improvements, limitations and any genuine blockers. Do not claim deployment or browser QA until actually verified.

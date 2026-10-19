# Interview guide — KollegeApply Management Trainee

## Resume bullets

- Built and deployed a seven-page Streamlit admission-marketing analytics platform using Python, Pandas, SQLite and Plotly, analyzing 50,000 synthetic leads across 120 campaigns and 24 fictional institutions with 12 SQL analyses and automated KPI reconciliation.
- Developed a constrained marketing-budget scenario planner, formula-based Excel management workbook and automated institution report exports; identified simulated application-conversion bottlenecks while documenting attribution, cohort maturity and forecasting limitations.

## 60–90 second explanation

“I built AdmissionFlow Intelligence as a portfolio simulation of an Indian EdTech marketing operation. The problem was to connect institutional campaign spend with student progression, so a manager could see where follow-up or campaign review was needed. I generated 50,000 reproducible student leads across 24 fictional institutions and 120 campaigns. I designed five relational tables, wrote 12 SQL analyses, and reconciled the metrics against Python.

The seven-page Streamlit dashboard separates aggregate campaign reach from student-level conversion and distinguishes mature cohorts from recent leads. In the simulation, 13,792 applications were completed and 5,627 enrollments were confirmed, at roughly ₹3,366 per enrollment. Campaign C007 had an 18.3% completed-application rate against a 29.1% mature pooled benchmark, making it a clear investigation candidate.

I also added institution report exports, an Excel management workbook and a constrained budget planner. The planner uses historical synthetic efficiency with explicit cost assumptions; it does not claim future uplift. This mirrors campaign monitoring, client reporting and analytical decision support relevant to a Management Trainee role.”

## Ten likely questions

1. **What business problem does this solve?** It combines spend, student progression and institutional reporting into a consistent campaign-management view. Managers can prioritize investigations instead of comparing disconnected spreadsheets.
2. **Why synthetic data?** No complete, legally reusable admission CRM dataset was available in the initial provenance review. Fictional records avoid personal data exposure and permit reproducible tests. Findings demonstrate methods, not actual company results.
3. **How did you avoid double-counting spend?** Campaign spend is aggregated at campaign grain before being compared with student counts. A lead has exactly one primary acquisition campaign; event rows never multiply campaign costs.
4. **How is conversion defined?** Lead-to-enrollment is confirmed enrollments divided by distinct leads in selected acquisition cohorts. Application completion is completions divided by starts; application-to-enrollment uses completed applications as denominator.
5. **How do you handle recent leads?** Outcomes are observed through 31 December 2025. Mature campaign comparisons require campaign end plus 91 days at or before the snapshot. This avoids interpreting short follow-up as poor final conversion, but is not survival modeling.
6. **What happens when a denominator is zero?** Ratios are undefined and display N/A. Zero-enrollment campaigns are retained for investigation, while the budget planner excludes them from unit-cost allocation rather than assuming zero CPE.
7. **How does the optimizer work?** It maximizes modeled enrollments under constant historical CPE and a fixed budget. Give every eligible channel its minimum share, then allocate to the lowest CPE until its cap binds. Validate feasibility and preserve the total to the paisa.
8. **Why not use machine learning?** Synthetic generator behavior is not evidence of real predictive validity. An explainable scenario model is more defensible; real response curves need independent data and experiments.
9. **What would you recommend to management?** Review C007's targeting and landing-page qualification, investigate incomplete applications, and validate lead quality and capacity before a controlled budget test. The 6,323 incomplete starts include recent students, so they are not all final losses.
10. **How did you validate and communicate the work?** Automated tests cover relational integrity, chronology, filters, KPI fixtures and SQL/Python reconciliation. Excel has formula controls against Python and scenario sensitivity checks. Institutional exports expose scope and limitations; deployment and test details are recorded in DELIVERY_STATUS.md.

## Findings and assumptions

All-2025 observed spend: ₹18,938,788.13; 50,000 unique leads; 13,792 completed applications; 5,627 enrollments; 11.254% lead-to-enrollment; 89.416% budget utilization. These are verified simulated outputs, not KollegeApply metrics.

Default ₹10 lakh planning case: about 302, 378 or 444 enrollment equivalents with cost multipliers 1.25, 1.00 or 0.85. These are hypothetical arithmetic, not projected incremental improvements. Do not claim campaign ROI, budget savings, revenue growth or employment experience from this portfolio.

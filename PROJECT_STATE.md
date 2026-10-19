# Project state — Session 2

Repository: https://github.com/harshvtomar/student-admission-funnel-analytics
Branch: main
Application/report checkpoint: `a9c04d2b6b1a778af8d9338af47fe0dccad294ec`.
This handoff commit is a documentation/evidence descendant; obtain its SHA with `git rev-parse HEAD`.

Live app: https://student-admission-funnel-analytics.streamlit.app/

Completed: Session 1 analytics preserved; seven deployed pages; mature-channel budget scenarios; institution HTML and CSV/ZIP exports; eight-tab Excel workbook; ten-slide editable deck and PDF; executive report; interview guide; screenshots; refresh and delivery documentation.

Dataset: fixed seed 20261018, 2025 acquisition, snapshot 31 December 2025. 50,000 leads, 24 institutions, 120 campaigns, 79,321 events, 5,627 enrollments, eight markets and seven channels. All synthetic.

Verification: 69 local tests passed, zero failed, 20.69 seconds. SQL/Python reconciliation and all seven AppTest pages pass. Application commit CI run 39182948308 succeeded. Excel headline and scenario checks pass; 904 formulas/six charts/no cached formula errors. All ten PDF pages inspected. Live app, planner warning and I001 report ZIP verified. Desktop and 390×844 viewport screenshots saved.

Deliverables: reports/session2/; scripts/build_workbook.mjs; scripts/build_deck.mjs; docs/INTERVIEW_GUIDE.md. Detailed evidence and limits: docs/DELIVERY_STATUS.md.

Known limits: synthetic associations, incomplete recent cohorts, constant-efficiency scenarios, fixed workbook export ranges, optional artifact-runtime dependency for Office regeneration, no native Microsoft Office or exhaustive accessibility/device testing. Do not present this as actual KollegeApply business results.

Next: optional real CRM integration with consent, controlled experiments, stronger device/accessibility QA and configurable workbook source ranges. No mandatory user action blocks use of the delivered portfolio.

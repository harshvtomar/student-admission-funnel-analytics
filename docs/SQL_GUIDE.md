# SQL analysis guide
`schema.sql` defines constrained tables, indexes, `lead_facts` and `campaign_performance` views. Each numbered query has an inline comment documenting its grain and caveat. Execute `python -m src.pipeline` to run all 12 and export their results.

1. Campaign performance: campaign grain, costs joined after lead aggregation.
2. Monthly acquisition: campaign acquisition month, not outcome month.
3. Unique lead conversion: distinct lead facts, guarded ratios.
4. Institution funnel: stages pooled by attributed client.
5. Channel CPL: pooled spend / pooled leads.
6. Channel CPE: pooled spend / confirmed enrollments, recent cohorts included.
7. Abandonment: unfinished started applications at snapshot, by institution.
8. Territory: conversion only; no geographic costs inferred.
9. Budget: actual / allocated campaign spend.
10. Cohorts: acquisition month split by individual 90-day maturity.
11. High cost: fully mature campaign-months, minimum lead volume, pooled benchmark.
12. Management: one-row campaign/spend/conversion review.

Do not join raw events directly to campaign spend and then sum costs: that multiplies spend by event rows. `lead_facts` first collapses events to one student; `campaign_performance` first collapses students to one campaign. Python reconciles campaign stage counts/cost metrics, channel and institutional aggregates, and maturity cohorts against SQL in automated tests.

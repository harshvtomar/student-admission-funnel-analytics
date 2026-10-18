# Simulated marketing management review

Snapshot: 31 December 2025; full Jan–Dec acquisition scope. Generated from the fixed seed, not empirical company results.

| Metric | Result |
|---|---:|
| Campaign spend | INR 18,938,788.13 |
| Unique leads | 50,000 |
| Qualified leads | 29,574 |
| Started applications | 20,115 |
| Completed applications | 13,792 |
| Offers | 10,213 |
| Confirmed enrollments | 5,627 |
| Lead-to-enrollment | 11.254% |
| Cost per enrollment | INR 3,365.70 |
| Budget utilization | 89.416% |

## Decisions to investigate
- **Campaign C007:** 349 leads, 18.3% completed-application conversion versus 29.1% across mature selected campaigns; spend INR 251,127. Audit targeting and landing-page qualification before a randomized messaging test.
- **Campaign C007:** 32 enrollments; CPE INR 7,848 versus pooled mature CPE INR 3,051. Inspect acquisition quality and downstream friction; do not automatically reallocate budget.
- **Campaign C007:** 38 of 102 starts remain incomplete (37.3%). Review application and upload steps with the institution.
- Across all observed cohorts, 6,323 started applications remain incomplete. This includes recent leads; it is not a permanent-dropout count.

Full recommendation evidence is recalculated by `src.recommendations` and exported in `recommendations.csv`. Whole-year cost includes right-censored recent cohorts, so it is not directly comparable with the mature-only benchmark. The channel differences are simulation parameters, not observed effectiveness; no real-world demand or causal uplift is inferred.

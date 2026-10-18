# Analytical contract

## Grains and relationships
- Institutions: one row per fictional institutional client.
- Campaigns: one campaign for one institution/channel over one whole calendar month. Budget, spend, impressions and clicks exist only at this grain.
- Leads: one synthetic individual and one immutable primary acquisition campaign. The source and institution must match that campaign. There is no PII or multiple-campaign identity matching.
- Events: one achieved event per lead and stage; only strictly sequential progression is valid. No skipped stages. A lead is not counted repeatedly for reaching the same stage.
- Enrollments: one confirmation per enrolled lead, matching the offer and enrollment event timestamps and institutional attribution.

The primary acquisition campaign is assigned at lead creation (single-touch acquisition, equivalent to first-touch in this single-interaction simulation). Event dates never reassign campaign credit. There are no alternate interaction records. This rule avoids double counting but does not measure incrementality.

## Reporting date and filters
Fixed as-of 2025-12-31 23:59:59, timezone-naive values representing India local time. Campaigns run January–December 2025. The sidebar month filter selects complete acquisition campaign-months; it does not slice spend by outcome dates or prorate costs. Numerators and denominators share that acquisition scope. Student outcomes may occur after campaign end but never after snapshot. Any future ingestion must normalize timezones and enforce the snapshot before analytics.

Individual lead maturity: acquired at least 90*24 hours before as-of. Fully mature campaign filter: `end_date + 91 days <= as_of`; the extra day conservatively includes leads acquired late on the final campaign day. Recommendations use this complete-campaign rule. Geography and individual-cohort summaries do not have cost allocations, so cost/reach quantities are undefined there. The funnel page suppresses aggregate reach when geography is selected.

Recent unprogressed leads may still convert. `not_qualified` includes not-yet-qualified leads; it is not a rejection decision. Stage gaps and abandonment mean incomplete at snapshot. Enrollment records contain confirmed outcomes only. Offers without enrollment can be pending or nonconverting; no unobserved outcome is fabricated.

## KPI contract
Counts: distinct lead IDs reaching an achieved stage at or before snapshot. Qualifier, start, completed, offer and enrolled flags are calculated independently from validated events. Spend, budget, impressions and clicks sum once per campaign. Pool before dividing; never average rates or CPEs. Missing required fields fail validation; they are not silently replaced with zeros. Valid zero-event stages count as zero; a zero denominator yields NaN/NULL.

| KPI | Numerator | Denominator |
|---|---|---|
| Total spend | Sum actual campaign spend | Not applicable |
| Impressions / clicks | Sum campaign interactions | Not applicable |
| Unique leads | Distinct acquired lead IDs | Not applicable |
| CTR | Clicks | Impressions |
| CPC | Actual spend | Clicks |
| CPL | Actual spend | Unique leads |
| Qualified rate | Qualified leads | Unique leads |
| Application start rate | Application starts | Qualified leads |
| Application completion rate | Completed applications | Application starts |
| Lead-to-application | Completed applications | Unique leads |
| Application-to-enrollment | Confirmed enrollments | Completed applications |
| Lead-to-enrollment | Confirmed enrollments | Unique leads |
| Cost per completed application | Actual spend | Completed applications |
| Cost per enrollment | Actual spend | Confirmed enrollments |
| Budget utilization | Actual spend | Campaign budget |
| Stage drop-off fraction | Previous stage count minus current stage count | Previous stage count |

Institution/channel metrics apply the same contract to their selected campaigns. Territory metrics use student geography and provide conversions only. Click-to-lead ratio is a cross-grain operational ratio; impressions/clicks are not distinct students and must never appear as a single unique-person funnel.

## Recommendations
Only fully mature campaign-months with at least 100 leads qualify. High-cost flags use CPE > 1.5 times pooled mature CPE, or zero enrollments. Weak-application flags use completed/leads < 80% of pooled mature rate and spend >= median mature campaign spend. Follow-up and abandonment flags require a gap >35% of qualified or started students respectively. Benchmarks are recomputed within selected campaigns. Every recommendation states the relevant count/rate and segment. Thresholds are transparent heuristics, not significance tests. Changes require controlled evaluation; the engine never asserts causal improvements or guaranteed savings.

## Validation, deduplication and persistence
`validate()` is non-mutating and returns all discovered diagnostics. Checks cover duplicate and missing keys, missing required fields, FK matches, campaign/source/institution consistency, chronology, stage prerequisites, future events, outcome consistency, nonnegative quantities and budgets. `deduplicate_exact()` drops exact duplicate rows only and raises on remaining conflicting identifiers. SQLite additionally enforces primary keys, foreign keys, non-null values, unique lead-stage pairs and unique enrollments. Validation precedes database writes. CSV diagnostics and SQL outputs reside in `reports/`.

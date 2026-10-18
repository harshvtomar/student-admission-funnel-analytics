# Complete data dictionary

All fields are required and non-null. Date/timestamps are ISO text in SQLite; times represent India local time. INR values are simulated. IDs are synthetic and have no external identity mapping. See METHODOLOGY.md for primary keys and grain.

## institutions

| Field | Python dtype | Definition |
|---|---|---|
| institution_id | object | Fictional institution key; FK to institutions outside the institutions table. |
| institution_name | object | Explicitly fictional CampusGrowth Demo Institute display name. |
| state | object | Indian state or union territory of fictional client. |
| city | object | Indian city of fictional client. |
| institution_category | object | Private university, Autonomous college or Specialist institute. |
| course_segment | object | Institution focus: Engineering, Management or Multidisciplinary. |
| campaign_budget_allocation | int64 | INR; sum of all allocated campaign budgets for this institution. |

## campaigns

| Field | Python dtype | Definition |
|---|---|---|
| campaign_id | object | Unique primary acquisition campaign; FK to campaigns for leads. |
| institution_id | object | Fictional institution key; FK to institutions outside the institutions table. |
| acquisition_channel | object | One of seven channels in generate.CHANNELS. |
| campaign_objective | object | Lead acquisition, Application completion or Enrollment consideration; descriptive objective, not a separate funnel rule. |
| start_date | object | ISO date; inclusive first day of campaign month. |
| end_date | object | ISO date; inclusive last day of campaign month. |
| budget | int64 | Hypothetical allocated INR budget, nonnegative. |
| actual_spend | float64 | Hypothetical incurred INR spend rounded to two decimals; includes operating costs for non-paid channels. |
| clicks | int64 | Aggregate campaign interaction count, not unique people. |
| impressions | int64 | Aggregate exposures, not unique people; >= clicks. |

## leads

| Field | Python dtype | Definition |
|---|---|---|
| lead_id | object | Unique anonymous synthetic student identifier; FK to leads in events/enrollments. |
| created_at | object | ISO local timestamp of acquisition, within attributed campaign dates. |
| acquisition_source | object | Must equal primary campaign acquisition_channel. |
| campaign_id | object | Unique primary acquisition campaign; FK to campaigns for leads. |
| institution_id | object | Fictional institution key; FK to institutions outside the institutions table. |
| geographic_market | object | One of eight Indian market labels; random simulated student location. |
| course_preference | object | Engineering, MBA, Arts & Science or Commerce; synthetic interest. |
| qualification_status | object | qualified if achieved by snapshot; otherwise not_qualified (includes pending). |

## events

| Field | Python dtype | Definition |
|---|---|---|
| event_id | object | Unique achieved-stage event identifier. |
| lead_id | object | Unique anonymous synthetic student identifier; FK to leads in events/enrollments. |
| event_type | object | qualified → application_started → application_completed → offer → enrolled; no skipped stages. |
| event_timestamp | object | ISO local timestamp; later than previous stage and <= snapshot. |
| event_status | object | achieved only; absence of event means not yet achieved at snapshot. |

## enrollments

| Field | Python dtype | Definition |
|---|---|---|
| enrollment_id | object | Unique enrollment confirmation identifier. |
| lead_id | object | Unique anonymous synthetic student identifier; FK to leads in events/enrollments. |
| institution_id | object | Fictional institution key; FK to institutions outside the institutions table. |
| admission_decision_date | object | ISO timestamp of the admission offer, despite the legacy date field name. |
| confirmation_date | object | ISO timestamp matching enrolled event. |
| enrollment_outcome | object | confirmed only; no rejected/withdrawn outcome inferred. |

## Derived fields

`lead_facts`: one boolean/integer flag per achieved stage, `month` = first seven characters of created_at, `mature` = at least 90 days since acquisition. `campaign_performance`: lead/stage counts aggregated per campaign, CPL, CPE and lead-to-enrollment conversion. All ratio fields and denominator rules are defined in METHODOLOGY.md.

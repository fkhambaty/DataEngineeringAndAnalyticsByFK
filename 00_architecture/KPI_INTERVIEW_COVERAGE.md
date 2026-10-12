# KPI Snowflake architect interview coverage

This is the release contract for the Meridian course. A topic is complete only when the
learner can see the idea, run the proof, and explain the result. The source interview is
`Jobs/.../KPI_ROUND1_DEBRIEF.html` in the private command-center repository; no personal
interview material is copied into the public student repository.

| Interview topic | Practical proof | Teaching/deck home | Student proof of completion |
|---|---|---|---|
| Snowflake keys are informational; `NOT NULL` is enforced | dbt `unique`, `not_null`, `relationships`, model contracts, and incoming-batch dedupe in `stg_postgres__transactions.sql` | E3, E6, study guide quality chapter | Deliberately duplicate a key; `dbt build` fails before publication |
| Existing tables can become corrupt outside a pipeline | `03_snowflake/11_mart_integrity_and_quarantine.sql`, dbt integrity test, daily Airflow integrity task | E9, study guide operations chapter | Orphan is recorded with its key and reason; daily DAG fails |
| Slow query triage has an order | `06_performance_lab/10_slow_query_triage_playbook.sql` | E8, performance study chapter | Compare fast/slow history, queue/execution, widest operator, then rerun |
| Pruning is not spilling | performance labs 02, 03, 06 | E8 | Partitions fall after a sargable range; spill bytes fall after shrinking work |
| Join explosion is a grain error | performance lab 04 and SCD2 overlap test | E2, E8 | Rows-out multiplier returns to one after effective-date predicate |
| Scale up is not scale out | performance labs 03 and 09 | E8 | Larger warehouse helps one memory-heavy query; multi-cluster reduces queueing |
| A tenant/country key is not a security boundary | country entitlement and deny-by-default proof in `03_snowflake/06_row_level_security.sql` | E11, E13 | Hong Kong role sees HK only; an unentitled user sees zero rows |
| Shared versus database-per-tenant is a design choice | ADR 0011 | E13, architecture study chapter | Learner can defend isolation, versioning, cost, and blast-radius trade-offs |
| PII needs masking as well as row filtering | tag-based masking in `03_snowflake/06_row_level_security.sql` | E11 | Staff sees masked contact fields while an approved role sees values |
| Micro-batch is not streaming | five-minute watermark DAG and bounded replay | E4, E7 | Learner states honestly that the project is micro-batch, not Kafka streaming |
| dbt transforms; Airflow orchestrates | daily, micro-batch, freshness, replay, and decisioning DAGs | E7 | DAG import succeeds; failed quality task blocks downstream publication |
| Native Snowflake automation is a separate option | `03_snowflake/04_streams_tasks_dynamic_tables_demo.sql` | E3 | Demo is run and suspended; learner can explain when dbt/Airflow remains preferable |
| Analytics starts with grain and identity | `12_case_studies/customer_health/` account crosswalk and daily snapshot | E2, E13, customer-health study chapter | Final mart is exactly one row per account per snapshot date; no join uses account name |
| Metric definitions must survive challenge | executable MRR, activity, adoption, support, CSAT and score calculations in the customer-health case | E13, customer-health study chapter | Reconciliation, range and missing-data assertions pass offline |
| A weighted score must be normalised and validated | versioned 0–100 health score, Unknown band, back-test plan and drift checks | E10, E13 | Every component is bounded before weighting; thresholds are not presented as truth until back-tested |
| Delivery is a product decision as well as a data model | six-week MVP, late-data contract, owners, UAT and phased rollout in the case runbook | E13 | Learner can defend what ships first and what is deliberately deferred |

## Release gates

1. Every executable proof above exists in the public student repository.
2. Every proof has a visual explanation and an exact command or SQL file to run.
3. No deck claims a live Snowflake result unless the repository contains the query that
   produces it; account-dependent results are labelled as expected results.
4. No course or student file contains the instructor's local path, account identifier,
   user name, private key, or interview transcript.
5. Offline tests, deck checks, internal links, slide counts, and 1600x900 final-state
   screenshots pass before either repository is tagged release-ready.

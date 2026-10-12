# E9 — Quality, CI, cost, runbook

Planned length: 30 minutes. Playlist position: 11 of 15.
Grounding: course/show/e9.html chapters Checks, Reconcile, Slim CI, 2 a.m., and course/show.html (30 min, 18 scenes).

## Title

Meridian E9: A green dbt build is only the first check

## Hook

A green build means the job finished. It does not mean the numbers are fit to publish.
Integrity, reconciliation, cost, and the 2 a.m. playbook each answer a different question.

## Description

A green build means the job finished. It does not mean the numbers are fit to publish.
Integrity, reconciliation, cost, and the 2 a.m. playbook each answer a different question.

Quality starts after the build is green. Freshness is a clock. A dbt test is a rule. Reconciliation asks the bank and the warehouse the same question. The offline reconciliation test expects the same keys and a money difference under one cent. That is the test's expectation. The published-mart sweep stores a missing dimension key or a duplicate business key, together with the reason. Unknown member -1 is a designed member, not an orphan. No live orphan count is on the slide, and this pack is not a counted orphan total. Slim CI parses and builds what changed. Cost attribution names the warehouse and the query tag. The runbook then covers a hot table that goes quiet, and a bounded replay that does not move the watermark.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E9 in the playlist, position 11 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- E6 marts and E7 schedules.
- GitHub Actions files can be shown without a warehouse.
- Cost and quarantine SQL are read as the queries to run.

Files covered
- .github/workflows/meridian-checks.yml
- .github/workflows/meridian-dbt-ci.yml
- .github/dependabot.yml
- 02_ingestion_python/dbt_artifact.py
- 03_snowflake/08_cost_attribution.sql
- 03_snowflake/09_zero_copy_dev_environment.sql
- 03_snowflake/10_dr_exercises.sql
- 04_dbt_meridian_dw/tests/assert_staging_complete_versus_bronze.sql
- 04_dbt_meridian_dw/tests/assert_raw_transactions_required_keys.sql
- 00_architecture/OPERATIONS_RUNBOOK.md
- 00_architecture/DR_RUNBOOK.md
- 03_snowflake/11_mart_integrity_and_quarantine.sql
- 04_dbt_meridian_dw/tests/assert_mart_referential_integrity.sql

Chapters
00:00 Checks
08:00 Reconcile
16:00 Slim CI
23:00 2 a.m.

Adjust these timestamps after the final edit. They are drafted to the planned 30-minute cut, not to a finished timeline.

Do not invent an orphan count. The integrity query stores hits when you run it. Until then, the honest line is: not a counted orphan total.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#DataQuality #dbt #DataEngineering #CICD #AnalyticsEngineering

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- E6 marts and E7 schedules.
- GitHub Actions files can be shown without a warehouse.
- Cost and quarantine SQL are read as the queries to run.

## Files covered

- `.github/workflows/meridian-checks.yml`
- `.github/workflows/meridian-dbt-ci.yml`
- `.github/dependabot.yml`
- `02_ingestion_python/dbt_artifact.py`
- `03_snowflake/08_cost_attribution.sql`
- `03_snowflake/09_zero_copy_dev_environment.sql`
- `03_snowflake/10_dr_exercises.sql`
- `04_dbt_meridian_dw/tests/assert_staging_complete_versus_bronze.sql`
- `04_dbt_meridian_dw/tests/assert_raw_transactions_required_keys.sql`
- `00_architecture/OPERATIONS_RUNBOOK.md`
- `00_architecture/DR_RUNBOOK.md`
- `03_snowflake/11_mart_integrity_and_quarantine.sql`
- `04_dbt_meridian_dw/tests/assert_mart_referential_integrity.sql`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 30-minute cut, not to a finished timeline.

```
00:00 Checks
08:00 Reconcile
16:00 Slim CI
23:00 2 a.m.
```

## Hashtags

#DataQuality #dbt #DataEngineering #CICD #AnalyticsEngineering

## Tags

data quality, dbt tests, reconciliation, CI CD, Snowflake cost, runbook, data engineering, analytics engineering, quarantine, freshness, Meridian Bank, tutorial

## Pinned comment

Open 03_snowflake/11_mart_integrity_and_quarantine.sql and say what gets stored when a key has no dimension row.

Why is member -1 not an orphan?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E9 is up: a green dbt build is only the first check. Integrity, cost, and the 2 a.m. playbook. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E10 — Cards: score, then offer. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E10), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e9-quality-after-green.mp4

## Thumbnail

- File: `thumbnails/E9.png`
- Badge: EPISODE 9
- On-image hook: Green is not enough
- Tech: Quality and CI

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] No orphan count is stated as a live result.
- [ ] The one-cent reconciliation line is labelled as the test expectation.

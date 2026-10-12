# E13 — Say it in two minutes

Status: not published yet.
Planned length: 20 minutes. Playlist position: 15 of 15.
Grounding: course/show/e13.html chapters The clock, The pipeline, The gate, The scar, and course/show.html (20 min, 19 scenes).

## Title

Explain This Project in 2 Minutes | Data Engineering Interview | Episode 13

## Hook

Problem, constraints, design, trade-offs, proof. Then stop.
The customer-health numbers are an offline synthetic case, not from a live customer.

## Description

Problem, constraints, design, trade-offs, proof. Then stop.
The customer-health numbers are an offline synthetic case, not from a live customer.

The close is a two-minute pitch: about 15 seconds on the problem, 15 on constraints, 40 on the design, 30 on the trade-offs, and 20 on the proof. One payment crosses eight doors. The watermark starts at 1900-01-01, the lag default is 10 seconds, and deletes live in cdc.deleted_records. Below a 0.70 holdout the model run is REJECTED. The same English question returns different rows because the policy reads the user. Shared tables versus a database per tenant is a 2-2 trade until the contract decides. Meridian is one bank with internal personas, so it ships shared marts and RAP_CUSTOMER_SCOPE. ADR 0011 records that. Then one failure you actually hit. Do not invent a measured twenty-minute wait. The task execution timeout in code is 20 minutes. The customer-health case is synthetic: grain is one Salesforce account per snapshot date, the October mart ranks Brightline first, Newly Co stays Unknown with priority 0, and the labelled back-test is precision 1.0 and recall 0.5, so automated outreach stays withheld. Those figures are not from a live customer. Claim only files you can open. Meridian has no production users.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 13, video 15 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- The earlier releases, enough that you can defend the design without opening a new tool.
- Have the student repository name ready as the last thing you point at.

Files covered
- 00_architecture/DESIGN_DOC.md
- 00_architecture/adr/0001-watermark-cdc-before-log-based.md
- 00_architecture/adr/0004-dbt-plus-airflow.md
- 00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md
- 00_architecture/adr/0010-contracts-at-public-boundaries.md
- 00_architecture/adr/0011-multitenancy-patterns.md
- 04_dbt_meridian_dw/models/marts/core/fct_transactions.sql
- 03_snowflake/06_row_level_security.sql
- 00_architecture/OPERATIONS_RUNBOOK.md
- 12_case_studies/customer_health/README.md
- 12_case_studies/customer_health/run_case.py
- tests/test_customer_health_case.py

Chapters
00:00 The clock
05:00 The pipeline
10:00 The gate
15:00 The scar

Adjust these timestamps after the final edit. They are drafted to the planned 20-minute cut, not to a finished timeline.

The scar must be a failure you can point at in the repository or in a run you did. The customer-health metrics are not from a live customer. Do not blend a separate employer story's numbers into Meridian.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#DataEngineering #SystemDesign #AnalyticsEngineering #Interview #DataArchitecture

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- The earlier releases, enough that you can defend the design without opening a new tool.
- Have the student repository name ready as the last thing you point at.

## Files covered

- `00_architecture/DESIGN_DOC.md`
- `00_architecture/adr/0001-watermark-cdc-before-log-based.md`
- `00_architecture/adr/0004-dbt-plus-airflow.md`
- `00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md`
- `00_architecture/adr/0010-contracts-at-public-boundaries.md`
- `00_architecture/adr/0011-multitenancy-patterns.md`
- `04_dbt_meridian_dw/models/marts/core/fct_transactions.sql`
- `03_snowflake/06_row_level_security.sql`
- `00_architecture/OPERATIONS_RUNBOOK.md`
- `12_case_studies/customer_health/README.md`
- `12_case_studies/customer_health/run_case.py`
- `tests/test_customer_health_case.py`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 20-minute cut, not to a finished timeline.

```
00:00 The clock
05:00 The pipeline
10:00 The gate
15:00 The scar
```

## Hashtags

#DataEngineering #SystemDesign #AnalyticsEngineering #Interview #DataArchitecture

## Tags

data engineering interview, system design, analytics engineering, data warehouse, Snowflake, dbt, Airflow, portfolio project, Meridian Bank, tutorial, dimensional modelling, data governance

## Pinned comment

The public code is the student repository. Point at it. Then stop.

Which trade-off in ADR 0011 would make you switch from one shared table to a database per tenant?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Finale: say the whole Meridian design in two honest minutes. The customer-health case stays synthetic. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

No next-episode card. This is the last release.
End screen, final 20 seconds: the playlist and Subscribe. Replay E0 only if you want a loop.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e13-two-minutes.mp4

## Thumbnail

- File: `thumbnails/E13.jpg`
- Red corner tag: EPISODE 13
- Headline: EXPLAIN THIS PROJECT IN 2 MINUTES
- Handwritten line: The interview answer

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Customer-health precision and recall are labelled as the offline synthetic case.
- [ ] No invented outage duration. The 20-minute figure is the task timeout in code.
- [ ] The last frame points at the public repository name.

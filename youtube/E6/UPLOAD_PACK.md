# E6 — The star schema, for real

Status: not published yet.
Planned length: 50 minutes. Playlist position: 8 of 15.
Grounding: course/show.html episode E6 (50 min, 14 scenes: FX at the day's rate, customer versions, facts, deletes, tests, reconciliation) and the dbt II plan in course/teach.html. Deck: course/show/e6.html.

## Title

Build the Star Schema in dbt | Facts, SCD2, Currency Rates on Snowflake | Episode 6

## Hook

Dollars use the rate from the day the payment happened, including a forward-filled weekend.
The fact points at the customer as they were that day. Remove that match and the test fails.

## Description

Dollars use the rate from the day the payment happened, including a forward-filled weekend.
The fact points at the customer as they were that day. Remove that match and the test fails.

The star is built for real. Weekend FX rates forward-fill from the last published rate, and USD stays 1. Facts join the customer and account version that was valid at the event, not whoever they are today. fct_transactions is an incremental merge: one row per transaction at its latest status. Deletes removed in staging stay removed. The reconciliation test is shown failing when the point-in-time match is taken out, then passing when it is put back. Selectors separate the five-minute work from the nightly work. Docs show the lineage.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 6, video 8 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Episode 5 staging models and snapshots.
- dbt build against your own dev or prod target. Do not borrow someone else's row counts.

Files covered
- 04_dbt_meridian_dw/models/intermediate/int_fx_rates_daily_filled.sql
- 04_dbt_meridian_dw/models/intermediate/int_transactions_with_fx.sql
- 04_dbt_meridian_dw/models/intermediate/int_account_primary_holder.sql
- 04_dbt_meridian_dw/models/marts/core/dim_customer.sql
- 04_dbt_meridian_dw/models/marts/core/dim_account.sql
- 04_dbt_meridian_dw/models/marts/core/fct_transactions.sql
- 04_dbt_meridian_dw/models/marts/core/fct_monthly_account_balance.sql
- 04_dbt_meridian_dw/models/marts/core/fct_loan_applications.sql
- 04_dbt_meridian_dw/models/marts/finance/agg_branch_daily_performance.sql
- 04_dbt_meridian_dw/models/marts/core/_core__models.yml
- 04_dbt_meridian_dw/tests/assert_fct_transactions_reconciles_to_staging.sql
- 04_dbt_meridian_dw/tests/assert_posted_transactions_have_fx.sql
- 04_dbt_meridian_dw/tests/assert_scd2_no_overlapping_versions.sql
- 04_dbt_meridian_dw/selectors.yml

Chapters
00:00 FX on the day it happened
10:00 Customer versions
20:00 The transaction fact
30:00 Deletes and incremental merge
40:00 A test that fails on purpose
46:00 Lineage

Adjust these timestamps after the final edit. They are drafted to the planned 50-minute cut, not to a finished timeline.

A failing test in this episode is a demonstration you cause on purpose. The pass or fail text is from that command, not from a remembered screenshot.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#dbt #StarSchema #DataEngineering #Kimball #AnalyticsEngineering

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Episode 5 staging models and snapshots.
- dbt build against your own dev or prod target. Do not borrow someone else's row counts.

## Files covered

- `04_dbt_meridian_dw/models/intermediate/int_fx_rates_daily_filled.sql`
- `04_dbt_meridian_dw/models/intermediate/int_transactions_with_fx.sql`
- `04_dbt_meridian_dw/models/intermediate/int_account_primary_holder.sql`
- `04_dbt_meridian_dw/models/marts/core/dim_customer.sql`
- `04_dbt_meridian_dw/models/marts/core/dim_account.sql`
- `04_dbt_meridian_dw/models/marts/core/fct_transactions.sql`
- `04_dbt_meridian_dw/models/marts/core/fct_monthly_account_balance.sql`
- `04_dbt_meridian_dw/models/marts/core/fct_loan_applications.sql`
- `04_dbt_meridian_dw/models/marts/finance/agg_branch_daily_performance.sql`
- `04_dbt_meridian_dw/models/marts/core/_core__models.yml`
- `04_dbt_meridian_dw/tests/assert_fct_transactions_reconciles_to_staging.sql`
- `04_dbt_meridian_dw/tests/assert_posted_transactions_have_fx.sql`
- `04_dbt_meridian_dw/tests/assert_scd2_no_overlapping_versions.sql`
- `04_dbt_meridian_dw/selectors.yml`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 50-minute cut, not to a finished timeline.

```
00:00 FX on the day it happened
10:00 Customer versions
20:00 The transaction fact
30:00 Deletes and incremental merge
40:00 A test that fails on purpose
46:00 Lineage
```

## Hashtags

#dbt #StarSchema #DataEngineering #Kimball #AnalyticsEngineering

## Tags

dbt, star schema, fact table, SCD2, foreign exchange, incremental merge, data tests, reconciliation, analytics engineering, Snowflake, Meridian Bank, tutorial

## Pinned comment

Open fct_transactions.sql and name the grain in one sentence.

Why must March use the March customer, even if that customer is premium now?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 6 is up: the star schema for real. The day's FX rate, the day's customer, and a test that can fail. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E7 — Airflow is the alarm clock. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E7), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e6-star-schema.mp4

## Thumbnail

- File: `thumbnails/E6.jpg`
- Red corner tag: EPISODE 6
- Headline: BUILD THE STAR SCHEMA IN DBT
- Handwritten line: Facts · SCD2 · currency rates

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Test output is read from the command you run, not typed from memory.

# E5 — dbt cleans the inbox

Status: not published yet.
Planned length: 45 minutes. Playlist position: 7 of 15.
Grounding: course/show.html episode E5 (45 min, 14 scenes: VARIANT to typed rows, incremental builds, snapshots, dev sandbox) and the dbt I plan in course/teach.html. Deck: course/show/e5.html.

## Title

Turn Raw JSON into Clean Tables | dbt Staging on Snowflake | Episode 5

## Hook

Bronze kept every copy. Staging is allowed to keep only the latest typed row.
Run the snapshot twice. A second version appears only when a tracked value changed.

## Description

Bronze kept every copy. Staging is allowed to keep only the latest typed row.
Run the snapshot twice. A second version appears only when a tracked value changed.

dbt cleans the inbox. The project layout, packages, and selectors come first. Staging parses VARIANT into typed, renamed columns. QUALIFY keeps one row per business key, newest extraction first. Source freshness is a clock. It is not a content test. Customer and account snapshots use a timestamp strategy. Run the snapshot again after a tracked change and a second version is the expected shape. A dev target is a sandbox. It does not inherit production persona grants.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 5, video 7 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Episode 4, so bronze has rows to parse.
- dbt Core with the packages in packages.yml.
- A local profiles file based on profiles.yml.example. The real profiles.yml stays off camera.

Files covered
- 04_dbt_meridian_dw/dbt_project.yml
- 04_dbt_meridian_dw/packages.yml
- 04_dbt_meridian_dw/selectors.yml
- 04_dbt_meridian_dw/profiles.yml.example
- 04_dbt_meridian_dw/models/staging/postgres/_postgres__sources.yml
- 04_dbt_meridian_dw/models/staging/postgres/stg_postgres__transactions.sql
- 04_dbt_meridian_dw/snapshots/snap_customers.sql
- 04_dbt_meridian_dw/snapshots/snap_accounts.sql
- 04_dbt_meridian_dw/snapshots/snap_branches.sql
- 04_dbt_meridian_dw/macros/helpers.sql
- 04_dbt_meridian_dw/macros/generate_schema_name.sql

Chapters
00:00 Project anatomy
08:00 VARIANT becomes typed rows
16:00 QUALIFY keeps one row
24:00 Freshness
32:00 Snapshots, run twice
40:00 A safe dev sandbox

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

A second snapshot version is the expected shape when a tracked column changes. Quote a version count only after that run.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#dbt #DataEngineering #AnalyticsEngineering #Snowflake #SQL

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Episode 4, so bronze has rows to parse.
- dbt Core with the packages in packages.yml.
- A local profiles file based on profiles.yml.example. The real profiles.yml stays off camera.

## Files covered

- `04_dbt_meridian_dw/dbt_project.yml`
- `04_dbt_meridian_dw/packages.yml`
- `04_dbt_meridian_dw/selectors.yml`
- `04_dbt_meridian_dw/profiles.yml.example`
- `04_dbt_meridian_dw/models/staging/postgres/_postgres__sources.yml`
- `04_dbt_meridian_dw/models/staging/postgres/stg_postgres__transactions.sql`
- `04_dbt_meridian_dw/snapshots/snap_customers.sql`
- `04_dbt_meridian_dw/snapshots/snap_accounts.sql`
- `04_dbt_meridian_dw/snapshots/snap_branches.sql`
- `04_dbt_meridian_dw/macros/helpers.sql`
- `04_dbt_meridian_dw/macros/generate_schema_name.sql`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 Project anatomy
08:00 VARIANT becomes typed rows
16:00 QUALIFY keeps one row
24:00 Freshness
32:00 Snapshots, run twice
40:00 A safe dev sandbox
```

## Hashtags

#dbt #DataEngineering #AnalyticsEngineering #Snowflake #SQL

## Tags

dbt, analytics engineering, Snowflake, staging models, QUALIFY, source freshness, snapshots, SCD2, data engineering, incremental model, Meridian Bank, tutorial

## Pinned comment

Open stg_postgres__transactions.sql and find the QUALIFY that keeps one row per key.

What is the difference between a freshness check and a content test?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 5 is up: dbt turns VARIANT into one typed row per key, then snapshots the customer. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E6 — The star schema, for real. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E6), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e5-dbt-cleans-inbox.mp4

## Thumbnail

- File: `thumbnails/E5.jpg`
- Red corner tag: EPISODE 5
- Headline: TURN RAW JSON INTO CLEAN TABLES
- Handwritten line: dbt staging on Snowflake

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Snapshot version counts are quoted only from the run you just did.
- [ ] profiles.yml is not shown.

# E3 — Snowflake: rooms, keys, shelves

Planned length: 40 minutes. Playlist position: 4 of 15.
Grounding: course/show/e3.html chapters The computer, The locks, Empty shelves, and course/show.html (40 min, 18 scenes).

## Title

Meridian E3: Snowflake rooms, roles, and shelves that stay empty

## Hook

Storage, compute, and a key that stays on your laptop. The bronze tables are created empty.
A Snowflake primary key is a label. The test is the lock. The demo stream is not the pipeline.

## Description

Storage, compute, and a key that stays on your laptop. The bronze tables are created empty.
A Snowflake primary key is a label. The test is the lock. The demo stream is not the pipeline.

Snowflake is opened as three separate bills: storage, compute, and cloud services. The setup script creates four warehouses for four jobs and a resource monitor written as 100 credits a month. That number is a limit in the file, not a bill already spent. People receive roles. The public key is attached in Snowflake. The private key stays on the laptop. Two databases are created, then empty append-only VARIANT shelves with five metadata columns. Streams, tasks, and dynamic tables are a demo file, then suspended. They are not the working path. The unit test transaction_status_update_keeps_the_latest_version uses fixture id 101. That fixture is not a live warehouse count.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E3 in the playlist, position 4 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Watch E0, E1, and E2.
- A Snowflake Enterprise trial. Create it in this episode.
- No password is stored in the repository. The private key never goes in the description or the chat.

Files covered
- 03_snowflake/01_account_setup_rbac.sql
- 03_snowflake/02_databases_schemas_grants.sql
- 03_snowflake/03_stages_raw_tables_control.sql
- 03_snowflake/04_streams_tasks_dynamic_tables_demo.sql
- 03_snowflake/05_time_travel_clone_demo.sql
- 03_snowflake/08_cost_attribution.sql
- 03_snowflake/09_zero_copy_dev_environment.sql
- 03_snowflake/10_dr_exercises.sql
- 11_platform_terraform/main.tf
- 00_architecture/adr/0002-append-only-variant-raw.md
- 00_architecture/adr/0004-dbt-plus-airflow.md

Chapters
00:00 The computer
06:00 Four warehouses, four jobs
12:00 The locks
20:00 Key pair, not a password
26:00 Empty shelves
33:00 A key is a label

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

Call a Snowflake number a live result only after you have run the statement and read it back. The key demo and fixture 101 are not a live warehouse count. The shelves are empty on purpose.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#Snowflake #DataEngineering #DataWarehouse #SQL #RBAC

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Watch E0, E1, and E2.
- A Snowflake Enterprise trial. Create it in this episode.
- No password is stored in the repository. The private key never goes in the description or the chat.

## Files covered

- `03_snowflake/01_account_setup_rbac.sql`
- `03_snowflake/02_databases_schemas_grants.sql`
- `03_snowflake/03_stages_raw_tables_control.sql`
- `03_snowflake/04_streams_tasks_dynamic_tables_demo.sql`
- `03_snowflake/05_time_travel_clone_demo.sql`
- `03_snowflake/08_cost_attribution.sql`
- `03_snowflake/09_zero_copy_dev_environment.sql`
- `03_snowflake/10_dr_exercises.sql`
- `11_platform_terraform/main.tf`
- `00_architecture/adr/0002-append-only-variant-raw.md`
- `00_architecture/adr/0004-dbt-plus-airflow.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

```
00:00 The computer
06:00 Four warehouses, four jobs
12:00 The locks
20:00 Key pair, not a password
26:00 Empty shelves
33:00 A key is a label
```

## Hashtags

#Snowflake #DataEngineering #DataWarehouse #SQL #RBAC

## Tags

Snowflake, data warehouse, data engineering, RBAC, key pair authentication, VARIANT, Time Travel, zero copy clone, streams and tasks, dynamic tables, primary key, Meridian Bank, tutorial

## Pinned comment

Run 03_snowflake/01_account_setup_rbac.sql as ACCOUNTADMIN, then stop before you invent a row count.

What does Snowflake store for a primary key, and what does it actually enforce?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E3 is up: Snowflake rooms, roles, and empty bronze shelves. A key in Snowflake is a label. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, P0 — Python foundations for this pipeline. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (P0), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e3-rooms-keys-shelves.mp4

## Thumbnail

- File: `thumbnails/E3.png`
- Badge: EPISODE 3
- On-image hook: Rooms, then shelves
- Tech: Snowflake

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Resource monitor 100 credits is the script's limit, not a spent total.
- [ ] Fixture id 101 is not described as a live warehouse count.
- [ ] The streams demo is labelled as not the working path.

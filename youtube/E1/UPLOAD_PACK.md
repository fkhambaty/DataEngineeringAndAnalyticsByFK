# E1 — The bank comes alive

Planned length: 55 minutes. Playlist position: 2 of 15.
Grounding: course/show.html episode E1 (55 min, 16 scenes: medallion, toolkit, PostgreSQL, twenty tables, a moving bank) and the setup plus source plan in course/teach.html. Deck: course/show/e1.html.

## Title

Meridian Episode 1: The fictional bank comes alive in PostgreSQL

## Hook

One payment shows raw, staging, and marts, then PostgreSQL in Docker starts moving.
The warehouse product stays closed. The bank on the laptop does not.

## Description

One payment shows raw, staging, and marts, then PostgreSQL in Docker starts moving.
The warehouse product stays closed. The bank on the laptop does not.

Episode 1 puts one payment through bronze, silver, and gold in plain words, then installs the laptop toolkit and builds the source. PostgreSQL 16 runs in Docker. The core schema is normalised. The seed and the simulator make the bank move, and the CDC triggers bump updated_at and log deletes. Card tables are created with the same source, ready for a later episode. Snowflake is not opened.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E1 in the playlist, position 2 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Watch E0 first.
- Docker Desktop, Python 3.12, Git, and an editor, using setup/MACOS_SETUP.md or setup/WINDOWS_SETUP.md.
- python3 setup/verify_setup.py passes before you record the source build.

Files covered
- setup/verify_setup.py
- setup/start_postgres.py
- setup/MACOS_SETUP.md
- setup/WINDOWS_SETUP.md
- 01_source_postgres/docker-compose.postgres.yml
- 01_source_postgres/00_create_database.sql
- 01_source_postgres/01_ddl_core_schema.sql
- 01_source_postgres/02_seed_reference_data.sql
- 01_source_postgres/03_seed_bulk_data.sql
- 01_source_postgres/04_cdc_triggers.sql
- 01_source_postgres/05_dml_simulator_functions.sql
- 01_source_postgres/06_sql_lessons.sql
- 01_source_postgres/07_ddl_cards.sql
- 01_source_postgres/08_seed_cards.sql
- 01_source_postgres/09_card_simulator.sql

Chapters
00:00 One payment, three layers
08:00 The toolkit on the laptop
18:00 PostgreSQL in Docker
30:00 The normalised source
42:00 The seeded payments
50:00 The bank starts moving

Adjust these timestamps after the final edit. They are drafted to the planned 55-minute cut, not to a finished timeline.

The moving rows are local PostgreSQL. This episode does not show a Snowflake result.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#PostgreSQL #DataEngineering #SQL #Docker #OLTP

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Watch E0 first.
- Docker Desktop, Python 3.12, Git, and an editor, using setup/MACOS_SETUP.md or setup/WINDOWS_SETUP.md.
- python3 setup/verify_setup.py passes before you record the source build.

## Files covered

- `setup/verify_setup.py`
- `setup/start_postgres.py`
- `setup/MACOS_SETUP.md`
- `setup/WINDOWS_SETUP.md`
- `01_source_postgres/docker-compose.postgres.yml`
- `01_source_postgres/00_create_database.sql`
- `01_source_postgres/01_ddl_core_schema.sql`
- `01_source_postgres/02_seed_reference_data.sql`
- `01_source_postgres/03_seed_bulk_data.sql`
- `01_source_postgres/04_cdc_triggers.sql`
- `01_source_postgres/05_dml_simulator_functions.sql`
- `01_source_postgres/06_sql_lessons.sql`
- `01_source_postgres/07_ddl_cards.sql`
- `01_source_postgres/08_seed_cards.sql`
- `01_source_postgres/09_card_simulator.sql`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 55-minute cut, not to a finished timeline.

```
00:00 One payment, three layers
08:00 The toolkit on the laptop
18:00 PostgreSQL in Docker
30:00 The normalised source
42:00 The seeded payments
50:00 The bank starts moving
```

## Hashtags

#PostgreSQL #DataEngineering #SQL #Docker #OLTP

## Tags

PostgreSQL, Docker, data engineering, SQL, OLTP, medallion architecture, bronze silver gold, source system, CDC trigger, Meridian Bank, tutorial, database design

## Pinned comment

Clone the repository and run python3 setup/verify_setup.py before Episode 1's source build.

Where does a normalised OLTP schema start to fight an analyst's question?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 1 is up: a fictional bank comes alive in PostgreSQL. Raw, staging, and marts, then a moving source. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E2 — Draw the warehouse first. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E2), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e1-bank-comes-alive.mp4

## Thumbnail

- File: `thumbnails/E1.png`
- Badge: EPISODE 1
- On-image hook: The bank wakes up
- Tech: PostgreSQL

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] The on-screen bank is PostgreSQL in Docker, not a Snowflake worksheet.
- [ ] Say Episode 1 when you introduce the badge.

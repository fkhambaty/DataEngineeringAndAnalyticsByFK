# E1 — The bank comes alive

Status: published (add the URL from YouTube Studio). Title, description and tags below are exactly what is live.
Planned length: 55 minutes. Playlist position: 2 of 15.
Grounding: course/show.html episode E1 (55 min, 16 scenes: medallion, toolkit, PostgreSQL, twenty tables, a moving bank) and the setup plus source plan in course/teach.html. Deck: course/show/e1.html.

## Title

Build a Real Bank on Your Laptop | PostgreSQL + 5 Million Payments | Episode 1

## Hook

One payment shows raw, staging, and marts, then PostgreSQL in Docker starts moving.
The warehouse product stays closed. The bank on the laptop does not.

## Description

#DataEngineering #PostgreSQL #Docker

A real bank, on your laptop. PostgreSQL 16 in Docker, 20 tables, and 5 million payments that keep arriving while you watch.

This is Episode 1 of the series. We do not open Snowflake yet. First the source has to be alive.

Code and setup guides:
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Mac: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK/blob/main/setup/MACOS_SETUP.md
Windows: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK/blob/main/setup/WINDOWS_SETUP.md

You will install the tools, start PostgreSQL, build the bank, connect with DBeaver, and see bronze, silver and gold on one payment.

Run these from the repository folder:

docker compose -f 01_source_postgres/docker-compose.postgres.yml up -d
python3 setup/start_postgres.py
python3 setup/verify_setup.py

Windows:
py -3.12 setup\start_postgres.py
py -3.12 setup\verify_setup.py

DBeaver: localhost, port 5432, database meridian_core, user meridian, password meridian.

Then, inside DBeaver:
SELECT * FROM core.sim_tick(500);

Next episode: draw the warehouse on paper before opening Snowflake.

Watch the intro first if you are new to the series.

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

#DataEngineering #PostgreSQL #Docker

## Tags

postgresql, postgres tutorial, docker, data engineering, dbeaver, sql, medallion architecture, python, snowflake, dbt, airflow, learn data engineering, episode 1

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

- File: `thumbnails/E1.jpg`
- Red corner tag: EPISODE 1
- Headline: BUILD A REAL BANK ON YOUR LAPTOP
- Handwritten line: PostgreSQL · 5 million payments

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] The on-screen bank is PostgreSQL in Docker, not a Snowflake worksheet.
- [ ] Say Episode 1 when you introduce the badge.

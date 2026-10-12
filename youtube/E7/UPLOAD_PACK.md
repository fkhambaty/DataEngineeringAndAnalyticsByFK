# E7 — Airflow is the alarm clock

Status: not published yet.
Planned length: 30 minutes. Playlist position: 9 of 15.
Grounding: course/show.html episode E7 (30 min, 14 scenes: five-minute DAG, nightly DAG, Docker paths, pools, retries, alerts) and the Airflow plan in course/teach.html. Deck: course/show/e7.html.

## Title

Airflow Runs It Every 5 Minutes | Schedule dbt and Snowflake | Episode 7

## Hook

Two clocks, one scheduler. Airflow never builds the star.
The replay is manual, and it leaves the live watermark where it is.

## Description

Two clocks, one scheduler. Airflow never builds the star.
The replay is manual, and it leaves the live watermark where it is.

Airflow is the alarm clock. dbt and Python still do the work. The five-minute DAG extracts the hot tables through a Postgres pool, loads them, then runs the narrow dbt selector. A health gate can stop the DAG. The nightly DAG loads reference data and the wider models. Freshness runs on its own schedule. Bounded replay takes a since and until window and does not move the live watermark. Retries, pools, and alerts are in the DAG files. Astro runs Airflow 3 on the laptop.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 7, video 9 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Episode 4, Episode 5, and Episode 6, so there is something to schedule.
- Astro CLI, installed in this episode rather than during laptop setup.

Files covered
- 05_airflow/dags/_common.py
- 05_airflow/dags/meridian_microbatch_ingest.py
- 05_airflow/dags/meridian_daily_batch.py
- 05_airflow/dags/meridian_source_freshness.py
- 05_airflow/dags/meridian_bounded_replay.py
- 05_airflow/dags/meridian_card_decisioning.py
- 05_airflow/dags/meridian_alerts.py
- 05_airflow/airflow_settings.yaml.example
- 05_airflow/README.md
- 00_architecture/adr/0004-dbt-plus-airflow.md

Chapters
00:00 Airflow rings the clock
06:00 The five-minute DAG
14:00 The nightly DAG
20:00 Pools, retries, alerts
25:00 Bounded replay

Adjust these timestamps after the final edit. They are drafted to the planned 30-minute cut, not to a finished timeline.

Task success on screen is that Airflow run. Do not describe a green box as proof of warehouse totals you did not query.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#ApacheAirflow #DataEngineering #dbt #Orchestration #ETL

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Episode 4, Episode 5, and Episode 6, so there is something to schedule.
- Astro CLI, installed in this episode rather than during laptop setup.

## Files covered

- `05_airflow/dags/_common.py`
- `05_airflow/dags/meridian_microbatch_ingest.py`
- `05_airflow/dags/meridian_daily_batch.py`
- `05_airflow/dags/meridian_source_freshness.py`
- `05_airflow/dags/meridian_bounded_replay.py`
- `05_airflow/dags/meridian_card_decisioning.py`
- `05_airflow/dags/meridian_alerts.py`
- `05_airflow/airflow_settings.yaml.example`
- `05_airflow/README.md`
- `00_architecture/adr/0004-dbt-plus-airflow.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 30-minute cut, not to a finished timeline.

```
00:00 Airflow rings the clock
06:00 The five-minute DAG
14:00 The nightly DAG
20:00 Pools, retries, alerts
25:00 Bounded replay
```

## Hashtags

#ApacheAirflow #DataEngineering #dbt #Orchestration #ETL

## Tags

Apache Airflow, Astro, data engineering, orchestration, dbt, DAG, micro-batch, retries, data pipeline, Meridian Bank, tutorial, ETL

## Pinned comment

Open meridian_microbatch_ingest.py and point at the task that shells out to dbt.

What does the bounded replay refuse to change?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 7 is up: Airflow rings two clocks. It schedules the pipeline and does not transform the data. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E8 — Break it, measure, fix. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E8), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e7-airflow-alarm-clock.mp4

## Thumbnail

- File: `thumbnails/E7.jpg`
- Red corner tag: EPISODE 7
- Headline: AIRFLOW RUNS IT EVERY 5 MINUTES
- Handwritten line: Schedule dbt, never babysit it

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] A green task is not narrated as a warehouse total.

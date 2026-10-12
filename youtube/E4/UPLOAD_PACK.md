# E4 — Python carries only what changed

Planned length: 40 minutes. Playlist position: 6 of 15.
Grounding: course/show.html episode E4 (40 min, 15 scenes: watermarks, Parquet, retries, first load, pipeline health) and Module 4 in course/teach.html. Deck: course/show/e4.html.

## Title

Meridian E4: Python carries only the rows that changed

## Hook

The extractor carries the rows that changed, and it moves the bookmark only after success.
Parquet keeps the cents exact. Deletes ride along in their own table.

## Description

The extractor carries the rows that changed, and it moves the bookmark only after success.
Parquet keeps the cents exact. Deletes ride along in their own table.

Python does the hop dbt cannot do: read PostgreSQL, write typed Parquet, PUT to an internal stage, and COPY INTO an append-only VARIANT table. The first watermark in code is 1900-01-01, so the first success is a full load. The lag default is 10 seconds so an in-flight commit is not skipped. The watermark advances to the maximum cursor actually seen, and only after the copy succeeds. Overlapping batches are allowed. Staging dedupes later. Deletes travel in cdc.deleted_records. Retries do not double-advance the bookmark.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E4 in the playlist, position 6 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- P0, a running PostgreSQL source from E1, and the empty raw tables plus key-pair auth from E3.
- Copy .env.example to a local env file. Never show that file.

Files covered
- 02_ingestion_python/config.py
- 02_ingestion_python/pg_to_snowflake.py
- 02_ingestion_python/simulate_activity.py
- 02_ingestion_python/reconcile_with_pandas.py
- 02_ingestion_python/README.md
- .env.example
- tests/test_extractor.py
- tests/test_reconciliation.py
- 00_architecture/adr/0001-watermark-cdc-before-log-based.md

Chapters
00:00 The watermark, drawn
08:00 The first full load
18:00 Parquet, PUT, COPY
26:00 The five-minute loop
33:00 Health view and replay

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

If you show LOAD_LOG or the health view, those numbers are from the run on screen. Do not type a row count from memory into the description.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#Python #CDC #DataEngineering #Parquet #Snowflake

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- P0, a running PostgreSQL source from E1, and the empty raw tables plus key-pair auth from E3.
- Copy .env.example to a local env file. Never show that file.

## Files covered

- `02_ingestion_python/config.py`
- `02_ingestion_python/pg_to_snowflake.py`
- `02_ingestion_python/simulate_activity.py`
- `02_ingestion_python/reconcile_with_pandas.py`
- `02_ingestion_python/README.md`
- `.env.example`
- `tests/test_extractor.py`
- `tests/test_reconciliation.py`
- `00_architecture/adr/0001-watermark-cdc-before-log-based.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

```
00:00 The watermark, drawn
08:00 The first full load
18:00 Parquet, PUT, COPY
26:00 The five-minute loop
33:00 Health view and replay
```

## Hashtags

#Python #CDC #DataEngineering #Parquet #Snowflake

## Tags

Python, CDC, watermark, Parquet, Snowflake COPY, data engineering, ETL, idempotent load, incremental extract, Meridian Bank, pipeline, tutorial

## Pinned comment

Read pg_to_snowflake.py from main() down to the watermark update.

Why does the bookmark move to the latest row you saw, and only after success?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E4 is up: Python carries only the rows that changed. The bookmark moves after a successful copy. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E5 — dbt cleans the inbox. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E5), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e4-only-what-changed.mp4

## Thumbnail

- File: `thumbnails/E4.png`
- Badge: EPISODE 4
- On-image hook: Only what changed
- Tech: Watermark CDC

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Any LOAD_LOG number on screen is from that run, not from this pack.
- [ ] The .env file is never shown.

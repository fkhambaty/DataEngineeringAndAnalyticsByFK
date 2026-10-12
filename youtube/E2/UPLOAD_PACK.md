# E2 — Draw the warehouse first

Planned length: 45 minutes. Playlist position: 3 of 15.
Grounding: course/show.html episode E2 (45 min, 14 scenes: grain, facts, dimensions, SCD2, fan-out, bus matrix) and Module 2 in course/teach.html. Deck: course/show/e2.html.

## Title

Meridian E2: Draw the star schema before you open Snowflake

## Hook

Declare the grain before you draw a single box of the star.
A customer who changes segment must still be counted as they were on the day.

## Description

Declare the grain before you draw a single box of the star.
A customer who changes segment must still be counted as they were on the day.

Kimball's four steps are done live: name the process, declare the grain, list the dimensions, then name the facts. The bus matrix is filled cell by cell. One customer is drawn with three versions on a timeline, and a transaction is dropped onto the version that was true that day. Transaction, periodic snapshot, and accumulating snapshot are three different facts. Flows and stocks are not added together. A join that forgets the time window multiplies the money. That is a grain error.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E2 in the playlist, position 3 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Watch E0 and E1.
- No Snowflake account. A whiteboard and 07_data_modelling/BUS_MATRIX.md are the whole studio.

Files covered
- 07_data_modelling/BUS_MATRIX.md
- 07_data_modelling/star_schema.mmd
- 00_architecture/adr/0003-kimball-for-the-presentation-layer.md
- 06_performance_lab/04_join_explosion_scd2.sql
- 04_dbt_meridian_dw/tests/assert_scd2_no_overlapping_versions.sql

Chapters
00:00 Kimball in four steps
08:00 Fill the bus matrix
18:00 Three versions on a timeline
28:00 Three kinds of fact
36:00 Flows are not stocks

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

This episode has no Snowflake session. The fan-out drawing is the grain lesson. It is not a counted warehouse total.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#Kimball #DataModeling #DataEngineering #StarSchema #SCD2

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Watch E0 and E1.
- No Snowflake account. A whiteboard and 07_data_modelling/BUS_MATRIX.md are the whole studio.

## Files covered

- `07_data_modelling/BUS_MATRIX.md`
- `07_data_modelling/star_schema.mmd`
- `00_architecture/adr/0003-kimball-for-the-presentation-layer.md`
- `06_performance_lab/04_join_explosion_scd2.sql`
- `04_dbt_meridian_dw/tests/assert_scd2_no_overlapping_versions.sql`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 Kimball in four steps
08:00 Fill the bus matrix
18:00 Three versions on a timeline
28:00 Three kinds of fact
36:00 Flows are not stocks
```

## Hashtags

#Kimball #DataModeling #DataEngineering #StarSchema #SCD2

## Tags

Kimball, dimensional modelling, star schema, bus matrix, SCD2, grain, fact table, dimension, data engineering, data warehouse, fan-out, Meridian Bank, tutorial

## Pinned comment

Open 07_data_modelling/BUS_MATRIX.md and say one grain as a sentence before you draw the star.

Which fact in that matrix is a stock, and which is a flow?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E2 is up: draw the star before Snowflake. Grain, versions, and three kinds of fact. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E3 — Snowflake: rooms, keys, shelves. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E3), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e2-draw-the-star.mp4

## Thumbnail

- File: `thumbnails/E2.png`
- Badge: EPISODE 2
- On-image hook: Draw the star first
- Tech: Kimball

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] No Snowflake screen is in this cut.
- [ ] The fan-out example is not quoted as a live row count.

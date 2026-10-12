# E0 — The problem, then the picture

Status: published (https://www.youtube.com/watch?v=aMUeQKyW51k). Title, description and tags below are exactly what is live.
Planned length: 45 minutes. Playlist position: 1 of 15.
Grounding: course/show.html episode E0 (45 min, 14 scenes) and the Episode 0 plan in course/teach.html. Deck: course/show/e0.html.

## Title

Snowflake, dbt, Airflow Project | PostgreSQL, SQL, Data Engineering

## Hook

Five promises from a fictional bank, then a picture that is not allowed to name a tool.
You should be able to say one grain out loud and name the design that was rejected.

## Description

End-to-end data engineering project with Snowflake, dbt, Airflow, PostgreSQL, and SQL. Don't learn Snowflake alone. Build the whole analytics stack.

This is the intro. A bank with 520 branches already has every answer in PostgreSQL, and it still cannot ask a big question without slowing down the customer at the ATM.

In this episode:
- Meridian Bank: 520 branches, 5 countries, 5 currencies, 200,000 customers, 5 million payments
- The questions leadership cannot ask today
- OLTP versus OLAP, and why a read-only copy of PostgreSQL is not enough
- One job each: PostgreSQL, Python, Parquet, Snowflake, dbt, Airflow, Streamlit, Docker, GitHub Actions

The bank is fictional. The tools and the pipeline are real. Later episodes build the source database, the Snowflake warehouse, the Python load, the dbt models, the Airflow schedule, data quality, and asking the data in English.

Playlist: End-to-End Data Engineering Project | PostgreSQL, Snowflake, dbt, Airflow

#Snowflake #dbt #DataEngineering

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- The public student repository.
- No Snowflake account, Docker, or warehouse result is required.

## Files covered

- `00_architecture/DESIGN_DOC.md`
- `00_architecture/ARCHITECTURE_PROCESS.md`
- `00_architecture/diagrams/01_context.mmd`
- `00_architecture/diagrams/02_container.mmd`
- `00_architecture/diagrams/03_conceptual.mmd`
- `00_architecture/diagrams/04_data_flow.mmd`
- `00_architecture/adr/README.md`
- `00_architecture/adr/0001-watermark-cdc-before-log-based.md`
- `00_architecture/adr/0002-append-only-variant-raw.md`
- `00_architecture/adr/0003-kimball-for-the-presentation-layer.md`
- `00_architecture/adr/0004-dbt-plus-airflow.md`
- `00_architecture/adr/0005-model-scores-land-in-the-warehouse.md`
- `00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md`
- `00_architecture/adr/0007-open-table-formats-deferred.md`
- `00_architecture/adr/0008-one-owner-per-object-type.md`
- `00_architecture/adr/0009-omni-search-is-a-serving-index.md`
- `00_architecture/adr/0010-contracts-at-public-boundaries.md`
- `00_architecture/adr/0011-multitenancy-patterns.md`
- `07_data_modelling/BUS_MATRIX.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 The business asks
07:00 A picture with no tool names
14:00 What the bank would recognise
22:00 One grain, said out loud
30:00 One payment, six rooms
38:00 The design we rejected
```

## Hashtags

#Snowflake #dbt #DataEngineering

## Tags

snowflake tutorial, snowflake project, dbt tutorial, dbt snowflake, apache airflow, airflow tutorial, postgresql, postgres, sql, data engineering, data engineering project, end to end data engineering, analytics engineering, data analytics, postgresql to snowflake, python data engineering, elt pipeline, data warehouse, data pipeline project, learn snowflake dbt airflow

## Pinned comment

Open 00_architecture/DESIGN_DOC.md beside the video.

Which requirement would you refuse to solve with streaming on day one, and why?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E0 is up: the warehouse picture before any tool name. One grain, said as a sentence. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E1 — The bank comes alive. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E1), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e0-problem-then-picture.mp4

## Thumbnail

- File: `thumbnails/E0.jpg`
- Red corner tag: INTRO VIDEO
- Headline: DON'T LEARN SNOWFLAKE ALONE
- Handwritten line: Learn the whole stack

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] No tool logo appears before the decision record.
- [ ] The rejected alternative is named out loud.

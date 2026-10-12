# E0 — The problem, then the picture

Planned length: 45 minutes. Playlist position: 1 of 15.
Grounding: course/show.html episode E0 (45 min, 14 scenes) and the Episode 0 plan in course/teach.html. Deck: course/show/e0.html.

## Title

Meridian E0: Design the warehouse before a single tool is named

## Hook

Five promises from a fictional bank, then a picture that is not allowed to name a tool.
You should be able to say one grain out loud and name the design that was rejected.

## Description

Five promises from a fictional bank, then a picture that is not allowed to name a tool.
You should be able to say one grain out loud and name the design that was rejected.

This episode is a design review. It walks the business asks and the non-functional requirements in the design doc, including a 5-minute micro-batch and a 15-minute p95, not streaming. The context picture has no product names. The conceptual model is one a banker would recognise. One grain is said as a sentence from the bus matrix. One decision record includes the option that was refused. SQL stays closed until that picture is done.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E0 in the playlist, position 1 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- The public student repository.
- No Snowflake account, Docker, or warehouse result is required.

Files covered
- 00_architecture/DESIGN_DOC.md
- 00_architecture/ARCHITECTURE_PROCESS.md
- 00_architecture/diagrams/01_context.mmd
- 00_architecture/diagrams/02_container.mmd
- 00_architecture/diagrams/03_conceptual.mmd
- 00_architecture/diagrams/04_data_flow.mmd
- 00_architecture/adr/README.md
- 00_architecture/adr/0001-watermark-cdc-before-log-based.md
- 00_architecture/adr/0002-append-only-variant-raw.md
- 00_architecture/adr/0003-kimball-for-the-presentation-layer.md
- 00_architecture/adr/0004-dbt-plus-airflow.md
- 00_architecture/adr/0005-model-scores-land-in-the-warehouse.md
- 00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md
- 00_architecture/adr/0007-open-table-formats-deferred.md
- 00_architecture/adr/0008-one-owner-per-object-type.md
- 00_architecture/adr/0009-omni-search-is-a-serving-index.md
- 00_architecture/adr/0010-contracts-at-public-boundaries.md
- 00_architecture/adr/0011-multitenancy-patterns.md
- 07_data_modelling/BUS_MATRIX.md

Chapters
00:00 The business asks
07:00 A picture with no tool names
14:00 What the bank would recognise
22:00 One grain, said out loud
30:00 One payment, six rooms
38:00 The design we rejected

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

There is no Snowflake worksheet in this episode, and no warehouse count to treat as a live result.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#DataEngineering #DataArchitecture #AnalyticsEngineering #Kimball #DataWarehouse

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

#DataEngineering #DataArchitecture #AnalyticsEngineering #Kimball #DataWarehouse

## Tags

data engineering, data architecture, analytics engineering, Kimball, bus matrix, data warehouse design, dimensional modelling, Meridian Bank, system design, decision record, requirements, fictional bank, tutorial

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

- File: `thumbnails/E0.png`
- Badge: EPISODE 0
- On-image hook: Picture before tools
- Tech: Architecture

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] No tool logo appears before the decision record.
- [ ] The rejected alternative is named out loud.

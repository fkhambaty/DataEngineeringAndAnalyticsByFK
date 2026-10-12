# E8 — Break it, measure, fix

Planned length: 45 minutes. Playlist position: 10 of 15.
Grounding: course/show/e8.html chapters Four beats, Read less, One change, The second run, and course/show.html (45 min, 16 scenes).

## Title

Meridian E8: Break the query, measure it, then fix one thing

## Hook

Read the query profile before you resize anything.
Pruning, spilling, and a lying cache are three different problems. The 3x join is an example, not a live total.

## Description

Read the query profile before you resize anything.
Pruning, spilling, and a lying cache are three different problems. The 3x join is an example, not a live total.

One habit: measure, name the waste, change one thing, measure again. The Postgres lab shows a sequential scan and then an index. The Snowflake pruning lab is written against a 100,000,000-row table. Record that build before the episode. A function wrapped around the filter column can blind pruning. Spilling means the work did not fit in memory. Rewrite before you resize. The join-explosion file's example, not a live total, is that 3 customer versions count 3 times. Search optimization is for needles. Clustering is for ranges. The second run can be the warehouse cache. Scale-up and scale-out answer different queues. The triage playbook is the order you say out loud.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E8 in the playlist, position 10 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- PostgreSQL from E1 and a Snowflake warehouse from E3.
- Build the large pruning table before you record, then cut to the result.
- Keep the scoreboard worksheet ready. Read it after each fix.

Files covered
- 06_performance_lab/README.md
- 06_performance_lab/00_measure.sql
- 06_performance_lab/01_postgres_missing_index.sql
- 06_performance_lab/02_snowflake_pruning_clustering.sql
- 06_performance_lab/03_spilling_and_warehouse_size.sql
- 06_performance_lab/04_join_explosion_scd2.sql
- 06_performance_lab/05_caching_layers.sql
- 06_performance_lab/06_predicate_antipatterns.sql
- 06_performance_lab/07_search_optimization_and_mv.sql
- 06_performance_lab/08_dbt_incremental_vs_full_refresh.md
- 06_performance_lab/09_warehouse_sizing_and_concurrency.sql
- 06_performance_lab/10_slow_query_triage_playbook.sql

Chapters
00:00 Four beats
08:00 Read less
20:00 One change
32:00 The second run
40:00 The triage order

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

The 3-version multiplier is the file's example, not a live total. Quote bytes scanned, spill, or duration only from the measure query you just ran. The whole-lab credit remark in the teaching notes is an upper bound to check with WAREHOUSE_METERING_HISTORY, not a number to invent.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#Snowflake #SQLPerformance #DataEngineering #QueryOptimization #dbt

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- PostgreSQL from E1 and a Snowflake warehouse from E3.
- Build the large pruning table before you record, then cut to the result.
- Keep the scoreboard worksheet ready. Read it after each fix.

## Files covered

- `06_performance_lab/README.md`
- `06_performance_lab/00_measure.sql`
- `06_performance_lab/01_postgres_missing_index.sql`
- `06_performance_lab/02_snowflake_pruning_clustering.sql`
- `06_performance_lab/03_spilling_and_warehouse_size.sql`
- `06_performance_lab/04_join_explosion_scd2.sql`
- `06_performance_lab/05_caching_layers.sql`
- `06_performance_lab/06_predicate_antipatterns.sql`
- `06_performance_lab/07_search_optimization_and_mv.sql`
- `06_performance_lab/08_dbt_incremental_vs_full_refresh.md`
- `06_performance_lab/09_warehouse_sizing_and_concurrency.sql`
- `06_performance_lab/10_slow_query_triage_playbook.sql`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 Four beats
08:00 Read less
20:00 One change
32:00 The second run
40:00 The triage order
```

## Hashtags

#Snowflake #SQLPerformance #DataEngineering #QueryOptimization #dbt

## Tags

Snowflake performance, query optimization, pruning, clustering, spilling, warehouse sizing, join explosion, SCD2, data engineering, SQL, cache, Meridian Bank, tutorial

## Pinned comment

Open 06_performance_lab/10_slow_query_triage_playbook.sql and say the order before you touch a warehouse size.

Which problem is pruning, and which problem is spilling?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E8 is up: break one query, measure it, fix one thing. The 3x join is an example, not a live total. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E9 — Quality, CI, cost, runbook. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E9), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e8-break-measure-fix.mp4

## Thumbnail

- File: `thumbnails/E8.png`
- Badge: EPISODE 8
- On-image hook: Measure, then fix
- Tech: Performance lab

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] The 3-version join is called an example, not a live total.
- [ ] No duration or credit figure is spoken unless it was just read from the account.

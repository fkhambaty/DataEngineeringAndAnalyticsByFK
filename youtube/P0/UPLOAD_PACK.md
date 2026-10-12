# P0 — Python foundations for this pipeline

Status: not published yet.
Planned length: 35 minutes. Playlist position: 5 of 15.
Grounding: course/show.html release P0 (35 min, 17 scenes) and the Python foundations section in course/teach.html. Deck: course/show/py0.html.

## Title

Python for Data Engineers | Read the Pipeline Line by Line | Python Primer

## Hook

Run Python, read the syntax, and see what each library is for.
Then reconcile two tiny systems before you trust a multi-million-row load.

## Description

Run Python, read the syntax, and see what each library is for.
Then reconcile two tiny systems before you trust a multi-million-row load.

This primer sits between Snowflake setup and the extractor. A browser editor is only for the first few minutes of print, variables, if, and a loop. Meridian itself uses Python 3.12 on the laptop, because a browser cannot see Docker, local Parquet, or the project settings. The four files cover values and casting, decisions and loops, functions, lists and dictionaries, imports, paths, arguments, exceptions, and a mini reconciliation with a non-zero exit when the totals disagree. pandas, pyarrow, psycopg, and the Snowflake connector are named as toolboxes, not as a second language.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Python Primer, video 5 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Python 3.12 from the Episode 1 setup.
- No Snowflake connection is required to run the four foundation files.

Files covered
- 02_ingestion_python/00_python_foundations/01_values_and_decisions.py
- 02_ingestion_python/00_python_foundations/02_loops_and_functions.py
- 02_ingestion_python/00_python_foundations/03_collections_paths_libraries.py
- 02_ingestion_python/00_python_foundations/04_mini_reconciliation.py
- 02_ingestion_python/00_python_foundations/README.md
- tests/test_python_foundations.py

Chapters
00:00 Browser practice, then the laptop
06:00 Values, decisions, loops
14:00 Lists, paths, libraries
24:00 A tiny reconciliation
31:00 What the extractor will need

Adjust these timestamps after the final edit. They are drafted to the planned 35-minute cut, not to a finished timeline.

The mini reconciliation uses the tiny tables in the foundations file. It is not a Snowflake production total.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#Python #DataEngineering #LearnPython #ETL #Pandas

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Python 3.12 from the Episode 1 setup.
- No Snowflake connection is required to run the four foundation files.

## Files covered

- `02_ingestion_python/00_python_foundations/01_values_and_decisions.py`
- `02_ingestion_python/00_python_foundations/02_loops_and_functions.py`
- `02_ingestion_python/00_python_foundations/03_collections_paths_libraries.py`
- `02_ingestion_python/00_python_foundations/04_mini_reconciliation.py`
- `02_ingestion_python/00_python_foundations/README.md`
- `tests/test_python_foundations.py`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 35-minute cut, not to a finished timeline.

```
00:00 Browser practice, then the laptop
06:00 Values, decisions, loops
14:00 Lists, paths, libraries
24:00 A tiny reconciliation
31:00 What the extractor will need
```

## Hashtags

#Python #DataEngineering #LearnPython #ETL #Pandas

## Tags

Python, Python tutorial, data engineering, ETL, pandas, pyarrow, functions, exceptions, reconciliation, Meridian Bank, beginner Python, pipeline

## Pinned comment

Run the four files under 02_ingestion_python/00_python_foundations/ before you open the extractor.

What should a failed reconciliation do to the process exit code?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Python primer is up: read the pipeline syntax, then reconcile two tiny systems. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E4 — Python carries only what changed. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E4), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-p0-python-primer.mp4

## Thumbnail

- File: `thumbnails/P0.jpg`
- Red corner tag: PYTHON PRIMER
- Headline: PYTHON FOR DATA ENGINEERS
- Handwritten line: Read every line of the pipeline

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] The thumbnail badge reads PYTHON PRIMER, not an episode number.
- [ ] No measured Snowflake score or row count is quoted.

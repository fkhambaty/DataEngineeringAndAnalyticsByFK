# E11 — Ask in English

Status: not published yet.
Planned length: 45 minutes. Playlist position: 13 of 15.
Grounding: course/show/e11.html chapters The menu, Four people, The lock, Ask it, and course/show.html (45 min, 18 scenes).

## Title

Ask Your Data in Plain English | Snowflake Cortex Analyst + Streamlit | Episode 11

## Hook

The menu stops the model inventing joins. The policy stops the right SQL returning the wrong rows.
Who sees what, on the slide, is the rule in the file. It is not a counted run.

## Description

The menu stops the model inventing joins. The policy stops the right SQL returning the wrong rows.
Who sees what, on the slide, is the rule in the file. It is not a counted run.

The semantic view SV_MERIDIAN_BANK is the menu: allowed tables, joins, metrics, and four questions whose SQL a human already checked. Approval rate is an average of a yes-or-no flag and must not be averaged again. Customers on the menu are who they are today. At the time uses the SCD2 key. Cortex Analyst writes SQL against that view. If the region has no Cortex, ask the same four questions from analyses/card_questions.sql while logged in as each demo user. The persona picture is the rule, not a counted result. The CEO sees every customer. The Mumbai manager and staff see home branch IN-MUM-0001. Staff contact cells are masked. The customer sees only their own id. USE ROLE does not change CURRENT_USER. Log out between demos. A country key labels the row. RAP_COUNTRY_SCOPE is the wall. A WHERE clause is not. The prove-it block at the bottom of 06_row_level_security.sql states expected results from the code, not a counted run, until you execute it.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 11, video 13 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Gold marts from Episode 6 and the card marts from Episode 10.
- Row-access script from 03_snowflake/06_row_level_security.sql, run as ACCOUNTADMIN after the prod build.
- Check Cortex region availability the week you record. Have card_questions.sql ready as the fallback.

Files covered
- 03_snowflake/06_row_level_security.sql
- 03_snowflake/07_omni_search.sql
- 04_dbt_meridian_dw/macros/governance.sql
- 04_dbt_meridian_dw/models/marts/serving/omni_search.sql
- 04_dbt_meridian_dw/models/marts/governance/ent_customer_branch.sql
- 04_dbt_meridian_dw/analyses/card_questions.sql
- 10_semantic_app/01_semantic_view.sql
- 10_semantic_app/streamlit_app.py
- 10_semantic_app/README.md
- 00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md
- 00_architecture/adr/0009-omni-search-is-a-serving-index.md

Chapters
00:00 The menu
10:00 Four people
22:00 The lock
34:00 Ask it

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

Do not narrate persona counts, masked-cell screenshots, or the Hong Kong fixture as measured totals unless you just ran them. The slide is the rule, not a counted run.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#Snowflake #Cortex #DataEngineering #DataGovernance #SemanticLayer

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Gold marts from Episode 6 and the card marts from Episode 10.
- Row-access script from 03_snowflake/06_row_level_security.sql, run as ACCOUNTADMIN after the prod build.
- Check Cortex region availability the week you record. Have card_questions.sql ready as the fallback.

## Files covered

- `03_snowflake/06_row_level_security.sql`
- `03_snowflake/07_omni_search.sql`
- `04_dbt_meridian_dw/macros/governance.sql`
- `04_dbt_meridian_dw/models/marts/serving/omni_search.sql`
- `04_dbt_meridian_dw/models/marts/governance/ent_customer_branch.sql`
- `04_dbt_meridian_dw/analyses/card_questions.sql`
- `10_semantic_app/01_semantic_view.sql`
- `10_semantic_app/streamlit_app.py`
- `10_semantic_app/README.md`
- `00_architecture/adr/0006-row-access-by-user-entitlements-owned-by-security.md`
- `00_architecture/adr/0009-omni-search-is-a-serving-index.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 The menu
10:00 Four people
22:00 The lock
34:00 Ask it
```

## Hashtags

#Snowflake #Cortex #DataEngineering #DataGovernance #SemanticLayer

## Tags

Snowflake, Cortex Analyst, semantic view, row access policy, data governance, masking, data engineering, Streamlit, English to SQL, Meridian Bank, tutorial, analytics

## Pinned comment

Open 10_semantic_app/01_semantic_view.sql and read one verified question before you ask it in English.

Why can the SQL match for four people while the rows do not?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 11 is up: ask the gold layer in English. Same SQL, different rows. The picture is the rule, not a counted run. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E12 — The rules survive a rebuild. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E12), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e11-ask-in-english.mp4

## Thumbnail

- File: `thumbnails/E11.jpg`
- Red corner tag: EPISODE 11
- Headline: ASK YOUR DATA IN PLAIN ENGLISH
- Handwritten line: Cortex Analyst + Streamlit

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] Persona results are called the rule, or expected results, until a live run is read back.
- [ ] Cortex absence is an allowed outcome. The checked SQL is the fallback.
- [ ] Demo passwords are set in Snowsight and are never spoken or typed on screen.

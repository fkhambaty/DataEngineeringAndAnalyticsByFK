# E12 — The rules survive a rebuild

Planned length: 45 minutes. Playlist position: 14 of 15.
Grounding: course/show.html episode E12 (45 min, 16 scenes: one owner per object, contracts that fail, access history) and Module 12 in course/teach.html. Deck: course/show/e12.html.

## Title

Meridian E12: Contracts and policies that survive a rebuild

## Hook

A rebuild will try to drop the lock. The post-hook puts the lock back.
One owner per object. A contract fails before the wrong shape is published.

## Description

A rebuild will try to drop the lock. The post-hook puts the lock back.
One owner per object. A contract fails before the wrong shape is published.

The rules have to survive the next rebuild. Terraform owns roles, warehouses, the resource monitor, and databases. dbt owns marts, grants, tests, and contracts. Security owns row-access policies, masking policies, and the entitlement table. Human users belong to an identity provider, which is not in this repo. terraform validate needs no account. terraform plan is the picture you show. Do not also apply the SQL setup scripts onto the same objects. A contract on dim_branch fails the build before a renamed column lands. Unit tests for weekend FX and the fraud rules run on rows you wrote by hand. CREATE OR REPLACE drops a policy. The prod post-hook apply_governance puts it back. ACCESS_HISTORY is the audit, and account-usage data can lag by hours.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is E12 in the playlist, position 14 of 15. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- E3 platform objects and E11 policies.
- Terraform 1.6 or newer for validate. Plan needs Snowflake env vars and must not be mixed with scripts 01 and 02 on the same account.

Files covered
- 11_platform_terraform/main.tf
- 11_platform_terraform/variables.tf
- 04_dbt_meridian_dw/macros/governance.sql
- 04_dbt_meridian_dw/models/marts/core/_core__models.yml
- 04_dbt_meridian_dw/models/marts/cards/_cards__unit_tests.yml
- 04_dbt_meridian_dw/models/staging/postgres/_postgres__unit_tests.yml
- 04_dbt_meridian_dw/models/intermediate/_intermediate__unit_tests.yml
- 00_architecture/adr/0008-one-owner-per-object-type.md
- 00_architecture/adr/0010-contracts-at-public-boundaries.md

Chapters
00:00 One owner per object
10:00 Terraform plan
20:00 A contract that fails the build
30:00 The policy survives a rebuild
38:00 Access history

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

An empty terraform plan, a contract error, or an ACCESS_HISTORY row is live only when it is on the screen you just produced. Do not invent a drift count.

Watch in this order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

#Terraform #DataEngineering #DataGovernance #dbt #Snowflake

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- E3 platform objects and E11 policies.
- Terraform 1.6 or newer for validate. Plan needs Snowflake env vars and must not be mixed with scripts 01 and 02 on the same account.

## Files covered

- `11_platform_terraform/main.tf`
- `11_platform_terraform/variables.tf`
- `04_dbt_meridian_dw/macros/governance.sql`
- `04_dbt_meridian_dw/models/marts/core/_core__models.yml`
- `04_dbt_meridian_dw/models/marts/cards/_cards__unit_tests.yml`
- `04_dbt_meridian_dw/models/staging/postgres/_postgres__unit_tests.yml`
- `04_dbt_meridian_dw/models/intermediate/_intermediate__unit_tests.yml`
- `00_architecture/adr/0008-one-owner-per-object-type.md`
- `00_architecture/adr/0010-contracts-at-public-boundaries.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 45-minute cut, not to a finished timeline.

```
00:00 One owner per object
10:00 Terraform plan
20:00 A contract that fails the build
30:00 The policy survives a rebuild
38:00 Access history
```

## Hashtags

#Terraform #DataEngineering #DataGovernance #dbt #Snowflake

## Tags

Terraform, Snowflake, dbt contracts, data governance, row access policy, unit tests, access history, data engineering, analytics engineering, platform engineering, Meridian Bank, tutorial

## Pinned comment

Break the dim_branch contract on purpose, read the dbt error, then put the column name back.

Who owns the row-access policy, and who is only allowed to attach it?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

E12 is up: one owner per object, a contract that can fail the build, and a policy that survives CREATE OR REPLACE. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E13 — Say it in two minutes. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E13), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e12-rules-survive.mp4

## Thumbnail

- File: `thumbnails/E12.png`
- Badge: EPISODE 12
- On-image hook: Rules that survive
- Tech: Terraform

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 PNG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] terraform plan output is read from the terminal, not from memory.
- [ ] SQL setup and Terraform are not both applied to the same objects in the demo.

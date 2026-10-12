# E10 — Cards: score, then offer

Status: not published yet.
Planned length: 40 minutes. Playlist position: 12 of 15.
Grounding: course/show.html episode E10 (40 min, 15 scenes: four models, a 0.70 holdout gate, scores as data, next best offer) and Module 10 in course/teach.html. Deck: course/show/e10.html.

## Title

Score Credit Cards with Python ML | scikit-learn on Snowflake | Episode 10

## Hook

The model scores. The SQL policy decides. Below 0.70, the new scores do not ship.
Fraud labels in this course are injected, and they are never a feature.

## Description

The model scores. The SQL policy decides. Below 0.70, the new scores do not ship.
Fraud labels in this course are injected, and they are never a feature.

Cards add a second set of processes on the same customers. There is no bureau file and no regulatory scorecard. The approve or reject label is a published policy plus noise. The model has to recover that policy. Four paths: card_decision_v1 on a 60-day holdout, card_propensity_v1 with a 20 percent holdout, fraud rules plus card_fraud_v1 on a 14-day holdout, and a marketplace-lift report that is not a model. MERIDIAN_AUC_GATE defaults to 0.70. A run below the gate is stored as REJECTED and its scores are not published. fraud_label is injected so recall can be measured. It is excluded from features. Scores land in MERIDIAN_RAW.ML and never return to PostgreSQL. fct_next_best_offer is one offer per customer, or no row. A blocked card or a rule-suspect authorization in 30 days suppresses the offer. --dry-run trains and prints, and writes nothing.

Meridian Bank is fictional: 520 branches (India 300, UAE 60, UK 60, United States 60, Singapore 40), currencies INR, AED, GBP, USD and SGD, and group figures in USD. The course seed is 200,000 customers and 5 million payments. This is Episode 10, video 12 of 15 in the playlist. It is not a production bank.

Student repository
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Prerequisites
- Gold marts from Episode 6 and the scheduler from Episode 7.
- Say, on camera, that labels are a policy plus noise and that fraud was injected.
- Prefer --dry-run when you only need the printout.

Files covered
- 09_decisioning_python/train_and_score.py
- 04_dbt_meridian_dw/macros/card_policy.sql
- 04_dbt_meridian_dw/models/marts/cards/ml_customer_features.sql
- 04_dbt_meridian_dw/models/marts/cards/fct_card_applications.sql
- 04_dbt_meridian_dw/models/marts/cards/fct_card_authorizations.sql
- 04_dbt_meridian_dw/models/marts/cards/fct_card_fraud_alerts.sql
- 04_dbt_meridian_dw/models/marts/cards/fct_next_best_offer.sql
- 04_dbt_meridian_dw/models/staging/ml/stg_ml__model_scores.sql
- 04_dbt_meridian_dw/tests/assert_fraud_rules_catch_injected_patterns.sql
- 04_dbt_meridian_dw/tests/assert_offers_skip_recent_fraud.sql
- tests/test_training.py
- 05_airflow/dags/meridian_card_decisioning.py
- 00_architecture/adr/0005-model-scores-land-in-the-warehouse.md

Chapters
00:00 Policy versus model
08:00 Four models
16:00 The 0.70 holdout gate
26:00 Scores land in the warehouse
33:00 The next best offer

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

Do not read a holdout AUC, a lift, or a contact-list count aloud unless it is on the run you just executed. The 0.70 figure is the gate in configuration, not a measured score.

Watch in order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4, Episode 5, Episode 6, Episode 7, Episode 8, Episode 9, Episode 10, Episode 11, Episode 12, Episode 13.

#MachineLearning #DataEngineering #scikitlearn #FraudDetection #dbt

## Student repository

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Prerequisites

- Gold marts from Episode 6 and the scheduler from Episode 7.
- Say, on camera, that labels are a policy plus noise and that fraud was injected.
- Prefer --dry-run when you only need the printout.

## Files covered

- `09_decisioning_python/train_and_score.py`
- `04_dbt_meridian_dw/macros/card_policy.sql`
- `04_dbt_meridian_dw/models/marts/cards/ml_customer_features.sql`
- `04_dbt_meridian_dw/models/marts/cards/fct_card_applications.sql`
- `04_dbt_meridian_dw/models/marts/cards/fct_card_authorizations.sql`
- `04_dbt_meridian_dw/models/marts/cards/fct_card_fraud_alerts.sql`
- `04_dbt_meridian_dw/models/marts/cards/fct_next_best_offer.sql`
- `04_dbt_meridian_dw/models/staging/ml/stg_ml__model_scores.sql`
- `04_dbt_meridian_dw/tests/assert_fraud_rules_catch_injected_patterns.sql`
- `04_dbt_meridian_dw/tests/assert_offers_skip_recent_fraud.sql`
- `tests/test_training.py`
- `05_airflow/dags/meridian_card_decisioning.py`
- `00_architecture/adr/0005-model-scores-land-in-the-warehouse.md`

## Chapters

Adjust these timestamps after the final edit. They are drafted to the planned 40-minute cut, not to a finished timeline.

```
00:00 Policy versus model
08:00 Four models
16:00 The 0.70 holdout gate
26:00 Scores land in the warehouse
33:00 The next best offer
```

## Hashtags

#MachineLearning #DataEngineering #scikitlearn #FraudDetection #dbt

## Tags

machine learning, scikit-learn, data engineering, fraud rules, AUC, feature leakage, credit card analytics, dbt, Snowflake, next best offer, Meridian Bank, tutorial

## Pinned comment

Open train_and_score.py and find the gate that rejects a run below 0.70.

Why must fraud_label stay out of the feature list?

Student repository: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Community post

Episode 10 is up: score the card, then let the policy decide. Below 0.70, the new scores stay unpublished. Code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Cards and end screen

Card: after the first chapter change, link the next upload, E11 — Ask in English. Paste that video URL once YouTube has assigned it.
End screen, final 20 seconds: next video (E11), this playlist, and Subscribe.
Do not attach a card to a private account, a key, or an unlisted secret. The GitHub URL stays in the description and the pinned comment. A website card is available only after the channel has a verified associated site.

## Upload settings

- Category: Education
- Language: English
- License: Standard YouTube License
- Audience: Not made for kids
- Visibility: Unlisted on upload. Public after this video is in the playlist at its canonical position.

## Filename

meridian-e10-score-then-offer.mp4

## Thumbnail

- File: `thumbnails/E10.jpg`
- Red corner tag: EPISODE 10
- Headline: SCORE CREDIT CARDS WITH PYTHON ML
- Handwritten line: scikit-learn on Snowflake data

## Pre-publish checks

- [ ] Title is 100 characters or fewer and matches this pack.
- [ ] Thumbnail is the 1280x720 JPG named below and is under 2MB.
- [ ] First chapter is 00:00. Move every later timestamp to match the final edit before you publish.
- [ ] No account locator, password, private key, or .env value is on screen or in the text.
- [ ] Meridian is described as a fictional bank. No production users are claimed.
- [ ] The student repository URL in the description matches the pinned comment.
- [ ] Upload as Unlisted. Switch to Public only after the video is in the playlist at this position.
- [ ] Cards and the end screen point at videos in this playlist.
- [ ] No AUC or offer count is quoted unless it was just printed by the script.
- [ ] Injected fraud and the policy-plus-noise label are said before any model claim.

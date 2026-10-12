# Meridian YouTube kit

Instructor-only upload sheets for the 15 Meridian releases. This folder stays in the instructor tree. `tools/sync_student_repo.py` copies an allowlist (`PUBLIC_DIRECTORIES` and `ARCHITECTURE_PATHS`) and does not include `youtube/`.

Student code, which every description and pinned comment already names:

https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

## Canonical order

E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13.

That is the order in `course/show.html`. Planned length is 610 minutes. P0 is the Python primer and sits after Snowflake setup and before the extractor. Its thumbnail badge is `PYTHON PRIMER`. Every other badge is `EPISODE` plus the episode number, so Episode 1 reads `EPISODE 1`.

## Playlist

Create one playlist before you make anything public.

| Setting | Value |
| --- | --- |
| Title | Meridian: from a live bank to an answer in English |
| Visibility | Public when the first public video is added. Until then, leave the videos Unlisted. |
| Ordering | Manual. Drag into the canonical order. Date-added order will put a later upload first. |
| Language | English |

Playlist description, from `catalog.json`:

```
Meridian is a fictional bank. This playlist builds one analytics platform in order: the problem, the PostgreSQL source, the star schema, Snowflake, a Python primer, watermark ingestion, dbt, Airflow, performance, quality, card decisioning, English questions with row policies, governance as code, and a two-minute defence.

Student code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Order: E0, E1, E2, E3, P0, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13. 610 planned minutes.

Snowflake numbers in the lessons are expected results from the repository until you run them on your own trial and read them back. Meridian has no production users.
```

## What is in each release folder

`E0/UPLOAD_PACK.md` through `E13/UPLOAD_PACK.md`, plus `P0/UPLOAD_PACK.md`, each contain:

- a title of 100 characters or fewer
- a two-line hook
- the full YouTube description, including the student repository, prerequisites, files, and chapters
- comma-separated tags of 500 characters or fewer
- hashtags, pinned comment, and community post
- cards and end-screen plan
- category, language, license, audience, and visibility
- the upload filename and thumbnail copy
- pre-publish checks

Copy the description from the Description section only. The rest of the pack is the instructor checklist.

## Thumbnails

`thumbnails/source.json` is the editable picture data: badge, 2–5 word hook, tech line, accent, and motif. `thumbnails/<ID>.png` is the 1280×720 file you upload. `thumbnails/contact-sheet.png` shows the whole series together for a consistency review. The drawings use local system fonts and generated geometry. There is no photo, no face, and no account identifier.

After a copy or colour change:

```bash
python3 build_thumbnails.py
```

Keep the same badge, hook, and tech in `catalog.json`. The checker fails if the two files disagree. Episode 1 must keep the badge `EPISODE 1`.

## Upload one release

1. Finish the cut. Open that release's `UPLOAD_PACK.md`.
2. Move the chapter times onto the final timeline. The first chapter stays `00:00`. The printed times are a draft for the planned length, not a finished edit.
3. Put the new times in `catalog.json`, then refresh the pack:

```bash
python3 check_youtube_pack.py --write-packs
python3 check_youtube_pack.py
python3 -m pytest -q test_youtube_pack.py
```

4. Export 16:9 at the recording frame rate, with readable 1080p-or-better text and no copyrighted music or artwork you do not own.
5. Upload the file named in the pack. Visibility: **Unlisted**. Category: **Education**. Language: **English**. License: **Standard YouTube License**. Audience: **Not made for kids**. Paid promotion: **No**, unless that fact changes.
6. Paste the title, the Description section, and the tags. Upload `thumbnails/<ID>.png`.
7. Review automatic captions from start to finish. Correct tool names, SQL, dbt, Snowflake, PostgreSQL, Airflow, names, and numbers; upload a corrected subtitle file if the automatic track is not reliable.
8. Add the video to the playlist and drag it to its canonical slot.
9. After the next video has a URL, add the card and the end screen from the pack. E13 has no next episode.
10. Test the description link, card, end screen, chapter jumps, subtitles, thumbnail crop, and audio on both desktop and phone.
11. Publish the community post, then pin the comment.
12. Switch the video to **Public** only after the playlist position is correct.

Run the commands from this `youtube/` directory. `build_thumbnails.py` and `check_youtube_pack.py` need Python's standard library and Pillow. They do not use the network.

## What you may say about Snowflake

A number is a live result only after you run the statement and read it back. Until then, say what the file expects.

- E3: fixture id 101 is not a live warehouse count. The resource monitor's 100 credits is a limit in the script. Streams, tasks, and dynamic tables are a demo, not the working path. The bronze shelves are empty on purpose.
- E8: the 3-version join is the lab file's example, not a live total. Quote bytes, spill, or duration only from the measure query on screen.
- E9: there is no counted orphan total on the slide. The one-cent reconciliation line is the offline test's expectation.
- E10: 0.70 is the configured gate, not a measured AUC. Fraud labels are injected. `--dry-run` writes nothing.
- E11: the four personas are the rule in the policy, not a counted run. If the region has no Cortex, use `analyses/card_questions.sql`.
- E13: customer-health precision 1.0 and recall 0.5 are the offline synthetic case, not a live customer. The 20-minute figure is the task timeout in code, not a measured wait.

## Where the words came from

Every release follows its cinematic deck in `course/show/`, the canonical order and duration in `course/show.html`, and the corresponding instructor notes in `course/teach.html`. Each pack names that grounding. File lists match the episode entries in `study/coverage.json`.

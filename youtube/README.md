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
| Title | End-to-End Data Engineering Project \| PostgreSQL, Snowflake, dbt, Airflow |
| Visibility | Public when the first public video is added. Until then, leave the videos Unlisted. |
| Ordering | Manual. Drag into the canonical order. Date-added order will put a later upload first. |
| Language | English |

Playlist description, from `catalog.json`:

```
Meridian is a fictional bank. This playlist builds one analytics platform in order: the problem, the PostgreSQL source, the star schema, Snowflake, a Python primer, watermark ingestion, dbt, Airflow, performance, quality, card decisioning, English questions with row policies, governance as code, and a two-minute defence.

Student code: https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK

Order: Intro, Episode 1, Episode 2, Episode 3, Python Primer, Episode 4 to Episode 13. 610 planned minutes.

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

Every thumbnail uses the design of the two published videos: light background, Fakhruddin on the right, four logo circles, a two-line condensed headline with one blue phrase, a handwritten line underneath and a red corner tag (`INTRO VIDEO`, `EPISODE N`, or `PYTHON PRIMER`).

- `thumbnails/<ID>.jpg` is the 1280×720 file you upload. `thumbnails/contact-sheet.jpg` shows the whole series together.
- E0 (the intro) and E1 are already on YouTube. Their files are byte-for-byte copies of `thumbnails/assets/intro.jpg` and `thumbnails/assets/episode-1.jpg`. Never redraw them.
- Every other thumbnail is drawn by headless Chrome over `thumbnails/assets/plate.jpg`, which is the intro photo with its text removed, so the face is identical in every episode. Fonts are Anton and Gochi Hand (open font licence, in `thumbnails/assets/fonts/`). Logos come from `course/show/deck/logos.js`.
- `thumbnails/source.json` holds the words and logos: `tag`, `line1`, `blue`, `rest`, `sub`, `logos`.

After a wording or logo change:

```bash
python3 build_thumbnails.py          # or: python3 build_thumbnails.py E5
```

Keep the tag, headline and handwritten line in `catalog.json` identical to `source.json`. The checker fails if they disagree.

## Published releases

E0 and E1 have `"published": true` in `catalog.json`. Their title, description and tags are exactly what is live on YouTube, so do not rewrite them. When you publish another release, paste the final text into its catalog entry, set `"published": true`, add `published_url`, and refresh the packs.

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
6. Paste the title, the Description section, and the tags. Upload `thumbnails/<ID>.jpg`.
7. Review automatic captions from start to finish. Correct tool names, SQL, dbt, Snowflake, PostgreSQL, Airflow, names, and numbers; upload a corrected subtitle file if the automatic track is not reliable.
8. Add the video to the playlist and drag it to its canonical slot.
9. After the next video has a URL, add the card and the end screen from the pack. E13 has no next episode.
10. Test the description link, card, end screen, chapter jumps, subtitles, thumbnail crop, and audio on both desktop and phone.
11. Publish the community post, then pin the comment.
12. Switch the video to **Public** only after the playlist position is correct.

Run the commands from this `youtube/` directory. `check_youtube_pack.py` needs Python's standard library and Pillow. `build_thumbnails.py` also needs Google Chrome or Chromium. Neither uses the network.

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

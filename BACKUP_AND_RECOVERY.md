# Meridian course backup and recovery

The course has two Git repositories and one deliberately separate media backup.

## What Git protects

Private instructor and publishing source:

```text
https://github.com/fkhambaty/commandcenter
└── DataEngineeringAndAnalyticsByFK/
    ├── course/       cinematic decks and instructor guide
    ├── youtube/      private thumbnails and upload packs
    ├── study/        source of the public study guide
    ├── tools/        release QA and student sync
    └── runnable project source
```

Public student project:

```text
https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK
```

The student repository contains the runnable, sanitized project and study guide.
It does not contain instructor notes, YouTube publishing files, interview records,
credentials, raw recordings, or the nested repository's `.git` directory.

## What Git does not protect

`Videos/` is excluded because the raw recordings are large. Copy the complete
`DataEngineeringAndAnalyticsByFK/Videos/` folder to an external SSD or a private
cloud-storage folder before giving up this laptop. Open at least one copied video
from the backup destination before considering that backup complete.

Example for a mounted external drive (replace the destination):

```bash
rsync -avh --progress Videos/ "/Volumes/COURSE_BACKUP/Meridian/Videos/"
diff -rq Videos/ "/Volumes/COURSE_BACKUP/Meridian/Videos/"
```

`diff -rq` must print nothing. Also compare the folder sizes:

```bash
du -sh Videos/ "/Volumes/COURSE_BACKUP/Meridian/Videos/"
```

Secrets and machine-local output are also excluded: `.env`, private keys, dbt
`profiles.yml`, Airflow `include/` and local settings, virtual environments,
Terraform state, dbt artifacts, caches, and `Printouts/`.

## Restore on another computer

```bash
git clone https://github.com/fkhambaty/commandcenter.git
cd commandcenter/DataEngineeringAndAnalyticsByFK

git clone https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK.git \
  snowflake_dbt_airflow_python_byFK
```

Then:

1. Open `README.md`.
2. Open `study/index.html` before the videos.
3. Open `course/teach.html` for instructor preparation.
4. Open `course/show.html` for the recording deck.
5. Read `youtube/README.md` when publishing.
6. Recreate `.env` from `.env.example`; never copy credentials from Git.
7. Restore the separately backed-up `Videos/` folder if raw recordings are needed.

## Verify a restored copy

```bash
python3 -m pytest -q tests
python3 -m tools.course_qa
python3 tools/sync_student_repo.py --check
python3 youtube/check_youtube_pack.py
```

The sync check should report no differences after both repositories have been
restored at the expected nested path. A nonzero result means the private source
and public student copy differ; inspect the plan before using `--apply`.

## Save future course changes

First update and verify the nested student repository, then commit it there.
Afterward, commit the private course source in `commandcenter` with explicit
paths. Never use `git add -A` at the command-center root because unrelated career
work may be present.

Before every push, confirm that no `.env`, private key, `profiles.yml`, Airflow
local file, Terraform state, raw video, or nested `.git` path is staged.

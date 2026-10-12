# Course release QA

Offline checks read the episode catalog in `course/show.html` and the deck
files it names. Screenshot capture is a separate command. It needs Chrome on
the machine and does not run under pytest.

The tools find the repository by walking upward from this package until
`course/show.html` exists. A home directory is not hardcoded.

## Offline gate

From the repository root:

```bash
python3 -m tools.course_qa
python3 tools/course_qa/check.py
```

The command exits 0 when every catalog deck passes, and 1 when it reports
findings. `--json` prints the same findings as JSON. `--root` points at a
checkout when you are not running inside one.

What it checks:

- The `scenes` count in the catalog equals the number of `<section class="s">`
  slides. Sections inside `<script>`, `<style>`, and comments are not counted.
- `data-episode` matches the catalog id when the deck sets it.
- Repo paths cited in a deck exist. A numbered prefix such as
  `00_architecture/adr/0001` or `03_snowflake/01` matches the file that starts
  with that id. Paths under `models/`, `macros/`, `analyses/`, `snapshots/`,
  and `seeds/` are resolved in the directory that contains `dbt_project.yml`.
- A cited `*.sql`, `*.py`, `*.md`, or other file that is not on disk is a
  missing student file. A path whose name is `.env` is accepted when the
  repository contains `.env.example`, because the student copies that file
  locally and it is not committed.
- Local `href` and `src` values resolve inside the repository. Fragment links
  (`#slide`) and `http`, `https`, `mailto`, and `data` URLs are not fetched.
- Decks and the player page must not contain a local home path (`/Users/`,
  `/home/`, or a Windows profile path), a PEM private key, a Snowflake
  org-account locator, or the checkout folder name when that name is not the
  public repository `snowflake_dbt_airflow_python_byFK`. The documented
  placeholder `xy12345.ap-south-1` is allowed.

The instructor plan `course/teach.html` is not a catalog deck, so this gate
does not read it.

```bash
pytest -q tests/test_course_release.py
```

That test is offline. It does not start Chrome, Snowflake, Docker, dbt, or a
network service.

## Screenshots

```bash
python3 -m tools.course_qa shoot
python3 tools/course_qa/shoot.py --deck e0
python3 tools/course_qa/shoot.py --list
```

`--list` prints every final-step hash and does not launch Chrome. A frame hash
is the 1-based slide, plus the final `data-steps` value when the slide has
one: `#4` or `#4.3`.

The capture opens each slide in headless Chrome at 1600x900, waits for the
final step to settle (4 seconds, or 4.5 seconds when the slide has steps),
and writes a PNG. Override the pause with `--wait-ms`. `--max-slides 1` shoots
only the first slide of each selected deck. `--deck` may be repeated.

Chrome is discovered from `CHROME_PATH`, the usual macOS application path, or
`google-chrome` / `chromium` on `PATH`. The debugger profile is a temporary
directory and is deleted when the command finishes.

After each PNG, the page runs a layout check: document scroll larger than the
viewport, and elements in the active slide that extend outside the 1600x900
stage. Orbit decorations, fixed chrome, and the ambient canvas are ignored.
A size other than 1600x900, a layout overflow, or a console exception makes
the command exit 1. The per-frame report is `tools/course_qa/out/layout.json`.

PNGs land in `tools/course_qa/out/<deck-id>/`. When Pillow is installed, contact
sheets of up to six slides (two columns, each cell 800x450) are written to
`tools/course_qa/out/sheets/`. Without Pillow the PNGs are still written and
the sheets are skipped. `--no-sheets` skips them even when Pillow is present.
The `out/` directory is gitignored.

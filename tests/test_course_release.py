"""Offline release gate for the course decks. Does not launch Chrome."""

from __future__ import annotations

import json
import re
import socket
import struct
import sys
import threading
from pathlib import Path

import pytest

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[misc, assignment]

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.course_qa.catalog import final_hashes, parse_catalog, slide_steps
from tools.course_qa.checks import main as check_main
from tools.course_qa.checks import run_checks
from tools.course_qa.paths import repo_root
from tools.course_qa.screenshots import (
    Debugger,
    encode_client_frame,
    encode_server_frame,
    frame_sort_key,
    main as shoot_main,
    plan_frames,
    png_size,
    websocket_accept,
    write_contact_sheets,
)
from tools.sync_student_repo import PUBLIC_DIRECTORIES, is_excluded


def _recvn(sock: socket.socket, size: int) -> bytes:
    blob = b""
    while len(blob) < size:
        chunk = sock.recv(size - len(blob))
        if not chunk:
            raise ConnectionError("socket closed")
        blob += chunk
    return blob


def _build_repo(tmp_path: Path) -> Path:
    (tmp_path / "course" / "show" / "deck").mkdir(parents=True)
    (tmp_path / "course" / "show" / "deck" / "deck.css").write_text("body{}\n", encoding="utf-8")
    for page in ("opening.html", "pictures.html", "code.html"):
        (tmp_path / "course" / "show" / page).write_text("<!doctype html><title>Course</title>\n", encoding="utf-8")
    (tmp_path / ".env.example").write_text("SNOWFLAKE_ACCOUNT=xy12345.ap-south-1\n", encoding="utf-8")
    (tmp_path / "01_source_postgres").mkdir()
    (tmp_path / "01_source_postgres" / "04_cdc_triggers.sql").write_text("select 1;\n", encoding="utf-8")
    (tmp_path / "00_architecture" / "adr").mkdir(parents=True)
    (tmp_path / "00_architecture" / "adr" / "0001-watermark.md").write_text("# adr\n", encoding="utf-8")
    (tmp_path / "03_snowflake").mkdir()
    (tmp_path / "03_snowflake" / "01_account_setup_rbac.sql").write_text("select 1;\n", encoding="utf-8")
    (tmp_path / "05_airflow").mkdir()
    dbt = tmp_path / "04_dbt_meridian_dw"
    (dbt / "models" / "staging").mkdir(parents=True)
    (dbt / "dbt_project.yml").write_text("name: meridian\n", encoding="utf-8")
    (dbt / "models" / "staging" / "stg_postgres__transactions.sql").write_text("select 1;\n", encoding="utf-8")
    return tmp_path


def _catalog(repo: Path, deck_id: str = "e0", scenes: int = 2) -> None:
    text = (
        "const EPISODES = [\n"
        f'{{id:"{deck_id}",code:"E0",title:"Title",mins:"1 min",color:"#fff",'
        f'deck:"show/{deck_id}.html",scenes:{scenes},desc:"A deck."}}\n'
        "];\n"
    )
    (repo / "course" / "show.html").write_text(text, encoding="utf-8")


def _deck(repo: Path, deck_id: str = "e0", extra: str = "", scenes_steps: tuple[int, ...] = (0, 3)) -> None:
    slides = []
    for steps in scenes_steps:
        attr = f' data-steps="{steps}"' if steps else ""
        slides.append(f'<section class="s"{attr}><p>01_source_postgres/04_cdc_triggers.sql</p></section>')
    html = (
        "<!doctype html><html><head><link rel=\"stylesheet\" href=\"deck/deck.css\"></head>"
        f'<body data-episode="{deck_id}">'
        + "".join(slides)
        + extra
        + "<script>var hidden = '<section class=\"s\"></section>';</script>"
        "</body></html>"
    )
    (repo / "course" / "show" / f"{deck_id}.html").write_text(html, encoding="utf-8")


def _codes(repo: Path) -> list[str]:
    return [item.code for item in run_checks(repo)]


def test_repo_root_walks_to_the_checkout():
    root = repo_root()
    assert (root / "course" / "show.html").is_file()
    assert repo_root(root / "tools" / "course_qa" / "paths.py") == root


def test_clean_fixture_passes(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo)
    _deck(
        repo,
        extra=(
            "<p>00_architecture/adr/0001</p>"
            "<p>03_snowflake/01 and 02</p>"
            "<p>models/staging/stg_postgres__transactions.sql</p>"
            "<h3>05_airflow/.env</h3>"
            '<span data-val="xy12345.ap-south-1"></span>'
            '<a href="../../00_architecture/adr/0001-watermark.md">adr</a>'
            '<a href="https://example.com/docs">docs</a>'
            '<mpath href="#wire"></mpath>'
        ),
    )
    assert run_checks(repo) == []


def test_section_count_must_match_the_catalog(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=9)
    _deck(repo)
    findings = run_checks(repo)
    assert [item.code for item in findings] == ["section-count"]
    assert "scenes=9" in findings[0].detail
    assert "2 section.s" in findings[0].detail


def test_sections_inside_script_are_not_slides():
    html = '<section class="s"></section><script><section class="s"></section></script>'
    assert slide_steps(html) == [0]
    assert final_hashes('<section class="s" data-steps="4"></section><section class="s bal"></section>') == ["1.4", "2"]


def test_missing_student_file_and_project_prefix(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=1)
    _deck(repo, scenes_steps=(0,), extra="<code>01_source_postgres/not_in_the_repo.sql</code><p>00_architecture/adr/9999</p>")
    assert _codes(repo) == ["missing-student-file", "missing-project-path"]


def test_env_without_example_is_a_missing_student_file(tmp_path: Path):
    repo = _build_repo(tmp_path)
    (repo / ".env.example").unlink()
    _catalog(repo, scenes=1)
    _deck(repo, scenes_steps=(0,), extra="<h3>05_airflow/.env</h3>")
    assert "missing-student-file" in _codes(repo)


def test_forbidden_home_account_key_and_checkout_name(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=1)
    _deck(
        repo,
        scenes_steps=(0,),
        extra=(
            "<p>/Users/someone/private.txt</p>"
            "<p>ABCDEF-GH12345</p>"
            "<p>-----BEGIN PRIVATE KEY-----</p>"
            f"<p>{repo.name}</p>"
        ),
    )
    findings = run_checks(repo)
    assert findings
    assert {item.code for item in findings} == {"forbidden-identity"}
    detail = " ".join(item.detail for item in findings)
    assert "/Users/someone/private.txt" in detail
    assert "ABCDEF-GH12345" in detail
    assert "private key" in detail
    assert repo.name in detail


def test_placeholder_account_is_allowed(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=1)
    _deck(repo, scenes_steps=(0,), extra="<span>SNOWFLAKE_ACCOUNT=xy12345.ap-south-1</span>")
    assert run_checks(repo) == []


def test_broken_and_escaping_html_links(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=1)
    _deck(
        repo,
        scenes_steps=(0,),
        extra='<img src="deck/missing.png"><a href="../../../../../../etc/passwd">x</a>',
    )
    details = [item.detail for item in run_checks(repo) if item.code == "html-link"]
    assert any("missing.png" in detail for detail in details)
    assert any("escapes" in detail for detail in details)


def test_missing_deck_and_bad_catalog(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo)
    findings = run_checks(repo)
    assert findings[0].code == "missing-deck"
    (repo / "course" / "show.html").write_text("<html></html>", encoding="utf-8")
    assert run_checks(repo)[0].code == "catalog"


def test_episode_id_must_match_when_declared(tmp_path: Path):
    repo = _build_repo(tmp_path)
    _catalog(repo, scenes=1)
    _deck(repo, scenes_steps=(0,))
    html_path = repo / "course" / "show" / "e0.html"
    html_path.write_text(html_path.read_text(encoding="utf-8").replace('data-episode="e0"', 'data-episode="e9"'), encoding="utf-8")
    assert "episode-id" in _codes(repo)


def test_check_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    repo = _build_repo(tmp_path)
    _catalog(repo)
    _deck(repo)
    assert check_main(["--root", str(repo)]) == 0
    assert "0 findings" in capsys.readouterr().out
    _catalog(repo, scenes=4)
    assert check_main(["--root", str(repo), "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["code"] == "section-count"


def test_shot_plan_lists_final_steps_without_chrome(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    repo = _build_repo(tmp_path)
    _catalog(repo)
    _deck(repo)
    frames = plan_frames(repo)
    assert [frame.slide_hash for frame in frames] == ["1", "2.3"]
    assert shoot_main(["--root", str(repo), "--list"]) == 0
    printed = capsys.readouterr().out
    assert "e0 #2.3" in printed
    assert "2 frames" in printed


def test_png_size_and_frame_order():
    blob = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0d" + b"IHDR" + struct.pack(">II", 1600, 900)
    assert png_size(blob) == (1600, 900)
    ordered = sorted(
        [Path("s10.2.png"), Path("s2.png"), Path("s2.4.png")],
        key=frame_sort_key,
    )
    assert [path.name for path in ordered] == ["s2.png", "s2.4.png", "s10.2.png"]


def test_client_frame_is_masked():
    frame = encode_client_frame('{"a":1}', mask=b"abcd")
    assert frame[0] == 0x81
    assert frame[1] & 0x80
    mask = frame[2:6]
    length = frame[1] & 0x7F
    payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(frame[6 : 6 + length]))
    assert payload == b'{"a":1}'
    assert encode_server_frame(b"hello") == b"\x81\x05hello"


def test_debugger_roundtrip_stays_on_localhost():
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    listener.settimeout(5)
    port = listener.getsockname()[1]

    def serve() -> None:
        conn, _addr = listener.accept()
        conn.settimeout(5)
        try:
            data = b""
            while b"\r\n\r\n" not in data:
                data += conn.recv(4096)
            key = ""
            for line in data.decode("latin1").split("\r\n"):
                if line.lower().startswith("sec-websocket-key:"):
                    key = line.split(":", 1)[1].strip()
            accept = websocket_accept(key)
            conn.sendall(
                (
                    "HTTP/1.1 101 Switching Protocols\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Accept: {accept}\r\n"
                    "\r\n"
                ).encode("ascii")
            )
            header = _recvn(conn, 2)
            length = header[1] & 0x7F
            mask = _recvn(conn, 4)
            payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(_recvn(conn, length)))
            message = json.loads(payload)
            reply = json.dumps({"id": message["id"], "result": {"ok": True}}).encode("utf-8")
            conn.sendall(encode_server_frame(reply))
            while conn.recv(1024):
                pass
        finally:
            conn.close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    debugger = Debugger.connect(f"ws://127.0.0.1:{port}/devtools/page/test", timeout=5)
    try:
        reply = debugger.call("Runtime.evaluate", {}, timeout=5)
    finally:
        debugger.close()
        listener.close()
    thread.join(5)
    assert reply["result"]["ok"] is True


def test_contact_sheet_when_pillow_is_installed(tmp_path: Path):
    if Image is None:
        pytest.skip("Pillow is not installed")

    images = []
    for name, color in (("s1.png", "navy"), ("s2.3.png", "teal")):
        path = tmp_path / name
        Image.new("RGB", (1600, 900), color).save(path)
        images.append(path)
    written = write_contact_sheets(images, tmp_path / "sheets", "e0")
    assert len(written) == 1
    with Image.open(written[0]) as sheet:
        assert sheet.size == (1600, 450)


def test_qa_sources_do_not_hardcode_a_local_identity():
    package = ROOT / "tools" / "course_qa"
    text = "\n".join(path.read_text(encoding="utf-8") for path in package.glob("*.py"))
    lowered = text.lower()
    assert "fakhruddinkhambaty" not in lowered
    assert "sjvoggd" not in lowered
    assert "mq92888" not in lowered
    assert "dataengineeringandanalyticsbyfk" not in lowered


def test_student_sync_excludes_private_release_assets():
    assert "course" not in PUBLIC_DIRECTORIES
    assert "youtube" not in PUBLIC_DIRECTORIES
    assert is_excluded(Path("tests/test_course_release.py"))
    assert not is_excluded(Path("tests/test_practical_labs.py"))


def test_study_coverage_resolves_to_public_files_and_anchors():
    coverage = json.loads((ROOT / "study" / "coverage.json").read_text(encoding="utf-8"))
    guide = (ROOT / coverage["guide"]).read_text(encoding="utf-8")
    anchors = set(re.findall(r'\bid=["\']([^"\']+)["\']', guide))
    assert coverage["order"] == [episode["id"] for episode in coverage["episodes"]]
    for episode in coverage["episodes"]:
        assert episode["anchor"] in anchors
        assert episode.get("planned_files", []) == []
        for topic in episode["topics"]:
            assert topic in anchors
        for relative in episode["files"]:
            assert (ROOT / relative).is_file(), relative
    lowered = guide.lower()
    assert "/users/" not in lowered
    assert "sjvoggd" not in lowered
    assert "driveone" not in lowered


def test_catalogued_decks_pass_release_checks():
    findings = run_checks(repo_root())
    assert findings == [], "\n".join(item.format() for item in findings)


def test_real_shot_plan_matches_slide_markup():
    root = repo_root()
    frames = plan_frames(root)
    decks = parse_catalog((root / "course" / "show.html").read_text(encoding="utf-8"))
    counted: dict[str, int] = {}
    for frame in frames:
        counted[frame.deck_id] = counted.get(frame.deck_id, 0) + 1
    for deck in decks:
        html = deck.html_path(root).read_text(encoding="utf-8")
        assert counted[deck.deck_id] == len(slide_steps(html))
        assert final_hashes(html)[0] == "1" or final_hashes(html)[0].startswith("1.")

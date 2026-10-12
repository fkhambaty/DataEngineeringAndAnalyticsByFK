"""Final-step 1600x900 screenshots of the catalog decks.

This is the deckshoot capture flow: headless Chrome, one fresh document per
slide, the hash set to that slide's last step, then a viewport PNG. Contact
sheets are written when Pillow is installed. A temporary Chrome profile is
used and removed; nothing is read from a shared debugger profile.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from tools.course_qa.catalog import CatalogError, declared_episode, final_hash, parse_catalog, slide_steps
from tools.course_qa.paths import repo_root

try:
    from PIL import Image
except ImportError:  # Pillow is optional; PNGs are still written without it.
    Image = None  # type: ignore[misc, assignment]

VIEW_W = 1600
VIEW_H = 900
CELL_W = 800
CELL_H = 450
SHEET_COLUMNS = 2
SHEET_SLOTS = 6
_WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

LAYOUT_JS = """
(() => {
  const tolerance = 8;
  const stage = document.getElementById("stage");
  const slide = document.querySelector("section.s.active") || document.querySelector("section.s");
  const doc = document.documentElement;
  const decorative = (el) => {
    for (let node = el; node && node !== slide; node = node.parentElement) {
      const cls = typeof node.className === "string" ? node.className : "";
      if (/(^|\\s)(orbit|sat|flowdot|bg)(\\s|$)/.test(cls)) return true;
      if (node.hasAttribute && node.hasAttribute("data-overflow-ok")) return true;
      if (node.id === "fx" || node.tagName === "CANVAS") return true;
      const pos = getComputedStyle(node).position;
      if (pos === "fixed") return true;
    }
    return false;
  };
  const offenders = [];
  if (stage && slide) {
    const box = stage.getBoundingClientRect();
    for (const el of slide.querySelectorAll("*")) {
      if (decorative(el)) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width < 1 || rect.height < 1) continue;
      const dx = Math.max(box.left - rect.left, rect.right - box.right, 0);
      const dy = Math.max(box.top - rect.top, rect.bottom - box.bottom, 0);
      if (dx > tolerance || dy > tolerance) {
        const cls = typeof el.className === "string" ? el.className : "";
        offenders.push({tag: el.tagName, cls: cls.slice(0, 80), dx: Math.round(dx), dy: Math.round(dy)});
        if (offenders.length >= 8) break;
      }
    }
  }
  return {
    scrollWidth: doc.scrollWidth,
    scrollHeight: doc.scrollHeight,
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    scrollOverflowX: doc.scrollWidth > window.innerWidth + tolerance,
    scrollOverflowY: doc.scrollHeight > window.innerHeight + tolerance,
    stageOverflows: offenders.length,
    offenders
  };
})()
"""


class ChromeNotFound(RuntimeError):
    """No Chrome executable was discovered."""


@dataclass(frozen=True)
class Frame:
    deck_id: str
    relpath: str
    html_path: Path
    slide_hash: str
    expect_episode: str | None
    expect_slides: int


def plan_frames(repo: Path, deck_ids: list[str] | None = None, max_slides: int = 0) -> list[Frame]:
    """Final-step frames for every catalog deck, or for ``deck_ids`` only."""
    repo = repo.resolve()
    show = (repo / "course" / "show.html").read_text(encoding="utf-8")
    decks = parse_catalog(show)
    wanted = set(deck_ids or [])
    if wanted:
        known = {deck.deck_id for deck in decks}
        missing = sorted(wanted - known)
        if missing:
            raise CatalogError("unknown deck id: " + ", ".join(missing))
    frames: list[Frame] = []
    for deck in decks:
        if wanted and deck.deck_id not in wanted:
            continue
        html_path = deck.html_path(repo)
        html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
        steps = slide_steps(html)
        episode = declared_episode(html)
        hashes = [final_hash(index, count) for index, count in enumerate(steps, start=1)]
        if max_slides > 0:
            hashes = hashes[:max_slides]
        for slide_hash in hashes:
            frames.append(
                Frame(
                    deck_id=deck.deck_id,
                    relpath=deck.relpath,
                    html_path=html_path,
                    slide_hash=slide_hash,
                    expect_episode=episode,
                    expect_slides=len(steps),
                )
            )
    return frames


def find_chrome() -> str | None:
    """Return a Chrome executable, honouring ``CHROME_PATH`` when it points at a file."""
    override = os.environ.get("CHROME_PATH")
    if override and Path(override).is_file():
        return override
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate
    for command in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(command)
        if found:
            return found
    for folder in (os.environ.get("PROGRAMFILES", ""), os.environ.get("LOCALAPPDATA", "")):
        if not folder:
            continue
        windows = Path(folder) / "Google" / "Chrome" / "Application" / "chrome.exe"
        if windows.is_file():
            return str(windows)
    return None


def png_size(data: bytes) -> tuple[int, int]:
    """Read width and height from a PNG IHDR chunk."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("screenshot is not a PNG")
    return struct.unpack(">II", data[16:24])


def frame_sort_key(path: Path) -> tuple[int, int]:
    match = re.search(r"s(\d+)(?:\.(\d+))?", path.name)
    if match is None:
        return (10**9, 0)
    return (int(match.group(1)), int(match.group(2) or 0))


def write_contact_sheets(images: list[Path], dest: Path, deck_id: str) -> list[Path]:
    """Pack up to six 800x450 cells per sheet. Returns [] when Pillow is absent."""
    if Image is None or not images:
        return []
    dest.mkdir(parents=True, exist_ok=True)
    ordered = sorted(images, key=frame_sort_key)
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
    written: list[Path] = []
    for part, start in enumerate(range(0, len(ordered), SHEET_SLOTS), start=1):
        chunk = ordered[start : start + SHEET_SLOTS]
        rows = (len(chunk) + SHEET_COLUMNS - 1) // SHEET_COLUMNS
        sheet = Image.new("RGB", (CELL_W * SHEET_COLUMNS, CELL_H * rows), "black")
        for index, image_path in enumerate(chunk):
            with Image.open(image_path) as image:
                cell = image.convert("RGB").resize((CELL_W, CELL_H), resample)
            sheet.paste(cell, ((index % SHEET_COLUMNS) * CELL_W, (index // SHEET_COLUMNS) * CELL_H))
        out = dest / f"sheet_{deck_id}_{part}.png"
        sheet.save(out)
        written.append(out)
    return written


def websocket_accept(key: str) -> str:
    digest = hashlib.sha1((key + _WS_GUID).encode("ascii")).digest()
    return base64.b64encode(digest).decode("ascii")


def encode_client_frame(text: str | bytes, mask: bytes | None = None, opcode: int = 0x1) -> bytes:
    """Mask a client frame. opcode 0x1 is text and 0xA is pong."""
    payload = text.encode("utf-8") if isinstance(text, str) else text
    mask = mask if mask is not None else os.urandom(4)
    if len(mask) != 4:
        raise ValueError("websocket mask must be 4 bytes")
    masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
    header = bytearray([0x80 | opcode])
    length = len(payload)
    if length < 126:
        header.append(0x80 | length)
    elif length < 65536:
        header.append(0x80 | 126)
        header += struct.pack("!H", length)
    else:
        header.append(0x80 | 127)
        header += struct.pack("!Q", length)
    return bytes(header) + mask + masked


def encode_server_frame(payload: bytes, opcode: int = 0x1) -> bytes:
    """Unmasked frame, used by tests and by Chrome."""
    header = bytearray([0x80 | opcode])
    length = len(payload)
    if length < 126:
        header.append(length)
    elif length < 65536:
        header.append(126)
        header += struct.pack("!H", length)
    else:
        header.append(127)
        header += struct.pack("!Q", length)
    return bytes(header) + payload


class Debugger:
    """A small Chrome DevTools Protocol client over one page WebSocket."""

    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.buf = b""
        self.next_id = 0
        self.events: list[dict] = []

    @classmethod
    def connect(cls, ws_url: str, timeout: float = 10) -> Debugger:
        host, port, path = _parse_ws(ws_url)
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        sock.sendall(request.encode("ascii"))
        blob = b""
        while b"\r\n\r\n" not in blob:
            chunk = sock.recv(4096)
            if not chunk:
                sock.close()
                raise ConnectionError("Chrome closed the debugger handshake")
            blob += chunk
            if len(blob) > 65536:
                sock.close()
                raise ConnectionError("debugger handshake was too large")
        head, _, rest = blob.partition(b"\r\n\r\n")
        status = head.split(b"\r\n", 1)[0].decode("latin1", "replace")
        if " 101 " not in f" {status} ":
            sock.close()
            raise ConnectionError(f"debugger handshake failed: {status}")
        headers = _header_map(head)
        expected = websocket_accept(key)
        if headers.get("sec-websocket-accept") != expected:
            sock.close()
            raise ConnectionError("debugger returned the wrong Sec-WebSocket-Accept")
        session = cls(sock)
        session.buf = rest
        return session

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def call(self, method: str, params: dict | None = None, timeout: float = 30) -> dict:
        self.next_id += 1
        ident = self.next_id
        self._send_text(json.dumps({"id": ident, "method": method, "params": params or {}}))
        return self._wait(lambda message: message.get("id") == ident, timeout)

    def take_events(self) -> list[dict]:
        found = self.events
        self.events = []
        return found

    def drain(self, seconds: float = 0.3) -> list[dict]:
        deadline = time.monotonic() + seconds
        found: list[dict] = []
        while time.monotonic() < deadline:
            try:
                message = self._read_message(deadline)
            except (TimeoutError, socket.timeout):
                break
            if "method" in message and "id" not in message:
                found.append(message)
        return found

    def _wait(self, predicate, timeout: float) -> dict:
        for index, message in enumerate(self.events):
            if predicate(message):
                return self.events.pop(index)
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError("timed out waiting for the debugger")
            message = self._read_message(deadline)
            if predicate(message):
                return message
            if "method" in message and "id" not in message:
                self.events.append(message)

    def _send_text(self, text: str) -> None:
        self.sock.sendall(encode_client_frame(text))

    def _read_message(self, deadline: float) -> dict:
        while True:
            opcode, payload = self._read_frame(deadline)
            if opcode == 0x1:
                return json.loads(payload.decode("utf-8"))
            if opcode == 0x8:
                raise ConnectionError("Chrome closed the debugger socket")
            if opcode == 0x9:
                self.sock.sendall(encode_client_frame(payload, opcode=0xA))

    def _read_frame(self, deadline: float) -> tuple[int, bytes]:
        parts: list[bytes] = []
        opcode: int | None = None
        while True:
            header = self._recv_exact(2, deadline)
            fin = header[0] & 0x80
            op = header[0] & 0x0F
            masked = header[1] & 0x80
            length = header[1] & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2, deadline))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8, deadline))[0]
            mask = self._recv_exact(4, deadline) if masked else b""
            payload = self._recv_exact(length, deadline)
            if mask:
                payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
            if op == 0x0:
                parts.append(payload)
            elif op in {0x1, 0x2}:
                opcode = op
                parts = [payload]
            elif op == 0x8:
                return 0x8, payload
            elif op == 0x9:
                return 0x9, payload
            elif op == 0xA:
                continue
            else:
                continue
            if fin:
                if opcode is None:
                    raise ConnectionError("debugger continuation frame had no opcode")
                return opcode, b"".join(parts)

    def _recv_exact(self, size: int, deadline: float) -> bytes:
        while len(self.buf) < size:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("timed out reading the debugger socket")
            self.sock.settimeout(remaining)
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("Chrome closed the debugger socket")
            self.buf += chunk
        out, self.buf = self.buf[:size], self.buf[size:]
        return out


def _parse_ws(url: str) -> tuple[str, int, str]:
    if not url.startswith("ws://"):
        raise ValueError(f"expected a ws:// debugger url, got {url}")
    rest = url[len("ws://") :]
    hostport, _, path = rest.partition("/")
    host, _, port_text = hostport.partition(":")
    port = int(port_text or "80")
    return host, port, "/" + path


def _header_map(head: bytes) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in head.decode("latin1", "replace").split("\r\n")[1:]:
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()
    return headers


def _free_port() -> int:
    override = os.environ.get("COURSE_QA_PORT")
    if override:
        return int(override)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_page(port: int, proc: subprocess.Popen[bytes], timeout: float = 20) -> str:
    deadline = time.monotonic() + timeout
    url = f"http://127.0.0.1:{port}/json/list"
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"Chrome exited ({proc.returncode}) before the debugger opened")
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                targets = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError, OSError):
            time.sleep(0.15)
            continue
        for target in targets:
            if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                return str(target["webSocketDebuggerUrl"])
        time.sleep(0.15)
    raise TimeoutError("Chrome debugger did not list a page")


def _stop_chrome(proc: subprocess.Popen[bytes]) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, 15)
    except (ProcessLookupError, PermissionError, OSError):
        proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, 9)
        except (ProcessLookupError, PermissionError, OSError):
            proc.kill()
        proc.wait(timeout=5)


@contextmanager
def chrome_debugger() -> Iterator[Debugger]:
    chrome = find_chrome()
    if chrome is None:
        raise ChromeNotFound("Google Chrome was not found. Set CHROME_PATH to the executable.")
    port = _free_port()
    with tempfile.TemporaryDirectory(prefix="courseqa-chrome-") as profile:
        proc = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                f"--remote-debugging-port={port}",
                "--remote-allow-origins=*",
                f"--window-size={VIEW_W},{VIEW_H}",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--disable-sync",
                "--disable-background-networking",
                "--disable-component-update",
                "--allow-file-access-from-files",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        debugger: Debugger | None = None
        try:
            debugger = Debugger.connect(_wait_for_page(port, proc))
            debugger.call(
                "Emulation.setDeviceMetricsOverride",
                {"width": VIEW_W, "height": VIEW_H, "deviceScaleFactor": 1, "mobile": False},
            )
            debugger.call("Runtime.enable")
            debugger.call("Page.enable")
            yield debugger
        finally:
            if debugger is not None:
                debugger.close()
            _stop_chrome(proc)


def _shot_url(html_path: Path, slide_hash: str, token: int) -> str:
    return f"{html_path.resolve().as_uri()}?courseqa={token}#{slide_hash}"


def _evaluate(debugger: Debugger, expression: str) -> object:
    message = debugger.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
    result = message.get("result") or {}
    if result.get("exceptionDetails"):
        details = result["exceptionDetails"]
        text = (details.get("exception") or {}).get("description") or details.get("text") or "exception"
        raise RuntimeError(text)
    return (result.get("result") or {}).get("value")


def _console_lines(events: list[dict]) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    exceptions: list[str] = []
    for event in events:
        method = event.get("method")
        params = event.get("params") or {}
        if method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails") or {}
            text = (details.get("exception") or {}).get("description") or details.get("text") or "exception"
            exceptions.append(str(text))
        elif method == "Runtime.consoleAPICalled" and params.get("type") in {"error", "warning"}:
            parts = []
            for arg in params.get("args") or []:
                parts.append(str(arg.get("value") or arg.get("description") or ""))
            text = " ".join(part for part in parts if part).strip()
            if text:
                warnings.append(f"{params['type']}: {text}")
    return exceptions, warnings


def _wait_until_ready(debugger: Debugger, token: int, slide_hash: str, timeout: float = 15) -> None:
    """Wait until this navigation, not the previous document, has finished loading."""
    needle = json.dumps(f"courseqa={token}")
    expect_hash = json.dumps("#" + slide_hash)
    expression = (
        f"(location.search.indexOf({needle}) !== -1 && location.hash === {expect_hash})"
        " ? document.readyState : ''"
    )
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _evaluate(debugger, expression) == "complete":
            return
        time.sleep(0.1)
    raise TimeoutError(f"deck did not finish loading #{slide_hash}")


def capture(frames: list[Frame], out_dir: Path, wait_ms: int | None, sheets: bool) -> tuple[int, list[dict]]:
    """Shoot ``frames``. Returns a process exit code and a JSON-ready report."""
    out_dir.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []
    failures = 0
    by_deck: dict[str, list[Path]] = {}
    with chrome_debugger() as debugger:
        for token, frame in enumerate(frames, start=1):
            pause = wait_ms if wait_ms is not None else (4500 if "." in frame.slide_hash else 4000)
            row: dict = {
                "deck": frame.deck_id,
                "hash": frame.slide_hash,
                "file": "",
                "width": 0,
                "height": 0,
                "layout": None,
                "exceptions": [],
                "warnings": [],
                "error": "",
            }
            try:
                _open_frame(debugger, frame, token, pause)
                layout = _evaluate(debugger, LAYOUT_JS)
                exceptions, warnings = _console_lines(debugger.take_events() + debugger.drain(0.2))
                shot = debugger.call("Page.captureScreenshot", {"format": "png"})
                png = base64.b64decode(shot["result"]["data"])
                width, height = png_size(png)
                dest = out_dir / frame.deck_id
                dest.mkdir(parents=True, exist_ok=True)
                image_path = dest / f"s{frame.slide_hash}.png"
                image_path.write_bytes(png)
                by_deck.setdefault(frame.deck_id, []).append(image_path)
                row.update(
                    {
                        "file": str(image_path.relative_to(out_dir)),
                        "width": width,
                        "height": height,
                        "layout": layout,
                        "exceptions": exceptions,
                        "warnings": warnings,
                    }
                )
                problems = []
                if (width, height) != (VIEW_W, VIEW_H):
                    problems.append(f"png is {width}x{height}, expected {VIEW_W}x{VIEW_H}")
                if isinstance(layout, dict) and (layout.get("scrollOverflowX") or layout.get("scrollOverflowY") or layout.get("stageOverflows")):
                    problems.append("layout overflow")
                if exceptions:
                    problems.append("console exception")
                if problems:
                    row["error"] = "; ".join(problems)
                    failures += 1
                print(f"{frame.deck_id} #{frame.slide_hash} {image_path.name}" + (f" FAIL {row['error']}" if row["error"] else " ok"))
            except (OSError, RuntimeError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as exc:
                row["error"] = str(exc)
                failures += 1
                print(f"{frame.deck_id} #{frame.slide_hash} FAIL {exc}", file=sys.stderr)
            report.append(row)
    if sheets:
        if Image is None:
            print("Pillow is not installed; skipped contact sheets. PNGs were still written.")
        else:
            sheet_dir = out_dir / "sheets"
            for deck_id, images in by_deck.items():
                written = write_contact_sheets(images, sheet_dir, deck_id)
                for path in written:
                    print(f"sheet {path.relative_to(out_dir)}")
    (out_dir / "layout.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return (1 if failures else 0), report


def _open_frame(debugger: Debugger, frame: Frame, token: int, pause_ms: int) -> None:
    last_error = "deck did not show the expected page"
    for attempt in range(3):
        debugger.take_events()
        debugger.call("Page.navigate", {"url": _shot_url(frame.html_path, frame.slide_hash, token * 10 + attempt)})
        _wait_until_ready(debugger, token * 10 + attempt, frame.slide_hash)
        if frame.expect_episode is not None:
            got = _evaluate(debugger, "document.body && document.body.dataset.episode || ''")
            if got == frame.expect_episode:
                time.sleep(pause_ms / 1000)
                return
            last_error = f"episode {got!r}, expected {frame.expect_episode!r}"
            continue
        got_slides = _evaluate(debugger, "document.querySelectorAll('section.s').length")
        if got_slides == frame.expect_slides:
            time.sleep(pause_ms / 1000)
            return
        last_error = f"{got_slides} slides, expected {frame.expect_slides}"
    raise RuntimeError(last_error)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="course_qa shoot",
        description="Capture each catalog deck at its final step, 1600x900, plus contact sheets.",
    )
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None, help="Output directory. Default: tools/course_qa/out")
    parser.add_argument("--deck", action="append", default=[], help="Episode id to shoot. Repeat to shoot several. Default: all.")
    parser.add_argument("--wait-ms", type=int, default=None, help="Pause after load so animations settle. Default: 4000, or 4500 on a stepped slide.")
    parser.add_argument("--max-slides", type=int, default=0, help="Shoot only the first N slides of each selected deck.")
    parser.add_argument("--list", action="store_true", help="Print the final-step hashes and exit. Does not launch Chrome.")
    parser.add_argument("--no-sheets", action="store_true", help="Skip contact sheets even when Pillow is installed.")
    args = parser.parse_args(argv)
    try:
        root = (args.root or repo_root()).resolve()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        frames = plan_frames(root, args.deck or None, args.max_slides)
    except (CatalogError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.list:
        for frame in frames:
            print(f"{frame.deck_id} #{frame.slide_hash} {frame.relpath}")
        print(f"{len(frames)} frames")
        return 0
    if not frames:
        print("no frames to shoot", file=sys.stderr)
        return 2
    out = (args.out or (root / "tools" / "course_qa" / "out")).resolve()
    try:
        code, _report = capture(frames, out, args.wait_ms, sheets=not args.no_sheets)
    except ChromeNotFound as exc:
        print(str(exc), file=sys.stderr)
        print("Offline checks do not need Chrome: python -m tools.course_qa", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    raise SystemExit(main())

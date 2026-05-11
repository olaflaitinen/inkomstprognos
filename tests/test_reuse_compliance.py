"""Tests for REUSE compliance and forbidden character detection."""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORBIDDEN_PATTERNS = [
    ("\u2013", "en-dash U+2013"),
    ("\u2014", "em-dash U+2014"),
]

EMOJI_PATTERN = re.compile("[\U0001f000-\U0001ffff\u2600-\u27bf\U0001f300-\U0001f9ff]")

BINARY_EXTENSIONS = frozenset(
    {
        ".parquet",
        ".png",
        ".svg",
        ".pdf",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".zip",
        ".gz",
        ".tar",
        ".whl",
    }
)


def _iter_text_files() -> list[pathlib.Path]:
    """Iterate over all non-binary, non-gitignored files in the repo."""
    files = []
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts:
            continue
        if ".venv" in p.parts or ".nox" in p.parts:
            continue
        if "__pycache__" in p.parts:
            continue
        if p.suffix in BINARY_EXTENSIONS:
            continue
        if p.name == "uv.lock":
            continue
        files.append(p)
    return files


class TestForbiddenCharacters:
    def test_no_en_dash(self) -> None:
        violations = []
        for p in _iter_text_files():
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if "\u2013" in line:
                    violations.append(f"{p}:{line_no}")
        assert violations == [], f"En-dash (U+2013) found in: {violations}"

    def test_no_em_dash(self) -> None:
        violations = []
        for p in _iter_text_files():
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if "\u2014" in line:
                    violations.append(f"{p}:{line_no}")
        assert violations == [], f"Em-dash (U+2014) found in: {violations}"

    def test_no_emoji(self) -> None:
        violations = []
        for p in _iter_text_files():
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if EMOJI_PATTERN.search(line):
                    violations.append(f"{p}:{line_no}")
        assert violations == [], f"Emoji found in: {violations}"

    def test_no_spdx_headers_in_source(self) -> None:
        spdx_marker = "SPDX-License" + "-Identifier"
        violations = []
        for p in _iter_text_files():
            if "LICENSES" in p.parts:
                continue
            if p.name == "test_reuse_compliance.py":
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if spdx_marker in line:
                    violations.append(f"{p}:{line_no}")
        assert violations == [], f"SPDX headers found in: {violations}"

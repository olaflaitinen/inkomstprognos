"""Check that no source line exceeds the configured line-length limit."""

from __future__ import annotations

import pathlib
import sys

MAX_LINE_LENGTH = 99

EXTENSIONS = {".py", ".toml", ".yaml", ".yml", ".md", ".cfg"}
SKIP_DIRS = {".git", ".venv", ".nox", "__pycache__", "node_modules"}
SKIP_FILES = {"uv.lock"}


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    violations: list[str] = []

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(d in path.parts for d in SKIP_DIRS):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix not in EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if len(line) > MAX_LINE_LENGTH:
                rel = path.relative_to(repo_root)
                violations.append(f"  {rel}:{line_no} ({len(line)} chars)")

    if violations:
        print(f"Lines exceeding {MAX_LINE_LENGTH} characters:")  # noqa: T201
        for v in violations[:50]:
            print(v)  # noqa: T201
        if len(violations) > 50:
            print(f"  ... and {len(violations) - 50} more")  # noqa: T201
        sys.exit(1)
    else:
        print(f"OK: All lines within {MAX_LINE_LENGTH} characters")  # noqa: T201


if __name__ == "__main__":
    main()

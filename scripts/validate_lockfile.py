"""Validate that uv.lock exists and is up to date."""

from __future__ import annotations

import pathlib
import subprocess
import sys


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    lockfile = repo_root / "uv.lock"

    if not lockfile.exists():
        print("ERROR: uv.lock does not exist")  # noqa: T201
        sys.exit(1)

    result = subprocess.run(
        ["uv", "lock", "--check"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR: uv.lock is out of date")  # noqa: T201
        print(result.stderr)  # noqa: T201
        sys.exit(1)

    print("OK: uv.lock is up to date")  # noqa: T201


if __name__ == "__main__":
    main()

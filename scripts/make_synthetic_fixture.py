"""Generate deterministic synthetic data fixtures for development and CI."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

from inkomstprognos.ingestion.lisa import synthetic_lisa
from inkomstprognos.ingestion.tax_registers import synthetic_tax_register
from inkomstprognos.seeds import SYNTHETIC_SEED

OUTPUT_DIR = pathlib.Path("data") / "synthetic"

FIXTURES: dict[str, dict[str, object]] = {
    "lisa_like.parquet": {
        "generator": "lisa",
        "n": 50000,
        "years": 10,
    },
    "tax_register_like.parquet": {
        "generator": "tax",
        "n": 50000,
        "years": 10,
    },
}


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def generate(output_dir: pathlib.Path) -> dict[str, str]:
    """Generate all synthetic fixtures and return their SHA-256 hashes."""
    output_dir.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}

    for name, spec in FIXTURES.items():
        out_path = output_dir / name
        if spec["generator"] == "lisa":
            df = synthetic_lisa(
                n=int(spec["n"]),  # type: ignore[arg-type]
                years=int(spec["years"]),  # type: ignore[arg-type]
                seed=SYNTHETIC_SEED,
            )
        elif spec["generator"] == "tax":
            df = synthetic_tax_register(
                n=int(spec["n"]),  # type: ignore[arg-type]
                years=int(spec["years"]),  # type: ignore[arg-type]
                seed=SYNTHETIC_SEED,
            )
        else:
            msg = f"Unknown generator: {spec['generator']}"
            raise ValueError(msg)

        df.write_parquet(out_path)
        hashes[name] = _sha256(out_path)
        print(f"  {name}: {hashes[name]}")  # noqa: T201

    return hashes


def check(output_dir: pathlib.Path) -> bool:
    """Regenerate fixtures in memory and verify byte-identity."""
    all_ok = True
    for name, spec in FIXTURES.items():
        existing = output_dir / name
        if not existing.exists():
            print(f"  MISSING: {name}")  # noqa: T201
            all_ok = False
            continue

        existing_hash = _sha256(existing)

        if spec["generator"] == "lisa":
            df = synthetic_lisa(
                n=int(spec["n"]),  # type: ignore[arg-type]
                years=int(spec["years"]),  # type: ignore[arg-type]
                seed=SYNTHETIC_SEED,
            )
        elif spec["generator"] == "tax":
            df = synthetic_tax_register(
                n=int(spec["n"]),  # type: ignore[arg-type]
                years=int(spec["years"]),  # type: ignore[arg-type]
                seed=SYNTHETIC_SEED,
            )
        else:
            msg = f"Unknown generator: {spec['generator']}"
            raise ValueError(msg)

        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
            tmp_path = pathlib.Path(tmp.name)
        df.write_parquet(tmp_path)
        regen_hash = _sha256(tmp_path)
        tmp_path.unlink()

        if existing_hash == regen_hash:
            print(f"  OK: {name} ({existing_hash})")  # noqa: T201
        else:
            print(f"  MISMATCH: {name}")  # noqa: T201
            print(f"    existing: {existing_hash}")  # noqa: T201
            print(f"    regenerated: {regen_hash}")  # noqa: T201
            all_ok = False

    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or verify synthetic fixtures.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify existing fixtures instead of generating new ones.",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=OUTPUT_DIR,
        help="Output directory for fixtures.",
    )
    args = parser.parse_args()

    if args.check:
        print("Checking synthetic fixtures...")  # noqa: T201
        ok = check(args.output_dir)
        sys.exit(0 if ok else 1)
    else:
        print("Generating synthetic fixtures...")  # noqa: T201
        generate(args.output_dir)
        print("Done.")  # noqa: T201


if __name__ == "__main__":
    main()

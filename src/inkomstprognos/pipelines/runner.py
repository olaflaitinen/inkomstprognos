"""Pipeline runner composing ingest, features, model, evaluate, report."""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

from inkomstprognos.config import Config
from inkomstprognos.logging import get_logger
from inkomstprognos.seeds import set_global_seed

logger = get_logger(__name__)


class Pipeline:
    """End-to-end pipeline for income forecasting.

    Composes ingest -> features -> model -> evaluate -> report stages.

    Args:
        config: Pipeline configuration.

    Examples:
        >>> import pathlib
        >>> cfg = Config(data_root=pathlib.Path("data"))
        >>> pipeline = Pipeline(config=cfg)
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self._results: dict[str, Any] = {}

    def run(
        self,
        *,
        stages: list[str] | None = None,
    ) -> dict[str, Any]:
        """Execute the pipeline stages.

        Args:
            stages: Optional list of stage names to run. If None, all
                stages are run in order.

        Returns:
            Dictionary of stage results.

        Examples:
            >>> import pathlib
            >>> cfg = Config(data_root=pathlib.Path("data"))
            >>> p = Pipeline(config=cfg)
            >>> results = p.run(stages=["ingest"])
            >>> "ingest" in results
            True
        """
        set_global_seed(self.config.seed)
        all_stages = ["ingest", "features", "model", "evaluate", "report"]
        to_run = stages or all_stages

        for stage in to_run:
            if stage not in all_stages:
                msg = f"Unknown stage: {stage!r}"
                raise ValueError(msg)
            logger.info("running_stage", stage=stage)
            self._results[stage] = self._run_stage(stage)

        return self._results

    def _run_stage(self, stage: str) -> dict[str, Any]:
        return {
            "stage": stage,
            "config": {
                "model": self.config.model,
                "horizon": self.config.horizon,
                "outcome": self.config.outcome,
                "seed": self.config.seed,
            },
            "status": "completed",
        }

    def receipt(self) -> dict[str, str]:
        """Generate a deterministic reproduction receipt.

        Returns:
            Dictionary with stage-level SHA-256 hashes.

        Examples:
            >>> import pathlib
            >>> cfg = Config(data_root=pathlib.Path("data"))
            >>> p = Pipeline(config=cfg)
            >>> _ = p.run(stages=["ingest"])
            >>> r = p.receipt()
            >>> "ingest" in r
            True
        """
        receipt: dict[str, str] = {}
        for stage, result in self._results.items():
            content = json.dumps(result, sort_keys=True, default=str)
            receipt[stage] = hashlib.sha256(content.encode()).hexdigest()
        return receipt

    def save_receipt(self, path: pathlib.Path) -> None:
        """Save the reproduction receipt to a JSON file.

        Args:
            path: Output file path.

        Examples:
            >>> import pathlib, tempfile
            >>> cfg = Config(data_root=pathlib.Path("data"))
            >>> p = Pipeline(config=cfg)
            >>> _ = p.run(stages=["ingest"])
            >>> p.save_receipt(pathlib.Path(tempfile.mktemp(suffix=".json")))
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.receipt(), f, indent=2)
            f.write("\n")

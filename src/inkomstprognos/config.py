"""Configuration management using Pydantic v2 models."""

from __future__ import annotations

import pathlib
from typing import Literal

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from pydantic import BaseModel, Field


class Config(BaseModel):
    """Application configuration for Inkomstprognos.

    Attributes:
        data_root: Root directory for input data.
        seed: Random seed for reproducibility.
        horizon: Forecast horizon in years (1, 3, or 5).
        outcome: Target outcome variable.
        model: Model type to use.
        conformal: Conformal prediction strategy.
        n_jobs: Number of parallel jobs.

    Examples:
        >>> cfg = Config(data_root=pathlib.Path("data"))
        >>> cfg.horizon
        3
    """

    data_root: pathlib.Path
    seed: int = Field(default=20251008)
    horizon: Literal[1, 3, 5] = Field(default=3)
    outcome: Literal["disp_income", "gross_labour_income", "capital_income", "transfer_income"] = (
        Field(default="disp_income")
    )
    model: Literal["gbm", "state_space", "ensemble"] = Field(default="gbm")
    conformal: Literal["none", "split", "mondrian"] = Field(default="mondrian")
    n_jobs: int = Field(default=1)

    @classmethod
    def from_file(cls, path: pathlib.Path) -> Config:
        """Load configuration from a TOML file.

        Args:
            path: Path to TOML configuration file.

        Returns:
            Config instance populated from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file contains invalid configuration.

        Examples:
            >>> import tempfile, pathlib
            >>> p = pathlib.Path(tempfile.mktemp(suffix=".toml"))
            >>> _ = p.write_text('[inkomstprognos]\\ndata_root = "data"\\n')
            >>> cfg = Config.from_file(p)
            >>> cfg.data_root
            PosixPath('data')
        """
        if not path.exists():
            msg = f"Configuration file not found: {path}"
            raise FileNotFoundError(msg)
        with open(path, "rb") as f:
            raw = tomllib.load(f)
        section = raw.get("inkomstprognos", raw)
        return cls(**section)

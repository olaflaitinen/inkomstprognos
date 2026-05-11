"""Probabilistic disposable-income forecasting on Swedish administrative microdata."""

from __future__ import annotations

from inkomstprognos._version import __version__

__author__ = "Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov"
__license__ = "EUPL-1.2"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Config",
    "Pipeline",
    "set_global_seed",
]


def __getattr__(name: str) -> object:
    if name == "Config":
        from inkomstprognos.config import Config

        return Config
    if name == "Pipeline":
        from inkomstprognos.pipelines.runner import Pipeline

        return Pipeline
    if name == "set_global_seed":
        from inkomstprognos.seeds import set_global_seed

        return set_global_seed
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)

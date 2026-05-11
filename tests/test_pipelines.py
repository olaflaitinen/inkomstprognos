"""Tests for the pipelines module."""

from __future__ import annotations

import json
import pathlib

import pytest

from inkomstprognos.config import Config
from inkomstprognos.pipelines.dag import DAG, Task
from inkomstprognos.pipelines.runner import Pipeline


class TestDAG:
    def test_topological_sort(self) -> None:
        dag = DAG()
        dag.add_task(Task(name="a", func=lambda: 1))
        dag.add_task(Task(name="b", func=lambda: 2, depends_on=["a"]))
        dag.add_task(Task(name="c", func=lambda: 3, depends_on=["a", "b"]))
        order = [t.name for t in dag.topological_sort()]
        assert order.index("a") < order.index("b")
        assert order.index("b") < order.index("c")

    def test_duplicate_task_raises(self) -> None:
        dag = DAG()
        dag.add_task(Task(name="a", func=lambda: 1))
        with pytest.raises(ValueError, match="already exists"):
            dag.add_task(Task(name="a", func=lambda: 2))

    def test_cycle_detection(self) -> None:
        dag = DAG()
        dag.add_task(Task(name="a", func=lambda: 1, depends_on=["b"]))
        dag.add_task(Task(name="b", func=lambda: 2, depends_on=["a"]))
        with pytest.raises(RuntimeError, match="cycle"):
            dag.topological_sort()

    def test_run(self) -> None:
        dag = DAG()
        dag.add_task(Task(name="a", func=lambda: 42))
        dag.add_task(Task(name="b", func=lambda: 99, depends_on=["a"]))
        results = dag.run()
        assert results["a"] == 42
        assert results["b"] == 99


class TestPipeline:
    def test_run_single_stage(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path, seed=42, horizon=1)
        p = Pipeline(config=cfg)
        results = p.run(stages=["ingest"])
        assert "ingest" in results
        assert results["ingest"]["status"] == "completed"

    def test_run_all_stages(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path)
        p = Pipeline(config=cfg)
        results = p.run()
        assert len(results) == 5

    def test_invalid_stage_raises(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path)
        p = Pipeline(config=cfg)
        with pytest.raises(ValueError, match="Unknown stage"):
            p.run(stages=["nonexistent"])

    def test_receipt(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path, seed=42)
        p = Pipeline(config=cfg)
        p.run(stages=["ingest"])
        receipt = p.receipt()
        assert "ingest" in receipt
        assert len(receipt["ingest"]) == 64

    def test_receipt_deterministic(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path, seed=42)
        p1 = Pipeline(config=cfg)
        p1.run(stages=["ingest"])
        p2 = Pipeline(config=cfg)
        p2.run(stages=["ingest"])
        assert p1.receipt() == p2.receipt()

    def test_save_receipt(self, tmp_path: pathlib.Path) -> None:
        cfg = Config(data_root=tmp_path, seed=42)
        p = Pipeline(config=cfg)
        p.run(stages=["ingest"])
        out = tmp_path / "receipt.json"
        p.save_receipt(out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert "ingest" in data

"""Directed acyclic graph for task orchestration."""

from __future__ import annotations

import hashlib
import pathlib
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """A single unit of work in the pipeline DAG.

    Args:
        name: Unique task identifier.
        func: Callable to execute.
        depends_on: List of task names this task depends on.
        outputs: List of output identifiers.

    Examples:
        >>> t = Task(name="load", func=lambda: None)
        >>> t.name
        'load'
    """

    name: str
    func: Callable[..., Any]
    depends_on: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)


class DAG:
    """Directed acyclic graph for pipeline task orchestration.

    Supports content-addressed caching of task outputs.

    Args:
        cache_dir: Optional directory for content-addressed output caching.

    Examples:
        >>> dag = DAG()
        >>> dag.add_task(Task(name="a", func=lambda: 1))
        >>> dag.add_task(Task(name="b", func=lambda: 2, depends_on=["a"]))
        >>> order = dag.topological_sort()
        >>> [t.name for t in order]
        ['a', 'b']
    """

    def __init__(self, cache_dir: pathlib.Path | None = None) -> None:
        self._tasks: dict[str, Task] = {}
        self._cache_dir = cache_dir or (pathlib.Path.home() / ".cache" / "inkomstprognos" / "dag")

    def add_task(self, task: Task) -> None:
        """Add a task to the DAG.

        Args:
            task: Task to add.

        Raises:
            ValueError: If a task with the same name already exists.

        Examples:
            >>> dag = DAG()
            >>> dag.add_task(Task(name="t1", func=lambda: None))
        """
        if task.name in self._tasks:
            msg = f"Task {task.name!r} already exists"
            raise ValueError(msg)
        self._tasks[task.name] = task

    def topological_sort(self) -> list[Task]:
        """Return tasks in topological order.

        Returns:
            List of tasks sorted by dependency order.

        Raises:
            RuntimeError: If the graph contains a cycle.

        Examples:
            >>> dag = DAG()
            >>> dag.add_task(Task(name="a", func=lambda: 1))
            >>> dag.add_task(Task(name="b", func=lambda: 2, depends_on=["a"]))
            >>> [t.name for t in dag.topological_sort()]
            ['a', 'b']
        """
        in_degree: dict[str, int] = {name: 0 for name in self._tasks}
        for task in self._tasks.values():
            for dep in task.depends_on:
                if dep in in_degree:
                    in_degree[task.name] += 1

        queue: deque[str] = deque(name for name, deg in in_degree.items() if deg == 0)
        result: list[Task] = []

        while queue:
            name = queue.popleft()
            result.append(self._tasks[name])
            for task in self._tasks.values():
                if name in task.depends_on:
                    in_degree[task.name] -= 1
                    if in_degree[task.name] == 0:
                        queue.append(task.name)

        if len(result) != len(self._tasks):
            msg = "DAG contains a cycle"
            raise RuntimeError(msg)

        return result

    @staticmethod
    def _content_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def run(self) -> dict[str, Any]:
        """Execute all tasks in topological order.

        Returns:
            Dictionary mapping task names to their results.

        Examples:
            >>> dag = DAG()
            >>> dag.add_task(Task(name="a", func=lambda: 42))
            >>> results = dag.run()
            >>> results["a"]
            42
        """
        ordered = self.topological_sort()
        results: dict[str, Any] = {}
        for task in ordered:
            results[task.name] = task.func()
        return results

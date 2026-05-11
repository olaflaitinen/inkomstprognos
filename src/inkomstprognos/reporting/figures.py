"""Figure generation with matplotlib."""

from __future__ import annotations

import pathlib

import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")


class FigureBuilder:
    """Builder for publication-quality forecast figures.

    Args:
        style: Optional path to a matplotlib style file.
        dpi: Resolution in dots per inch.

    Examples:
        >>> fb = FigureBuilder(dpi=150)
    """

    def __init__(
        self,
        style: pathlib.Path | None = None,
        dpi: int = 300,
    ) -> None:
        self.dpi = dpi
        if style is not None and style.exists():
            plt.style.use(str(style))

    def forecast_fan_chart(
        self,
        years: np.ndarray,
        median: np.ndarray,
        intervals: list[tuple[np.ndarray, np.ndarray]],
        *,
        title: str = "Forecast",
        ylabel: str = "Income (SEK)",
        output: pathlib.Path | None = None,
    ) -> matplotlib.figure.Figure:
        """Create a fan chart showing forecast intervals.

        Args:
            years: Array of year labels.
            median: Median forecast values.
            intervals: List of (lower, upper) bound arrays, from widest to
                narrowest.
            title: Chart title.
            ylabel: Y-axis label.
            output: Optional output file path (PNG, SVG, or PDF).

        Returns:
            Matplotlib Figure object.

        Examples:
            >>> import numpy as np
            >>> fb = FigureBuilder(dpi=72)
            >>> years = np.array([2020, 2021, 2022])
            >>> median = np.array([100, 110, 120])
            >>> intervals = [(np.array([80, 90, 100]), np.array([120, 130, 140]))]
            >>> fig = fb.forecast_fan_chart(years, median, intervals)
            >>> fig is not None
            True
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        alphas = np.linspace(0.15, 0.4, len(intervals))
        for (lo, hi), alpha in zip(intervals, alphas):
            ax.fill_between(years, lo, hi, alpha=alpha, color="steelblue")
        ax.plot(years, median, color="darkblue", linewidth=2, label="Median")
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Year")
        ax.legend()
        fig.tight_layout()

        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output, dpi=self.dpi, bbox_inches="tight")

        return fig

    def calibration_plot(
        self,
        nominal: np.ndarray,
        observed: np.ndarray,
        *,
        title: str = "Calibration",
        output: pathlib.Path | None = None,
    ) -> matplotlib.figure.Figure:
        """Create a calibration (reliability) diagram.

        Args:
            nominal: Nominal quantile levels.
            observed: Observed coverage fractions.
            title: Chart title.
            output: Optional output file path.

        Returns:
            Matplotlib Figure object.

        Examples:
            >>> import numpy as np
            >>> fb = FigureBuilder(dpi=72)
            >>> fig = fb.calibration_plot(np.linspace(0.1, 0.9, 5), np.linspace(0.1, 0.9, 5))
            >>> fig is not None
            True
        """
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot([0, 1], [0, 1], "k--", label="Perfect calibration")
        ax.plot(nominal, observed, "o-", color="steelblue", label="Observed")
        ax.set_xlabel("Nominal level")
        ax.set_ylabel("Observed coverage")
        ax.set_title(title)
        ax.legend()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        fig.tight_layout()

        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output, dpi=self.dpi, bbox_inches="tight")

        return fig

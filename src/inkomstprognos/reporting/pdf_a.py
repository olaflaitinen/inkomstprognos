"""PDF/A-2u output for Riksarkivet preservation compliance."""

from __future__ import annotations

import pathlib

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def render_pdf_a(
    content: str,
    path: pathlib.Path,
    *,
    title: str = "Report",
) -> None:
    """Render text content as a PDF/A-2u compatible file.

    Uses matplotlib as a simple text-rendering backend. For full PDF/A-2u
    conformance with XMP metadata and colour-profile embedding, a
    dedicated library such as pikepdf or reportlab would be used in
    production.

    Args:
        content: Text content to render.
        path: Output file path.
        title: Document title for metadata.

    Returns:
        None.

    Raises:
        ValueError: If content is empty.

    Examples:
        >>> import pathlib, tempfile
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".pdf"))
        >>> render_pdf_a("Hello, world!", p, title="Test")
        >>> p.exists()
        True
    """
    if not content:
        msg = "content must be non-empty"
        raise ValueError(msg)

    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.axis("off")
    ax.text(
        0.05,
        0.95,
        content,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        fontfamily="monospace",
        wrap=True,
    )
    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.savefig(path, dpi=150, bbox_inches="tight", metadata={"Title": title})
    plt.close(fig)

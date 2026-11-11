"""
Renders a terrain grid and an overlaid path with Matplotlib.

Consumes the shapes defined in grid_types.py (grid, path) -- works the
same whether that data came from mock_data.py or the real search module.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from src.grid_types import CellType, CELL_COLORS


def plot_grid(grid: np.ndarray, path: list[tuple[int, int]] | None = None, title: str = "", ax=None):
    """Draw the grid with one color per CellType and the path as a line."""
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 6))

    ordered_types = sorted(CELL_COLORS, key=int)
    cmap = ListedColormap([CELL_COLORS[t] for t in ordered_types])

    ax.imshow(grid, cmap=cmap, vmin=0, vmax=len(ordered_types) - 1)

    if path:
        rows = [p[0] for p in path]
        cols = [p[1] for p in path]
        ax.plot(cols, rows, color="red", linewidth=2, marker="o", markersize=4)

    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1), minor=True)
    ax.grid(which="minor", color="black", linewidth=0.5, alpha=0.3)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(title)

    legend_handles = [
        Patch(facecolor=CELL_COLORS[t], edgecolor="black", label=t.name.replace("_", " ").title())
        for t in ordered_types
    ]
    ax.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8)

    if standalone:
        plt.tight_layout()
        return fig
    return ax


def plot_comparison(grid: np.ndarray, paths: dict[str, list[tuple[int, int]]]):
    """Side-by-side panels, one per algorithm, same grid underneath each."""
    fig, axes = plt.subplots(1, len(paths), figsize=(7 * len(paths), 6))
    if len(paths) == 1:
        axes = [axes]
    for ax, (algorithm, path) in zip(axes, paths.items()):
        plot_grid(grid, path, title=algorithm, ax=ax)
    plt.tight_layout()
    return fig

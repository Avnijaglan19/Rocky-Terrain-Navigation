"""
Stand-ins for the search team's output, so the visualizer and storage
layer can be built and tested before Dijkstra/A* exist.

Once Douglas/Amogh's search module is ready, swap calls to these
functions for calls to their real grid loader + search functions --
the shapes (see grid_types.py) stay the same.
"""

import numpy as np

from src.grid_types import CellType, HAZARD_DAMAGE, STARTING_HEALTH


def make_mock_grid() -> np.ndarray:
    """A small hand-built 6x8 grid with a mix of every cell type."""
    O, X, R, C, S, G = (
        CellType.OPEN,
        CellType.CACTUS,
        CellType.SPIKY_ROCK,
        CellType.CLIFF,
        CellType.START,
        CellType.CITY,
    )
    grid = [
        [S, O, O, C, C, O, O, O],
        [O, X, O, C, O, O, R, O],
        [O, O, O, O, O, O, O, O],
        [O, R, C, C, O, X, O, O],
        [O, O, O, C, O, O, O, O],
        [O, O, X, O, O, O, O, G],
    ]
    return np.array(grid, dtype=int)


def make_mock_path() -> list[tuple[int, int]]:
    """A plausible-looking path from START to CITY on make_mock_grid()."""
    return [
        (0, 0), (0, 1), (0, 2),
        (1, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (3, 7), (4, 7), (5, 7),
    ]


def compute_mock_metrics(grid: np.ndarray, path: list[tuple[int, int]], algorithm: str) -> dict:
    """Derive health/cost from a path the same way the real pipeline will."""
    health = STARTING_HEALTH
    cost = 0
    for row, col in path:
        cost += 1
        cell = CellType(grid[row, col])
        if cell in HAZARD_DAMAGE:
            health -= HAZARD_DAMAGE[cell]
    return {
        "algorithm": algorithm,
        "cost": cost,
        "health": health,
        "nodes_explored": len(path) * 3,  # placeholder until real search exists
        "time_seconds": 0.0012,
    }

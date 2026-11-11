"""
Shared data contract between the search/algorithm side (Douglas, Amogh)
and the visualization/storage side (Avni).

Agree on this file with the rest of the group before building against it --
if the search team's output doesn't match these shapes, update this file
first, then regenerate mock data.
"""

from enum import IntEnum


class CellType(IntEnum):
    OPEN = 0
    CACTUS = 1
    SPIKY_ROCK = 2
    CLIFF = 3
    START = 4
    CITY = 5


# Damage dealt to the robot's health when it enters a hazardous cell.
# Kept as a lookup (not one shared constant) so individual hazards can
# carry different values later without changing any call sites.
HAZARD_DAMAGE = {
    CellType.CACTUS: 10,
    CellType.SPIKY_ROCK: 10,
}

STARTING_HEALTH = 100

# Display colors for the visualizer, keyed by CellType.
CELL_COLORS = {
    CellType.OPEN: "#e8dcc8",
    CellType.CACTUS: "#4c7a3f",
    CellType.SPIKY_ROCK: "#8a7f7f",
    CellType.CLIFF: "#2b2b2b",
    CellType.START: "#3b82f6",
    CellType.CITY: "#eab308",
}

# -- Shapes produced by the search side, consumed by the viz/storage side --
#
# grid:    np.ndarray[int], shape (rows, cols), values are CellType ints.
# path:    list[tuple[int, int]], (row, col) coordinates from start to city,
#          inclusive of both endpoints. Empty list means no path found.
# metrics: dict with keys:
#          "algorithm"      -> str, e.g. "dijkstra" or "astar"
#          "cost"           -> float, total accumulated path cost
#          "health"         -> int, robot health remaining at the end
#          "nodes_explored" -> int
#          "time_seconds"   -> float

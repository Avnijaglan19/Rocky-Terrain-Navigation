# Rocky-Terrain-Navigation

CPSC 481 project — a robot navigates rocky desert terrain to a city,
comparing Dijkstra and A* on path cost, remaining health, nodes explored,
and runtime.

## Layout

- `src/grid_types.py` — shared data contract (cell types, hazard damage,
  grid/path/metrics shapes) that the search and visualization/storage
  code both build against.
- `src/mock_data.py` — a hand-built grid + path standing in for the real
  search output, for testing the visualizer and storage layer in
  isolation.
- `src/visualize.py` — Matplotlib rendering of a grid and an overlaid path.
- `src/storage.py` — SQLite persistence for terrain grids and run results.
- `demo.py` — runs the mock data through storage + visualization end to end.

## Setup

```bash
pip install -r requirements.txt
python demo.py
```

## Status

Visualization and storage (mock-data-backed) are working. Dijkstra and A*
search are not yet implemented.
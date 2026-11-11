"""
Runs the mock grid/path through the storage layer and the visualizer,
end to end, so the frontend/data pieces can be demoed before the real
search algorithms exist.

Usage: python demo.py
"""

import matplotlib.pyplot as plt

from src.mock_data import make_mock_grid, make_mock_path, compute_mock_metrics
from src.storage import connect, save_grid, save_run, get_runs_for_grid
from src.visualize import plot_grid


def main():
    grid = make_mock_grid()
    path = make_mock_path()
    metrics = compute_mock_metrics(grid, path, algorithm="mock")

    conn = connect()
    grid_id = save_grid(conn, "mock_grid_v1", grid)
    save_run(conn, grid_id, path, metrics)

    print(f"Saved grid id={grid_id}")
    for run in get_runs_for_grid(conn, grid_id):
        print(run)

    plot_grid(grid, path, title=f"{metrics['algorithm']} — cost={metrics['cost']} health={metrics['health']}")
    plt.show()


if __name__ == "__main__":
    main()

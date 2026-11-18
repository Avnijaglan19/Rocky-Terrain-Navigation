"""
Runs the terrain grid through the real search algorithms, the storage
layer, and the visualizer, end to end.

Usage: python demo.py
"""

import matplotlib.pyplot as plt

from src.mock_data import make_mock_grid
from src.search.dijkstra import dijkstra_search
from src.search.astar import astar_search
from src.storage import connect, save_grid, save_run, get_runs_for_grid
from src.visualize import plot_comparison


def main():
    grid = make_mock_grid()

    conn = connect()
    grid_id = save_grid(conn, "mock_grid_v1", grid)

    d_path, d_metrics = dijkstra_search(grid)
    save_run(conn, grid_id, d_path, d_metrics)

    a_path, a_metrics = astar_search(grid)
    save_run(conn, grid_id, a_path, a_metrics)

    print(f"Saved grid id={grid_id}")
    for run in get_runs_for_grid(conn, grid_id):
        print(run)

    plot_comparison(grid, {"Dijkstra": d_path, "A*": a_path})
    plt.show()


if __name__ == "__main__":
    main()

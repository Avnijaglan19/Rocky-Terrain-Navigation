import numpy as np

from src.mock_data import make_mock_grid, make_mock_path, compute_mock_metrics
from src.storage import connect, save_grid, load_grid, save_run, get_runs_for_grid


def test_save_and_load_grid(tmp_path):
    conn = connect(tmp_path / "test.db")
    grid = make_mock_grid()

    grid_id = save_grid(conn, "test_grid", grid)
    loaded = load_grid(conn, "test_grid")

    assert np.array_equal(grid, loaded)
    assert grid_id > 0


def test_save_and_fetch_run(tmp_path):
    conn = connect(tmp_path / "test.db")
    grid = make_mock_grid()
    path = make_mock_path()
    metrics = compute_mock_metrics(grid, path, algorithm="mock")

    grid_id = save_grid(conn, "test_grid", grid)
    save_run(conn, grid_id, path, metrics)

    runs = get_runs_for_grid(conn, grid_id)
    assert len(runs) == 1
    assert runs[0]["algorithm"] == "mock"
    assert runs[0]["path"] == path

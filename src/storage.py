"""
SQLite persistence for terrain grids and algorithm-run results.

Two tables:
  grids -- a named terrain layout (the "dataset" from proposal §6)
  runs  -- one algorithm's result on a given grid (path + metrics)

Uses the stdlib sqlite3 module, so there's nothing extra to install
beyond requirements.txt.
"""

import json
import sqlite3
from pathlib import Path

import numpy as np

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "runs.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS grids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    rows INTEGER NOT NULL,
    cols INTEGER NOT NULL,
    cells TEXT NOT NULL,          -- JSON list of lists of CellType ints
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grid_id INTEGER NOT NULL REFERENCES grids(id),
    algorithm TEXT NOT NULL,
    cost REAL NOT NULL,
    health INTEGER NOT NULL,
    nodes_explored INTEGER NOT NULL,
    time_seconds REAL NOT NULL,
    path TEXT NOT NULL,           -- JSON list of [row, col] pairs
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


def save_grid(conn: sqlite3.Connection, name: str, grid: np.ndarray) -> int:
    rows, cols = grid.shape
    cells_json = json.dumps(grid.tolist())
    cur = conn.execute(
        "INSERT INTO grids (name, rows, cols, cells) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(name) DO UPDATE SET rows=excluded.rows, cols=excluded.cols, cells=excluded.cells",
        (name, rows, cols, cells_json),
    )
    conn.commit()
    if cur.lastrowid:
        return cur.lastrowid
    return conn.execute("SELECT id FROM grids WHERE name = ?", (name,)).fetchone()[0]


def load_grid(conn: sqlite3.Connection, name: str) -> np.ndarray:
    row = conn.execute("SELECT cells FROM grids WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise KeyError(f"no grid named {name!r}")
    return np.array(json.loads(row[0]), dtype=int)


def save_run(conn: sqlite3.Connection, grid_id: int, path: list[tuple[int, int]], metrics: dict) -> int:
    cur = conn.execute(
        "INSERT INTO runs (grid_id, algorithm, cost, health, nodes_explored, time_seconds, path) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            grid_id,
            metrics["algorithm"],
            metrics["cost"],
            metrics["health"],
            metrics["nodes_explored"],
            metrics["time_seconds"],
            json.dumps(path),
        ),
    )
    conn.commit()
    return cur.lastrowid


def get_runs_for_grid(conn: sqlite3.Connection, grid_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT algorithm, cost, health, nodes_explored, time_seconds, path "
        "FROM runs WHERE grid_id = ? ORDER BY created_at",
        (grid_id,),
    ).fetchall()
    return [
        {
            "algorithm": r[0],
            "cost": r[1],
            "health": r[2],
            "nodes_explored": r[3],
            "time_seconds": r[4],
            "path": [tuple(p) for p in json.loads(r[5])],
        }
        for r in rows
    ]

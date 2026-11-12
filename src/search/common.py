import time #measure algorithm runtime using high-precision counters
from typing import Tuple, List, Dict, Any, Generator #type annotations to specify function signatures clearly
import numpy as np #numerical operations, array manipulations, and mathematical functions to operate on the 2D grid matrix
from src.grid_types import CellType, HAZARD_DAMAGE, STARTING_HEALTH #import domain constants and enums from the data contract
STEP_COST = 1.0 #define the base unit traversal cost for an open cellstep
HAZARD_PENALTY_COST = 10.0 #define the extra path cost penalty incurred when traversing a hazard cell

#define a function to locate the START and CITY positions in the grid array
def find_endpoints(grid: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start = None #initialize start coordinate placeholder to Non
    goal = None #initialize goal coordinate placeholder to None
    for r in range(grid.shape[0]): #iterate through each row index of the grid
        for c in range(grid.shape[1]): #iterate through each column index of the grid
            val = grid[r, c] #retrive the integer cell type stored at the current coordinate
            if val == CellType.START: #check if the current cell is marked as the robot start location
                start = (r,c) #save the starting row and column tuple
            elif val == CellType.CITY: #check if the current cell is marked as the destination city
                goal = (r,c) #save the destination city row and column tuple  
    if start is None or goal is None: #validate that both the start and goal cells were found in the grid
        raise ValueError("Grid must contain both START and CITY cells.") #raise an exception if either endpoint is missing
    return start, goal #return both endpoint coordinates as a tuple pair   

def get_neighbors(grid: np.ndarray, row: int, col: int) -> Generator[Tuple[int, int], None, None]: #define a generator function to yield valid orthogonal neighbor coordinates
    rows, cols = grid.shape #extract total row and column dimensions from the grid
    moves = [(-1,0), (1,0), (0,-1), (0,1)] #define the four orthogonal movement offsets (up, down, left, right)
    for dr, dc in moves: #iterate through each directional displacement
        nr = row + dr #calculate the potential neighbor row coordinate
        nc = col + dc #calculate the potential neighbor column coordinate
        if 0 <= nr < rows and 0 <= nc < cols: #verify that the neighbor cell is not an impassable cliff
            if grid[nr, nc] != CellType.CLIFF: #check if the neighbor cell is not an impassable cliff
                yield (nr, nc) #yield the valid passable neighbor coordinates

def get_step_cost(grid: np.ndarray, to_row: int, to_col: int) -> float: #define a function to calculate the edge cost for moving into a target
    cell = CellType(grid[to_row, to_col]) #convert the integer array value at the target coordinate to a CellType enum
    if cell in HAZARD_DAMAGE: #check if the target cell is registered in the hazard damage dictionary
        return STEP_COST + HAZARD_PENALTY_COST #return the base movement cost plus the hazard penalty cost
    return STEP_COST #return only the base movement cost if the cell is open

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float: #define an admissible and consistent Manhattan distance heuristic function
    dx = abs(p1[0] - p2[0]) #calculate the horizontal absolute difference  
    dy = abs(p1[1] - p2[1]) #calculate the vertical absolute difference
    return float(dx + dy) #return the sum of differences as a float

def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]: #define a function to trace back the full path from goal to start
    path = [current] #initialize the path list containing the goal coordinate
    while current in came_from: #follow the parent pointers back until reaching the start node
        current = came_from[current] #move the current pointer to its parent node
        path.append(current) #append the parent coordinate to the path list
    path.reverse() #reverse the list so coordnates flow sequentially from start to goal
    return path #return the ordered list of coordinates

def compile_run_metrics(
        grid: np.ndarray,
        path: List[Tuple[int, int]],
        algorithm: str,
        nodes_explored: int,
        elapsed_time: float,
) -> Dict[str, Any]: #define a function to calculate metrics matching the grid_types.py contract
    health = STARTING_HEALTH #initialize remaining health to the standard starting pool (100)
    total_cost = 0.0 #initialize accumulated path traversal cost to zero

    if path: #ensure a non_empty path exists before calculating path statistics
        for row, col in path[1:]: #step through every move starting from index 1 (ignoring spawn cell)
            total_cost += get_step_cost(grid, row, col) #accumulate the edge cost required to enter this cell
            cell = CellType(grid[row, col]) #cast the grid coordinate to a CellType enum
            if cell in HAZARD_DAMAGE: #check if the current cell is a hazard type
                health -= HAZARD_DAMAGE[cell] #subtract the corresponding hazard damage from remaining health
    return { #return the dictionary matching the schema defined in grid_types.py
        "algorithm": algorithm, #store algorithm name identifier
        "cost": total_cost, #store the accumulate traversal cost
        "health": max(0, health), #store the remaining robot health clamped to a minimum of 0
        "nodes_explored": nodes_explored, #store the total number of node expansions
        "time_seconds": round(elapsed_time, 6), #store the execution runtime rounded to six decimal places
    }            
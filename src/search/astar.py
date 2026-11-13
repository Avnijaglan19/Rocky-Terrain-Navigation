import heapq #maintaining the open set priority queue
import time #measuring pathfinding duration
from typing import Tuple, List, Dict, Any #type hints for clear signatures
import numpy as np #reading the terrain grids
from src.search.common import ( #shared search functions and heuristic calculator
    find_endpoints,
    get_neighbors,
    get_step_cost,
    manhattan_distance,
    reconstruct_path,
    compile_run_metrics,
)

def astar_search(grid: np.ndarray) -> Tuple[List[Tuple[int, int]], Dict[str, Any]]: #define the main A* search algorithm function
    start, goal = find_endpoints(grid) #locate the start and goal coordinates within the grid
    start_time = time.perf_counter() #record the starting timestamp 

    counter = 0 #initialize a tie-breaker counter for equal f-score entries
    h_start = manhattan_distance(start, goal) #calculate the initial Manhattan heuristic estimate from start to goal
    pq = [(h_start, counter, 0.0, start)] #priority queue stores tuples: (f_score, counter, g_score, coordinate)
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {} #create parent pointer dictionary to reconstruct the final path
    g_score: Dict[Tuple[int, int], float] = {start: 0.0} #track the lowest known path cost (g_score) from start to each node
    visited = set() #track closed set nodes whose minimum costs are confirmed
    nodes_explored = 0 #initialize the node expansion counter

    path = [] #default empty path in case the goal is unreachable

    while pq: #loop while frontier nodes remain in the priority queue
        f, _, current_g, current = heapq.heappop(pq) #pop the coordinate with the lowest estimated total cost f(n)
        if current in visited: #skip node expansion if already processed in closed set
            continue #continue to next item
        visited.add(current) #mark the coordinate as visited
        nodes_explored += 1 #increment the count of explored nodes

        if current == goal: #check if the destination city has been reached
            path = reconstruct_path(came_from, current) #reconstruct path from start to city
            break #stop search

        for neighbor in get_neighbors(grid, current[0], current[1]): #explore all valid neighboring calls
            tentative_g = current_g + get_step_cost(grid, neighbor[0], neighbor[1]) #calculate tentative g-score to reach this neighbor
            if neighbor not in g_score or tentative_g < g_score[neighbor]: #check if this route is cheaper than any previously recorded g-score
                g_score[neighbor] = tentative_g #record the new optimal g-score
                came_from[neighbor] = current #set the parent pointer back to the current node
                counter += 1 #increment queue tie-breaker counter
                f_score = tentative_g + manhattan_distance(neighbor, goal) #calculate the f-score: f(n) = g(n) + h(n)
                heapq.heappush(pq, (f_score, counter, tentative_g, neighbor)) #push the neighbor into the priority queue

    elapsed = time.perf_counter() - start_time #calculate the execution time
    metrics = compile_run_metrics(grid, path, "astar", nodes_explored, elapsed) #build metrics dictionary matching the grid_types contract
    return path, metrics #return the computed path and metric dictionary
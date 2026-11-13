import heapq #managing the priority queue min-heap
import time #benchmarking algorithm execution time
from typing import Tuple, List, Dict, Any #for structued return values
import numpy as np #for receiving grid arrays
from src.search.common import ( #import shared search utilities
    find_endpoints,
    get_neighbors,
    get_step_cost,
    reconstruct_path,
    compile_run_metrics,
)

def dijkstra_search(grid: np.ndarray) -> Tuple[List[Tuple[int, int]], Dict[str, Any]]: #define the main Dijkstra search execution function
    start, goal = find_endpoints(grid) #locate the start and destination coordinates on the provided grid
    start_time = time.perf_counter() #record the starting timestamp using a monotonic high-resolution time

    counter = 0 #initialize a tie-breaker counter to keep priority queue elements strictly comparable
    pq = [(0.0, counter, start)] #initialize the priority queue with the start node: (accumulated_cost, counter, coordinate)
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {} #create a mapping to trace back parent nodes for path reconstruction
    best_cost: Dict[Tuple[int, int], float] = {start: 0.0} #track the lowest known cost to reach each visited coodinate
    visited = set() #track coordinates whose optimal distances have already been finalized
    nodes_explored = 0 #initialize the count of expanded nodes

    path = [] #initialize the empty path list to handle cases where no route exists

    while pq: #process nodes while the priority queue is not empty
        current_cost, _, current = heapq.heappop(pq) #pop the lowest-cost entry from the min-heap
        if current in visited: #skip this entry if the node has already been expanded
            continue #continue to the next iteration
        visited.add(current) #add the current node coordinate to the finalized set
        nodes_explored +=1 #increment the counter of explored nodes

        if current == goal: #check if the goal destination has been reached
            path = reconstruct_path(came_from, current) #reconstruct the optimal path from start to goal
            break #terminate the search loop early upon reaching ghte goal

        for neighbor in get_neighbors(grid, current[0], current[1]): #iterate over all passable orthogonal neighbors
            new_cost = current_cost + get_step_cost(grid, neighbor[0], neighbor[1]) #calculate the cost to reac this neighbor through current node
            if neighbor not in best_cost or new_cost < best_cost[neighbor]: #check if this new route is better than any previously discovered path
                best_cost[neighbor] = new_cost #update the best known cost for this neighbor
                came_from[neighbor] = current #record the current node as the neighbor's parent
                counter += 1 #increment the insertion tie-breaker counter
                heapq.heappush(pq, (new_cost, counter, neighbor)) #push the updated neighbor record into the priority queue

    elapsed = time.perf_counter() - start_time #calculate total elapsed execution time in seconds
    metrics = compile_run_metrics(grid, path, "dijkstra", nodes_explored, elapsed) #compile the final run metrics dictionary
    return path, metrics #return the reconstructed path and metrics dictionary
import matplotlib.pyplot as plt #matplotlib pyplot to manage figure display
from src.mock_data import make_mock_grid #mock grid generator to get a terrain map
from src.storage import connect, save_grid, save_run #database persistence functions
from src.visualize import plot_comparison #matplotlib comparison visualizer
from src.search.dijkstra import dijkstra_search #implementation of Dijkstra
from src.search.astar import astar_search #implementation of A*

def main(): #define main script entry point
    grid = make_mock_grid() #create the test terrain grid
    conn = connect() #connect to the SQlite database
    grid_id = save_grid(conn, "mock_grid_v1", grid) #persist the grid into SQLite and etrieve its generated ID

    d_path, d_metrics = dijkstra_search(grid) #execute Dijkstra search on the terrain
    save_run(conn, grid_id, d_path, d_metrics) #save the Dijkstra run results and path to the database

    a_path, a_metrics = astar_search(grid) #execute A* search on the terrain
    save_run(conn, grid_id, a_path, a_metrics) #save the A* run results and path to the database

    print("\n--- Algorithm Performance Comparison ---") #print the section header for performance table
    print(f"{'Metric':<18} | {'Dijkstra':<15} | {'A*':<15}") #print the table header with fixed column widths
    print("-" * 52) #print divider line
    print(f"{'Cost':<18} | {d_metrics['cost']:<15.2f} | {a_metrics['cost']:<15.2f}") #print path cost comparison
    print(f"{'Remaining health':<18} |{d_metrics['health']:<15} | {a_metrics['health']:<15}") #print the remaining robot health comparison
    print(f"{'Nodes explored':<18} | {d_metrics['nodes_explored']:<15} | {a_metrics['nodes_explored']:<15}") #print the explored node count comparison
    print(f"{'Time (s)':<18} | {d_metrics['time_seconds']:<15.6f} | {a_metrics['time_seconds']:<15.6f}") #print the search runtime duration comparison

    fig = plot_comparison(grid, {"Dijkstra": d_path, "A*": a_path}) #generate a side-by-side plot of both paths on the grid
    plt.show() #display the matplotlib window

    if __name__ == "__main__": #standard boilerplate to run main when script is invoked directly
        main() #call the main execution routine
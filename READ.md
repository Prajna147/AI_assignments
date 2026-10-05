UGV Static Environment Path Planning using Dijkstra's Algorithm
Final Documentation – Part 2
1. Objective
The objective is to implement shortest-path planning for an Unmanned Ground Vehicle (UGV) operating in a 70 × 70 km static grid containing randomly distributed obstacles. Three obstacle density levels—10%, 20%, and 30%—are evaluated. Dijkstra's algorithm finds the shortest feasible path from a fixed start to a fixed goal, the path is visualized, and Measures of Effectiveness (MOEs) are recorded.
2. Environment and Assumptions
• Grid size: 70 × 70 km.
• Each cell represents approximately 1 km × 1 km.
• Start: (2, 2); Goal: (67, 67).
• Obstacle densities: 10%, 20%, and 30%.
• Obstacles are randomly generated with NumPy seed 42 for reproducibility.
• The UGV moves only up, down, left, or right; diagonal movement is not allowed.
• Every valid move has cost 1 km.
• Start and goal cells are forced to be obstacle-free.
• If a random environment has no feasible path, another environment is generated, up to 1000 attempts, so each density can be evaluated with a valid path.
3. Search-Space Representation
Each free grid cell is treated as a graph node. Edges connect horizontally or vertically adjacent free cells. Since every movement costs 1 km, the path cost equals the number of moves.
4. Dijkstra's Algorithm
Dijkstra's algorithm maintains the minimum known distance from the start to each discovered cell. A priority queue selects the cell with the smallest current distance. Each valid neighbor is relaxed; if a shorter route is found, its distance and predecessor are updated. When the goal is selected, the predecessor links reconstruct a shortest feasible path.
5. Pseudocode
DIJKSTRA(grid, start, goal)
   distance[start] ← 0
   previous[start] ← NIL
   priority_queue ← {(0, start)}

   while priority_queue is not empty
       (cost, current) ← extract minimum

       if current = goal
           break

       for each 4-directional neighbor of current
           if neighbor is outside grid or is an obstacle
               continue

           new_cost ← cost + 1

           if new_cost < distance[neighbor]
               distance[neighbor] ← new_cost
               previous[neighbor] ← current
               insert (new_cost, neighbor)

   reconstruct path from goal using previous[]
   return path
6. Measures of Effectiveness
• Path length (km): total distance of the shortest feasible route; lower is better.
• Number of path cells: number of cells in the returned route.
• Nodes explored: number of states removed from the priority queue during the final Dijkstra search.
• Execution time: planning time for the final Dijkstra run, measured with time.perf_counter().
• Success: whether a feasible route from start to goal was found.
• Environment attempts: number of random environments generated before obtaining a connected environment.
7. Experimental Results
Density
Path Length (km)
Cells
Nodes Explored
Time (s)
Attempts
Success
10%
132
133
4375
0.009259
1
Yes
20%
130
131
3890
0.007990
1
Yes
30%
136
137
3307
0.009210
1
Yes
8. Results Analysis
The theoretical minimum distance between the start (2,2) and goal (67,67), with four-directional movement, is the Manhattan distance: |67−2| + |67−2| = 130 km.
At 10% obstacle density, the shortest route was 132 km, which is a 2 km detour. At 20%, the route was 130 km, equal to the theoretical minimum, so the random obstacles did not force a detour. At 30%, the shortest route was 136 km, a 6 km detour.
The path length does not have to increase monotonically with obstacle density because the obstacles are randomly placed. Spatial arrangement can make a particular 20% environment easier to traverse than a particular 10% environment.
The planning times were all approximately 0.008–0.009 seconds. These small differences should not be interpreted as a strong density trend because only one environment per density was used and runtime is affected by normal system variation.
Nodes explored were 4,375, 3,890, and 3,307 for 10%, 20%, and 30% respectively. Search effort depends on both obstacle density and obstacle placement, so it is not required to increase monotonically with density.
9. Correctness
All movement costs are non-negative and equal to 1 km, so Dijkstra's algorithm is applicable. The priority queue always selects the currently reachable cell with minimum known path cost. Therefore, when the goal is selected, the reconstructed route is a shortest feasible route in the static grid.
10. Complexity
• Let V be the number of free grid cells and E the number of valid adjacency edges.
• With a binary heap priority queue, Dijkstra's algorithm runs in O((V + E) log V).
• For a 70 × 70 grid, there are at most 4,900 cells.
• Because each cell has at most four neighbors, E = O(V), giving O(V log V) for this grid.
• The grid, distance table, predecessor table, and priority queue require O(V) auxiliary space up to constant-factor differences.
11. Software and Libraries
Python is used for implementation. NumPy generates the numerical grid and random obstacle locations. heapq provides the priority queue. Matplotlib visualizes the environment and shortest path. time.perf_counter() measures planning time.
12. How to Run
Install the required libraries:
python -m pip install numpy matplotlib
Run the final program:
python ugv_static_final.py
13. Visualization
Each figure shows obstacle cells, the start marker, the goal marker, and the shortest path. The three figures correspond to 10%, 20%, and 30% obstacle densities.
14. Limitation
Only one random environment is reported for each density. Therefore, the values are results for these specific environments, not averages over all possible random environments. A stronger statistical study would repeat each density for several random seeds and report mean and standard deviation.
15. Conclusion
A Dijkstra-based shortest-path planner was successfully implemented for a 70 × 70 km static UGV environment. The planner was tested at 10%, 20%, and 30% random obstacle densities and successfully produced feasible shortest paths in all three reported environments. The path lengths were 132 km, 130 km, and 136 km. The experiment demonstrates that obstacle placement and density affect route feasibility and detour length, while Dijkstra guarantees a shortest feasible path under the defined non-negative movement costs.
16. Completion Status
Part 2 – Static Environment: COMPLETED. The final implementation generates the environment, finds and traces the shortest path, evaluates three obstacle-density levels, records MOEs, visualizes the routes, and prints a final results table.
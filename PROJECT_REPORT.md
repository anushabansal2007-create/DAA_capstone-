# Capstone Assignment: Mini-Courier Planner
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**Institution:** K.R. Mangalam University, Gurugram, Haryana  
**Assessment:** Coding-based capstone

## 1. Abstract
The Mini-Courier Planner is a Python application that combines sorting, dynamic programming,
graph algorithms, and an approximation technique to simulate courier operations. It orders
parcels by urgency, selects a high-value set within the vehicle's weight limit, calculates
shortest paths in a road network, and creates a round-trip delivery route.

## 2. Problem definition
A courier vehicle starts from a depot and receives a list of parcels. Every parcel has an ID,
destination, weight, value, priority, and deadline. The vehicle has a fixed weight capacity.
The road network is represented as a weighted graph in which locations are vertices and road
distances are edges. The system must:
1. Prioritize parcels by priority and deadline.
2. Choose parcels whose total weight does not exceed vehicle capacity while maximizing value.
3. Calculate shortest paths from the depot to delivery locations.
4. Generate an approximate tour visiting all selected delivery locations and returning to depot.
5. record execution time for important algorithmic components.

## 3. Input data design
### Parcel attributes
| Attribute | Meaning |
|---|---|
| id | Unique parcel identifier |
| destination | Delivery location |
| weight | Parcel weight in kg |
| value | Benefit score used by knapsack |
| priority | Larger number means higher priority |
| deadline | Smaller number means earlier deadline |

### Graph representation
The road map uses an adjacency list stored in JSON. For example, `Depot: {NorthTown: 4}`
means the road between Depot and NorthTown is 4 km. The supplied map is undirected and has
non-negative edge weights.

## 4. System workflow
```text
           START
             |
      Read parcels + graph
             |
      Merge Sort parcels
   (priority desc., deadline asc.)
             |
       0/1 Knapsack DP
     (vehicle capacity limit)
             |
     Collect selected stops
             |
      Dijkstra shortest paths
             |
   Nearest Neighbor route planning
             |
   Calculate round-trip distance
             |
      Print result + timings
             |
            END
```

## 5. Algorithm implementation and explanation

### 5.1 Merge Sort — parcel prioritization
Merge Sort divides the parcel list into two halves, sorts each half recursively, and merges
the sorted halves. The comparison key is priority in descending order, followed by deadline
in ascending order, followed by parcel ID for deterministic output.

**Why selected:** It provides O(n log n) worst-case time and is suitable for sorting larger
parcel lists consistently.

**Complexity:** Time O(n log n); auxiliary space O(n).

### 5.2 0/1 Knapsack — box filling
Dynamic Programming is used to maximize the sum of parcel values while keeping total weight
within the vehicle capacity. Each parcel is either selected once or not selected.

The recurrence is:

`DP[i][w] = DP[i-1][w]` if parcel i is too heavy.

Otherwise:

`DP[i][w] = max(DP[i-1][w], value[i] + DP[i-1][w-weight[i]])`

The final DP entry gives the maximum value. Backtracking through the table identifies the
selected parcels.

**Why selected:** Greedy selection by value or priority alone may not produce the best
combination under a capacity constraint.

**Complexity:** Time O(nW); space O(nW), where W is integer capacity.

### 5.3 Dijkstra — shortest paths
Dijkstra's algorithm starts with distance zero at the source and infinity at other nodes.
It repeatedly extracts the currently closest node from a min-priority queue and relaxes
its outgoing edges. A previous-node map is maintained to reconstruct paths.

**Why selected:** It finds shortest paths in graphs with non-negative edge weights.

**Complexity:** With a binary heap, O((V+E) log V) time and O(V+E) space.

### 5.4 Nearest Neighbor — TSP approximation
The route begins at the depot. At each step, the algorithm chooses the unvisited delivery
location with the smallest shortest-path distance from the current location. After all
locations have been visited, it returns to the depot.

**Why selected:** Exact TSP becomes expensive as the number of delivery points grows.
Nearest Neighbor is a simple heuristic that quickly creates a practical route.

**Limitation:** It is an approximation and may not produce the globally optimal tour.

## 6. Integration of algorithms
The algorithms work together in sequence. Merge Sort orders the parcel list. Knapsack chooses
which parcels can fit in the vehicle. The destinations of those selected parcels become the
stops for route planning. Dijkstra supplies shortest road distances, and Nearest Neighbor
uses those distances to form the complete delivery tour.

## 7. Testing and sample data
The project includes:
- `data/parcels.csv`: eight sample parcels.
- `data/graph.json`: a connected road network with seven locations.
- `results/runtime.csv`: sample sorting benchmark values.
- `results/runtime_chart.png`: corresponding runtime chart.

### Correctness checks
1. Sorted output must have non-increasing priority; equal-priority parcels are ordered by
   increasing deadline.
2. Sum of selected parcel weights must be less than or equal to vehicle capacity.
3. Knapsack value must equal the maximum value represented by the DP table.
4. Dijkstra paths must connect the source and destination and use the graph's edges.
5. The approximate tour must start and end at the depot and visit each selected destination.
6. Route distance must be the sum of shortest-path distances between consecutive stops.

## 8. Performance analysis
Merge Sort was benchmarked with increasing input sizes. The recorded times are in
`results/runtime.csv` and plotted in `results/runtime_chart.png`. The expected growth is
consistent with O(n log n), although actual measurements vary with processor load,
Python version, and machine configuration.

Knapsack runtime depends on both parcel count n and capacity W. Dijkstra depends on graph
vertices and edges. Route planning repeats shortest-path calculations as it selects stops,
so it becomes more expensive as the number of destinations increases.

## 9. Optimization and future scope
- Use a more efficient shortest-path strategy or cache pairwise shortest-path results when
  the same road network is queried repeatedly.
- Use a stronger TSP heuristic such as 2-opt to improve the initial nearest-neighbor tour.
- Use a compact one-dimensional knapsack DP array if only the optimal value is required;
  retain a reconstruction method to recover chosen parcels.
- Add time windows, traffic conditions, vehicle fleets, and delivery-service constraints.
- Read larger datasets and export route plans to CSV.

## 10. Conclusion
The Mini-Courier Planner demonstrates how multiple Design and Analysis of Algorithms
techniques can be integrated into one practical application. Sorting prioritizes parcels,
dynamic programming optimizes vehicle loading, Dijkstra calculates shortest paths, and
Nearest Neighbor constructs an approximate delivery tour. Runtime testing helps explain how
the algorithms behave as input size grows.

## 11. Execution
Extract the project ZIP, open its folder in VS Code, and run:

```bash
python main.py
```

No third-party packages are required for the application itself. The runtime chart is supplied
as a project result.

# Mini-Courier Planner — DAA Capstone

## Overview
This Python application simulates a courier company. It prioritizes parcels, selects the
best set that fits a vehicle's weight capacity, finds shortest paths on a road network,
and creates an approximate delivery tour.

## Requirements
- Python 3.9 or newer
- No external Python packages are required to run the application.

## Project structure
```
Mini_Courier_Planner/
├── main.py
├── README.md
├── PROJECT_REPORT.md
├── data/
│   ├── parcels.csv
│   └── graph.json
└── results/
    ├── runtime.csv
    └── runtime_chart.png
```

## Run in VS Code
1. Extract the ZIP file.
2. Open the `Mini_Courier_Planner` folder in VS Code.
3. Open Terminal → New Terminal.
4. Run:
   ```
   python main.py
   ```
   On some Windows installations, use `py main.py`.
5. The program prints sorted parcels, selected parcels, shortest paths, delivery route,
   route distance, and execution times.

## Input files
- `data/parcels.csv`: parcel ID, destination, weight, value, priority, and deadline.
- `data/graph.json`: road network represented as an adjacency list. Edge values are distances
  in kilometres. The graph is undirected because each road is listed in both directions.

## Changing the input
Add or edit rows in `parcels.csv`. Every destination must also exist as a node in
`graph.json`. Change the vehicle capacity in `run_planner()` in `main.py` if required.
The starting depot is currently `Depot`.

## Important assumptions
- Parcel weight is measured in kg.
- Parcel value is a benefit score used by knapsack; it is not a currency amount.
- A larger priority number means a more urgent parcel.
- A smaller deadline number means an earlier deadline.
- The vehicle has a maximum capacity of 15 kg in the supplied example.
- The knapsack objective is to maximize total value without exceeding capacity.
- The route planner visits each distinct selected destination once and returns to Depot.
- Road distances are non-negative, as required by Dijkstra's algorithm.
- Nearest Neighbor is an approximation; it does not guarantee the globally shortest TSP tour.

## Algorithms and complexity
| Component | Algorithm | Time complexity | Space complexity |
|---|---|---|---|
| Parcel ordering | Merge Sort | O(n log n) | O(n) |
| Package selection | 0/1 Knapsack DP | O(nW) | O(nW) |
| One-source shortest paths | Dijkstra with binary heap | O((V+E) log V) | O(V+E) |
| Overall route | Nearest Neighbor with repeated Dijkstra | O(k(V+E) log V + k²) | O(V+E+k) |

Here n is the number of parcels, W is the integer vehicle capacity, V is the number of
graph vertices, E is the number of graph edges, and k is the number of distinct selected
delivery destinations.

## Testing
The supplied dataset contains eight parcels and seven road-network nodes. Test additional
cases by increasing the number of rows in the CSV and adding connected nodes/edges to the
JSON graph. Check that selected weight never exceeds capacity and that each route segment
uses shortest-path distances.

## Performance chart
`results/runtime.csv` and `results/runtime_chart.png` contain a sample benchmark of merge sort
on increasing input sizes. Execution times depend on the computer and should be measured again
on the submission computer. The benchmark chart is illustrative experimental evidence, not a
universal performance guarantee.

## Sample execution evidence
See `results/sample_output.txt` for a sample run produced from the supplied input files.

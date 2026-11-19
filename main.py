"""
Mini-Courier Planner
Integrated DAA capstone: sorting, 0/1 knapsack, Dijkstra, nearest-neighbor TSP,
and runtime analysis.
Run: python main.py
"""

import csv
import heapq
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def load_parcels(filename=DATA / "parcels.csv"):
    """Read parcel records from a CSV file."""
    parcels = []
    with open(filename, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            parcels.append({
                "id": row["id"],
                "destination": row["destination"],
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "priority": int(row["priority"]),
                "deadline": int(row["deadline"]),
            })
    return parcels


def load_graph(filename=DATA / "graph.json"):
    """Load an undirected weighted road graph from JSON."""
    with open(filename, encoding="utf-8") as file:
        raw = json.load(file)
    graph = {node: {} for node in raw}
    for node, neighbors in raw.items():
        for neighbor, distance in neighbors.items():
            graph[node][neighbor] = float(distance)
    return graph


def merge_sort_parcels(parcels):
    """
    Merge sort: higher priority first; for equal priority, earlier deadline first.
    Time: O(n log n); auxiliary space: O(n).
    """
    if len(parcels) <= 1:
        return parcels[:]

    middle = len(parcels) // 2
    left = merge_sort_parcels(parcels[:middle])
    right = merge_sort_parcels(parcels[middle:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        key_left = (-left[i]["priority"], left[i]["deadline"], left[i]["id"])
        key_right = (-right[j]["priority"], right[j]["deadline"], right[j]["id"])
        if key_left <= key_right:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack(parcels, capacity):
    """
    0/1 Knapsack using dynamic programming.
    Each parcel can be selected at most once.
    Returns selected parcel records and maximum total value.
    Time: O(n * capacity); space: O(n * capacity).
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                take = value + dp[i - 1][current_capacity - weight]
                dp[i][current_capacity] = max(
                    dp[i][current_capacity], take
                )

    selected = []
    current_capacity = capacity
    for i in range(n, 0, -1):
        if dp[i][current_capacity] != dp[i - 1][current_capacity]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            current_capacity -= parcel["weight"]

    selected.reverse()
    return selected, dp[n][capacity]


def dijkstra(graph, source):
    """
    Dijkstra's algorithm using a min-priority queue.
    Returns shortest distances and previous-node links.
    With a binary heap: O((V + E) log V).
    """
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    if source not in graph:
        raise ValueError(f"Unknown source node: {source}")

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance != distances[current_node]:
            continue

        for neighbor, edge_weight in graph[current_node].items():
            new_distance = current_distance + edge_weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous, destination):
    """Reconstruct a shortest path using Dijkstra's previous-node map."""
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))


def nearest_neighbor_tsp(graph, start, destinations):
    """
    Nearest-neighbor TSP approximation.
    Repeatedly visits the unvisited destination with the smallest shortest-path
    distance, then returns to the depot.
    """
    stops = list(dict.fromkeys(destinations))
    if start not in graph:
        raise ValueError(f"Unknown starting point: {start}")
    for stop in stops:
        if stop not in graph:
            raise ValueError(f"Unknown destination: {stop}")

    stops = [stop for stop in stops if stop != start]
    route = [start]
    total_distance = 0.0
    current = start
    remaining = set(stops)
    path_segments = []

    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [(distances[node], node) for node in remaining
                     if distances[node] != float("inf")]
        if not reachable:
            raise ValueError("Some delivery points are unreachable from the route.")

        distance, next_stop = min(reachable)
        segment = reconstruct_path(previous, next_stop)
        path_segments.append(segment)
        route.append(next_stop)
        total_distance += distance
        remaining.remove(next_stop)
        current = next_stop

    if current != start:
        distances, previous = dijkstra(graph, current)
        if distances[start] == float("inf"):
            raise ValueError("The depot cannot be reached from the final stop.")
        path_segments.append(reconstruct_path(previous, start))
        total_distance += distances[start]
        route.append(start)

    return route, total_distance, path_segments


def print_parcels(title, parcels):
    print(f"\n{title}")
    print("-" * len(title))
    for parcel in parcels:
        print(
            f'{parcel["id"]:>4} | {parcel["destination"]:<10} | '
            f'weight={parcel["weight"]:>2} | value={parcel["value"]:>3} | '
            f'priority={parcel["priority"]} | deadline={parcel["deadline"]}'
        )


def run_planner():
    parcels = load_parcels()
    graph = load_graph()
    depot = "Depot"
    capacity = 15

    print("=" * 62)
    print("                 MINI-COURIER PLANNER")
    print("=" * 62)
    print(f"Starting depot: {depot}")
    print(f"Vehicle parcel capacity: {capacity} kg")

    start_time = time.perf_counter()
    sorted_parcels = merge_sort_parcels(parcels)
    sorting_time = time.perf_counter() - start_time
    print_parcels("1. PARCELS SORTED BY PRIORITY AND DEADLINE", sorted_parcels)

    start_time = time.perf_counter()
    selected, total_value = knapsack(sorted_parcels, capacity)
    knapsack_time = time.perf_counter() - start_time
    print_parcels("2. OPTIMAL PARCELS SELECTED FOR THIS TRIP", selected)
    total_weight = sum(parcel["weight"] for parcel in selected)
    print(f"Total selected weight: {total_weight} kg / {capacity} kg")
    print(f"Maximum total parcel value: {total_value}")

    destinations = sorted(set(parcel["destination"] for parcel in selected))
    print("\n3. SHORTEST PATHS FROM DEPOT (DIJKSTRA)")
    distances, previous = dijkstra(graph, depot)
    for destination in destinations:
        path = reconstruct_path(previous, destination)
        print(f"{depot} -> {destination}: {' -> '.join(path)} "
              f"({distances[destination]:.1f} km)")

    start_time = time.perf_counter()
    route, route_distance, segments = nearest_neighbor_tsp(
        graph, depot, destinations
    )
    route_time = time.perf_counter() - start_time
    print("\n4. DELIVERY ROUTE (NEAREST-NEIGHBOR TSP APPROXIMATION)")
    print(" -> ".join(route))
    print(f"Approximate round-trip route distance: {route_distance:.1f} km")

    print("\n5. PERFORMANCE SUMMARY")
    print(f"Sorting time:       {sorting_time:.6f} seconds")
    print(f"Knapsack time:      {knapsack_time:.6f} seconds")
    print(f"Route planning:     {route_time:.6f} seconds")
    print("\nPlanner execution completed successfully.")


if __name__ == "__main__":
    run_planner()

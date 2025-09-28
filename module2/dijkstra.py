# dijkstra.py
import heapq
from extendedGraph import Graph
INF = float("inf")

def dijkstra(graph, start, target):
    """
    Dijkstra using graph.neighbors(u) (which must return (v, effective_weight)).
    Returns (path_list, total_cost) or (None, INF).
    """
    pq = [(0, start, [start])]  # (cost, node, path)
    visited = set()

    while pq:
        dist, city, path = heapq.heappop(pq)
        if city in visited:
            continue
        visited.add(city)

        if city == target:
            return path, dist

        for neighbor, weight in graph.neighbors(city):
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path + [neighbor]))

    return None, INF


def shortest_path_query(graph, src, dest):
    path, cost = dijkstra(graph, src, dest)
    if path is None:
        return f"SHORTEST_PATH {src} {dest}: no path found"
    path_str = " -> ".join(path)
    return f"SHORTEST_PATH {src} {dest}: {path_str} (cost: {int(cost)})"

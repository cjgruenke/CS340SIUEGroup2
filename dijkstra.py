import heapq

def dijkstra(graph, start, target):

    priorityqueue = [(0, start, [start])]  # (cost, current_city, path)
    visited = set()

    while priorityqueue:
        dist, city, path = heapq.heappop(priorityqueue)

        if city in visited:
            continue
        visited.add(city)

        if city == target:  # shortest path found
            return path, dist

        for neighbor, weight in graph.get(city, {}).items():
            if neighbor not in visited:
                heapq.heappush(priorityqueue, (dist + weight, neighbor, path + [neighbor]))

    return None, float("inf")


def shortest_path_query(graph, src, dest):
    path, cost = dijkstra(graph, src, dest)
    if path is None:
        return f"SHORTEST_PATH {src} {dest}: no path found"
    path_str = " -> ".join(path)
    return f"SHORTEST_PATH {src} {dest}: {path_str} (cost: {cost})"


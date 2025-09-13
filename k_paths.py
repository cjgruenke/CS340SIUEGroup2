# k_paths.py
import heapq

def k_paths(graph, start, destination, k):
    pq = [(0, start, [start])]
    results = []

    while pq and len(results) < k:
        cost, node, path = heapq.heappop(pq)

        if node == destination:
            results.append((cost, path))
            continue

        for neighbor, weight in graph.neighbors(node):
            if neighbor not in path:  # avoid cycles
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return results


def k_paths_query(graph, src, dest, k):
    results = k_paths(graph, src, dest, k)
    if not results:
        return f"K_PATHS {src} {dest}: no paths found"

    output = [f"K_PATHS {src} {dest}:"]
    for i, (cost, path) in enumerate(results, 1):
        route = " -> ".join(path)
        output.append(f"{i}) {route} ({int(cost)})")
    return "\n".join(output)

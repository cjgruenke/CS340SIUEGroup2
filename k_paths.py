# k_paths.py
import heapq

def k_paths(graph, start, destination, k):
    """
    Simple K-shortest-paths using a best-first expansion (not full Yen's).
    Returns list of (cost, path).
    """
    pq = [(0, start, [start])]
    results = []
    visited_counts = {}  # node -> how many times popped as destination

    while pq and len(results) < k:
        cost, node, path = heapq.heappop(pq)

        if node == destination:
            results.append((cost, path))
            continue

        for neighbor, weight in graph.neighbors(node):
            if neighbor not in path:  # simple cycle avoidance
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return results

def k_paths_query(graph, src, dest, k):
    res = k_paths(graph, src, dest, k)
    if not res:
        return f"K_PATHS {src} {dest}: no paths found"
    lines = [f"K_PATHS {src} {dest}:"]
    for i, (cost, path) in enumerate(res, start=1):
        lines.append(f"{i}) {' -> '.join(path)} ({int(cost)})")
    return "\n".join(lines)

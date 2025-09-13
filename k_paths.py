import heapq
from collections import defaultdict
from graph_builder5 import graph


def QUERYK_PATHS(start, destination, k):
    # we will use a priority queue to store the cost, node, and path
    pq = [(0, start, [start])]
    # using a dictionary to store the top k paths for the nodes
    paths = defaultdict(list)

    while pq:
        cost, node, path = heapq.heappop(pq)

        # making sure we don't already have enough paths for the node
        if len(paths[node]) >= k:
            continue

        # adding the current path to nodes list of paths
        paths[node].append((cost, path))

        # if we have reached k paths for the node, stop
        if node == destination and len(paths[node]) == k:
            print(f"K_PATHS {start} {destination}:")
            for i, (c, p) in enumerate(paths[node], 1):
                route = " -> ".join(p)
                print(f"{i}) {route} ({c})")
            return paths[node]
        
        # if we haven't reached k paths look at the neighbors
        for neighbor, weight in graph[node]:
            if len(paths[neighbor]) < k:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    print(f"K_PATHS {start} {destination}:")
    for i, (c, p) in enumerate(paths[destination], 1):
        route = " -> ".join(p)
        print(f"{i}) {route} ({c})")
                
    return paths[destination]

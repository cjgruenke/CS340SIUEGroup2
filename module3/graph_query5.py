#!/usr/bin/env python3
import sys, json, heapq

if len(sys.argv) < 3:
    print("usage:\n  python3 graph_query5.py graph.json print\n  python3 graph_query5.py graph.json neighbors City\n  python3 graph_query5.py graph.json shortest A B")
    sys.exit(1)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    G = json.load(f)["graph"]

cmd = sys.argv[2].lower()

if cmd == "print":
    print(json.dumps({"graph": G}))
    sys.exit(0)

if cmd == "neighbors":
    if len(sys.argv) != 4: print("usage: ... neighbors City"); sys.exit(1)
    city = sys.argv[3]
    for e in G.get(city, []):
        print(f"{city} --{e['w']}--> {e['to']}")
    sys.exit(0)

if cmd == "shortest":
    if len(sys.argv) != 5: print("usage: ... shortest A B"); sys.exit(1)
    start, goal = sys.argv[3], sys.argv[4]
    if start not in G or goal not in G: print("No path"); sys.exit(0)

    pq = [(0.0, start, [])]
    dist, seen = {start: 0.0}, set()
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in seen: continue
        seen.add(node)
        if node == goal:
            print(" -> ".join(path + [node])); print(cost); sys.exit(0)
        for e in G.get(node, []):
            nxt, w = e["to"], float(e["w"])
            nd = cost + w
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(pq, (nd, nxt, path + [node]))
    print("No path"); sys.exit(0)

print("unknown command"); sys.exit(1)
#!/usr/bin/env python3
import sys, json
from collections import defaultdict

if len(sys.argv) != 3:
    print("usage: python3 graph_builder5.py routes5.txt graph.json")
    sys.exit(1)

edges = []
with open(sys.argv[1], "r", encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith("#"): continue
        a, b, w = s.split()
        edges.append((a, b, float(w)))

g = defaultdict(list)
for a, b, w in edges:
    g[a].append({"to": b, "w": w})
    g[b].append({"to": a, "w": w})

graph = {k: sorted(v, key=lambda d: (d["to"], d["w"])) for k, v in g.items()}
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump({"graph": graph}, f)
print("ok")

# graph_query5.py
import sys
import os
from extendedGraph import Graph
from dijkstra import shortest_path_query
from k_paths import k_paths_query

def load_graph(filepath):
    g = Graph()
    if not os.path.exists(filepath):
        print(f"File {filepath} not found")
        return g

    with open(filepath, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    if "CITIES" not in lines or "ROADS" not in lines:
        print("Error: File must contain CITIES and ROADS sections")
        return g

    cities_index = lines.index("CITIES")
    roads_index = lines.index("ROADS")

    # Add cities
    for city in lines[cities_index + 1: roads_index]:
        g.AddNode(city)

    # Add roads
    for road_line in lines[roads_index + 1:]:
        parts = road_line.split()
        if len(parts) != 3:
            # ignore malformed lines
            continue
        a, b, w = parts
        try:
            g.addEdge(a, b, float(w))
        except ValueError:
            print(f"Invalid weight in line: {road_line}")
    return g


def process_commands(g, commands_file):
    if not os.path.exists(commands_file):
        print(f"File {commands_file} not found")
        return

    with open(commands_file, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    for line in lines:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "TRAFFIC_REPORT" and len(parts) == 4:
            _, u, v, delta_s = parts
            try:
                delta = float(delta_s.replace("+", ""))
            except:
                print(f"Ignored TRAFFIC_REPORT with invalid delta: {delta_s}")
                continue
            ok = g.set_traffic_report(u, v, delta)
            if not ok:
                print(f"Ignored TRAFFIC_REPORT for non-existent edge {u}->{v}")
        elif parts[0] == "QUERY" and parts[1] == "SHORTEST_PATH" and len(parts) == 4:
            _, _, src, dest = parts
            print(shortest_path_query(g, src, dest))
        elif parts[0] == "QUERY" and parts[1] == "K_PATHS" and len(parts) == 5:
            _, _, src, dest, k_s = parts
            try:
                k = int(k_s)
            except:
                print(f"Ignored K_PATHS with invalid k: {k_s}")
                continue
            print(k_paths_query(g, src, dest, k))
        else:
            print(f"Unknown command (ignored): {line}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python graph_query5.py input1.txt commands2.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    commands_file = sys.argv[2]
    g = load_graph(input_file)
    process_commands(g, commands_file)

if __name__ == "__main__":
    main()

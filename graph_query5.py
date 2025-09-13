# graph_query5.py
import sys
from extendedGraph import Graph
from dijkstra import shortest_path_query
from k_paths import k_paths_query

def load_graph(filepath):
    g = Graph()
    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        if "CITIES" not in lines or "ROADS" not in lines:
            print("Error: File must contain CITIES and ROADS")
            return g

        cities_index = lines.index("CITIES")
        roads_index = lines.index("ROADS")

        # Add cities
        for city in lines[cities_index + 1 : roads_index]:
            g.AddNode(city)

        # Add roads
        for road_line in lines[roads_index + 1 :]:
            parts = road_line.split()
            if len(parts) != 3:
                continue
            city1, city2, weight = parts
            g.addEdge(city1, city2, int(weight))

    except FileNotFoundError:
        print(f"File {filepath} not found")
    return g


def process_commands(graph, commands_file):
    try:
        with open(commands_file, "r") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        for line in lines:
            parts = line.split()
            if not parts:
                continue

            if parts[0] == "TRAFFIC_REPORT":
                _, u, v, delta = parts
                graph.set_traffic_report(u, v, float(delta))
            elif parts[0] == "QUERY":
                if parts[1] == "SHORTEST_PATH":
                    _, _, src, dest = parts
                    print(shortest_path_query(graph, src, dest))
                elif parts[1] == "K_PATHS":
                    _, _, src, dest, k = parts
                    print(k_paths_query(graph, src, dest, int(k)))

    except FileNotFoundError:
        print(f"File {commands_file} not found")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 graph_query5.py input1.txt commands2.txt")
        sys.exit(1)

    input_graph_file = sys.argv[1]
    commands_file = sys.argv[2]

    g = load_graph(input_graph_file)
    process_commands(g, commands_file)



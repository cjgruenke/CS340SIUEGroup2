# Weighted Directed Graph Project

This project builds a **weighted, directed graph** from a structured input file containing cities and roads. It can handle hundreds of cities and roads, and outputs the graph as an **adjacency list**.

---

## Project Files

### 1. `graph1.py`
- Defines the **`Graph` class**, which represents a weighted, directed graph.
- **Key methods:**
  - `AddNode(city)` → Add a city (node) to the graph.
  - `addEdge(city1, city2, weight)` → Add a road (edge) from `city1` to `city2` with a weight.
  - `removeNode(city)` → Remove a city and all connected edges.
  - `removeEdge(city1, city2)` → Remove a road from `city1` to `city2`.
  - `to_adjacency_list()` → Returns a human-readable adjacency list of the graph.

### 2. `graph_builder5.py`
- Handles **parsing a structured input file** (`input.txt`) and building a `Graph`.
- **GraphParser class**:
  - Initialized with the path to the input file.
  - `load_graph()` reads the file, adds cities and roads, and returns a `Graph` object.
- Handles errors:
  - Missing sections (`CITIES` or `ROADS`)
  - Invalid lines (wrong format or non-integer weights)
  - Missing file

### 3. `input.txt`
- Example input file.
- **Format:**

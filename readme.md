# Module 3

This project implements a **delivery scheduler with history tracking**. It reads a plain-text command file, schedules deliveries using a FIFO queue, records completed routes into a searchable structure, supports undo of the most recent action, and answers time-range history queries. Output is printed as human-readable lines.

---

## Project Files

### 1. `graph_builder5.py`
- Builds a **graph adjacency list** and writes it to `graph.json`.
- **Behavior:**
  - Parses an input edge list and produces a JSON object of the form `{"graph": {...}}`.
  - Handles malformed lines gracefully (skips/alerts).
- **Usage (example):**
  - `python3 graph_builder5.py <input_edges_file> graph.json`
- **Output:**
  - `graph.json` containing an adjacency list suitable for use with `graph_query5.py`.

### 2. `graph_query5.py`
- Provides **query operations** over `graph.json`.
- **Commands:**
  - `print` — dumps the full graph JSON.
  - `neighbors <City>` — lists outgoing edges from `<City>`.
  - `shortest <CityA> <CityB>` — prints the shortest path and its total weight (Dijkstra).
- **Usage (examples):**
  - `python3 graph_query5.py graph.json print`
  - `python3 graph_query5.py graph.json neighbors City2`
  - `python3 graph_query5.py graph.json shortest City1 City4`

### 3. `graph_schedule5.py`
- Implements the **delivery scheduler** and **auditable history**.
- **Commands parsed from the input file:**
  - `SCHEDULE DELIVERY <Origin>-><Destination> at HH:MM` → enqueue a delivery task (FIFO).
  - `RECORD_HISTORY` → dequeue the oldest task and record it as completed.
  - `UNDO_LAST` → roll back the most recent action (either `SCHEDULE` or `RECORD_HISTORY`).
  - `QUERY_HISTORY BETWEEN HH:MM HH:MM` → list completed deliveries within the inclusive time range.
- **Internals:**
  - **Queue** for pending deliveries.
  - **BST** for `(origin, destination)` audit trail.
  - **Time-sorted index** (parallel lists) for efficient range queries.
  - **Undo stack** of inverse operations for clean rollbacks.
- **Run:**
  - `python3 graph_schedule5.py schedule5.txt`

### 4. `schedule5.txt`
- Example **input command file** for the scheduler (editable) and not hard coded.

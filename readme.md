# Module 3 — Delivery Scheduler with History Tracking (Group 5)

This module contains three programs:
1) a **graph builder** that converts an edge list into a JSON adjacency list,  
2) a **graph query** tool (print, neighbors, shortest path), and  
3) a **delivery scheduler** that maintains an auditable history with undo and time-range queries.

All programs are self-contained and require only Python 3.8+.

---

## Project Files

### 1. `graph_builder5.py`
Builds a **graph adjacency list** and writes it to `graph.json`.

- **Behavior**
  - Reads a plain edge list file where each line is: `CityA CityB weight`.
  - Treats edges as **undirected** (adds both directions).
  - Produces a deterministic adjacency list ordered by destination then weight.
- **Usage**
  - `python3 graph_builder5.py routes5.txt graph.json`
- **Input**
  - Lines beginning with `#` or blank lines are ignored.
  - Example:
    ```
    City1 City2 10
    City2 City3 8
    City3 City4 5
    City1 City4 20
    ```
- **Output**
  - Writes `{"graph": { ... }}` to `graph.json`, e.g.:
    ```json
    {
      "graph": {
        "City1": [{"to":"City2","w":10.0},{"to":"City4","w":20.0}],
        "City2": [{"to":"City1","w":10.0},{"to":"City3","w":8.0}],
        ...
      }
    }
    ```

---

### 2. `graph_query5.py`
Provides simple queries over a `graph.json` produced by the builder.

- **Commands**
  - `print` — dump the full graph JSON.
  - `neighbors <City>` — list outgoing edges from `<City>`.
  - `shortest <CityA> <CityB>` — compute path and total weight (Dijkstra).
- **Usage**
  - `python3 graph_query5.py graph.json print`
  - `python3 graph_query5.py graph.json neighbors City2`
  - `python3 graph_query5.py graph.json shortest City1 City4`
- **Notes**
  - If either endpoint is missing, `shortest` prints `No path`.

---

### 3. `graph_schedule.py`
Implements a **delivery scheduler** with an auditable history, undo, and time-range queries.

- **Accepted Commands** (one per line, case-insensitive)
  - `SCHEDULE DELIVERY <Origin>-><Destination> at HH:MM`  
    Enqueue a delivery in FIFO order.
  - `RECORD_HISTORY`  
    Dequeue the **oldest** scheduled delivery and record it as completed.
  - `UNDO_LAST`  
    Revert the most recent action (either a `SCHEDULE` or a `RECORD_HISTORY`).
  - `QUERY_HISTORY BETWEEN HH:MM HH:MM`  
    List completed deliveries whose times fall in the inclusive window.
- **Data Structures**
  - **Queue** (`collections.deque`) for pending deliveries.
  - **BST** (`DelHistory`) storing `(origin, destination)` for audit/traversal.
  - **Time index**: parallel **sorted lists** (`hist_times`, `hist_entries`) in minutes since midnight for efficient range queries.
  - **Undo stack**: LIFO of inverse operations for both scheduling and recording.
- **Usage**
  - `python3 graph_schedule.py input.txt`  
    (If no filename is provided, it defaults to `input.txt`.)
- **Command File Notes**
  - `HH:MM` is 24-hour time; `9:00` and `09:00` are both accepted.
  - Lines starting with `#` are ignored.

**Example input**
SCHEDULE DELIVERY City1->City4 at 9:00
SCHEDULE DELIVERY City2->City3 at 9:15
RECORD_HISTORY
UNDO_LAST
QUERY_HISTORY BETWEEN 9:00 9:30

**Example output**
Scheduled: City1->City4 at 9:00
Scheduled: City2->City3 at 9:15
Recorded history
Undid last action
History between 9:00 and 9:30:

City1->City4 at 9:00

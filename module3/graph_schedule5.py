import sys, re, queue
from collections import deque
from bisect import bisect_left, bisect_right, bisect_right as br

command_queue = queue.Queue()
cmd_file = sys.argv[1] if len(sys.argv) >= 2 else "input.txt"
with open(cmd_file, "r", encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        if s:
            command_queue.put(s)

class DelRouteNode:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.left = None
        self.right = None
    def __str__(self):
        return f"{self.origin} -> {self.destination}"

class DelHistory:
    def __init__(self):
        self.root = None
    def _compare(self, a, b):
        return (a.origin + a.destination) < (b.origin + b.destination)
    def insert(self, origin, destination):
        n = DelRouteNode(origin, destination)
        if not self.root:
            self.root = n
        else:
            self._insert_recursive(self.root, n)
    def _insert_recursive(self, cur, n):
        if self._compare(n, cur):
            if cur.left: self._insert_recursive(cur.left, n)
            else: cur.left = n
        else:
            if cur.right: self._insert_recursive(cur.right, n)
            else: cur.right = n
    def delete(self, origin, destination):
        target = DelRouteNode(origin, destination)
        self.root = self._delete_rec(self.root, target)
    def _delete_rec(self, node, target):
        if not node: return None
        if self._compare(target, node):
            node.left = self._delete_rec(node.left, target)
        elif self._compare(node, target):
            node.right = self._delete_rec(node.right, target)
        else:
            if not node.left: return node.right
            if not node.right: return node.left
            s = node.right
            while s.left: s = s.left
            node.origin, node.destination = s.origin, s.destination
            node.right = self._delete_rec(node.right, s)
        return node

def DelRecords(history_tree, origin, destination, status):
    if status.lower() == "completed":
        history_tree.insert(origin, destination)

SCHED_RE = re.compile(r"^SCHEDULE\s+DELIVERY\s+([A-Za-z0-9_ -]+)->([A-Za-z0-9_ -]+)\s+at\s+(\d{1,2}:\d{2})\s*$", re.I)
RECORD   = "RECORD_HISTORY"
UNDO_CMD = "UNDO_LAST"
QH_RE    = re.compile(r"^QUERY_HISTORY\s+BETWEEN\s+(\d{1,2}:\d{2})\s+(\d{1,2}:\d{2})\s*$", re.I)
TIME_RE  = re.compile(r"^(\d{1,2}):(\d{2})$")

def parse_time(t):
    m = TIME_RE.match(t.strip())
    if not m: raise ValueError(f"Invalid time: {t!r}")
    h, m2 = int(m.group(1)), int(m.group(2))
    if not (0 <= h < 24 and 0 <= m2 < 60): raise ValueError(f"Invalid time: {t!r}")
    return h*60 + m2

pending = deque()              # (origin, destination, time_str)
history_bst = DelHistory()
hist_times, hist_entries = [], []  # time-index for range queries
undo_stack = []

while not command_queue.empty():
    line = command_queue.get()

    m = SCHED_RE.match(line)
    if m:
        o, d, t = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        task = (o, d, t)
        pending.append(task)
        print(f"Scheduled: {o}->{d} at {t}")
        def _undo_schedule(task=task):
            for i in range(len(pending)-1, -1, -1):
                if pending[i] == task:
                    del pending[i]; break
        undo_stack.append(_undo_schedule)
        continue

    if line.upper() == RECORD:
        if not pending:
            print("No pending deliveries to record")
        else:
            o, d, t = pending.popleft()
            DelRecords(history_bst, o, d, "completed")
            tm = parse_time(t)
            idx = br(hist_times, tm)
            hist_times.insert(idx, tm)
            hist_entries.insert(idx, f"{o}->{d} at {t}")
            print("Recorded history")
            def _undo_record(o=o, d=d, t=t, tm=tm):
                history_bst.delete(o, d)
                for j in range(len(hist_times)-1, -1, -1):
                    if hist_times[j] == tm and hist_entries[j] == f"{o}->{d} at {t}":
                        del hist_times[j]; del hist_entries[j]; break
                pending.appendleft((o, d, t))
            undo_stack.append(_undo_record)
        continue

    if line.upper() == UNDO_CMD:
        if not undo_stack:
            print("Nothing to undo")
        else:
            undo_stack.pop()()
            print("Undid last action")
        continue

    m2 = QH_RE.match(line)
    if m2:
        t1, t2 = m2.group(1), m2.group(2)
        a, b = parse_time(t1), parse_time(t2)
        if a > b: a, b = b, a
        i, j = bisect_left(hist_times, a), bisect_right(hist_times, b)
        print(f"History between {t1} and {t2}:")
        if i >= j:
            print("- (none)")
        else:
            for k in range(i, j):
                print(f"- {hist_entries[k]}")
        continue

    print(line)
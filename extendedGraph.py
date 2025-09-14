# ExtendedGraph.py
class Graph:
    def __init__(self):
        self.city_dict = {}        # {city: {neighbor: base_weight}}
        self.traffic_delta = {}    # {(u,v): delta}

    def AddNode(self, city):
        if city not in self.city_dict:
            self.city_dict[city] = {}

    def addEdge(self, city, city2, weight):
        if city not in self.city_dict:
            self.AddNode(city)
        if city2 not in self.city_dict:
            self.AddNode(city2)
        # store as float so traffic deltas mix cleanly
        self.city_dict[city][city2] = float(weight)

    def removeEdge(self, city, city2):
        if city in self.city_dict and city2 in self.city_dict[city]:
            del self.city_dict[city][city2]

    def removeNode(self, city):
        if city in self.city_dict:
            del self.city_dict[city]
        for c in list(self.city_dict.keys()):
            if city in self.city_dict[c]:
                del self.city_dict[c][city]

    def to_adjacency_list(self, effective=False):
        lines = []
        for city, nbrs in self.city_dict.items():
            if nbrs:
                if effective:
                    roads = ", ".join(f"{nbr}({self.effective_weight(city, nbr)})" for nbr in nbrs)
                else:
                    roads = ", ".join(f"{nbr}({nbrs[nbr]})" for nbr in nbrs)
                lines.append(f"{city}: {roads}")
            else:
                lines.append(f"{city}:")
        return "\n".join(lines)

    # --- traffic support ---
    def set_traffic_report(self, u, v, delta):
        """Apply +delta (can be negative). Returns True if edge exists, False otherwise."""
        if u in self.city_dict and v in self.city_dict[u]:
            self.traffic_delta[(u, v)] = self.traffic_delta.get((u, v), 0.0) + float(delta)
            return True
        return False

    def clear_traffic(self, u, v):
        self.traffic_delta.pop((u, v), None)

    def clear_all_traffic(self):
        self.traffic_delta.clear()

    def base_weight(self, u, v):
        return self.city_dict[u][v]

    def effective_weight(self, u, v):
        return self.city_dict[u][v] + self.traffic_delta.get((u, v), 0.0)

    # --- required by algorithms ---
    def neighbors(self, u):
        """Return list of (neighbor, effective_weight)."""
        if u not in self.city_dict:
            return []
        return [(v, self.effective_weight(u, v)) for v in self.city_dict[u]]

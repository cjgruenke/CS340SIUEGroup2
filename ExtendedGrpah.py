class Graph():

    def __init__(self):
        self.city_dict = {}
        self.traffic_delta = {}

    def AddNode(self, city) :
        if city not in self.city_dict: # checks if city is in dict, if not add it otherwise throw "city already exists"
            self.city_dict[city] = {}
        else: 
            print(city, "already exists")

    def addEdge(self, city, city2, weight) :
        if city not in self.city_dict :       # checks if both citys that need to be connected are in dict, then adds whichever needs to be added 
            self.AddNode(city)
        if city2 not in self.city_dict :
            self.AddNode(city2) 
        self.city_dict[city][city2] = weight  # makes city two another dict and adds the weight to it

    def removeEdge(self, city, city2):                               
        if city in self.city_dict and city2 in self.city_dict[city]:      #Remove the road from city → city2 if it exists"
            del self.city_dict[city][city2]
        else:
            print(f"No edge from {city} to {city2} exists.")

    def removeNode(self, city) :    
        del self.city_dict[city]        # removes the first mention of the city in the dict

        for c in self.city_dict:              # This makes sure that the city thats deleted gets deleted from any roads that are connected to it.
            if city in self.city_dict[c]:
                del self.city_dict[c][city]

    def to_adjacency_list(self):
        result = []
        for city, neighbors in self.city_dict.items():
            if neighbors:
                roads = ", ".join(f"{nbr}({w})" for nbr, w in neighbors.items())
                result.append(f"{city}: {roads}")
            else:
                result.append(f"{city}:")
        return "\n".join(result)


    def set_traffic_report(self, u, v, delta):
            """Apply a traffic report like +3/-2 to edge u->v (additive)."""
            if u in self.city_dict and v in self.city_dict[u]:                       
                self.traffic_delta[(u, v)] = self.traffic_delta.get((u, v), 0.0) + float(delta) 
            else:
                print(f"Ignored TRAFFIC_REPORT for non-existent edge {u}->{v}")

    def clear_traffic(self, u, v):
        """Clear any traffic adjustment for edge u->v."""
        self.traffic_delta.pop((u, v), None)

    def clear_all_traffic(self):
        """Clear all traffic adjustments."""
        self.traffic_delta.clear()

    def base_weight(self, u, v):
        """Return the original (static) weight; raises KeyError if missing."""
        return self.city_dict[u][v]

    def effective_weight(self, u, v):
        """Return weight with traffic: base + delta (delta defaults to 0)."""
        return self.city_dict[u][v] + self.traffic_delta.get((u, v), 0.0)

g = Graph()

g.AddNode("Columbia")
g.addEdge("Columbia", "Sedalia", 5)
g.AddNode("Moberly")
g.addEdge("Moberly", "Columbia", 10)
g.AddNode("Edwardsville")

print("Before:", g.city_dict, "\n")

g.set_traffic_report("Columbia", "Sedalia", +2) #Traffic change

print("After:", g.traffic_delta)


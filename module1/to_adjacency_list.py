def to_adjacency_list(self):
        result = []
        for city, neighbors in self.city_dict.items():
            if neighbors:
                roads = ", ".join(f"{nbr}({w})" for nbr, w in neighbors.items())
                result.append(f"{city}: {roads}")
            else:
                result.append(f"{city}:")
        return "\n".join(result)
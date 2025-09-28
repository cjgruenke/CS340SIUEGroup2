from graph1 import Graph

class GraphParser:
    def __init__(self, filepath): 
    # Initialize with the path to the input file for us to read from
        self.filepath = filepath

    def load_graph(self): 
        # Constructs a graph object from the input file
        g = Graph()
        try:
            with open(self.filepath, "r") as f:
             # Open the file and read all lines, remove blank lines and comments
                lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                
            # Check that the file has both the CITIES and ROADS
            if "CITIES" not in lines or "ROADS" not in lines:
                print("Error: File must contain both 'CITIES' and 'ROADS' sections")
                return g # return empty graph

            try:
                cities_index = lines.index("CITIES")
                roads_index = lines.index("ROADS")
            except ValueError:
                print("Error: Missing CITIES or ROADS section headers")
                return g

            # Cities (Nodes)
            for city in lines[cities_index + 1 : roads_index]:
                g.AddNode(city)

            # Roads (Edges)
            for lineno, road_line in enumerate(lines[roads_index + 1 :], start=roads_index + 2):
                parts = road_line.split()
                if len(parts) != 3:
                    print(f"Error on line {lineno}: expected 'City1 City2 weight', got '{road_line}'")
                    continue

                city1, city2, weight_str = parts
                try:
                    #Convert weight to integer and add edge
                    weight = int(weight_str)
                    g.addEdge(city1, city2, weight)
                    # Error handling for non-integer weights
                except ValueError:
                    print(f"Error on line {lineno}: weight '{weight_str}' is not an integer")

        except FileNotFoundError:
            # If the file doesn't exist, print an error message
            print(f"File '{self.filepath}' not found.")
            # If file not found, return empty graph
        except Exception as e:
            print(f"Unexpected error while reading file: {e}")
        #Return the graph
        return g  
    
if __name__ == "__main__":
    parser = GraphParser("input.txt") 
    graph = parser.load_graph()
    print(graph.to_adjacency_list())

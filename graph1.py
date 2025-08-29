class Graph():

    def __init__(self):
        self.city_dict = {}

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

g = Graph()

g.AddNode("Columbia")
g.addEdge("Columbia", "sedalia", 5)
g.AddNode("Moberly")
g.addEdge("Moberly", "Columbia", 10)
g.AddNode("Edwardsville")

print("Before:", g.city_dict, "\n")

g.removeEdge("Columbia", "sedalia")

print("After:", g.city_dict)

GeneratorExit
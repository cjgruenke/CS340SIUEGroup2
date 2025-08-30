from abc import ABC, abstractmethod

class reports(ABC):  
    @abstractmethod
    def cityreport(self, city): # will be able to grab total reports for any city
        pass

    @abstractmethod
    def trafficreport(self, city, city2): # Will grab reprorts for roads leading into cities
        pass

class deliveries(ABC):
    @abstractmethod
    def getdeliveries(self, city, city2): # Will show all deliveries between two cities
        pass

    @abstractmethod
    def compdeliveries(self, city, city2): # Will show all completed deliveries between two cities
        pass

    @abstractmethod
    def incompdeliveries(self, city, city2): # Will show all incomplete deliveries between two cities
        pass

    @abstractmethod
    def addelivery(self, city, city2): # Will add a delivery to the schedule
        pass

class undo(ABC):
    @abstractmethod
    def removedelivery(self, city, city2): # Will remove a delivery from the schedule for two cities
        pass

class routs(ABC):
    @abstractmethod
    def cityrouts(self, city): # Will show all routes to get to a city
        pass

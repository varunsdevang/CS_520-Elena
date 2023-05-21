import osmnx as ox
from a_star import A_Star
from djikistra import Djikistra

class AlgorithmSelector:
    def __init__(self,start,end):
		self.start = start
		self.end = end
		self.get_nodes()
        self.a_star = A_Star()
    
    def get_nodes(self):
        start_lat,start_lng = ox.geocode(self.start)
        end_lat,end_lng = ox.geocode(self.end)
        self.starting_node = ox.nearest_nodes(self.graph,start_lng,start_lat)
        self.ending_node = ox.nearest_nodes(self.graph,end_lng,end_lat)

    def optimal_route(self):

    

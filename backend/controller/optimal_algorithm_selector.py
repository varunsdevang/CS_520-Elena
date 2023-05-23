import osmnx as ox
from a_star import A_Star
from djikistra import Djikistra
from utils import UtilsController
import pickle as pkl

class AlgorithmSelector:
    def __init__(self,G,start,end,elevation_gain, percent_gain):
        self.start = start
        self.end = end
        self.graph = G
        self.elevation_gain = elevation_gain
        self.percent_gain = percent_gain
        self.get_nodes()
        self.utils = UtilsController()

        # initialize both A_star and Djikistra modules so that we can select the best route
        self.a_star = A_Star(G,self.starting_node,self.ending_node)
        self.djikistra = Djikistra(G,self.starting_node,self.ending_node)
    
    def get_nodes(self):
        # get nearest nodes on the graph from the start and destination address
        start_lat,start_lng = ox.geocode(self.start)
        end_lat,end_lng = ox.geocode(self.end)
        self.starting_node = ox.nearest_nodes(self.graph,start_lng,start_lat)
        self.ending_node = ox.nearest_nodes(self.graph,end_lng,end_lat)

    def optimal_route(self):
        # generating path from both a_star and djikistra
        a_star_path = self.a_star.shortest_path()
        # calculcating elevation of both the paths
        a_star_elevation = self.utils.calculate_path_elevation(self.graph, a_star_path)
        optimal_path = self.djikistra.path_with_elevation_gain(self.elevation_gain,self.percent_gain)
        print("with elevation :",optimal_path)
        djikistra_elevation = self.utils.calculate_path_elevation(self.graph, optimal_path)
        # calculating elevation gain with respect to reference path
        elevation_gain = djikistra_elevation
        return optimal_path, elevation_gain







    

import osmnx as ox
from a_star import A_Star
from djikistra import Djikistra
from utils import UtilsController
import pickle as pkl

class AlgorithmSelector:
    def __init__(self,G,start,end,elevation_gain):
        self.start = start
        self.end = end
        self.graph = G
        self.elevation_gain = elevation_gain
        self.get_nodes()
        self.utils = UtilsController()
        self.a_star = A_Star(G,self.starting_node,self.ending_node)
        self.djikistra = Djikistra(G,self.starting_node,self.ending_node)
    
    def get_nodes(self):
        start_lat,start_lng = ox.geocode(self.start)
        end_lat,end_lng = ox.geocode(self.end)
        self.starting_node = ox.nearest_nodes(self.graph,start_lng,start_lat)
        self.ending_node = ox.nearest_nodes(self.graph,end_lng,end_lat)

    def optimal_route(self):
        a_star_path = self.a_star.shortest_path()
        a_star_elevation = self.utils.calculate_path_elevation_gain(self.graph, a_star_path)
        djikistra_path = self.djikistra.path_with_elevation_gain(self.elevation_gain,125)
        djikistra_elevation = self.utils.calculate_path_elevation_gain(self.graph, djikistra_path)
        print(a_star_elevation, djikistra_elevation)
        if self.elevation_gain=="max":
            if djikistra_elevation>a_star_elevation:
                return djikistra_path,djikistra_elevation
            else:
                return a_star_path,a_star_elevation
        else:
            if djikistra_elevation>a_star_elevation:
                return a_star_path,a_star_elevation
            else:
                return djikistra_path,djikistra_elevation

# start = "147 Brittany Manor Drive, Amherst, Massachusetts, USA"
# end = "650 N Pleasant St, Amherst, Massachusetts, USA"
# #midpoint_lat,midpoint_lng = ox.geocode(start)
# # start_lat,start_lng = ox.geocode(start)
# # end_lat,end_lng = ox.geocode(end)
# G = pkl.load(open("../model/graphs/Amherst_Massachusetts.pkl","rb"))#ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=10000)

# a = AlgorithmSelector(G,start,end,"max")
# path = a.optimal_route()

# print("Shortest path:", path)







    

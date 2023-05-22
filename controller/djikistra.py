import osmnx as ox
import heapq
import pickle as pkl
from utils import UtilsController

class Djikistra:
	def __init__(self,G,starting_node,ending_node):
		self.graph = G
		self.starting_node = starting_node
		self.ending_node = ending_node
	
	def elevation_diff(self,node_a,node_b):
		return abs(self.graph.nodes[node_b]["elevation"] - self.graph.nodes[node_a]["elevation"])

	def return_path(self,closest_nodes):
		path = [self.ending_node]
		curr_node = self.ending_node
		while(curr_node!=self.starting_node):
			curr_node = closest_nodes[curr_node]
			path.insert(0,curr_node)
		return path

	def shortest_path(self):
		nodes = []
		heapq.heappush(nodes, (0,self.starting_node))
		closest_node_record = {}
		closest_node_record[self.starting_node] = None
        
		cost_record = {}
		cost_record[self.starting_node] = 0

		while nodes:
			cost, node = heapq.heappop(nodes)
			if (node == self.ending_node):
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				cost_a_b = path_info["length"]
				if ((end_b not in cost_record) or (cost_record[end_b] > cost_record[end_a] + cost_a_b)):
					cost_record[end_b] = cost_record[end_a] + cost_a_b
					closest_node_record[end_b] = end_a
					heapq.heappush(nodes, (cost_record[end_b], end_b))
		path = self.return_path(closest_node_record)
		return path, cost_record
	

	def elevation_comparison_condition(self, current, updated, condition):
		if condition=="max":
			if updated>current:
				return True
			else:
				return False
		else:
			if updated>=current:
				return False
			else:
				return True
	
	def path_with_elevation_gain(self, elevation_condition, percent_inc_param):
		
		shortest_path, shortest_path_weight_record = self.shortest_path()
		shortest_path_length = utils.get_path_length(self.graph,shortest_path)

		nodes = []
		heapq.heappush(nodes, (0,self.starting_node))
		closest_node_record = {}
		closest_node_record[self.starting_node] = None
        
		cost_record = {}
		cost_record[self.starting_node] = 0

		elevation_record = {}
		elevation_record[self.starting_node] = 0

		while nodes:
			elevation, node = heapq.heappop(nodes)
			if (node == self.ending_node):
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				elevation_a_b = self.elevation_diff(end_a, end_b)
				new_route_elevation = elevation_record[end_a] + elevation_a_b 
				if ((end_b not in elevation_record) or self.elevation_comparison_condition(elevation_record[end_b],new_route_elevation,elevation_condition)):
					elevation_record[end_b] = new_route_elevation
					closest_node_record[end_b] = end_a
					if elevation_condition=="max":
						heapq.heappush(nodes, (-1*elevation_record[end_b], end_b))
					else:
						heapq.heappush(nodes, (elevation_record[end_b], end_b))

		elevation_path = self.return_path(closest_node_record)
		elevation_path_length = self.get_path_length(elevation_path)

		#print(shortest_path_length, elevation_path_length)
		if(elevation_path_length<percent_inc_param*shortest_path_length/100):
			return elevation_path
		return shortest_path
	


# start = "115 Brittany Manor Dr, Amherst, Massachusetts, USA"
# end = "650 N Pleasant St, Amherst, Massachusetts, USA"
# #end = "151 Brittany Manor Dr, Amherst, Massachusetts, USA"
# # midpoint_lat,midpoint_lng = ox.geocode(start)
# # G = ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=10000)
# G = pkl.load(open("../model/graphs/Amherst_Massachusetts.pkl","rb"))
# d = Djikistra(G,start,end)
# print(d.starting_node,d.ending_node)
# print(d.path_with_elevation_gain("min",125))
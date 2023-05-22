import osmnx as ox
import heapq
import pickle as pkl
from utils import UtilsController

class Djikistra:
	def __init__(self,G,starting_node,ending_node):
		self.graph = G
		self.starting_node = starting_node
		self.ending_node = ending_node
		self.utils = UtilsController()
	
	def elevation_diff(self,node_a,node_b):
		# get elevation gain
		return self.graph.nodes[node_b]["elevation"] - self.graph.nodes[node_a]["elevation"]

	def shortest_path(self):
		nodes = []
		heapq.heappush(nodes, (0,self.starting_node))

		# storing the nearest node to reach the current node
		closest_node_record = {}
		closest_node_record[self.starting_node] = None
        
		# storing the minimum cost(length) to reach the current node
		cost_record = {}
		cost_record[self.starting_node] = 0

		while nodes:
			cost, node = heapq.heappop(nodes)
			if (node == self.ending_node):
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				cost_a_b = path_info["length"]
				# we need to update only if the new way to reach the current node has lesser cost than already stored
				if ((end_b not in cost_record) or (cost_record[end_b] > cost_record[end_a] + cost_a_b)):
					cost_record[end_b] = cost_record[end_a] + cost_a_b
					closest_node_record[end_b] = end_a
					heapq.heappush(nodes, (cost_record[end_b], end_b))

		# constructing path from the nearest node record
		path = self.utils.return_path(closest_node_record)
		return path, cost_record
	

	def elevation_comparison_condition(self, current, updated, condition):
		# boolean comparison condition according to the elevation gain condition set by user
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
		
		# getting the shortest path length record to be used as a reference
		shortest_path, shortest_path_weight_record = self.shortest_path()
		shortest_path_length = self.utils.get_path_length(self.graph,shortest_path)
		print(shortest_path_length)

		# running djikistra again but now with elevation as base condition
		nodes = []
		heapq.heappush(nodes, (0,self.starting_node))
		closest_node_record = {}
		closest_node_record[self.starting_node] = None
        
		# storing cost_record at the same time
		cost_record = {}
		cost_record[self.starting_node] = 0

		elevation_record = {}
		elevation_record[self.starting_node] = 0

		while nodes:
			elevation, node = heapq.heappop(nodes)
			# if the cost to traverse the node with the current path is more expensive than the percentage constraint condition remove it from the path
			if cost_record[node]>(percent_inc_param*shortest_path_length)/100:
				del closest_node_record[node]
				continue
			# if we reach the ending node, we have found the path
			if (node == self.ending_node):
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				# calculate updated elevation
				elevation_a_b = self.elevation_diff(end_a, end_b)
				new_route_elevation = elevation_record[end_a] + elevation_a_b 

				# we should update the node details only if the new elevation is min/max compared to the already stored path, based on the user's constraint
				if ((end_b not in elevation_record) or self.elevation_comparison_condition(elevation_record[end_b],new_route_elevation,elevation_condition)):
					updated_length = cost_record[end_a] + path_info["length"]
					# we also need to check for the distance constraint
					if(end_b in shortest_path_weight_record and updated_length<percent_inc_param*shortest_path_weight_record[end_b]/100):
						elevation_record[end_b] = new_route_elevation
						closest_node_record[end_b] = end_a
						cost_record[end_b] = updated_length
						if elevation_condition=="max":
							heapq.heappush(nodes, (-1*elevation_record[end_b], end_b))
						else:
							heapq.heappush(nodes, (elevation_record[end_b], end_b))
					# only if both are satisfied, push the neighbours 

		elevation_path = self.utilsreturn_path(closest_node_record)
		elevation_path_length = self.utils.get_path_length(self.graph,elevation_path)
		print(elevation_path_length)

		# return elevation_path only if it satisfies the percent_gain constraint, if not the case, default to shortest_path
		if(elevation_path_length<percent_inc_param*shortest_path_length/100):
			return elevation_path
		return shortest_path
	


# start = "115 Brittany Manor Dr, Amherst, Massachusetts, USA"
# end = "650 N Pleasant St, Amherst, Massachusetts, USA"
# #end = "151 Brittany Manor Dr, Amherst, Massachusetts, USA"
# # # midpoint_lat,midpoint_lng = ox.geocode(start)
# # # G = ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=10000)
# G = pkl.load(open("../model/graphs/Amherst_Massachusetts_drive.pkl","rb"))
# node1 = ox.nearest_nodes(G,ox.geocode(start)[1],ox.geocode(start)[0])
# node2 = ox.nearest_nodes(G,ox.geocode(end)[1],ox.geocode(end)[0])
# d = Djikistra(G,node1,node2)
# print(d.starting_node,d.ending_node)
# print(d.path_with_elevation_gain("min",100.5))
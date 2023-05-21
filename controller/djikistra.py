import osmnx as ox
import heapq

class Djikistra:
	def __init__(self,G,start,end):
		self.graph = G
		self.start = start
		self.end = end
		self.get_nodes()

	def get_nodes(self):
		start_lat,start_lng = ox.geocode(self.start)
		end_lat,end_lng = ox.geocode(self.end)
		self.starting_node = ox.nearest_nodes(self.graph,start_lng,start_lat)
		self.ending_node = ox.nearest_nodes(self.graph,end_lng,end_lat)

	def return_path(self,closest_nodes):
		path = [self.ending_node]
		curr_node = self.ending_node
		while(curr_node!=self.starting_node):
			print(curr_node)
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
				print(self.ending_node)
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				cost_a_b = path_info["length"]
				if ((end_b not in cost_record) or (cost_record[end_b] > cost_record[end_a] + cost_a_b)):
					cost_record[end_b] = cost_record[end_a] + cost_a_b
					closest_node_record[end_b] = end_a
					heapq.heappush(nodes, (cost_record[end_b], end_b))
		#print(closest_node_record)
		path = self.return_path(closest_node_record)
		return path

# start = "360 Huntington Ave, Boston, Massachusetts, USA"
# end = "650 N Pleasant St, Amherst, Massachusetts, USA"
# midpoint_lat,midpoint_lng = ox.geocode(start)
# G = ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=10000)
# d = Djikistra(G,start,end)
# print(d.shortest_path())
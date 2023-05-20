import osmnx as ox
import heapq

class Djikistra:
	def __init__(self,G,start,end):
		self.graph = G
		self.start = start
		self.end = end

	def return_path(self,closest_nodes):
		path = [self.end]
		curr_node = self.end
		while(curr_node!=self.start):
			curr_node = closest_nodes[curr_node]
			path.insert(0,curr_node)
		return path

	def shortest_path(self):
		nodes = []
		heapq.heappush(nodes, (0,self.start))
		closest_node_record = {}
		closest_node_record[self.start] = None
        
		cost_record = {}
		cost_record[self.start] = 0

		while nodes:
			cost, node = heapq.heappop(nodes)
			if (node == self.end):
				break

			for end_a,end_b,path_info in self.graph.edges(node,data=True):
				cost_a_b = path_info["length"]
				if ((end_b not in cost_record) or (cost_record[end_b] > cost_record[end_a] + cost_a_b)):
					cost_record[end_b] = cost_record[end_a] + cost_a_b
					closest_node_record[end_b] = end_a
					heapq.heappush(nodes, (cost_record[end_b], end_b))

		path = self.return_path(closest_node_record)
		print(path)

G = ox.graph_from_xml(filepath='amherst.osm')
d = Djikistra(G,66730551,6371920027)
d.shortest_path()
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath("."))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import osmnx as ox
import networkx as nx
import heapq
import pickle as pkl

class A_Star:
    def __init__(self,G,starting_node,ending_node):
        self.graph = G
        self.starting_node = starting_node
        self.ending_node = ending_node
        #self.utils = UtilsController()

    def heuristic_distance(self, node1, node2):
        # for f score generating shortest distance between two points
        return nx.shortest_path_length(self.graph, node1, node2, weight="length")
    
    def return_path(self,closest_nodes):
		# generate path by backtracking
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

        # initializing g-scores and f-scores
        g_scores = {self.starting_node: 0}  
        f_scores = {self.starting_node: self.heuristic_distance(self.starting_node, self.ending_node)}

        while nodes:
            # getting the least cost node to start route computation
            cost, node = heapq.heappop(nodes)
            if (node == self.ending_node):
                break

            for end_a,end_b,path_info in self.graph.edges(node,data=True):
                cost_a_b = path_info["length"]
                # updating the cost of the node only if the new route is less expensive comparing both g and f_score
                if ((end_b not in g_scores) or (g_scores[end_b] > g_scores[end_a] + cost_a_b)):
                    g_scores[end_b] = g_scores[end_a] + cost_a_b
                    f_scores[end_b] = g_scores[end_b] + self.heuristic_distance(end_b, self.ending_node)
                    closest_node_record[end_b] = end_a
                    # adding the node back to list of nodes to traverse
                    heapq.heappush(nodes, (f_scores[end_b], end_b))

        path = self.return_path(closest_node_record)
        return path


# start = "147 Brittany Manor Drive, Amherst, Massachusetts, USA"
# end = "650 N Pleasant St, Amherst, Massachusetts, USA"
# #midpoint_lat,midpoint_lng = ox.geocode(start)
# # start_lat,start_lng = ox.geocode(start)
# # end_lat,end_lng = ox.geocode(end)
# G = pkl.load(open("../model/graphs/Amherst_Massachusetts.pkl","rb"))#ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=10000)

# # Find the nearest nodes in the graph to the origin and destination
# # origin_node = ox.distance.nearest_nodes(G, start_lng,start_lat)
# # destination_node = ox.distance.nearest_nodes(G, end_lng,end_lat)
# # print(origin_node,destination_node)
# # Run A* algorithm to find the shortest path
# a = A_Star(G,start,end)
# path = a.shortest_path()

# print("Shortest path:", path)

from flask import jsonify

class UtilsController:

    def convert_nodes_to_coordinates(self,graph,path):
        # accumalate lat and long of each node in the path
        coordinates = []
        for node in path:
            lat = graph.nodes[node]['y']
            lng = graph.nodes[node]['x']
            coordinates.append({"lat":lat,"lng":lng})
        return coordinates

    def get_path_length(self,graph,path):
        # calculate length of the path by checking each edge in the graph
        node_pointer = 1
        prev_node_pointer = 0
        length = graph.edges[path[prev_node_pointer],path[node_pointer],0]["length"]
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            length+=graph.edges[path[prev_node_pointer],path[node_pointer],0]["length"]
        return length

    def calculate_path_elevation(self,graph, path):
        # calculate elevation of the path by comparing each pair of nodes in the graph consequtively and summing them up
        nodes = list(graph.nodes)
        node_pointer = 1
        prev_node_pointer = 0
        total_elevation = abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            total_elevation+= abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
        return total_elevation

    def return_path(self,closest_nodes):
		# generate path by backtracking
		path = [self.ending_node]
		curr_node = self.ending_node
		while(curr_node!=self.starting_node):
			curr_node = closest_nodes[curr_node]
			path.insert(0,curr_node)
		return path

    def get_path_time(self,graph,path):
        node_pointer = 1
        prev_node_pointer = 0
        travel_time = graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            travel_time+=graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
        return travel_time
    
    def return_error_response(self, error_message):
        return jsonify({"errorMessage":error_message}),400

    
    


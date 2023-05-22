class UtilsController:

    def convert_nodes_to_coordinates(self,graph,path):
        coordinates = []
        for node in path:
            lat = graph.nodes[node]['y']
            lng = graph.nodes[node]['x']
            coordinates.append({"lat":lat,"lng":lng})
        return coordinates

    def get_path_length(self,graph,path):
        node_pointer = 1
        prev_node_pointer = 0
        length = graph.edges[path[prev_node_pointer],path[node_pointer],0]["length"]
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            length+=graph.edges[path[prev_node_pointer],path[node_pointer],0]["length"]
        return length

    def calculate_path_elevation_gain(self,graph, path):
        nodes = list(graph.nodes)
        node_pointer = 1
        prev_node_pointer = 0
        total_elevation = abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            total_elevation+= abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
        return total_elevation

    def get_path_time(self,graph,path):
        node_pointer = 1
        prev_node_pointer = 0
        travel_time = graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
        while(node_pointer<len(path)-1):
            prev_node_pointer+=1
            node_pointer+=1
            travel_time+=graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
        return travel_time

    
    


def convert_nodes_to_coordinates(graph,path):
    coordinates = []
    for node in path:
        lat = graph.nodes[node]['y']
        lng = graph.nodes[node]['x']
        coordinates.append({"lat":lat,"lng":lng})
    return coordinates

def calculate_path_elevation_gain(graph,path):
    nodes = list(graph.nodes)
    node_pointer = 1
    prev_node_pointer = 0
    total_elevation = abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
    while(node_pointer<len(path)-1):
        prev_node_pointer+=1
        node_pointer+=1
        total_elevation+= abs(graph.nodes[nodes[node_pointer]]["elevation"] - graph.nodes[nodes[prev_node_pointer]]["elevation"])
    return total_elevation


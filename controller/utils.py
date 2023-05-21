def convert_nodes_to_coordinates(graph,path):
    coordinates = []
    for node in path:
        lat = graph.nodes[node]['y']
        lng = graph.nodes[node]['x']
        coordinates.append({"lat":lat,"lng":lng})
    return coordinates

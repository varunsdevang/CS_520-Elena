import osmnx as ox

class UtilsForModel:

    def checkForSourceAndDestCity(self,start,end):
        source_address = start.split(",")
        destination_address = end.split(",")
        source_city,source_state = source_address[-3].strip(),source_address[-2].strip()
        dest_city,dest_state = destination_address[-3].strip(),destination_address[-2].strip()
        if(source_state==dest_state):
            state_match = True
            if(source_city==dest_city):
                city_match = True
            else:
                city_match = False
        else:
            state_match = False
        return {"city_match":city_match, "state_match":state_match, "result":{"city":source_city if city_match else None,"state":source_state if state_match else None}}

    def get_path_time(self,path):
            node_pointer = 1
            prev_node_pointer = 0
            travel_time = graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
            while(node_pointer<len(path)-1):
                prev_node_pointer+=1
                node_pointer+=1
                travel_time+=graph.edges[path[prev_node_pointer],path[node_pointer],0]["travel_time"]
            return travel_time

    def calculateTimeTakenForEachEdge(self,graph,mode):
        graph = ox.add_edge_speeds(graph)
        graph = ox.add_edge_travel_times(graph)
        if mode == "walk":
            travel_speed = 4.5
        elif mode == "bike":
            travel_speed = 20
        for u, v, k, data in graph.edges(data=True, keys=True):
            data['travel_time'] = (data['length']/1000) / ((travel_speed if (mode=="walk" or mode=="bike") else data['speed_kph']))
        return graph

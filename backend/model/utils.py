import osmnx as ox
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath("CS_520-Elena"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import constants
import logging

logging.basicConfig(level = logging.INFO)

class UtilsForModel:

    def checkForSourceAndDestCity(self,start,end):
        source_address = start.split(",")
        destination_address = end.split(",")
        try:
            source_city,source_state = source_address[-3].strip(), source_address[-2].strip()
            dest_city,dest_state = destination_address[-3].strip(), destination_address[-2].strip()
        except:
            logging.error("Something went wrong, please enter adresses in the correct format and try again!")
            return {}
        
        city_match = False
        state_match = False
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
        
        # fetching travel speeds for bike and walk modes
        travel_speed = constants.mode_and_speed_mapping[mode]
        
        # for drive mode calculating via osmnx values for each edge
        for u, v, k, data in graph.edges(data=True, keys=True):
            data['travel_time'] = (data['length']/1000) / ((travel_speed if travel_speed else data['speed_kph']))
        return graph

    def return_graph_file(self,args):
        # forming the file name
        file_name = "_".join(args) + constants.extension
        print(file_name)
        # getting absolute directory path
        file_path = os.path.join(constants.graphs_folder,file_name)
        
        # checking if graph exists in cache
        if file_name in constants.graphs_available_in_cache:
            return True, file_path
        else:
            return False, file_path

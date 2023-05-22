import osmnx as ox
import requests
import time
from .utils import *
import pickle as pkl
import os
import logging

graphs = "../model/graphs/"
extension = ".pkl"
request = "https://api.opentopodata.org/v1/aster30m?locations="
logging.basicConfig(level = logging.INFO)

class Graph:
    def __init__(self,start,end,mode):
        self.start_point = start
        self.end_point = end
        self.graph = None
        self.mode = mode
        self.generate_graph()

    def generate_graph(self):
        logging.info(f"Checking for same area (city,state) match for source and destination to plot graph for the entire city")
        area_match = checkForSourceAndDestCity(self.start_point,self.end_point)
        same_area = False
        graphs_available_in_cache = os.listdir(graphs)
        if(area_match["result"]):
            same_area = True
        if same_area:
            city = area_match["city"]
            state = area_match["state"]
            logging.info(f"Source and destination found to be of the same area - {city},{state}")
            location = city+"_"+state
            file_name = location+extension
            if file_name in graphs_available_in_cache:
                logging.info(f"Getting {city} graph from cache!")
                self.graph = pkl.load(open(graphs+file_name,"rb"))
            else:
                logging.info(f"Generating {city} graph and saving it in cache for future use!")
                self.graph = ox.graph_from_place(city+","+state+",USA")
                logging.info(f"Adding elevation data to the graph!")
                self.add_elevation_data()
                pkl.dump(self.graph, open(graphs+file_name, "wb"))
        else:
            midpoint_lat,midpoint_lng = ox.geocode(self.start_point)
            self.graph = ox.graph.graph_from_point((midpoint_lat,midpoint_lng),dist=2000)
    
    def add_elevation_data(self):
        n = len(self.graph.nodes)
        print(n)
        node_ids = list(self.graph.nodes)
        n_calls = (n//100)+1
        graph_data = dict([(node,{"lat":self.graph.nodes[node_ids[node]]['y'],"lng":self.graph.nodes[node_ids[node]]['x']}) for node in range(n)])
        elevation_data = []
        for calls in range(n_calls):
            lower_index = calls*100
            higher_index = min((calls+1)*100,n)
            print(lower_index,higher_index)
            node_coordinates = list(graph_data.items())[lower_index:higher_index]
            str_locations = []
            for node_data in node_coordinates:
                lat,lng = node_data[1].values()
                str_locations.append(str(lat)+","+str(lng))
            request_data = '|'.join(str_locations)
            response = requests.get(request + request_data).json()
            if "results" not in response:
                continue
            elevation_data.extend([x["elevation"] for x in response["results"]])
            time.sleep(1)

        for node in range(n):
            self.graph.nodes[node_ids[node]]["elevation"] = elevation_data[node]
    
    def get_graph(self):
        return self.graph

#G = Graph("Stop & Shop, 440 Russell Street, Hadley, Massachusetts, USA", "650 N Pleasant St, Amherst, Massachusetts, USA","dr")



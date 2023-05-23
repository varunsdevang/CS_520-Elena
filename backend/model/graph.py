import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath("CS_520-Elena"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import osmnx as ox
import requests
import time
from .utils import UtilsForModel
import pickle as pkl
import logging
import constants
from geopy.distance import geodesic
logging.basicConfig(level = logging.INFO)

class Graph:
    def __init__(self,start,end,mode):
        self.start_point = start
        self.end_point = end
        self.graph = None
        self.mode = mode
        self.file_name = ""
        self.utils = UtilsForModel()
        self.generate_graph()
        self.save_graph()

    def generate_graph(self):
        logging.info(f"Checking for same area match for source and destination to plot appropriate graph..")
        area_match = self.utils.checkForSourceAndDestCity(self.start_point,self.end_point)
        
        # error handling
        if not area_match:
            self.graph = None
            return
        
        city_match = area_match["city_match"]
        state_match = area_match["state_match"]
        
        if city_match and state_match:
            # both state and city are the same so it is enough to generate only city graph
            city = area_match["result"]["city"]
            state = area_match["result"]["state"]
            
            logging.info(f"Source and destination found to be of the same area - {city},{state}")
            
            file_exists,self.file_name = self.utils.return_graph_file([city,state,self.mode])
        
            if file_exists:
                try:
                    logging.info(f"Getting {city} graph from cache!")
                    self.graph = pkl.load(open(self.file_name,"rb"))
                except:
                    logging.error("Something went wrong while reading the graph from cache!!")
                    self.graph = None
                    return
            else:
                logging.info(f"Generating {city} graph...")
                
                try:
                    self.graph = ox.graph_from_place(city+","+state+",USA", network_type=self.mode)
                except:
                    logging.error("Something went wrong while generating the graph from osmnx module!!")
                    self.graph = None
                    return
                
                logging.info(f"Adding elevation data to the graph!")
                self.add_elevation_data()
            
            logging.info(f"Adding speed and time of travel for each edge on the graph...")
            self.graph = self.utils.calculateTimeTakenForEachEdge(self.graph,self.mode)
        
        elif state_match:
            state = area_match["result"]["state"]
            logging.info(f"Source and destination found to be of the same state - {state}")
            file_exists, self.file_name = utils.return_graph_file([state,self.mode])
            if file_exists:
                try:
                    logging.info(f"Getting {state} graph from cache!")
                    self.graph = pkl.load(open(self.file_name,"rb"))
                except:
                    logging.error("Something went wrong while reading the graph from cache!!")
                    self.graph = None
                    return
            else:
                logging.info(f"Generating {state} graph...")
                self.file_name = '_'.join([state,self.mode])
                try:
                    self.graph = ox.graph_from_place(state+",USA", network_type=self.mode)
                except:
                    logging.error("Something went wrong while generating the graph from osmnx module!!")
                    self.graph = None
                    return
                
                self.add_elevation_data()

        else:
            start_lat,start_lng = ox.geocode(self.start_point)
            end_lat,end_lng = ox.geocode(self.end_point)

            distance=geodesic((start_lat,start_lng),(end_lat,end_lng)).km
            
            if distance<10:
                logging.info(f"Source and destination aren't in the same area, generating new graph within 10km radius...")
                self.graph = ox.graph.graph_from_point((start_lat,start_lng),dist=10000)
            else:
                logging.error(f"Source and destination aren't in 10km radius of each other, cannot carry out operation!")
                self.graph = None  

    def save_graph(self):
        if self.file_name:
            try:
                pkl.dump(self.graph, open(self.file_name, "wb")) 
            except:
                logging.error("Something went wrong while saving the generated graph!!")
                return
        else:
            logging.warn("Something might have gone wrong while generating the graph...")     
    
    def add_elevation_data(self):
        logging.info(f"Adding elevation data by making calls to OpenTopo...")
        n = len(self.graph.nodes)
        print(n)
        node_ids = list(self.graph.nodes)

        # number of calls per batch to be sent to the api is max 100
        n_calls = (n//100)+1
        # getting graph data as latitude and longitude
        graph_data = dict([(node,{"lat":self.graph.nodes[node_ids[node]]['y'],"lng":self.graph.nodes[node_ids[node]]['x']}) for node in range(n)])
        elevation_data = []
        
        for calls in range(n_calls):    
            # batching the nodes to be sent to the api
            lower_index = calls*100
            higher_index = min((calls+1)*100,n)
            logging.info(f"Making batch calls to OpenTopo from {low} to {high}", lower_index, higher_index)
            node_coordinates = list(graph_data.items())[lower_index:higher_index]
            
            # formatting the coordinates as needed by the api -- lat1,lng1|lat2,lng2|lat3,lng3...
            str_locations = []
            for node_data in node_coordinates:
                lat,lng = node_data[1].values()
                str_locations.append(str(lat)+","+str(lng))
            request_data = '|'.join(str_locations)

            # sending request to the open-topo api
            try:
                response = requests.get(constants.open_topo_request + request_data).json()
            except:
                logging.error(f"Some error occured while making calls to OpenTopo for current batch!!")
                self.graph = None
                return
            
            if "results" not in response:
                continue
            elevation_data.extend([x["elevation"] for x in response["results"]])

            # number of calls allowed is 1 call per second, hence waiting for a second before making the next call
            time.sleep(1)

        # adding elevation data obtained to the graph nodes
        for node in range(n):
            self.graph.nodes[node_ids[node]]["elevation"] = elevation_data[node]
        logging.info(f"Added elevation data to the graph!")
    
    def get_graph(self):
        return self.graph

#G = Graph("147 Brittany Manor Dr, Amherst, Massachusetts, USA", "650 N Pleasant St, Amherst, Massachusetts, USA","fly")



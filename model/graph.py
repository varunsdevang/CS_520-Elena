import osmnx as ox
import requests
import time
from utils import UtilsForModel
import pickle as pkl
import os
import logging

graphs_folder = "../model/graphs/"
extension = ".pkl"
graphs_available_in_cache = os.listdir(graphs_folder)
request = "https://api.opentopodata.org/v1/aster30m?locations="
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
        logging.info(f"Checking for same area (city,state) match for source and destination to plot graph for the entire city")
        area_match = self.utils.checkForSourceAndDestCity(self.start_point,self.end_point)
        city_match = area_match["city_match"]
        state_match = area_match["state_match"]
        
        if city_match and state_match:
            city = area_match["result"]["city"]
            state = area_match["result"]["state"]
            
            logging.info(f"Source and destination found to be of the same area - {city},{state}")
            
            temp_file_name = city+"_"+state+"_"+self.mode+extension
            self.file_name = graphs_folder + temp_file_name
            if temp_file_name in graphs_available_in_cache:
                logging.info(f"Getting {city} graph from cache!")
                self.graph = pkl.load(open(self.file_name,"rb"))
            else:
                logging.info(f"Generating {city} graph...")
                self.graph = ox.graph_from_place(city+","+state+",USA", network_type=self.mode)
                logging.info(f"Adding elevation data to the graph!")
                self.add_elevation_data()
            logging.info(f"Adding speed and time of travel for each edge on the graph...")
            self.graph = self.utils.calculateTimeTakenForEachEdge(self.graph,self.mode)
        
        elif state_match:
            state = area_match["result"]["state"]
            logging.info(f"Source and destination found to be of the same state - {state}")
            temp_file_name = state+"_"+self.mode+extension
            self.file_name = graphs_folder + temp_file_name
            if temp_file_name in graphs_available_in_cache:
                logging.info(f"Getting {state} graph from cache!")
                self.graph = pkl.load(open(graphs+file_name,"rb"))
            else:
                logging.info(f"Generating {state} graph...")
                self.graph = ox.graph_from_place(state+",USA", network_type=self.mode)
                self.add_elevation_data()

        else:
            start_lat,start_lng = ox.geocode(self.start_point)
            end_lat,end_lng = ox.geocode(self.end_point)
            distance = ox.eucledian_distance(start_lat,start_lng,end_lat,end_lng)
            if distance<10000:
                logging.info(f"Source and destination aren't in the same area, generating new graph within 10km radius...")
                self.graph = ox.graph.graph_from_point((start_lat,start_lng),dist=10000)
            else:
                logging.error(f"Source and destination aren't in 10km radius of each other, cannot carry out operation!")
                self.graph = None  

    def save_graph(self):
        pkl.dump(self.graph, open(self.file_name, "wb"))      
    
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
            print(lower_index,higher_index)
            node_coordinates = list(graph_data.items())[lower_index:higher_index]
            
            # formatting the coordinates as needed by the api -- lat1,lng1|lat2,lng2|lat3,lng3...
            str_locations = []
            for node_data in node_coordinates:
                lat,lng = node_data[1].values()
                str_locations.append(str(lat)+","+str(lng))
            request_data = '|'.join(str_locations)

            # sending request to the open-topo api
            response = requests.get(request + request_data).json()
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

G = Graph("147 Brittany Manor Dr, Amherst, Massachusetts, USA", "650 N Pleasant St, Amherst, Massachusetts, USA","drive")



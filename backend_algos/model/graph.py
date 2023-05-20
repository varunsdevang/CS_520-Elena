import osmnx as ox
import requests
import time
import utils
import pickle as pkl

graphs = "./graphs/"
extension = ".pkl"
request = "https://api.opentopodata.org/v1/aster30m?locations="

class Graph:
    def __init__(self,start,end):
        self.start_point = start
        self.end_point = end
        self.cache = {"Amherst_Massachusetts"} #load cache later somehow
        self.graph = None
        self.generate_graph()

    def generate_graph(self):
        area_match = utils.checkForSourceAndDestCity(self.start_point,self.end_point)
        same_area = False
        if(area_match["result"]):
            same_area = True
        if same_area:
            city = area_match["city"]
            state = area_match["state"]
            location = city+"_"+state
            if location in self.cache:
                self.graph = pkl.load(open(graphs+location+extension,"rb"))
            else:
                self.graph = ox.graph_from_place(city+","+state+",USA")
                self.add_elevation_data()
                pkl.dump(self.graph, open(graphs+location+extension, "wb"))
        else:
            midpoint_lat,midpoint_lng = ox.geocode(self.location)
            return ox.graph.graph_from_point(midpoint_lat,midpoint_lng,dist=2000)
    
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

G = Graph("147, Brittany Manor Dr, Amherst, Massachusetts, USA", "650 N Pleasant St, Amherst, Massachusetts, USA")



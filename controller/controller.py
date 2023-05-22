from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import sys
import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath("graph.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import model.graph

from utils import UtilsController
from optimal_algorithm_selector import AlgorithmSelector


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

utils = UtilsController()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get-route", methods = ['POST'])
def get_route():
    
    body=request.get_json()
    print("body  ===  ", body)
    
    starting_point = body["source"]
    ending_point = body["destination"]
    mode = body["navType"]
    percent_gain = body["distConstraint"]
    elevation = body["elevationGain"]

    model1 = model.graph.Graph(starting_point,ending_point,mode)
    G = model1.get_graph()

    # in case of error, model won't return a graph; hence performing error handling
    if not G:
        return jsonify({"errorMessage":"Source and destination are too far away from each other, please select closer places!"})

    # performing main logic
    path_finder = AlgorithmSelector(G,starting_point,ending_point,elevation)
    nodes_list, elevation= path_finder.optimal_route()

    # convering list of nodes to list of coordinates
    path_coordinates = utils.convert_nodes_to_coordinates(G,nodes_list)
    time_taken = utils.get_path_time(G,nodes_list)
    distance = utils.get_path_length(G,nodes_list)
    return jsonify({"path":path_coordinates,"elevation":elevation,"time":time_taken,"distance":distance})


@app.route("/get-place", methods = ['GET'])
def get_places():
    print("In some stuff")
    place = request.args.get("place")
    map_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&key=AIzaSyB7szZ54ue7G5mZX-R0yDKo6aw2vvxzL60".format(place)
    response = requests.request("GET", map_url)
    resp = response.json()
    preds = resp["predictions"]
    options = []
    for pred in preds:
        options.append(pred["description"])
    return jsonify({"places": options})





if __name__=="__main__":
    app.run(debug=True)
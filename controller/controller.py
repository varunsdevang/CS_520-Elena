from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import sys
import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath("graph.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from model.graph import Graph
import utils
import djikistra


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get-route", methods = ['GET'])
def get_route():
    starting_point = request.args.get("source")
    ending_point = request.args.get("destination")
    mode = "driving"
    percent_gain = "125"
    elevation = "max"

    model1 = Graph(starting_point,ending_point,"dr")
    G = model1.get_graph()
    path_finder = djikistra.Djikistra(G,starting_point,ending_point)
    nodes_list = path_finder.shortest_path()
    path_coordinates = utils.convert_nodes_to_coordinates(G,nodes_list)
    return jsonify({"result":path_coordinates})


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
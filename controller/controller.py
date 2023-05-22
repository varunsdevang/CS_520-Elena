from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import sys
import os

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

@app.route("/get-route", methods = ['GET'])
def get_route():
    # get params from front-end
    starting_point = request.args.get("source")
    ending_point = request.args.get("destination")
    mode = request.args.get("mode")
    percent_gain = "125"
    elevation = "max"

    # generating model - graph
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



if __name__=="__main__":
    app.run(debug=True)
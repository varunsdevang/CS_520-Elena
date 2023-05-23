import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath("CS_520-Elena"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import sys
import os
import requests
import constants
import model.graph
import logging
import validation_helper

from utils import UtilsController
from optimal_algorithm_selector import AlgorithmSelector


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

utils = UtilsController()
logging.basicConfig(level = logging.INFO)

@app.route("/get-route", methods = ['POST'])
def get_route():
    
    body=request.get_json()
    try:
        starting_point = body["source"]
        ending_point = body["destination"]
        mode = body["navType"]
        percent_gain = body["distConstraint"]
        elevation = body["elevationGain"]
    except:
        logging.error("Needed params - source, destination, travel_mode, percent_gain and elevation_gain; one/some/all aren't provided!!!")
        return utils.return_error_response("Missing params in request!")
        

    if not validation_helper.validate_input_for_route(body):
        print(utils.return_error_response("Source and destination are too far away from each other, please select closer places!"))
        logging.error("Parameters passed to the api are incorrect!!")
        logging.error("Please recheck and try again!")
        return utils.return_error_response("Wrong params provided!")
    
    logging.info(f"Obtained a request to generate route between {starting_point} and {ending_point}...")
    model_graph = model.graph.Graph(starting_point,ending_point,mode)
    G = model_graph.get_graph()

    # in case of error, model won't return a graph; hence performing error handling
    if not G:
        print(utils.return_error_response("Source and destination are too far away from each other, please select closer places!"))
        return utils.return_error_response("Source and destination are too far away from each other, please select closer places!")

    # performing main logic
    path_finder = AlgorithmSelector(G,starting_point,ending_point,elevation, percent_gain)
    nodes_list, elevation = path_finder.optimal_route()

    # converting list of nodes to list of coordinates
    path_coordinates = utils.convert_nodes_to_coordinates(G,nodes_list)
    time_taken = utils.get_path_time(G,nodes_list)
    distance = utils.get_path_length(G,nodes_list)
    return jsonify({"path":path_coordinates,"elevation":elevation,"time":time_taken,"distance":distance})


@app.route("/get-place", methods = ['GET'])
def get_places():
    place = request.args.get("place")
    
    logging.info(f"Generating auto-complete resulrs for \"{place}\"")
    
    map_url = constants.autocomplete_url.format(place)
    try:
        response = requests.request("GET", map_url)
    except:
        logging.error("Fatal error occured while calling auto-complete reults...")
        return utils.return_error_message("Error occured while calling auto-complete!")

    preds = response.json()["predictions"]
    options = []
    for pred in preds:
        options.append(pred["description"])
    
    return jsonify({"places": options})


if __name__=="__main__":
    app.run(debug=True, port=3001)
from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath("graph.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import model.graph
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
    mode = "drive"
    percent_gain = "125"
    elevation = "max"

    model1 = model.graph.Graph(starting_point,ending_point,"dr")
    G = model1.get_graph()
    if not G:
        return jsonify({"errorMessage":"Source and destination are too far away from each other, please select closer places!"})
    path_finder = djikistra.Djikistra(G,starting_point,ending_point)
    nodes_list = path_finder.shortest_path()
    path_coordinates = utils.convert_nodes_to_coordinates(G,nodes_list)
    return jsonify({"result":path_coordinates})



if __name__=="__main__":
    app.run(debug=True)
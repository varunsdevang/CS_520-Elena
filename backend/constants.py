import os
import sys

# SCRIPT_DIR = os.path.dirname(os.path.abspath("."))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

graphs_folder = (os.path.abspath("../model/graphs"))
graphs_available_in_cache = os.listdir(graphs_folder)

extension = ".pkl"
open_topo_request = "https://api.opentopodata.org/v1/aster30m?locations="

mode_and_speed_mapping = {
    "walk":4.5,
    "bike":20,
    "drive": None
}

valid_modes = mode_and_speed_mapping.keys()
valid_elevation = ["max","min"]
autcomplete_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&key=AIzaSyB7szZ54ue7G5mZX-R0yDKo6aw2vvxzL60"
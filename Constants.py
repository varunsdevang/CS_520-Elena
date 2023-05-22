import os
SCRIPT_DIR = os.path.dirname(os.path.abspath("."))

graphs_folder = os.path.dirname(os.path.abspath("model/graphs/"))
graphs_available_in_cache = os.listdir(graphs_folder)

extension = ".pkl"
open_topo_request = "https://api.opentopodata.org/v1/aster30m?locations="
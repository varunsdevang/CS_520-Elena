import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath("CS_520-Elena"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import constants
import logging
logging.basicConfig(level = logging.INFO)


def validate_input_for_route(body):
    starting_point = body["source"]
    ending_point = body["destination"]
    mode = body["navType"]
    percent_gain = body["distConstraint"]
    elevation = body["elevationGain"]

    source_address_length = len(starting_point.split(","))
    dest_address_length = len(ending_point.split(","))
    if(source_address_length<4 or dest_address_length<4):
        logging.warn("Source or/and Destination not passed in the proper format...")
        logging.warn("Format expected is - <Area, City, State, Country>")
        logging.error("Something went wrong, please enter adresses in the correct format and try again!")
        return False
    
    if mode not in constants.valid_modes:
        logging.error("Unknown mode provided, acceptable modes are only (bike,walk,drive)!!")
        return False
    
    if elevation not in constants.valid_elevation:
        logging.error("Unknown elevation gain option provided, acceptable modes are only (min,max)!!")
        return False
    
    return True
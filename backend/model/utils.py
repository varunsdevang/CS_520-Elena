def checkForSourceAndDestCity(start,end):
    source_address = start.split(",")
    destination_address = end.split(",")
    source_city,source_state = source_address[-3].strip(),source_address[-2].strip()
    dest_city,dest_state = destination_address[-3].strip(),destination_address[-2].strip()
    if(source_city==dest_city and source_state==dest_state):
        return {"result":True,"city":source_city,"state":source_state}
    else:
        return {"result":False}

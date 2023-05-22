def checkForSourceAndDestCity(start,end):
    source_address = start.split(",")
    destination_address = end.split(",")
    source_city,source_state = source_address[-3].strip(),source_address[-2].strip()
    dest_city,dest_state = destination_address[-3].strip(),destination_address[-2].strip()
    if(source_state==dest_state):
        state_match = True
        if(source_city==dest_city):
            city_match = True
        else:
            city_match = False
    else:
        state_match = False
    return {"city_match":city_match, "state_match":state_match, "result":{"city":source_city if city_match else None,"state":source_state if state_match else None}}

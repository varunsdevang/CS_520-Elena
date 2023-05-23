# Elena Backend Configuration #

Backend for elena is developed using flask,OSMNX.

Two algorithms are considered for selecting the optimal algorithm after considering elevation and short path.

1. [A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) 

A* (pronounced "A-star") is a graph traversal and path search algorithm which has a special feature where it stores all generated nodes in memory.


2. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

Dijkstra's original algorithm is an algorithm to find the shortest path between two given nodes source and destination using a single node as the "source" node and finds shortest paths from the source to all other nodes in the graph, producing a shortest-path tree.




## Elena - Backend Component

Backend server is REST-based web server hosting both the routing algorithms Dijkstra and A*. It is written in Python using Flask framework which uses MVC Pattern as the application architecture. Backend, with reference to our design document, consists of the Model and the Controller. 
-	Controller:
Controller is a flask REST application hosted on http://127.0.0.1:3003. It consists of the following API calls:
1.	/get-route, POST
Body: Needs the params to run the algorithm properly – source, destination, % increase, elevation_gain, mode
Response types: 200,success and 400,error
Reponse_object: path: list of coordinates, distance
2.	/get-place, GET
Query-params: text to be autocompleted
Response types: 200 and 400
-	Model:
Model is a data model that consists of the Geo-Spatial data i.e. details of latitude, longitude and elevation. It is populated by an abstraction layer with third party geospatial data providers like Google maps API and OpenStreetMap which will be used by the backend server.

To execute the application
-  Run the backend server , first install dependencies, pip3 install -r requirements.txt
- change directory to backend/controller, python3 controller. py






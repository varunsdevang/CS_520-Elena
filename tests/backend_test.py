import unittest
import requests,json,sys,os
import pickle as pkl
import osmnx as ox

SCRIPT_DIR = os.path.abspath("../backend")
sys.path.append(os.path.dirname(SCRIPT_DIR))
import backend.controller.utils 

import backend.controller.a_star
import backend.controller.djikistra


# import the MyHandler class from the main script

class TestElenaService(unittest.TestCase):
    def test_validate_route__success(self):
        
        #Validate location using Google Directions Service for querying ground-truth
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='max' #max
        percentage=125
        navType="drive"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("path",data)
    

    def test_validate_route__failure(self):
        
        #Validate location using Google Directions Service for querying ground-truth
        
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='2415 Ellendale Pl, Los Angeles, CA'
        elevation_type='max' #max
        percentage=125
        navType="drive"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        #print("data:",data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errorMessage",data)
    
    def test_elevation_validation(self):
        
        #Path Elevation Validation with optimal path 

        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        actual_Elevation=31.0
        lat_long_path=[{'lat': 42.348348, 'lng': -72.529334}, {'lat': 42.351556, 'lng': -72.527381}, {'lat': 42.351601, 'lng': -72.525857}, {'lat': 42.350055, 'lng': -72.525768}]
        elevation_expected=backend.controller.utils.UtilsController.calculate_path_elevation(self,graph,lat_long_path)
        print("Elevation :",elevation_expected)
        #self.assertIn("elevation",data)
        self.assertEqual(elevation_expected,actual_Elevation)
        
    
     

    def test_validate_pathlength(self):
        
        #Validate path length Validate coordinates
    
        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        actual_Pathlength= 724.4209999999999
        nodes=[66685931, 66730551, 66770901, 66711889]
        pathlength_expected=backend.controller.utils.UtilsController.get_path_length(self,graph,nodes)
        print("Pathlength :",pathlength_expected)
        #self.assertIn("elevation",data)
        self.assertEqual(pathlength_expected,actual_Pathlength)
        

    def test_nodes_to_coordinates(self):
        
        #Validate the conversion of nodes to coordinates

        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        nodes = [66685931, 66730551, 66770901, 66711889]
        lat_long_actual=[{'lat': 42.348348, 'lng': -72.529334}, {'lat': 42.351556, 'lng': -72.527381}, {'lat': 42.351601, 'lng': -72.525857}, {'lat': 42.350055, 'lng': -72.525768}]
        lat_long_tested=backend.controller.utils.UtilsController.convert_nodes_to_coordinates(self,graph,nodes)
        print("lat_long_tested :",lat_long_tested)
        #self.assertIn("elevation",data)
        self.assertEqual(lat_long_actual,lat_long_tested)

    def test_path_time(self):
        
        #Validate the time taken to travel the route
        
        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        nodes = [66685931, 66730551, 66770901, 66711889]
        time_actual=0.0158886187529923
        time_tested=backend.controller.utils.UtilsController.get_path_time(self,graph,nodes)
        print("time tested :",time_tested)
        
        self.assertEqual(time_actual,time_tested)
        


    
    def test_valid_Astar_algo_with_Max_ElevationGain(self):
        
        #validating the Astar algorithm for max elevation
         
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='max' #max
        percentage=125
        navType="drive"

        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        actual_AstarPath=[66685931, 66730551, 66770901, 66723660, 66626867, 66631944, 66751010, 66715414, 66652025, 66591361, 6775672007, 66721706, 66704925, 66745361, 66704169, 66686920, 66593243, 66618152, 66613374, 66714028, 66696544, 66672799, 6744652171, 66773373, 66711080, 66718580, 66614337, 66652501, 66702502, 4277546617, 66688563, 66623950, 66764082, 6371920027]
        start_lat,start_lng = ox.geocode(origin)
        end_lat,end_lng = ox.geocode(destination)
        starting_node = ox.nearest_nodes(graph,start_lng,start_lat)
        ending_node = ox.nearest_nodes(graph,end_lng,end_lat)
        d=backend.controller.a_star.A_Star(graph,starting_node,ending_node)
        calculated_AstarPath=d.shortest_path()
        self.assertCountEqual(calculated_AstarPath,actual_AstarPath)
        self.assertEqual(calculated_AstarPath,actual_AstarPath)


    def test_valid_Astar_algo_with_Min_ElevationGain(self):
        
        #validating the Astar algorithm for max elevation 

        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type=0 #max
        percentage=125
        navType="drive"
        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        actual_AstarPath=[66685931, 66730551, 66770901, 66723660, 66626867, 66631944, 66751010, 66715414, 66652025, 66591361, 6775672007, 66721706, 66704925, 66745361, 66704169, 66686920, 66593243, 66618152, 66613374, 66714028, 66696544, 66672799, 6744652171, 66773373, 66711080, 66718580, 66614337, 66652501, 66702502, 4277546617, 66688563, 66623950, 66764082, 6371920027]
        start_lat,start_lng = ox.geocode(origin)
        end_lat,end_lng = ox.geocode(destination)
        starting_node = ox.nearest_nodes(graph,start_lng,start_lat)
        ending_node = ox.nearest_nodes(graph,end_lng,end_lat)
        d=backend.controller.a_star.A_Star(graph,starting_node,ending_node)
        calculated_AstarPath=d.shortest_path()
        #print("calculated_AstarPath:",calculated_AstarPath)
        self.assertCountEqual(calculated_AstarPath,actual_AstarPath)
        self.assertEqual(calculated_AstarPath,actual_AstarPath)

    
    def test_valid_dijistra_algo_with_Max_ElevationGain(self):
        
        #validating the dijikstra algorithm for max elevation 

        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='151 Brittany Manor Dr, Amherst, Massachusetts, USA'
        elevation_type='max' #max
        percentage=125
        navType="drive"
        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        #actual_AstarPath=[66685931, 66730551, 66770901, 66723660, 66626867, 66631944, 66751010, 66715414, 66652025, 66591361, 6775672007, 66721706, 66704925, 66745361, 66704169, 66686920, 66593243, 66618152, 66613374, 66714028, 66696544, 66672799, 6744652171, 66773373, 66711080, 66718580, 66614337, 66652501, 66702502, 4277546617, 66688563, 66623950, 66764082, 6371920027]
        #actual_Astar_Elevation=1003.0
        actual_DijistraPath=[66685931, 66730551, 66770901, 66711889]
        start_lat,start_lng = ox.geocode(origin)
        end_lat,end_lng = ox.geocode(destination)
        starting_node = ox.nearest_nodes(graph,start_lng,start_lat)
        ending_node = ox.nearest_nodes(graph,end_lng,end_lat)
        d=backend.controller.djikistra.Djikistra(graph,starting_node,ending_node)
        calculated_DijistraPath=d.path_with_elevation_gain(elevation_type,percentage)
        self.assertEqual(calculated_DijistraPath,actual_DijistraPath)

    def test_valid_dijistra_algo_with_Min_ElevationGain(self):
        
        #validating the dijikstra algorithm for max elevation 

        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='151 Brittany Manor Dr, Amherst, Massachusetts, USA'
        elevation_type='min' #max
        percentage=125
        navType="drive"
        graph=pkl.load(open('../backend/model/graphs/Amherst_MA_drive.pkl',"rb"))
        actual_AstarPath=[66685931, 66730551, 66770901, 66723660, 66626867, 66631944, 66751010, 66715414, 66652025, 66591361, 6775672007, 66721706, 66704925, 66745361, 66704169, 66686920, 66593243, 66618152, 66613374, 66714028, 66696544, 66672799, 6744652171, 66773373, 66711080, 66718580, 66614337, 66652501, 66702502, 4277546617, 66688563, 66623950, 66764082, 6371920027]
        actual_Astar_Elevation=1003.0
        actual_DijistraPath=[66685931, 66730551, 66770901, 66711889]
        actual_DijistraElevation=1005.0

        start_lat,start_lng = ox.geocode(origin)
        end_lat,end_lng = ox.geocode(destination)
        starting_node = ox.nearest_nodes(graph,start_lng,start_lat)
        ending_node = ox.nearest_nodes(graph,end_lng,end_lat)
        d=backend.controller.djikistra.Djikistra(graph,starting_node,ending_node)
        calculated_DijistraPath=d.shortest_path()[0]
        print("calculated_DijistraPath:",calculated_DijistraPath)
        self.assertCountEqual(calculated_DijistraPath,actual_DijistraPath)
        self.assertEqual(calculated_DijistraPath,actual_DijistraPath)
        
    def test_invalid_mode_Of_Transport(self):

        '''
        testing with a mode other than valid modes < drive,walk,bike >
        '''
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='151 Brittany Manor Dr, Amherst, Massachusetts, USA'
        elevation_type='max' #max
        percentage=125
        navType="fly"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        print("data:",data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errorMessage",data)
        self.assertEqual('Wrong params provided!',data['errorMessage'])


    def test_invalid_address(self):

        '''
        testing with invalid address format other than format <address, city, state>
        '''
        origin='Boston'
        destination='NewYork'
        elevation_type='max' #max
        percentage=125
        navType="drive"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        print("data:",data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errorMessage",data)
        self.assertEqual('Wrong params provided!',data['errorMessage'])

    def test_invalid_elevationtype(self):

        '''
        testing with invalid elevation type other than min or max
        '''
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='151 Brittany Manor Dr, Amherst, Massachusetts, USA'
        elevation_type='0' #max
        percentage=125
        navType="drive"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        print("data:",data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errorMessage",data)
        self.assertEqual('Wrong params provided!',data['errorMessage'])

    def test_invalid_percentage(self):

        '''
        testing with invalid elevation type other than min or max
        '''
        origin='147 Brittany Manor Dr, Amherst, Massachusetts, USA'
        destination='151 Brittany Manor Dr, Amherst, Massachusetts, USA'
        elevation_type='0' #max
        percentage=300
        navType="drive"
        
        body={
            'source': origin,
            'destination': destination,
            'elevationGain': elevation_type,
            'distConstraint': percentage,
            'navType': navType
          }
        url ='http://127.0.0.1:3001/get-route'
        response = requests.post(url,json=body)
        print(response)
        data = response.json()
        print("data:",data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errorMessage",data)
        self.assertEqual('Wrong params provided!',data['errorMessage'])
           


    

        
    

    


if __name__ == '__main__':
    unittest.main()
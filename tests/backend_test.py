import unittest
import requests,json

# import the MyHandler class from the main script

class TestElenaService(unittest.TestCase):

    '''
    Validate location using Google Directions Service for querying ground-truth
    Validate the Location 
    Validate the Test Location
    Path Elevation Validation
    Validate path length Validate coordinates
    Validate Find the closest node in the graph
    Validate the Dijikstra Path Finding Algorithm
    Validate the A* Path Finding Algorithm

    '''

    def validate_location_test(self):
        '''
        Validate location using Google Directions Service for querying ground-truth
        '''
        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='100' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("result",data)

        
    def elevation_validation_test(self):
        '''
        Path Elevation Validation
        '''
        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='100' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        elevation_expected=get_elevation(origin,destination,elevation_type,percentage)
        self.assertIn("elevation",data)
        self.assertEqual(elevation_expected,data['elevation'])
     

    def validate_pathlength_test(self):
        '''
        Validate path length Validate coordinates
        '''
        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='100' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        pathlength_expected=get_pathlength(origin,destination,elevation_type,percentage)
        self.assertIn("pathlength",data)
        self.assertEqual(pathlength_expected,data['pathlength'])

    def valid_dijikstra_algo_max_test(self):
        '''
        validating the dijikstra algorithm for max elevation 
        '''
        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='100' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        expected_Pathlength=   #put the correct pathlength
        expectedroute=          #put the route
        actualroute,actual_pathlength=getshortestpath_dijistra(origin,destination,elevation_type,percentage)
        self.assertEqual(expected_Pathlength,actual_pathlength)
        self.assertEqual(expectedroute,actualroute)

    def test_valid_dijikstra_algo_min(self):
        '''
        validating the dijikstra algorithm for min elevation 
        '''

        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='0' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        expected_Pathlength=   #put the correct pathlength
        expectedroute=          #put the route
        actualroute,actual_pathlength=getshortestpath_dijistra(origin,destination,elevation_type,percentage)
        self.assertEqual(expected_Pathlength,actual_pathlength)
        self.assertEqual(expectedroute,actualroute)
        
    def test_valid_astar_algo_max(self):

        '''
        validating the Astar algorithm for max elevation 
        '''

        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='100' #max
        percentage=100
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        expected_Pathlength=   #put the correct pathlength
        expectedroute=          #put the route
        actualroute,actual_pathlength=getshortestpath_astar(origin,destination,elevation_type,percentage)
        self.assertEqual(expected_Pathlength,actual_pathlength)
        self.assertEqual(expectedroute,actualroute)

    def test_valid_astar_algo_min(self):
        '''
        validating the dijikstra algorithm for min elevation 
        '''

        origin='360 Huntington Ave, Boston, Massachusetts, USA'
        destination='650 N Pleasant St, Amherst, Massachusetts, USA'
        elevation_type='0' #max
        percentage=0
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&elevation_type={elevation_type}&percentage={percentage}"
        response = requests.get(url)
        data = response.json()
        expected_Pathlength=   #put the correct pathlength
        expectedroute=          #put the route
        actualroute,actual_pathlength=getshortestpath_astar(origin,destination,elevation_type,percentage)
        self.assertEqual(expected_Pathlength,actual_pathlength)
        self.assertEqual(expectedroute,actualroute)

    


if __name__ == '__main__':
    unittest.main()
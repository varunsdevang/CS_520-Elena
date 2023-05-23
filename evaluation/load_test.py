import requests
import time

max_clients = 5
number_of_requests = 10
host = '10.0.0.35'
url = "http://"+host+":3001"
req_body = {
    'source': '147 Brittany Manor Dr, Amherst, Massachusetts, USA',
    'destination': '650 N Pleasant St, Amherst, Massachusetts, USA',
    'elevationGain': 'min',
    'distConstraint': 125,
    'navType': 'drive'
}

sum = 0

for i in range(0, number_of_requests):
    start = time.time()
    response = requests.post(url+'/get-route', json=req_body, headers={'Content-Type': 'application/json'})
    end = time.time()
    t = end - start
    print(response.status_code)
    sum += t
print("average response time : ", sum/number_of_requests)

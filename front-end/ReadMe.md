# Elena - Frontend component
- React based javascript application.
- Uses Google Maps API to render maps
- Uses Material-UI components to styling.
- Base code created using create-react-app

## Execution
- change directory to elena/src
- install npm and its dependencies.
- install project dependencies ```npm install```
- to start the server -  ```npm start ``` 
- to run test cases - ``` npm test ```

## Components
### App
Main component which will be rendered.
#### NavForm
Form which accepts inputs.
### Map
Wrapper around Google Map and its map elements.
### ErrorDialog
Error dialog box
### MetricsTable
Tabular representation of route metadata.

## Frontend Component

Frontend is browser-based application that is accessed by user to input location details such as source and destination address, percentage increase in shortest path that is acceptable, minimum, or maximum elevation gain, and the mode of transport for which the route needs to be rendered. The front-end code is written using HTML, CSS and ReactJS. 

Front-end is a react web-app hosted on http://127.0.0.1:3000.

It gives the user the following choices to generate a path:
1.	Source
2.	Destination
3.	Percentage increase from shortest path
4.	Elevation gain (max or min)
5.	Mode of transport
The input params are formatted as a JSON object and sent as body to the backend POST api (/get-route). 
Repone consists of the following attributes:
1.	The “path” key returns a list of coordinates comprising the optimum path that are rendered on the map. 
2.	Other details such as the distance, elevation gain form the shortest path, time required to travel between the source and destination are also returned from the response which are displayed in a tabular format within the form.

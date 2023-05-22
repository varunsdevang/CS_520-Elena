import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

// Metrics Component which will render the route information.
// Implemented using a mui table.
// Currently hardcoded to static values. 
// TODO: use values from props.
const MetricTable = (props) => {
    // const mode= props.mode
    // const metrics = [ "Distance Travelled: ", "Elevation Gain: ", "Est. Travel Time: ", "Calories: "];
    // const elevationGain= ((props.elevation).toFixed(2));
    // const travelDistance=  (((props.distance)/1000).toFixed(2)) + " kms";
    // const travelTime= ((props.time).toFixed(2)) + " hr"
    // const caloriesConsumed="234 cal/hr";
    // const values = [ travelDistance, elevationGain, travelTime, caloriesConsumed]; //values populated from backend

    const mode= props.mode
    const metrics_walkcycle = [ "Distance Travelled: ", "Elevation Gain: ", "Est. Travel Time: ", "Calories: "];
    const metrics_driving = [ "Distance Travelled: ", "Elevation Gain: ", "Est. Travel Time: "];

    const elevationGain= (((props.elevation)/30).toFixed(2)) + " m";
    const travelDistance=  (((props.distance)/1000).toFixed(2)) + " kms";
    const travelTime= ((props.time).toFixed(2)) + " hr"

    const calWalk= 194 //average calories burnt by an individual in an hour while walking
    const calCyc= 300 //average calories burnt by an individual in an hour while cycling
    const caloriesConsumedWalking= (calWalk*(((props.distance)/1000).toFixed(2))) + "cal/hr"
    const caloriesConsumedCycling= (calCyc*(((props.distance)/1000).toFixed(2))) +  "cal/hr"

    const values_walking = [ travelDistance, elevationGain, travelTime, caloriesConsumedWalking]; //values populated from backend
    const values_cycling = [ travelDistance, elevationGain, travelTime, caloriesConsumedCycling]; //values populated from backend
    const values_driving = [ travelDistance, elevationGain, travelTime]; 

    return (
        <div>
                { mode === 'walk'? (
                    <TableContainer className="routeinfo-table-container" component={Paper}>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <h3> ROUTE INFORMATION </h3>
                        </div>
                        <Table aria-label="simple table">
                            <TableBody>
                            {metrics_walkcycle.map((m, index) => (
                                <TableRow key={index}>
                                    <TableCell>{m}</TableCell>
                                    <TableCell>{values_walking[index]}</TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>) 
                    : mode === 'bike'? (
                    <TableContainer className="routeinfo-table-container" component={Paper}>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <h3> ROUTE INFORMATION </h3>
                        </div>
                        <Table aria-label="simple table">
                            <TableBody>
                            {metrics_walkcycle.map((m, index) => (
                                <TableRow key={index}>
                                    <TableCell>{m}</TableCell>
                                    <TableCell>{values_cycling[index]}</TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>) 
                    : (
                    <TableContainer className="routeinfo-table-container" component={Paper}>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <h3> ROUTE INFORMATION </h3>
                        </div>
                        <Table aria-label="simple table">
                            <TableBody>
                            {metrics_driving.map((m, index) => (
                                <TableRow key={index}>
                                    <TableCell>{m}</TableCell>
                                    <TableCell>{values_driving[index]}</TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    )
                }
        </div> 
    );

}

// default export of the file.
export default MetricTable;
 
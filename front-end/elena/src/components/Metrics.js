import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
// import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const MetricTable = (props) => {
    const metrics = [ "Distance Travelled: ", "Elevation Gain: ", "Est. Travel Time: ", "Calories: "];
    const elevationGain=1;
    const travelDistance=2;
    const travelTime=3;
    const caloriesConsumed=4;
    const values = [ travelDistance, elevationGain, travelTime, caloriesConsumed]; //values populated from backend

    return (
        <TableContainer className="routeinfo-table-container" component={Paper}>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <h3> ROUTE INFORMATION </h3>
            </div>
            <Table aria-label="simple table">
                {/* 
                <TableHead>
                <TableRow>
                    <TableCell className="table-header" align="center" ><b>ROUTE INFORMATION</b></TableCell>
                    <TableCell align="center"></TableCell>
                </TableRow>
                </TableHead> */}

                <TableBody>
                {metrics.map((m, index) => (
                    <TableRow key={index}>
                        <TableCell>{m}</TableCell>
                        <TableCell>{values[index]}</TableCell>
                    </TableRow>
                ))}
                </TableBody>

            </Table>
        </TableContainer>
        
    );
}

export default MetricTable;
 
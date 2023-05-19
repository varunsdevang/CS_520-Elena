import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const MetricTable = (props) => {
    const metrics = ["Elevation Gain: ", "Distance Travelled: ", "Est. Travel Time: ", "Calories: "]
    
    return (
        <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
            <TableRow>
                <TableCell align="center">Route Information</TableCell>
            </TableRow>
            </TableHead>
            <TableBody>
                {
                    metrics.map( (m) => (
                       <TableRow>
                            <TableCell >{m}</TableCell>
                            <TableCell >100</TableCell>
                       </TableRow>
                    ))
                }
            </TableBody>
        </Table>
        </TableContainer>
    );
}

export default MetricTable;
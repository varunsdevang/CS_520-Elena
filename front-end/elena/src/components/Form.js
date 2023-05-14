import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import TerrainroundedIcon from '@mui/icons-material/TerrainRounded';
import DirectionsBikeIcon from '@mui/icons-material/DirectionsBike';
import DriveEtaIcon from '@mui/icons-material/DriveEta';
import HikingIcon from '@mui/icons-material/Hiking';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Slider from '@mui/material/Slider';
import Button from '@mui/material/Button';
import React, { useState } from 'react';
import ErrorDialog from './ErrorDialog';
import MetricTable from './Metrics';

const NavForm = (props) => {
    const {setRoute} = props;
    const [formData, setFormData] = useState({
        source: '',
        destination: '',
        elevationGain: 0,
        distConstraint: 0,
        navType:'',
        errorMessage: '',
        apiError: false,
    })

    const handleDialogClose = () => {
        setFormData({...formData, apiError: false, errorMessage: ''});
    };

    const handleSubmit = () => {
        console.log('Submit');
        console.log(formData);
        /*
        fetch('http://backend.com/api/path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => console.log(data)) // set map route from props
        .catch(error => console.error(error)); // set error window.
        */
       
        // To error message on failure scenarioss
       // setFormData({...formData, apiError: true, errorMessage: "this is a error message"})
       let route = [{lat: 42.395080, lng: -72.526807},{lat: 42.386089,lng:  -72.522535},{ lat: 42.381570,lng: -72.519363}]
        setRoute(route);
    }
    return (
        <Container>
            <h1> Elena <TerrainroundedIcon fontSize='inherit'></TerrainroundedIcon> </h1>
            <TextField id="outlined-basic" label="Source" variant="outlined" value={formData.source} onChange={e => setFormData({...formData, source:e.target.value})}/>
            <TextField id="outlined-basic" label="Destination" variant="outlined" value={formData.destination} onChange={e => setFormData({...formData, destination:e.target.value})}/>
            <br></br>
            <Slider  defaultValue={10} value={formData.distConstraint} aria-label="slider" onChange={e=> setFormData({...formData, distConstraint: e.target.value})}/>
            <ToggleButtonGroup
                color="primary"
                exclusive
                aria-label="Way"
                >
                <ToggleButton value="walking"><HikingIcon></HikingIcon></ToggleButton>
                <ToggleButton value="cycling"><DirectionsBikeIcon></DirectionsBikeIcon></ToggleButton>
                <ToggleButton value="driving"><DriveEtaIcon></DriveEtaIcon></ToggleButton>
            </ToggleButtonGroup>
            <Button variant="contained" onClick={handleSubmit}>Submit</Button>
            <ErrorDialog open={formData.apiError} message={formData.errorMessage} onClose={handleDialogClose}>
            </ErrorDialog>
            <MetricTable></MetricTable>
        </Container>     
    );
}

export default NavForm;
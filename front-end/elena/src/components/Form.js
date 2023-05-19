import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import TerrainroundedIcon from '@mui/icons-material/TerrainRounded';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import DirectionsBikeIcon from '@mui/icons-material/DirectionsBike';
import DriveEtaIcon from '@mui/icons-material/DriveEta';
import HikingIcon from '@mui/icons-material/Hiking';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Slider from '@mui/material/Slider';
import { FormGroup, Switch, FormControlLabel } from '@mui/material';
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
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <h1> EleNa <TerrainroundedIcon fontSize='inherit' /></h1>
            </div>
            <div className="textfield-container">
                <div className="source-textfield">
                    <TextField id="outlined-basic" label="Source" variant="outlined" value={formData.source} onChange={e => setFormData({...formData, source:e.target.value})}/>
                </div>
                <div className="navigation-icon" >
                    <SwapHorizIcon className="navigation-icon" style={{ fontSize: '3.5rem' }}></SwapHorizIcon>
                </div>
                <div className="destination-textfield">
                    <TextField id="outlined-basic" label="Destination" variant="outlined" value={formData.destination} onChange={e => setFormData({...formData, destination:e.target.value})}/>
                </div>
            </div>
            <div className='slider-element'>
                <Slider color="primary" defaultValue={10} value={formData.distConstraint} aria-label="slider" valueLabelDisplay="auto" 
                onChange={e=> setFormData({...formData, distConstraint: e.target.value})}/>      
            </div>
            <FormGroup style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <FormControlLabel control={<Switch defaultChecked />} label="Min. Gain" defaultChecked color="default" />
                <FormControlLabel control={<Switch defaultChecked />} label="Max. Gain" defaultChecked color="default" />
            </FormGroup>
            <ToggleButtonGroup
                style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                className='icons-container'
                color="primary"
                exclusive
                aria-label="Way" >
                <ToggleButton value="walking"><HikingIcon></HikingIcon></ToggleButton>
                <ToggleButton value="cycling"><DirectionsBikeIcon></DirectionsBikeIcon></ToggleButton>
                <ToggleButton value="driving"><DriveEtaIcon></DriveEtaIcon></ToggleButton>
            </ToggleButtonGroup>
            <div className='submit-button' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                <Button variant="contained" onClick={handleSubmit}>Go!</Button>
            </div>
            <ErrorDialog open={formData.apiError} message={formData.errorMessage} onClose={handleDialogClose}>
            </ErrorDialog>
            <div className='metrictable-container' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <MetricTable></MetricTable>
            </div>
        </Container>     
    );
}

export default NavForm;
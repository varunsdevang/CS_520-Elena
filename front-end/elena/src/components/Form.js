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
import { Select, InputLabel, FormControl, MenuItem } from '@mui/material';
import Button from '@mui/material/Button';
import React, { useState } from 'react';
import ErrorDialog from './ErrorDialog';
import MetricTable from './Metrics'; 
import Map from './Map'; 
import CircularProgress from '@mui/material/CircularProgress';
import Autocomplete from '@mui/material/Autocomplete';
import { BACKEND_URL } from './Constant';

const NavForm = (props) => {
    
    const {setRoute} = props; // setRoute function from Parent component.
    const [selectedWay, setSelectedWay] = useState(null);
    const [isLoading, setIsLoading] = useState(false); // boolean for loading state(when blocked by backend api call).
    const [progress, setProgress] = useState(0);
    const [options, setOptions] = useState([]); // options for source/destination auto-complete components.
    
    // state for form control.
    const [formData, setFormData] = useState({
        source: '',
        destination: '',
        elevationGain: 0,
        distConstraint: 0,
        navType:'',
        errorMessage: '',
        route:[],
        apiError: false, // error state for error dialog handling.
        submitted: false,
    })

    // handler for transport mode change.
    const handleWayChange = (event, newWay) => {
      setSelectedWay(newWay);
      setFormData({...formData, navType:newWay});
    }

    // handler for Error dialog close.
    const handleDialogClose = () => {
        setFormData({...formData, apiError: false, errorMessage: ''});
    };

    // Form submit handler
    // fetches route from backend for the given form inputs and sets route for the map to render.
    const handleSubmit = () => {
        setIsLoading(true); // set the website in loading mode.
        //console.log('Submit');
        //console.log(formData);
        setFormData({...formData, apiError: false, submitted: true});

        const requestBody = {
            source: formData.source,
            destination: formData.destination,
            elevationGain: formData.elevationGain,
            distConstraint: formData.distConstraint,
            navType: formData.navType
          };
          
          // REST POST request to the backend.
          fetch(`${BACKEND_URL}/get-route`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
          })
        .then(response => response.json())
        .then(data =>  setFormData({...formData, route:data["result"]})) // set map route from props
        .catch(error => console.error(error)); // set error window.
       
        // For debugging...
       //let route = [{lat: 42.395080, lng: -72.526807},{lat: 42.386089,lng:  -72.522535},{ lat: 42.381570,lng: -72.519363}]
       console.log(formData.route);
       setRoute(formData.route);
       setIsLoading(false); 
       
    }

    // method to load place suggestions for the given input. will only be invoked after the input string length of 3 is reached.
    const getOptions = (inp) => {
        console.log(BACKEND_URL)
        fetch(`${BACKEND_URL}/get-place?place=${inp}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data =>  {
            console.log(data["places"]);
            setOptions([...data["places"]]);

        }) // set map route from props
        .catch(err => console.log(err))
    }

    return (
        <div className={`container ${isLoading ? 'blur' : ''}`}>
        <Container>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <TerrainroundedIcon />
                <h1 className="elenaHeading" style={{ alignItems: "center" }}  > EleNa </h1>
                <TerrainroundedIcon />
            </div>

            <div className="textfield-container">
                <div className="source-textfield">
                    <Autocomplete
                        required
                        filterOptions={(val) => val}
                        value={formData.source}
                        opt
                        options={options}
                        onChange={(event, val) => {
                        setFormData({ ...formData, source: val });
                        }}
                        onInputChange={(event, value, cause) => {
                        if (cause === 'input' && value.length >= 3) {
                            getOptions(value);
                        }
                        }}
                        getOptionLabel={(val) => val}
                        renderInput={(vals) => (
                        <TextField
                            {...vals}
                            id="sourceInput"
                            variant="outlined"
                            aria-labelledby="sourceLabel"
                            label="Source"
                        />
                        )}
                    />
                </div>

                <div className="destination-textfield">
                    <Autocomplete
                        required
                        filterOptions={(val) => val}
                        value={formData.destination}
                        opt
                        options={options}
                        onChange={(event, val) => {
                        setFormData({ ...formData, destination: val });
                        }}
                        onInputChange={(event, value, cause) => {
                        if (cause === 'input' && value.length >= 3) {
                            getOptions(value);
                        }
                        }}
                        getOptionLabel={(val) => val}
                        renderInput={(vals) => (
                        <TextField
                            {...vals}
                            id="destinationInput"
                            variant="outlined"
                            aria-labelledby="destinationLabel"
                            label="Destination"
                        />
                        )}
                    />
                </div>
            </div>

            <div className='slider-element'>
                <Slider color="primary" defaultValue={100}  min={100} max={200} value={formData.distConstraint} aria-label="slider" valueLabelDisplay="auto" 
                onChange={e=> setFormData({...formData, distConstraint: e.target.value})}/>      
            </div> 

            <div style={{ display: 'flex', justifyContent: 'left', alignItems: 'center' }}>
                <h5> Increase % from minimum distance </h5>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <FormControl fullWidth sx={{ width: '50%' }} >
                    <InputLabel id="demo-simple-select-label">Elevation Gain</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        label="ElevationGain"
                        onChange={e=> setFormData({...formData, elevationGain: e.target.value})}>
                        <MenuItem value={0}>Minimum</MenuItem>
                        <MenuItem value={100}>Maximum</MenuItem>
                    </Select>
                </FormControl>
            </div>

            <ToggleButtonGroup
                style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                className='icons-container'
                color="primary"
                exclusive
                aria-label="Way" 
                value={selectedWay}
                onChange={handleWayChange}
                // onChange={e=> setFormData({...formData, navType:e.target.value})}
                >
                <ToggleButton value="walking" ><HikingIcon ></HikingIcon></ToggleButton>
                <ToggleButton value="cycling" ><DirectionsBikeIcon></DirectionsBikeIcon></ToggleButton>
                <ToggleButton value="driving" ><DriveEtaIcon ></DriveEtaIcon></ToggleButton>
            </ToggleButtonGroup>

            <div className='submit-button' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                <Button variant="contained" onClick={handleSubmit} >Go!</Button>
            </div>
            
            
            {isLoading ? (
                <div className="loading-overlay">
                    <CircularProgress />
                </div>
                ) : (
            <>
            <ErrorDialog open={formData.apiError} message={formData.errorMessage} onClose={handleDialogClose} />
            
            { (formData.route).length !== 0 && (
            <div className='outputParent'>
                <div className='metrictable-container' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <MetricTable />
                </div>

                {/* <div className='map-container-formjs'>
                    <Map />
                </div> */}
                {/* when route is empty (isLoading true), keep form data blurred
                when route is not empty then pass values returned from route to metrics table and display it
                parallely with metrics table, load route on map */}
                </div>
            )}
            </>
            )}
        </Container>  
        </div>   
    );
}
export default NavForm;
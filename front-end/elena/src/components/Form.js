import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import TerrainroundedIcon from '@mui/icons-material/TerrainRounded';
//import Autocomplete from 'react-google-autocomplete';
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
import Autocomplete from '@mui/material/Autocomplete';

const NavForm = (props) => {
    const {setRoute} = props;
    const [selectedWay, setSelectedWay] = useState(null);
    const [options, setOptions] = useState([]);
    const [formData, setFormData] = useState({
        source: '',
        destination: '',
        elevationGain: 0,
        distConstraint: 0,
        navType:'',
        errorMessage: '',
        route:[],
        apiError: false,
        submitted: false,
    })

    const handleWayChange = (event, newWay) => {
      setSelectedWay(newWay);
      setFormData({...formData, navType:newWay});
    }

    const handleDialogClose = () => {
        setFormData({...formData, apiError: false, errorMessage: ''});
    };

    const handleSubmit = () => {
        console.log('Submit');
        console.log(formData);
        setFormData({...formData, apiError: false, submitted: true});
        
        fetch(`http://127.0.0.1:3003/get-route?source=${formData["source"]}&destination=${formData["destination"]}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data =>  setFormData({...formData, route:data["result"]})) // set map route from props
        .catch(error => {console.error(error); setFormData({...formData, apiError: true, errorMessage: "Error fetching route. Please try again later"})}); // set error window.
       
        //To error message on failure scenarioss
        // setFormData({...formData, apiError: true, errorMessage: "this is a error message"})
       //let route = [{lat: 42.395080, lng: -72.526807},{lat: 42.386089,lng:  -72.522535},{ lat: 42.381570,lng: -72.519363}]
       console.log(formData["route"])
       setRoute(formData["route"]);
    }

    const getOptions = (inp) => {
        fetch(`http://127.0.0.1:3003/get-place?place=${inp}`, {
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
        <Container>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <TerrainroundedIcon />
                <h1 className="elenaHeading" style={{ alignItems: "center" }}  > EleNa </h1>
                <h1><TerrainroundedIcon /></h1>
            </div>

            {/* <div className="textfield-container">
                <div className="source-textfield">
                    <TextField id="outlined-basic" label="Source" variant="outlined" value={formData.source} onChange={e => setFormData({...formData, source:e.target.value})}/>
                </div>
                <div className="navigation-icon" >
                    <SwapHorizIcon className="navigation-icon" style={{ fontSize: '3.5rem' }}></SwapHorizIcon>
                </div>
                <div className="destination-textfield">
                    <TextField id="outlined-basic" label="Destination" variant="outlined" value={formData.destination} onChange={e => setFormData({...formData, destination:e.target.value})}/>
                </div>
            </div> */}

            <div className="textfield-container">
                <div className="source-textfield">

                <Autocomplete
                    required
                    filterOptions={(val) => val}
                    value={formData.source}
                    opt
                    options={options}
                    onChange={(event, val)=>{
                        setFormData({ ...formData, source: val });
                    }}
                    onInputChange={(event, value, cause) => {
                        if (cause === 'input') {
                            if (value.length >= 3) {
                                getOptions(value);
                        }}}}
                    getOptionLabel={(val) => val}
                    renderInput={(vals) => (
                    <TextField {...vals}  variant='outlined' />
                    )}
                />
                </div>

                <div className="navigation-icon">
                <SwapHorizIcon className="navigation-icon" style={{ fontSize: '1.5rem' }} />
                </div>

                <div className="destination-textfield">
                
                    {/* <Autocomplete
                    apiKey="AIzaSyB7szZ54ue7G5mZX-R0yDKo6aw2vvxzL60"
                    onPlaceSelected={(place) => {
                    const destination = place.formatted_address;
                    setFormData({ ...formData, destination });
                    }}
                    options={{
                    types: ['geocode'],
                    }} />
                    <TextField
                    id="outlined-basic"
                    label="Destination"
                    variant="outlined"
                    value={formData.destination}
                    onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
                    /> */}

                    <Autocomplete
                        required
                        filterOptions={(val) => val}
                        value={formData.destination}
                        opt
                        options={options}
                        onChange={(event, val)=>{
                            setFormData({ ...formData, destination: val });
                        }}
                        onInputChange={(event, value, cause) => {
                            if (cause === 'input') {
                                if (value.length >= 3) {
                                    getOptions(value);
                            }}}}
                        getOptionLabel={(val) => val}
                        renderInput={(vals) => (
                        <TextField {...vals}  variant='outlined' />
                        )}
                    />
                    </div>
            </div>


            <div className='slider-element'>
                <Slider color="primary" defaultValue={0} value={formData.distConstraint} aria-label="slider" valueLabelDisplay="auto" 
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
                <Button variant="contained" onClick={handleSubmit}>Go!</Button>
            </div>
            <ErrorDialog open={formData.apiError} message={formData.errorMessage} onClose={handleDialogClose}>
            </ErrorDialog>
            
            {formData.submitted && (
                <div className='metrictable-container' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <MetricTable />
                </div>
            )}

            {/* <div className='metrictable-container' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <MetricTable />
            </div> */}
        </Container>     
    );
}

export default NavForm;
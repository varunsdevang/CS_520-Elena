import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import TerrainroundedIcon from '@mui/icons-material/TerrainRounded';
import DirectionsBikeIcon from '@mui/icons-material/DirectionsBike';
import DriveEtaIcon from '@mui/icons-material/DriveEta';
import HikingIcon from '@mui/icons-material/Hiking';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Slider from '@mui/material/Slider';

const NavForm = () => {
    return (
        <Container>
            <h1> Elena <TerrainroundedIcon fontSize='inherit'></TerrainroundedIcon> </h1>
            <TextField id="outlined-basic" label="Source" variant="outlined" />
            <TextField id="outlined-basic" label="Destination" variant="outlined" />
            <br></br>
            <Slider  defaultValue={30} aria-label="Disabled slider" />
            <ToggleButtonGroup
                color="primary"
                exclusive
                aria-label="Way"
                >
                <ToggleButton value="walking"><HikingIcon></HikingIcon></ToggleButton>
                <ToggleButton value="cycling"><DirectionsBikeIcon></DirectionsBikeIcon></ToggleButton>
                <ToggleButton value="driving"><DriveEtaIcon></DriveEtaIcon></ToggleButton>
            </ToggleButtonGroup>
        </Container>     
    );
}

export default NavForm;
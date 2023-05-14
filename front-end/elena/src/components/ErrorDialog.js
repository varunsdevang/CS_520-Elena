import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';

const ErrorDialog = (props)=>{
    return (
    <Dialog open={props.open} onClose={props.onClose} maxWidth="md">
      <DialogTitle>
        Error!
      </DialogTitle>
      <DialogContent>
        <DialogContentText>
        <Typography color="red">
            {props.message}
        </Typography>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.onClose} color="primary">
          close
        </Button>
      </DialogActions>
    </Dialog>
    );
}

export default ErrorDialog;
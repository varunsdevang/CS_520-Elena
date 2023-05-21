// import logo from './logo.svg';
import './App.css';
import Map from './components/Map';
import NavForm  from './components/Form';
import {useState} from 'react';

function App() {

  const [state, setState] = useState({
    route: [],
  })
  const setRoute= (route) => {
    setState({...state, route: route});
  }

  return (
   
    <div className="app-container">
      <div className="form-container">
      <NavForm setRoute={setRoute}/>
      </div>
      <div className="map-container">
        <Map route={state.route}/>
      </div>
    </div>
  );
}

export default App;

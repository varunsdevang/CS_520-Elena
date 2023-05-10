import logo from './logo.svg';
import './App.css';
import Map from './Map';
import NavForm  from './Form';

function App() {
  return (
   
    <div className="app-container">
      <div className="form-container">
      <NavForm/>
      </div>
      <div className="map-container">
        <Map />
      </div>
    </div>
  );
}

export default App;

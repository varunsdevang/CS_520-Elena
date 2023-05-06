import logo from './logo.svg';
import './App.css';
import Map from './Map';
import Form  from './Form';

function App() {
  return (
   
    <div className="app-container">
      <div className="form-container">
      <Form/>
      </div>
      <div className="map-container">
        <Map />
      </div>
    </div>
  );
}

export default App;

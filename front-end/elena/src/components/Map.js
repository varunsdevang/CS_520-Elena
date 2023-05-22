import { GoogleMap, Marker, useLoadScript, Polyline } from "@react-google-maps/api";
import { useEffect, useState } from "react";
import "../App.css";
import { GOOGLE_API_KEY } from './Constant';

// Map - uses Google Maps and its features to render the calculated route.
const Map = (props) => {
  // route passed from parent.
  const {route} = props;
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: GOOGLE_API_KEY,
  });

  const [state, setState] = useState({
    // default state - loaded for latlng 0
    center: { lat: 0, lng: 0 },
    currentLocation: { lat: 0, lng: 0},
    zoom: 10,
  });

  useEffect(() => {
    // load current location.
    navigator.geolocation.getCurrentPosition((position)=>{
      setState({...state, currentLocation: {lat: position.coords.latitude, lng: position.coords.longitude}})
    })
  }, []);

  useEffect(() => {
    // change the zoom level when route changes/updates. (zoom in for better UX)
    setState({...state, zoom: 13, center: route[1]})
  }, [route]);

  return (
    <div className="Map">
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : (
        <GoogleMap
          center={state.center}
          zoom={state.zoom}
          mapContainerClassName="map-container"
        >
        {/* <Marker position={{ lat: state.currentLocation.lat, lng: state.currentLocation.lng }} /> //default maeker removed */}
        { 
          // marker for source location.
          route.length >= 2 && 
          <Marker position={{ lat: route[0].lat, lng: route[0].lng}} />
        }
        { 
          // marker for destination location.
          route.length >= 2 && 
          <Marker position={{ lat: route[route.length-1].lat, lng: route[route.length-1].lng}} />
        }
        <Polyline path={route} visible={true}  strokeColor={'#006aff'} strokeOpacity={1.0} strokeWeight={2}></Polyline>
        </GoogleMap>
      )}
    </div>
);
};

export default Map;
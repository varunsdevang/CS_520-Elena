import { GoogleMap, Marker, useLoadScript, Polyline } from "@react-google-maps/api";
import { useEffect, useState } from "react";
import "../App.css";

const Map = (props) => {
  const {route} = props;
  const { isLoaded } = useLoadScript({
    // googleMapsApiKey: 'AIzaSyB7szZ54ue7G5mZX-R0yDKo6aw2vvxzL60', //Varun API
    // googleMapsApiKey: 'AIzaSyCGP0U5PmCV0ZYtrlvOGQ3sdaWMi05LQt4'  //Prathiksha API
  });

  const [state, setState] = useState({
    center: { lat: 42.3732, lng: -72.519 },
    currentLocation: { lat: 42.3732, lng: -72.519},
    zoom: 10,
  })

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position)=>{

      setState({...state, currentLocation: {lat: position.coords.latitude, lng: position.coords.longitude}})
      console.log('position', position);
    })
  }, [])

  useEffect(() => {
    //route = route.map((coords) => new google.maps.LatLng(coords.lat, coords.lng))
    console.log('route', route);
    setState({...state, zoom: 13, center: route[1]})
  }, [route])

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
          <Marker position={{ lat: state.currentLocation.lat, lng: state.currentLocation.lng }} />
         <Polyline path={route} visible={true}  strokeColor={'#006aff'} strokeOpacity={1.0} strokeWeight={2}></Polyline>
        </GoogleMap>
      )}
    </div>
);
};

export default Map;
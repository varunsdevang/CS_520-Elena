import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";
import { useEffect, useMemo } from "react";
import "../App.css";

const Map = () => {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: 'AIzaSyB7szZ54ue7G5mZX-R0yDKo6aw2vvxzL60',
  });
  const center = useMemo(() => ({ lat: 42.3732, lng: -72.519 }), []);
  const currentLocation = {lat: center.lat, lng: center.lng};

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position)=>{
      currentLocation.lat = position.coords.latitude;
      currentLocation.lng = position.coords.longitude;
      console.log('position', position);
    })
  }, [])

  return (
    <div className="Map">
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : (
        <GoogleMap
          center={center}
          zoom={10}
          mapContainerClassName="map-container"
        >
          <Marker position={{ lat: currentLocation.lat, lng: currentLocation.lng }} />
        </GoogleMap>
      )}
    </div>
);
};

export default Map;
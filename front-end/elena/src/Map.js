import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";
import { useMemo } from "react";
import "./App.css";

const Map = () => {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: 'paste-ur-key-here',
  });
  const center = useMemo(() => ({ lat: 42.3732, lng: -72.519 }), []);

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
          <Marker position={{ lat: 18.52043, lng: 73.856743 }} />
        </GoogleMap>
      )}
    </div>
);
};

export default Map;
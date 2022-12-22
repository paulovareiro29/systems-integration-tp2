import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import ObjectMarkersGroup from "./ObjectMarkersGroup";

function ObjectsMap() {
  return (
    <MapContainer
      style={{ width: "100%", height: "100vh" }}
      center={[40.71536, -74.00097]}
      zoom={15}
      scrollWheelZoom={false}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <ObjectMarkersGroup />
    </MapContainer>
  );
}

export default ObjectsMap;

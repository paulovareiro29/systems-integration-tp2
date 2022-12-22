import React, { useEffect, useState } from "react";
import { LayerGroup, useMap } from "react-leaflet";
import { ObjectMarker } from "./ObjectMarker";
import useAPI from "../Hooks/useAPI";

function ObjectMarkersGroup() {
  const map = useMap();
  const { GET } = useAPI();

  const [geom, setGeom] = useState([]);
  const [bounds, setBounds] = useState(map.getBounds());

  /**
   * Setup the event to update the bounds automatically
   */
  useEffect(() => {
    const cb = () => {
      setBounds(map.getBounds());
    };
    map.on("moveend", cb);

    return () => {
      map.off("moveend", cb);
    };
  }, []);

  /* Updates the data for the current bounds */
  useEffect(() => {
    console.log(`> getting data for bounds`, bounds);
    GET(
      `/tile?neLat=${bounds._northEast.lat}&neLng=${bounds._northEast.lng}&swLat=${bounds._southWest.lat}&swLng=${bounds._southWest.lng}`
    )
      .then((result) => {
        const data = result.data;
        console.log(data);
        setGeom(data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [bounds]);

  return (
    <LayerGroup>
      {geom.map((geoJSON) => (
        <ObjectMarker key={geoJSON.id} geoJSON={geoJSON} />
      ))}
    </LayerGroup>
  );
}

export default ObjectMarkersGroup;

import {
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import React from "react";
import { Marker, Popup } from "react-leaflet";
import { icon as leafletIcon, point } from "leaflet";

import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import ApartmentIcon from "@mui/icons-material/Apartment";

const LIST_PROPERTIES = [
  { key: "price", label: "Price", Icon: AttachMoneyIcon },
  { key: "neighbourhood", label: "Neighbourhood", Icon: ApartmentIcon },
];

export function ObjectMarker({ geoJSON }) {
  const properties = geoJSON?.properties;
  const { name } = properties;
  const coordinates = geoJSON?.geometry?.coordinates;

  const imgUrl = "https://cdn-icons-png.flaticon.com/512/609/609803.png";

  return (
    <Marker
      position={coordinates}
      icon={leafletIcon({
        iconUrl: imgUrl,
        iconRetinaUrl: imgUrl,
        iconSize: point(50, 50),
      })}
    >
      <Popup>
        <List dense={true}>
          <ListItem>
            <ListItemIcon>
              <Avatar alt={name} src={imgUrl} />
            </ListItemIcon>
            <ListItemText primary={name} />
          </ListItem>
          {LIST_PROPERTIES.map(({ key, label, Icon }) => (
            <ListItem key={key}>
              <ListItemIcon>
                <Icon style={{ color: "black" }} />
              </ListItemIcon>
              <ListItemText
                primary={
                  <span>
                    {properties[key]}
                    <br />
                    <label style={{ fontSize: "xx-small" }}>({label})</label>
                  </span>
                }
              />
            </ListItem>
          ))}
        </List>
      </Popup>
    </Marker>
  );
}

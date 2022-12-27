import React, { useEffect, useState } from "react";
import {
  Box,
  CircularProgress,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";
import useAPI from "../Hooks/useAPI";
import useGraphql from "../Hooks/useGraphql";

const ELEMENTS = ["airbnbs", "areas", "types"];

function FullList() {
  const { GET } = useAPI();
  const gql = useGraphql();

  const [selectedElement, setSelectedElement] = useState("");

  const [procData, setProcData] = useState(null);
  const [gqlData, setGQLData] = useState(null);

  useEffect(() => {
    setGQLData(null);
    setProcData(null);

    if (selectedElement === "") return;

    GET(`/${selectedElement}`).then((result) => {
      const data = result.data;
      setProcData(data);
    });

    gql(`{
      ${selectedElement} {
        name
      }
    }`).then((result) => {
      const data = result.data.data;
      const elements = data[selectedElement];

      setGQLData(elements.map((el) => el.name));
    });
  }, [selectedElement]);

  return (
    <>
      <h1>Full List</h1>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "background.default",
          padding: "2rem",
          borderRadius: "1rem",
        }}
      >
        <Box>
          <h2 style={{ color: "white" }}>Options</h2>
          <FormControl fullWidth>
            <InputLabel id="elements-select-label">Element</InputLabel>
            <Select
              labelId="elements-select-label"
              id="demo-simple-select"
              value={selectedElement}
              label="Element"
              onChange={(e, v) => {
                setSelectedElement(e.target.value);
              }}
            >
              <MenuItem value={""}>
                <em>None</em>
              </MenuItem>
              {ELEMENTS.map((el) => (
                <MenuItem key={el} value={el}>
                  {el}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Container>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "info.dark",
          padding: "2rem",
          marginTop: "2rem",
          borderRadius: "1rem",
          color: "white",
        }}
      >
        <h2>
          Results <small>(PROC)</small>
        </h2>
        {procData ? (
          <ul>
            {procData.map((data, index) => (
              <li key={index}>{data}</li>
            ))}
          </ul>
        ) : selectedElement ? (
          <CircularProgress />
        ) : (
          "--"
        )}
        <h2>
          Results <small>(GraphQL)</small>
        </h2>
        {gqlData ? (
          <ul>
            {gqlData.map((data, index) => (
              <li key={index}>{data}</li>
            ))}
          </ul>
        ) : selectedElement ? (
          <CircularProgress />
        ) : (
          "--"
        )}
      </Container>
    </>
  );
}

export default FullList;

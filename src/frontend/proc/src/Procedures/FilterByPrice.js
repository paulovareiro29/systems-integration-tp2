import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  FormControl,
  CircularProgress,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Button,
} from "@mui/material";
import useAPI from "../Hooks/useAPI";
import useGraphql from "../Hooks/useGraphql";

function FilterByPrice() {
  const { GET } = useAPI();
  const gql = useGraphql();

  const [filter, setFilter] = useState({
    direction: "higher", // "higher" or "lower"
    amount: 0,
  });

  const [loading, setLoading] = useState(false);

  const [procData, setProcData] = useState(null);
  const [gqlData, setGQLData] = useState(null);

  const fetchData = () => {
    setGQLData(null);
    setProcData(null);
    setLoading(true);

    GET(`/airbnbs/price/${filter.direction}?value=${filter.amount}`).then(
      (result) => {
        const data = result.data;
        setProcData(data);
        setLoading(false);
      }
    );

    const capitalizedDirection =
      filter.direction.charAt(0).toUpperCase() + filter.direction.slice(1);

    gql(`{
      by${capitalizedDirection}Price(value: ${filter.amount}) {
        name
      }
    }`).then((result) => {
      const data = result.data.data;
      const elements = data[`by${capitalizedDirection}Price`];

      setGQLData(elements.map((el) => el.name));
    });
  };

  return (
    <>
      <h1>Filter By Price</h1>

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
            <InputLabel id="direction-select-label">
              Select Direction
            </InputLabel>
            <Select
              labelId="direction-select-label"
              id="direction-select"
              value={filter.direction}
              label="Element"
              onChange={(e, v) => {
                setFilter({ ...filter, direction: e.target.value });
              }}
            >
              <MenuItem value={"higher"}>Higher</MenuItem>
              <MenuItem value={"lower"}>Lower</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <TextField
              type="number"
              label="Amount"
              value={filter.amount}
              onChange={(e) => {
                setFilter({ ...filter, amount: e.target.value });
              }}
            />
          </FormControl>
          <Button
            sx={{ mt: 2 }}
            variant="contained"
            fullWidth
            onClick={fetchData}
          >
            Fetch Data
          </Button>
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
        ) : loading ? (
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
        ) : loading ? (
          <CircularProgress />
        ) : (
          "--"
        )}
      </Container>
    </>
  );
}

export default FilterByPrice;

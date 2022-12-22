import { useEffect, useState } from "react";
import {
  CircularProgress,
  Pagination,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

import useAPI from "../Hooks/useAPI";

function Airbnbs() {
  const PAGE_SIZE = 10;
  const { GET } = useAPI();
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [maxDataSize, setMaxDataSize] = useState(0);

  useEffect(() => {
    GET(`/airbnb/?page=${page - 1}&limit=${PAGE_SIZE}`)
      .then((result) => {
        const data = result.data;
        setData(data.data);
        setMaxDataSize(data.pagination.count);
      })
      .catch((err) => console.log(err));
  }, [page]);

  if (!data)
    return (
      <>
        <CircularProgress />
      </>
    );

  return (
    <>
      <h1>Airbnbs</h1>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell component="th" width={"1px"} align="center">
                ID
              </TableCell>
              <TableCell align="center">Airbnb Name</TableCell>
              <TableCell align="center">Price</TableCell>
              <TableCell align="center">Neighbourhood</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data ? (
              data.map((row) => (
                <TableRow
                  key={row.id}
                  style={{ background: "gray", color: "black" }}
                >
                  <TableCell component="td" align="center">
                    {row.id}
                  </TableCell>
                  <TableCell component="td" align="center" scope="row">
                    {row.name}
                  </TableCell>
                  <TableCell component="td" align="center" scope="row">
                    {row.price}
                  </TableCell>
                  <TableCell component="td" align="center" scope="row">
                    {row.neighbourhood}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3}>
                  <CircularProgress />
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      {maxDataSize && (
        <div style={{ background: "black", padding: "1rem" }}>
          <Pagination
            style={{ color: "black" }}
            variant="outlined"
            shape="rounded"
            color={"primary"}
            onChange={(e, v) => {
              setPage(v);
            }}
            page={page}
            count={Math.ceil(maxDataSize / PAGE_SIZE)}
          />
        </div>
      )}
    </>
  );
}

export default Airbnbs;

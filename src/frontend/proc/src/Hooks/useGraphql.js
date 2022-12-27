import axios from "axios";
import { API_GRAPHQL_URL } from "../Utils/constants";

export default (URL = API_GRAPHQL_URL) => {
  const options = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const gql = (query) => {
    return axios.post(URL, { query }, options);
  };

  return gql;
};

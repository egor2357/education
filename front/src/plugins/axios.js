import axios from "axios";

const headers = {
  "Content-type": "application/json",
};

export default axios.create({
  withCredentials: true,
  headers: headers,
  baseURL: process.env.NODE_ENV !== "development" ? '/back' : '/'
});

const path = require("path");
const express = require("express");
const app = express();

// add middlewares
app.use(express.static(path.join(__dirname, "..", "build")));
app.use(express.static("public"));

app.use((req, res, next) => {
  res.sendFile(path.join(__dirname, "..", "build", "index.html"));
});

const port = parseInt(process?.argv[2] || 3000);

// start express server on port 5000
app.listen(port, () => {
  console.log(`server started on port ${port}`);
});
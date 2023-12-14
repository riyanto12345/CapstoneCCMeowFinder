const express = require('express')
const userRoutes = require('./routes/userRoutes');
const app = express()
const port = 8080
const bodyParser = require('body-parser');

app.use(bodyParser.json());


app.use('/user',userRoutes);

app.get('/', (req, res) => {
  res.send('API IS RUNNING!')
});

app.use("*", (req, res) => {
  res.status(404).send({
      status: 404,
      error: 'Not found'
  });
});


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

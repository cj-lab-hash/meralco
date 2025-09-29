const express = require('express');
const bodyParser = require('body-parser');
const billingRoutes = require('./routes/billing');

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use('/', billingRoutes);

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

let records = [];

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.render('index', { record: records[records.length - 1] || [] });
});

app.post('/', (req, res) => {
  const {
    actual_bill,
    current_consumption,
    previous_consumption,
    rate_per_kwh,
    gen_current,
    gen_previous,
  } = req.body;

  // Convert to numbers
  const actualBill = parseFloat(actual_bill);
  const current = parseFloat(current_consumption);
  const previous = parseFloat(previous_consumption);
  const rate = parseFloat(rate_per_kwh);
  const genCurrentNum = parseFloat(gen_current);
  const genPreviousNum = parseFloat(gen_previous);

  // Compute values
  const consumption = current - previous;
  const genConsumption = genCurrentNum - genPreviousNum;
  const generalConsumption = consumption - genConsumption;
  const genBillComputed = genConsumption * rate
  const jmBill = generalConsumption * rate;

  const additionalCharges = (actualBill - (jmBill + genBillComputed)) / 2;
  const jmbillWithCharges = jmBill + additionalCharges;
  const genBillWithCharges = genBillComputed + additionalCharges;

  // Save record
  const record = [
    "", actualBill.toFixed(2), consumption.toFixed(2), rate.toFixed(2),
    current.toFixed(2), previous.toFixed(2),
    genPreviousNum.toFixed(2), genCurrentNum.toFixed(2),genConsumption.toFixed(2),
    genBillWithCharges.toFixed(2), jmbillWithCharges.toFixed(2)
  ];

  records.push(record);
  res.redirect('/');
});

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
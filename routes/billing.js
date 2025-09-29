const express = require('express');
const router = express.Router();
const db = require('../db/database');

router.get('/', (req, res) => {
  db.all('SELECT * FROM records ORDER BY date DESC', (err, rows) => {
    if (err) {
      console.error("Fetch error:", err.message);
      return res.status(500).send("Database error");
    }

    // Format each row
    rows.forEach(record => {
      record.formattedActualBill = formatPeso(record.actual_bill);
      record.formattedGenBill = formatPeso(record.gen_bill);
      record.formattedJmBill = formatPeso(record.jm_bill);
    });

    const latest = rows[0]; // Most recent record
    res.render('index', { record: latest, records: rows });
  });
});

function formatPeso(amount) {
  return '₱' + parseFloat(amount).toLocaleString('en-PH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}
router.post('/', (req, res) => {
  const {
  actual_bill, current_consumption, previous_consumption,
  rate_per_kwh, gen_current, gen_previous, billing_date
} = req.body;

  const actualBill = parseFloat(actual_bill);
  const current = parseFloat(current_consumption);
  const previous = parseFloat(previous_consumption);
  const rate = parseFloat(rate_per_kwh);
  const genCurrentNum = parseFloat(gen_current);
  const genPreviousNum = parseFloat(gen_previous);

  const consumption = current - previous;
  const genConsumption = parseFloat((genCurrentNum - genPreviousNum).toFixed(2));
  const generalConsumption = consumption - genConsumption;
  const genBillComputed = parseFloat((genConsumption * rate).toFixed(2));
  const jmBill = parseFloat((generalConsumption * rate).toFixed(2));

  const additionalCharges = (actualBill - (jmBill + genBillComputed)) / 2;
  const jmbillWithCharges = parseFloat((jmBill + additionalCharges).toFixed(2));
  const genBillWithCharges = parseFloat((genBillComputed + additionalCharges).toFixed(2));



  db.run(`
  INSERT INTO records (
    actual_bill, total_consumption, rate,
    current_reading, previous_reading,
    gen_previous, gen_current, gen_consumption,
    gen_bill, jm_bill, date
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`, [
  actualBill, consumption, rate,
  current, previous,
  genPreviousNum, genCurrentNum, genConsumption,
  genBillWithCharges, jmbillWithCharges, billing_date
], (err) => {
  if (err) {
    console.error("Insert error:", err.message);
    return res.status(500).send("Insert error");
  }
  res.redirect('/');
});
});
module.exports = router;

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db/billing.db');

// Create table if it doesn't exist
db.run(`
  CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    billing_date REAL,
    actual_bill REAL,
    total_consumption REAL,
    rate REAL,
    current_reading REAL,
    previous_reading REAL,
    gen_previous REAL,
    gen_current REAL,
    gen_consumption REAL,
    gen_bill REAL,
    jm_bill REAL
    date TEXT
  )
`);

module.exports = db;
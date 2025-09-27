import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS billing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ate_gen_previous Real,
    ate_gen_current Real
    actual_bill REAL,
    previous_reading REAL,
    current_reading REAL,
    consumption REAL,
    rate_per_kwh REAL,
    ate_gen_consumption REAL,
    ate_gen_bill REAL,
    jm_bill REAL
)
""")
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        actual_bill = float(request.form['actual_bill'])
        previous_reading = float(request.form['previous_reading'])
        current_reading = float(request.form['current_reading'])
        ate_gen_previous = float(request.form['ate_gen_previous'])
        ate_gen = request.form['ate_gen_current']
        consumption = current_reading - previous_reading
        rate_per_kwh = actual_bill / consumption if consumption != 0 else 0
        ate_gen_consumption = ate_gen - ate_gen_previous
        ate_gen_bill = ate_gen_consumption * rate_per_kwh
        jm_bill = (consumption - ate_gen_consumption) * rate_per_kwh

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
        INSERT INTO billing (
            ate_gen, actual_bill, previous_reading, current_reading,ate_gen_previous,
            consumption, rate_per_kwh, ate_gen_consumption, ate_gen_bill, jm_bill
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ate_gen, actual_bill, previous_reading, current_reading,ate_gen_previous,
            consumption, rate_per_kwh, ate_gen_consumption, ate_gen_bill, jm_bill
        ))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM billing')
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
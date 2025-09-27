from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create database and table if not exists
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS billing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actual_bill REAL,
    previous_reading REAL,
    current_reading REAL,
    consumption REAL,
    rate_per_kwh REAL,
    ate_gen_previous REAL,
    ate_gen_current REAL,
    ate_gen_consumption REAL,
    jm_consumption REAL,
    ate_gen_share REAL,
    jm_share REAL
)
""")
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            actual_bill = float(request.form['actual_bill'])
            previous_reading = float(request.form['previous_reading'])
            current_reading = float(request.form['current_reading'])
            ate_gen_previous = float(request.form['ate_gen_previous'])
            ate_gen_current = float(request.form['ate_gen_current'])

            consumption = current_reading - previous_reading
            rate_per_kwh = actual_bill / consumption if consumption != 0 else 0

            ate_gen_consumption = ate_gen_current - ate_gen_previous
            jm_consumption = consumption - ate_gen_consumption

            ate_gen_share = ate_gen_consumption * rate_per_kwh
            jm_share = jm_consumption * rate_per_kwh

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO billing (actual_bill, previous_reading, current_reading, consumption, rate_per_kwh, ate_gen_previous, ate_gen_current, ate_gen_consumption, jm_consumption, ate_gen_share, jm_share) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (actual_bill, previous_reading, current_reading, consumption, rate_per_kwh, ate_gen_previous, ate_gen_current, ate_gen_consumption, jm_consumption, ate_gen_share, jm_share))
            conn.commit()
            conn.close()
        except (ValueError, KeyError):
            return "Invalid input. Please enter numeric values for all fields.", 400

        return redirect('/')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM billing")
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)

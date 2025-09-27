from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ate_gen TEXT,
        previous_reading REAL,
        current_reading REAL,
        consumption REAL,
        actual_bill REAL,
        rate_per_kwh REAL
    )""")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == "POST":
        ate_gen = request.form["ate_gen"]
        previous_reading = float(request.form["previous_reading"])
        current_reading = float(request.form["current_reading"])
        actual_bill = float(request.form["actual_bill"])
        rate_per_kwh = float(request.form["rate_per_kwh"])
        consumption = current_reading - previous_reading

        c.execute("INSERT INTO billing (ate_gen, previous_reading, current_reading, consumption, actual_bill, rate_per_kwh) VALUES (?, ?, ?, ?, ?, ?)",
                  (ate_gen, previous_reading, current_reading, consumption, actual_bill, rate_per_kwh))
        conn.commit()
        return redirect("/")

    c.execute("SELECT * FROM billing")
    records = c.fetchall()
    conn.close()
    return render_template("index.html", records=records)

@app.route("/move_reading", methods=["POST"])
def move_reading():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, current_reading FROM billing WHERE ate_gen = 'Ate Gen' ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    if result:
        record_id, current_reading = result
        c.execute("UPDATE billing SET previous_reading = ? WHERE id = ?", (current_reading, record_id))
        conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

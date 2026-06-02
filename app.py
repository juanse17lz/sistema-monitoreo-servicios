from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def dashboard():
    conn = sqlite3.connect("monitor.db")
    conn.row_factory = sqlite3.Row
    cursor= conn.cursor()

    cursor.execute("""
    SELECT *
    FROM logs
    WHERE id IN (
        SELECT MAX(id)
        FROM logs
        GROUP BY service               
    )
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    total = len(logs)
    up_count = sum(1 for log in logs if log[3] == "UP")
    error_count = sum(1 for log in logs if log[3] == "ERROR")

    conn.close()

    return render_template(
        "index.html",
        logs=logs,
        total=total,
        up_count=up_count,
        error_count=error_count
        )

if __name__ == "__main__":
    app.run(debug=True)
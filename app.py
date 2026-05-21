from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Database ----------
conn = sqlite3.connect("notifications.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

# ---------- Home ----------
@app.route("/")
def index():
    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        notifications=notifications
    )

# ---------- Add Notification ----------
@app.route("/add", methods=["POST"])
def add_notification():
    message = request.form["message"]

    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notifications (message, status) VALUES (?, ?)",
        (message, "Unread")
    )

    conn.commit()
    conn.close()

    return redirect("/")

# ---------- Mark as Read ----------
@app.route("/read/<int:notification_id>")
def mark_read(notification_id):
    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notifications SET status=? WHERE id=?",
        ("Read", notification_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# ---------- Delete ----------
@app.route("/delete/<int:notification_id>")
def delete_notification(notification_id):
    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notifications WHERE id=?",
        (notification_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

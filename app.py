from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def create_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )

            connection.commit()
            connection.close()

            message = "Registration successful!"

        except sqlite3.IntegrityError:
            message = "Duplicate email detected! User already exists."

    return render_template("index.html", message=message)


@app.route("/users")
def users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, phone FROM users")
    users = cursor.fetchall()

    connection.close()

    return render_template("users.html", users=users)


create_database()

if __name__ == "__main__":
    app.run(debug=True)

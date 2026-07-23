from flask import Flask, render_template, request, redirect
from google import genai
from dotenv import load_dotenv
import sqlite3
import requests
from datetime import date, datetime, timedelta
import os

#SETUP

load_dotenv()

app = Flask(__name__)
DATABASE = "paytracker.db"

client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))
#api key has been put into a .gitignore file so it is not shared publicly. It is stored in a .env file and loaded using the dotenv library

#DATABASE SETUP
def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shift_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            hours_worked REAL NOT NULL,
            day_type TEXT NOT NULL,
            pay_rate_applied REAL NOT NULL,
            gross_earnings REAL NOT NULL,
            tax_withheld REAL NOT NULL,
            take_home_pay REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pay_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weekday_rate REAL NOT NULL,
            weekend_rate REAL NOT NULL,
            public_holiday_rate REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            savings_goal REAL NOT NULL,
            avg_weekly_spending REAL NOT NULL,
            setup_complete INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

#ROUTES

@app.route("/")
def index():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM settings")
    settings = cursor.fetchone()
    connection.close()

    if not settings or settings[3] == 0:
        return redirect("/setup")

    return render_template("index.html")


@app.route("/setup", methods=["GET", "POST"])
def setup():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    
    cursor.execute("SELECT * FROM settings")
    settings = cursor.fetchone()
    connection.close()

    
    if settings and settings[3] == 1:
        return redirect("/")

    if request.method == "POST":
        weekday_rate = request.form["weekday_rate"]
        weekend_rate = request.form["weekend_rate"]
        public_holiday_rate = request.form["public_holiday_rate"]
        savings_goal = request.form["savings_goal"]
        avg_weekly_spending = request.form["avg_weekly_spending"]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO pay_rates (weekday_rate, weekend_rate, public_holiday_rate)
            VALUES (?, ?, ?)
        """, (weekday_rate, weekend_rate, public_holiday_rate))

        cursor.execute("""
            INSERT INTO settings (savings_goal, avg_weekly_spending, setup_complete)
            VALUES (?, ?, 1)
        """, (savings_goal, avg_weekly_spending))

        connection.commit()
        connection.close()
        return redirect("/")    

    return render_template("setup.html")

@app.route("/shifts", methods=["GET", "POST"])
def shifts():
    return render_template("shifts.html")

@app.route("/savings")
def savings():
    return render_template("savings.html")

@app.route("/ai", methods=["GET", "POST"])
def ai():
    return render_template("ai.html")

@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    return render_template("settings.html")

#RUN

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
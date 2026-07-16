from flask import Flask, render_template, request, redirect
from google import genai
import sqlite3
import requests
from datetime import date, datetime, timedelta
import os

app = Flask(__name__)
DATABASE = "paytracker.db"

client = genai.Client(api_key="AQ.Ab8RN6IgUDlOWjLiAS474kon_Qk56OtRPKr-KqI5PwZWfJimug")

# ── DATABASE SETUP ───────────────────────────────────

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

# ── ROUTES ───────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/setup", methods=["GET", "POST"])
def setup():
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

# ── RUN ──────────────────────────────────────────────

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
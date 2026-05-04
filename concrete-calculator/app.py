from math import pi, ceil
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Database connection  
def get_db_connection():
    try:
        """ 
        # Connect to PostgreSQL database: case local, port 5442, db "concrete", user "user", password "password"
        conn = psycopg2.connect(
            host="localhost",
            port="5442",
            database="concrete",
            user="user",
            password="password"
        ) 
        """
        # Connect using environment variables with defaults
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"), # Docker internal default PostgreSQL port
            database=os.getenv("DB_NAME", "concrete"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password")
        )

        print("✅ PostgreSQL connection successful")

        return conn

    except psycopg2.Error as e:
        print("❌ PostgreSQL connection failed")
        print("pgerror:", e.pgerror)
        print("diag:", e.diag.message_primary if e.diag else None)
        print("full:", repr(e))
        raise


def get_diameters_from_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, diameter_mm FROM diameters")
    
    diameters = {}
    for name, d in cur.fetchall():
        diameters[name] = d

    cur.close()
    conn.close()

    return diameters



""" 
# diameters in mm for HA bars
DIAMETERS = {
    "HA8": 8,
    "HA10": 10,
    "HA12": 12,
    "HA14": 14,
    "HA16": 16,
    "HA20": 20,
    "HA25": 25,
    "HA32": 32,
    "HA40": 40
} 
"""
# calculate area of one bar in cm²
def area_bar_cm2(d_mm):
    return (pi * (d_mm ** 2) / 4) / 100.0  # mm² → cm²

def compute_counts_and_spacing(as_cm2, b_mm, e_mm):
    DIAMETERS = get_diameters_from_db()

    b_eff = b_mm - 2 * e_mm  # effective width after cover
    results = []

    for name, d in DIAMETERS.items():
        a_bar = area_bar_cm2(d)
        count = int(ceil(as_cm2 / a_bar))

        # spacing calculation
        if count > 1:
            spacing = (b_eff - count * d) / (count - 1)
            spacing = round(spacing, 1)
        else:
            spacing = "N/A"

        results.append({
            "name": name,
            "diameter_mm": d,
            "area_per_bar_cm2": round(a_bar, 4),
            "count": count,
            "spacing_mm": spacing
        })

    return results

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            as_val = float(request.form.get("as_cm2", "").replace(",", "."))
            b_val = float(request.form.get("b_mm", "").replace(",", "."))
            e_val = float(request.form.get("e_mm", "").replace(",", "."))

            if as_val <= 0 or b_val <= 0 or e_val < 0:
                raise ValueError("Invalid values")

        except Exception:
            return render_template("index.html", error="Veuillez saisir des valeurs valides.")

        return redirect(url_for("result", as_cm2=as_val, b_mm=b_val, e_mm=e_val))

    return render_template("index.html")

@app.route("/result")
def result():
    try:
        as_cm2 = float(request.args.get("as_cm2"))
        b_mm = float(request.args.get("b_mm"))
        e_mm = float(request.args.get("e_mm"))
    except Exception:
        return redirect(url_for("index"))

    results = compute_counts_and_spacing(as_cm2, b_mm, e_mm)

    return render_template("result.html",
                           as_cm2=as_cm2,
                           b_mm=b_mm,
                           e_mm=e_mm,
                           results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


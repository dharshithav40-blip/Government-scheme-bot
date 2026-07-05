# ─────────────────────────────────────────────────────────────
#  app.py  –  Flask Web App  |  Government Scheme Bot v2.0
#  Run  :  python app.py
#  Open :  http://127.0.0.1:5000
# ─────────────────────────────────────────────────────────────

from flask import Flask, request, render_template
import json
import webbrowser

app = Flask(__name__)

# Load schemes data
with open("schemes.json", encoding="utf-8") as f:
    schemes = json.load(f)



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/result", methods=["POST"])
def result():
    user_type = request.form.get("type", "").strip().lower()
    income_raw = request.form.get("income", "0").strip()

    # Validate income input
    try:
        income = int(income_raw)
    except ValueError:
        income = 0

    # Match schemes by category and income limit
    matched = [
        s for s in schemes
        if s["category"].lower() == user_type
        and income <= s["income_limit"]
    ]

    return render_template("index.html", results=matched)



if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)

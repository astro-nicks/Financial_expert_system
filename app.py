from flask import Flask, render_template, request
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()

prolog.consult("financial_expert.pl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = request.form["name"]
        income = float(request.form["income"])
        expenses = float(request.form["expenses"])
        savings = float(request.form["savings"])
        essentials = float(request.form.get("essentials", 0))  # Optional field
        non_essentials = float(request.form.get("non_essentials", 0))  # Optional field

        # Assert facts into Prolog
        prolog.assertz(f"income({user}, {income})")
        prolog.assertz(f"expenses({user}, {expenses})")
        prolog.assertz(f"savings({user}, {savings})")
        prolog.assertz(f"essential_expenses({user}, {essentials})")
        prolog.assertz(f"non_essential_expenses({user}, {non_essentials})")

        # Query Prolog for financial advice
        advice = []

        if list(prolog.query(f"overspending({user})")):
            advice.append(f"⚠️ {user} is overspending! Reduce expenses or increase income.")

        if list(prolog.query(f"should_save_more({user})")):
            advice.append(f"💰 {user} should save at least 20% of income.")

        if list(prolog.query(f"high_essential_spending({user})")):
            advice.append(f"🔍 {user} is spending too much on essentials. Consider cost-cutting strategies.")

        if list(prolog.query(f"needs_emergency_fund({user})")):
            advice.append(f"🚨 {user} needs a better emergency fund! Save at least 3 months of essential expenses.")

        if list(prolog.query(f"high_non_essential_spending({user})")):
            advice.append(f"💸 {user} is spending too much on non-essentials. Consider budgeting better.")

        return render_template("result.html", advice=advice)

    return render_template("index.html")

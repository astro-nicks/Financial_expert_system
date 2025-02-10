from flask import Flask, request, jsonify, render_template, redirect, url_for
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()

# Load Prolog knowledge base
prolog.consult("financial_expert.pl")
# # Function to query Prolog
# def query_prolog(query):
#     try:
#         result = subprocess.run(
#             ["swipl", "-s", "financial_expert", "-g", query, "-t", "halt"],
#             capture_output=True,
#             text=True
#         )
#         return result.stdout.strip()
#     except Exception as e:
#         return str(e)

# Route: Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Route: Home Page
@app.route("/Homepage")
def home():
    return render_template("homepage.html")

# Route: Sign In Page
@app.route("/signin")
def signin():
    return render_template("signinpage.html")

# Route: Sign Up Page
@app.route("/signup")
def signup():
    return render_template("signuppage.html")

# Route: Expert Advice Page
@app.route("/expert_advice", methods=["GET", "POST"])
def expert_advice():
    if request.method == "POST":
        user = request.form["name"]
        income = float(request.form["income"])
        expenses = float(request.form["expenses"])
        savings = float(request.form["savings"])
        debt = float(request.form["debt"])
        essential_expenses = float(request.form["essential_expenses"])
        non_essential_expenses = float(request.form["non_essential_expenses"])
        investments = float(request.form["investments"])
        passive_income = float(request.form["passive_income"])

        # Clear old Prolog facts (prevents duplicates)
        facts = ["income", "expenses", "savings", "debt", "essential_expenses",
                 "non_essential_expenses", "investments", "passive_income"]
        for fact in facts:
            prolog.retractall(f"{fact}('{user}', _)")

        # Insert new facts into Prolog
        prolog.assertz(f"income('{user}', {income})")
        prolog.assertz(f"expenses('{user}', {expenses})")
        prolog.assertz(f"savings('{user}', {savings})")
        prolog.assertz(f"debt('{user}', {debt})")
        prolog.assertz(f"essential_expenses('{user}', {essential_expenses})")
        prolog.assertz(f"non_essential_expenses('{user}', {non_essential_expenses})")
        prolog.assertz(f"investments('{user}', {investments})")
        prolog.assertz(f"passive_income('{user}', {passive_income})")

        # Query Prolog for financial insights
        advice = []
        queries = [
            "budget_advice", "savings_advice","investment_advice"
        ]
        
        for query in queries:
            result = list(prolog.query(f"{query}('{user}', Advice)"))
            if result:
                advice.append(f"✅ {result[0]['Advice']}")

        return render_template("result.html", advice=advice)

    return render_template("expertadvicepage.html")

# @app.route('/follow_up_response', methods=['POST'])
# def follow_up_response():
#     user = request.form['user']
#     question = request.form['follow_up_question']
#     response = request.form['response']  # Get user's response
    
#     # Example Prolog query (Modify based on your rules)
#     follow_up_advice = list(prolog.query(f"process_followup('{user}', '{question}', '{response}', Advice)"))

#     if follow_up_advice:
#         advice_text = follow_up_advice[0]['Advice']
#     else:
#         advice_text = "No further insights available."

#     return render_template('result.html', advice=[advice_text])


# Route: Investment Page
@app.route("/investment", methods=["GET", "POST"])
def investment():
    results = None
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        income = float(request.form["income"])
        savings = float(request.form["savings"])
        debt = float(request.form["debt"])

        # Remove old facts
        for fact in ["income", "savings", "debt"]:
            prolog.retractall(f"{fact}({user_id}, _)")

        # Add new facts
        prolog.assertz(f"income({user_id}, {income})")
        prolog.assertz(f"savings({user_id}, {savings})")
        prolog.assertz(f"debt({user_id}, {debt})")

        # Query investment-related rules
        results = {}
        queries = [
            "investment_advice",
            "passive_income_options",
            "investment_diversification"
        ]
        for query in queries:
            result = list(prolog.query(f"{query}({user_id}, Advice)"))
            if result:
                results[query] = result[0]["Advice"]
        return render_template("investment_result.html", results=results)
    return render_template("investmentpage.html", results=results)


@app.route("/loans", methods=["GET", "POST"])
def loans():
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        income = float(request.form["income"])
        expenses = float(request.form["expenses"])
        savings = float(request.form["savings"])
        debt = float(request.form["debt"])

        # Clear old Prolog facts (prevents duplicates)
        facts = ["income", "expenses", "savings", "debt"]
        for fact in facts:
            prolog.retractall(f"{fact}({user_id}, _)")

        # Insert new facts into Prolog
        prolog.assertz(f"income({user_id}, {income})")
        prolog.assertz(f"expenses({user_id}, {expenses})")
        prolog.assertz(f"savings({user_id}, {savings})")
        prolog.assertz(f"debt({user_id}, {debt})")


        print("Stored Facts in Prolog:")
        for fact in ["income", "expenses", "savings", "debt"]:
            stored_fact = list(prolog.query(f"{fact}({user_id}, Value)"))
            print(f"{fact}({user_id}, Value) -> {stored_fact}")

        # Query Prolog for loan and credit insights
        results = {}
        queries = [
            "calculate_risk_level",
            "loan_eligibility",
            "credit_score",
        ]

        for query in queries:
            result = list(prolog.query(f"{query}({user_id}, Result)"))
            if result:
                results[query] = result[0]["Result"]

        return render_template("loanresult.html", results=results)

    return render_template("loanspage.html", results=None)

# Route: Result Page
@app.route("/result")
def result():
    return render_template("result.html")

# API Route: Budget Advice
@app.route("/budget_advice", methods=["GET"])
def budget_advice():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"budget_advice({user_id}, Advice), write(Advice)."
    advice = query_prolog(query)
    return jsonify({"user_id": user_id, "budget_advice": advice})

# API Route: Savings Advice
@app.route("/savings_advice", methods=["GET"])
def savings_advice():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"savings_advice({user_id}, Advice), write(Advice)."
    advice = query_prolog(query)
    return jsonify({"user_id": user_id, "savings_advice": advice})

# API Route: Expense Category
@app.route("/expense_category", methods=["GET"])
def expense_category():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"expense_category({user_id}, Category), write(Category)."
    category = query_prolog(query)
    return jsonify({"user_id": user_id, "expense_category": category})

# API Route: Debt Management
@app.route("/debt_management", methods=["GET"])
def debt_management():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"debt_management({user_id}, Advice), write(Advice)."
    advice = query_prolog(query)
    return jsonify({"user_id": user_id, "debt_management": advice})

# API Route: Investment Advice
@app.route("/investment_advice", methods=["GET"])
def investment_advice():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"investment_advice({user_id}, Advice), write(Advice)."
    advice = query_prolog(query)
    return jsonify({"user_id": user_id, "investment_advice": advice})

# API Route: Follow-Up Question
@app.route("/follow_up_question", methods=["GET"])
def follow_up_question():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    query = f"follow_up_question({user_id}, Question), write(Question)."
    question = query_prolog(query)
    return jsonify({"user_id": user_id, "follow_up_question": question})

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)

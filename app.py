from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import func
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "finance.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # income / expense
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), default="")
    transaction_date = db.Column(db.Date, default=date.today, nullable=False)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)


def current_month_filter(query):
    today = date.today()
    return query.filter(
        db.extract("month", Transaction.transaction_date) == today.month,
        db.extract("year", Transaction.transaction_date) == today.year
    )


def generate_insights(income, expenses, category_spend):
    insights = []
    savings = income - expenses

    if income <= 0:
        insights.append("Add your monthly income to generate a personalized budget.")
        return insights

    if savings < 0:
        insights.append("Your current expenses are higher than income. Review discretionary categories first.")
    elif savings / income < 0.10:
        insights.append("Your current savings rate is below 10%. Consider setting a small automatic savings target.")
    else:
        insights.append(f"Your current estimated savings are ₹{savings:,.2f} for this month.")

    if category_spend:
        top_category, top_amount = max(category_spend.items(), key=lambda x: x[1])
        insights.append(f"Highest spending category: {top_category} (₹{top_amount:,.2f}). Check whether this category can be optimized.")

    return insights


@app.route("/")
def dashboard():
    income = current_month_filter(Transaction.query.filter_by(transaction_type="income")).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar() or 0

    expenses = current_month_filter(Transaction.query.filter_by(transaction_type="expense")).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar() or 0

    category_rows = current_month_filter(Transaction.query.filter_by(transaction_type="expense")).with_entities(
        Transaction.category, func.sum(Transaction.amount)
    ).group_by(Transaction.category).all()
    category_spend = {category: float(amount) for category, amount in category_rows}

    budgets = Budget.query.order_by(Budget.category).all()
    recent = Transaction.query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).limit(8).all()
    savings = income - expenses
    savings_rate = (savings / income * 100) if income else 0
    insights = generate_insights(income, expenses, category_spend)

    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        savings=savings,
        savings_rate=savings_rate,
        category_spend=category_spend,
        budgets=budgets,
        recent=recent,
        insights=insights,
    )


@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError
            item = Transaction(
                transaction_type=request.form["transaction_type"],
                category=request.form["category"].strip(),
                amount=amount,
                description=request.form.get("description", "").strip(),
                transaction_date=datetime.strptime(request.form["transaction_date"], "%Y-%m-%d").date()
            )
            db.session.add(item)
            db.session.commit()
            flash("Transaction added successfully.", "success")
        except (ValueError, KeyError):
            flash("Please enter valid transaction details.", "danger")
        return redirect(url_for("transactions"))

    items = Transaction.query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    return render_template("transactions.html", transactions=items)


@app.post("/transactions/<int:transaction_id>/delete")
def delete_transaction(transaction_id):
    item = Transaction.query.get_or_404(transaction_id)
    db.session.delete(item)
    db.session.commit()
    flash("Transaction deleted.", "success")
    return redirect(url_for("transactions"))


@app.route("/budget", methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        try:
            category = request.form["category"].strip()
            limit = float(request.form["monthly_limit"])
            if not category or limit <= 0:
                raise ValueError
            existing = Budget.query.filter_by(category=category).first()
            if existing:
                existing.monthly_limit = limit
            else:
                db.session.add(Budget(category=category, monthly_limit=limit))
            db.session.commit()
            flash("Budget saved.", "success")
        except (ValueError, KeyError):
            flash("Enter a valid category and positive monthly limit.", "danger")
        return redirect(url_for("budget"))

    budgets = Budget.query.order_by(Budget.category).all()
    return render_template("budget.html", budgets=budgets)


@app.post("/budget/<int:budget_id>/delete")
def delete_budget(budget_id):
    item = Budget.query.get_or_404(budget_id)
    db.session.delete(item)
    db.session.commit()
    flash("Budget deleted.", "success")
    return redirect(url_for("budget"))


@app.route("/reports")
def reports():
    monthly = db.session.query(
        db.extract("year", Transaction.transaction_date).label("year"),
        db.extract("month", Transaction.transaction_date).label("month"),
        Transaction.transaction_type,
        func.sum(Transaction.amount).label("total")
    ).group_by(
        db.extract("year", Transaction.transaction_date),
        db.extract("month", Transaction.transaction_date),
        Transaction.transaction_type
    ).order_by(
        db.extract("year", Transaction.transaction_date).desc(),
        db.extract("month", Transaction.transaction_date).desc()
    ).all()

    return render_template("reports.html", monthly=monthly)


@app.route("/api/summary")
def api_summary():
    income = current_month_filter(Transaction.query.filter_by(transaction_type="income")).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar() or 0
    expenses = current_month_filter(Transaction.query.filter_by(transaction_type="expense")).with_entities(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).scalar() or 0
    return jsonify({
        "income": round(float(income), 2),
        "expenses": round(float(expenses), 2),
        "savings": round(float(income - expenses), 2)
    })


def seed_demo_data():
    if Transaction.query.count() > 0:
        return

    demo = [
        Transaction(transaction_type="income", category="Salary", amount=45000, description="Monthly salary", transaction_date=date.today()),
        Transaction(transaction_type="expense", category="Rent", amount=12000, description="Monthly rent", transaction_date=date.today()),
        Transaction(transaction_type="expense", category="Food", amount=4500, description="Groceries and meals", transaction_date=date.today()),
        Transaction(transaction_type="expense", category="Transport", amount=2200, description="Travel", transaction_date=date.today()),
        Transaction(transaction_type="expense", category="Entertainment", amount=1500, description="Movies and outings", transaction_date=date.today()),
    ]
    db.session.add_all(demo)
    db.session.add_all([
        Budget(category="Rent", monthly_limit=13000),
        Budget(category="Food", monthly_limit=6000),
        Budget(category="Transport", monthly_limit=3500),
        Budget(category="Entertainment", monthly_limit=2500),
    ])
    db.session.commit()


with app.app_context():
    db.create_all()
    # seed_demo_data()


if __name__ == "__main__":
    app.run(debug=True)

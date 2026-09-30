# Personal Finance Advisor Bot

An educational full-stack Flask project for tracking income, expenses, monthly budgets, savings, and financial insights.

## Features

- Monthly income and expense tracking
- Expense categories
- Add/delete transactions
- Monthly category budgets
- Automatic savings calculation
- Spending insights
- Monthly financial reports
- JSON summary API
- SQLite database
- Responsive dashboard UI
- Demo data on first launch

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Database: SQLite + SQLAlchemy
- Architecture: Flask full-stack web application

## Hardware Requirements

- Intel Core i5 8th Gen+ / AMD Ryzen 5 or equivalent
- Minimum 8 GB RAM
- 256 GB SSD recommended
- Stable internet connection for optional future cloud/AI integrations

## Software Requirements

- Windows 10/11, macOS, or Linux
- Python 3.9+
- Google Chrome / Firefox / Edge
- VS Code or another IDE
- Git

## Installation

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## Project Structure

```text
personal_finance_advisor_bot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── budget.html
│   └── reports.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── instance/
    └── finance.db   # generated automatically
```

## Important

This is a student/demo financial-planning application, not a regulated financial-advice service. It does not connect to bank accounts or execute investments.

## Future Enhancements

- Secure user authentication
- AI/LLM-powered natural-language financial assistant
- Predictive spending analytics
- Goal-based savings tracking
- Investment education/recommendations with appropriate disclosures
- Export to PDF/Excel
- Cloud deployment on AWS
- Email notifications
- Charts using Chart.js

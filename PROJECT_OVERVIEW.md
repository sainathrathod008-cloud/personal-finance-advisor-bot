# Project Overview

## Problem Statement
Many individuals find it difficult to maintain a clear record of income, daily expenses, budgets, and savings. Manual tracking can make it harder to identify overspending and plan monthly goals.

## Proposed Solution
The Personal Finance Advisor Bot provides a centralized web interface where users can:
1. Record income.
2. Record daily expenses by category.
3. Define monthly budgets.
4. Monitor estimated savings.
5. View category-wise spending.
6. Read automatically generated spending insights.
7. Review monthly reports.

## Technical Architecture

User
  |
  v
Flask Web Application
  |
  +---- Dashboard / Transactions / Budget / Reports
  |
  v
SQLAlchemy ORM
  |
  v
SQLite Database

The project is structured so an AI/LLM service can later be connected to the insight layer without changing the main database design.

## Four Example Scenarios

### Scenario 1 - Salaried Professional
Tracks salary, rent, food, transport and entertainment. The dashboard highlights spending and savings.

### Scenario 2 - College Student
Uses a limited allowance and sets category limits for food, transport and discretionary expenses.

### Scenario 3 - Freelancer
Records variable income and project expenses. The report provides a historical view useful for planning an emergency fund.

### Scenario 4 - Household Manager
Tracks shared family income and household categories such as groceries, utilities and education.

## Responsible Use
The project is intended for education and budgeting assistance. It should not be presented as a substitute for a qualified financial professional, and users should verify important financial decisions independently.

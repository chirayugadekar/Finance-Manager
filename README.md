💸 Finance Manager – Personal Finance Dashboard
📌 Overview
Finance Manager is a Streamlit-based Personal Finance Management System that helps users track expenses, visualize monthly budgets, analyze savings trends, manage transactions, and predict future expenses using Machine Learning.
This project integrates data visualization, file handling, session management, and predictive analytics into one interactive financial dashboard.

🚀 Features
📊 Budget Overview
Monthly expense summary
Interactive bar charts
Budget evaluation based on user income
Smart financial suggestions

🧾 Transaction Management
Add daily transactions
Categorize expenses
Automatic Excel export
Pie chart for spending distribution

📈 Expense Prediction
Predicts next 2 months' expenses
Uses Linear Regression (Scikit-learn)
Actual vs Predicted comparison graph

💰 Savings Tracker
Monthly spending trend analysis
Detects increase/decrease in expenses
Provides savings insights

📤 CSV Export
Create custom transaction dataset
Download CSV instantly
🗄 Database Support
SQLite integration for transaction storage

🛠 Tech Stack
Python
Streamlit
Pandas
Matplotlib
Scikit-learn
SQLite
OpenPyXL

Finance-Manager/
│
├── app.py               # Main Streamlit app
├── budget.py            # Budget visualization module
├── transaction.py       # Transaction management
├── prediction.py        # Expense prediction module
├── savings.py           # Savings analysis
├── payment.py           # Credit/Debit summary
├── database.py          # SQLite database setup
├── help.py              # Help page
├── Finance.db           # SQLite database
└── transactions.xlsx    # Exported transactions

🎯 Learning Outcomes
Real-world financial data analysis
Data visualization techniques
Machine Learning implementation
Streamlit web app development
Session state management
File handling (CSV & Excel)
SQLite database integration

🔮 Future Improvements
User authentication system
Cloud deployment
Real-time bank API integration
Advanced ML forecasting models
Mobile responsive UI

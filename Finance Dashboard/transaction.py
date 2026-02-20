# transaction.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def show_transaction():
    st.title("🧾 Add a Transaction")

    # Initialize transaction DataFrame
    if "transactions" not in st.session_state:
        st.session_state.transactions = pd.DataFrame(columns=["date", "expenses", "category", "description"])

    # Input form
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", value=datetime.today())
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        with col2:
            category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Shopping", "Entertainment", "Other"])
            description = st.text_input("Description")

        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            new_row = pd.DataFrame([[date, amount, category, description]],
                                   columns=["date", "amount", "category", "description"])
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
            st.success("Transaction added!")

            # Save to Excel
            st.session_state.transactions.to_excel("transactions.xlsx", index=False)

    # Show transactions table
    if not st.session_state.transactions.empty:
        st.subheader("📋 Your Transactions")

        # Convert 'date' column to datetime64[ns] to avoid PyArrow error
        st.session_state.transactions["date"] = pd.to_datetime(st.session_state.transactions["date"])
        st.dataframe(st.session_state.transactions)

        # Group by category for pie chart
        st.subheader("💸 Spending by Category")

        category_summary = st.session_state.transactions.groupby("category")["amount"].sum()

        fig, ax = plt.subplots(figsize=(5, 5))  # Smaller size for better alignment
        ax.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

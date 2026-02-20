# budget.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Motivational quotes
QUOTES = [
    "A budget is telling your money where to go instead of wondering where it went. – Dave Ramsey",
    "Do not save what is left after spending, but spend what is left after saving. – Warren Buffett",
    "Beware of little expenses; a small leak will sink a great ship. – Benjamin Franklin",
    "The goal isn't more money. The goal is living life on your terms.",
    "A budget is the first step toward financial freedom."
]

def show_budget(uploaded_file):
    st.title("📂 Budget Overview")
    st.write("Visualize and evaluate your budget based on the uploaded CSV file.")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            # Ensure required columns exist
            required_cols = {"date", "expenses", "category", "description"}
            if not required_cols.issubset(df.columns):
                st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                return

            # Convert date and extract month
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M").astype(str)

            # Group by month
            monthly_budget = df.groupby("month")["expenses"].sum().reset_index()

            st.subheader("📊 Monthly Expense Summary")
            st.dataframe(monthly_budget)

            # Plot monthly budget
            st.subheader("📈 Monthly Budget Flow")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(monthly_budget["month"], monthly_budget["expenses"], color="#0072ff")
            ax.set_title("Monthly Expenses")
            ax.set_xlabel("Month")
            ax.set_ylabel("Total Expenses (₹)")
            ax.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig)

            # Budget Evaluation
            st.subheader("💼 Budget Evaluation")
            income = st.number_input("Enter your Monthly Income (₹)", min_value=0.0, step=1000.0)

            if st.button("Suggest Budget"):
                total_expense = df["expenses"].sum()
                st.write(f"### 📌 Total Expenses: ₹{total_expense:,.2f}")
                st.write(f"### 💼 Monthly Income: ₹{income:,.2f}")

                if income == 0:
                    st.warning("⚠️ Please enter a valid income to get suggestions.")
                elif total_expense > income:
                    st.error("🚨 You're overspending! Try to cut down on unnecessary categories.")
                elif income - total_expense < income * 0.2:
                    st.warning("⚠️ You’re close to your budget limit. Try saving at least 20% of your income.")
                else:
                    st.success("✅ Great job! You’re managing your budget well!")

                st.info(f"💡 *{random.choice(QUOTES)}*")

        except Exception as e:
            st.error(f"Something went wrong while reading the file: {e}")
    else:
        st.info("No CSV file found. Please upload a file from the dashboard sidebar.")

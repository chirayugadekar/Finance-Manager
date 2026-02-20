# payment.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_payment():
    st.title("🏦 Daily Credit & Debit Summary")

    uploaded_file = st.file_uploader("Upload your bank statement CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            # Validate columns
            expected_cols = {"date", "amount", "type"}
            if not expected_cols.issubset(df.columns):
                st.error("CSV must contain columns: date, amount, type (credit/debit)")
                return

            df["date"] = pd.to_datetime(df["date"]).dt.date
            today = datetime.today().date()

            # Filter today's transactions
            today_data = df[df["date"] == today]
            if today_data.empty:
                st.warning("No transactions found for today.")
                return

            # Group by type
            summary = today_data.groupby("type")["amount"].sum().reset_index()

            # Text Summary
            credit = summary[summary["type"] == "credit"]["amount"].sum()
            debit = summary[summary["type"] == "debit"]["amount"].sum()

            st.subheader("💬 Summary for Today:")
            st.markdown(f"🔼 **Credited**: ₹{credit:,.2f}")
            st.markdown(f"🔽 **Debited**: ₹{debit:,.2f}")
            st.markdown(f"💰 **Net Change**: ₹{credit - debit:,.2f}")

            # Flow Chart
            st.subheader("📊 Credit vs Debit")
            fig, ax = plt.subplots()
            ax.bar(["Credit", "Debit"], [credit, debit], color=["green", "red"])
            ax.set_ylabel("Amount (₹)")
            ax.set_title("Today's Financial Flow")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
    else:
        st.info("📥 Upload a CSV file exported from your bank to begin.")

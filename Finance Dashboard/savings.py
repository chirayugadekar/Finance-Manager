# savings.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_savings(uploaded_file):
    st.subheader("💰 Monthly Savings Tracker")

    if uploaded_file is None:
        st.warning("📂 Please upload your transaction file to view savings.")
        return

    try:
        # Read and validate CSV
        file_content = uploaded_file.read().decode('utf-8')
        if not file_content.strip():
            st.error("❌ The uploaded file is empty.")
            return

        # Reset file pointer for pandas
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_cols = {"date", "expenses"}
        if not required_cols.issubset(df.columns):
            st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
            return

        # Convert and clean
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M")
        df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce").fillna(0)

        # Group by month
        monthly = df.groupby("month")["expenses"].sum().reset_index()
        monthly["month_str"] = monthly["month"].astype(str)
        monthly["change"] = monthly["expenses"].diff().fillna(0)

        # Chart
        st.write("### 📊 Monthly Expense Overview")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(monthly["month_str"], monthly["expenses"], marker="o", color="#2c7be5")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Expenses (₹)")
        ax.set_title("Monthly Expense Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Insights
        st.write("### 💬 Savings Insights")
        for i in range(1, len(monthly)):
            month = monthly.loc[i, "month_str"]
            change = monthly.loc[i, "change"]
            if change < 0:
                st.success(f"🎉 In **{month}**, you saved ₹{abs(change):,.0f} compared to the previous month!")
                st.caption("💪 You're mastering your money!")
            elif change > 0:
                st.warning(f"⚠️ In **{month}**, expenses increased by ₹{change:,.0f}.")
                st.caption("🔍 Let’s optimize your budget next month!")
            else:
                st.info(f"ℹ️ In **{month}**, your spending was unchanged from the previous month.")

    except Exception as e:
        st.error(f"❌ Error analyzing savings: {e}")

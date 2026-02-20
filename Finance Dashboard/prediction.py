# prediction.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import calendar
import random

QUOTES = [
    "💡 A budget is telling your money where to go instead of wondering where it went.",
    "💬 Save money and money will save you.",
    "💸 The more you know about your money, the more you can do with it.",
    "📊 A small leak will sink a great ship. Watch your spending.",
    "🚀 Invest in your future by managing your present."
]

def show_prediction():
    st.title("📈 Budget Prediction")

    uploaded_file = st.file_uploader("Upload your budget CSV", type=["csv"])

    if uploaded_file:
        try:
            # Read and check file
            df = pd.read_csv(uploaded_file)
            if "date" not in df.columns or "expenses" not in df.columns:
                st.error("CSV must contain 'date' and 'expenses' columns.")
                return

            # Preprocess
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.month
            df["year"] = df["date"].dt.year
            df["month_name"] = df["date"].dt.strftime("%b") + " " + df["date"].dt.year.astype(str)
            df["month_num"] = (df["year"] - df["year"].min()) * 12 + df["month"]

            monthly_total = df.groupby(["month_num", "month_name"])["expenses"].sum().reset_index()
            monthly_total = monthly_total.sort_values("month_num").reset_index(drop=True)

            # Train
            X = monthly_total[["month_num"]]
            y = monthly_total["expenses"]
            model = LinearRegression()
            model.fit(X, y)

            # Predict
            last_month_num = monthly_total["month_num"].max()
            future_month_nums = [last_month_num + 1, last_month_num + 2]
            future_month_names = pd.date_range(
                start=pd.to_datetime(df["date"].max()) + pd.offsets.MonthBegin(1),
                periods=2,
                freq="MS"
            ).strftime("%b %Y").tolist()

            future_df = pd.DataFrame({
                "month_num": future_month_nums,
                "month_name": future_month_names
            })

            future_df["expenses"] = model.predict(future_df[["month_num"]])
            future_df["expenses"] = future_df["expenses"].clip(lower=0)

            # Combine
            actual = monthly_total[["month_name", "expenses"]].copy()
            actual["Type"] = "Actual"
            future = future_df[["month_name", "expenses"]].copy()
            future["Type"] = "Predicted"
            combined = pd.concat([actual, future], ignore_index=True)

            # Plot
            st.subheader("📉 Actual vs Predicted Expenses")
            fig, ax = plt.subplots(figsize=(10, 5))
            for label, grp in combined.groupby("Type"):
                ax.plot(grp["month_name"], grp["expenses"], marker="o", label=label)

            ax.set_xlabel("Month")
            ax.set_ylabel("Expense (₹)")
            ax.set_title("Monthly Budget Forecast")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Show predictions in words
            st.subheader("📝 Predicted Budget Summary")
            for _, row in future.iterrows():
                st.markdown(f"➡️ **{row['month_name']}**: ₹{row['expenses']:.2f}")

            # Quote
            st.subheader("💬 Financial Tip")
            st.info(random.choice(QUOTES))

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
    else:
        st.info("📁 Please upload a CSV file to begin.")

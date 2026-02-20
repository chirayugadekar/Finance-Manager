import streamlit as st

def show_help():
    st.subheader("❓ Help")
    st.markdown("""
    This is your personal finance dashboard.

    - **Budget**: Upload your CSV to view monthly expenses in a bar chart.
    - **Transaction**: Add expenses manually and export them to Excel. Pie chart shows spending distribution.
    - **Prediction**: View predicted expenses for the next 2 months based on past trends.
    - **SUPPORT**: You can contact with the user.
    """)

import streamlit as st
from budget import show_budget
from transaction import show_transaction
from prediction import show_prediction
from help import show_help
import openpyxl
import io
import pandas as pd
from savings import show_savings





def show_csv_export_page():
    st.title("📤 Export Your Custom Transaction Data")

    # Initialize data collection
    if "export_data" not in st.session_state:
        st.session_state.export_data = pd.DataFrame(columns=["date", "expenses", "category", "description"])

    with st.form("add_export_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
            expense = st.number_input("Expense (₹)", min_value=0.0, step=10.0)
        with col2:
            category = st.text_input("Category")
            description = st.text_input("Description")

        submitted = st.form_submit_button("Add to CSV")
        if submitted:
            new_row = pd.DataFrame([[date, expense, category, description]],
                                   columns=["date", "expenses", "category", "description"])
            st.session_state.export_data = pd.concat([st.session_state.export_data, new_row], ignore_index=True)
            st.success("✅ Entry added to your export file!")

    # Display DataFrame
    if not st.session_state.export_data.empty:
        st.subheader("📝 Preview")
        st.dataframe(st.session_state.export_data)

        # Convert to CSV in memory
        csv_buffer = io.StringIO()
        st.session_state.export_data.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode()

        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=csv_bytes,
            file_name="custom_transactions.csv",
            mime="text/csv"
        )

# Set page config
st.set_page_config(page_title="💸 Financial Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Dashboard","📤 Export CSV", "📊 Budget", "🧾 Transactions", "📈 Predictions","💵 Savings","❓ Help"])

# CSV Upload Slot (shared by all modules)
st.sidebar.markdown("### 📂 Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Upload your transaction CSV", type=["csv"])
if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file

# Main page content
if page == "🏠 Dashboard":
    st.title("💰 Personal Finance Assistant")
    st.markdown("""
    Welcome to your personal finance dashboard. Use the navigation on the left to:
    - Upload your monthly transaction data
    - Visualize your budget using charts
    - Add/view your transactions
    - Predict your future spending
    """)
    
    # Show uploaded file preview
    if "uploaded_file" in st.session_state:
        st.success("✅ File uploaded successfully!")
        import pandas as pd
        df = pd.read_csv(st.session_state["uploaded_file"])
        st.subheader("📋 Uploaded File Preview")
        st.dataframe(df.head())
        st.markdown(f"**Columns detected:** {', '.join(df.columns)}")

    else:
        st.info("Please upload a CSV file in the sidebar to begin.")
    
elif page == "📊 Budget":
    show_budget(st.session_state.get("uploaded_file"))
  # ✅ correct call

elif page == "🧾 Transactions":
    show_transaction()

elif page == "📈 Predictions":
    show_prediction()

elif page == "❓ Help":
    show_help()

elif page == "📤 Export CSV":
    show_csv_export_page()

elif page == "💵 Savings":
    if st.session_state.uploaded_file:
        show_savings(st.session_state.uploaded_file)
    else:
        st.warning("⚠️ Please upload a CSV file to analyze savings.")



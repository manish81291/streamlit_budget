import streamlit as st
from utils.budgetManager import Account  
import time  
from auth import AuthManager

st.set_page_config(page_title='Finfluencer', page_icon='')
st.logo('img/logo.png',size='large')

auth = AuthManager()
users = auth.fetch_users()
Authenticator = auth.get_authenticatar(users)
Authenticator.login(location='unrendered',key='Login')
if not st.session_state.get('authentication_status'):
    st.warning("Please log in to continue :)")
    st.stop()

Authenticator.logout(location='sidebar')


username = st.session_state.username
account = Account(username=username)



st.title("💵 Log Transactions")
st.divider()
if "balance" not in st.session_state:
    st.session_state.balance = account.getBalance()  # Fetch from database


formatted_balance = f"₹{st.session_state.balance:.2f}"
st.write(f"Current Balance: {formatted_balance}")

# Add Expense
with st.expander("⬆ Add New Expense"):
    with st.form("expense_form"):
        exName = st.text_input("Expense Title")
        exDate = st.date_input("Date Of Expense")
        exAmount = st.number_input("Amount Spent", min_value=0.0)
        exDes = st.text_area("Description")
        exCategory = st.selectbox("Category of expense", ("-","Food 🍕", "Personal 👨 ", "Transport 🚌", "Investment 💱"))
        submit_expense = st.form_submit_button("Add Expense ➕")
       
        if submit_expense:
            account.addExpense(exDate, exName, exAmount, exCategory, exDes)
            st.session_state.balance -= exAmount  # Deduct from balance
            st.toast("✅ Expense Added Successfully!")
            time.sleep(1.5)  # Delay for 1.5 seconds-IMPORTANT
            st.rerun() 


# Add Income
with st.expander("⬇ Add New Income"):
    with st.form("income_form"):
        InName = st.text_input("Income Title")
        InDate = st.date_input("Income Date")
        InAmount = st.number_input("Amount Received", min_value=0.0)
        InDes = st.text_area("Description")
        InSource = st.selectbox("Source Of Income", ("-","Salary 💳", "Family 👨 ", "Investment 💱", "Other"))
        submit_income = st.form_submit_button("Add Income ➕")
       
        if submit_income:
            account.addIncome(InDate, InName, InAmount, InSource, InDes)
            st.session_state.balance += InAmount  # Add to balance
            st.toast("✅ Income Added Successfully!")
            time.sleep(1.5)  
            st.rerun()  





























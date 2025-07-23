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

user_email = st.session_state.user_email
db_name = f"{user_email}.db"  

account = Account(db_name=db_name)

st.title("Your Transactions 🧾")
st.divider()

# Expenses Section
st.subheader("View Expenses")
expenses_df = account.expenseList()
if expenses_df.empty:
    st.caption("No expenses to show ＞︿＜")
else:
    st.dataframe(expenses_df)

if not expenses_df.empty:
    with st.expander("Delete Expense"):
        with st.form("delete_expense_form"):
            expense_id = st.number_input("Expense ID to Delete", min_value=0, step=1)
            if st.form_submit_button("🗑️Delete"):
                account.deleteExpense(expense_id)
                st.toast("✅ Expense Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()

# Income Section
st.subheader("View Income")
income_df = account.incomeList()
if income_df.empty:
    st.caption("No incomes to show ＞︿＜")
else:
    st.dataframe(income_df)

# Delete Income
if not income_df.empty:
    with st.expander("Delete Income"):
        with st.form("delete_income_form"):
            income_id = st.number_input("Income ID to Delete", min_value=0, step=1)
            if st.form_submit_button("🗑️ Delete"):
                account.deleteIncome(income_id)
                st.toast("✅ Income Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()

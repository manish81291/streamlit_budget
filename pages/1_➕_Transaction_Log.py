import streamlit as st
from utils.budgetManager import Account  
import time  
from auth import AuthManager
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Finfluencer', page_icon='')
st.logo('img/logo.png',size='large')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

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



st.header("💵 Log Transactions")
st.divider()
if "balance" not in st.session_state:
    st.session_state.balance = account.getBalance()  # Fetch from database


formatted_balance = f"₹{st.session_state.balance:.2f}"
st.badge(f"Current Balance: {formatted_balance}")

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Cash In", "Cash Out","Add Category"],
    icons=["bi-arrow-down-left-circle-fill", "bi-arrow-up-right-circle-fill","bi-plus-square-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

df = account.categoryList()

df_in = df[df['category_type'] == 'Cash In']
df_out = df[df['category_type'] == 'Cash Out']

df_income = account.incomeList()
df_expense = account.expenseList()

# --- PLOT PERIODS ---
if selected == "Cash In":
    st.subheader(':green[Cash In]')
    with st.form("income_form"):
        InCategory = st.selectbox("Source Of Income", df_in['category'].tolist())
        InDate = st.date_input("Income Date")
        InAmount = st.number_input("Amount Received", min_value=0.0)
        InDes = st.text_area("Description")
        submit_income = st.form_submit_button("Add Cash In ➕")

        st.write(':green[Top 10 Recent Cash In Transactions]')
        st.dataframe(df_income, use_container_width=True, hide_index=True)
       
        if submit_income:
            account.addIncome(InCategory, InDate, InAmount, InDes)
            st.session_state.balance += InAmount  # Add to balance
            st.toast("✅ Income Added Successfully!")
            time.sleep(1.5)  
            st.rerun()  
    

if selected == "Cash Out":
    st.subheader(':red[Cash Out]')
    with st.form("expense_form"):
        exCategory = st.selectbox("Category of expense", df_out['category'].tolist())
        exDate = st.date_input("Date Of Expense")
        exAmount = st.number_input("Amount Spent", min_value=0.0)
        exDes = st.text_area("Description")
        submit_expense = st.form_submit_button("Add Cash Out ➕")

        st.write(':red[Top 10 Recent Cash Out Transactions]')
        st.dataframe(df_expense, use_container_width=True, hide_index=True)

        if submit_expense:
            account.addExpense(exCategory, exDate, exAmount, exDes)
            st.session_state.balance -= exAmount  # Deduct from balance
            st.toast("✅ Expense Added Successfully!")
            time.sleep(1.5)  # Delay for 1.5 seconds-IMPORTANT
            st.rerun()
    

if selected == "Add Category":

    df_in['category_new'] = df_in.category.apply(lambda x: ':green-badge['+x+']')
    df_out['category_new'] = df_out.category.apply(lambda x: ':red-badge['+x+']')

    tab1, tab2 = st.tabs(["Add Cash In Categories", "Add Cash Out Categories"])

    with tab1:
        st.markdown("Available Categories - "+" ".join(df_in.category_new.to_list()))
        with st.form("add_category_form_in"):
            category_name_in = st.text_input("Category Name")
            submit_category_in = st.form_submit_button("Add Cash In Category ➕")

            if submit_category_in:
                if category_name_in:
                    if category_name_in in df_in.category.values:
                        st.warning(f"Category '{category_name_in}' already exists!")
                    else:
                        account.CategoryManager.addCategory('Cash In',category_name_in)
                        st.success(f"Cash In Category '{category_name_in}' added successfully!")
                        st.rerun()
                else:
                    st.warning("Please enter a category name.")

    with tab2:
        st.markdown("Available Categories - "+" ".join(df_out.category_new.to_list()))
        with st.form("add_category_form_out"):
            category_name_out = st.text_input("Category Name")
            submit_category_out = st.form_submit_button("Add Cash Out Category ➕")

            if submit_category_out:
                if category_name_out:
                    if category_name_out in df_out.category.values:
                        st.warning(f"Category '{category_name_out}' already exists!")
                    else:
                        account.CategoryManager.addCategory('Cash Out',category_name_out)
                        st.success(f"Cash Out Category '{category_name_out}' added successfully!")
                        st.rerun()
                else:
                    st.warning("Please enter a category name.")























import streamlit as st
from utils.accountManager import Account  
import time  
from auth import AuthManager
from streamlit_option_menu import option_menu
from utils.finbot import FinFlowBot

st.set_page_config(page_title='Budget Target', page_icon='')
st.logo('img/logo.png',size='large')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                    max-width: 80%;
                }
            h2 {
                        padding: 0 !important;
                }
                img {
                    height: auto !important;
                }
        </style>
        """, unsafe_allow_html=True)

finbot  = FinFlowBot()
auth = AuthManager()
users = auth.fetch_users()
Authenticator = auth.get_authenticatar(users)
Authenticator.login(location='unrendered',key='Login')
if not st.session_state.get('authentication_status'):
    st.toast("Please log in to continue! 😊, Redirecting to Login Page..")
    time.sleep(2)
    st.switch_page('Home.py')  # Redirect to Home page if not authenticated
    st.stop()

Authenticator.logout(location='sidebar')


username = st.session_state.username
account = Account(username=username)



st.header("🎯 Budget Target")
st.divider()

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Expense Budget Target", "Add Expense Category"],
    icons=["bi-bullseye","bi-plus-square-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

df = account.categoryList()
budget = account.BudgetManager.viewBudget()

df_out = df[df['category_type'] == 'Cash Out']

budget_str = None
budget_str_val = {}
short_term_goal = None
long_term_goal = None

if not budget.empty:
    budget_str = budget.iloc[0]['budget_str']
    budget_str_val = eval(budget_str) if budget_str else {}
    short_term_goal = budget.iloc[0]['short_term_goal']
    long_term_goal = budget.iloc[0]['long_term_goal']

if selected == "Expense Budget Target":
    st.write(':red[Expense Budget Target]')

    col1, col2 = st.columns([3,2])

    with col1:

        with st.form("budget_form"):
            budget_var = {}

            for x in df_out['category'].tolist():
                budget_var[x] = st.slider(
                                    label=f"{x} in %".format(x),
                                    min_value=0,  # Minimum value
                                    max_value=100,  # Maximum value
                                    value= budget_str_val[x] if x in budget_str_val else 0,  # Default value
                                    step=1  # Step size
                                )

            short_term_goal = st.text_input("Short Term Goal", value=short_term_goal)
            long_term_goal = st.text_input("Long Term Goal", value=long_term_goal)
            submit_budget = st.form_submit_button("Update Budget Target")
            if submit_budget:
                if sum(list(budget_var.values())) > 100:
                    st.toast("Sum of all the Expense Budget target is greater than 100% of average Cash In",icon="⚠️")
                if not budget.empty:
                    account.BudgetManager.updateBudget(str(budget_var), short_term_goal, long_term_goal)
                else:
                    account.BudgetManager.addBudget(str(budget_var), short_term_goal, long_term_goal)
                st.toast("✅ Budget updated successfully!")
                time.sleep(2)  
                st.rerun()
    with col2:
        if st.button("💡Generate Budgeting recommendation",key='gi3'):
            with st.spinner("Thinking with Gemini..."):
                df_profile_chat = account.ProfileManager.viewProfile()
                df_profile_chat = df_profile_chat[['business_type','business_open_date','business_size','business_location']]
                df_profile_chat.columns = ['business type','business open date','business size','business location']

                df_budget_chat = account.BudgetManager.viewBudget()
                df_budget_chat = df_budget_chat[['budget_str','short_term_goal','long_term_goal']]
                df_budget_chat.columns = ['Maximum Expense budget','short term goal','long term goal']


                parent_prompt = """I have business profile ("Business Information") and Budget Allocation data for my business.

                Here is the data in JSON format:
                Business Information: {}
                Budget Allocation: {}

                """.format(df_profile_chat.iloc[0].to_json(),df_budget_chat.iloc[0].to_json())

                summarise_prompt= parent_prompt+"""
                Please perform the following analysis:
                1. Make sure profit margin of the industry is considered you deduct that before budgeting recommendation.
                2. Based on the business information provided, short and long term plan, what is the recommended budget allocation. Give allocation in percentage only for categories present in expense.
                3. Don't provide response in more than 100 words."""



                response = finbot.call_ai(summarise_prompt)
                st.markdown(response.text)
                finbot.textToSpeech(response.text)

if selected == "Add Expense Category":
    df_out['category_new'] = df_out.category.apply(lambda x: ':red-badge['+x+']')
    st.write(':red[Add Expense/Cash Out Category]')
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
                    st.toast(f"✅ Cash Out Category '{category_name_out}' added successfully!")
                    st.rerun()
            else:
                st.warning("Please enter a category name.")
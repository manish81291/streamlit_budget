from google import genai
import  streamlit as st
import time  
from auth import AuthManager
from utils.accountManager import Account  
from utils.finbot import FinFlowBot

finbot = FinFlowBot()
st.set_page_config(page_title='Insights', page_icon='')
st.logo('img/logo.png',size='large')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
            h2 {
                        padding: 0 !important;
                }
                img {
                    height: auto !important;
                }
        </style>
        """, unsafe_allow_html=True)

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

df_income_chat = account.incomeList()
df_expense_chat = account.expenseList()
df_profile_chat = account.ProfileManager.viewProfile()
df_profile_chat = df_profile_chat[['business_type','business_open_date','business_size','business_location']]
df_profile_chat.columns = ['business type','business open date','business size','business location']

df_budget_chat = account.BudgetManager.viewBudget()
df_budget_chat = df_budget_chat[['budget_str','short_term_goal','long_term_goal']]
df_budget_chat.columns = ['Maximum Expense budget','short term goal','long term goal']


parent_prompt = """I have monthly income ("Cash In"), expense ("Cash Out") , business profile ("Business Information") and Budget Allocation data for the past 12 months.

                Here is the data in JSON format:
                Cash In: {}
                Cash Out: {}
                Business Information: {}
                Budget Allocation: {}

                """.format(df_income_chat.to_json(),df_expense_chat.to_json(),df_profile_chat.iloc[0].to_json(),df_budget_chat.iloc[0].to_json())

summarise_prompt= parent_prompt+"""
You are a financial bot, make sure there is no text formatting issue. Don't include codes in your response.
Please perform the following analysis:
1. Identify if the business will need funding and by when.
2. Provide funding opportunities base on Business Information, prioritize funding or loan from Deutsche Bank like Business Instalment Loan, unsecured Business Loan. Provide link for the loan and funding opportunities, manadtory from Deutsche Bank.
3. Who can the business achieve short term and long term goal.
4. What are other insights can you provie.
5. Identify any risks.
6. Summarise everything in not more than 2 pages."""
st.write("")
if st.button("Genarate Insight for you business"):
    with st.spinner("Thinking with Gemini..."):
        client = genai.Client(
        vertexai=True, project='hack-team-finfluenzers', location='us-central1'
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=summarise_prompt
        )

        st.markdown(response.text)
        finbot.textToSpeech(response.text)

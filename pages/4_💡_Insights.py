from google import genai
import  streamlit as st
import time  
from auth import AuthManager
from utils.accountManager import Account  

st.set_page_config(page_title='Transactions', page_icon='')
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

df_income = account.incomeList()
df_expense = account.expenseList()
df_profile = account.ProfileManager.viewProfile()
df_budget = account.BudgetManager.viewBudget()

parent_prompt = """I have monthly income ("Cash In") and expense ("Cash Out") data for the past 12 months.
Here is the data:
Cash In: {}
Cash Out: {}

""".format(df_income.to_json(),df_expense.to_json())

summarise_prompt= parent_prompt+"""Please perform the following analysis:
1.  Summarise in not motre than 3 points"""


client = genai.Client(
    vertexai=True, project='hack-team-finfluenzers', location='us-central1'
)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=summarise_prompt
)

st.write(response.text)
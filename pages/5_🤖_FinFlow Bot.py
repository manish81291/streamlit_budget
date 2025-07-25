import  streamlit as st
import time  
from auth import AuthManager
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from utils.accountManager import Account

st.set_page_config(page_title='Insights', page_icon='')
st.logo('img/logo.png',size='large')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                    max-width: 90%;
                }
            h2 {
                        padding: 0 !important;
                }
                img {
                    height: auto !important;
                }
            .stBottom > div > div {
            max-width: 90%;
            padding: 1rem 0rem 3.5rem;
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

# 🔧 Init Vertex AI with your GCP project and region
PROJECT_ID = "hack-team-finfluenzers"  # Replace with your project
REGION = "us-central1"              # or the appropriate region

vertexai.init(project=PROJECT_ID, location=REGION)

# Load Gemini Flash 2.5 model
model = GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

# Page settings
st.set_page_config(page_title="FinFlow Bot", page_icon="🤖")
st.subheader("🤖 FinFlow Bot (Powered by Gemini Flash 2.5)")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Show chat history
for role, message in st.session_state.history:
    st.chat_message(role).markdown(message)

df_income = account.incomeList()
df_expense = account.expenseList()
df_profile = account.ProfileManager.viewProfile()
df_budget = account.BudgetManager.viewBudget()

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append(("user", prompt))

    # Call Gemini Flash 2.5
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.history.append(("assistant", response.text))
            except Exception as e:
                st.error(f"Error from Gemini: {e}")

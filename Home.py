import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import sqlite3
import time
from auth import AuthManager
from utils.accountManager import Account
import pandas as pd
import plotly.express as px

auth = AuthManager()


# st.set_page_config(page_title='Finfluencer', page_icon='', initial_sidebar_state='collapsed')

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
                h2 {
                        padding: 0 !important;
                }
        </style>
        """, unsafe_allow_html=True)

try:

    users = auth.fetch_users()
    Authenticator = auth.get_authenticatar(users)

    if not users:
        auth.sign_up()
    else:

        Authenticator.login(location='unrendered',key='Login')

        if not st.session_state.get('authentication_status'):

            tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

            with tab1:
            
                Authenticator.login(location='main',key='Login')

                if st.session_state.get('authentication_status') is False:
                    st.error('Username/password is incorrect')
                elif st.session_state.get('authentication_status') is None:
                    st.warning('Please enter your username and password')
                # else:
                #     st.toast(f"Welcome to Finfluencer, {st.session_state.get('username')}! An AI assisted budgeting and Literacy tool! 😊")
                #     time.sleep(2)
    
            with tab2:
                auth.sign_up()
        else:
            Authenticator.logout(location='sidebar')
            st.header(f'Welcome to Finfluenzer :green[*{st.session_state.get("username")}*] 👤 \n :orange[*An AI assisted budgeting and Literacy tool!*] 😊',divider='gray')

            account = Account(username=st.session_state.get('username'))
            df_income = account.incomeList()
            df_expense = account.expenseList()

            if not df_expense.empty and not df_income.empty:

                df_income['date'] = pd.to_datetime(df_income['date'])
                df_expense['date'] = pd.to_datetime(df_expense['date'])

                df_expense["month"] = df_expense["date"].dt.strftime('%b %Y')
                df_income["month"] = df_income["date"].dt.strftime('%b %Y')

                # monthly_expense = df_expense.groupby("month")["amount"].sum().reset_index()
                # monthly_income = df_income.groupby("month")["amount"].sum().reset_index()

                df = pd.merge(
                    df_income.groupby("month")["amount"].sum().reset_index(),
                    df_expense.groupby("month")["amount"].sum().reset_index(),
                    on="month",
                    how="outer"
                ).fillna(0)
                df.columns = ["month", "Income", "Expense"]
                df["month_new"] = pd.to_datetime(df["month"], format='%b %Y')

                df.sort_values(by='month_new', inplace=True)    

                fig = px.line(
                    df,
                    x="month",
                    y=["Income", "Expense"],
                    title="Monthly Income vs Expense Trend",
                    markers=True
                )

                # add average dotted lines
                avg_income = df["Income"].mean()
                avg_expense = df["Expense"].mean()

                fig.add_hline(y=avg_income, line_dash="dot", line_color="green", annotation_text="Avg Cash In", annotation_position="top left")
                fig.add_hline(y=avg_expense, line_dash="dot", line_color="red", annotation_text="Avg Cash Out", annotation_position="top left")         

                st.plotly_chart(fig)

                budget = account.BudgetManager.viewBudget()
                if not budget.empty:
                    pass
                    #calculate Monthly expense by category and see if ar espendign more than budget
                    




except Exception as ex:
    st.error(f"An error occurred: {ex}")
    # st.success('Refresh Page')
import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import sqlite3
import time
from auth import AuthManager
from utils.accountManager import Account
from utils.finbot import FinFlowBot
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

auth = AuthManager()
finbot = FinFlowBot()

# st.set_page_config(page_title='Finfluencer', page_icon='', initial_sidebar_state='collapsed')

st.set_page_config(page_title='FinFlow', page_icon='')
st.logo('img/logo.png',size='large')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                    max-width: 95%;
                }
                h2 {
                        padding: 0 !important;
                }
                img {
                    height: auto !important;
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
            st.header(f'Welcome to FinFlow :green[*{st.session_state.get("username").capitalize()}*] 👤 \n :orange[*An AI assisted budgeting and Literacy tool!*] 😊',divider='gray')
            
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
                df.columns = ["month", "Cash In", "Cash Out"]
                df["month_new"] = pd.to_datetime(df["month"], format='%b %Y')

                df.sort_values(by='month_new', inplace=True)    

                fig = px.line(
                    df,
                    x="month",
                    y=["Cash In", "Cash Out"],
                    title="Monthly Income vs Expense Trend",
                    markers=True
                )

                # # add average dotted lines
                # avg_income = df["Income"].mean()
                # avg_expense = df["Expense"].mean()

                # fig.add_hline(y=avg_income, line_dash="dot", line_color="green", annotation_text="Avg Cash In", annotation_position="top left")
                # fig.add_hline(y=avg_expense, line_dash="dot", line_color="red", annotation_text="Avg Cash Out", annotation_position="top left")         
                # Calculate trendline using numpy (linear regression)
                x = np.arange(len(df))  # Convert dates to numerical indices
                y_inc = df['Cash In']
                coeffs_inc = np.polyfit(x, y_inc, 1)  # Linear fit (degree=1)
                trendline_inc = np.polyval(coeffs_inc, x)

                y_exp = df['Cash Out']
                coeffs_exp = np.polyfit(x, y_exp, 1)  # Linear fit (degree=1)
                trendline_exp = np.polyval(coeffs_exp, x)

                # Create the line plot
                # fig = px.line(df, x='date', y='amount', title='Amount with Trendline')

                # Add trendline to the plot
                fig.add_trace(go.Scatter(x=df['month'], y=trendline_inc, mode='lines', name='Cash In Trendline', line=dict(dash='dot', color='green')))
                fig.add_trace(go.Scatter(x=df['month'], y=trendline_exp, mode='lines', name='Cash Out Trendline', line=dict(dash='dot', color='red')))
                
                col1, col2 = st.columns([2,1])

                with col1:
                    st.plotly_chart(fig)

                with col2:
                    if st.button("💡Generate Insight",key='gi1'):
                        with st.spinner("Thinking with Gemini..."):
                            df_income_chat = account.incomeList()
                            df_expense_chat = account.expenseList()

                            parent_prompt = """I have monthly income ("Cash In") and expense ("Cash Out") data for the past 12 months.
                            Here is the data:
                            Cash In: {}
                            Cash Out: {}

                            """.format(df_income_chat.to_json(),df_expense_chat.to_json())

                            summarise_prompt= parent_prompt+"""Please perform the following analysis:
                            1.  Summarize in not more than 3 points, make sure there is no formatting issue"""



                            response = finbot.call_ai(summarise_prompt)
                            st.markdown(response.text)
                            finbot.textToSpeech(response.text)
                

                budget = account.BudgetManager.viewBudget()
                # if not budget.empty:
                #     pass
                #     #calculate Monthly expense by category and see if ar espendign more than budget
                st.divider()
                if not df_expense.empty and not df_income.empty and not budget.empty:


                        # Ensure proper datetime
                    df_expense['date'] = pd.to_datetime(df_expense['date'])
                    df_income['date'] = pd.to_datetime(df_income['date'])

                    df_expense['month'] = df_expense['date'].dt.strftime('%b %Y')
                    df_income['month'] = df_income['date'].dt.strftime('%b %Y')

                    # Group income per month
                    income_by_month = df_income.groupby("month")["amount"].sum().reset_index()
                    income_by_month.columns = ["month", "Monthly Income"]

                    # Parse user budget dict
                    try:
                        budget_dict = eval(budget.iloc[0]["budget_str"])
                    except Exception:
                        st.warning("⚠️ Could not parse budget data")
                        budget_dict = {}

                    # Dropdown for category
                    all_categories = sorted(set(df_expense["category"]).union(budget_dict.keys()))
                    selected_category = st.selectbox("📂 Select Expense Category", all_categories)

                    # Actual expense per month for selected category
                    actuals = df_expense[df_expense["category"] == selected_category]
                    actuals_by_month = actuals.groupby("month")["amount"].sum().reset_index()
                    actuals_by_month.columns = ["month", "Actual Expense"]

                    # Budgeted = % of income
                    percent = budget_dict.get(selected_category, 0)
                    budgeted_by_month = income_by_month.copy()
                    budgeted_by_month["Budgeted Expense"] = (budgeted_by_month["Monthly Income"] * percent) / 100
                    budgeted_by_month = budgeted_by_month[["month", "Budgeted Expense"]]

                    # Merge actual & budgeted
                    comparison_df = pd.merge(budgeted_by_month, actuals_by_month, on="month", how="outer").fillna(0)
                    comparison_df["month_dt"] = pd.to_datetime(comparison_df["month"], format="%b %Y")
                    comparison_df.sort_values("month_dt", inplace=True)

                    # Summary for selected category
                    total_budget = comparison_df["Budgeted Expense"].sum()
                    total_actual = comparison_df["Actual Expense"].sum()
                    diff = total_actual - total_budget
                    percent_diff = (diff / total_budget * 100) if total_budget > 0 else 0

                    # 📝 Summary message
                    st.markdown(f"""
                    ##### 📊 Summary for **{selected_category}**
                    - 🔸 **Total Budgeted**: ₹{total_budget:,.2f}
                    - 🔹 **Total Spent**: ₹{total_actual:,.2f}
                    - {"🟢 Under budget" if diff < 0 else "🔴 Over budget"} by ₹{abs(diff):,.2f} ({percent_diff:+.1f}%)
                    """)

                    # Melt for plot
                    melted = comparison_df.melt(id_vars="month", value_vars=["Budgeted Expense", "Actual Expense"])

                    # Base line chart
                    fig = px.line(
                        melted,
                        x="month",
                        y="value",
                        color="variable",
                        markers=True,
                        title=f"📈 Budget vs Actual for {selected_category}",
                        labels={"value": "Amount (₹)", "month": "Month", "variable": "Type"},
                        color_discrete_map={
                            "Budgeted Expense": "orange",
                            "Actual Expense": "blue"
                        }
                    )

                    # 🔴 Highlight overspending months
                    overspent = comparison_df[comparison_df["Actual Expense"] > comparison_df["Budgeted Expense"]]
                    for _, row in overspent.iterrows():
                        fig.add_annotation(
                            x=row["month"],
                            y=row["Actual Expense"],
                            text="🔺 Over",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowcolor="red",
                            font=dict(color="red", size=12),
                            yshift=10
                        )

                    col5, col6 = st.columns([2,1])

                    with col5:
                        st.plotly_chart(fig, use_container_width=True)
                    with col6:
                        if st.button("💡Generate Insight",key='gi2'):
                            with st.spinner("Thinking with Gemini..."):
                                df_expense_chat = account.expenseList()
                                df_budget_chat = account.BudgetManager.viewBudget()
                                df_budget_chat = df_budget_chat[['budget_str','short_term_goal','long_term_goal']]
                                df_budget_chat.columns = ['Maximum Expense budget','short term goal','long term goal']


                                parent_prompt = """I have monthly expense ("Cash Out") and Budget Allocation data for the past 12 months.
                                
                                Here is the data in JSON format:
                                Cash Out: {}
                                Budget Allocation: 

                                """.format(df_expense_chat.to_json(),df_budget_chat.iloc[0].to_json())

                                summarise_prompt= parent_prompt+"""
                                    Please perform the following analysis:
                                    1. Do not provide the data in response 
                                    2. Analyze {} expense category specifically, providing details on its actual spending, its allocated budget, and the variance (over or under budget), percentage average  monthly increase over for the past 12 months. Identify any trends or notable spikes/drops in spending within this category.
                                    3. Summarize in not more than 3 points, make sure there is no formatting issue""".format(selected_category)



                                response = finbot.call_ai(summarise_prompt)
                                st.markdown(response.text)
                                finbot.textToSpeech(response.text)


                    



except Exception as ex:
    st.error(f"An error occurred: {ex}")
    # st.success('Refresh Page')
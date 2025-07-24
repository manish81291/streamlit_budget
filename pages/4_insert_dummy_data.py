import streamlit as st
from utils.dummy_data import  InsertIncome,InsertExpense

with st.form("add_data"):
    submit_add_data= st.form_submit_button("Add dummy data ➕")

    if submit_add_data:
        a = InsertIncome()
        b = InsertExpense()

        a.addIncome()
        b.addExpense()

        st.success('data inserted')
import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import sqlite3
import time
from auth import AuthManager

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
    
            with tab2:
                auth.sign_up()
        else:
            Authenticator.logout(location='sidebar')
            st.header(f'Welcome  :green[*{st.session_state.get("username")}*] 👤',divider='gray')
            


except Exception as ex:
    st.error(f"An error occurred: {ex}")
    # st.success('Refresh Page')
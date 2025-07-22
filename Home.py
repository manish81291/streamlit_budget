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
# st.title("Finfluencer")
# st.write("An AI powered budgeting app.")

try:

    users = auth.fetch_users()

    if not users:
        auth.sign_up()
    else:
 
        credentials = {'usernames': {}}
        usernames = []
        for user in users:
             usernames.append(user[1])
             credentials['usernames'][user[1]] = {'name': user[0], 'password': user[2]}

        
        Authenticator = stauth.Authenticate(credentials, cookie_name='Finfluencer', key='Finfluencer', cookie_expiry_days=4)

        Authenticator.login(location='main',key='Login')

        if st.session_state.get('authentication_status'):
            Authenticator.logout()
            st.write(f'Welcome *{st.session_state.get("username")}*')
            st.title('Some content')
            st.subheader('This is the home page')
        elif st.session_state.get('authentication_status') is False:
            st.error('Username/password is incorrect')
        elif st.session_state.get('authentication_status') is None:
            st.warning('Please enter your username and password')




        # info, info1 = st.columns(2)

        # if not authentication_status:
        #     auth.sign_up()

        # if username:
        #     if username in usernames:
        #         if authentication_status:
        #             # let User see app
        #             st.sidebar.subheader(f'Welcome {username}')
        #             Authenticator.logout('Log Out', 'sidebar')

        #             st.subheader('This is the home page')
        #             st.markdown(
        #                 """
        #                 ---
        #                 Created with ❤️ by SnakeByte
                        
        #                 """
        #             )

        #         elif not authentication_status:
        #             with info:
        #                 st.error('Incorrect Password or username')
        #         else:
        #             with info:
        #                 st.warning('Please feed in your credentials')
        #     else:
        #         with info:
        #             st.warning('Username does not exist, Please Sign up')

except Exception as ex:
    st.error(f"An error occurred: {ex}")
    # st.success('Refresh Page')
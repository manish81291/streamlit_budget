import streamlit as st
from utils.accountManager import Account  
import time  
from auth import AuthManager
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Business Profile', page_icon='')
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
    st.toast("Please log in to continue! 😊, Redirecting to Login Page..")
    time.sleep(2)
    st.switch_page('Home.py')  # Redirect to Home page if not authenticated
    st.stop()

Authenticator.logout(location='sidebar')


username = st.session_state.username
account = Account(username=username)



st.header("📙 Business Profile")
st.divider()

business_name = None
business_type = None
business_open_date = None
business_size = None
business_location = None

profile = account.ProfileManager.viewProfile()
if not profile.empty:
    business_name = profile.iloc[0]['business_name']
    business_type = profile.iloc[0]['business_type']
    business_open_date = profile.iloc[0]['business_open_date']
    business_size = profile.iloc[0]['business_size']
    business_location = profile.iloc[0]['business_location']

with st.form("profile_form"):
    business_name = st.text_input("Business Name",value=business_name)
    business_type = st.text_input("Business Type",value=business_type)
    business_open_date = st.date_input("Business Open Date",value=business_open_date if business_open_date else "today")
    business_size = st.selectbox("Business Size", ["Small", "Medium", "Large"],index=["Small", "Medium", "Large"].index(business_size) if business_size else 0)
    business_location = st.text_input("Business Location",value=business_location)
    submit_profile = st.form_submit_button("Update Profile")
    if submit_profile:
        if not business_name or not business_type or not business_location:
            st.warning("Please fill in all fields.",icon="⚠️")
            st.stop()
        # Update Profile in DB
        if not profile.empty:
            account.ProfileManager.updateProfile(business_name, business_type, business_open_date, business_size, business_location)
        else:
            account.ProfileManager.addProfile(business_name, business_type, business_open_date, business_size, business_location)
        st.success("Profile updated successfully!")
        time.sleep(1.5)  
        st.rerun()
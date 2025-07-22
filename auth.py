import sqlite3
import streamlit as st
import hashlib
import datetime
import re
import streamlit_authenticator as stauth

class AuthManager:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Create users table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email TEXT UNIQUE,
                                username TEXT UNIQUE,
                                password TEXT)''')
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email, username, password):
        try:
            self.cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists

    def login_user(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return self.cursor.fetchone() is not None
    
    def fetch_users(self):
        self.cursor.execute("SELECT email, username, password FROM users")
        users = self.cursor.fetchall()
        return users
    
    def validate_email(self, email):
        """Validate email format."""
        # Simple regex pattern for basic email validation
        # This can be improved with more complex patterns if needed
        pattern = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com
        if re.match(pattern, email):
            return True
        return False

    def get_user_emails(self,email):
        """
        Fetch User Emails
        :return List of user emails:
        """
        self.cursor.execute("SELECT * FROM users WHERE email=?", [email])
        return self.cursor.fetchone() is None
    
    def get_usernames(self,username):
        """
        Fetch Usernames
        :return List of user usernames:
        """
        self.cursor.execute("SELECT * FROM users WHERE username=?", [username])
        return self.cursor.fetchone() is None

    def validate_username(self, username):
        """
        Checks Validity of userName
        :param username:
        :return True if username is valid else False:
        """

        pattern = "^[a-zA-Z0-9]*$"
        if re.match(pattern, username):
            return True
        return False
    
    def sign_up(self):
        with st.form(key='signup', clear_on_submit=True):
            st.subheader(':green[Sign Up]')
            email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
            username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
            password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

            if email:
                if self.validate_email(email):
                    if self.get_user_emails(email):
                        if self.validate_username(username):
                            if self.get_usernames(username):
                                if len(username) >= 2:
                                    if len(password1) >= 6:
                                        if password1 == password2:
                                            # Add User to DB
                                            self.register_user(email, username, password1)
                                            st.success('Account created successfully!!')
                                            st.balloons()
                                        else:
                                            st.warning('Passwords Do Not Match')
                                    else:
                                        st.warning('Password is too Short')
                                else:
                                    st.warning('Username Too short')
                            else:
                                st.warning('Username Already Exists')

                        else:
                            st.warning('Invalid Username')
                    else:
                        st.warning('Email Already exists!!')
                else:
                    st.warning('Invalid Email')
            st.form_submit_button('Sign Up')
import streamlit as st
import re
from db_manager import register_user

def register_page():

    st.markdown(
        """ 
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://media.istockphoto.com/id/1880065388/vector/digital-technology-futuristic-internet-network-connection-blue-white-background-cyber-nano.jpg?s=612x612&w=0&k=20&c=pIJI9mCFKjdRxWC0O4mDnakr7f6rCQT3nvzC5qrIyls=');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.6);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Center the registration form container using Streamlit form layout
    col,col2,col3=st.columns([1,4,1])

    with col2.form(key="register_form"):
        # Title
        st.title("Sign Up🔐")

        # Form Fields
        col1,col2=st.columns(2)
        name = col1.text_input("Name")
        email = col2.text_input("Email")
        col1,col2=st.columns(2)
        age = col1.number_input('Enter Age',value=18)
        user=col2.selectbox('Select User Type',['Pregnant','Normal'])
        otp=None
        col1, col2 = st.columns(2)
        password = col1.text_input("Password", type="password")
        retype_password = col2.text_input("Retype Password", type="password")

        # Submit Button inside the form
        register_button = st.form_submit_button("Register",type='primary')

        # Handling form submission
        if register_button:
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                st.error("Invalid Email!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif password != retype_password:
                st.error("Passwords do not match!")
            else:
                if register_user(name, email,age,otp,user, password):
                    st.markdown(
                        """
                        <div style="text-align: center; padding: 1px; background-color: green; border-radius: 1px; border: 1.5px solid black; margin-bottom: 20px;">
                            <p style="color: black; font-size: 20px;"><b>Registration Successful! Please login to continue.</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="text-align: center; padding: 1px; background-color: red; border-radius: 1px; border: 1.5px solid black; margin-bottom: 20px;">
                            <p style="color: black; font-size: 20px;"><b>Registration Failed! Email already exists.</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

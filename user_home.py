import streamlit as st
from streamlit_option_menu import option_menu
from db_manager import fetch_details
from pregnant import pregnant_page
from normal import normal_page
def user_home_page():
    # Navigation menu for user dashboard
    user=st.session_state['user']
    if user[5]=='Pregnant':
        pregnant_page()
    if user[5]=='Normal':
        normal_page()




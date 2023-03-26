# streamlit_app.py

import streamlit as st
from PIL import Image

st.session_state["password_correct_global"] = False

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct. 
        st.session_state["password_correct_global"] = True #Custom ADD
        st.balloons()  #Custom ADD
        return True

if check_password():
    aldo_logo = Image.open('./assets/aldo_logo.png')
    st.image(aldo_logo, width = 100)

    st.title("Alassane's apps")
    st.title("for ALDO - Consumer Experience")
    st.title("")
    st.header("⬅ Use the menu on the left to navigate 🚀")

    

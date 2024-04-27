import sqlite3
import streamlit as st
import re

def get_connection():
    return sqlite3.connect('diabetesgit.db')

def create_account(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    if not name or not email or not password:
        cursor.close()
        conn.close()
        return "Please enter all fields"
    try:
        cursor.execute("INSERT INTO patienttable (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        user_id = cursor.lastrowid  # Get the ID of the newly inserted row
        cursor.close()
        conn.close()
        return user_id
    except Exception as e:
        cursor.close()
        conn.close()
        print("Error creating account:", e)
        return False

def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    if not email or not password:
        cursor.close()
        conn.close()
        return "Please enter all fields"
    cursor.execute("SELECT * FROM patienttable WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result  # Return user details if login successful
    else:
        return "Invalid email or password"

def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def app():
    no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    # Check if user is logged in
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False

    # If user is already logged in, display user details and options
    if st.session_state.user_logged_in:
        user_details = st.session_state.user_details
        st.write(f"Welcome, {user_details['name']}")
        st.write(f"Email: {user_details['email']}")
        if st.button("Go to My Account"):
            st.write("Redirecting to patient page...")
            st.switch_page("pages/patient.py")
        if st.button("Logout"):
            st.session_state.user_logged_in = False
            st.write("Logged out successfully")
            st.button("Login Again")  # Button to allow users to log in again

    else:
        option = st.radio("Select Option",["Login", "Sign up"],
        captions = ["If you do not have account Signup.", "By signing you can create an account."])
        st.markdown("""<style>
                        div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
                        font-size: 32px;}
                        </style>""", unsafe_allow_html=True)
        # Login form
        if option == "Login":
            st.subheader("Login")
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            if st.button("Login"):
                result = login(login_email, login_password)
                if isinstance(result, tuple):
                    user_details = {'id': result[0], 'name': result[1], 'email': result[2]}
                    st.session_state.user_logged_in = True
                    st.session_state.user_details = user_details
                    st.success("Login successful")
                    st.switch_page("pages/patient.py")
                else:
                    st.error(result)

        # Signup form
        elif option == "Sign up":
            st.subheader("Signup")
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                # Check if email is valid
                if not is_valid_email(email):
                    st.warning("Please enter a valid email address.")
                else:
                    # Check if email already exists
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM patienttable WHERE email = ?", (email,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        st.warning("An account with this email already exists. Please use a different email.")
                    else:
                        result = create_account(name, email, password)
                        if isinstance(result, int):
                            user_details = {'id': result, 'name': name, 'email': email}
                            st.session_state.user_logged_in = True
                            st.session_state.user_details = user_details
                            st.success("Account created successfully")
                            st.switch_page("pages/patient.py")
                        else:
                            st.error(result)
                            cursor.close()
                            conn.close()

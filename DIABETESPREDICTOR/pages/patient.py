import streamlit as st
from streamlit_option_menu import option_menu
from pages import patient_reports
from pages import prevention  # Adjusted import statement
from pages import patient_health
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)


def runpatient():
    app = option_menu('WELCOME',
                      ['MY HEALTH', 'MY REPORTS', 'MORE DETAILS'],
                      icons=['heart', 'report', 'details'],
                      menu_icon="cast",
                      default_index=0,
                      orientation="horizontal",
                      styles={
                          "container": {"padding": "0!important", "background-color": "#ffffff80"},
                          "icon": {"color": "black", "font-size": "20px"},
                          "nav-link": {"font-size": "15px", "text_align": "left", "margin": "0px",
                                       "--hover-color": "#eee"},
                          "nav-link-selected": {"background-color": "#50ABE7"},
                      })

    if app == "MY HEALTH":
        patient_health.patient_page()
    elif app == 'MY REPORTS':
        patient_reports.app()
    elif app == 'MORE DETAILS':
        prevention.app()

runpatient()

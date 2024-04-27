import sqlite3
import streamlit as st
import pandas as pd
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from reportlab.platypus import Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
import re

# Establish connection to SQLite database
conn = sqlite3.connect('DIABETESPREDICTOR/diabetes.db')
cursor = conn.cursor()

# Function to fetch patient data for the logged-in user
def fetch_patient_data(patient_id):
    try:
        # Open connection and create cursor within a context manager
        with sqlite3.connect('DIABETESPREDICTOR/diabetes.db') as conn:
            cursor = conn.cursor()
            
            # Define SQL query to fetch patient data
            sql = "SELECT * FROM patientsdata WHERE patient_id = ?"
            val = (patient_id,)
            
            # Execute query and fetch data
            cursor.execute(sql, val)
            patient_data = cursor.fetchall()
            
            return patient_data
    except Exception as e:
        print("Error fetching patient data:", e)
        return None


def generate_report_pdf(df, name, age, gender):
    filename = "patient_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    user_details_style = ParagraphStyle(name='UserDetails', parent=normal_style, fontSize=14)

    elements = []

    name_paragraph = Paragraph(f"Name: {name}", user_details_style)
    age_paragraph = Paragraph(f"Age: {age}", user_details_style)
    gender_paragraph = Paragraph(f"Gender: {gender}", user_details_style)

    elements.append(name_paragraph)
    elements.append(Spacer(1, 6))
    elements.append(age_paragraph)
    elements.append(Spacer(1, 6))
    elements.append(gender_paragraph)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Here are your prediction reports"))
    elements.append(Spacer(1, 12))

    columns_to_include = ["created_at", "Symptoms", "Prediction"]
    truncated_df = df[columns_to_include]
    col_widths = [100] * len(truncated_df.columns)

    data = [truncated_df.columns.tolist()] + truncated_df.values.tolist()
    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    
    return filename

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def app():
    no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("You must be logged in to view your patient data.")
        return

    patient_id = st.session_state.user_details['id']
    
    patient_data = fetch_patient_data(patient_id)

    st.subheader("Generate Your Reports - Click On Generate")
    if not patient_data:
        st.write("No patient data found.")
    else:
        df = pd.DataFrame(patient_data, columns=["ID", "created_at", "patient_id", "age", "gender", "Polyuria", "Polydipsia",
                                                        "Sudden_Weight_Loss", "Weakness", "Polyphagia",
                                                        "Genital_Thrush", "Visual_Blurring", "Itching",
                                                        "Irritability", "Delayed_Healing", "Partial_Paresis",
                                                        "Muscle_Stiffness", "Alopecia", "Obesity", "Prediction"])

        if 'Symptoms' not in df.columns:
            symptom_columns = [col for col in df.columns if df[col].eq('Yes').any()]
            df['Symptoms'] = df[symptom_columns].apply(lambda row: '\n '.join(row.index[row == 'Yes']), axis=1)

        st.dataframe(df)

        user_name = st.text_input("Enter Your Name")
        user_age = st.number_input("Enter Your Age", min_value=25, max_value=65, step=1)
        user_gender = st.radio("Select Your Gender", ["Male", "Female"])

        selected_ids = st.multiselect("Select IDs for Report Generation (Leave empty to generate reports for all IDs)", df["ID"].unique())

        if not selected_ids:
            selected_ids = df["ID"].unique()

        filtered_df = df[df["ID"].isin(selected_ids)]

        if st.button("GENERATE"):
            if not filtered_df.empty:
                filename = generate_report_pdf(filtered_df, user_name, user_age, user_gender)
                with open(filename, "rb") as f:
                    pdf_data = f.read()
                pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
                href = f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="{filename}">Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
                os.remove(filename)
            else:
                st.write("No data selected for report generation.")

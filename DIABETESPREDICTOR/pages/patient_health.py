import streamlit as st
import joblib
import numpy as np
import sqlite3

# Connect to SQLite database
db_connection = sqlite3.connect('DIABETESPREDICTOR/diabetes.db')

def predict_diabetes(age, gender, *symptoms):
    # Load the trained model and scaler
    RF_classifier = joblib.load(open('DIABETESPREDICTOR/Backend/diabetic_predictor.pkl','rb'))
    sc = joblib.load(open('DIABETESPREDICTOR/Backend/Standard_Scalar.pkl','rb'))

    # Transform input features and make prediction
    prediction = RF_classifier.predict(sc.transform(np.array([[age, gender, *symptoms]])))
    return prediction

from datetime import datetime

def save_patient_data(patient_id, age, gender, symptoms, prediction):
    try:
        # Open connection and create cursor within a context manager
        with sqlite3.connect('DIABETESPREDICTOR/diabetes.db') as conn:
            cursor = conn.cursor()
            
            # Convert boolean values to "Yes" or "No"
            symptoms = ["Yes" if symptom else "No" for symptom in symptoms]
            if prediction:
                prediction = 'Positive'
            else:
                prediction = 'Negative'
            if gender == 0:
                gender = "Female"
            else:
                gender = "Male"
                
            # Save patient data to the database
            cursor.execute("""
            INSERT INTO patientsdata (patient_id, age, gender, Polyuria, Polydipsia, Sudden_Weight_Loss, Weakness, Polyphagia, Genital_Thrush, Visual_Blurring, Itching, Irritability, Delayed_Healing, Partial_Paresis, Muscle_Stiffness, Alopecia, Obesity, Prediction) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, age, gender, *symptoms, prediction))

            conn.commit()
    except Exception as e:
        print("Error saving patient data:", e)



def patient_page():
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("You must be logged in to view your patient data.")
        return
    no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)
    st.title("CHECK YOUR HEALTH")
    warning_css = """
            <style>
                .warning-message {
                    background-color: #ffcccb;
                    color: #8b0000;
                    padding: 10px;
                    border-radius: 5px;
                    border: 2px solid #8b0000;
                    font-size: 18px;
                    font-weight: bold;
                }
            </style>
            """
    # Define custom CSS for success message
    success_css = """
    <style>
        .success-message {
            background-color: #90ee90;
            color: #006400;
            padding: 10px;
            border-radius: 5px;
            border: 2px solid #006400;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """

    # Apply custom CSS
    st.markdown(success_css, unsafe_allow_html=True)
    # Apply custom CSS
    st.markdown(warning_css, unsafe_allow_html=True)
    # Age and Gender
    # Age input with validation
    age = st.number_input("What is your Age?", min_value=0, max_value=120, value=30, step=1, format="%d")
    if age < 25 or age > 60:
        st.error("Age must be between 25 and 65.")
    else:

        gender = st.radio("What is your Gender?", ("Male", "Female"))

        # Split symptoms into two columns
        symptoms = [
        "Do you urinate frequently?",  # Polyuria
        "Do you feel unusually thirsty?",  # Polydipsia
        "Have you experienced sudden weight loss?",  # Sudden Weight Loss
        "Do you feel weak or fatigued?",  # Weakness
        "Do you have an increased appetite?",  # Polyphagia
        "Have you had recurring genital infections?",  # Genital Thrush
        "Do you experience blurry vision?",  # Visual Blurring
        "Do you suffer from itching, especially in the genital area?",  # Itching
        "Are you irritable or experiencing mood changes?",  # Irritability
        "Do you notice that your wounds take longer to heal?",  # Delayed Healing
        "Do you have numbness, tingling, or pain in your extremities?",  # Partial Paresis
        "Do you experience muscle stiffness?",  # Muscle Stiffness
        "Have you noticed hair loss?",  # Alopecia
        "Are you overweight or obese?"  # Obesity
    ]
        st.markdown("""
        <div style="text-align:center; background-color:#f0f0f0; padding:10px;">
            <h3 style="color:#0278ae;">SELECT SYMPTOMS YOU HAVE</h3>
        </div>
    """, unsafe_allow_html=True)

    # Add a line space
        st.write("")
        half_len = len(symptoms) // 2
        col1, col2 = st.columns(2)

        # First column with first 7 symptoms
        with col1:
            
            selected_symptoms_1 = []
            for i, symptom in enumerate(symptoms[:half_len]):
                selected = st.checkbox(symptom)
                selected_symptoms_1.append(selected)

        # Second column with remaining symptoms
        with col2:
            
            selected_symptoms_2 = []
            for i, symptom in enumerate(symptoms[half_len:], start=half_len):
                selected = st.checkbox(symptom)
                selected_symptoms_2.append(selected)

        # Prediction button
        if st.button("Predict"):
            # Check if any symptoms are selected
            if not any(selected_symptoms_1) and not any(selected_symptoms_2):
                st.error("Please select at least one symptom before predicting.")
            else:
                all_selected_symptoms = selected_symptoms_1 + selected_symptoms_2
                user_id = st.session_state.user_details['id']  # Get user ID from session state
                prediction = predict_diabetes(age, 1 if gender == "Male" else 0, *all_selected_symptoms)
                if prediction == 1:
                    st.markdown('<p class="warning-message">You might have Diabetes. Please consult with a Doctor.</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="success-message">Hurray! You don\'t have Diabetes. Please consult with a Doctor for verification.</p>', unsafe_allow_html=True)
                    st.balloons()
                # Save patient data to database
                save_patient_data(user_id, age, 1 if gender == "Male" else 0, all_selected_symptoms,prediction)

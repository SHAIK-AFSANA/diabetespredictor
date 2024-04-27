import streamlit as st

def app():
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("You must be logged in to view your patient data.")
        return
    st.header("PREVENTION")
   

    # Dictionary mapping prevention measures to their descriptions
    prevention_data = {
        "Stay hydrated by drinking plenty of water throughout the day.": "Hydration is important for overall health. Drink at least 8 glasses of water daily.",
        "Avoid sugary drinks and excessive caffeine intake.": "Limit your consumption of sugary drinks and opt for healthier alternatives like water or herbal tea.",
        "Maintain a balanced diet with regular meals and healthy snacks.": "Eat a variety of foods, including fruits, vegetables, whole grains, lean proteins, and healthy fats.",
        "Exercise regularly to improve muscle strength and overall health.": "Engage in physical activity for at least 30 minutes most days of the week.",
        "Focus on eating smaller, more frequent meals to help manage hunger.": "Eating smaller meals throughout the day can help stabilize blood sugar levels and prevent overeating.",
        "age hunger.":"Keeping track of your blood sugar levels regularly can help you understand how your body responds to different foods and activities."
    }

    # Display prevention measures in one column
    col1, col2 = st.columns([3, 4])
    with col1:
        for prevention_measure, description in prevention_data.items():
            st.write(description)
    # Display the image in the other column
    with col2:
        st.image("DIABETESPREDICTOR/Images/Complications-of-Diabetes.jpg", use_column_width=True)


     # Treatment heading
    st.header("TREATMENT")
    # Introduction text
    st.write("""
    Treatment of diabetes depends on the type of diabetes you have. It also depends on whether you have any other health conditions or not.
    """)

    # Treatment information dictionary
    treatment_info = {
        "Type-1 Diabetes": "In type-1 diabetes, pancreatic cells do not produce insulin. Patients with type-1 diabetes need to take insulin injections daily.",
        "Type-2 Diabetes": "Doctors prescribe medications along with lifestyle changes like maintaining a healthy lifestyle, losing weight, and being physically active. Some medications may be prescribed for both diabetes and other conditions that can cause diabetes.",
        "Prediabetes": "The main concern of doctors is to control the symptoms of progressing diabetes and to treat the risk factors that can cause diabetes in the future. Treatment includes maintaining a healthy lifestyle, losing weight, and following a healthy diet such as the Mediterranean diet.",
        "Gestational Diabetes": "In gestational diabetes, blood sugar levels are not too high. Initially, doctors focus on modifying lifestyle and diet, recommending regular exercise. If blood glucose levels remain unbalanced, medication may be prescribed.",
         
    }

    # Display treatment information in four columns
    col1, col2, col3, col4 = st.columns(4)
    for i, (treatment, description) in enumerate(treatment_info.items()):
        if i % 4 == 0:
            container = col1
        elif i % 4 == 1:
            container = col2
        elif i % 4 == 2:
            container = col3
        else:
            container = col4

        with container:
            st.subheader(treatment)
            st.write(description)
    # Treatment information dictionary
    treatment_inf = {
        
        "Medication Working Mechanisms": "Medications for diabetes have various mechanisms, including stimulating pancreatic cells to synthesize more insulin, slowing glucose release from the liver, increasing urination to excrete excess glucose, and inhibiting the digestion of carbohydrates to improve insulin sensitivity.",
        "Food to Consume in Diabetes": "Consuming healthy foods helps in managing diabetes. Patients are advised to eat fruits, vegetables, foods high in fiber, whole grains, healthy fats like olive oil and nuts, and lean protein sources like fish and chicken."
    }

    # Display treatment information in two columns
    col1, col2 = st.columns([3, 3])
    with col1:
        # Display treatment images
        st.image("DIABETESPREDICTOR/Images/Complications-of-Diabetes.jpg",  use_column_width=True)

    with col2:
        # Display treatment information
        for treatment, description in treatment_inf.items():
            st.subheader(treatment)
            st.write(description)
    st.header("COMPLICATIONS")

    # Introduction text
    st.markdown("""
    Complications of diabetes can affect various parts of the body and can be serious if not managed properly. Here are some common complications associated with diabetes:
    """)

    # Complications information dictionary
    complications_info = {
        "Cardiovascular Disease": "Diabetes increases the risk of cardiovascular diseases such as heart attack, stroke, and peripheral artery disease.",
        "Nephropathy (Kidney Disease)": "Diabetes can damage the kidneys over time, leading to kidney disease and eventual kidney failure.",
        "Neuropathy (Nerve Damage)": "Nerve damage caused by diabetes can result in neuropathy, leading to symptoms such as tingling, numbness, and pain, especially in the hands and feet.",
        "Retinopathy (Eye Damage)": "Diabetic retinopathy is a common complication that can lead to vision loss or blindness if left untreated.",
        "Foot Complications": "Diabetes can cause nerve damage and poor blood flow to the feet, increasing the risk of foot ulcers, infections, and even amputation.",
        "Skin Complications": "People with diabetes are prone to skin problems such as bacterial and fungal infections, as well as diabetic dermopathy and necrobiosis lipoidica diabeticorum.",
        "Gastroparesis (Digestive Problems)": "Gastroparesis is a condition where the stomach takes too long to empty its contents, leading to digestive problems such as nausea, vomiting, and bloating.",
        
    }

    # Display complications information in two columns
    col1, col2 = st.columns([2, 1])
    for complication, description in complications_info.items():
        with col1:
            
            st.write(description)
    with col2:
            # Add images here
        st.image("DIABETESPREDICTOR/Images/Complications-of-Diabetes.jpg",  use_column_width=True)  # Placeholder for images, you can add image elements here using st.image()
    html_temp = """
        <div style="background-color:#0278ae;padding:5px">
        <h3 style="color:white;text-align:center;"><span style="float:right; font-style: italic;">PREVENTION IS BETTER THAN CURE...</span></h3>
        </div>
        <br>
        """
    st.markdown(html_temp, unsafe_allow_html=True)



            
            

    
    


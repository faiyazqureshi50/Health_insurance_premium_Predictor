import streamlit as st
from prediction_helper import predict  # Your prediction function
import pandas as pd
import os

# Set up Streamlit page configuration
st.set_page_config(page_title="Insurance Premium Predictor", layout="wide", initial_sidebar_state="expanded")

# CSS for styling like a professional website
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3 {
        text-align: center;
        color: #2c3e50;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .predict-btn {
        background-color: #2980b9;
        color: white;
        font-weight: 600;
        font-size: 16px;
        border-radius: 6px;
        padding: 12px 24px;
    }
    .result-box {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        font-size: 24px;
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        font-weight: bold;
        margin-top: 30px;
    }
    .stSelectbox > label, .stNumberInput > label {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("""
<h1>🏥 Premium Estimator</h1>
<p style='text-align:center; color:#34495e; font-size:18px;'>Estimate your health insurance premium with precision.</p>
""", unsafe_allow_html=True)

# Input sections
st.markdown("""<h2>👤 Personal & Lifestyle Info</h2>""", unsafe_allow_html=True)

# Categorical input options
options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Married', 'Unmarried'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High Blood Pressure', 'Diabetes & High BP',
        'Thyroid', 'Heart Disease', 'BP & Heart Disease', 'Diabetes & Thyroid',
        'Diabetes & Heart Disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Form layout
with st.form("insurance_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox('⚧️ Gender', options['Gender'])
        bmi_category = st.selectbox('⚖️ BMI Category', options['BMI Category'])
        employment_status = st.selectbox('💼 Employment Status', options['Employment Status'])
        smoking_status = st.selectbox('🚬 Smoking Status', options['Smoking Status'])

    with col2:
        age = st.number_input('🎂 Age', min_value=18, max_value=100, value=30)
        income_lakhs = st.number_input('💰 Annual Income (in Lakhs)', min_value=0.0, max_value=200.0, value=10.0)
        number_of_dependants = st.number_input('👨‍👩‍👧‍👦 Dependants', 0, 20, 1)
        marital_status = st.selectbox('💍 Marital Status', options['Marital Status'])

    with col3:
        region = st.selectbox('🌎 Region', options['Region'])
        genetical_risk = st.number_input('🧬 Genetical Risk (0=Low, 5=High)', 0, 5, 2)
        insurance_plan = st.selectbox('📜 Insurance Plan', options['Insurance Plan'])
        medical_history = st.selectbox('🏥 Medical History', options['Medical History'])

    # Submit button
    submit = st.form_submit_button('🎯 Predict Premium', use_container_width=True)

    # Gather inputs
    inputs = {
        'Age': age,
        'Income in Lakhs': income_lakhs,
        'Number of Dependants': number_of_dependants,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

# Prediction Output
if submit:
    with st.spinner("⏳ Calculating your premium..."):
        result = predict(inputs)
        try:
            result = float(result)
            formatted = f"₹ {result:,.2f}"
        except:
            formatted = str(result)

    st.balloons()
    st.success("Prediction Successful! 🎉")
    st.markdown(f"<div class='result-box'>💰 Estimated Premium: {formatted}</div>", unsafe_allow_html=True)

    # Save form data to Excel
    submission_df = pd.DataFrame([inputs])
    submission_df['Predicted Premium'] = formatted
    submission_file = "submissions.xlsx"

    if os.path.exists(submission_file):
        existing_df = pd.read_excel(submission_file)
        updated_df = pd.concat([existing_df, submission_df], ignore_index=True)
    else:
        updated_df = submission_df

    updated_df.to_excel(submission_file, index=False)

# Footer
st.markdown("""
---
<p style='text-align:center; color:gray;'>Crafted with care using Streamlit | © 2025</p>
""", unsafe_allow_html=True)

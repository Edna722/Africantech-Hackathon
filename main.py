import streamlit as st
import os
import pickle
import pandas as pd
from PIL import Image

# Function to simulate real-time data from CGMS device
import time
import random


def get_realtime_data():
    # Replace this function with code to retrieve real-time data from CGMS device
    # For demonstration purposes, we are using random data
    glucose_level = 100 + 10 * (random.random() - 0.5)  # Simulate random glucose level
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
    return glucose_level, timestamp


# Function to preprocess input data (if needed)
def preprocess_input(data):
    # One-hot encode categorical features
    categorical_cols = ['gender', 'hypertension', 'heart_disease', 'smoking_history']
    data_encoded = pd.get_dummies(data, columns=categorical_cols)

    # Ensure all features used during training are present in the input data
    # Add missing features with default value 0
    all_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level',
                    'gender_Female', 'gender_Male', 'gender_Other',
                    'hypertension_0', 'hypertension_1',
                    'heart_disease_0', 'heart_disease_1',
                    'smoking_history_former', 'smoking_history_never', 'smoking_history_current']

    missing_features = set(all_features) - set(data_encoded.columns)
    for feature in missing_features:
        data_encoded[feature] = 0

    # Reorder columns to match the order used during training
    data_encoded = data_encoded[all_features]

    return data_encoded

# Load the pre-trained Gradient Boosting model
model_file_path = "C:/Users/wanji/Desktop/african techgirl hackathon/Africantech-Hackathon/gradient_boost_model.pkl"
with open(model_file_path, "rb") as f:
    gb_model_updated = pickle.load(f)

# Set Streamlit app background color
st.markdown('<style>body{background-color: #F0F8FF;}</style>', unsafe_allow_html=True)

# Load and display the image
image_path = "C:/Users/wanji/Desktop/african techgirl hackathon/Africantech-Hackathon/image 3.jpg"
image = Image.open(image_path)
st.image(image, caption="Your Image Caption", use_column_width=True)

# Add a title to the app
st.title("African TechGirl Hackathon - Diabetes Prediction")

# User authentication
st.sidebar.title("Login / Sign Up")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# Simulate sign up process (for demonstration purposes)
if st.sidebar.button("Sign Up"):
    # Replace this with your actual sign-up logic
    # For demonstration purposes, we'll assume all sign-ups are successful
    st.success("Account created successfully. You can now log in.")

# Simulate login process (for demonstration purposes)
if st.sidebar.button("Login"):
    # Replace this with your actual login logic
    # For demonstration purposes, we'll assume all logins are successful
    st.success("Logged in as {}".format(user_email))

# If the user is not logged in, stop the app
if not user_email:
    st.warning("Please log in or sign up to continue.")
    st.stop()

# Add some explanation or instructions
st.write("Please input the following features to make predictions.")

# Get user input for numerical features
age = st.number_input("Enter age:")
bmi = st.number_input("Enter bmi:")
HbA1c_level = st.number_input("Enter HbA1c_level:")
blood_glucose_level = st.number_input("Enter blood_glucose_level:")

# Get user input for categorical features
gender = st.selectbox("Select gender:", ["Female", "Male", "Other"])
hypertension = st.selectbox("Select hypertension:", ["No", "Yes"])
heart_disease = st.selectbox("Select heart_disease:", ["No", "Yes"])
smoking_history = st.selectbox("Select smoking_history:", ["Never", "Former", "Current"])

# Add a "Predict" button
if st.button("Predict"):
    # Convert user input to a DataFrame
    input_data = pd.DataFrame({
        "age": [age],
        "bmi": [bmi],
        "HbA1c_level": [HbA1c_level],
        "blood_glucose_level": [blood_glucose_level],
        "gender": [gender],
        "hypertension": [hypertension],
        "heart_disease": [heart_disease],
        "smoking_history": [smoking_history]
    })

    # Preprocess the input data
    input_df = preprocess_input(input_data)

    # Make predictions using the pre-trained Gradient Boosting model
    predictions_gb_updated = gb_model_updated.predict(input_df)

    # Display the predictions
    st.subheader("Predictions:")
    if predictions_gb_updated[0] == 0:
        st.write("Diabetes: No")
    else:
        st.write("Diabetes: Yes")

# Simulate real-time data
# (Since we don't have the actual CGMS device data, this part is commented out)
# glucose_level, timestamp = get_realtime_data()
# st.subheader("Real-Time Data:")
# st.write("Glucose Level:", glucose_level)
# st.write("Timestamp:", timestamp)

# Check for critical glucose level and display a warning message
# (Since we don't have the actual CGMS device data, this part is commented out)
# if glucose_level > 180:
#     st.warning("Warning: High glucose level detected!")

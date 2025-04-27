import streamlit as st
import pandas as pd
import requests
from utils.auth_utils import validate_login, register_user
from utils.marketplace import marketplace_page
from utils.price_prediction import price_prediction_page
from utils.crop_recommendation import recommend_crops

# Set page configuration
st.set_page_config(page_title="AgriPredict", layout="wide")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None

# Login/Signup Page
if not st.session_state.authenticated:
    st.title("🔐 Login / Signup")

    # Tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["farmer", "company"])

        if st.button("Login"):
            if validate_login(username, password, role):
                st.session_state.authenticated = True
                st.session_state.role = role
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.header("Signup")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["farmer", "company"], key="signup_role")

        if st.button("Signup"):
            message = register_user(username, password, role)
            if "Account created" in message:
                st.success(message)
            else:
                st.error(message)

# Main App
else:
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Home", "Price Prediction", "Crop Recommendation", "Marketplace"])

    # Home Page
    if selected_page == "Home":
        st.title("🌾 AgriPredict - Home")
        st.markdown("""
        **Welcome to AgriPredict!**
        - AgriPredict is a comprehensive platform designed to empower farmers and agribusinesses.
        - With tools for price prediction, crop recommendation, and a marketplace for trading agricultural products, we aim to revolutionize the agricultural ecosystem.
        - Explore the platform to maximize your yields and profits.
        """)

    # Price Prediction Page
    elif selected_page == "Price Prediction":
        price_prediction_page()

    # Crop Recommendation Page
    elif selected_page == "Crop Recommendation":
        st.title("🌾 Crop Recommendation")

        # Inputs
        soil_type = st.selectbox("Select Soil Type", ["Loamy", "Sandy", "Clay"])
        land_size = st.number_input("Enter Land Size (in acres)", min_value=1.0)
        place = st.selectbox("Select Place", ["North Karnataka", "South Karnataka", "Central Karnataka"])

        if st.button("Get Recommendations"):
            # Prepare input data
            recommendations = recommend_crops(place, soil_type, land_size)

            # Display recommendations
            df = pd.DataFrame(recommendations)
            st.table(df)

    # Marketplace Page
    elif selected_page == "Marketplace":
        marketplace_page()

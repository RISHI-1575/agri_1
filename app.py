import streamlit as st
import pandas as pd
import requests
from utils.auth_utils import validate_login, register_user
from utils.marketplace import marketplace_page
from utils.price_prediction import price_prediction_page
from utils.crop_recommendation import recommend_crops

# Set page configuration
st.set_page_config(page_title="AgriPredict", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["Home", "Price Prediction", "Crop Recommendation", "Marketplace"])

# Home Page
if selected_page == "Home":
    st.title("🌾 AgriPredict - Home")

    # Area Selection
    state = st.selectbox("Select Your State", ["Karnataka"])
    district = st.selectbox("Select Your District", ["Bangalore", "Mysore", "Hubli", "Mangalore"])

    # Weather API
    if st.button("Get Weather"):
        api_key = "your_openweather_api_key"  # Replace with your API key
        city = district
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            st.success(f"Weather in {city}: {weather}, Temperature: {temp}°C")
        else:
            st.error("Unable to fetch weather data. Please try again later.")

    # Farming Tips
    st.subheader("Farming Tips")
    st.markdown("""
    - Use high-quality seeds for better crop yield.
    - Practice crop rotation to maintain soil fertility.
    - Ensure proper irrigation and pest control.
    - Stay updated with market trends to maximize profits.
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

    if st.button("Get Recommendations"):
        # Prepare input data
        recommendations = recommend_crops("Karnataka", soil_type, land_size)

        # Display recommendations
        df = pd.DataFrame(recommendations)
        st.table(df)

        st.info("Note: These are tentative profits based on predicted prices and demand.")

# Marketplace Page
elif selected_page == "Marketplace":
    marketplace_page()

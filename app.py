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
        state = st.selectbox("Select Your State", ["Karnataka"])
        district = st.selectbox("Select Your District", ["Bangalore", "Mysore", "Hubli", "Mangalore"])
        if st.button("Get Weather"):
            api_key = "your_openweather_api_key"
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

    # Price Prediction Page
    elif selected_page == "Price Prediction":
        price_prediction_page()

    # Crop Recommendation Page
    elif selected_page == "Crop Recommendation":
        st.title("🌾 Crop Recommendation")
        soil_type = st.selectbox("Select Soil Type", ["Loamy", "Sandy", "Clay"])
        land_size = st.number_input("Enter Land Size (in acres)", min_value=1.0)
        irrigation = st.selectbox("Irrigation Type", ["Drip", "Sprinkler", "Flood"])
        harvest_season = st.selectbox("Preferred Harvest Season", ["Kharif", "Rabi", "Zaid"])
        if st.button("Get Recommendations"):
            recommendations = recommend_crops("Karnataka", soil_type, land_size, irrigation, harvest_season)
            df = pd.DataFrame(recommendations)
            st.table(df)

    # Marketplace Page
    elif selected_page == "Marketplace":
        marketplace_page()

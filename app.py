import streamlit as st
import pandas as pd
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
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Default to Home page

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
    # Feature menu box (displayed on all pages)
    menu_box_style = """
        <style>
        .menu-box {
            position: fixed;
            top: 50px;
            right: 50px;
            width: 300px;
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .menu-box h4 {
            font-size: 20px;
            margin-bottom: 15px;
            text-align: center;
        }
        div.stButton > button {
            font-size: 16px; /* Adjust button font size */
            width: 100%; /* Stretch buttons to full width */
            margin-bottom: 10px; /* Add space between buttons */
        }
        </style>
        <div class="menu-box">
            <h4>🌾 AgriPredict</h4>
    """
    st.markdown(menu_box_style, unsafe_allow_html=True)

    # Render buttons for navigation inside the menu box
    if st.button("🏠 Home", key="home"):
        st.session_state.current_page = "Home"
    if st.button("📈 Price Prediction", key="price_prediction"):
        st.session_state.current_page = "Price Prediction"
    if st.button("🌾 Crop Recommendation", key="crop_recommendation"):
        st.session_state.current_page = "Crop Recommendation"
    if st.button("🏪 Marketplace", key="marketplace"):
        st.session_state.current_page = "Marketplace"

    # Close the menu box HTML
    st.markdown("</div>", unsafe_allow_html=True)

    # Render the selected page
    if st.session_state.current_page == "Home":
        # Welcome message only on the Home page
        st.title("🌾 Welcome to AgriPredict!")
        st.markdown("""
        **A platform to help farmers and agribusinesses make informed decisions.**
        Navigate to different sections using the buttons in the menu box.
        """)

    elif st.session_state.current_page == "Price Prediction":
        price_prediction_page()

    elif st.session_state.current_page == "Crop Recommendation":
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

    elif st.session_state.current_page == "Marketplace":
        marketplace_page()

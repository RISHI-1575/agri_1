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
                # Update session state
                st.session_state.authenticated = True
                st.session_state.role = role

                # Rerun the app to reflect changes
                st.success("Login successful!")
                st.experimental_rerun()  # This should now work as expected
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
    # Keep the welcome message at the top for all pages
    st.title("🌾 Welcome to AgriPredict!")
    st.markdown("""
    **A platform to help farmers and agribusinesses make informed decisions.**
    Navigate to different sections using the buttons below.
    """)

    # Feature buttons in a line below the welcome message
    button_style = """
        <style>
        div.stButton > button {
            font-size: 18px; /* Increase font size */
            height: 50px; /* Adjust height */
            width: 100%; /* Stretch buttons to column width */
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = "Home"

    with col2:
        if st.button("📈 Price Prediction"):
            st.session_state.current_page = "Price Prediction"

    with col3:
        if st.button("🌾 Crop Recommendation"):
            st.session_state.current_page = "Crop Recommendation"

    with col4:
        if st.button("🏪 Marketplace"):
            st.session_state.current_page = "Marketplace"

    # Render the selected page
    if st.session_state.current_page == "Home":
        # Additional points about the project on the Home page
        st.markdown("### About AgriPredict")
        
        # Detailed explanation of features
        st.markdown("#### Data-Driven Insights")
        st.markdown("""
        1. Provides actionable insights by analyzing agricultural data such as soil types, crop patterns, and market trends.
        2. Helps farmers and agribusinesses make informed decisions to optimize productivity and profitability.
        3. Encourages sustainable farming practices by recommending data-driven strategies.
        4. Enables real-time monitoring and updates on agricultural trends, ensuring users stay ahead of challenges.
        """)
        
        st.markdown("#### Price Prediction")
        st.markdown("""
        1. Predicts the future prices of crops based on historical data and market conditions.
        2. Assists farmers in choosing the right time to sell their produce to maximize profits.
        3. Uses advanced machine learning algorithms to ensure accurate and reliable price forecasts.
        4. Helps mitigate risks by providing early warnings about potential price drops or market fluctuations.
        """)
        
        st.markdown("#### Crop Recommendation")
        st.markdown("""
        1. Suggests the most suitable crops for a specific region based on soil type, climate, and available land size.
        2. Enhances productivity by recommending crops that are best suited to the local environment.
        3. Provides region-specific recommendations that account for climatic conditions and water availability.
        4. Reduces trial-and-error farming, saving time, effort, and resources for farmers.
        """)
        
        st.markdown("#### Marketplace Integration")
        st.markdown("""
        1. Connects farmers directly with potential buyers, reducing dependency on intermediaries.
        2. Facilitates seamless transactions by providing a virtual marketplace for agricultural goods.
        3. Encourages transparency in pricing, ensuring fair trade practices for both farmers and buyers.
        4. Boosts farmers' income by providing access to a larger customer base, including businesses and distributors.
        """)
        
        st.markdown("#### User-Friendly Interface")
        st.markdown("""
        1. Designed to be intuitive and easy-to-use for both tech-savvy and non-tech-savvy users.
        2. Offers a simple and clean layout to ensure users can access features quickly and efficiently.
        3. Provides multilingual support to cater to users from diverse linguistic backgrounds.
        4. Ensures accessibility through mobile and web platforms, making it convenient for farmers in remote areas.
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

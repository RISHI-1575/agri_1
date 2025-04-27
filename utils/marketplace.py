import streamlit as st
import pandas as pd

MARKETPLACE_FILE = "data/marketplace_data.csv"

def marketplace_page():
    st.title("🛒 Marketplace")

    # Load marketplace data
    df = pd.read_csv(MARKETPLACE_FILE)
    st.dataframe(df)

    if st.session_state.role == "company":
        st.subheader("Post a Requirement")
        company = st.text_input("Company Name")
        crop = st.text_input("Crop")
        quantity = st.number_input("Quantity (kg)", min_value=1)
        price = st.number_input("Price (₹/kg)", min_value=1.0)
        deadline = st.date_input("Deadline")
        contact = st.text_input("Contact Info")

        if st.button("Submit"):
            new_entry = pd.DataFrame([[company, crop, quantity, price, deadline, contact]],
                                     columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(MARKETPLACE_FILE, index=False)
            st.success("Requirement posted successfully!")
    else:
        st.error("Only companies can post requirements.")

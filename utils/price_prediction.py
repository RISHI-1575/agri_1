import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def price_prediction_page():
    # Add a title for the price prediction page
    st.title("📈 Crop Price Prediction")

    # Load the pre-trained model
    with open("models/price_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Load historical price data
    df = pd.read_csv("data/price_data.csv")

    # User input for crop and city
    crop = st.selectbox("Select Crop", df["Crop"].unique())
    city = st.selectbox("Select City", df["City"].unique())

    # Filter data based on user input
    filtered = df[(df["Crop"] == crop) & (df["City"] == city)]

    if filtered.empty:
        st.error("No data available for the selected crop and city.")
    else:
        # Get the most recent data for prediction
        last_row = filtered.iloc[-1]
        month = pd.to_datetime(last_row["Date"]).month
        year = pd.to_datetime(last_row["Date"]).year

        # Predict prices for the next 6 months
        future_months = [(month + i - 1) % 12 + 1 for i in range(6)]
        predictions = model.predict(np.array(future_months).reshape(-1, 1))

        # Map future months to string labels (e.g., "Jan", "Feb")
        month_labels = [pd.Timestamp(f"{year}-{m:02d}-01").strftime("%b") for m in future_months]

        # Plot the historical and predicted prices
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Modal Price"], name="Historical Prices"))
        fig.add_trace(go.Scatter(x=month_labels, y=predictions, name="Predicted Prices"))
        st.plotly_chart(fig)

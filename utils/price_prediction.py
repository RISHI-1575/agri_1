import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def price_prediction_page():
    st.title("📈 Crop Price Prediction")

    try:
        # Load historical price data
        df = pd.read_csv("data/price_data.csv")

        # User input for crop and city
        crop = st.selectbox("Select Crop", df["Crop"].unique())
        city = st.selectbox("Select City", df["City"].unique())

        # Load the dictionary of pre-trained models
        with open("models/price_models.pkl", "rb") as f:
            crop_models = pickle.load(f)

        # Get the model for the selected crop
        model = crop_models.get(crop.lower())
        if model is None:
            st.error(f"No model found for the selected crop: {crop}")
            st.stop()

        # Filter data for the selected crop and city
        filtered = df[(df["Crop"] == crop) & (df["City"] == city)]

        if filtered.empty:
            st.error("No data available for the selected crop and city.")
            st.stop()

        # Sort data by date
        filtered = filtered.sort_values("Date")

        # Get the last available date and price
        last_date = pd.to_datetime(filtered["Date"].iloc[-1])
        last_price = filtered["Modal Price"].iloc[-1]

        # Define Seasonal Index for future months (Oct 2025 - Feb 2026)
        seasonal_indices = {
            "tomato": {10: 0.6, 11: 0.5, 12: 0.5, 1: 0.4, 2: 0.3},
            "banana": {10: 0.6, 11: 0.5, 12: 0.5, 1: 0.5, 2: 0.6},
            "mango": {10: 1.0, 11: 1.0, 12: 1.0, 1: 0.9, 2: 1.0},
            "onion": {10: 0.6, 11: 0.5, 12: 0.4, 1: 0.3, 2: 0.3},
            "carrot": {10: 0.7, 11: 0.8, 12: 0.6, 1: 0.7, 2: 0.8},
            "apple": {10: 0.5, 11: 0.5, 12: 0.5, 1: 0.5, 2: 0.6}
        }

        # Predict prices for the next 5 months
        future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 6)]
        future_months = [date.month for date in future_dates]
        predictions = []

        # Iteratively predict each month
        current_price = last_price
        for month in future_months:
            # Prepare features for the current month
            month_sin = np.sin(2 * np.pi * month / 12)
            month_cos = np.cos(2 * np.pi * month / 12)
            seasonal_index = seasonal_indices[crop.lower()][month]
            features = np.array([[month_sin, month_cos, current_price, seasonal_index]])

            # Predict the price
            pred = model.predict(features)[0]
            predictions.append(pred)

            # Update the lagged price for the next iteration
            current_price = pred

        # Convert predictions to numpy array
        predictions = np.array(predictions)

        # Constrain predictions to historical range (for realism)
        historical_min = filtered["Modal Price"].min()
        historical_max = filtered["Modal Price"].max()
        predictions = np.clip(predictions, historical_min * 0.9, historical_max * 1.1)

        if predictions is None or len(predictions) == 0:
            st.error("Unable to generate predictions. Please try again later.")
            st.stop()

        # Plot the data
        fig = go.Figure()

        # Historical Prices
        fig.add_trace(go.Scatter(
            x=filtered["Date"], 
            y=filtered["Modal Price"], 
            mode="lines+markers",
            name="Historical Prices"
        ))

        # Predicted Prices
        fig.add_trace(go.Scatter(
            x=[date.strftime("%Y-%m-%d") for date in future_dates], 
            y=predictions, 
            mode="lines+markers",
            name="Predicted Prices"
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            title=f"Price Prediction for {crop} in {city}",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()

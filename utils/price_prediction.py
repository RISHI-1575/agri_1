import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import pickle
from datetime import timedelta

def price_prediction_page():
    st.title("📈 Crop Price Prediction")

    try:
        # Load historical price data
        df = pd.read_csv("data/price_data.csv")
        df["Date"] = pd.to_datetime(df["Date"])

        # User input for crop and city
        crop = st.selectbox("Select Crop", df["Crop"].unique())
        city = st.selectbox("Select City", df["City"].unique())

        # Load the model and encoder
        with open("models/price_model.pkl", "rb") as f:
            saved_data = pickle.load(f)
            model = saved_data["model"]
            encoder = saved_data["encoder"]

        # Filter data for the selected crop and city
        filtered = df[(df["Crop"] == crop) & (df["City"] == city)].sort_values("Date")

        if filtered.empty:
            st.error("No data available for the selected crop and city.")
            return

        # Get the last available date and price
        last_date = filtered["Date"].iloc[-1]
        last_price = filtered["Modal Price"].iloc[-1]

        # Define seasonal indices for future months (Oct 2025 - Feb 2026)
        seasonal_indices = {
            "tomato": {10: 0.6, 11: 0.5, 12: 0.5, 1: 0.4, 2: 0.3},
            "banana": {10: 0.6, 11: 0.5, 12: 0.5, 1: 0.5, 2: 0.6},
            "mango": {10: 1.0, 11: 1.0, 12: 1.0, 1: 0.9, 2: 1.0},
            "onion": {10: 0.6, 11: 0.5, 12: 0.4, 1: 0.3, 2: 0.3},
            "carrot": {10: 0.7, 11: 0.8, 12: 0.6, 1: 0.7, 2: 0.8},
            "apple": {10: 0.5, 11: 0.5, 12: 0.5, 1: 0.5, 2: 0.6}
        }

        #  # Predict prices for the next 5 months
        future_dates = [last_date + timedelta(days=30 * i) for i in range(1, 6)]
        future_months = [(last_date.month + i - 1) % 12 + 1 for i in range(1, 6)]
        predictions = []

        # Prepare features for predictions
        crop_encoded = encoder.transform([[crop]])
        crop_encoded_df = pd.DataFrame(crop_encoded, columns=encoder.get_feature_names_out(["Crop"]))

        current_price = last_price
        for month in future_months:
            month_sin = np.sin(2 * np.pi * month / 12)
            month_cos = np.cos(2 * np.pi * month / 12)
            seasonal_index = seasonal_indices[crop.lower()][month]
            features = pd.concat([
                crop_encoded_df,
                pd.DataFrame([[month_sin, month_cos, seasonal_index, current_price]],
                             columns=["Month_sin", "Month_cos", "Seasonal_Index", "Lagged_Price"])
            ], axis=1)

            # Predict the price
            pred = model.predict(features)[0]
            predictions.append(pred)
            current_price = pred  # Update lagged price

        # Constrain predictions to historical range
        historical_min = filtered["Modal Price"].min()
        historical_max = filtered["Modal Price"].max()
        predictions = np.clip(predictions, historical_min * 0.9, historical_max * 1.1)

        # Plot the data
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered["Date"],
            y=filtered["Modal Price"],
            mode="lines+markers",
            name="Historical Prices"
        ))
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

if __name__ == "__main__":
    price_prediction_page()

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

        # Load the model and metadata
        with open("models/price_model.pkl", "rb") as f:
            saved_data = pickle.load(f)
            model = saved_data["model"]
            encoder = saved_data["encoder"]
            historical_stats = saved_data["historical_stats"]
            trend = saved_data["trend"]

        # Filter data for the selected crop and city
        filtered = df[(df["Crop"] == crop) & (df["City"] == city)].sort_values("Date")
        if filtered.empty:
            st.error("No data available for the selected crop and city.")
            return

        # Get the last available date and price
        last_date = filtered["Date"].iloc[-1]
        last_price = filtered["Modal Price"].iloc[-1]
        last_ma3 = filtered["Modal Price"].rolling(window=3, min_periods=1).mean().iloc[-1]

        # Seasonal indices for May 2025 - Sep 2025
        seasonal_indices = {
            "tomato": {5: 0.5, 6: 0.8, 7: 1.0, 8: 1.0, 9: 0.8},
            "banana": {5: 0.6, 6: 0.7, 7: 0.7, 8: 0.7, 9: 0.6},
            "mango": {5: 0.4, 6: 0.3, 7: 0.7, 8: 0.8, 9: 0.9},
            "onion": {5: 0.6, 6: 0.8, 7: 1.0, 8: 1.0, 9: 0.8},
            "carrot": {5: 0.6, 6: 0.5, 7: 0.5, 8: 0.5, 9: 0.6},
            "apple": {5: 0.5, 6: 0.5, 7: 0.5, 8: 0.5, 9: 0.5}
        }

        # Prepare features for predictions
        crop_encoded = encoder.transform([[crop]])
        crop_encoded_df = pd.DataFrame(crop_encoded, columns=encoder.get_feature_names_out(["Crop"]))
        crop_stats = historical_stats[historical_stats["Crop"] == crop].iloc[0]
        crop_trend = trend[crop]

        # Predict prices for the next 5 months
        future_dates = [last_date + timedelta(days=30 * i) for i in range(1, 6)]
        future_months = [5, 6, 7, 8, 9]  # May to Sep 2025
        predictions = []
        current_price = last_price
        current_ma3 = last_ma3

        for i, month in enumerate(future_months):
            month_sin = np.sin(2 * np.pi * month / 12)
            month_cos = np.cos(2 * np.pi * month / 12)
            seasonal_index = seasonal_indices[crop.lower()][month]
            features = pd.concat([
                crop_encoded_df,
                pd.DataFrame([[
                    month_sin, month_cos, seasonal_index, current_price, current_ma3,
                    crop_stats["min"], crop_stats["max"], crop_stats["mean"], crop_trend
                ]], columns=[
                    "Month_sin", "Month_cos", "Seasonal_Index", "Lagged_Price", "Price_MA3",
                    "min", "max", "mean", "Trend"
                ])
            ], axis=1)

            # Predict the price
            pred = model.predict(features)[0]
            predictions.append(pred)

            # Update lagged price and moving average
            current_price = pred
            current_ma3 = (current_ma3 * 3 - current_ma3 + pred) / 3  # Simplified MA update

        # Constrain predictions to historical range
        historical_min = filtered["Modal Price"].min()
        historical_max = filtered["Modal Price"].max()
        predictions = np.clip(predictions, historical_min * 0.85, historical_max * 1.15)

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

        # Display predictions
        st.write("### Predicted Prices")
        for date, price in zip(future_dates, predictions):
            st.write(f"{date.strftime('%Y-%m-%d')}: ₹{price:.2f}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    price_prediction_page()

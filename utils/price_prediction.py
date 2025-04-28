import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def price_prediction_page():
    st.title("📈 Crop Price Prediction")

    try:
        # Load the pre-trained model
        with open("models/price_model.pkl", "rb") as f:
            model = pickle.load(f)

        # Load historical price data
        df = pd.read_csv("data/price_data.csv")

        # User input for crop
        crop = st.selectbox("Select Crop", df["Crop"].unique())

        # Filter data for Bangalore and selected crop
        filtered = df[(df["Crop"] == crop) & (df["City"] == "Bangalore")]

        if filtered.empty:
            st.error("No data available for the selected crop in Bangalore.")
        else:
            # Get the most recent data for prediction
            last_row = filtered.iloc[-1]
            month = pd.to_datetime(last_row["Date"]).month
            year = pd.to_datetime(last_row["Date"]).year

            # Predict prices for the next 5 months
            future_months = [(month + i - 1) % 12 + 1 for i in range(1, 6)]
            predictions = model.predict(np.array(future_months).reshape(-1, 1))

            # Map future months to string labels (e.g., "May", "Jun")
            month_labels = [pd.Timestamp(f"{year}-{m:02d}-01").strftime("%b") for m in future_months]

            # Plot the historical and predicted prices
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered["Date"],
                y=filtered["Modal Price"],
                mode="lines+markers",
                name="Historical Prices"
            ))
            fig.add_trace(go.Scatter(
                x=month_labels,
                y=predictions,
                mode="lines+markers",
                name="Predicted Prices"
            ))
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

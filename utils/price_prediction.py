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

        # User input for crop and city
        crop = st.selectbox("Select Crop", df["Crop"].unique())
        city = st.selectbox("Select City", df["City"].unique())

        # Filter data for the selected crop and city
        filtered = df[(df["Crop"] == crop) & (df["City"] == city)]

        if filtered.empty:
            st.error("No data available for the selected crop and city.")
            st.stop()

        # Get the most recent data for prediction
        last_row = filtered.iloc[-1]
        month = pd.to_datetime(last_row["Date"]).month
        year = pd.to_datetime(last_row["Date"]).year

        # Predict prices for the next 5 months
        future_months = [(month + i - 1) % 12 + 1 for i in range(1, 6)]
        try:
            predictions = model.predict(np.array(future_months).reshape(-1, 1))

            if predictions is None or len(predictions) == 0:
                st.error("Unable to generate predictions. Please try again later.")
                st.stop()

            # Generate labels for future months
            month_labels = [pd.Timestamp(f"{year}-{m:02d}-01").strftime("%b") for m in future_months]

            # Plot the data
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
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred while generating predictions: {e}")
            st.stop()

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()

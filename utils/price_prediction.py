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

        # Sort data by date
        filtered = filtered.sort_values("Date")

        # Get the last available date
        last_date = pd.to_datetime(filtered["Date"].iloc[-1])

        # Predict prices for the next 5 months
        future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 6)]
        future_months = [date.month for date in future_dates]

        try:
            predictions = model.predict(np.array(future_months).reshape(-1, 1))

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
            st.error(f"An error occurred while generating predictions: {e}")
            st.stop()

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def price_prediction_page():
    with open("models/price_model.pkl", "rb") as f:
        model = pickle.load(f)

    df = pd.read_csv("data/price_data.csv")
    crop = st.selectbox("Select Crop", df["Crop"].unique())
    city = st.selectbox("Select City", df["City"].unique())

    filtered = df[(df["Crop"] == crop) & (df["City"] == city)]
    if filtered.empty:
        st.error("No data available.")
    else:
        last_row = filtered.iloc[-1]
        month = pd.to_datetime(last_row["Date"]).month
        year = pd.to_datetime(last_row["Date"]).year

        future_months = [(month + i - 1) % 12 + 1 for i in range(6)]
        predictions = model.predict(np.array(future_months).reshape(-1, 1))

        # Map future months to string labels (e.g., "Jan", "Feb")
        month_labels = [pd.Timestamp(f"{year}-{m:02d}-01").strftime("%b") for m in future_months]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Modal Price"], name="Historical"))
        fig.add_trace(go.Scatter(x=month_labels, y=predictions, name="Predicted"))
        st.plotly_chart(fig)

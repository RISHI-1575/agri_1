from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def train_price_model(data):
    """
    Train a linear regression model to predict crop prices based on historical data.
    """
    model = LinearRegression()
    data["Month"] = pd.to_datetime(data["Date"]).dt.month
    model.fit(data[["Month"]], data["Modal Price"])
    return model

def predict_price(model, months_ahead, start_month, start_year):
    """
    Predict crop prices for the next 'months_ahead' months.
    
    Args:
        model: Trained LinearRegression model.
        months_ahead: Number of months to predict.
        start_month: Current month (integer).
        start_year: Current year (integer).
    
    Returns:
        A list of tuples (month_year_string, predicted_price).
    """
    try:
        # Generate future months
        months = []
        for i in range(months_ahead):
            next_month = (start_month + i - 1) % 12 + 1
            next_year = start_year + (start_month + i - 1) // 12
            months.append(f"{next_year}-{next_month:02d}")  # Format as "YYYY-MM"

        # Predict prices
        future_months_numeric = [(start_month + i - 1) % 12 + 1 for i in range(months_ahead)]
        predicted_prices = model.predict(np.array(future_months_numeric).reshape(-1, 1))

        # Combine months and predicted prices
        predictions = list(zip(months, predicted_prices))
        return predictions
    except Exception as e:
        print(f"Error in predict_price: {e}")
        return []

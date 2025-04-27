import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# Load the price data
data = pd.read_csv("data/price_data.csv")

# Prepare the data for training
data["Month"] = pd.to_datetime(data["Date"]).dt.month
X = data[["Month"]]  # Input features (Month)
y = data["Modal Price"]  # Target variable (Price)

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the trained model to a file
with open("models/price_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Price prediction model saved to models/price_model.pkl")
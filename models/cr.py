import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Load the recommendation data
data = pd.read_csv("data/recommendation_data.csv")

# Prepare the data for training
# Convert categorical variables to numeric
soil_mapping = {"Loamy": 0, "Sandy": 1, "Clay": 2}
region_mapping = {"North Karnataka": 0, "South Karnataka": 1}
crop_mapping = {"Tomato": 0, "Onion": 1, "Chili": 2}

data["soil_type"] = data["soil_type"].map(soil_mapping)
data["region"] = data["region"].map(region_mapping)
data["crop_type"] = data["crop_type"].map(crop_mapping)

X = data[["soil_type", "region", "land_size"]]  # Input features
y = data["crop_type"]  # Target variable (Crop type)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the trained model to a file
with open("models/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Crop recommendation model saved to models/crop_model.pkl")

import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Load the recommendation data
data = pd.read_csv("data/recommendation_data.csv")

# Define full mappings based on all your current data
soil_mapping = {
    "Loamy": 0,
    "Sandy": 1,
    "Clay": 2,
    "Silty": 3,
    "Peaty": 4
}

region_mapping = {
    "North Karnataka": 0,
    "South Karnataka": 1,
    "Coastal Karnataka": 2,
    "Central Karnataka": 3
}

crop_mapping = {
    "Tomato": 0,
    "Onion": 1,
    "Chili": 2,
    "Cotton": 3,
    "Sugarcane": 4,
    "Corn": 5
}

# Only keep necessary columns for training
data = data[["soil_type", "region", "land_size", "crop_type"]]

# Map categorical variables to numeric
data["soil_type"] = data["soil_type"].map(soil_mapping)
data["region"] = data["region"].map(region_mapping)
data["crop_type"] = data["crop_type"].map(crop_mapping)

# Drop rows with any unmapped (NaN) values
data = data.dropna()

# Separate features and target
X = data[["soil_type", "region", "land_size"]]
y = data["crop_type"]

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the trained model to a file
with open("models/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Crop recommendation model saved to models/crop_model.pkl")

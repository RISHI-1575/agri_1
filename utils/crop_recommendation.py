import pandas as pd
import pickle
import numpy as np

def recommend_crops(place, soil, land_area):
    """
    Crop Recommendation System using a trained model and historical data.
    Inputs:
        place (str): Region or place name
        soil (str): Soil type
        land_area (float): Land area in acres
    Output:
        List of recommended crops with expected return, suitability score, and market demand level.
    """
    # Define mappings (same as in training)
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
        0: "Tomato",
        1: "Onion",
        2: "Chili",
        3: "Cotton",
        4: "Sugarcane",
        5: "Corn"
    }

    # Validate inputs
    if place not in region_mapping:
        raise ValueError(f"Invalid region. Choose from {list(region_mapping.keys())}")
    if soil not in soil_mapping:
        raise ValueError(f"Invalid soil type. Choose from {list(soil_mapping.keys())}")
    if not isinstance(land_area, (int, float)) or land_area <= 0:
        raise ValueError("Land area must be a positive number")

    # Load the trained model
    try:
        with open("models/crop_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Model file 'models/crop_model.pkl' not found. Please train the model first.")

    # Map inputs to numeric values
    soil_numeric = soil_mapping[soil]
    region_numeric = region_mapping[place]

    # Prepare input for model
    input_data = np.array([[soil_numeric, region_numeric, land_area]])

    # Predict crop
    predicted_crop_numeric = model.predict(input_data)[0]
    predicted_crop = crop_mapping.get(predicted_crop_numeric, "Unknown")

    # Load historical data
    try:
        data = pd.read_csv('data/recommendation_data.csv')
    except FileNotFoundError:
        raise FileNotFoundError("Data file 'data/recommendation_data.csv' not found.")

    # Filter by place, soil type, and predicted crop
    filtered_data = data[
        (data['region'] == place) &
        (data['soil_type'] == soil) &
        (data['crop_type'] == predicted_crop)
    ]

    # If no matching data, return empty list with warning
    if filtered_data.empty:
        return []

    # Dynamically calculate expected return based on land size
    filtered_data['dynamic_expected_return'] = filtered_data['expected_return_per_acre'] * land_area

    # Sort crops by dynamic expected return and demand score
    recommended_crops = filtered_data.sort_values(by=['dynamic_expected_return', 'demand_score'], ascending=False)

    # Prepare output
    output = recommended_crops[['crop_type', 'dynamic_expected_return', 'demand_score']].to_dict(orient='records')
    return output

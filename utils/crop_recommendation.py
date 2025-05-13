import pandas as pd
import pickle
import numpy as np

def recommend_crops(place, soil, land_area):
    """
    Crop Recommendation System for North and South Karnataka, optimized for wasteland.
    Inputs:
        place (str): Region (North Karnataka or South Karnataka)
        soil (str): Soil type
        land_area (float): Land area in acres
    Output:
        List of 2-3 recommended crops with expected return and market demand level.
    """
    # Define mappings
    soil_mapping = {
        "Loamy": 0,
        "Sandy": 1,
        "Clay": 2,
        "Silty": 3,
        "Peaty": 4
    }

    region_mapping = {
        "North Karnataka": 0,
        "South Karnataka": 1
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
        raise ValueError("Invalid region. Choose from ['North Karnataka', 'South Karnataka']")
    if soil not in soil_mapping:
        raise ValueError(f"Invalid soil type. Choose from {list(soil_mapping.keys())}")
    if not isinstance(land_area, (int, float)) or land_area <= 0:
        raise ValueError("Land area must be a positive number")

    # Load the trained model
    try:
        with open("models/crop_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Model file 'models/crop_model.pkl' not found.")

    # Map inputs to numeric
    soil_numeric = soil_mapping[soil]
    region_numeric = region_mapping[place]

    # Predict crop probabilities
    input_data = np.array([[soil_numeric, region_numeric, land_area]])
    probas = model.predict_proba(input_data)[0]
    top_crop_indices = np.argsort(probas)[-3:][::-1]  # Get top 3 crops
    top_crops = [crop_mapping.get(idx, "Unknown") for idx in top_crop_indices]

    # Load and filter historical data
    try:
        data = pd.read_csv('data/recommendation_data.csv')
        data = data[data['region'].isin(["North Karnataka", "South Karnataka"])]
    except FileNotFoundError:
        raise FileNotFoundError("Data file 'data/recommendation_data.csv' not found.")

    # Filter by region and top crops
    filtered_data = data[
        (data['region'] == place) &
        (data['crop_type'].isin(top_crops))
    ]

    # If fewer than 2 crops, include all crops for the region as fallback
    if len(filtered_data['crop_type'].unique()) < 2:
        filtered_data = data[data['region'] == place]
        top_crops = filtered_data['crop_type'].unique()[:3].tolist()

    # Aggregate by crop type (mean return and demand score)
    aggregated_data = filtered_data.groupby('crop_type').agg({
        'expected_return_per_acre': 'mean',
        'demand_score': 'mean'
    }).reset_index()

    # Filter to top crops if not fallback
    if len(filtered_data['crop_type'].unique()) >= 2:
        aggregated_data = aggregated_data[aggregated_data['crop_type'].isin(top_crops)]

    # Calculate expected return
    aggregated_data['dynamic_expected_return'] = aggregated_data['expected_return_per_acre'] * land_area

    # Sort by return and demand, limit to 2-3 crops
    recommended_crops = aggregated_data.sort_values(by=['dynamic_expected_return', 'demand_score'], ascending=False)
    output = recommended_crops[['crop_type', 'dynamic_expected_return', 'demand_score']].head(3).to_dict(orient='records')

    # Ensure at least 2 crops if available
    return output if output else []

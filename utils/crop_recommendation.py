import pandas as pd

def recommend_crops(place, soil, land_area):
    """
    Crop Recommendation System.
    Inputs:
        place (str): Region or place name
        soil (str): Soil type
        land_area (float): Land area in acres
    Output:
        List of recommended crops with expected return, suitability score, and market demand level.
    """

    # Load historical data
    data = pd.read_csv('data/recommendation_data.csv')

    # Filter by place and soil type
    filtered_data = data[
        (data['region'] == place) &
        (data['soil_type'] == soil)
    ]

    # Dynamically calculate expected return based on land size
    filtered_data['dynamic_expected_return'] = filtered_data['expected_return_per_acre'] * land_area

    # Sort crops by dynamic expected return and demand score
    recommended_crops = filtered_data.sort_values(by=['dynamic_expected_return', 'demand_score'], ascending=False)

    # Prepare output
    output = recommended_crops[['crop_type', 'dynamic_expected_return', 'demand_score']].to_dict(orient='records')
    return output

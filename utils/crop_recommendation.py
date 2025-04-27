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

    # Sort crops by expected return and demand score
    recommended_crops = filtered_data.sort_values(by=['expected_return_per_acre', 'demand_score'], ascending=False)

    # Prepare output
    output = recommended_crops[['crop_type', 'expected_return_per_acre', 'demand_score']].to_dict(orient='records')
    return output

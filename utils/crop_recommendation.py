import pandas as pd

def recommend_crops(region, soil, land_area, irrigation, season):
    """
    Advanced Crop Recommendation System.
    Inputs:
        region (str): Region name
        soil (str): Soil type
        land_area (float): Land area in acres
        irrigation (str): Type of irrigation
        season (str): Harvest season
    Output:
        List of recommended crops with expected return, suitability score, and market demand level.
    """

    # Load historical data
    data = pd.read_csv('data/recommendation_data.csv')

    # Filter by region, soil type, irrigation, and season
    filtered_data = data[
        (data['region'] == region) &
        (data['soil_type'] == soil) &
        (data['irrigation'] == irrigation) &
        (data['season'] == season)
    ]

    # Sort crops by expected return and demand score
    recommended_crops = filtered_data.sort_values(by=['expected_return_per_acre', 'demand_score'], ascending=False)

    # Prepare output
    output = recommended_crops[['crop_type', 'expected_return_per_acre', 'demand_score']].to_dict(orient='records')
    return output

import pandas as pd
import numpy as np
import geopandas as gpd
import jsonify
import mysql.connector
from sqlalchemy import create_engine

def rental_process(rental_geo):
    # Change CRS for coordinate system
    rental_for_export = rental_geo.to_crs(4326)

    # Get coordinates for each point
    rental_for_export['lat'] = rental_for_export.get_coordinates().y
    rental_for_export['lon'] = rental_for_export.get_coordinates().x

    # Drop "," from id column
    rental_for_export = rental_for_export.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)

    rental_for_export = rental_for_export.applymap(lambda x: x.replace('-', '') if isinstance(x, str) else x)

    # Export to GEOJSON
    rental_for_export.to_file('geo_data/rental_geo.geojson', driver='GeoJSON')

    # Prepare for SQL Upload
    rental_for_export_column = rental_for_export[['RegistrationNum', 'PropertyName', 'OriginalAddress1', 'OriginalCity', 'OriginalState', 'OriginalZip', 'lat', 'lon' ]]
    rental_for_export_column.columns = ['id', 'property_name', 'address', 'city', 'state', 'zip', 'lat', 'lon' ]

    return rental_for_export_column

def restaurant(df):
    df['website'] = df['website'].str.split('.com/').str[0] + '.com'

    cols = ['id', 'addr:city', 'addr:housenumber', 'addr:postcode', 'addr:state', 'addr:street', 'amenity', 'bar', 'brewery', 'cuisine', 'delivery', 'microbrewery', 'name', 'opening_hours', 'outdoor_seating', 'phone', 'takeaway', 'website', 'geometry']
    restaurant_geo = df[cols]

    #Fill NA
    restaurant_geo_filter = restaurant_geo.fillna(0).to_crs(4326)

    # Get the coordinates from the 'geometry' column
    restaurant_geo_filter['lat'] = restaurant_geo_filter.get_coordinates().y
    restaurant_geo_filter['lon'] = restaurant_geo_filter.get_coordinates().x

    #Export to GEOJSON
    restaurant_geo_filter.to_file('geo_data/restaurant_geo.geojson', driver='GeoJSON')

    # Prepare for SQL Upload
    restaurant_geo_filter = restaurant_geo_filter.drop(columns=['amenity','geometry', 'bar', 'brewery', 'microbrewery', 'takeaway','outdoor_seating','delivery' , 'opening_hours'])

    restaurant_geo_filter.columns = ['ID', 'ADDRESS_CITY', 'ADDRESS_HOUSENUMBER', 'ADDRESS_POSTCODE', 'ADDRESS_STATE', 'ADDRESS_STREET', 'CUISINE', 'NAME', 'PHONE', 'WEBSITE', 'LAT', 'LON']

    restaurant_geo_filter.columns = restaurant_geo_filter.columns.str.lower()

    return restaurant_geo_filter

def connect_rental_restaurant(rental_geo, restaurant_geo):
    # Create an empty GeoDataFrame to store the results
    rental_results = pd.DataFrame(columns=['id', 'restaurant_ids'])

    # Iterate through the rental properties
    for i, rental_row in rental_geo.iterrows():
        # Get the ID and geometry of the rental property
        rental_id = rental_row['RegistrationNum']
        rental_geom = rental_row.geometry
        
        # Create a buffer of 500 meters around the rental property
        rental_buffer = rental_geom.buffer(400)
        
        # Create an empty list to store the IDs of the restaurants
        restaurant_ids = []
        
        # Iterate through the restaurants
        for j, restaurant_row in restaurant_geo.iterrows():
            # Get the ID and geometry of the restaurant
            restaurant_id = restaurant_row['id']
            restaurant_geom = restaurant_row.geometry
            
            # Check if the rental property's buffer includes the restaurant
            if rental_buffer.contains(restaurant_geom):
                # Add the ID of the restaurant to the list
                restaurant_ids.append(restaurant_id)
        
        # Create a new row for the rental property with the restaurant IDs
        new_row = pd.Series({'id': rental_id, 'restaurant_ids': restaurant_ids})
        
        # Add the new row to the GeoDataFrame
        rental_results.loc[len(rental_results)] = new_row

    rental_results_explode = rental_results.explode('restaurant_ids')
    rental_results_explode.columns = ['rental_id', 'restaurant_id']
    rental_results_explode = rental_results_explode.dropna()

    return rental_results_explode


def process_data():
    # Connect to MySQL server
    amenity_fp = 'geo_data/restaurant.geojson'

    rental_geo_fp = 'geo_data/seattle_apartment_data.geojson'

    crs = 3043

    rental_geo = gpd.read_file(rental_geo_fp).to_crs(crs)

    restaurant_geo = gpd.read_file(amenity_fp).to_crs(crs)

    rental_data = rental_process(rental_geo)

    restaurant_data = restaurant(restaurant_geo)

    restaurant_connector = connect_rental_restaurant(rental_geo, restaurant_geo)

    engine = create_engine('postgresql+psycopg2://myuser:mypassword@localhost:5433/rentalrestaurant?sslmode=disable')

    rental_data.to_sql('rental', engine, if_exists='append' , index=False)

    restaurant_data.to_sql('restaurant', engine, if_exists='append', index=False)

    restaurant_connector.to_sql('connector', engine, if_exists='append', index=False)


if __name__ == '__main__':
    process_data()
import mysql.connector
import pandas as pd
import requests


cols = ['ID', 'ADDRESS', 'PRICE', 'BEDS', 'BATHS', 'SQFT', 'NAME', 'LAT', 'LON']

rental = pd.read_csv('Data_Manip/Data/Rental.2023-02-02.csv').fillna(0)

rental_filter = rental[['property_id', 'address', 'price_raw', 'beds', 'baths', 'sqft', 'name', 'lat', 'lon']]

rental_filter.columns = cols

rental_restaurant = pd.read_csv('Data_Manip/Data/Rental_Restaurant.2023-02-02.csv').fillna(0)

#establishing the connection
conn = mysql.connector.connect(
   user='root', password='#1234abcd', host='localhost', database='rentalrestaurant')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Convert DataFrame rows to list of tuples
values = [tuple(row) for index, row in rental_filter.iterrows()]

# Define SQL query to insert data
insert_query = "INSERT INTO rental (ID, ADDRESS, PRICE, BEDS, BATHS, SQFT, NAME, LAT, LON) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Insert data into MySQL database
cursor.executemany(insert_query, values)



for index, row in rental.iterrows():
   #location = str(row['lat']) + "," + str(row['lon'])
   #radius = 400
   #type = 'restaurant'
   
   #url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={google_key}"
   
   # make the request
   #response = requests.get(url)

   # extract the results
   #json_results = response.json()
      
   #df_results = pd.json_normalize(data=json_results['results'])\
   #df_results['property_id'] = row['property_id']

   df_results = rental_restaurant[rental_restaurant['property_id'] == row['property_id']]

   df_results_2 = df_results[['place_id', 'vicinity', 'rating', 'name', 'geometry.location.lat', 'geometry.location.lng']]

   df_results_2.columns = ['ID', 'ADDRESS', 'RATING', 'NAME', 'LAT', 'LON']

   insert_query = "INSERT INTO restaurant (ID, ADDRESS, RATING, NAME, LAT, LON) VALUES (%s, %s, %s, %s, %s, %s)"
   

   # Convert DataFrame rows to list of tuples
   values = [tuple(row) for index, row in df_results_2.iterrows()]

   # Insert data into MySQL database
   cursor.executemany(insert_query, values)
   
   df_results = df_results[['property_id', 'place_id']]

   df_results.columns = ['RENTAL_ID', 'RESTAURANT_ID']

   insert_query = "INSERT INTO connector (RENTAL_ID, RESTAURANT_ID) VALUES (%s, %s)"
   values = [tuple(row) for index, row in df_results.iterrows()]
   cursor.executemany(insert_query, values)

conn.commit()
cursor.close()
conn.close()


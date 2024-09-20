import pandas as pd
import numpy as np
import requests
import json
import time
import math
import os
#import boto3
from datetime import datetime, timezone

# s3_client = boto3.client("s3",
#     aws_access_key_id = os.getenv('ACCESS_KEY'),
#     aws_secret_access_key = os.getenv('SECRET'))
    

LOCAL_DIR = '/tmp/'

S3_BUCKET = "testbucketdevynduvall"  # please replace with your bucket name
CHUNK_SIZE = 10  # determined based on API, memory constraints, experimentation


rapid_key = '9721c01c02mshe3bb7787cca809bp1c8acejsn038764c4e983'


def get_file_name(export_type):
    dt_now = datetime.now(tz=timezone.utc)
    KEY = (
        export_type
        + "."
        + dt_now.strftime("%Y-%m-%d")

        + ".csv"
    )
    return KEY
    
# Running the API call for the Reality in US API (https://rapidapi.com/apidojo/api/realty-in-us/) 
# Returns a JSON file of the call
def get_rent_data(offset):
    url = "https://realty-in-us.p.rapidapi.com/properties/list-for-rent"
    
    querystring = {"state_code":"WA",
                   "city":"Seattle",
                   "limit":CHUNK_SIZE,
                   "offset": offset,
                   "sort":"relevance",
                   "price_min":"1600",
                   "price_max":"2500"}
    
    headers = {
        "X-RapidAPI-Key": rapid_key,
        "X-RapidAPI-Host": "realty-in-us.p.rapidapi.com"
    }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        json = response.json()
        return json
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)

# Runs the API call multiple times based on the number of calls the number of total rows
# Returns a DataFrame with all the Rental Data
def get_all_rent_data():
    for_rent_rqst = get_rent_data(1)
    df_for_rent = pd.json_normalize(data=for_rent_rqst['listings'])
    # total_offset = math.ceil(get_rent_data(1)['matching_rows'] / 200)
    # df_all = pd.json_normalize(data=for_rent_rqst['listings'])
    # for i in range(1, total_offset):
    #    for_rent_rqst = get_rent_data(i)
    #    df_for_rent = pd.json_normalize(data=for_rent_rqst['listings'])
    #    df_all = pd.concat([df_all, df_for_rent], ignore_index=True)

    return df_for_rent
    

# Writes the Rental Data to data.csv
def write_rent_data(key, df):
    os.chdir(LOCAL_DIR)
    df.to_csv(str(LOCAL_DIR + key))
    print('Put complete')
    
    

# def upload_to_aws(key):
#     try:
#         s3_client.upload_file(str(LOCAL_DIR + key), S3_BUCKET, str("Rental/" + key))
#         print("Upload Successful")
#         return None
#     except FileNotFoundError:
#         print("The file was not found")
#         return None
        

# Start the Process
def start(event, context):
    key = get_file_name("Rental")
    df_rent = get_all_rent_data()
    write_rent_data(key, df_rent)
    #upload_to_aws(key)
    df_rent.to_csv(str(LOCAL_DIR + key))
    #df_restaurant_rent = write_restaurant_rent_data(df_rent)
    #return {"df_rent" : df_rent.to_json(), "df_rent_restaurant" : df_restaurant_rent.to_json()}
    return {"status":200}

if __name__ == '__main__':
    start(None, None)
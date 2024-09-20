import psycopg2
import os

def drop_create_db():
    # Connect to MySQL server
    mydb = psycopg2.connect(
        host= 'localhost',
        user='postgres',
        password='5#Wheeler5',
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Drop the database if it exists
    mycursor.execute("DROP DATABASE IF EXISTS rentalrestaurant")

    # Create a new database
    mycursor.execute("CREATE DATABASE rentalrestaurant")

    # Close the cursor and connection
    mycursor.close()
    mydb.close()

import mysql.connector 

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "#1234abcd",
)

# Create a Cursor
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE rentalrestaurant")

# Create a Database
mycursor.execute("CREATE DATABASE rentalrestaurant")

# Close the Connection
mydb.close()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:/root:#1234abcd@localhost/rentalrestaurant'

db = SQLAlchemy(app)  # Initialize the database

from models import Rental, Restaurant, Connector

with app.app_context():
    db.create_all()

from views import *




if __name__ == '__main__':
    app.run(debug=True)
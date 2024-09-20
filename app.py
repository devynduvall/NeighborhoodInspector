from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from Data_Manip.update_db import insert_data

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5433/mydatabase'

db = SQLAlchemy(app)  # Initialize the database

with app.app_context():
    db.create_all()

from views import *


if __name__ == '__main__':
    app.run(debug=True)
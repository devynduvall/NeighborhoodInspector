from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///rentalrestaurant.db'  # Example URI, use your actual database URI

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from views import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)





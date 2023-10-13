from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)  # Initialize the database

<<<<<<< HEAD

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///rentalrestaurant.db'  # Example URI, use your actual database URI

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from views import *

with app.app_context():
    db.create_all()
=======
# Import routes here to avoid circular imports
from routes import *
>>>>>>> 433d7ba1da0320e97a5b7c618ce2859611a720f3

if __name__ == '__main__':
    app.run(debug=True)
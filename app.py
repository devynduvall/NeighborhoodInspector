from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)  # Initialize the database


from views import *

with app.app_context():
    db.create_all()

# Import routes here to avoid circular imports
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

app = Flask(__name__)




app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'


db = SQLAlchemy()
migrate = Migrate(app, db)
from models import Rental, Restaurant, Connector

# Initialize the app
db.init_app(app)

# Get marker_id and send data to index.html
@app.route('/', methods = ["GET", "POST"])
@app.route('/index')
def index():
    rent = Rental.query.all()
    rest = Restaurant.query.all()
    marker_id = 0
    data = []
    if request.method == "POST":
       marker_id = request.form["marker_id"]
       print(marker_id)

       print("quieried database for marker matches")
    
    print(data)
    return render_template('index.html', markers = rent, marker_match = marker_id, marker_match_data = data)


# Determine the marker values
@app.route('/marker/<int:marker_id>/points')
def get_marker_points(marker_id):
    # Use SQLAlchemy to query the database for additional points based on marker_id
    subquery = (
        db.session.query(Connector.restaurant_id).filter(Connector.rental_id == marker_id)
    )
    print(subquery)
    data = (
        db.session.query(Restaurant).filter(Restaurant.id.in_(subquery)).all()
    )
    # Serialize the points into a format that can be consumed by Leaflet
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [point.lon, point.lat]
                },
                "properties": {
                    "id": point.id,
                }
            }
            for point in data
        ]
    }

    # Return the serialized data to the client-side JavaScript code
    return jsonify(feature_collection)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)





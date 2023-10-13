from app import app, db
from flask import render_template, request, jsonify

from models import Rental, Restaurant, Connector


# Get marker_id and send data to index.html
@app.route('/', methods=["GET", "POST"])
@app.route('/index')
def index():
    rent = Rental.query.all()
    rest = Restaurant.query.all()
    marker_id = 0
    data = []
    if request.method == "POST":
        marker_id = request.form["marker_id"]
        print(marker_id)
        print("queried database for marker matches")
    
    print(data)
    return render_template('index.html', markers=rent, marker_match=marker_id, marker_match_data=data)

# Determine the marker values
@app.route('/marker/<int:marker_id>/points')
def get_marker_points(marker_id):
    subquery = (
        db.session.query(Connector.restaurant_id).filter(Connector.rental_id == marker_id)
    )
    print(subquery)
    data = (
        db.session.query(Restaurant).filter(Restaurant.id.in_(subquery)).all()
    )
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
    return jsonify(feature_collection)
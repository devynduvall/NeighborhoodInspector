from flask import Flask, render_template, request, jsonify

from app import app, db, Rental, Restaurant, Connector

import json



#a simple initial greeting
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
       data = Restaurant.query.filter_by(id = Connector.query.filter_by(rental_id = marker_id))
    return render_template('index.html', markers = rent, marker_match = marker_id, marker_match_data = data)


@app.route('/marker/<int:marker_id>/points')
def get_marker_points(marker_id):
    # Use SQLAlchemy to query the database for additional points based on marker_id
    subquery = (
        db.session.query(Connector.restaurant_id).filter(Connector.rental_id == marker_id)
    )
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

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    data = Rental.query.filter(Rental.address.like(search_term)).all()
    print(data)
    # Process the search term here (e.g., query a database)
    return f"Search term: {data}"

@app.route('/about')
def about():
    return render_template('about.html')
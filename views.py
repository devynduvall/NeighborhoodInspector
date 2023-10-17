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
       print("quieried database for marker matches")

    print(data)
    # print(rent)
    print("--------------------")
    #print(rent[0].id)
    return render_template('index.html', markers = rent, marker_match = marker_id, marker_match_data = data)


@app.route('/marker/<int:marker_id>/points')
def get_marker_points(marker_id):
    # Use SQLAlchemy to query the database for additional points based on marker_id
    subquery = (
        db.session.query(Connector.id).filter(Connector.rental_id == marker_id)
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
    print(feature_collection)
    # Return the serialized data to the client-side JavaScript code
    return jsonify(feature_collection)


#@views.route('/marker-selected/<int:marker_id>')
#def marker_selected(marker_id):
  # Query the database for data related to the selected marker
#  data = Restaurant.query.filter_by(id = Connector.query.filter_by(rental_id = marker_id))

  # Convert the data to a dictionary that can be returned as JSON


  # Return the JSON data
#  return render_template('index.html', rest_marker = data)

# Import Flask, render_template, request, and jsonify modules
from flask import Flask, render_template, request, jsonify


# Import the app, db, Rental, Restaurant, and Connector modules from the app package
from app import app, db, Rental, Restaurant, Connector
# Import the json module
import json



# Define a route for the index page
@app.route('/', methods = ["GET", "POST"])
@app.route('/index')
def index():
    # Query all rentals and restaurants from the database
    rent = Rental.query.all()

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
                    "address": point.address,
                    "name": point.name
                    
                }
            }
            for point in rent
        ]
    }

    # Initialize marker_id and data variables
    marker_id = 0
    data = [] 
    
    # Check if the request method is POST
    if request.method == "POST":
        # Get the marker_id from the form data
        marker_id = request.form["marker_id"]
        print(marker_id)
        
        # Query the restaurants that match the rental_id
        data = Restaurant.query.filter_by(id = Connector.query.filter_by(rental_id = marker_id))
    
    # Print the rentals to the console
    print(rent)
    
    # Render the index.html template with the rentals, marker_id, and data variables
    return render_template('index.html', markers = feature_collection, marker_match = marker_id, marker_match_data = data)

# Define a route for the marker points
@app.route('/marker/<int:marker_id>/points', methods=['GET', 'POST'])
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
                    "address": point.address,
                    "rating": point.rating,
                    "name": point.name
                    
                }
            }
            for point in data
        ]
    }
    
    # Return the serialized data to the client-side JavaScript code
    return jsonify(feature_collection)

# # Define a route for the search functionality
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'GET':
#         # Get the search term from the query string parameters
#         search_term = request.args.get('search_term')
#     elif request.method == 'POST':
#         # Get the search term from the form data
#         search_term = request.form['search_term']

#     # Query the database for the coordinates of the searched term
#     data = db.session.query(Rental).filter(Rental.address.ilike(f"%{search_term}%")).all()

#     feature_collection = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": {
#                     "type": "Point",
#                     "coordinates": [point.lat, point.lon]
#                 },
#                 "properties": {
#                     "id": point.id,
#                     "address": point.address,
#                     "name": point.name
#                 }
#             }
#             for point in data
#         ]
#     }

#     # Return the coordinates to the front-end
#     return jsonify(feature_collection)

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     search_term = request.form['search_term']

#     # Query the database for the rentals that match the search term
#     data = db.session.query(Rental).filter(Rental.address.ilike(f"%{search_term}%")).all()

#     # Create a GeoJSON feature collection for the matching rentals
#     feature_collection = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": {
#                     "type": "Point",
#                     "coordinates": [point.lon, point.lat]
#                 },
#                 "properties": {
#                     "id": point.id,
#                     "address": point.address,
#                     "name": point.name
#                 }
#             }
#             for point in data
#         ]
#     }

#     # Return the GeoJSON feature collection to the front-end
#     return jsonify(feature_collection)

# Define a route to serve the markers as a feature collection
@app.route('/markers')
def markers():
    # Query all rentals from the database
    rent = Rental.query.all()
    # Create a feature collection of the rentals
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
                    "address": point.address,
                    "name": point.name
                }
            }
            for point in rent
        ]
    }
    rent_json = jsonify(feature_collection)

    # Return the feature collection as JSON
    return rent_json

# Define a route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/Users')
def Users():
    return render_template('Users.html')
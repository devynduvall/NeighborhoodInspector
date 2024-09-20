from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
# Import Flask, render_template, request, and jsonify modules
from flask import Flask, render_template, request, jsonify
# Import the app, db, Rental, Restaurant, and Connector modules from the app package
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from webforms import LoginForm, UserForm, FilteringForm


from Data_Manip.update_db import insert_data


from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey that you aren't able to understand"

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5433/mydatabase'

db = SQLAlchemy(app)  # Initialize the database

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            # Check the hash
            print(check_password_hash(user.password_hash, form.password_hash.data))
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                print("Login Succesfull!!")
                return redirect(url_for('dashboard'))
            else:
                print("Wrong Password - Try Again!")
        else:
            print("That User Doesn't Exist! Try Again...")

    # Add an else block to the if statement
    else:
        print("Form Validation Failed! Try Again...")

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		
	else:
		return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)
# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update, id=id)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id=id)
	else:
		return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
	# Check logged in id vs. id to delete
	if id == current_user.id:
		user_to_delete = Users.query.get_or_404(id)
		name = None
		form = UserForm()

		try:
			db.session.delete(user_to_delete)
			db.session.commit()
			flash("User Deleted Successfully!!")

			our_users = Users.query.order_by(Users.date_added)
			return render_template("add_user.html", 
			form=form,
			name=name,
			our_users=our_users)

		except:
			flash("Whoops! There was a problem deleting user, try again...")
			return render_template("add_user.html", 
			form=form, name=name,our_users=our_users)
	else:
		flash("Sorry, you can't delete that user! ")
		return redirect(url_for('dashboard'))

# Define a route for the index page
@app.route('/', methods = ["GET", "POST"])
@app.route('/index')
@app.route('/marker/<string:marker_id>/points', methods=['GET', 'POST'])
def index(marker_id=None):
    form = FilteringForm()

    # If the form is submitted, store the cuisine in the session
    if form.validate_on_submit(extra_validators=None):
        session['cuisine'] = form.restaurant_cuisine.data
        return redirect(url_for('index', marker_id=marker_id))

    cuisine = session.get('cuisine', None)

    # If the cuisine is in the session, use it

    print(cuisine)
    if marker_id:
        # Use SQLAlchemy to query the database for additional points based on marker_id
        subquery = (
            db.session.query(Connector.restaurant_id).filter(Connector.rental_id == marker_id)
        )

        if cuisine == ['all']:
            cuisine = None

        print("inside of get_marker_points")

        if cuisine:
            data = (
                db.session.query(Restaurant)
                .filter(Restaurant.id.in_(subquery))
                .filter(Restaurant.cuisine.in_(cuisine))# Filter by cuisine
                .all()
            )
        else:
            data = (
                db.session.query(Restaurant)
                .filter(Restaurant.id.in_(subquery))  # Return all restaurants
                .all()
            )

        print(len(data))
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
                        "address": point.address_street,
                        "name": point.name,
                        "cuisine": point.cuisine,
                        "website": point.website,
                        "phone": point.phone
                    }
                }
                for point in data
            ]
        }
    
        # Return the serialized data to the client-side JavaScript code
        return jsonify(feature_collection)
    else:
        # Your existing index function code goes here
        pass


    

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

    # Render the index.html template with the rentals, marker_id, and data variables
    return render_template('index.html', filtering_form = form, markers = feature_collection)

# # Define a route for the marker points
# @app.route('/marker/<string:marker_id>/points', methods=['GET', 'POST'])
# def get_marker_points(marker_id):
#     # print("request inside /marker/<int:marker_id>/points" + marker_id)
#     # Use SQLAlchemy to query the database for additional points based on marker_id
#     subquery = (
#         db.session.query(Connector.restaurant_id).filter(Connector.rental_id == marker_id)
#     )

#     print("inside of get_marker_points")

#     data = (
#         db.session.query(Restaurant).filter(Restaurant.id.in_(subquery)).all()
#     )
#     print(len(data))
#     # Serialize the points into a format that can be consumed by Leaflet
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
#                     "address": point.address_street,
#                     "name": point.name
                    
#                 }
#             }
#             for point in data
#         ]
#     }
    
#     # Return the serialized data to the client-side JavaScript code
#     return jsonify(feature_collection)

@app.route('/search/<string:search_term>/coordinates', methods=['GET', 'POST'])
def search_coordinates(search_term):
    data = db.session.query(Rental).filter(Rental.address.ilike(f"%{search_term}%")).all()
    print(data)
    # Create a GeoJSON feature collection for the matching rentals
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
            for point in data
        ]
    }

    # Return the GeoJSON feature collection to the front-end
    return jsonify(feature_collection)

@app.route('/user/add', methods = ["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            #hash the password
            new_user = Users(name = form.name.data, username = form.username.data, email = form.email.data, password = form.password_hash.data)
            db.session.add(new_user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''

    return render_template("add_user.html", 
        name = name,
        form = form)


# Define a route for the about page
@app.route('/about')
def about():
    return render_template('about.html')





if __name__ == '__main__':
    app.run()
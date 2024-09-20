from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Rental(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    address = db.Column(db.String(120), index=True, unique=False)
    price = db.Column(db.String(50), index=False, unique=False)
    beds = db.Column(db.String(120), index=True, unique=False)
    baths = db.Column(db.String(50), index=False, unique=False)
    sqft = db.Column(db.String(25), index=False, unique=False)
    name = db.Column(db.String(120), index=True, unique=False)
    lat = db.Column(db.Float, index=False, unique=False)
    lon = db.Column(db.Float, index=False, unique=False)
    connector = db.relationship('Connector', backref='rental', lazy='dynamic', cascade='all, delete, delete-orphan')

class Restaurant(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(120), index = True, unique = False)
    address_city = db.Column(db.String(120), index = True, unique = False)
    address_housenumber = db.Column(db.String(120), index = True, unique = False)
    address_postcode = db.Column(db.String(120), index = True, unique = False)
    address_state = db.Column(db.String(120), index = True, unique = False)
    address_street = db.Column(db.String(120), index = True, unique = False)
    phone = db.Column(db.String(120), index = True, unique = False)
    website = db.Column(db.String(256), index = True, unique = False)
    cuisine = db.Column(db.String(120), index = True, unique = False)
    delivery = db.Column(db.Boolean, index = True, unique = False)
    microbrewery = db.Column(db.Boolean, index = True, unique = False)
    opening_hours = db.Column(db.String(120), index = True, unique = False)
    outdoor_seating = db.Column(db.Boolean, index = True, unique = False)
    bar = db.Column(db.Boolean, index = True, unique = False)
    brewery = db.Column(db.Boolean, index = True, unique = False)
    takeaway = db.Column(db.Boolean, index = True, unique = False)
    lat = db.Column(db.Float, index = False, unique = False)
    lon = db.Column(db.Float, index = False, unique = False)
    connector = db.relationship('Connector', backref = 'restaurant', lazy = 'dynamic', cascade = 'all, delete, delete-orphan' )

class Shop(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(120), index = True, unique = False)
    address_city = db.Column(db.String(120), index = True, unique = False)
    address_housenumber = db.Column(db.String(120), index = True, unique = False)
    address_postcode = db.Column(db.String(120), index = True, unique = False)
    address_state = db.Column(db.String(120), index = True, unique = False)
    address_street = db.Column(db.String(120), index = True, unique = False)
    opening_hours = db.Column(db.String(120), index = True, unique = False)
    website = db.Column(db.String(256), index = True, unique = False)
    phone = db.Column(db.String(120), index = True, unique = False)
    service = db.Column(db.String(120), index = True, unique = False)
    website = db.Column(db.String(250), index = True, unique = False)
    shop = db.Column(db.String(120), index = True, unique = False)
    lat = db.Column(db.Float, index = False, unique = False)
    lon = db.Column(db.Float, index = False, unique = False)
    shop_connector = db.relationship('Shop_Connector', backref = 'shop', lazy = 'dynamic', cascade = 'all, delete, delete-orphan' )

class Connector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.String(50), db.ForeignKey('restaurant.id'))
    rental_id = db.Column(db.String(50), db.ForeignKey('rental.id'))

class Shop_Connector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.String(50), db.ForeignKey('shop.id'))
    rental_id = db.Column(db.String(50), db.ForeignKey('rental.id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=False)
    name = db.Column(db.String(50), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

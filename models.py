from app import db

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
    address = db.Column(db.String(120), index = True, unique = False)
    rating = db.Column(db.String(50), index = False, unique = False)
    name = db.Column(db.String(120), index = True, unique = False)
    lat = db.Column(db.Float, index = False, unique = False)
    lon= db.Column(db.Float, index = False, unique = False)
    connector = db.relationship('Connector', backref = 'restaurant', lazy = 'dynamic', cascade = 'all, delete, delete-orphan' )

class Connector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.String(50), db.ForeignKey('restaurant.id'))
    rental_id = db.Column(db.String(50), db.ForeignKey('rental.id'))



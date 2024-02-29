
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class City(db.Model):
    cityId = db.Column(db.Integer, primary_key=True)
    cityName = db.Column(db.String(80), nullable=False)

class UserData(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    userAddress = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    cityId = db.Column(db.Integer, db.ForeignKey('city.cityId'), nullable=False)
    city = db.relationship('City', backref=db.backref('users', lazy=True))

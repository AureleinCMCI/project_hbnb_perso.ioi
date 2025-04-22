
import uuid
from datetime import datetime
from sqlalchemy.orm import validates
from .base_model import BaseModel
from app.extensions import db



place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Modèle SQLAlchemy pour un lieu (Place)"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)  # L'ID du propriétaire (UUID)
    amenities = db.relationship('Amenity', secondary=place_amenities, backref='places')
    address = db.Column(db.String(255), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        """Validation : Le titre ne doit pas être vide et doit être <= 100 caractères"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        return title[:100]

    @validates('price')
    def validate_price(self, key, price):
        """Validation : Le prix doit être un nombre positif"""
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validation : Latitude entre -90 et 90"""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validation : Longitude entre -180 et 180"""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def to_dict(self):
        """Convertir un objet Place en dictionnaire"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [amenity.to_dict() for amenity in self.amenities],
            "address": self.address
        }

    def __repr__(self):
        return f"<Place {self.title} - {self.latitude}, {self.longitude}>"

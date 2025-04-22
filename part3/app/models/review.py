
import uuid
from datetime import datetime
from .base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    """Modèle SQLAlchemy pour une évaluation (Review)"""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Clé étrangère vers User
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)  # Clé étrangère vers Place

    def __init__(self, text: str, user_id: str, place_id: str, rating: int):
        self.text = text.strip() if text and text.strip() else "No review provided"
        self.rating = max(1, min(5, rating))  # ✅ Assurer une note entre 1 et 5
        self.user_id = user_id  # Stocker l'ID de l'utilisateur
        self.place_id = place_id  # Stocker l'ID du lieu

    def to_dict(self):
        """Convertir un objet Review en dictionnaire"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def __repr__(self):
        return f"<Review {self.id} - Rating: {self.rating}>"

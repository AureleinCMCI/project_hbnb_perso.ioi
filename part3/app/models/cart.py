from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.extensions import db


class Cart(db.Model):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='cart')
    places = Column(JSON, nullable=False, default=[])  # Stocker les places dans un champ JSON (listes d'ID de places)

    def __repr__(self):
        return f"<Cart {self.id}>"

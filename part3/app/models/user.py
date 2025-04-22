from app.extensions import db, bcrypt
import uuid
from .base_model import BaseModel  # Import BaseModel from its module
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = relationship('Cart', back_populates='user', uselist=False)  # Un utilisateur peut avoir un seul panier

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
   
    
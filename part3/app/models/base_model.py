from datetime import datetime
import uuid
from app.extensions import db


class BaseModel(db.Model):
    """Classe de base pour les modèles SQLAlchemy"""
    __abstract__ = True  # Indique que cette classe ne doit pas être instanciée directement

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Ajoute l'instance à la session et commit les modifications"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'instance de la base de données"""
        db.session.delete(self)
        db.session.commit()

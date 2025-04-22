
import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True  # ✅ Empêche SQLAlchemy de créer une table pour cette classe

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Enregistre l'objet dans la base de données"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'objet de la base de données"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Convertit l'objet SQLAlchemy en dictionnaire"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

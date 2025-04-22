from abc import ABC, abstractmethod
from app.extensions import db  # Assuming you have set up SQLAlchemy in your Flask app


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}
        self.data = {}
        
    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)  # Récupérer l'objet
        if obj:
            if not isinstance(data, dict):
                data = data.__dict__  # Convertir l'objet en dictionnaire
            
            for key, value in data.items():  # Itérer sur le dictionnaire data
                if hasattr(obj, key):  # Vérifier si l'attribut existe
                    setattr(obj, key, value)  # Mettre à jour l'attribut

            self.save(obj)  # Sauvegarder l'objet mis à jour dans la base de données
        return obj



    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
        
    def save(self, obj):
        self._storage[obj.id] = obj  # Remplace l'objet existant avec la version mise à jour

    def get_by_place_id(self, place_id):
        """Récupère un propriétaire via l'ID du lieu"""
        for owner in self.data.values():
            if owner.get("place_id") == place_id:
                return owner
        return None  
    
    def get_reviews_by_place_id(self, place_id):
        """Récupère tous les avis pour un lieu spécifique"""
        return [review for review in self._storage.values() if str(review.place_id) == str(place_id)]


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        places = self.model.query.all()
        print(f"🔍 DEBUG: get_all() fetched: {places}")  # 🔹 Vérifie si des données sont récupérées
        return places

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.add(obj) 
            db.session.commit()
        return obj 
    
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    def get_by_attributeAll(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).all()
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.cart import Cart
from datetime import datetime
from app.extensions import db , bcrypt# ✅ Ajout de db pour initialisation
from sqlalchemy.orm.attributes import flag_modified

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    ###########################################################################
    # 🧑‍💻 CRUD UTILISATEURS
    ###########################################################################

    def hash_password(self, password):
        """Génère un hash bcrypt pour stocker en base"""
        return bcrypt.generate_password_hash(password).decode('utf-8')
    def verify_password(self, user, password):
        """Vérifie si le mot de passe correspond au hash stocké"""
        if not user or not user.password:  # Vérifie si l'utilisateur existe et a un mot de passe
            return False
        return bcrypt.check_password_hash(user.password, password)

    def create_user(self, user_data):
        user = User(**user_data)
        if "password" in user_data:
            user_data["password"] = self.hash_password(user_data["password"])
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repository.get(user_id)
        
        print(f"🔍 DEBUG: user_id: {user_id}, type: {type(user_id)} ")  # Vérifier le type
        print(f"🔍 DEBUG: user: {user}, type: {type(user)}")  # Vérifier si c'est bien un objet User

        if not user:
            return {'error': 'User not found'}, 404  # Retourne une erreur si l'utilisateur n'existe pas

        if "password" in user_data:
            user_data["password"] = self.hash_password(user_data["password"])  # Hash du mot de passe

        updated_user = self.user_repository.update(user.id, user_data)  # ✅ On passe user.id au lieu de user !
        print(f"🔍 DEBUG: updated_user: {updated_user}, type: {type(updated_user)}")  # Vérification

        if not updated_user:
            return {'error': 'Failed to update user'}, 500

        return updated_user
    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute("email", email) 

    ###########################################################################
    # 🏠 CRUD LIEUX
    ###########################################################################
    @staticmethod
    def create_place(data):
        amenities_ids = data.get('amenities', [])
        new_place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner_id=data['owner_id'],
            address=data['address']
        )

        # Attacher explicitement les amenities ici ✅
        for amenity_id in amenities_ids:
            amenity = Amenity.query.get(amenity_id)
            if amenity:
                new_place.amenities.append(amenity)

        db.session.add(new_place)
        db.session.commit()
        return new_place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        places = self.place_repository.get_all()
        print(f"🔍 DEBUG: get_all_places() fetched: {places}, type: {type(places)}")  # 🔹 Vérifie si une liste est retournée
        return places

    def update_place(self, place_id, data):
        place = self.place_repository.get(place_id)  
        if 'amenities' in data:
            amenities_ids = data['amenities']  # La liste des IDs des amenities
            if isinstance(amenities_ids, list) and all(isinstance(a, str) for a in amenities_ids):
                data['amenities'] = [self.amenity_repository.get(a_id) for a_id in amenities_ids]

        # Récupérer l'objet depuis la base
        if not place:
            print(f"❌ ERROR: Place with id {place_id} not found")
            return None

        # ✅ S'assurer que `data` est bien un dictionnaire
        if isinstance(data, Place):
            print(f"🔍 FIX: Converting Place object to dict")

        if not isinstance(data, dict):
            print(f"❌ ERROR: Expected dict but got {type(data)}")
            return None  # Éviter de continuer avec un mauvais type

        print(f"🔍 DEBUG: Before update - {place.to_dict()}")

        for key, value in data.items():
            setattr(place, key, value)  # Modifier l'objet
            flag_modified(place, key)  # Informer SQLAlchemy du changement

        db.session.add(place)
        db.session.commit()

        print(f"✅ DEBUG: Commit successful - {place.to_dict()}")
        return place





    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    ###########################################################################
    # ⭐ CRUD REVIEWS
    ###########################################################################

    def create_review(self, review_data):
        """
        Crée un nouvel avis (review) et l'enregistre dans la base de données.
        """
        print(f"✅ DEBUG: Received review data: {review_data}")

        if not isinstance(review_data, dict):
            print(f"❌ ERROR: Expected dict but got {type(review_data)}")
            return None

        # Vérification des champs requis
        required_fields = ["text", "rating", "place_id", "user_id"]
        for field in required_fields:
            if field not in review_data:
                print(f"❌ ERROR: Missing required field '{field}' in review_data")
                return None

        print(f"✅ DEBUG: Creating review with data: {review_data}")

        try:
            new_review = Review(**review_data)  # Création de l'objet Review
            self.review_repository.add(new_review)  # Ajout en base
            db.session.commit()  # Sauvegarde des changements
            print(f"✅ SUCCESS: Review created: {new_review.to_dict()}")  
            return new_review
        except Exception as e:
            print(f"❌ ERROR: Failed to create review: {e}")
            return None

    def get_all_reviews(self):
        return self.review_repository.get_all()
    
    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Récupère toutes les reviews associées à un lieu spécifique.
        Assure que le résultat est toujours une liste.
        """
        # Récupérer les reviews via le repository
        reviews = self.review_repository.get_by_attributeAll('place_id', place_id)
        
        # Gérer tous les cas possibles
        if reviews is None:
            # Aucun résultat trouvé
            return []
        elif isinstance(reviews, list):
            # Déjà une liste, parfait
            return reviews
        else:
            # Un seul objet Review, convertir en liste
            print(f"DEBUG: Converting single review to list for place_id: {place_id}")
        return [reviews]

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        
        if not review:
            print(f"❌ ERROR: Review with id {review_id} not found")
            return None

        # ✅ Assurer que review_data est bien un dictionnaire
        if isinstance(review_data, Review):  
            print(f"🔍 FIX: Converting Review object to dict")
            review_data = review_data.to_dict()

        if not isinstance(review_data, dict):
            print(f"❌ ERROR: Expected dict but got {type(review_data)}")
            return None

        print(f"🔍 DEBUG: Before update - {review.to_dict()}")  # ✅ Debug avant modification

        for key, value in review_data.items():
            setattr(review, key, value)  # Modifier l'objet
            flag_modified(review, key)  # Informer SQLAlchemy du changement

        db.session.add(review)
        db.session.commit()

        print(f"✅ SUCCESS: Review updated - {review.to_dict()}")  # ✅ Debug après modification
        return review

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    ###########################################################################
    # 🏨 CRUD AMENITIES
    ###########################################################################

    def create_amenity(self, data):
        existing_amenity = Amenity.query.filter_by(name=data["name"]).first()
        if existing_amenity:
            raise ValueError("Amenity already exists")

        new_amenity = Amenity(name=data["name"], description=data.get("description", ""))
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repository.update(amenity)
        return amenity

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)
############################ CARD ##############################################
    def get_cart_by_user_id(self, user_id):
        return Cart.query.filter_by(user_id=user_id).first()

    def create_cart(self, user_id, places):
        cart = Cart(user_id=user_id, places=places)
        db.session.add(cart)
        db.session.commit()
        return cart

    def update_cart(self, cart):
        db.session.commit()
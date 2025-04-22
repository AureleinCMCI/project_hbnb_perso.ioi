from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1.auth import api as auth_ns
from app.extensions import db 
jwt = JWTManager()
from config import DevelopmentConfig
from flask_cors import CORS

bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    """Factory function pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5501", 
                                    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["Content-Type", "Authorization"]}})
    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Création de l'API
    api = Api(app, version="1.0", title="API Flask", description="Une API REST avec Flask-RESTx")

    # Import des namespaces APRES l'initialisation pour éviter les imports circulaires
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.cart import api as cart_ns  # Ajoutez l'importation du namespace cart

    # Ajout des routes
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(cart_ns, path='/api/v1/cart')  # Ajout du namespace cart

    return app


if __name__ == "__main__":
    app = create_app()
    app.config.from_object('config.DevelopmentConfig')
    app.run(debug=True)

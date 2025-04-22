from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
import json
from app import api  # Assurez-vous d'avoir l'instance `api` dans votre projet

# Définir le Namespace pour le panier
api = Namespace('cart', description='Cart operations')
facade = HBnBFacade()

# Modèle de réponse pour le panier
cart_model = api.model('Cart', {
    'id': fields.Integer(readonly=True, description='The cart identifier'),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'items': fields.List(fields.String, required=True, description='List of cart items')
})

# Assurez-vous que le modèle est bien enregistré dans l'API
api.models['Cart'] = cart_model  # Ceci enregistre le modèle dans l'API

# Définir les opérations de ressource pour le panier
@api.route('/')
class CartResource(Resource):
    @jwt_required()
    @api.response(200, 'Cart retrieved successfully', cart_model)
    @api.response(404, 'Cart not found')
    def get(self):
        """Retrieve the cart for the logged-in user"""
        user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur à partir du JWT

        # Récupérer le panier de l'utilisateur
        cart = facade.get_cart_by_user_id(user_id)
        if not cart:
            return {'message': 'No cart found for this user'}, 404

        return {'places': cart.places}, 200

    @jwt_required()
    @api.expect(cart_model)
    @api.response(200, 'Cart updated successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Add places to the cart for the logged-in user"""
        user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur à partir du JWT

        # Récupérer les lieux envoyés dans la requête
        cart_data = api.payload
        places = cart_data.get('places', [])

        if not places:
            return {'error': 'The cart must contain at least one place'}, 400

        # Récupérer ou créer un panier pour l'utilisateur
        cart = facade.get_cart_by_user_id(user_id)
        if not cart:
            # Si le panier n'existe pas, on crée un nouveau panier
            cart = facade.create_cart(user_id, places)
        else:
            # Sinon, on met à jour les lieux dans le panier existant
            cart.places.extend(places)
            facade.update_cart(cart)

        return {'message': 'Cart updated successfully', 'places': cart.places}, 200

    @jwt_required()
    @api.response(200, 'Cart cleared successfully')
    def delete(self):
        """Clear the cart for the logged-in user"""
        user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur à partir du JWT

        # Récupérer et vider le panier de l'utilisateur
        cart = facade.get_cart_by_user_id(user_id)
        if not cart:
            return {'message': 'No cart found for this user'}, 404

        cart.places = []  # Vider le panier
        facade.update_cart(cart)

        return {'message': 'Cart cleared successfully'}, 200

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')  # 🔹 Ajout du mot de passe
})

# User response model (sans le password pour la sécurité)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})


# 🔹 Liste et création des utilisateurs
@api.route('/')
class UserList(Resource):
    @api.response(200, 'User list retrieved successfully', [user_response_model])
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404
        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]

        return user_list, 200

    # 🔹 Création d'un utilisateur
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Vérifier si l'email existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])

        
        if existing_user:
            return {'error': 'Email already registered'}, 400
        user_data['password'] = facade.hash_password(user_data['password'])


        # 🔹 Création de l'utilisateur avec hachage du mot de passe
        new_user = facade.create_user(user_data)

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


# 🔹 Gestion des utilisateurs individuels
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details, including password if provided"""
        user_data = api.payload  

        # 🔹 Vérifier si le mot de passe est présent et doit être mis à jour
        if 'password' in user_data and user_data['password']:
            user_data['password'] = facade.hash_password(user_data['password'])  # Hash du password

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200


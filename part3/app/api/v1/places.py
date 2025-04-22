from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'address': fields.String(required=True, description="l'address !")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        place_data = api.payload

        # Validation des données
        if not place_data.get('title'):
            return {'error': 'Title is required'}, 400
        
        if not place_data.get('price') or place_data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400
        
        if not (-90 <= place_data['latitude'] <= 90):
            return {'error': 'Latitude must be between -90 and 90'}, 400
        
        if not (-180 <= place_data['longitude'] <= 180):
            return {'error': 'Longitude must be between -180 and 180'}, 400
        
        new_place = facade.create_place(place_data)

        return new_place.to_dict(), 201
    
    def get(self):
        """Retrieve the list of places"""
        places = facade.get_all_places()
        print(f"🔍 DEBUG: places fetched = {places}, type = {type(places)}")  # 🔹 Debug

        if not places or len(places) == 0:
            return {'message': 'No places found'}, 404  # ✅ Ajoute un message clair

        return [place.to_dict() for place in places], 200 

       

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        # Log the place ID being retrieved
        print(f"Retrieving place with ID: {place_id}")

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        
        return {
            'message': 'Place updated successfully',
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'address':place.address
        }, 200  # ✅ Utilise la méthode to_dict()


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Internal Server Error')
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload

        # Log the incoming data
        print(f"Received data for update: {place_data}")

        # Log the place ID being updated
        print(f"Updating place with ID: {place_id}")

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Validation des données
        validations = [
            ('title', lambda p: p and len(p) > 0, 'Title is required and cannot be empty.'),
            ('price', lambda p: p and p > 0, 'Price must be a positive number.'),
            ('latitude', lambda p: p is not None and -90 <= p <= 90, 'Latitude must be between -90 and 90.'),
            ('longitude', lambda p: p is not None and -180 <= p <= 180, 'Longitude must be between -180 and 180.')
        ]

        for field, validate_fn, error_message in validations:
            if field not in place_data or not validate_fn(place_data.get(field)):
                return {'error': f'Invalid input data. "{field}" {error_message}'}, 400

        try:
            place.title = place_data.get('title', place.title)
            place.description = place_data.get('description', place.description)
            place.price = place_data.get('price', place.price)
            place.latitude = place_data.get('latitude', place.latitude)
            place.longitude = place_data.get('longitude', place.longitude)
            facade.update_place(place_id, place_data)

            return {
                'message': 'Place updated successfully',
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
            }, 200
        except Exception as e:
            print(f"Error updating place: {e}")
            return {'message': 'Internal Server Error'}, 500
@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'No reviews found for this place')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        print(f"Retrieving reviews for place ID: {place_id}")  # Debug

        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'message': 'No reviews found for this place'}, 404

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        review_data = api.payload

        # Validation des données
        if not review_data.get('text'):
            return {'error': 'Text is required'}, 400

        new_review = facade.create_review(review_data)
        return {
            'id': new_review.id,
            'text': new_review.text,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201


    def get(self):
            """Retrieve all reviews"""
            reviews = facade.get_all_reviews()  # ✅ Utilisation correcte de `facade`
            if not reviews:
                return {'message': 'No reviews found'}, 404

            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                } for review in reviews
            ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):  # ✅ Assure-toi que cette méthode existe bien !
        """Update a review"""
        review_data = api.payload

        updated_review = facade.update_review(review_id, review_data)

        if not updated_review:
            return {'error': 'Review not found'}, 404

        return updated_review.to_dict(), 200 



    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200
    
@api.route('/places/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'No reviews found for this place')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        print(f"🔍 DEBUG: Retrieving reviews for place ID: {place_id}")  # Debug

        reviews = facade.get_reviews_by_place(place_id)  # ✅ Récupérer les avis sous forme de liste

        if not reviews:
            return {'message': 'No reviews found for this place'}, 404

        # ✅ Convertir chaque review en dictionnaire
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat(),  # Format ISO pour la lisibilité JSON
                'updated_at': review.updated_at.isoformat()
            } for review in reviews  # 🔥 Boucle bien sur chaque review !
        ], 200

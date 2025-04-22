document.addEventListener('DOMContentLoaded', function () {
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    
    // Récupérer l'ID du lieu depuis l'URL
    const placeId = new URLSearchParams(window.location.search).get('placeId');
    
    if (!placeId) {
        placeDetailsContainer.innerHTML = '<p>Le lieu n\'a pas été trouvé.</p>';
        return;
    }

    // Fonction pour récupérer les détails du lieu depuis l'API
    function fetchPlaceDetails() {
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
            .then(response => response.json())
            .then(place => {
                displayPlaceDetails(place);
                fetchReviews(placeId);  // Récupérer les avis pour ce lieu
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des détails du lieu:', error);
                placeDetailsContainer.innerHTML = '<p>Erreur lors du chargement des détails du lieu.</p>';
            });
    }

    // Fonction pour afficher les détails du lieu dans le DOM
    function displayPlaceDetails(place) {
        const title = document.createElement('h1');
        title.textContent = place.title;

        const description = document.createElement('p');
        description.textContent = `Description: ${place.description || 'Aucune description'}`;

        const price = document.createElement('p');
        price.textContent = `Prix par nuit: $${place.price}`;

        const amenities = document.createElement('p');
        
        // Vérifier si 'amenities' existe et est un tableau
        if (Array.isArray(place.amenities) && place.amenities.length > 0) {
            amenities.textContent = `Commodités: ${place.amenities.join(', ')}`;
        } else {
            amenities.textContent = 'Commodités: Non spécifiées';
        }

        // Ajouter tous les éléments au conteneur des détails du lieu
        placeDetailsContainer.appendChild(title);
        placeDetailsContainer.appendChild(description);
        placeDetailsContainer.appendChild(price);
        placeDetailsContainer.appendChild(amenities);
    }

    // Fonction pour récupérer et afficher les avis du lieu
    function fetchReviews(placeId) {
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
            .then(response => response.json())
            .then(reviews => {
                displayReviews(reviews);
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des avis:', error);
                reviewsContainer.innerHTML = '<p>Aucun avis pour ce lieu.</p>';
            });
    }

    // Fonction pour afficher les avis dans le DOM
    function displayReviews(reviews) {
        reviewsContainer.innerHTML = ''; // Réinitialiser la section des avis
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>Aucun avis pour ce lieu.</p>';
            return;
        }

        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';

            const reviewText = document.createElement('p');
            reviewText.textContent = review.text;

            const rating = document.createElement('p');
            rating.textContent = `Note: ${review.rating}`;

            reviewCard.appendChild(reviewText);
            reviewCard.appendChild(rating);
            reviewsContainer.appendChild(reviewCard);
        });
    }

    // Appeler la fonction pour récupérer les détails du lieu au chargement de la page
    fetchPlaceDetails();
});
document.addEventListener('DOMContentLoaded', function () {
    const reviewSection = document.getElementById('review-section');
    const feedback = document.getElementById('review-feedback');

    // Récupérer placeId depuis l'URL
    const placeId = new URLSearchParams(window.location.search).get('placeId');
    if (!placeId) {
        feedback.textContent = "❌ Aucune place spécifiée dans l'URL.";
        return;
    }

    // Vérifie si l'utilisateur est connecté
    const userId = localStorage.getItem('user_id');
    if (!userId) {
        feedback.textContent = "❌ Vous devez être connecté pour ajouter un avis.";
        return;
    }

    // Créer dynamiquement le formulaire uniquement si connecté
    const form = document.createElement('form');
    form.id = 'review-form';
    form.innerHTML = `
        <h2>Ajouter un Avis</h2>

        <label for="review-text">Votre avis :</label><br>
        <textarea id="review-text" required></textarea><br>

        <label for="rating">Note :</label><br>
        <select id="rating" required>
            <option value="">--Choisir une note--</option>
            <option value="1">1 ⭐</option>
            <option value="2">2 ⭐⭐</option>
            <option value="3">3 ⭐⭐⭐</option>
            <option value="4">4 ⭐⭐⭐⭐</option>
            <option value="5">5 ⭐⭐⭐⭐⭐</option>
        </select><br>

        <button type="submit">Envoyer l'avis</button>
    `;

    reviewSection.appendChild(form);

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const text = document.getElementById('review-text').value;
        const rating = parseInt(document.getElementById('rating').value);

        if (!text || !rating) {
            feedback.textContent = '❌ Veuillez remplir tous les champs.';
            return;
        }

        const reviewData = {
            text: text,
            rating: rating,
            user_id: userId, // injecté automatiquement
            place_id: placeId
        };

        fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de l\'envoi de l\'avis.');
            }
            return response.json();
        })
        .then(data => {
            feedback.textContent = '✅ Avis ajouté avec succès !';
            form.reset();
        })
        .catch(error => {
            console.error(error);
            feedback.textContent = '❌ Une erreur est survenue lors de l\'envoi.';
        });
    });
});

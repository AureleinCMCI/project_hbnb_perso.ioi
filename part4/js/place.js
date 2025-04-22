document.addEventListener('DOMContentLoaded', function () {
    const placesList = document.getElementById('places-list');
    let cart = [];

    function getUserIdFromSession() {
        return localStorage.getItem('user_id');
    }

    function loadCartFromStorage() {
        const userId = getUserIdFromSession();
        if (!userId) return;

        const storedCart = localStorage.getItem(`cart_${userId}`);
        if (storedCart) {
            cart = JSON.parse(storedCart);
        }
    }

    function getDynamicImage(index) {
        const imageUrls = [
            'base_fil/images/maison.jpg',
            'base_fil/images/vila.avif',
            'base_fil/images/maison.jpg',
            'base_fil/images/place4.jpg',
            'base_fil/images/place5.jpg'
        ];
        return imageUrls[index % imageUrls.length];
    }

    function addToCart(place) {
        // Fonction à compléter selon tes besoins
        alert(`Voir les détails du lieu : ${place.title}`);
    }

    function fetchPlaces() {
        fetch('http://127.0.0.1:5000/api/v1/places/')
            .then(response => response.json())
            .then(places => {
                placesList.innerHTML = ''; // Vider la liste

                places.forEach((place, index) => {
                    const col = document.createElement('div');
                    col.className = 'col-sm';

                    const card = document.createElement('div');
                    card.className = `card custom-card card-${place.id}`;

                    // Image de couverture
                    const cardCover = document.createElement('div');
                    cardCover.className = 'card-cover';
                    cardCover.style.backgroundImage = `url('${getDynamicImage(index)}')`;
                    card.appendChild(cardCover);

                    // Titre
                    const title = document.createElement('h5');
                    title.className = 'card-title';
                    title.textContent = place.title;
                    card.appendChild(title);

                    // Prix
                    const price = document.createElement('p');
                    price.className = 'card-text';
                    price.textContent = `Prix par nuit : $${place.price}`;
                    card.appendChild(price);

                    // Description
                    const desc = document.createElement('p');
                    desc.className = 'card-text';
                    desc.textContent = `Description : ${place.description}`;
                    card.appendChild(desc);

                    // Bouton voir les détails (lien)
                    const button = document.createElement('a');
                    button.className = 'choose-button btn btn-primary';
                    button.textContent = 'Voir les détails';
                    button.href = `place.html?placeId=${place.id}`;
                    card.appendChild(button);

                    col.appendChild(card);
                    placesList.appendChild(col);
                });
            })
            .catch(err => {
                console.error('Erreur lors du chargement des lieux :', err);
                placesList.innerHTML = '<p>Erreur lors du chargement.</p>';
            });
    }

    loadCartFromStorage();
    fetchPlaces();
});

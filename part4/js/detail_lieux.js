document.addEventListener('DOMContentLoaded', function () {
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('placeId');

    console.log("ID de la place récupéré:", placeId);

    // Vérification que l'ID existe
    if (!placeId) {
        console.error("Aucun ID de place trouvé dans l'URL");
        document.getElementById('place-details').innerHTML = '<p>Aucun lieu spécifié</p>';
    } else {
        // Requête fetch corrigée
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
            .then(response => {
                console.log("Statut de la réponse:", response.status);
                if (!response.ok) {
                    throw new Error(`Erreur HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Données reçues:", data);
                if (data) {
                    displayPlaceDetails(data);
                    fetchReviews(placeId);
                } else {
                    throw new Error("La réponse est vide");
                }
            })
            .catch(error => {
                console.error("Erreur lors de la récupération:", error);
                document.getElementById('place-details').innerHTML = 
                    `<p>Erreur lors du chargement des détails: ${error.message}</p>`;
            });
    }


    function displayPlaceDetails(place) {
        // Images grid
        const placeImagesMap = {
            '363748f0-48f3-469f-a996-d6ead1414a99': [
                'base_fil/images/vila.avif',
                'base_fil/images/vila1.avif',
                'base_fil/images/vila2.avif',
                'base_fil/images/vila3.avif',
                'base_fil/images/vila4.avif'
            ],
            '94c45241-9ecc-4e70-a5ab-7f7c57a15225': [
                'base_fil/images/maisonbelle.avif',
                'base_fil/images/MaisonBelle2.avif',
                'base_fil/images/MaisonBelle3.avif',
                'base_fil/images/MaisonBelle4.avif',
                'base_fil/images/MaisonBelle5.avif',
            ],
        };
        const imageUrls = placeImagesMap[place.id] || [];
        const imagesGridContainer = document.createElement('div');
        imagesGridContainer.className = 'images-grid';

        if (imageUrls.length > 0) {
            const mainImage = document.createElement('img');
            mainImage.src = imageUrls[0];
            mainImage.alt = 'Image principale';
            mainImage.className = 'main-image';
            imagesGridContainer.appendChild(mainImage);

            const sideImagesContainer = document.createElement('div');
            sideImagesContainer.className = 'side-images';
            for (let i = 1; i < 5 && i < imageUrls.length; i++) {
                const sideImg = document.createElement('img');
                sideImg.src = imageUrls[i];
                sideImg.alt = `Image ${i + 1}`;
                sideImg.className = 'side-image';
                sideImagesContainer.appendChild(sideImg);
            }
            imagesGridContainer.appendChild(sideImagesContainer);
        } else {
            const noImagesMsg = document.createElement('p');
            noImagesMsg.textContent = 'Aucune image disponible pour ce lieu.';
            imagesGridContainer.appendChild(noImagesMsg);
        }
        placeDetailsContainer.appendChild(imagesGridContainer);

        // Modal pour images
        let modal = document.getElementById('image-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'image-modal';
            modal.innerHTML = `
                <span class="close-modal">&times;</span>
                <img class="modal-content" id="modal-img">
                <button class="modal-prev">&#10094;</button>
                <button class="modal-next">&#10095;</button>
            `;
            document.body.appendChild(modal);
            modal.querySelector('.close-modal').onclick = function () {
                modal.style.display = "none";
            };
        }
        const allImages = imagesGridContainer.querySelectorAll('img');
        let currentImgIndex = 0;
        allImages.forEach((img, idx) => {
            img.style.cursor = 'pointer';
            img.onclick = function () { showModal(idx); };
        });
        function showModal(index) {
            currentImgIndex = index;
            modal.style.display = "flex";
            modal.querySelector('#modal-img').src = imageUrls[currentImgIndex];
        }
        modal.querySelector('.modal-prev').onclick = function () {
            currentImgIndex = (currentImgIndex === 0) ? imageUrls.length - 1 : currentImgIndex - 1;
            showModal(currentImgIndex);
        };
        modal.querySelector('.modal-next').onclick = function () {
            currentImgIndex = (currentImgIndex === imageUrls.length - 1) ? 0 : currentImgIndex + 1;
            showModal(currentImgIndex);
        };

        // --- FLEX ROW SOUS LES IMAGES ---
        const detailsRow = document.createElement('div');
        detailsRow.className = 'details-row';


        const infoCol = document.createElement('div');
        infoCol.className = 'info-col';
        const title = document.createElement('h1');
        title.textContent = place.title;
        infoCol.appendChild(title);

        
        const reservationCol = document.createElement('div');
        reservationCol.className = 'reservation-col';
        reservationCol.id = 'reservation-box';
        
        const address = document.createElement('div');
        address.className = 'place-address';
        address.innerHTML = `<h2>l'address se trouve </h2><p>${place.address}</p>`;
        infoCol.appendChild(address);

        
        const description = document.createElement('div');
        description.className = 'place-description';
        description.innerHTML = `<h2>À propos de ce logement</h2><p>${place.description}</p>`;
        infoCol.appendChild(description);

        const price = document.createElement('div');
        price.className = 'place-price';
        price.innerHTML = `<p>Prix par nuit: $${place.price}</p>`;
        infoCol.appendChild(price);

        if (Array.isArray(place.amenities) && place.amenities.length > 0)
        {
            const amenitiesDiv = document.createElement('div');
            amenitiesDiv.className = 'place_amenities';
            amenitiesDiv.innerHTML = `<h3>Équipements</h3>`;
            const ul = document.createElement('ul');
            place.amenities.forEach(a => {
                const li = document.createElement('li');
                li.textContent = typeof a === 'object' && a !== null ? a.name : a;
                ul.appendChild(li);
            });
            amenitiesDiv.appendChild(ul);
            infoCol.appendChild(amenitiesDiv);
        }
        else
        {
            // Si pas d'équipements, tu peux afficher un message ou rien
            const noAmenities = document.createElement('div');
            noAmenities.className = 'place-amenities';
            noAmenities.innerHTML = `<h3>Équipements</h3><p>Aucun équipement renseigné.</p>`;
            infoCol.appendChild(noAmenities);
        }


        detailsRow.appendChild(infoCol);


        placeDetailsContainer.appendChild(detailsRow);
        let mapDiv = document.getElementById('map');
        if (!mapDiv) {
            mapDiv = document.createElement('div');
            mapDiv.id = 'map';
            mapDiv.style.width = '100%';
            mapDiv.style.height = '400px';
            mapDiv.style.margin = '30px 0';
            placeDetailsContainer.appendChild(mapDiv);
        }
        // Affiche la carte si coordonnées valides
        if (
            typeof place.latitude === "number" && typeof place.longitude === "number" &&
            place.latitude >= -90 && place.latitude <= 90 &&
            place.longitude >= -180 && place.longitude <= 180
        ) {
            // Coordonnées valides, affiche la carte
            displayMap(place.latitude, place.longitude, place.title);
        } else if (place.address) {
            // Sinon, géocode l'address pour obtenir les coordonnées
            geocodeAddress(place.address, function(lat, lng) {
                displayMap(lat, lng, place.title);
            });
        }

        // Appel pour remplir la réservation
        displayReservationBox(place);
    }

    function displayMap(latitude, longitude, title) {
        const mapElement = document.getElementById("map");
        if (!mapElement) {
            console.error("Element with id 'map' not found.");
            return;
        }
        // Pour éviter d'empiler plusieurs cartes
        mapElement.innerHTML = "";
        // Initialise la carte centrée sur la position
        const map = new google.maps.Map(mapElement, {
            zoom: 14,
            center: { lat: latitude, lng: longitude }
        });
        // Ajoute un marqueur
        new google.maps.Marker({
            position: { lat: latitude, lng: longitude },
            map: map,
            title: title
        });
    }
    
    function displayReservationBox(place) {
        const box = document.getElementById('reservation-box');
        if (!box) return;
        box.innerHTML = `
            <div class="reservation-card">
                <div class="price-row">
                    <span class="price">${place.price} €</span> <span class="per-night">par nuit</span>
                </div>
                <form id="booking-form">
                    <div class="date-row">
                        <div>
                            <label>Arrivée</label>
                            <input type="date" id="date-arrivee" required>
                        </div>
                        <div>
                            <label>Départ</label>
                            <input type="date" id="date-depart" required>
                        </div>
                    </div>
                    <div>
                        <label>Voyageurs</label>
                        <select id="voyageurs">
                            <option>1 voyageur</option>
                            <option>2 voyageurs</option>
                            <option>3 voyageurs</option>
                            <option>4 voyageurs</option>
                            <option>5 voyageurs</option>
                            <option>6 voyageurs</option>
                            <option>7 voyageurs</option>
                        </select>
                    </div>
                    <button type="button" id="btn-reserver">Réserver</button>
                </form>
                <div id="booking-details" style="display:none;">
                    <div class="row"><span>${place.price} € x <span id="nb-nuits">0</span> nuits</span> <span id="prix-nuits">0 €</span></div>
                    <div class="row"><span>Frais de ménage</span> <span id="frais-menage">100 €</span></div>
                    <div class="row"><span>Frais de service Airbnb</span> <span id="frais-service">311 €</span></div>
                    <div class="row"><span>Taxes</span> <span id="taxes">10 €</span></div>
                    <div class="row total"><span>Total</span> <span id="total">0 €</span></div>
                </div>
            </div>
        `;
        document.getElementById('btn-reserver').onclick = function () {
            const arrivee = document.getElementById('date-arrivee').value;
            const depart = document.getElementById('date-depart').value;
            const voyageurs = document.getElementById('voyageurs').value;
            const prixNuit = place.price;
            const nbNuits = (new Date(depart) - new Date(arrivee)) / (1000 * 60 * 60 * 24);

            if (nbNuits > 0) {
                const total = (prixNuit * nbNuits) + 100 + 311 + 10;
                const userId = localStorage.getItem('user_id') || 'guest';
                const cartKey = `cart_${userId}`;
                const cartItem = {
                    id: place.id,
                    title: place.title,
                    description: `${arrivee} au ${depart} - ${voyageurs}`,
                    price: total,
                    nights: nbNuits,
                    dateStart: arrivee,
                    dateEnd: depart
                };
                let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
                cart.push(cartItem);
                localStorage.setItem(cartKey, JSON.stringify(cart));

                // --- ENVOI DU SMS ---
                // Récupère le numéro de téléphone (à adapter à ta logique utilisateur)
                let phoneNumber = localStorage.getItem('user_phone');
                if (!phoneNumber) {
                    phoneNumber = prompt("Entrez votre numéro de téléphone pour recevoir un SMS d'avis :");
                }
                if (phoneNumber) {
                    fetch('http://127.0.0.1:5000/api/v1/send_review_sms', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            to_number: phoneNumber,
                            place_id: place.id
                        })
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === 'ok') {
                                alert('Un SMS pour laisser un avis vous a été envoyé !');
                            } else {
                                alert('Erreur lors de l\'envoi du SMS : ' + (data.error || ''));
                            }
                        })
                        .catch(err => {
                            alert('Erreur lors de l\'envoi du SMS.');
                            console.error(err);
                        });
                }

                window.location.href = `add_review.html?placeId=${place.id}`;
            } else {
                alert("Veuillez sélectionner des dates valides.");
            }
        };
    }

    function fetchReviews(placeId) {
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
            .then(response => response.json())
            .then(reviews => {
                displayReviews(reviews);
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des avis:', error);
                reviewsContainer.innerHTML = '<p>Erreur lors du chargement des avis.</p>';
            });
    }

    function displayReviews(reviews) {
        reviewsContainer.innerHTML = '';
        const reviewsTitle = document.createElement('h2');
        reviewsTitle.textContent = 'Avis';
        reviewsTitle.className = 'reviews-title';
        reviewsContainer.appendChild(reviewsTitle);

        if (reviews.length === 0) {
            reviewsContainer.innerHTML += '<p>Aucun avis pour ce lieu.</p>';
            return;
        }
        const reviewsGrid = document.createElement('div');
        reviewsGrid.className = 'reviews-grid';
        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';

            const reviewText = document.createElement('p');
            reviewText.textContent = review.text;

            const rating = document.createElement('p');
            rating.textContent = `Note: ${review.rating}`;

            reviewCard.appendChild(reviewText);
            reviewCard.appendChild(rating);
            reviewsGrid.appendChild(reviewCard);
        });
        reviewsContainer.appendChild(reviewsGrid);
    }

    fetchPlaceDetails();
    function geocodeAddress(address, callback) {
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 'address': address }, function(results, status) {
            if (status === 'OK' && results[0]) {
                const location = results[0].geometry.location;
                callback(location.lat(), location.lng());
            } else {
                alert("Impossible de géocoder l'address : " + status);
            }
        });
    }
});



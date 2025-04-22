console.log("bonjour")
document.addEventListener("DOMContentLoaded", () => {
  // On récupère le user_id depuis le localStorage (ou autre méthode sécurisée)

const userId = localStorage.getItem('user_id');

  // Sécurité : vérifier s'il existe
  if (!userId) {
      document.getElementById("user-info").innerHTML = "<p>Utilisateur non connecté.</p>";
      return;
  }

  // Appel à l'API Flask pour récupérer les infos utilisateur
  fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`)
      .then(response => {
          if (!response.ok) {
              throw new Error("Erreur lors de la récupération");
          }
          return response.json();
      })
      .then(user => {
          const infoHtml = `
              <p><strong>Prénom :</strong> ${user.first_name}</p>
              <p><strong>Nom :</strong> ${user.last_name}</p>
              <p><strong>Email :</strong> ${user.email}</p>
          `;
          document.getElementById("user-info").innerHTML = infoHtml;
      })
      .catch(error => {
          console.error("Erreur de chargement des données utilisateur :", error);
          document.getElementById("user-info").innerHTML = "<p>Erreur de chargement.</p>";
      });

  // Gestion du bouton de déconnexion
  document.getElementById("logout-btn").addEventListener("click", () => {
      localStorage.removeItem("user_id"); // ou token si tu l'utilises
      window.location.href = "login.html"; // redirection vers la page de login
  });
});

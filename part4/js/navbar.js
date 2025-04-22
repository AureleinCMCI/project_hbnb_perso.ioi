document.addEventListener('DOMContentLoaded', function () {
  // 1. Générer la sidebar dynamiquement
  document.getElementById('sidebar-root').innerHTML = `
    <nav id="sidebar">
      <a href="index.html">
        <img src="logo.png" alt="App Logo" class="logo">
      </a>
      <ul class="nav">
        <li><a href="mon_compte.html"><i class="fa fa-phone"></i>Mon compte</a></li>
        <!-- Boutons Connexion / Déconnexion -->
        <li><a href="login.html" id="login-link" style="display: none;"><i class="fa fa-sign-in-alt"></i>Connexion</a></li>
        <li><a href="#" id="logout-link" style="display: none;"><i class="fa fa-sign-out-alt"></i>Déconnexion</a></li>
      </ul>
    </nav>
  `;

  // 2. Gérer le toggle de la sidebar
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('toggleSidebar');
  let sidebarOpen = true;

  if (toggleBtn) {
    toggleBtn.onclick = function() {
      sidebarOpen = !sidebarOpen;
      if (sidebarOpen) {
        sidebar.classList.remove('closed');
        document.getElementById('viewport').style.paddingLeft = '250px';
      } else {
        sidebar.classList.add('closed');
        document.getElementById('viewport').style.paddingLeft = '0';
      }
    };
  }

  // 3. Vérification dans localStorage pour afficher le bon bouton
  const token = localStorage.getItem("token");
  const loginLink = document.getElementById("login-link");
  const logoutLink = document.getElementById("logout-link");

  if (token) {
    // Si connecté : cacher "Connexion", afficher "Déconnexion"
    if (loginLink) loginLink.style.display = "none";
    if (logoutLink) logoutLink.style.display = "block";
  } else {
    // Si pas connecté : afficher "Connexion", cacher "Déconnexion"
    if (loginLink) loginLink.style.display = "block";
    if (logoutLink) logoutLink.style.display = "none";
  }

  if (logoutLink) {
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem('token');
      window.location.reload();
    });
  }
});

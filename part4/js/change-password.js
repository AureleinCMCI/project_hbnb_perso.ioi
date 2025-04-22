console.log("✅ change-password.js bien chargé !");

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('changePasswordForm');
  const errorMessage = document.getElementById('error-message');
  const successMessage = document.getElementById('success-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const currentPassword = formData.get('current_password');
    const newPassword = formData.get('new_password');
    const confirmPassword = formData.get('confirm_password');

    if (newPassword !== confirmPassword) {
      errorMessage.textContent = "Les nouveaux mots de passe ne correspondent pas.";
      errorMessage.style.display = 'block';
      return;
    }

    try {
      const token = getCookie('token'); // <-- récupère le token s'il est stocké dans les cookies

      const response = await fetch('http://127.0.0.1:5000/api/v1/users/change-password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Erreur lors du changement de mot de passe");
      }

      successMessage.textContent = "Mot de passe mis à jour avec succès !";
      successMessage.style.display = 'block';
      errorMessage.style.display = 'none';

    } catch (error) {
      errorMessage.textContent = error.message;
      errorMessage.style.display = 'block';
      successMessage.style.display = 'none';
    }
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
});

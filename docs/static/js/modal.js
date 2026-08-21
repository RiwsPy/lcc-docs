let modal;

document.addEventListener("DOMContentLoaded", () => {
  modal = document.getElementById("downloadModal");
  const modalFullUrl = document.getElementById("modalFullUrl");
  const confirmBtn = document.getElementById("confirmDownloadBtn");

  // Gestion des liens avec téléchargement direct
  document.querySelectorAll("a.security_check").forEach(link => {
    link.addEventListener("click", (e) => {
      showConfirmModal(modalFullUrl, confirmBtn, link.getAttribute("href"));
      e.preventDefault()
    })
  })

  // Clic n'importe où : on ferme
  modal.addEventListener("click", () => closeModal());
  // Échap : on ferme
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) { closeModal(); }
  });
})

// Fonction d'ouverture de la modale
function showConfirmModal(modalFullUrl, confirmBtn, fullUrl) {
  modalFullUrl.textContent = fullUrl;
  modalFullUrl.title = fullUrl;
  confirmBtn.href = fullUrl;
  confirmBtn.title = fullUrl;
  modal.classList.add("active");
}

// Fermeture de la modale
function closeModal() {
  modal.classList.remove("active");
}
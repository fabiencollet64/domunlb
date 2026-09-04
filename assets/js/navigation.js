/* Menu de navigation en petit écran.
   Progressive enhancement : sans JavaScript, le menu reste déplié et
   entièrement utilisable — l'attribut data-ouvert n'est posé qu'ici. */
(function () {
  "use strict";

  var bouton = document.querySelector("[data-bouton-menu]");
  var nav = document.querySelector("[data-nav]");
  if (!bouton || !nav) return;

  bouton.hidden = false;
  nav.setAttribute("data-ouvert", "false");
  bouton.setAttribute("aria-expanded", "false");

  function basculer(ouvrir) {
    nav.setAttribute("data-ouvert", ouvrir ? "true" : "false");
    bouton.setAttribute("aria-expanded", ouvrir ? "true" : "false");
  }

  bouton.addEventListener("click", function () {
    basculer(bouton.getAttribute("aria-expanded") !== "true");
  });

  // Échap referme le menu et rend le focus au bouton.
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && bouton.getAttribute("aria-expanded") === "true") {
      basculer(false);
      bouton.focus();
    }
  });

  // Au-delà de 900 px la navigation est toujours visible : on nettoie l'état.
  var large = window.matchMedia("(min-width: 900px)");
  function auRedimensionnement() {
    if (large.matches) basculer(false);
  }
  large.addEventListener("change", auRedimensionnement);
})();

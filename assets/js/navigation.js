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
    mesurerEntete();
  }
  large.addEventListener("change", auRedimensionnement);
  window.addEventListener("resize", mesurerEntete);
})();

/* En-tête collant : hauteur réelle et ombre au défilement.
   La hauteur est publiée dans --hauteur-entete, dont dépend le
   scroll-padding-top : sans elle, une ancre se placerait sous l'en-tête. */
function mesurerEntete() {
  var entete = document.querySelector("[data-entete]");
  if (!entete) return;
  document.documentElement.style.setProperty(
    "--hauteur-entete", entete.offsetHeight + "px");
}

(function () {
  "use strict";
  var entete = document.querySelector("[data-entete]");
  if (!entete) return;

  mesurerEntete();

  var defile = false;
  function auDefilement() {
    var doit = window.scrollY > 8;
    if (doit !== defile) {
      defile = doit;
      entete.classList.toggle("entete--defile", doit);
      mesurerEntete();
    }
  }
  auDefilement();
  window.addEventListener("scroll", auDefilement, { passive: true });
})();

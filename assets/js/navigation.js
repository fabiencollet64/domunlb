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

  // Refermer le menu referme aussi le sous-menu qu'il contenait.
  var ancienBasculer = basculer;
  basculer = function (ouvrir) {
    ancienBasculer(ouvrir);
    if (!ouvrir) fermerSousMenus();
  };

  // Échap referme le menu et rend le focus au bouton.
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && bouton.getAttribute("aria-expanded") === "true") {
      basculer(false);
      bouton.focus();
    }
  });

  // Au-delà de 900 px la navigation est toujours visible : on nettoie l'état.
  // Au-delà de 1100 px la navigation tient sur la ligne de l'en-tête.
  var large = window.matchMedia("(min-width: 1100px)");
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

/* Sous-menu « Nos services ».

   Ouverture au clic et jamais au survol : un menu qui se déplie au passage de
   la souris est difficile à viser, et ne se referme pas au clavier. Le
   regroupement existe parce que les huit entrées à plat réclamaient 1428 px
   pour 1152 px disponibles ; sans lui, l'en-tête ne pouvait pas tenir sur une
   seule ligne sans descendre sous le corps de 18 px.

   Sans JavaScript, le bouton reste inerte : les quatre services demeurent
   accessibles depuis la page d'accueil, le pied de page et le fil d'Ariane.
*/
function fermerSousMenus(sauf) {
  var boutons = document.querySelectorAll("[data-sous-menu]");
  Array.prototype.forEach.call(boutons, function (bouton) {
    if (bouton === sauf) return;
    bouton.setAttribute("aria-expanded", "false");
    var liste = document.getElementById(bouton.getAttribute("aria-controls"));
    if (liste) liste.hidden = true;
  });
}

(function () {
  "use strict";

  var boutons = document.querySelectorAll("[data-sous-menu]");
  if (!boutons.length) return;

  Array.prototype.forEach.call(boutons, function (bouton) {
    var liste = document.getElementById(bouton.getAttribute("aria-controls"));
    if (!liste) return;

    bouton.addEventListener("click", function () {
      var ouvert = bouton.getAttribute("aria-expanded") === "true";
      fermerSousMenus(bouton);
      bouton.setAttribute("aria-expanded", ouvert ? "false" : "true");
      liste.hidden = ouvert;
    });
  });

  // Échap referme et rend le focus au bouton du sous-menu concerné.
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var ouvert = document.querySelector('[data-sous-menu][aria-expanded="true"]');
    if (!ouvert) return;
    fermerSousMenus();
    ouvert.focus();
  });

  // Un clic ou un focus hors du groupe referme le sous-menu.
  function siDehors(e) {
    var ouvert = document.querySelector('[data-sous-menu][aria-expanded="true"]');
    if (ouvert && !ouvert.closest(".nav-groupe").contains(e.target)) {
      fermerSousMenus();
    }
  }
  document.addEventListener("click", siDehors);
  document.addEventListener("focusin", siDehors);
})();

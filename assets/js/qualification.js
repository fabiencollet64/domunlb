/* Formulaire de qualification de la page d'accueil.

   Amélioration progressive : le HTML contient les trois étapes les unes à la
   suite des autres, avec un seul bouton d'envoi. Sans JavaScript, le
   formulaire reste donc entièrement remplissable. Ce script se contente de
   masquer les étapes non courantes et d'ajouter la navigation.

   Points d'accessibilité tenus ici :
   - le focus est porté sur le titre de l'étape à chaque changement ;
   - la progression est annoncée par une zone aria-live ;
   - une étape incomplète affiche un message en toutes lettres et renvoie le
     focus sur le premier champ concerné ;
   - aucune étape n'est validée par la couleur seule.
*/
(function () {
  "use strict";

  var form = document.querySelector("[data-qualification]");
  if (!form) return;

  var etapes = Array.prototype.slice.call(
    form.querySelectorAll("[data-etape]"));
  if (etapes.length < 2) return;

  var envoi = form.querySelector("[data-envoi]");
  var courante = 0;

  /* --- Progression ------------------------------------------------------ */
  var progression = document.createElement("p");
  progression.className = "qualif__progression";
  progression.setAttribute("aria-live", "polite");
  var texteProgression = document.createElement("span");
  var jauge = document.createElement("span");
  jauge.className = "qualif__jauge";
  var remplissage = document.createElement("span");
  jauge.appendChild(remplissage);
  progression.appendChild(texteProgression);
  progression.appendChild(jauge);
  form.insertBefore(progression, form.firstChild);

  /* --- Navigation ------------------------------------------------------- */
  var navigation = document.createElement("div");
  navigation.className = "qualif__navigation";

  var retour = document.createElement("button");
  retour.type = "button";
  retour.className = "bouton bouton--secondaire";
  retour.textContent = "Retour";

  var suivant = document.createElement("button");
  suivant.type = "button";
  suivant.className = "bouton bouton--principal";
  suivant.textContent = "Continuer";

  navigation.appendChild(retour);
  navigation.appendChild(suivant);
  envoi.parentNode.insertBefore(navigation, envoi);

  /* --- Affichage d'une étape -------------------------------------------- */
  function titreDe(etape) {
    return etape.querySelector("legend");
  }

  function afficher(indice, deplacerFocus) {
    courante = indice;
    etapes.forEach(function (etape, i) {
      etape.hidden = i !== indice;
    });

    var derniere = indice === etapes.length - 1;
    retour.hidden = indice === 0;
    suivant.hidden = derniere;
    envoi.hidden = !derniere;

    texteProgression.textContent =
      "Étape " + (indice + 1) + " sur " + etapes.length;
    remplissage.style.width =
      Math.round(((indice + 1) / etapes.length) * 100) + "%";

    if (deplacerFocus) {
      var titre = titreDe(etapes[indice]);
      if (titre) {
        titre.setAttribute("tabindex", "-1");
        titre.focus();
      }
    }
  }

  /* --- Validation d'une étape ------------------------------------------- */
  function retirerAlerte(etape) {
    var ancienne = etape.querySelector(".qualif__alerte");
    if (ancienne) ancienne.parentNode.removeChild(ancienne);
  }

  function signaler(etape, message, champ) {
    retirerAlerte(etape);
    var alerte = document.createElement("p");
    alerte.className = "qualif__alerte";
    alerte.setAttribute("role", "alert");
    alerte.textContent = message;
    etape.appendChild(alerte);
    if (champ) champ.focus();
  }

  function etapeValide(etape) {
    retirerAlerte(etape);

    // Groupes de boutons radio obligatoires
    var groupes = etape.querySelectorAll("[data-groupe-requis]");
    for (var i = 0; i < groupes.length; i++) {
      var nom = groupes[i].getAttribute("data-groupe-requis");
      var choix = etape.querySelectorAll('input[name="' + nom + '"]');
      var coche = etape.querySelector('input[name="' + nom + '"]:checked');
      if (!coche) {
        signaler(etape, "Choisissez une réponse pour continuer.", choix[0]);
        return false;
      }
    }

    // Champs de saisie obligatoires
    var champs = etape.querySelectorAll("input[required], textarea[required]");
    for (var j = 0; j < champs.length; j++) {
      var champ = champs[j];
      var vide = champ.type === "checkbox" ? !champ.checked : !champ.value.trim();
      if (vide) {
        var libelle = etape.querySelector('label[for="' + champ.id + '"]');
        var intitule = libelle
          ? libelle.textContent.replace(/\s*\(obligatoire\)\s*/i, "").trim()
          : "ce champ";
        signaler(etape, "Renseignez « " + intitule + " » pour continuer.", champ);
        return false;
      }
    }
    return true;
  }

  /* --- Événements ------------------------------------------------------- */
  suivant.addEventListener("click", function () {
    if (!etapeValide(etapes[courante])) return;
    if (courante < etapes.length - 1) afficher(courante + 1, true);
  });

  retour.addEventListener("click", function () {
    if (courante > 0) {
      retirerAlerte(etapes[courante]);
      afficher(courante - 1, true);
    }
  });

  // Entrée dans un champ texte : passer à l'étape suivante plutôt qu'envoyer
  form.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    if (e.target.tagName === "TEXTAREA") return;
    if (courante < etapes.length - 1) {
      e.preventDefault();
      suivant.click();
    }
  });

  // Le formulaire porte l'attribut novalidate : la validation native du
  // navigateur est donc désactivée, y compris à l'envoi. Sans ce contrôle,
  // la dernière étape partirait sans qu'aucun champ obligatoire soit vérifié.
  form.addEventListener("submit", function (e) {
    if (!etapeValide(etapes[etapes.length - 1])) e.preventDefault();
  });

  // Choisir une option fait disparaître le message d'erreur de l'étape
  form.addEventListener("change", function (e) {
    if (e.target.type === "radio" || e.target.type === "checkbox") {
      retirerAlerte(etapes[courante]);
    }
  });

  afficher(0, false);
})();

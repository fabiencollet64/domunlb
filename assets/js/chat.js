/* Assistant Domun LB — widget de discussion guidée.

   Ce n'est pas un agent conversationnel : les réponses sont écrites à
   l'avance et reprennent le contenu du site (services, tarifs, déroulé de la
   mise en place). Aucune réponse n'est générée, donc aucune information ne
   peut être inventée. Chaque branche se termine par un chemin humain :
   appeler, ou être rappelé via le formulaire.

   Pour brancher un service de discussion avec un conseiller, c'est ce fichier
   qu'il faut remplacer : le balisage du panneau et ses styles restent
   valables, seule la source des messages change.

   Sans JavaScript, le lanceur n'est jamais révélé : aucun bouton inerte
   n'apparaît et le téléphone de l'en-tête reste le chemin de contact.
*/
(function () {
  "use strict";

  var racine = document.querySelector("[data-chat]");
  if (!racine) return;

  var lanceur = racine.querySelector("[data-chat-ouvrir]");
  var panneau = racine.querySelector("#chat-panneau");
  var fermer = racine.querySelector("[data-chat-fermer]");
  var fil = racine.querySelector("[data-chat-fil]");
  var zoneChoix = racine.querySelector("[data-chat-choix]");
  var titre = racine.querySelector(".chat__titre");
  var prefixe = racine.getAttribute("data-prefixe") || "";

  function lien(cible, libelle) {
    return '<a href="' + prefixe + cible + '">' + libelle + "</a>";
  }

  var ARBRE = {
    accueil: {
      message:
        "Bonjour. Je réponds aux questions les plus courantes. " +
        "Que souhaitez-vous savoir&nbsp;?",
      options: [
        ["Quels services proposez-vous&nbsp;?", "services"],
        ["Combien cela coûte&nbsp;?", "tarifs"],
        ["Comment cela se met en place&nbsp;?", "demarrage"],
        ["Je cherche un emploi", "emploi"]
      ]
    },
    services: {
      message:
        "Nous intervenons de quatre façons&nbsp;:<ul>" +
        "<li>" + lien("services/auxiliaire-de-vie.html", "Auxiliaire de vie") +
        "&nbsp;: aide au lever, à la toilette, aux repas.</li>" +
        "<li>" + lien("services/aide-soignante.html", "Aide-soignante") +
        "&nbsp;: soins d'hygiène et de confort.</li>" +
        "<li>" + lien("services/aide-menagere.html", "Aide ménagère") +
        "&nbsp;: entretien du logement et du linge.</li>" +
        "<li>" + lien("services/mandataire.html", "Mode mandataire") +
        "&nbsp;: vous êtes l'employeur, nous gérons l'administratif.</li></ul>",
      options: [
        ["Combien cela coûte&nbsp;?", "tarifs"],
        ["Comment cela se met en place&nbsp;?", "demarrage"],
        ["Je préfère qu'on me rappelle", "rappel"]
      ]
    },
    tarifs: {
      message:
        "Les tarifs horaires vont de 26&nbsp;€ pour l'aide ménagère à 34&nbsp;€ " +
        "pour une aide-soignante. Le crédit d'impôt de 50&nbsp;% ramène le " +
        "reste à charge à la moitié, que vous soyez imposable ou non. " +
        "Le détail et les aides possibles sont sur la page " +
        lien("tarifs.html", "Tarifs") + ". Ces montants sont indicatifs&nbsp;: " +
        "le tarif définitif figure sur le devis, remis après une visite " +
        "d'évaluation gratuite.",
      options: [
        ["Quelles aides puis-je obtenir&nbsp;?", "aides"],
        ["Comment cela se met en place&nbsp;?", "demarrage"],
        ["Je préfère qu'on me rappelle", "rappel"]
      ]
    },
    aides: {
      message:
        "Trois aides peuvent s'ajouter au crédit d'impôt&nbsp;: l'APA versée " +
        "par le département, une participation de votre caisse de retraite, " +
        "et parfois votre mutuelle ou votre contrat de prévoyance. Savoir ce " +
        "à quoi vous avez droit demande d'examiner votre situation&nbsp;: " +
        "nous montons le dossier avec vous.",
      options: [
        ["Je préfère qu'on me rappelle", "rappel"],
        ["Voir la page Tarifs", "tarifs"]
      ]
    },
    demarrage: {
      message:
        "En quatre étapes&nbsp;: vous nous appelez, nous venons évaluer les " +
        "besoins à domicile (c'est gratuit et sans engagement), vous recevez " +
        "un devis clair, puis vous rencontrez l'intervenant avant son premier " +
        "jour. Comptez quelques jours, moins en cas d'urgence.",
      options: [
        ["Je préfère qu'on me rappelle", "rappel"],
        ["Combien cela coûte&nbsp;?", "tarifs"]
      ]
    },
    emploi: {
      message:
        "Nous recrutons toute l'année des auxiliaires de vie, aides-soignantes " +
        "et aides ménagères. Vous pouvez déposer votre candidature sur la page " +
        lien("candidature.html", "Candidature") + ", ou nous appeler " +
        "directement&nbsp;: nous prenons aussi les candidatures par téléphone.",
      options: [["Autre question", "accueil"]]
    },
    rappel: {
      message:
        "Le formulaire de la " + lien("index.html", "page d'accueil") +
        " prend deux minutes et nous permet de vous rappeler en connaissant " +
        "déjà votre situation. Si vous préférez, le numéro ci-dessous est " +
        "ouvert du lundi au samedi, de 8h à 19h.",
      options: [["Autre question", "accueil"]]
    }
  };

  /* --- Rendu ------------------------------------------------------------ */
  function ajouterMessage(html, auteur) {
    var p = document.createElement("p");
    p.className = "chat__message chat__message--" + auteur;
    if (auteur === "visiteur") {
      p.textContent = html.replace(/&nbsp;/g, " ");
    } else {
      p.innerHTML = html;
    }
    fil.appendChild(p);
    fil.scrollTop = fil.scrollHeight;
  }

  function afficherChoix(options) {
    zoneChoix.textContent = "";
    options.forEach(function (option) {
      var bouton = document.createElement("button");
      bouton.type = "button";
      bouton.className = "bouton bouton--secondaire";
      bouton.innerHTML = option[0];
      bouton.addEventListener("click", function () {
        ajouterMessage(option[0], "visiteur");
        aller(option[1]);
      });
      zoneChoix.appendChild(bouton);
    });
  }

  function aller(cle) {
    var noeud = ARBRE[cle];
    if (!noeud) return;
    ajouterMessage(noeud.message, "assistant");
    afficherChoix(noeud.options);
  }

  /* --- Ouverture et fermeture ------------------------------------------- */
  var demarre = false;

  function ouvrir() {
    panneau.hidden = false;
    lanceur.setAttribute("aria-expanded", "true");
    if (!demarre) {
      demarre = true;
      aller("accueil");
    }
    titre.focus();
  }

  function refermer() {
    panneau.hidden = true;
    lanceur.setAttribute("aria-expanded", "false");
    lanceur.focus();
  }

  lanceur.hidden = false;
  lanceur.addEventListener("click", function () {
    if (panneau.hidden) ouvrir();
    else refermer();
  });
  fermer.addEventListener("click", refermer);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panneau.hidden) refermer();
  });
})();

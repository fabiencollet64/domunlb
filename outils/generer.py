# -*- coding: utf-8 -*-
"""Génère les pages HTML statiques du site Domun LB.

    python3 outils/generer.py

Le contenu rédactionnel (chiffres, tarifs, témoignages) est un contenu
d'amorçage à faire valider par Domun LB — voir README.md § Contenu.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gabarits as g

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ecrire(chemin_relatif, html):
    chemin = os.path.join(RACINE, chemin_relatif)
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html)
    print("écrit  " + chemin_relatif)


ICONES = {
    "coeur": '<path d="M12 21s-8-5.2-8-11a4.6 4.6 0 0 1 8-3 4.6 4.6 0 0 1 8 3c0 5.8-8 11-8 11z"/>',
    "soin": '<path d="M13 3h-2v6H5v2h6v6h2v-6h6V9h-6z"/>',
    "maison": '<path d="M12 3 2 11h3v9h6v-6h2v6h6v-9h3z"/>',
    "dossier": '<path d="M4 4h6l2 2h8v14H4z"/>',
}


def icone(nom):
    return (f'<span class="carte__icone" aria-hidden="true">'
            f'<svg viewBox="0 0 24 24">{ICONES[nom]}</svg></span>')


# ---------------------------------------------------------------------------
# Les quatre services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "fichier": "services/auxiliaire-de-vie.html",
        "titre": "Auxiliaire de vie",
        "icone": "coeur",
        "resume": "Un accompagnement quotidien pour rester chez soi en sécurité, "
                  "du lever au coucher.",
        "description": "Auxiliaire de vie à domicile : aide au lever, à la toilette, "
                       "aux repas et à la vie sociale.",
        "missions": [
            "Aide au lever, au coucher et aux déplacements dans le logement",
            "Aide à la toilette, à l'habillage et à la prise des repas",
            "Courses, préparation des repas et accompagnement aux rendez-vous",
            "Présence et compagnie, maintien du lien social",
            "Veille sur l'état général et alerte de la famille en cas de changement",
        ],
        "pour_qui": "Pour une personne âgée ou en perte d'autonomie qui souhaite "
                    "continuer à vivre chez elle, avec une présence régulière.",
        "rythme": "D'une heure par semaine à une présence quotidienne, y compris "
                  "le week-end.",
    },
    {
        "fichier": "services/aide-soignante.html",
        "titre": "Aide-soignante",
        "icone": "soin",
        "resume": "Des soins d'hygiène et de confort réalisés par un personnel "
                  "diplômé, en lien avec le médecin traitant.",
        "description": "Aide-soignante à domicile : soins d'hygiène, de confort et "
                       "surveillance, en coordination avec l'équipe médicale.",
        "missions": [
            "Soins d'hygiène et de confort adaptés à l'état de santé",
            "Aide à la mobilisation et prévention des escarres",
            "Surveillance des constantes et de l'état général",
            "Accompagnement au retour d'hospitalisation",
            "Transmission écrite à la famille et au médecin traitant",
        ],
        "pour_qui": "Pour une personne dont l'état de santé demande des gestes "
                    "professionnels que l'entourage ne peut pas assurer seul.",
        "rythme": "Passages quotidiens, matin et soir, selon la prescription et "
                  "l'évaluation réalisée à domicile.",
    },
    {
        "fichier": "services/aide-menagere.html",
        "titre": "Aide ménagère",
        "icone": "maison",
        "resume": "Un logement propre et ordonné, sans effort et sans risque de "
                  "chute.",
        "description": "Aide ménagère à domicile : ménage, linge, courses et "
                       "entretien courant du logement.",
        "missions": [
            "Entretien courant des pièces de vie, de la cuisine et de la salle de bain",
            "Lavage, repassage et rangement du linge",
            "Courses et préparation des repas simples",
            "Rangement et remise en ordre après un retour d'hospitalisation",
            "Petits gestes du quotidien qui deviennent difficiles ou risqués",
        ],
        "pour_qui": "Pour toute personne qui ne peut plus assurer l'entretien de "
                    "son logement sans se mettre en danger.",
        "rythme": "À partir de deux heures par semaine, à jour et horaire fixes "
                  "pour garder des repères.",
    },
    {
        "fichier": "services/mandataire.html",
        "titre": "Mode mandataire",
        "icone": "dossier",
        "resume": "Vous êtes l'employeur de votre intervenant, nous prenons en "
                  "charge toutes les démarches administratives.",
        "description": "Mode mandataire : Domun LB recrute et gère l'administratif, "
                       "la famille reste l'employeur.",
        "missions": [
            "Recherche, sélection et présentation des candidats",
            "Rédaction du contrat de travail et des avenants",
            "Établissement des bulletins de paie et des déclarations sociales",
            "Gestion des congés, des absences et du remplacement",
            "Accompagnement en cas de fin de contrat",
        ],
        "pour_qui": "Pour une famille qui veut choisir elle-même l'intervenant et "
                    "garder la main sur l'organisation, sans gérer la paperasse.",
        "rythme": "Le volume horaire est fixé librement par vous, dans le respect "
                  "du droit du travail.",
    },
]


def page_service(s):
    missions = "".join(f"<li>{m}</li>" for m in s["missions"])
    autres = "".join(
        f"""<article class="carte carte--lien">
          {icone(a['icone'])}
          <h3><a class="carte__lien" href="../{a['fichier']}">{a['titre']}</a></h3>
          <p>{a['resume']}</p>
        </article>"""
        for a in SERVICES if a["fichier"] != s["fichier"]
    )

    corps = f"""{g.fil_ariane([("index.html", "Accueil"), (None, s['titre'])], prof=1)}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <p class="badge">Service d'aide à domicile</p>
    <h1>{s['titre']}</h1>
    <p class="chapo">{s['resume']}</p>
    <div class="groupe-boutons">
      {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
      <a class="bouton bouton--secondaire" href="../tarifs.html">Voir les tarifs</a>
    </div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <div class="duo">
      <div>
        <h2>Ce que fait l'intervenant</h2>
        <ul class="liste-puces">{missions}</ul>
      </div>
      <div class="carte">
        <h3>Pour qui&nbsp;?</h3>
        <p>{s['pour_qui']}</p>
        <h3>À quel rythme&nbsp;?</h3>
        <p>{s['rythme']}</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Comment cela se passe</h2>
    <ol class="etapes">
      <li><strong>Vous nous appelez.</strong> Nous prenons le temps de comprendre
        la situation, sans engagement de votre part.</li>
      <li><strong>Nous venons évaluer à domicile.</strong> La visite est gratuite.
        Nous regardons ensemble les besoins réels et le logement.</li>
      <li><strong>Nous vous proposons un intervenant.</strong> Vous le rencontrez
        avant le début de la mission.</li>
      <li><strong>Nous suivons la mission.</strong> Un référent reste joignable et
        organise les remplacements.</li>
    </ol>
    <div class="encadre">
      <h3>Aides financières</h3>
      <p>Une partie du coût peut être prise en charge&nbsp;: crédit d'impôt sur les
        services à la personne, APA, caisse de retraite, mutuelle. Nous vous aidons
        à monter le dossier et à savoir ce à quoi vous avez droit.</p>
      <a class="bouton bouton--secondaire" href="../tarifs.html">Comprendre le coût réel</a>
    </div>
  </div>
</section>

<section class="section section--serree">
  <div class="conteneur">
    <h2>Nos autres services</h2>
    <div class="grille">{autres}</div>
  </div>
</section>

{g.rappel_action(prof=1)}"""

    return g.page(
        titre=s["titre"], description=s["description"], corps=corps,
        page_active=s["fichier"], prof=1, classe_body="page-service",
    )


for s in SERVICES:
    ecrire(s["fichier"], page_service(s))


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
cartes_services = "".join(
    f"""<article class="carte carte--lien">
      {icone(s['icone'])}
      <h3><a class="carte__lien" href="{s['fichier']}">{s['titre']}</a></h3>
      <p>{s['resume']}</p>
    </article>"""
    for s in SERVICES
)

accueil = f"""<section class="section section--degrade">
  <div class="conteneur">
    <div class="duo">
      <div class="entete-page">
        <h1>Rester chez soi, bien entouré</h1>
        <p class="chapo">Domun LB accompagne à domicile les personnes âgées et en
          perte d'autonomie&nbsp;: aide au quotidien, soins, entretien du logement.
          Un référent joignable, des intervenants que vous rencontrez avant le
          début de la mission.</p>
        <div class="groupe-boutons">
          {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
          <a class="bouton bouton--inverse" href="tarifs.html">Voir nos tarifs</a>
        </div>
      </div>
      <div class="carte carte--marque">
        <h2>Un premier échange gratuit</h2>
        <ul class="liste-puces">
          <li>Une évaluation à domicile sans frais et sans engagement</li>
          <li>Une réponse sous 48&nbsp;heures</li>
          <li>Un devis clair, avec le reste à charge après crédit d'impôt</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Nos quatre services</h2>
    <p>Chaque situation est différente. Nous partons de vos besoins réels, pas
      d'une formule toute faite.</p>
    <div class="grille">{cartes_services}</div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Ce sur quoi vous pouvez compter</h2>
    <div class="grille">
      <div class="carte">
        <p class="badge">Intervenants formés</p>
        <p>Nos intervenants sont recrutés sur leur expérience et leurs
          références, puis accompagnés tout au long de la mission.</p>
      </div>
      <div class="carte">
        <p class="badge">Continuité assurée</p>
        <p>En cas d'absence, nous organisons le remplacement. Vous n'avez pas à
          chercher une solution dans l'urgence.</p>
      </div>
      <div class="carte">
        <p class="badge">Un référent joignable</p>
        <p>Une personne suit votre dossier et connaît votre situation. Vous
          n'expliquez pas tout depuis le début à chaque appel.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Comment démarrer</h2>
    <ol class="etapes">
      <li><strong>Vous nous appelez au {g.TEL_AFFICHE}.</strong> Nous écoutons la
        situation et répondons à vos premières questions.</li>
      <li><strong>Nous venons chez vous.</strong> La visite d'évaluation est
        gratuite et sans engagement.</li>
      <li><strong>Vous recevez un devis clair.</strong> Le tarif horaire et le
        reste à charge estimé après crédit d'impôt y figurent.</li>
      <li><strong>La mission commence.</strong> Vous rencontrez l'intervenant
        avant son premier jour.</li>
    </ol>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Ce que disent les familles</h2>
    <div class="grille">
      <article class="carte">
        {g.etoiles(5)}
        <blockquote><p>«&nbsp;Ma mère a gardé le même intervenant pendant deux ans.
          C'est ce qui a le plus compté pour elle.&nbsp;»</p></blockquote>
        <p><strong>Claire M.</strong></p>
      </article>
      <article class="carte">
        {g.etoiles(5)}
        <blockquote><p>«&nbsp;On nous a expliqué le crédit d'impôt clairement,
          devis à l'appui. Aucune mauvaise surprise.&nbsp;»</p></blockquote>
        <p><strong>Bernard T.</strong></p>
      </article>
      <article class="carte">
        {g.etoiles(4)}
        <blockquote><p>«&nbsp;Le remplacement pendant les congés a été organisé
          sans que j'aie à m'en occuper.&nbsp;»</p></blockquote>
        <p><strong>Sylvie D.</strong></p>
      </article>
    </div>
  </div>
</section>

{g.rappel_action()}"""

ecrire("index.html", g.page(
    titre="Aide à domicile pour personnes âgées",
    description="Domun LB : auxiliaire de vie, aide-soignante, aide ménagère et "
                "mode mandataire. Évaluation à domicile gratuite. " + g.TEL_AFFICHE,
    corps=accueil, page_active="index.html", prof=0,
))


# ---------------------------------------------------------------------------
# Tarifs
# ---------------------------------------------------------------------------
LIGNES_TARIFS = [
    ("Aide ménagère", "26,00 €", "13,00 €", "En semaine, journée"),
    ("Auxiliaire de vie", "28,00 €", "14,00 €", "En semaine, journée"),
    ("Aide-soignante", "34,00 €", "17,00 €", "Sur évaluation, en lien avec le médecin"),
    ("Mode mandataire", "Frais de gestion mensuels", "50 % du montant", "Salaire de l'intervenant en sus"),
]
lignes = "".join(
    f'<tr><th scope="row">{n}</th><td class="tarif">{t}</td>'
    f'<td class="tarif">{r}</td><td>{c}</td></tr>'
    for n, t, r, c in LIGNES_TARIFS
)

tarifs = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Tarifs")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <h1>Nos tarifs</h1>
    <p class="chapo">Un tarif horaire, pas de frais de dossier, pas d'abonnement.
      Ce que vous payez réellement, c'est la colonne «&nbsp;reste à charge&nbsp;».</p>
  </div>
</section>

<section class="section section--serree">
  <div class="conteneur">
    <div class="tableau-enveloppe">
      <table class="tableau">
        <caption>Tarifs horaires indicatifs et reste à charge après crédit d'impôt de 50&nbsp;%</caption>
        <thead>
          <tr>
            <th scope="col">Service</th>
            <th scope="col">Tarif horaire</th>
            <th scope="col">Reste à charge estimé</th>
            <th scope="col">Conditions</th>
          </tr>
        </thead>
        <tbody>{lignes}</tbody>
      </table>
    </div>
    <p><strong>Tarifs indicatifs.</strong> Le tarif définitif figure sur le devis
      remis après la visite d'évaluation, qui est gratuite. Majorations
      applicables les dimanches et jours fériés.</p>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Le crédit d'impôt, concrètement</h2>
    <div class="duo">
      <div>
        <p>Les services à la personne ouvrent droit à un crédit d'impôt de
          <span class="surligne">50&nbsp;% des sommes versées</span>, dans la limite
          d'un plafond annuel. Il s'applique que vous soyez imposable ou non.</p>
        <p>Avec l'avance immédiate, la réduction est appliquée au moment du
          paiement&nbsp;: vous ne réglez que la moitié, sans attendre l'année
          suivante. Nous nous occupons de la déclaration du service.</p>
      </div>
      <div class="carte">
        <h3>Un exemple</h3>
        <ul class="liste-puces">
          <li>4&nbsp;heures d'aide ménagère par semaine</li>
          <li>Soit environ 416&nbsp;€ par mois</li>
          <li><strong>Reste à charge estimé&nbsp;: environ 208&nbsp;€ par mois</strong></li>
        </ul>
        <p>Cet exemple est donné à titre indicatif et ne tient pas compte des
          aides complémentaires.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Les aides qui peuvent s'ajouter</h2>
    <div class="grille">
      <div class="carte">
        <h3>APA</h3>
        <p>L'allocation personnalisée d'autonomie est versée par le département
          selon le degré de perte d'autonomie et les ressources.</p>
      </div>
      <div class="carte">
        <h3>Caisse de retraite</h3>
        <p>De nombreuses caisses financent une partie des heures d'aide à
          domicile pour leurs affiliés.</p>
      </div>
      <div class="carte">
        <h3>Mutuelle et prévoyance</h3>
        <p>Certains contrats prévoient une aide après une hospitalisation ou en
          cas de perte d'autonomie.</p>
      </div>
    </div>
    <div class="encadre">
      <h3>Nous montons le dossier avec vous</h3>
      <p>Savoir à quoi on a droit prend du temps. Appelez-nous&nbsp;: nous
        regardons ensemble ce qui s'applique à votre situation.</p>
      {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
    </div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur faq">
    <h2>Questions fréquentes</h2>
    <details>
      <summary>La visite d'évaluation est-elle payante&nbsp;?</summary>
      <p>Non. La visite à domicile et le devis qui en découle sont gratuits et
        sans engagement.</p>
    </details>
    <details>
      <summary>Y a-t-il un nombre d'heures minimum&nbsp;?</summary>
      <p>Nous intervenons à partir de deux heures par semaine. En dessous, il est
        souvent plus juste de vous orienter vers une autre solution.</p>
    </details>
    <details>
      <summary>Que se passe-t-il si l'intervenant est absent&nbsp;?</summary>
      <p>Nous organisons le remplacement et vous prévenons. Vous n'avez pas de
        démarche à faire.</p>
    </details>
    <details>
      <summary>Puis-je arrêter à tout moment&nbsp;?</summary>
      <p>Oui, avec un préavis indiqué au contrat. Il n'y a ni engagement de durée
        ni frais de résiliation.</p>
    </details>
  </div>
</section>

{g.rappel_action()}"""

ecrire("tarifs.html", g.page(
    titre="Tarifs et aides financières",
    description="Tarifs horaires Domun LB, reste à charge après crédit d'impôt de "
                "50 %, APA, caisse de retraite. Devis gratuit.",
    corps=tarifs, page_active="tarifs.html", prof=0,
))


# ---------------------------------------------------------------------------
# Candidature
# ---------------------------------------------------------------------------
POSTES = [s["titre"] for s in SERVICES[:3]] + ["Je ne sais pas encore"]
options_poste = "".join(
    f'<div class="choix"><input type="radio" id="poste-{i}" name="poste" value="{p}">'
    f'<label for="poste-{i}">{p}</label></div>'
    for i, p in enumerate(POSTES)
)

candidature = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Candidature")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <p class="badge">Nous recrutons</p>
    <h1>Rejoindre Domun LB</h1>
    <p class="chapo">Vous êtes auxiliaire de vie, aide-soignante ou aide
      ménagère&nbsp;? Nous recrutons toute l'année. Le formulaire prend cinq
      minutes. Si vous préférez, appelez-nous au {g.TEL_AFFICHE}.</p>
  </div>
</section>

<section class="section section--clair section--serree">
  <div class="conteneur">
    <h2>Travailler chez nous</h2>
    <div class="grille">
      <div class="carte">
        <p class="badge">Secteur d'intervention limité</p>
        <p>Nous construisons les plannings par secteur pour réduire les trajets
          entre deux interventions.</p>
      </div>
      <div class="carte">
        <p class="badge">Planning stable</p>
        <p>Des horaires fixes d'une semaine à l'autre autant que possible, et des
          bénéficiaires réguliers.</p>
      </div>
      <div class="carte">
        <p class="badge">Une équipe joignable</p>
        <p>Un référent que vous pouvez appeler pendant vos interventions en cas
          de difficulté.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Votre candidature</h2>
    <p>Les champs suivis de <span class="champ__obligatoire">(obligatoire)</span>
      doivent être remplis.</p>

    <form class="formulaire" action="#" method="post" novalidate>
      <fieldset>
        <legend>Vos coordonnées</legend>

        <div class="champ">
          <label class="champ__libelle" for="nom">
            Nom et prénom <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <input type="text" id="nom" name="nom" autocomplete="name" required>
        </div>

        <div class="champ">
          <label class="champ__libelle" for="telephone">
            Téléphone <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <span class="champ__aide" id="aide-telephone">
            Pour vous rappeler. Exemple&nbsp;: 06 12 34 56 78
          </span>
          <input type="tel" id="telephone" name="telephone" autocomplete="tel"
                 aria-describedby="aide-telephone" required>
        </div>

        <div class="champ">
          <label class="champ__libelle" for="courriel">Adresse électronique</label>
          <span class="champ__aide" id="aide-courriel">
            Facultatif. Nous vous répondrons par téléphone si vous n'en avez pas.
          </span>
          <input type="email" id="courriel" name="courriel" autocomplete="email"
                 aria-describedby="aide-courriel">
        </div>

        <div class="champ">
          <label class="champ__libelle" for="ville">
            Ville ou code postal <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <span class="champ__aide" id="aide-ville">
            Pour vous proposer un secteur proche de chez vous.
          </span>
          <input type="text" id="ville" name="ville" autocomplete="postal-code"
                 aria-describedby="aide-ville" required>
        </div>
      </fieldset>

      <fieldset>
        <legend>Le poste</legend>

        <div class="champ">
          <p class="champ__libelle" id="libelle-poste">Quel poste vous intéresse&nbsp;?</p>
          <div role="radiogroup" aria-labelledby="libelle-poste">{options_poste}</div>
        </div>

        <div class="champ">
          <label class="champ__libelle" for="experience">Années d'expérience</label>
          <select id="experience" name="experience">
            <option value="">Sélectionnez une réponse</option>
            <option>Moins d'un an</option>
            <option>De 1 à 3 ans</option>
            <option>De 3 à 10 ans</option>
            <option>Plus de 10 ans</option>
          </select>
        </div>

        <div class="champ">
          <label class="champ__libelle" for="disponibilite">Vos disponibilités</label>
          <span class="champ__aide" id="aide-dispo">
            Jours, horaires, temps plein ou temps partiel.
          </span>
          <textarea id="disponibilite" name="disponibilite" rows="4"
                    aria-describedby="aide-dispo"></textarea>
        </div>

        <div class="champ">
          <div class="choix">
            <input type="checkbox" id="permis" name="permis" value="oui">
            <label for="permis">Je dispose du permis B et d'un véhicule</label>
          </div>
        </div>
      </fieldset>

      <fieldset>
        <legend>Votre message</legend>
        <div class="champ">
          <label class="champ__libelle" for="message">
            Quelques mots sur votre parcours
          </label>
          <span class="champ__aide" id="aide-message">
            Inutile de rédiger une lettre de motivation. Dites-nous simplement ce
            que vous avez fait et ce que vous cherchez.
          </span>
          <textarea id="message" name="message" rows="6"
                    aria-describedby="aide-message"></textarea>
        </div>
        <div class="champ">
          <div class="choix">
            <input type="checkbox" id="consentement" name="consentement"
                   value="oui" required>
            <label for="consentement">
              J'accepte que Domun LB conserve ces informations pour traiter ma
              candidature <span class="champ__obligatoire">(obligatoire)</span>
            </label>
          </div>
        </div>
      </fieldset>

      <button class="bouton bouton--principal bouton--large" type="submit">
        Envoyer ma candidature
      </button>
    </form>

    <div class="encadre">
      <h3>Vous préférez le téléphone&nbsp;?</h3>
      <p>Appelez-nous du lundi au samedi, de 8h à 19h. Nous prenons votre
        candidature directement par téléphone.</p>
      {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
    </div>
  </div>
</section>"""

ecrire("candidature.html", g.page(
    titre="Candidature et recrutement",
    description="Domun LB recrute auxiliaires de vie, aides-soignantes et aides "
                "ménagères. Candidatez en ligne ou au " + g.TEL_AFFICHE + ".",
    corps=candidature, page_active="candidature.html", prof=0,
))


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------
ARTICLES = [
    ("Crédit d'impôt : ce qui change pour l'aide à domicile",
     "2026-02-12", "12 février 2026", "Aides financières",
     "L'avance immédiate évite d'attendre l'année suivante pour récupérer la "
     "moitié des sommes versées. Voici comment l'activer."),
    ("Six aménagements simples pour éviter les chutes",
     "2026-01-28", "28 janvier 2026", "Prévention",
     "Un tapis, un fil électrique, un éclairage trop faible : la plupart des "
     "chutes à domicile ont des causes évitables."),
    ("Aide à domicile ou maison de retraite : comment décider",
     "2026-01-15", "15 janvier 2026", "Bien choisir",
     "Il n'y a pas de bonne réponse générale. Il y a des critères concrets à "
     "poser, situation par situation."),
    ("Retour d'hospitalisation : organiser les premiers jours",
     "2026-01-03", "3 janvier 2026", "Bien choisir",
     "La sortie d'hôpital est un moment de bascule. Ce qu'il faut avoir prévu "
     "avant le retour à la maison."),
    ("Mode mandataire ou prestataire : quelles différences",
     "2025-12-18", "18 décembre 2025", "Bien choisir",
     "Qui est l'employeur, qui gère la paie, qui remplace en cas d'absence. "
     "Le tableau comparatif."),
    ("Parler d'aide à domicile avec un parent qui refuse",
     "2025-12-05", "5 décembre 2025", "Prévention",
     "Le refus est presque toujours une question de dignité, pas de confort. "
     "Quelques façons d'aborder le sujet."),
]

liste_articles = "".join(
    f"""<article class="carte carte--lien article-liste">
      <p class="article-liste__meta"><span class="badge badge--discret">{cat}</span>
        <span class="visuellement-cache">Publié le </span>
        <time datetime="{iso}">{date}</time></p>
      <h3><a class="carte__lien" href="#">{titre}</a></h3>
      <p>{chapo}</p>
    </article>"""
    for titre, iso, date, cat, chapo in ARTICLES
)

blog = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Blog")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <h1>Le blog</h1>
    <p class="chapo">Des repères concrets sur le maintien à domicile, les aides
      financières et l'organisation du quotidien. Écrit simplement, sans jargon.</p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2 class="visuellement-cache">Tous les articles</h2>
    <div class="grille grille--2">{liste_articles}</div>
  </div>
</section>

{g.rappel_action(
    titre="Une question sur votre situation&nbsp;?",
    texte="Un article ne remplace pas un échange. Appelez-nous, nous prenons le "
          "temps de vous répondre.")}"""

ecrire("blog.html", g.page(
    titre="Blog — maintien à domicile et aides",
    description="Conseils Domun LB sur le maintien à domicile, les aides "
                "financières, la prévention des chutes et le choix d'un service.",
    corps=blog, page_active="blog.html", prof=0,
))


# ---------------------------------------------------------------------------
# Charte graphique (page de référence du système de design)
# ---------------------------------------------------------------------------
PALETTE = [
    ("--navy",   "#0a1557", "Texte principal, titres, pied de page"),
    ("--violet", "#4c1472", "Couleur de marque, aplats de section, icônes"),
    ("--rose",   "#d12686", "Boutons d'action et accents, jamais en texte courant"),
    ("--bleu",   "#b9d1f4", "Fonds de section clairs, cartes, encadrés"),
    ("--jaune",  "#fdd377", "Badges, puces, surlignage, étoiles d'avis"),
    ("--blanc",  "#ffffff", "Fond de page"),
]
nuancier = "".join(
    f"""<article class="carte">
      <span style="display:block;height:5rem;border-radius:var(--rayon-s);
                   border:2px solid var(--navy);background:{hexa}"></span>
      <h3><code>{jeton}</code></h3>
      <p><strong>{hexa}</strong></p>
      <p>{usage}</p>
    </article>"""
    for jeton, hexa, usage in PALETTE
)

COMBINAISONS = [
    ("Navy sur blanc", "16,70:1", "Texte courant, titres"),
    ("Navy sur bleu clair", "10,72:1", "Texte sur section claire, cartes"),
    ("Blanc sur violet", "12,72:1", "Aplats de section et en-têtes"),
    ("Blanc sur navy", "16,70:1", "Pied de page, bas du dégradé"),
    ("Blanc sur rose", "4,85:1", "Libellé du bouton principal"),
    ("Violet sur blanc", "12,72:1", "Libellé du bouton secondaire"),
    ("Navy sur jaune", "11,74:1", "Badges et surlignage uniquement"),
]
lignes_contraste = "".join(
    f'<tr><th scope="row">{c}</th><td class="tarif">{r}</td><td>{u}</td></tr>'
    for c, r, u in COMBINAISONS
)

INTERDITS = [
    "Du texte posé sur le jaune en couleur claire — le jaune ne porte que du navy.",
    "Du texte clair sur le bleu clair — le bleu clair ne reçoit que du navy.",
    "Du rose en texte courant, en titre ou en lien de paragraphe.",
    "Un dégradé du violet vers le rose — seul violet vers navy est autorisé.",
    "Une septième couleur, y compris un gris de remplissage ou un rouge d'erreur.",
    "Un libellé de champ affiché uniquement en texte indicatif (placeholder).",
    "Une zone cliquable de moins de 48 px, ou un texte de corps sous 18 px.",
]
liste_interdits = "".join(f"<li>{i}</li>" for i in INTERDITS)

charte = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Charte graphique")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <h1>Charte graphique Domun LB</h1>
    <p class="chapo">Référence du système de design&nbsp;: palette, typographie,
      composants et règles d'accessibilité. Toute page du site doit pouvoir se
      construire avec les seuls éléments présentés ici.</p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Palette</h2>
    <p>Six couleurs, aucune autre. Elles sont déclarées une seule fois, dans
      <code>assets/css/tokens.css</code>, et ne sont jamais écrites en dur
      ailleurs.</p>
    <div class="grille grille--4">{nuancier}</div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Contrastes vérifiés</h2>
    <p>Toutes les associations utilisées sur le site dépassent le seuil de
      4,5:1. La vérification est rejouable&nbsp;:
      <code>python3 outils/verifier-contrastes.py</code>.</p>
    <div class="tableau-enveloppe">
      <table class="tableau">
        <caption>Rapports de contraste des associations autorisées</caption>
        <thead><tr>
          <th scope="col">Association</th>
          <th scope="col">Rapport</th>
          <th scope="col">Usage</th>
        </tr></thead>
        <tbody>{lignes_contraste}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Typographie</h2>
    <div class="duo">
      <div>
        <p>Le corps de texte est à <strong>18&nbsp;px minimum</strong>, porté à
          <strong>20&nbsp;px sur les pages services</strong>. L'interlignage est
          de <strong>1,6</strong> partout.</p>
        <p>Aucune taille n'est écrite en pixels dans le CSS&nbsp;: tout est en
          <code>rem</code>, pour que le réglage «&nbsp;taille du texte&nbsp;» du
          navigateur reste opérant. La longueur de ligne est plafonnée à 68
          caractères.</p>
      </div>
      <div class="carte">
        <p style="font-size:var(--texte-3xl);font-weight:700;line-height:1.2;margin:0">Titre h1</p>
        <p style="font-size:var(--texte-2xl);font-weight:700;line-height:1.2;margin:0">Titre h2</p>
        <p style="font-size:var(--texte-xl);font-weight:700;line-height:1.2;margin:0">Titre h3</p>
        <p style="font-size:var(--texte-m);margin:0">Corps 20&nbsp;px — pages services</p>
        <p style="font-size:var(--texte-s);margin:0">Corps 18&nbsp;px — plancher général</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Boutons</h2>
    <div class="grille">
      <div class="carte">
        <h3>Principal</h3>
        <p>Rose plein, libellé blanc gras. Un seul par écran visible&nbsp;: le
          rose garde sa valeur de signal.</p>
        <p><a class="bouton bouton--principal" href="#contenu">Demander un devis</a></p>
      </div>
      <div class="carte">
        <h3>Secondaire</h3>
        <p>Contour violet sur fond blanc. Pour toutes les actions de second
          rang.</p>
        <p><a class="bouton bouton--secondaire" href="#contenu">En savoir plus</a></p>
      </div>
      <div class="carte carte--marque">
        <h3>Sur aplat de marque</h3>
        <p>Sur violet ou sur le dégradé, le bouton passe en blanc plein.</p>
        <p><a class="bouton bouton--inverse" href="#contenu">Nous contacter</a></p>
      </div>
    </div>
    <p>Tous les boutons font au minimum 48&nbsp;px de haut et 18&nbsp;px de
      libellé.</p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Réassurance en jaune</h2>
    <p>Le jaune ne sert qu'aux micro-éléments&nbsp;: badges, puces, surlignage et
      étoiles d'avis. Il ne porte jamais d'information à lui seul, et reçoit
      toujours un contour navy — sans quoi il serait invisible sur blanc
      (1,42:1).</p>
    <div class="grille">
      <div class="carte">
        <h3>Badge</h3>
        <p><span class="badge">Intervenants formés</span></p>
      </div>
      <div class="carte">
        <h3>Puces</h3>
        <ul class="liste-puces"><li>Devis gratuit</li><li>Sans engagement</li></ul>
      </div>
      <div class="carte">
        <h3>Surlignage</h3>
        <p>Un crédit d'impôt de <span class="surligne">50&nbsp;%</span>.</p>
      </div>
      <div class="carte">
        <h3>Étoiles d'avis</h3>
        {g.etoiles(5)}
      </div>
    </div>
  </div>
</section>

<section class="section section--degrade">
  <div class="conteneur">
    <h2>Dégradé</h2>
    <p>Cette section est le seul dégradé autorisé&nbsp;: violet vers navy. Le
      texte blanc reste conforme aux deux extrémités (12,72:1 sur violet,
      16,70:1 sur navy). Le dégradé violet vers rose est interdit.</p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Champs de formulaire</h2>
    <p>Le libellé est toujours visible <strong>au-dessus</strong> du champ. Le
      texte indicatif ne remplace jamais le libellé. Les erreurs associent une
      icône et un texte&nbsp;: jamais la couleur seule.</p>
    <form class="formulaire" action="#" onsubmit="return false">
      <div class="champ">
        <label class="champ__libelle" for="demo-nom">Nom et prénom</label>
        <input type="text" id="demo-nom" name="demo-nom" autocomplete="name">
      </div>
      <div class="champ champ--erreur">
        <label class="champ__libelle" for="demo-tel">Téléphone</label>
        <span class="champ__aide" id="demo-aide">Exemple&nbsp;: 06 12 34 56 78</span>
        <input type="tel" id="demo-tel" name="demo-tel"
               aria-describedby="demo-aide demo-erreur" aria-invalid="true" value="06 12">
        <p class="champ__erreur" id="demo-erreur">
          Ce numéro est incomplet. Saisissez les 10 chiffres.
        </p>
      </div>
    </form>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Ce qui est interdit</h2>
    <ul class="liste-puces">{liste_interdits}</ul>
  </div>
</section>"""

ecrire("charte.html", g.page(
    titre="Charte graphique et système de design",
    description="Référence du système de design Domun LB : palette, contrastes, "
                "typographie, composants et règles d'accessibilité.",
    corps=charte, page_active="charte.html", prof=0,
))

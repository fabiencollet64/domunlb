# -*- coding: utf-8 -*-
"""Génère les pages HTML statiques du site Domun LB.

    python3 outils/generer.py

Le contenu rédactionnel (chiffres, tarifs, témoignages) est un contenu
d'amorçage à faire valider par Domun LB — voir README.md § Contenu.
"""
import hashlib
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
# Feuille de style et empreinte de version
# ---------------------------------------------------------------------------
FEUILLES = ("tokens.css", "base.css", "mise-en-page.css", "composants.css")
SCRIPTS = ("navigation.js", "qualification.js", "chat.js")


def construire_css():
    """Concatène les feuilles en un seul fichier et calcule l'empreinte.

    Les quatre feuilles étaient auparavant assemblées par des @import dans
    domun.css. Deux inconvénients : le navigateur devait charger domun.css,
    l'analyser, puis aller chercher quatre fichiers de plus — une cascade qui
    retarde le premier rendu ; et surtout chacun de ces quatre fichiers était
    mis en cache séparément, donc ajouter un numéro de version à domun.css
    n'aurait pas suffi à les rafraîchir. Un navigateur gardant l'ancien CSS
    l'appliquait alors au nouveau HTML, et la page s'affichait cassée sans que
    rien ne le signale.
    """
    css = "\n".join(
        open(os.path.join(RACINE, "assets", "css", f), encoding="utf-8").read()
        for f in FEUILLES
    )
    entete = (
        "/* FICHIER GÉNÉRÉ — ne pas modifier à la main.\n"
        "   Produit par outils/generer.py à partir de : "
        + ", ".join(FEUILLES) + ".\n"
        "   Modifier l'un de ces fichiers, puis relancer la génération. */\n\n"
    )
    chemin = os.path.join(RACINE, "assets", "css", "domun.css")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(entete + css)

    empreinte = hashlib.sha256(css.encode("utf-8"))
    for nom in SCRIPTS:
        with open(os.path.join(RACINE, "assets", "js", nom), "rb") as f:
            empreinte.update(f.read())
    return empreinte.hexdigest()[:10]


g.VERSION = construire_css()
print("css    assets/css/domun.css (version %s)" % g.VERSION)

# ---------------------------------------------------------------------------
# Les quatre services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "fichier": "services/auxiliaire-de-vie.html",
        "image": "auxiliaire-de-vie.jpg",
        "alt": "Une intervenante tient les mains d'une dame âgée et l'écoute, assises face à face.",
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
        "image": "aide-soignante.jpg",
        "alt": "Une aide-soignante, stéthoscope autour du cou, enlace une dame âgée souriante.",
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
        "image": "aide-menagere.jpg",
        "alt": "Une intervenante en tenue professionnelle ouvre les rideaux d'une pièce lumineuse et rangée.",
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
        "image": "mandataire.jpg",
        "alt": "Deux personnes signent un document administratif, l'une désignant un passage du contrat.",
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
  <div class="conteneur">
    <div class="duo">
      <div class="entete-page">
        <p class="badge">Service d'aide à domicile</p>
        <h1>{s['titre']}</h1>
        <p class="chapo">{s['resume']}</p>
        <div class="groupe-boutons">
          {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
          <a class="bouton bouton--secondaire" href="../tarifs.html">Voir les tarifs</a>
        </div>
      </div>
      {g.media(s['image'], s['alt'], prof=1, chargement="eager")}
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

# Formulaire de qualification de la demande, en trois étapes.
# Le HTML porte les trois étapes à la suite : sans JavaScript, le formulaire
# reste entièrement remplissable (cf. assets/js/qualification.js).
def options(nom, intitule, choix, colonnes=False):
    boutons = "".join(
        f'''<div class="qualif__option">
            <input type="radio" id="{nom}-{i}" name="{nom}" value="{c}">
            <label for="{nom}-{i}">{c}</label>
          </div>'''
        for i, c in enumerate(choix)
    )
    paire = " qualif__options--paire" if colonnes else ""
    return f'''<div class="qualif__question">
        <span class="qualif__intitule" id="intitule-{nom}">{intitule}</span>
        <div class="qualif__options{paire}" role="radiogroup"
             aria-labelledby="intitule-{nom}" data-groupe-requis="{nom}">
          {boutons}
        </div>
      </div>'''


formulaire_qualification = f"""<form class="qualif" data-qualification
      action="#" method="post" novalidate aria-labelledby="titre-qualif">
  <h2 id="titre-qualif">Votre demande en 2 minutes</h2>
  <p>Répondez à quelques questions, nous vous rappelons pour préciser le besoin
    et convenir d'une visite d'évaluation gratuite.</p>

  <fieldset class="qualif__etape" data-etape="1">
    <legend>Votre besoin</legend>
    {options("pour-qui", "Pour qui recherchez-vous une aide&nbsp;?",
             ["Pour moi-même", "Pour un proche"], colonnes=True)}
    {options("type-aide", "De quel type d'aide s'agit-il&nbsp;?",
             ["Aide au quotidien (auxiliaire de vie)",
              "Soins et hygiène (aide-soignante)",
              "Entretien du logement (aide ménagère)",
              "Je ne sais pas encore"])}
  </fieldset>

  <fieldset class="qualif__etape" data-etape="2">
    <legend>Le rythme souhaité</legend>
    {options("volume", "Quel volume d'aide envisagez-vous&nbsp;?",
             ["Quelques heures par semaine",
              "Plusieurs heures par jour",
              "Une présence jour et nuit",
              "Je ne sais pas encore"])}
    {options("delai", "Quand souhaitez-vous démarrer&nbsp;?",
             ["Dès que possible", "Dans les 15 jours",
              "Dans le mois", "Je me renseigne"], colonnes=True)}
  </fieldset>

  <fieldset class="qualif__etape" data-etape="3">
    <legend>Vos coordonnées</legend>
    <div class="champ">
      <label class="champ__libelle" for="qualif-cp">
        Code postal <span class="champ__obligatoire">(obligatoire)</span>
      </label>
      <span class="champ__aide" id="qualif-aide-cp">
        Pour vous orienter vers l'équipe de votre secteur.
      </span>
      <input type="text" id="qualif-cp" name="code-postal" required
             inputmode="numeric" autocomplete="postal-code"
             aria-describedby="qualif-aide-cp">
    </div>
    <div class="champ">
      <label class="champ__libelle" for="qualif-nom">
        Nom et prénom <span class="champ__obligatoire">(obligatoire)</span>
      </label>
      <input type="text" id="qualif-nom" name="nom" required autocomplete="name">
    </div>
    <div class="champ">
      <label class="champ__libelle" for="qualif-tel">
        Téléphone <span class="champ__obligatoire">(obligatoire)</span>
      </label>
      <span class="champ__aide" id="qualif-aide-tel">
        C'est par téléphone que nous vous rappelons. Exemple&nbsp;: 06 12 34 56 78
      </span>
      <input type="tel" id="qualif-tel" name="telephone" required
             autocomplete="tel" aria-describedby="qualif-aide-tel">
    </div>
    <div class="champ">
      <label class="champ__libelle" for="qualif-courriel">Adresse électronique</label>
      <span class="champ__aide" id="qualif-aide-courriel">
        Facultatif. Nous vous répondons par téléphone si vous n'en avez pas.
      </span>
      <input type="email" id="qualif-courriel" name="courriel"
             autocomplete="email" aria-describedby="qualif-aide-courriel">
    </div>
    <div class="champ">
      <div class="choix">
        <input type="checkbox" id="qualif-consentement" name="consentement"
               value="oui" required>
        <label for="qualif-consentement">
          J'accepte d'être rappelé par Domun LB au sujet de ma demande
          <span class="champ__obligatoire">(obligatoire)</span>
        </label>
      </div>
    </div>
  </fieldset>

  <button class="bouton bouton--principal bouton--large" type="submit" data-envoi>
    Être rappelé gratuitement
  </button>

  <ul class="reassurance qualif__reassurance">
    <li>Réponse sous 48&nbsp;h</li>
    <li>Évaluation gratuite</li>
    <li>Sans engagement</li>
  </ul>
</form>"""


accueil = f"""<section class="section section--degrade">
  <div class="conteneur">
    <div class="duo duo--formulaire">
      <div class="entete-page">
        <h1>Rester chez soi, bien entouré</h1>
        <p class="chapo">Domun LB accompagne à domicile les personnes âgées et en
          perte d'autonomie&nbsp;: aide au quotidien, soins, entretien du logement.
          Un référent joignable, des intervenants que vous rencontrez avant le
          début de la mission.</p>
        <ul class="liste-puces">
          <li>Une évaluation à domicile sans frais et sans engagement</li>
          <li>Une réponse sous 48&nbsp;heures</li>
          <li>Un devis clair, avec le reste à charge après crédit d'impôt</li>
        </ul>
        <p class="accroche-tel">Vous préférez le téléphone&nbsp;?<br>
          {g.lien_tel(prefixe_libelle="Nous appeler au ")}</p>
      </div>
      {formulaire_qualification}
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
        <h3 class="carte__titre">Intervenants formés</h3>
        <p>Nos intervenants sont recrutés sur leur expérience et leurs
          références, puis accompagnés tout au long de la mission.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Continuité assurée</h3>
        <p>En cas d'absence, nous organisons le remplacement. Vous n'avez pas à
          chercher une solution dans l'urgence.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Un référent joignable</h3>
        <p>Une personne suit votre dossier et connaît votre situation. Vous
          n'expliquez pas tout depuis le début à chaque appel.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Comment démarrer</h2>
    <div class="duo">
      <div>
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
      {g.media("accompagnement.jpg",
               "Une intervenante remonte un plaid sur les épaules d'une dame "
               "âgée installée dans son canapé.")}
    </div>
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
    scripts=("qualification.js",),
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
    <div class="duo">
      <div class="encadre">
        <h3>Nous montons le dossier avec vous</h3>
        <p>Savoir à quoi on a droit prend du temps. Appelez-nous&nbsp;: nous
          regardons ensemble ce qui s'applique à votre situation.</p>
        {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
      </div>
      {g.media("credit-impot.jpg",
               "Une personne calcule un montant à la calculatrice, feuillets "
               "et ordinateur portable posés sur le bureau.")}
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
        <h3 class="carte__titre">Secteur d'intervention limité</h3>
        <p>Nous construisons les plannings par secteur pour réduire les trajets
          entre deux interventions.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Planning stable</h3>
        <p>Des horaires fixes d'une semaine à l'autre autant que possible, et des
          bénéficiaires réguliers.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Une équipe joignable</h3>
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
        <h3 class="carte__titre">Titre de carte</h3>
        <p>Un badge n'est pas un titre&nbsp;: employé ainsi, il occupe toute la
          largeur de la carte et se lit comme un bouton.</p>
      </div>
      <div class="carte">
        <h3>Ligne de réassurance</h3>
        <ul class="reassurance">
          <li>Réponse sous 48&nbsp;h</li>
          <li>Sans engagement</li>
        </ul>
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


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
OBJETS = [
    "Une demande d'aide à domicile",
    "Une question sur les tarifs ou les aides",
    "Une candidature",
    "Autre sujet",
]
options_objet = "".join(
    f'<div class="choix"><input type="radio" id="objet-{i}" name="objet" value="{o}">'
    f'<label for="objet-{i}">{o}</label></div>'
    for i, o in enumerate(OBJETS)
)

contact = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Nous contacter")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <h1>Nous contacter</h1>
    <p class="chapo">Le plus simple reste le téléphone&nbsp;: nous répondons
      nous-mêmes, sans serveur vocal. Si vous préférez écrire, le formulaire
      ci-dessous nous parvient directement.</p>
  </div>
</section>

<section class="section section--serree">
  <div class="conteneur">
    <div class="duo">
      <div class="carte carte--clair">
        <h2>Par téléphone</h2>
        <p>Du lundi au samedi, de 8h à 19h.</p>
        {g.lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
        <p>C'est le moyen le plus rapide, en particulier pour une situation
          urgente ou une sortie d'hospitalisation.</p>
      </div>
      <div class="carte">
        <h2>Ce qui se passe ensuite</h2>
        <ul class="liste-puces">
          <li>Nous vous rappelons sous 48&nbsp;heures ouvrées</li>
          <li>Nous convenons d'une visite d'évaluation à domicile, gratuite
            et sans engagement</li>
          <li>Vous recevez un devis clair, avec le reste à charge estimé après
            crédit d'impôt</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Nous écrire</h2>
    <div class="duo">
      <div>
        <p>Décrivez votre situation en quelques lignes&nbsp;: nous vous
          rappelons en connaissant déjà l'essentiel.</p>
        <p>Les champs suivis de
          <span class="champ__obligatoire">(obligatoire)</span> doivent être
          remplis.</p>
      </div>
      {g.media("contact.jpg",
               "Un couple consulte un ordinateur portable dans sa cuisine, "
               "en souriant.")}
    </div>

    <form class="formulaire" action="#" method="post" novalidate>
      <fieldset>
        <legend>Vos coordonnées</legend>
        <div class="champ">
          <label class="champ__libelle" for="contact-nom">
            Nom et prénom <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <input type="text" id="contact-nom" name="nom" required autocomplete="name">
        </div>
        <div class="champ">
          <label class="champ__libelle" for="contact-tel">
            Téléphone <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <span class="champ__aide" id="contact-aide-tel">
            C'est par téléphone que nous vous répondons.
            Exemple&nbsp;: 06 12 34 56 78
          </span>
          <input type="tel" id="contact-tel" name="telephone" required
                 autocomplete="tel" aria-describedby="contact-aide-tel">
        </div>
        <div class="champ">
          <label class="champ__libelle" for="contact-courriel">Adresse électronique</label>
          <span class="champ__aide" id="contact-aide-courriel">
            Facultatif. Nous vous répondons par téléphone si vous n'en avez pas.
          </span>
          <input type="email" id="contact-courriel" name="courriel"
                 autocomplete="email" aria-describedby="contact-aide-courriel">
        </div>
      </fieldset>

      <fieldset>
        <legend>Votre demande</legend>
        <div class="champ">
          <p class="champ__libelle" id="libelle-objet">Quel est l'objet de votre message&nbsp;?</p>
          <div role="radiogroup" aria-labelledby="libelle-objet">{options_objet}</div>
        </div>
        <div class="champ">
          <label class="champ__libelle" for="contact-message">
            Votre message <span class="champ__obligatoire">(obligatoire)</span>
          </label>
          <span class="champ__aide" id="contact-aide-message">
            Décrivez la situation en quelques lignes&nbsp;: cela nous permet de
            vous rappeler en connaissant déjà l'essentiel.
          </span>
          <textarea id="contact-message" name="message" rows="6" required
                    aria-describedby="contact-aide-message"></textarea>
        </div>
        <div class="champ">
          <div class="choix">
            <input type="checkbox" id="contact-consentement" name="consentement"
                   value="oui" required>
            <label for="contact-consentement">
              J'accepte d'être recontacté par Domun LB au sujet de ma demande
              <span class="champ__obligatoire">(obligatoire)</span>
            </label>
          </div>
        </div>
      </fieldset>

      <button class="bouton bouton--principal bouton--large" type="submit">
        Envoyer mon message
      </button>
    </form>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Vous cherchez autre chose&nbsp;?</h2>
    <div class="grille">
      <div class="carte">
        <h3>Vous voulez postuler</h3>
        <p>Nous recrutons toute l'année. La page dédiée recueille votre
          candidature en cinq minutes.</p>
        <a class="bouton bouton--secondaire" href="candidature.html">Déposer ma candidature</a>
      </div>
      <div class="carte">
        <h3>Vous voulez connaître les tarifs</h3>
        <p>Les tarifs horaires, le crédit d'impôt et les aides mobilisables
          sont détaillés sur la page Tarifs.</p>
        <a class="bouton bouton--secondaire" href="tarifs.html">Voir les tarifs</a>
      </div>
      <div class="carte">
        <h3>Vous préférez qu'on vous rappelle</h3>
        <p>Le formulaire de la page d'accueil qualifie votre besoin en deux
          minutes et nous permet de vous rappeler préparés.</p>
        <a class="bouton bouton--secondaire" href="index.html">Aller au formulaire</a>
      </div>
    </div>
  </div>
</section>"""

ecrire("contact.html", g.page(
    titre="Nous contacter",
    description="Contacter Domun LB : par téléphone au " + g.TEL_AFFICHE +
                " du lundi au samedi 8h–19h, ou par formulaire.",
    corps=contact, page_active="contact.html", prof=0,
))


# ---------------------------------------------------------------------------
# Notre équipe
# ---------------------------------------------------------------------------
# CONTENU D'AMORÇAGE. Ces portraits sont fictifs : ni les prénoms, ni les
# parcours, ni les citations ne viennent de Domun LB. Ils sont là pour que la
# page ait sa forme définitive, et doivent être remplacés par de vrais
# portraits — après accord écrit des personnes concernées, la publication d'un
# nom et d'une photographie relevant de leur consentement.
EQUIPE = [
    ("SM", "Sylvie M.", "Auxiliaire de vie", "14 ans d'expérience",
     "Ce qui compte, c'est de garder les habitudes de la personne. "
     "C'est chez elle, pas chez moi."),
    ("KB", "Karim B.", "Aide-soignant", "9 ans d'expérience",
     "Je note tout ce que j'observe. La famille et le médecin savent "
     "exactement où on en est."),
    ("NF", "Nadia F.", "Aide ménagère", "6 ans d'expérience",
     "Un logement en ordre, c'est moins de chutes. On ne le dit pas assez."),
    ("PL", "Patrick L.", "Auxiliaire de vie", "11 ans d'expérience",
     "J'interviens chez le même monsieur depuis trois ans. On a nos "
     "habitudes, et ça change tout."),
    ("AD", "Amina D.", "Aide-soignante", "17 ans d'expérience",
     "Les retours d'hospitalisation demandent de la vigilance. "
     "Les premiers jours se préparent."),
    ("TR", "Thomas R.", "Auxiliaire de vie", "5 ans d'expérience",
     "Le plus utile, souvent, c'est de prendre le temps de discuter."),
]

portraits = "".join(
    f"""<article class="carte portrait">
      <p class="portrait__avatar" aria-hidden="true">{initiales}</p>
      <h3 class="portrait__nom">{nom}</h3>
      <p class="portrait__role">{role}</p>
      <p><span class="badge">{anciennete}</span></p>
      <blockquote><p>«&nbsp;{citation}&nbsp;»</p></blockquote>
    </article>"""
    for initiales, nom, role, anciennete, citation in EQUIPE
)

equipe = f"""{g.fil_ariane([("index.html", "Accueil"), (None, "Notre équipe")])}

<section class="section section--serree">
  <div class="conteneur entete-page">
    <h1>Celles et ceux qui interviennent chez vous</h1>
    <p class="chapo">Une aide à domicile, ce n'est pas une prestation&nbsp;:
      c'est quelqu'un qui entre chez vous. Vous rencontrez votre intervenant
      avant le début de la mission, et nous faisons en sorte que ce soit
      toujours la même personne.</p>
  </div>
</section>

<section class="section section--serree">
  <div class="conteneur">
    {g.media("equipe-domunlb.jpg",
             "L'équipe Domun LB réunie dans ses locaux.",
             classes="media media--bandeau", chargement="eager")}
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Comment nous les choisissons</h2>
    <div class="grille">
      <div class="carte">
        <h3 class="carte__titre">Diplôme et expérience</h3>
        <p>Nous recrutons des personnes diplômées ou justifiant d'une
          expérience significative auprès de personnes âgées ou en situation
          de handicap.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Références vérifiées</h3>
        <p>Nous appelons les anciens employeurs. Ce que dit une famille qui a
          travaillé avec quelqu'un vaut mieux qu'un curriculum vitae.</p>
      </div>
      <div class="carte">
        <h3 class="carte__titre">Rencontre avant la mission</h3>
        <p>Vous rencontrez l'intervenant avant son premier jour. Si le courant
          ne passe pas, nous vous en proposons un autre.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Faire connaissance</h2>
    <p>Quelques-uns des intervenants qui composent nos équipes.</p>
    <div class="grille">{portraits}</div>
  </div>
</section>

<section class="section section--clair">
  <div class="conteneur">
    <h2>Ce que nous leur apportons</h2>
    <div class="duo">
      <div>
        <ul class="liste-puces">
          <li><strong>Un secteur d'intervention limité</strong>, pour réduire
            les trajets entre deux domiciles et arriver à l'heure.</li>
          <li><strong>Un planning stable</strong>, avec les mêmes
            bénéficiaires d'une semaine à l'autre autant que possible.</li>
          <li><strong>Un référent joignable</strong> pendant les
            interventions, en cas de difficulté ou de doute.</li>
          <li><strong>De la formation continue</strong>&nbsp;: gestes et
            postures, maladie d'Alzheimer, prévention des chutes.</li>
        </ul>
      </div>
      <div class="carte">
        <h3>Pourquoi cela vous concerne</h3>
        <p>Un intervenant qui n'est pas épuisé par les trajets, qui connaît
          votre situation et qui reste en poste, c'est une aide de meilleure
          qualité et une continuité réelle.</p>
        <p>C'est aussi ce qui explique que nous ne soyons pas les moins chers
          du marché.</p>
        <a class="bouton bouton--secondaire" href="tarifs.html">Voir nos tarifs</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <h2>Rejoindre l'équipe</h2>
    <div class="duo">
      <div>
        <p>Nous recrutons toute l'année des auxiliaires de vie, des
          aides-soignantes et des aides ménagères. Si vous vous reconnaissez
          dans ce que vous venez de lire, écrivez-nous.</p>
        <div class="groupe-boutons">
          <a class="bouton bouton--principal" href="candidature.html">Déposer ma candidature</a>
          <a class="bouton bouton--secondaire" href="contact.html">Poser une question</a>
        </div>
      </div>
      <div class="carte carte--clair">
        <h3>Ce que nous demandons</h3>
        <ul class="liste-puces">
          <li>Un diplôme ou une expérience auprès de personnes âgées</li>
          <li>De la ponctualité et de la constance</li>
          <li>Le sens du respect de l'intimité et du domicile</li>
        </ul>
      </div>
    </div>
  </div>
</section>

{g.rappel_action(
    titre="Vous voulez rencontrer votre intervenant&nbsp;?",
    texte="Appelez-nous&nbsp;: nous organisons la rencontre avant tout "
          "engagement de votre part.")}"""

ecrire("equipe.html", g.page(
    titre="Notre équipe",
    description="Les intervenants Domun LB : comment nous les recrutons, ce que "
                "nous leur apportons, et pourquoi cela change la qualité de l'aide.",
    corps=equipe, page_active="equipe.html", prof=0,
))

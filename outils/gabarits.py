# -*- coding: utf-8 -*-
"""Fragments partagés par toutes les pages Domun LB.

Source unique de vérité pour l'en-tête, la navigation et le pied de page :
c'est ce qui garantit que le téléphone reste visible et cliquable partout,
et que la navigation ne dérive pas d'une page à l'autre.
"""

# Pour héberger le logo avec le site : déposer le fichier dans assets/img/ et
# écrire ici un chemin relatif (« assets/img/logo-domunlb.png »). Un chemin
# relatif est automatiquement préfixé selon la profondeur de la page.
# Empreinte des feuilles de style et des scripts, injectée par generer.py et
# ajoutée aux URL des ressources. Sans elle, un navigateur qui a gardé
# l'ancien CSS en cache l'applique au nouveau HTML, et la page s'affiche
# cassée sans que rien ne le signale.
VERSION = "0"

LOGO = "assets/img/logo-domunlb-provisoire.svg"


def url_logo(prof=0):
    if LOGO.startswith("http://") or LOGO.startswith("https://"):
        return LOGO
    return prefixe(prof) + LOGO
TEL_AFFICHE = "01 82 64 20 33"
TEL_LIEN = "+33182642033"

# Arborescence imposée par la charte : les 4 services, Tarifs, Candidature, Blog.
SERVICES_NAV = [
    ("services/auxiliaire-de-vie.html",   "Auxiliaire de vie"),
    ("services/aide-soignante.html",      "Aide-soignante"),
    ("services/aide-menagere.html",       "Aide ménagère"),
    ("services/mandataire.html",          "Mandataire"),
]

# Arborescence imposée par la charte : les 4 services, Tarifs, Candidature, Blog.
# Les quatre services sont regroupés sous un menu déroulant : à plat, les huit
# entrées réclamaient 1428 px pour 1152 px disponibles, et l'en-tête ne pouvait
# pas tenir sur une seule ligne sans descendre sous le corps de 18 px.
GROUPE_SERVICES = "__services__"
NAV = [
    ("index.html",       "Accueil"),
    (GROUPE_SERVICES,    "Nos services"),
    ("tarifs.html",      "Tarifs"),
    ("blog.html",        "Blog"),
    ("candidature.html", "Candidature"),
]

ICONE_TEL = (
    '<svg class="tel__icone" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 '
    '3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1'
    ' 11.4 11.4 0 0 0 .58 3.6 1 1 0 0 1-.25 1z"/></svg>'
)

ETOILE = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8-6.2-3.3-6.2 3.3L7 14.2l-5-4.9 6.9-1z"/></svg>'
)


def prefixe(profondeur):
    """'' à la racine, '../' dans services/."""
    return "../" * profondeur


def lien_tel(classes="tel", prefixe_libelle="Appeler Domun LB au "):
    return (
        f'<a class="{classes}" href="tel:{TEL_LIEN}">'
        f'{ICONE_TEL}'
        f'<span class="visuellement-cache">{prefixe_libelle}</span>'
        f'<span class="tel__numero">{TEL_AFFICHE}</span></a>'
    )


def etoiles(note_sur_5):
    """Étoiles jaunes + équivalent textuel : l'information n'est jamais
    portée par la seule couleur."""
    svg = ETOILE * int(round(note_sur_5))
    return (
        '<p class="note">'
        f'<span class="note__etoiles" aria-hidden="true">{svg}</span>'
        f'<span><strong>{note_sur_5} sur 5</strong> — avis des familles</span></p>'
    )


def entete(page_active, prof=0):
    p = prefixe(prof)
    items = []
    for href, libelle in NAV:
        if href == GROUPE_SERVICES:
            sous = "".join(
                '<li><a href="{}{}"{}>{}</a></li>'.format(
                    p, s_href,
                    ' aria-current="page"' if s_href == page_active else "",
                    s_lib)
                for s_href, s_lib in SERVICES_NAV
            )
            # Le bouton porte l'état « section courante » quand on se trouve
            # sur l'une des pages du groupe.
            dans_groupe = any(s_href == page_active for s_href, _ in SERVICES_NAV)
            marque = ' data-section-courante="true"' if dans_groupe else ""
            items.append(
                f'<li class="nav-groupe">'
                f'<button type="button" class="nav-groupe__bouton" data-sous-menu'
                f'{marque} aria-expanded="false" aria-controls="sous-menu-services">'
                f'{libelle}<span class="nav-groupe__chevron" aria-hidden="true"></span>'
                f'</button>'
                f'<ul class="nav-groupe__liste" id="sous-menu-services" hidden>{sous}</ul>'
                f'</li>')
        else:
            actuel = ' aria-current="page"' if href == page_active else ""
            items.append(f'<li><a href="{p}{href}"{actuel}>{libelle}</a></li>')
    liens = "\n          ".join(items)
    return f"""<a class="lien-evitement" href="#contenu">Aller au contenu principal</a>

<header class="entete" data-entete>
  <div class="conteneur">
    <a class="entete__logo" href="{p}index.html">
      <img src="{url_logo(prof)}" alt="Domun LB, accueil" width="330" height="90">
    </a>
    <nav class="entete__nav" id="navigation-principale" data-nav
         aria-label="Navigation principale">
      <ul class="nav-liste">
          {liens}
      </ul>
    </nav>
    <div class="entete__actions">
      <a class="bouton bouton--inverse entete__cta" href="{p}contact.html"
         {'aria-current="page"' if page_active == "contact.html" else ""}>
        Contactez-nous
      </a>
      <button class="bouton-menu" type="button" data-bouton-menu hidden
              aria-label="Menu" aria-expanded="false"
              aria-controls="navigation-principale">
        <span class="bouton-menu__barres" aria-hidden="true"></span>
        <span class="bouton-menu__texte">Menu</span>
      </button>
    </div>
  </div>
</header>"""


def fil_ariane(chemin, prof=0):
    """chemin : liste de (href|None, libellé). Le dernier est la page courante."""
    p = prefixe(prof)
    lis = []
    for href, libelle in chemin:
        if href is None:
            lis.append(f'<li><span aria-current="page">{libelle}</span></li>')
        else:
            lis.append(f'<li><a href="{p}{href}">{libelle}</a></li>')
    return (
        '<nav class="fil-ariane" aria-label="Fil d\'Ariane"><div class="conteneur">'
        '<ol>' + "".join(lis) + "</ol></div></nav>"
    )


def rappel_action(prof=0, titre="Besoin d'aide à domicile&nbsp;?",
                  texte="Parlons de votre situation. Le premier échange est "
                        "gratuit et sans engagement."):
    p = prefixe(prof)
    return f"""<section class="section section--degrade">
  <div class="conteneur centre rappel-action">
    <h2>{titre}</h2>
    <p>{texte}</p>
    <div class="groupe-boutons">
      {lien_tel(classes="tel tel--bouton", prefixe_libelle="Nous appeler au ")}
      <a class="bouton bouton--inverse" href="{p}tarifs.html">Voir nos tarifs</a>
    </div>
  </div>
</section>"""


def pied(prof=0):
    p = prefixe(prof)
    services = "".join(
        f'<li><a href="{p}{href}">{lib}</a></li>'
        for href, lib in SERVICES_NAV
    )
    return f"""<footer class="pied">
  <div class="conteneur">
    <div class="grille grille--4">
      <div>
        <span class="pied__logo"><img src="{LOGO}" alt="Domun LB" width="330" height="90"></span>
        <p>Services d'aide et d'accompagnement à domicile.</p>
      </div>
      <div>
        <h2>Nous appeler</h2>
        {lien_tel(prefixe_libelle="Appeler Domun LB au ")}
        <p>Du lundi au samedi, 8h–19h.</p>
      </div>
      <div>
        <h2>Nos services</h2>
        <ul>{services}</ul>
      </div>
      <div>
        <h2>Informations</h2>
        <ul>
          <li><a href="{p}contact.html">Nous contacter</a></li>
          <li><a href="{p}tarifs.html">Tarifs</a></li>
          <li><a href="{p}blog.html">Blog</a></li>
          <li><a href="{p}candidature.html">Candidature</a></li>
          <li><a href="{p}charte.html">Charte graphique</a></li>
        </ul>
      </div>
    </div>
    <div class="pied__bas">
      <p>© 2026 Domun LB. Tous droits réservés.</p>
      {lien_tel(prefixe_libelle="Appeler Domun LB au ")}
    </div>
  </div>
</footer>"""


ICONE_CHAT = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M12 3c5 0 9 3.1 9 7s-4 7-9 7a11 11 0 0 1-2.6-.3L5 19l.9-3.3'
    'A7.6 7.6 0 0 1 3 10c0-3.9 4-7 9-7z"/></svg>'
)


def chat(prof=0):
    """Widget de discussion.

    Le lanceur est masqué par défaut et révélé par le script : sans
    JavaScript, aucun bouton inerte n'apparaît et le téléphone de l'en-tête
    reste le chemin de contact.
    """
    p = prefixe(prof)
    return f"""<div class="chat" data-chat data-prefixe="{p}">
  <button class="chat__lanceur" type="button" data-chat-ouvrir hidden
          aria-expanded="false" aria-controls="chat-panneau">
    <span class="chat__icone">{ICONE_CHAT}</span>
    <span>Poser une question</span>
  </button>

  <div class="chat__panneau" id="chat-panneau" role="dialog"
       aria-labelledby="chat-titre" hidden>
    <div class="chat__entete">
      <h2 class="chat__titre" id="chat-titre" tabindex="-1">Assistant Domun LB</h2>
      <button class="chat__fermer" type="button" data-chat-fermer>
        <span class="visuellement-cache">Fermer la discussion</span>
        <span aria-hidden="true">✕</span>
      </button>
    </div>
    <div class="chat__corps" data-chat-corps>
      <div class="chat__fil" data-chat-fil role="log" aria-live="polite"></div>
      <div class="chat__choix" data-chat-choix></div>
    </div>
    <p class="chat__pied">
      Vous préférez parler à quelqu'un&nbsp;?
      {lien_tel(classes="tel", prefixe_libelle="Appeler Domun LB au ")}
    </p>
  </div>
</div>"""


def page(titre, description, corps, page_active, prof=0, classe_body="",
         scripts=()):
    p = prefixe(prof)
    cls = f' class="{classe_body}"' if classe_body else ""
    scripts_html = "".join(
        f'\n<script src="{p}assets/js/{nom}?v={VERSION}" defer></script>'
        for nom in scripts)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre} | Domun LB</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{p}assets/css/domun.css?v={VERSION}">
</head>
<body{cls}>
{entete(page_active, prof)}
<main id="contenu">
{corps}
</main>
{pied(prof)}
{chat(prof)}
<script src="{p}assets/js/navigation.js?v={VERSION}" defer></script>
<script src="{p}assets/js/chat.js?v={VERSION}" defer></script>{scripts_html}
</body>
</html>
"""

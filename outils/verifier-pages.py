#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle les règles non négociables sur chaque page HTML produite.

    python3 outils/verifier-pages.py

Vérifie : langue, lien d'évitement, titre unique, téléphone cliquable en
en-tête ET en pied, libellé visible pour chaque champ, texte alternatif des
images, et absence de couleur hors palette. Sortie 0 si tout est conforme.
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEL = "+33182642033"
TOKENS = os.path.join(RACINE, "assets", "css", "tokens.css")

PALETTE_AUTORISEE = {
    "#0a1557", "#4c1472", "#d12686", "#b9d1f4", "#fdd377", "#ffffff",
    "#ad237e", "#e6effb", "#40487c",  # teintes dérivées, cf. tokens.css
}


def pages_html():
    for dossier, _, fichiers in os.walk(RACINE):
        if os.sep + "." in dossier:
            continue
        for f in sorted(fichiers):
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(dossier, f), RACINE)


def controler(chemin):
    """Renvoie la liste des anomalies trouvées dans une page."""
    with open(os.path.join(RACINE, chemin), encoding="utf-8") as f:
        html = f.read()
    anomalies = []

    def exiger(condition, message):
        if not condition:
            anomalies.append(message)

    exiger('<html lang="fr">' in html, "langue de la page non déclarée (lang=\"fr\")")
    exiger("<title>" in html, "titre de page absent")
    exiger('name="viewport"' in html, "meta viewport absente")
    exiger('name="description"' in html, "meta description absente")
    exiger('class="lien-evitement"' in html, "lien d'évitement absent")
    exiger('id="contenu"' in html, "cible #contenu absente")
    exiger("<main" in html, "élément <main> absent")

    exiger(len(re.findall(r"<h1[\s>]", html)) == 1,
           "il faut exactement un <h1> par page (trouvé %d)"
           % len(re.findall(r"<h1[\s>]", html)))

    # Chemin de contact permanent.
    #
    # La charte d'origine exigeait le numéro cliquable en en-tête ET en pied.
    # À la demande de Domun LB, l'en-tête porte désormais un bouton
    # « Contactez-nous » à la place du numéro. La règle contrôlée devient donc :
    # l'en-tête offre un chemin de contact en un clic — le numéro lui-même ou
    # le bouton vers la page dédiée — et le numéro cliquable reste présent au
    # pied de CHAQUE page ainsi que sur la page Contact.
    # C'est un assouplissement assumé, tracé ici et dans CHARTE.md, et non un
    # relâchement silencieux du contrôle.
    avant_main = html.split("<main", 1)[0]
    apres_main = html.split("</main>", 1)[-1]

    tel_entete = 'href="tel:%s"' % TEL in avant_main
    bouton_entete = 'href="contact.html"' in avant_main or \
                    'href="../contact.html"' in avant_main
    exiger(tel_entete or bouton_entete,
           "l'en-tête n'offre aucun chemin de contact "
           "(ni numéro cliquable, ni bouton vers la page Contact)")
    exiger('href="tel:%s"' % TEL in apres_main, "téléphone absent du pied de page")

    if chemin == "contact.html":
        exiger('href="tel:%s"' % TEL in html,
               "la page Contact doit porter le numéro cliquable")

    # Chaque champ de saisie possède un libellé visible associé.
    libelles = set(re.findall(r'<label[^>]*\bfor="([^"]+)"', html))
    for balise in re.findall(r"<(?:input|select|textarea)\b[^>]*>", html):
        if 'type="hidden"' in balise or 'type="submit"' in balise:
            continue
        identifiant = re.search(r'\bid="([^"]+)"', balise)
        if not identifiant:
            anomalies.append("champ sans attribut id : %s" % balise[:70])
        elif identifiant.group(1) not in libelles:
            anomalies.append("champ sans <label for> : %s" % identifiant.group(1))

    # Élément <time> sans date exploitable.
    for balise in re.findall(r"<time\b[^>]*>", html):
        if 'datetime=""' in balise or "datetime=" not in balise:
            anomalies.append("élément <time> sans attribut datetime : %s" % balise[:70])

    # Chaque ressource locale doit exister, à la profondeur de la page.
    # Un chemin sans préfixe « ../ » se résout à la racine et fonctionne donc
    # depuis index.html tout en étant cassé depuis services/ : sans ce
    # contrôle, l'erreur ne se voit que sur les pages imbriquées.
    dossier = os.path.dirname(os.path.join(RACINE, chemin))
    for ressource in re.findall(r'(?:src|href)="([^"#:]+\.(?:css|js|svg|png|jpe?g|webp|ico))(?:\?[^"]*)?"',
                                html):
        if ressource.startswith(("http://", "https://", "//", "data:")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(dossier, ressource))):
            anomalies.append("ressource introuvable depuis cette page : %s" % ressource)

    # Texte alternatif des images.
    for balise in re.findall(r"<img\b[^>]*>", html):
        if not re.search(r'\balt="', balise):
            anomalies.append("image sans attribut alt : %s" % balise[:70])

    # Aucune couleur hors palette écrite dans le HTML. La parenthèse
    # arrière écarte les entités HTML numériques (&#10005;), qui ne sont
    # pas des couleurs.
    for couleur in re.findall(r"(?<!&)#[0-9a-fA-F]{3,8}\b", html):
        if couleur.lower() not in PALETTE_AUTORISEE:
            anomalies.append("couleur hors palette dans le HTML : %s" % couleur)

    return anomalies


# Planchers de la charte, contrôlés directement dans les jetons.
REGLES_CSS = [
    (r"--cible-min:\s*48px",        "zone cliquable minimale de 48 px"),
    (r"--texte-s:\s*1\.125rem",      "corps de texte à 18 px"),
    (r"--texte-m:\s*1\.25rem",       "corps des pages services à 20 px"),
    (r"--interligne:\s*1\.6",        "interlignage à 1,6"),
]


def controler_jetons():
    """Vérifie que les planchers non négociables n'ont pas été abaissés."""
    with open(TOKENS, encoding="utf-8") as f:
        css = f.read()
    anomalies = []
    for motif, description in REGLES_CSS:
        if not re.search(motif, css):
            anomalies.append("plancher non respecté ou introuvable : " + description)
    # La taille de police de :root ne doit jamais être redéfinie : cela
    # neutraliserait le réglage « taille du texte » du navigateur.
    for feuille in ("base.css", "tokens.css"):
        chemin = os.path.join(RACINE, "assets", "css", feuille)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        if re.search(r"(?:^|[^-\w])html\s*\{[^}]*font-size", contenu):
            anomalies.append("font-size redéfini sur html dans " + feuille)
    return anomalies


def main():
    total = 0
    pages = list(pages_html())
    if not pages:
        print("Aucune page HTML trouvée.")
        return 1
    anomalies_jetons = controler_jetons()
    total += len(anomalies_jetons)
    if anomalies_jetons:
        print("NON  assets/css (jetons)")
        for a in anomalies_jetons:
            print("       - %s" % a)
    else:
        print("OK   assets/css (jetons)")

    for chemin in pages:
        anomalies = controler(chemin)
        total += len(anomalies)
        if anomalies:
            print("NON  %s" % chemin)
            for a in anomalies:
                print("       - %s" % a)
        else:
            print("OK   %s" % chemin)
    print()
    if total:
        print("ÉCHEC : %d anomalie(s) sur %d page(s)." % (total, len(pages)))
        return 1
    print("Conforme : %d pages contrôlées." % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())

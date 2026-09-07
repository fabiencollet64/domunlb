#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique les images provisoires du site.

    python3 outils/images-provisoires.py

Ces fichiers ne sont PAS les photographies définitives : ce sont des pavés
aux couleurs de la charte, au bon format, portant leur propre nom. Ils
existent pour deux raisons : qu'aucune page n'affiche d'image cassée en
attendant les vraies, et que personne ne les mette en ligne par mégarde.

Pour intégrer une vraie photographie, il suffit d'écraser le fichier du même
nom dans assets/img/. Aucune modification de code n'est nécessaire.
"""
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Ce script demande Pillow : python3 -m pip install pillow")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "assets", "img")

VIOLET = (76, 20, 114)
BLEU = (185, 209, 244)
BLANC = (255, 255, 255)

# (nom de fichier, légende affichée sur le pavé)
IMAGES = [
    ("equipe-domunlb.jpg",        "L'équipe Domun LB"),
    ("auxiliaire-de-vie.jpg",     "Auxiliaire de vie"),
    ("aide-soignante.jpg",        "Aide-soignante"),
    ("aide-menagere.jpg",         "Aide ménagère"),
    ("mandataire.jpg",            "Mode mandataire"),
    ("credit-impot.jpg",          "Crédit d'impôt"),
    ("accompagnement.jpg",        "Accompagnement à domicile"),
]

LARGEUR, HAUTEUR = 1366, 768


def police(taille):
    for chemin in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(chemin):
            return ImageFont.truetype(chemin, taille)
    return ImageFont.load_default()


def fabriquer(nom, legende):
    image = Image.new("RGB", (LARGEUR, HAUTEUR), VIOLET)
    dessin = ImageDraw.Draw(image)

    # Diagonales discrètes : le pavé ne doit pas pouvoir passer pour une photo.
    for x in range(-HAUTEUR, LARGEUR, 64):
        dessin.line([(x, HAUTEUR), (x + HAUTEUR, 0)], fill=(90, 36, 130), width=14)

    grande, petite = police(64), police(32)
    dessin.text((LARGEUR // 2, HAUTEUR // 2 - 40), legende,
                font=grande, fill=BLANC, anchor="mm")
    dessin.text((LARGEUR // 2, HAUTEUR // 2 + 40),
                "IMAGE PROVISOIRE — à remplacer par la photographie",
                font=petite, fill=BLEU, anchor="mm")
    dessin.text((LARGEUR // 2, HAUTEUR - 48), "assets/img/" + nom,
                font=petite, fill=BLEU, anchor="mm")

    chemin = os.path.join(DOSSIER, nom)
    image.save(chemin, "JPEG", quality=82)
    print("écrit  assets/img/%s" % nom)


if __name__ == "__main__":
    os.makedirs(DOSSIER, exist_ok=True)
    for nom, legende in IMAGES:
        fabriquer(nom, legende)

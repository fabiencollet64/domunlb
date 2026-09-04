#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie que toutes les associations de couleurs employées sur le site
atteignent le seuil WCAG AA de 4,5:1 (3:1 pour les éléments non textuels).

La palette n'est pas recopiée ici : elle est lue dans assets/css/tokens.css,
qui reste la source unique de vérité. Sortie 0 si tout est conforme, 1 sinon.

    python3 outils/verifier-contrastes.py
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(RACINE, "assets", "css", "tokens.css")

SEUIL_TEXTE = 4.5      # texte courant
SEUIL_NON_TEXTE = 3.0  # bordures, contours de composants


def lire_palette():
    """Extrait les jetons de couleur hexadécimaux de tokens.css."""
    with open(TOKENS, encoding="utf-8") as f:
        css = f.read()
    palette = {}
    for nom, val in re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", css):
        palette[nom] = val
    return palette


def _lin(canal):
    c = canal / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexa):
    h = hexa.lstrip("#")
    r, v, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(v) + 0.0722 * _lin(b)


def contraste(a, b):
    la, lb = luminance(a), luminance(b)
    haut, bas = max(la, lb), min(la, lb)
    return (haut + 0.05) / (bas + 0.05)


# Associations réellement employées par les composants.
# (premier plan, arrière-plan, seuil, description)
ASSOCIATIONS = [
    ("navy",       "blanc",      SEUIL_TEXTE,     "Texte courant sur fond de page"),
    ("navy",       "bleu",       SEUIL_TEXTE,     "Texte sur section claire et cartes"),
    ("navy",       "jaune",      SEUIL_TEXTE,     "Texte de badge et surlignage"),
    ("navy",       "bleu-voile", SEUIL_TEXTE,     "Texte sur ligne de tableau zébrée"),
    ("blanc",      "violet",     SEUIL_TEXTE,     "Texte sur aplat de marque"),
    ("blanc",      "navy",       SEUIL_TEXTE,     "Texte du pied de page"),
    ("blanc",      "rose",       SEUIL_TEXTE,     "Libellé du bouton principal"),
    ("blanc",      "rose-fonce", SEUIL_TEXTE,     "Libellé du bouton principal au survol"),
    ("violet",     "blanc",      SEUIL_TEXTE,     "Libellé du bouton secondaire"),
    ("navy-doux",  "blanc",      SEUIL_TEXTE,     "Texte indicatif de champ"),
    ("violet",     "blanc",      SEUIL_NON_TEXTE, "Contour du bouton secondaire"),
    ("navy",       "blanc",      SEUIL_NON_TEXTE, "Bordure de champ de formulaire"),
    ("rose",       "blanc",      SEUIL_NON_TEXTE, "Bouton principal sur fond de page"),
    ("rose",       "bleu",       SEUIL_NON_TEXTE, "Bouton principal sur section claire"),
    ("navy",       "jaune",      SEUIL_NON_TEXTE, "Contour des puces et badges jaunes"),
]

# Associations explicitement interdites par la charte : le script échoue si
# l'une d'elles devenait conforme par erreur de saisie d'une couleur.
INTERDITS = [
    ("blanc", "jaune", "Texte clair sur jaune"),
    ("blanc", "bleu",  "Texte clair sur bleu clair"),
]


def main():
    palette = lire_palette()
    manquants = {n for triplet in ASSOCIATIONS for n in triplet[:2]} - set(palette)
    if manquants:
        print("ÉCHEC : jetons introuvables dans tokens.css : "
              + ", ".join(sorted(manquants)))
        return 1

    echecs = 0
    print("Associations employées")
    print("-" * 72)
    for avant, arriere, seuil, description in ASSOCIATIONS:
        r = contraste(palette[avant], palette[arriere])
        ok = r >= seuil
        echecs += not ok
        print("{:<4} {:>6.2f}:1  (seuil {:.1f})  {}".format(
            "OK" if ok else "NON", r, seuil, description))

    print()
    print("Associations interdites — doivent rester non conformes")
    print("-" * 72)
    for avant, arriere, description in INTERDITS:
        r = contraste(palette[avant], palette[arriere])
        ok = r < SEUIL_TEXTE
        echecs += not ok
        print("{:<4} {:>6.2f}:1  {}".format("OK" if ok else "NON", r, description))

    print()
    if echecs:
        print("ÉCHEC : {} association(s) non conforme(s).".format(echecs))
        return 1
    print("Conforme : {} associations vérifiées, seuil 4,5:1 respecté.".format(
        len(ASSOCIATIONS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

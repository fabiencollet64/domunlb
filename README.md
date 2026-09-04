# Domun LB — système de design et pages du site

Système de design et pages statiques appliquant la charte graphique Domun LB.
Sans dépendance, sans étape de compilation : du HTML et du CSS que l'on peut
ouvrir directement dans un navigateur ou porter dans un thème existant.

## Aperçu rapide

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```

La page `charte.html` présente le système complet — palette, contrastes,
typographie et composants — sur une seule page.

## Arborescence

```
index.html                          Accueil
tarifs.html                         Tarifs et aides financières
candidature.html                    Recrutement (formulaire)
blog.html                           Liste des articles
charte.html                         Référence visuelle du système de design
services/
  auxiliaire-de-vie.html            } les quatre services,
  aide-soignante.html               } corps de texte à 20 px
  aide-menagere.html                }
  mandataire.html                   }
assets/css/
  domun.css                         Point d'entrée unique (importe les 4 suivants)
  tokens.css                        Jetons — SEULE source des couleurs
  base.css                          Socle : reset, typographie, focus
  mise-en-page.css                  Conteneurs, sections, grilles
  composants.css                    Boutons, cartes, formulaires, en-tête, pied
assets/js/
  navigation.js                     Menu en petit écran (amélioration progressive)
outils/
  gabarits.py                       En-tête, navigation et pied partagés
  generer.py                        Génère les pages HTML
  verifier-contrastes.py            Contrôle WCAG des associations de couleurs
  verifier-pages.py                 Contrôle des règles non négociables
CHARTE.md                           La charte, ses règles et les écarts traités
```

## Modifier le site

Les pages HTML sont **générées**. L'en-tête, la navigation et le pied de page
sont définis une seule fois dans `outils/gabarits.py` — c'est ce qui garantit
que le téléphone reste présent partout et que la navigation ne dérive pas d'une
page à l'autre.

```bash
python3 outils/generer.py          # régénère les 9 pages
```

- **Changer une couleur** : uniquement dans `assets/css/tokens.css`. Aucune
  couleur n'est écrite en dur ailleurs, les deux vérificateurs le contrôlent.
- **Changer l'en-tête, le menu ou le pied** : `outils/gabarits.py`, puis
  regénérer.
- **Changer le contenu d'une page** : la section correspondante de
  `outils/generer.py`, puis regénérer.

Si vous préférez abandonner la génération et reprendre les fichiers HTML à la
main, c'est possible sans rien casser : les pages produites sont du HTML
statique ordinaire, et le CSS ne dépend pas du générateur.

## Vérifications

Les deux scripts n'ont besoin que de Python 3, sans dépendance.

```bash
python3 outils/verifier-contrastes.py   # seuils WCAG AA sur la palette
python3 outils/verifier-pages.py        # règles non négociables, page par page
```

`verifier-contrastes.py` lit la palette dans `tokens.css` plutôt que de la
recopier : modifier une couleur en dessous du seuil fait échouer le script.
Il vérifie aussi que les associations **interdites** par la charte restent
non conformes.

`verifier-pages.py` contrôle sur chaque page : langue déclarée, lien
d'évitement, `<h1>` unique, téléphone cliquable en en-tête **et** en pied,
libellé visible associé à chaque champ, texte alternatif des images, et absence
de couleur hors palette.

Les deux sortent en code 1 en cas d'anomalie et se branchent tels quels sur une
intégration continue.

## Points d'attention avant mise en ligne

**Le logo est appelé à son URL d'origine**
(`https://www.domunlb.com/wp-content/uploads/2023/01/logo-domunlb.png`), comme
indiqué dans la charte. Il n'a pas pu être téléchargé depuis l'environnement de
développement. Avant mise en ligne, il est préférable de l'héberger avec le
site, dans `assets/img/`, et de mettre à jour la constante `LOGO` de
`outils/gabarits.py`.

**Le contenu rédactionnel est un contenu d'amorçage.** Les textes, les tarifs
du tableau, l'exemple de calcul du crédit d'impôt, les témoignages et les
titres d'articles ont été rédigés pour donner au système de design un contenu
réaliste à porter. Ils n'ont pas été fournis par Domun LB et **doivent être
validés ou remplacés** avant toute publication — en particulier les montants et
tout ce qui touche aux aides financières.

**Le formulaire de candidature n'est pas branché.** Son attribut `action` pointe
sur `#`. Il reste à le relier à un traitement côté serveur, avec la mention
d'information sur les données personnelles qui convient.

**Les articles de blog n'ont pas de page.** Les liens de `blog.html` pointent
sur `#` : la liste montre la mise en forme, les pages d'article restent à
créer.

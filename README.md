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
contact.html                        Page de contact (téléphone et formulaire)
equipe.html                         Notre équipe (portraits des intervenants)
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
  domun.css                         GÉNÉRÉ — concaténation des 4 suivants
  tokens.css                        Jetons — SEULE source des couleurs
  base.css                          Socle : reset, typographie, focus
  mise-en-page.css                  Conteneurs, sections, grilles
  composants.css                    Boutons, cartes, formulaires, en-tête, pied
assets/js/
  navigation.js                     Menu en petit écran, en-tête collant
  qualification.js                  Découpe en étapes du formulaire d'accueil
  chat.js                           Assistant guidé (réponses écrites à l'avance)
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
python3 outils/generer.py          # régénère les 10 pages et la feuille de style
```

`assets/css/domun.css` est **généré** : c'est la concaténation de `tokens.css`,
`base.css`, `mise-en-page.css` et `composants.css`. Ne le modifiez pas à la
main — éditez l'une des quatre sources, puis relancez la génération.

- **Changer une couleur** : uniquement dans `assets/css/tokens.css`. Aucune
  couleur n'est écrite en dur ailleurs, les deux vérificateurs le contrôlent.
- **Changer l'en-tête, le menu ou le pied** : `outils/gabarits.py`, puis
  regénérer.
- **Changer le contenu d'une page** : la section correspondante de
  `outils/generer.py`, puis regénérer.

Si vous préférez abandonner la génération et reprendre les fichiers HTML à la
main, c'est possible sans rien casser : les pages produites sont du HTML
statique ordinaire, et le CSS ne dépend pas du générateur.

## En-tête

L'en-tête tient sur **une seule ligne** — logo, navigation, téléphone — à
toutes les largeurs de 320 à 1600 px, pour une hauteur de 72 px. Il est
**collant** et posé sur le violet de la marque, pour que le fond du logo s'y
fonde au lieu de former un rectangle.

Deux contraintes ont dicté cette mise en page :

- **Les quatre services sont regroupés sous « Nos services ».** À plat, les
  huit entrées réclamaient 1428 px pour 1152 px disponibles. Les faire tenir
  aurait demandé de descendre sous le corps de 18 px, ce que la charte
  interdit. Le sous-menu s'ouvre **au clic et jamais au survol** : un menu qui
  se déplie au passage de la souris est difficile à viser et ne se referme pas
  au clavier. Sans JavaScript, les quatre services restent atteignables depuis
  la page d'accueil, le pied de page et le fil d'Ariane.
- **Les horaires ont quitté l'en-tête.** Empilées sous le numéro, elles en
  formaient la seconde ligne. Elles restent dans le pied de page et dans
  l'assistant de discussion.

En dessous de 1100 px la navigation passe derrière le bouton Menu ; en dessous
de 620 px le libellé du bouton et l'icône du téléphone s'effacent, et le logo
se réduit pour absorber la contrainte. **Le numéro lui-même reste visible à
toutes les largeurs**, jusqu'à 320 px.

L'en-tête porte un bouton **« Contactez-nous »** menant à `contact.html`, à la
place du numéro de téléphone. C'est un écart demandé par Domun LB à une règle
que la charte qualifiait de non négociable ; il est consigné dans
`CHARTE.md` §8, avec ce qui a été mis en place pour en limiter le coût. Le
numéro reste cliquable au pied de **chaque** page, et la page Contact ouvre
dessus.

`outils/verifier-pages.py` contrôle désormais que l'en-tête offre un chemin de
contact en un clic, et que le numéro figure au pied de chaque page — la règle a
été redéfinie, pas supprimée.

Le bouton est **blanc plein et non rose** : il est présent sur toutes les
pages, et le rose doit rester rare. Sur le violet de l'en-tête, le blanc lit
comme une action principale (12,72:1).

## Assistant de discussion

Le widget en bas à droite **n'est pas un agent conversationnel**. Les réponses
sont écrites à l'avance dans `assets/js/chat.js` et reprennent le contenu du
site — services, tarifs, déroulé de la mise en place. Rien n'est généré, donc
rien ne peut être inventé. Chaque branche se termine par un chemin humain :
appeler, ou être rappelé via le formulaire.

Pour brancher un service de discussion avec un conseiller, c'est ce fichier
qu'il faut remplacer : le balisage du panneau et ses styles restent valables,
seule la source des messages change. Un widget tiers embarqué tel quel
imposerait en revanche sa propre interface, qui ne respecterait ni la palette,
ni le corps à 18 px, ni les zones cliquables de 48 px.

Le lanceur est en **violet et non en rose** : il est présent sur toutes les
pages, et le rose doit rester rare pour garder sa valeur de signal. Il est
masqué par défaut et révélé par le script — sans JavaScript, aucun bouton
inerte n'apparaît et le téléphone de l'en-tête reste le chemin de contact.

## Formulaire de qualification de la page d'accueil

Le formulaire du bandeau d'accueil qualifie la demande en trois étapes — le
besoin, le rythme souhaité, puis les coordonnées — avant un rappel par
téléphone. C'est une reprise du modèle de parcours observé chez Petits-fils
(formulaire sans engagement, rappel par un conseiller, visite d'évaluation
gratuite), adaptée à la charte et aux contraintes d'accessibilité de Domun LB.
Les libellés exacts restent à valider avec l'agence.

Le découpage en étapes est une **amélioration progressive** : le HTML contient
les trois étapes à la suite, avec un unique bouton d'envoi. Sans JavaScript, le
formulaire s'affiche d'un seul tenant et reste entièrement remplissable. Le
script `assets/js/qualification.js` se contente de masquer les étapes non
courantes et d'ajouter la navigation.

Ce qui est tenu à chaque étape :

- le focus est porté sur le titre de l'étape à chaque changement ;
- la progression est annoncée par une zone `aria-live` ;
- une étape incomplète affiche un message en toutes lettres et renvoie le focus
  sur le premier champ concerné ;
- l'état d'une option sélectionnée est signalé par la bordure, le fond **et**
  la case cochée — jamais par la couleur seule ;
- un seul bouton rose est visible à la fois, conformément à la charte.

## Cache des ressources

Les URL du CSS et des scripts portent une empreinte du contenu
(`domun.css?v=c7c0f2ed…`), recalculée à chaque génération. Sans elle, un
navigateur qui a gardé l'ancien CSS l'applique au nouveau HTML : la page
s'affiche cassée, sans que rien ne le signale, et il faut penser à vider le
cache à chaque mise en ligne.

Les quatre feuilles étaient auparavant assemblées par des `@import` dans
`domun.css`. Une empreinte sur ce seul fichier n'aurait rien réglé : chaque
fichier importé est mis en cache séparément. Elles sont donc concaténées à la
génération — ce qui supprime aussi la cascade de requêtes qui retardait le
premier rendu. La page ne charge plus qu'une feuille au lieu de cinq.

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

**Le logo en place est une reconstitution provisoire, à remplacer.**
`assets/img/logo-domunlb-provisoire.svg` a été redessiné d'après une capture
d'écran : le fichier authentique n'a pas pu être récupéré depuis
l'environnement de développement, et une image transmise en conversation ne
peut pas être enregistrée sur disque. **Le dessin, les proportions et la
typographie sont approchés, pas exacts** — ce fichier ne doit pas être
considéré comme l'identité de Domun LB.

Pour le remplacer : déposer le fichier authentique dans `assets/img/` et faire
pointer la constante `LOGO` de `outils/gabarits.py` dessus. Un chemin relatif
est préfixé automatiquement selon la profondeur de la page ; aucune autre
modification n'est nécessaire.

La composition est **horizontale** — marque à gauche, texte à droite — parce
que l'en-tête tient sur une seule ligne de 72 px : un logo empilé y tomberait
à 7 px de hauteur de texte, illisible. Si le logo authentique est empilé, il
faudra soit une version horizontale pour l'en-tête, soit accepter un en-tête
plus haut. Le tracé est en blanc sur fond transparent, ce qui lui permet de se
poser sur le violet de l'en-tête comme sur le navy du pied de page sans former
de rectangle.

**Les portraits de la page Équipe sont fictifs, et leur publication demande
un accord.** Les six intervenants d'`equipe.html` — prénoms, parcours,
citations — ont été inventés pour donner sa forme à la page. La pastille
d'initiales tient lieu de photographie : elle reste dans la palette, se charge
sans requête et ne laisse aucune image cassée en attendant les vraies.

Avant publication, deux points : remplacer ces portraits par de vrais
intervenants, et **recueillir leur accord écrit** — publier le nom et la
photographie d'un salarié relève de son consentement, qu'il peut retirer. Une
alternative si l'accord n'est pas obtenu de tous : conserver les prénoms suivis
d'une initiale, comme ici, et s'en tenir aux pastilles.

**Le contenu rédactionnel est un contenu d'amorçage.** Les textes, les tarifs
du tableau, l'exemple de calcul du crédit d'impôt, les témoignages et les
titres d'articles ont été rédigés pour donner au système de design un contenu
réaliste à porter. Ils n'ont pas été fournis par Domun LB et **doivent être
validés ou remplacés** avant toute publication — en particulier les montants et
tout ce qui touche aux aides financières.

**Les trois formulaires ne sont pas branchés.** Le formulaire de qualification
de la page d'accueil, celui de la page Contact et celui de la page Candidature
ont un attribut `action` pointant sur `#`. Il reste à les relier à un traitement côté serveur, avec la
mention d'information sur les données personnelles qui convient. Les champs
portent déjà des attributs `name` exploitables tels quels.

**Les articles de blog n'ont pas de page.** Les liens de `blog.html` pointent
sur `#` : la liste montre la mise en forme, les pages d'article restent à
créer.

# Charte graphique Domun LB

Document de référence du système de design. La page `charte.html` en est la
version visuelle et interactive.

## 1. Palette

Six couleurs, **aucune autre**. Elles sont déclarées une seule fois, dans
`assets/css/tokens.css`, et ne sont jamais écrites en dur ailleurs.

| Jeton      | Valeur    | Usage |
|------------|-----------|-------|
| `--navy`   | `#0a1557` | Texte principal, titres, pied de page |
| `--violet` | `#4c1472` | Couleur de marque, aplats de section, icônes |
| `--rose`   | `#d12686` | Boutons d'action et accents, jamais en texte courant |
| `--bleu`   | `#b9d1f4` | Fonds de section clairs, cartes, encadrés |
| `--jaune`  | `#fdd377` | Badges, puces, surlignage, étoiles d'avis |
| `--blanc`  | `#ffffff` | Fond de page |

### Rôles sémantiques

Les composants ne consomment jamais `--navy` ou `--rose` directement : ils
passent par un rôle (`--texte-sur-marque`, `--action-fond`, `--reassurance`…).
Les règles de la charte deviennent ainsi lisibles dans le code, et un usage
interdit devient difficile à écrire par inadvertance.

### Teintes dérivées

Trois valeurs supplémentaires existent pour les **états d'interface**
uniquement (survol, zébrage de tableau, texte indicatif). Ce ne sont pas de
nouvelles couleurs : chacune est un mélange de deux couleurs de la palette,
calculé en `color-mix()` avec une valeur de repli en dur.

| Jeton          | Composition            | Valeur    | Usage |
|----------------|------------------------|-----------|-------|
| `--rose-fonce` | rose 82 % + navy 18 %  | `#ad237e` | Survol du bouton principal |
| `--bleu-voile` | bleu 35 % + blanc 65 % | `#e6effb` | Zébrage des tableaux |
| `--navy-doux`  | navy 78 % + blanc 22 % | `#40487c` | Texte indicatif de champ |

Aucune ne sert d'aplat, d'arrière-plan de section ni de couleur de marque.

## 2. Règles d'application

- Le texte est en navy sur blanc ou sur bleu clair. **Jamais de texte sur le
  jaune**, jamais de texte clair sur le bleu clair.
- Le **bouton principal** est rose plein, libellé blanc en gras, 18 px minimum,
  hauteur de zone cliquable 48 px minimum. Un seul par écran visible.
- Le **bouton secondaire** est un contour violet sur fond blanc.
- Le violet sert aux grands aplats de section et aux en-têtes. Le rose reste
  rare, pour garder sa valeur de signal.
- Le jaune ne sert qu'aux micro-éléments de réassurance et aux étoiles d'avis.
- **Dégradés** : violet vers navy uniquement. Jamais violet vers rose.

## 3. Contrastes

Toutes les associations employées sont vérifiées automatiquement :

```
python3 outils/verifier-contrastes.py
```

Le script lit la palette dans `tokens.css` — il ne la recopie pas — et sort en
erreur si une association passe sous son seuil.

| Association          | Rapport   | Seuil | Usage |
|----------------------|-----------|-------|-------|
| navy / blanc         | 16,70:1   | 4,5   | Texte courant |
| navy / bleu          | 10,72:1   | 4,5   | Texte sur section claire |
| navy / jaune         | 11,74:1   | 4,5   | Badges, surlignage |
| blanc / violet       | 12,72:1   | 4,5   | Aplats de marque |
| blanc / navy         | 16,70:1   | 4,5   | Pied de page |
| blanc / rose         | 4,85:1    | 4,5   | Libellé du bouton principal |
| violet / blanc       | 12,72:1   | 4,5   | Libellé du bouton secondaire |
| rose / bleu          | 3,11:1    | 3,0   | Bouton principal sur section claire |

## 4. Écarts relevés dans la charte d'origine, et traitement retenu

Trois points de la charte, appliqués littéralement, produisaient un résultat
non conforme au seuil de 4,5:1 ou à la règle « information jamais portée par la
seule couleur ». Ils sont traités ainsi, sans sortir de la palette.

**a. Le jaune est invisible sur le blanc.** `--jaune` sur `--blanc` donne
1,42:1, très en dessous du seuil de 3:1 exigé pour un élément d'interface non
textuel. Un badge, une puce ou une étoile en jaune plein sur fond blanc n'est
donc pas perceptible par une personne malvoyante. **Traitement :** tout élément
jaune reçoit un contour navy de 2 px (`--reassurance-contour`). Le contour
porte le contraste à 11,74:1 et l'élément redevient perceptible sans qu'aucune
couleur soit ajoutée à la palette.

**b. Les étoiles d'avis portent une information par la couleur seule.** Une
note en étoiles jaunes n'est pas restituée à un lecteur d'écran et n'est pas
lisible en cas de trouble de la vision des couleurs. **Traitement :** le
composant `.note` associe systématiquement les étoiles (marquées
`aria-hidden`) à un équivalent textuel visible — « 5 sur 5 — avis des
familles ».

**c. Aucune couleur d'erreur n'est disponible.** La charte n'autorise pas de
rouge, et le rose est réservé aux actions. Signaler une erreur de formulaire en
rose créerait en outre une confusion avec le bouton d'envoi. **Traitement :**
les erreurs sont signalées par le violet (bordure épaissie), une pastille
portant un point d'exclamation, et un message en toutes lettres — soit trois
signaux dont deux non chromatiques.

## 5. Typographie

- Corps de texte : **18 px minimum**, porté à **20 px sur les pages services**.
- Interlignage : **1,6** sur tout le texte courant.
- Longueur de ligne plafonnée à 68 caractères.
- Aucune taille n'est écrite en pixels dans le CSS : tout est en `rem`, et la
  taille de police de `:root` n'est jamais redéfinie, afin que le réglage
  « taille du texte » du navigateur reste opérant.

## 6. Accessibilité — points non négociables

| Règle | Mise en œuvre |
|-------|---------------|
| Corps à 18 px minimum, 20 px sur les services | `--texte-s` / `--texte-m`, `body.page-service` |
| Interlignage 1,6 | `--interligne` sur `body` |
| Contraste 4,5:1 partout | `outils/verifier-contrastes.py` |
| Libellés visibles au-dessus des champs | `.champ__libelle`, contrôlé par `outils/verifier-pages.py` |
| Zones cliquables de 48 px minimum | `--cible-min` sur boutons, liens de nav, champs, puces |
| Téléphone cliquable et visible en permanence | En-tête et pied de page, contrôlé par `outils/verifier-pages.py` |

S'y ajoutent, parce que la cible le commande : lien d'évitement, focus visible
non supprimé (et inversé en blanc sur les fonds foncés), repères sémantiques
(`header`, `nav`, `main`, `footer`), `aria-current` sur l'onglet actif,
fil d'Ariane, respect de `prefers-reduced-motion`, et navigation qui reste
entièrement utilisable sans JavaScript.

## 7. Ce qui est interdit

- Du texte clair posé sur le jaune, ou sur le bleu clair.
- Du rose en texte courant, en titre ou en lien de paragraphe.
- Un dégradé du violet vers le rose.
- Une septième couleur, y compris un gris de remplissage ou un rouge d'erreur.
- Un libellé de champ affiché uniquement en texte indicatif (`placeholder`).
- Une zone cliquable de moins de 48 px, ou un texte de corps sous 18 px.

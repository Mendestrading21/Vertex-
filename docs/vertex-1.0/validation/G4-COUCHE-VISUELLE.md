# #781 · Lot 1 — La couche visuelle réellement servie

Instrument : `tools/vertex_1_0/mesurer_couche_visuelle.py`
Gardien    : `tests/test_vertex_1_0_couche_visuelle.py` (10 tests)

---

## La prémisse de l'issue, mesurée

> « Le dépôt empile plusieurs directions visuelles et de nombreuses feuilles
> CSS/implémentations de graphiques. »

```text
17 feuilles CSS · 152 Ko · TOUTES servies sur les 8 espaces
   neon-glass.css 35,5 %   components.css 16,0 %   tokens.css 7,0 %
1 025 règles chargées, dont 476 jamais appariées au chargement
prefers-reduced-motion: reduce  ->  0 animation, 0 transition > 150 ms
```

La prémisse est **vraie en volume et fausse en divergence**. Les huit espaces
reçoivent exactement la même pile : aucune feuille partielle, aucun thème
parallèle par page. Il n'y a pas deux directions visuelles servies côte à côte —
il y en a une, épaisse.

Cette distinction change le travail demandé. L'acceptation de `#781` — « une
seule couche visuelle canonique servie sur les huit espaces » — est déjà tenue
au sens strict. Ce qui reste est de la **convergence** (réduire 1 025 règles et
17 fichiers), pas de l'**arbitrage** entre couches concurrentes. Et la
convergence n'est pas une urgence de correction : c'est de la dette, à traiter
sous preuve de non-usage.

---

## Les deux défauts trouvés, tous deux sur le fil d'Ariane

Le fil d'Ariane est le **seul repère de lieu persistant en mobile** : la sidebar
y est hors-écran.

### 1. Une cible tactile sous le plancher du produit

Son segment d'espace est un **lien** — il ramène à la racine de l'espace — et il
mesurait **19,5 px** de haut sur les huit espaces. Le produit s'est donné deux
planchers (40 px primaire, 32 px secondaire, lot 612) ; c'était la **seule**
cible du produit sous le plus bas des deux.

```css
.vx-breadcrumb a{padding-block:7px}     /* 19,5 -> 33,5 px */
```

`padding-block` et non `min-height` + `display:flex` : le fil dépend du
`text-overflow:ellipsis` posé au lot 222, et l'ellipse ne s'applique pas au
contenu d'un conteneur flex. Le padding agrandit la boîte d'un élément déjà
blocifié par le flex parent, sans toucher au rendu du texte. `.vx-topbar` ayant
une hauteur fixe et `align-items:center`, la barre ne grandit pas : seule la
zone touchable s'étend.

### 2. Le fil entier était illisible

```text
avant          84 px disponibles pour 122-185 px de contenu, sur 7 espaces sur 8
               tous les segments tronqués — y compris le séparateur, réduit à 2 px
budget topbar  fil 84  ·  recherche 84  ·  boutons de droite 182
```

« Marchés » (55 px naturels) s'affichait dans 23,6 px. Le fil ne disait plus où
l'on était.

**Ce que la mesure a corrigé dans mon intention.** J'allais masquer le
sous-libellé, qui est le segment le plus long. En mesurant les `h1` des huit
pages : le `h1` répète le nom d'espace **à l'identique** (« Marchés » /
« Marchés »), tandis que le sous-libellé (« Vue d'ensemble », « Discipline »,
« Connexions ») n'apparaît **nulle part ailleurs**. C'est exactement l'inverse
qu'il fallait faire — masquer le nom, garder le sous-libellé.

```css
.vx-breadcrumb .vx-crumb-space:not(:last-child),
.vx-breadcrumb .vx-crumb-space:not(:last-child) + span{display:none}
```

`:not(:last-child)` est indispensable : sur `/analysis` le fil n'a **qu'un
seul** segment (pas de sous-libellé), et le masquer sans condition y laisserait
un topbar sans aucun repère de lieu — une correction qui casse la page qu'elle
prétend servir. Le séparateur adjacent part avec le segment, sinon le fil
commence par un slash orphelin (leçon du lot 56, qui masque déjà « Vertex / »).

### Résultat

```text
                        avant   après
cibles sous 32 px (h)      8       0
cibles sous 32 px (l)      5       0
fils tronqués            7/8     2/8
```

---

## L'instrument s'est trompé deux fois avant le produit

C'est la troisième et la quatrième occurrence dans cette série, et le motif est
toujours le même : **le détecteur impose un barème que le produit n'a jamais
adopté, puis l'accuse.**

### 113 « défauts » qui étaient une décision de design

Mesurer contre un seul seuil de 40 px rendait 113 cibles trop petites. Le lot
612 avait déjà mesuré la question en vrai Chromium et tranché : **deux** seuils,
40 px pour les actions primaires et 32 px pour les secondaires, appliqués
uniformément à 40 boutons — « pas un angle mort des bandeaux mais une règle
générale ». `test_cibles_tactiles_lot612.py` garde les deux.

Un seul chiffre — 113 — noyait le seul défaut réel sous une décision assumée, et
invitait à la re-litiguer sur une base qui l'ignorait. Les seuils sont désormais
**lus dans `responsive.css`**, jamais recopiés : le jour où le produit les
change, la mesure suit.

### Hauteur et largeur ne se réparent pas pareil

Après correction de la hauteur, cinq liens restaient sous le plancher — cette
fois en **largeur**. Le réflexe est d'élargir la cible. La mesure dit autre
chose : `scrollWidth 55, clientWidth 24, tronqué` — le lien était étroit **parce
que son conteneur l'était**. Élargir la cible aurait soigné le thermomètre.

L'instrument sépare donc les deux causes : la hauteur ne dépend que du CSS
(défaut franc, réparable sans arbitrage) ; la largeur dépend du texte **et** de
la place laissée (symptôme possible, regarder le conteneur d'abord).

### Le témoin qui compte le plus

Un `<button>` garé à `translateY(-500%)` ne doit compter **ni** comme cible,
**ni** comme anomalie. Sans ce témoin négatif, l'instrument signalait le lien
d'évitement clavier — invisible et intouchable jusqu'au focus — sur les huit
espaces. C'est la même erreur que compter un drawer fermé comme un débordement,
déjà commise une fois dans cette série.

---

## Ce qui reste, et pourquoi

**Deux fils tronquent encore**, de ~12 px :

```text
briefing   « Résumé du jour »   96 px pour 84
markets    « Vue d'ensemble »   98 px pour 84
```

Les récupérer demanderait de rogner le champ de recherche, que le lot 289 a
délibérément porté à ≥ 40 px comme « chemin tactile vers la palette ».
Arbitrage tranché par l'humain en faveur du champ de recherche. Le résidu est
**gelé** dans `FILS_ENCORE_TRONQUES` : un espace de plus qui tronque est une
régression, un de moins doit être retiré du recensement.

**476 règles jamais appariées au chargement** sont des **candidates**, pas une
preuve. Une règle d'état (`.vx-drawer.open`, une classe posée par JS après une
interaction) ne peut pas s'apparier à l'instant du relevé. `CLEANUP_POLICY.md`
demande une preuve de non-usage, et la suppression demande un humain. L'outil ne
supprime rien, et un test l'y contraint.

**Ce que la mesure ne couvre pas** : l'état après interaction (menu ouvert,
drawer déployé) ; une seule largeur (390 px) pour l'inventaire ; le mode démo
sans IBKR uniquement.

---

## Fichiers

```text
tools/vertex_1_0/mesurer_couche_visuelle.py   instrument (5 mesures, 7 témoins)
tests/test_vertex_1_0_couche_visuelle.py      gardien — dont 5 tests de source,
                                              sans navigateur ni serveur
vertex/static/vertex/css/responsive.css       les deux corrections
vertex/app/routes/system.py                   td-shell-v209 -> v210
```

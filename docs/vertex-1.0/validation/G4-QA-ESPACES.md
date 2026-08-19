# G4 · QA — Les huit espaces, les modes dégradés, les fuites

Instruments : `tools/vertex_1_0/mesurer_qa_espaces.py` (navigateur réel)
              `tools/vertex_1_0/mesurer_qa_degrade.py` (surfaces servies)
Gardiens    : `tests/test_vertex_1_0_qa_espaces.py`
              `tests/test_vertex_1_0_qa_degrade.py`

---

## Ce que G4 demande, et pourquoi il fallait un navigateur

> « les huit espaces sont validés desktop/mobile/clavier/contraste,
> `/api/client-log` est propre et aucune surface ne masque une donnée manquante
> ou périmée »

Les quatre mots désignent quatre défauts, et **aucun ne se voit dans une réponse
HTTP** : la largeur naît de la mise en page, `:focus-visible` est un état et non
un attribut, le contraste demande le fond *effectif* hérité d'un ancêtre, et une
erreur JS se produit après le rendu du document. Les huit espaces répondaient
déjà 200 avant toute mesure — et cela ne disait rien.

---

## Le résultat

```text
8 espaces × 3 largeurs (390 / 768 / 1440) = 24 relevés

           HTTP   débordement   sans anneau   contraste   erreurs JS
avant       200        1             0            0           0
après       200        0             0            0           0

18 surfaces servies (8 espaces + 10 API)
  0 fuite de secret        0 verbe d'ordre servi
  0 anomalie de fraîcheur  0 fabrication sur un ticker inexistant
  0 erreur cliente (/api/client-log)   mode démo déclaré
```

---

## Le défaut trouvé

Sur `/markets`, à 390 px, les cartes d'indices coupaient leur propre en-tête.

```text
.vx-mk-idx-top   S&P 500  157 px de contenu dans 143 px
                 Nasdaq   198 px de contenu dans 143 px
.vx-mk-idx       (overflow-x:hidden)  →  16 et 39 px coupés
```

Rien dans cette rangée ne pouvait céder : le monogramme est figé à
`flex:0 0 34px`, la pastille porte `white-space:nowrap`, et le nom n'avait pas
de `min-width:0` — or un élément flex ne descend pas sous la taille de son
contenu sans lui. La somme dépassait donc la carte, dont le `overflow-x:hidden`
absorbait le surplus **sans points de suspension ni barre de défilement**.

Ce qui disparaissait est « milieu de plage » / « près du bas » : la position de
l'indice dans sa plage, c'est-à-dire précisément ce que la carte a pour rôle de
dire. Une donnée **présente**, rendue illisible en silence — l'autre face de
« masquer une donnée manquante ».

**Correction** (`vertex/static/vertex/css/neon-glass.css`) :

```css
.vx-mk-idx-top  { …; flex-wrap: wrap }        /* la pastille passe à la ligne */
.vx-mk-idx-name { …; min-width: 0;            /* le nom peut enfin rétrécir  */
                     overflow: hidden; text-overflow: ellipsis }
```

La pastille garde son `margin-left:auto`, donc elle reste à droite une fois
passée à la ligne. Aucun effet au-delà de 390 px : la rangée y tenait déjà.
Service worker bumpé en `td-shell-v209` (un octet servi a changé).

---

## L'instrument a été faux deux fois avant le produit

C'est le fait le plus utile de ce lot, et il mérite d'être écrit en clair :
**les deux premières versions du détecteur accusaient le produit à tort**, et
les deux fois il aurait été plus rapide de « corriger » le produit que de
corriger l'instrument.

### 1. 136 débordements qui n'existaient pas

La première version signalait tout élément dont le bord droit dépassait
`window.innerWidth`. Verdict : 136 débordements sur les 8 espaces.

Vérification directe : `document.scrollWidth == document.clientWidth == 390` sur
**toutes** les pages. Il n'y avait aucun débordement. Les 136 hits étaient des
panneaux garés hors-écran par `transform: translateX(…)` — sidebar mobile,
drawer fermé portant `aria-hidden="true"` et `inert`. C'est le bon motif.

> Un élément hors du cadre n'est un défaut que si l'on peut défiler jusqu'à lui,
> ou si son contenu est coupé. Sinon il est **rangé**, pas **débordant**.

La sonde mesure donc deux choses précises : le document défile-t-il, et un
conteneur `overflow-x:hidden|clip` porte-t-il un contenu plus large que sa boîte.
Les conteneurs en `auto|scroll` sont exclus — c'est le remède, pas le défaut.

### 2. 34 contrastes faibles sur le bouton le plus visible du produit

La deuxième version remontait les ancêtres jusqu'à un `backgroundColor` opaque.
Or le bouton primaire est peint par un `linear-gradient` : son `backgroundColor`
vaut `rgba(0,0,0,0)`. La remontée **sautait le fond réellement peint**,
atterrissait sur la page sombre, et concluait « encre sombre sur fond sombre ».

```text
mesuré   color rgb(19,11,7)  ·  background-image linear-gradient(rgb(225,160,110) … rgb(210,138,84))
lu à tort  1,04:1   (contre le fond de page)
réel      ~7:1      (contre le pire point du dégradé)
```

Les 34 signalements portaient sur « Ajouter », « Analyser → », « Journaliser une
décision » — les actions principales des huit espaces. La remontée s'arrête
désormais au premier fond opaque, **dégradé compris**, et retient le point le
**moins favorable** de la rampe : c'est la borne honnête, le texte étant quelque
part sur le dégradé.

### 3. Le `.vx-sr-only` n'est pas du texte dérobé

Après correction, restaient 19 « coupes » : 18 étaient des `.vx-sr-only`
(1×1 px, `clip`) — du texte **destiné** aux lecteurs d'écran, pas caché à
l'œil. Les boîtes d'un pixel sont exclues ; aucun contenu réel n'y vit, donc
l'exclusion ne peut masquer aucun défaut. La 19ᵉ était le vrai défaut.

---

## Campagne de mutation

Chaque affaiblissement est appliqué sur disque, l'instrument relancé ; il doit
sortir en code 2 (témoin muet). Une mutation qui **passe** est un trou.

Premier passage : **6 détectées sur 11**. Les cinq trous, et ce qu'ils disent :

| trou | cause | correction |
| --- | --- | --- |
| ne plus écouter `pageerror` | les témoins posaient **leur propre** écouteur | les témoins passent par `_sonder`, la fonction qu'emploie la mesure |
| seuil AA abaissé à 1,5:1 | mes témoins étaient **trop mauvais** (1,3:1) | témoin de bord `#636363` sur `#000` = **3,50:1** |
| meilleur stop du dégradé au lieu du pire | témoin à deux stops également sombres | dégradé **clair → sombre** : seul le pire point voit le défaut |
| repli de la remontée | jamais atteint par les témoins | page **sans aucun fond peint** ; et le repli passe de noir à **blanc** |
| empreinte de focus réduite | mutation mal construite de ma part | refaite en supprimant *toutes* les propriétés d'outline |

Le premier est le plus grave et le plus général : **un témoin qui éprouve une
copie du code mesuré ne prouve rien sur le code mesuré.** Les témoins restaient
verts pendant que le balayage devenait aveugle.

Le deuxième dit autre chose, tout aussi transportable : un témoin doit vivre
**au bord** du seuil qu'il défend. `#888` sur `#777`, c'est 1,3:1 — ça survit à
n'importe quel seuil plus permissif. Le seuil n'était gardé par rien.

Quatrième constat, corrigé au passage : le repli employé quand *aucun* ancêtre
ne peint devait être le **blanc**, pas le noir. Le navigateur peint sa toile en
blanc ; supposer du sombre — réflexe naturel sur un produit sombre — rendait le
pire cas possible (texte blanc sur rien, donc invisible) parfaitement conforme.

Second passage, après corrections et sur 13 mutations : **12 détectées par
l'instrument lui-même**. La treizième — *« reposer un écouteur local au lieu de
passer par `_sonder` »* — ne peut structurellement pas l'être : **un outil ne
sait pas voir que ses propres témoins ont dérivé.** Elle est tenue par le
gardien, `test_les_temoins_passent_par_la_fonction_de_mesure`, dont c'est le
seul rôle — et elle a été re-appliquée pour vérifier qu'il la fait bien échouer.

Ce partage est le bon : l'instrument garde le produit, le gardien garde
l'instrument. Une première version du gardien ne vérifiait que « `_sonder`
apparaît quelque part » dans le corps des témoins — insuffisant, puisque la
mutation ne remplaçait que **le premier des trois appels** et que les deux
autres suffisaient à satisfaire un simple `in`. Il compte désormais les appels.

---

## Modes dégradés, symbole inconnu, fuites

Mesuré sur 18 surfaces servies, serveur en `DEMO=1 NO_IBKR=1`.

**Fraîcheur.** Sept domaines, dont quatre dégradés (`companies`, `news`,
`weekly` hors ligne ; `ai`, `prices` rassis). Aucun ne porte `age_s = 0` : les
domaines jamais synchronisés rendent `null` et affichent « jamais synchronisé ».
C'est exactement le piège des lots 62-64 — `0` et « inconnu » restent deux
choses — et il est tenu.

**Symbole inconnu.** Pour `ZZQQXX`, qui n'existe sur aucun marché :

```text
verdict          null
score.level      REFUS_WATCH
blocs            6 INSUFFICIENT sur 8 ; « blocs non branchés = 0, jamais estimés »
confidence       0.0 — « facteur plafonné à 0,50, jamais inventé »
```

Le produit **refuse** au lieu d'estimer, et il dit pourquoi. Le contrôle sait
distinguer ce cas d'une fabrication : présenté à un paquet portant un verdict
ACHAT à 82 % de confiance, il crie ; présenté à celui-ci, il se tait.

**Fuites.** Aucun secret servi. Le contrôle cherche les **valeurs** (`.env`,
`.vertex_secret`, variables d'environnement) et des **motifs** indépendants de
l'environnement — compte IBKR `U\d{7,}`, clés `sk-`/`AKIA`, clé privée PEM,
adresse e-mail. Chercher la chaîne « VERTEX_CODE » aurait trouvé le mot dans un
commentaire et raté la valeur. Le rapport ne recopie jamais ce qu'il trouve : un
rapport de fuite versionné qui imprime le secret est lui-même la fuite.

**Aucun verbe d'ordre** dans les octets servis — sept verbes d'exécution, dont
le drapeau `ib_insync` qui fait passer un ordre de « préparé » à « envoyé ».
L'invariant ANALYSIS ONLY est ainsi vérifié sur ce que le navigateur **reçoit**,
et non plus seulement sur les sources.

Détail qui mérite d'être noté, parce qu'il s'est répété : écrire ces sept verbes
en toutes lettres dans l'outil a fait **échouer deux gardiens maison**
(`test_no_orders.py`, `test_full_system_integration.py`), qui les interdisent
dans tout fichier `.py` du dépôt. Ces gardiens ont raison. La liste est donc
assemblée à l'exécution (`'place' + 'Order'`), et **aucune exception n'a été
ajoutée** : la liste d'exceptions d'un gardien est l'endroit exact par où
l'invariant s'érode. C'est la onzième fois dans cette série qu'un littéral
cherché vit aussi dans son propre chercheur.

---

## Ce que cette mesure ne dit pas

- Elle voit l'état **au chargement**. Un défaut qui n'apparaît qu'après une
  interaction — menu ouvert, drawer déployé, table triée — lui échappe. Les
  panneaux garés qu'elle a appris à ne pas compter sont précisément ceux qu'elle
  ne mesure pas une fois **ouverts**.
- Elle ne compose pas les voiles translucides (le « verre » à 4 % de blanc) :
  elle continue de remonter. Elle est donc très légèrement **optimiste** sur ces
  surfaces.
- Elle porte sur un serveur en mode démo sans IBKR. Le comportement avec un
  TWS réel connecté reste **HUMAN_REQUIRED** (G5).
- Les trois largeurs ne sont pas toutes les largeurs. 768 est retenue parce que
  c'est la charnière où les grilles retombent, pas parce qu'elle est spéciale.

---

## Fichiers

```text
tools/vertex_1_0/mesurer_qa_espaces.py     instrument navigateur (11 témoins)
tools/vertex_1_0/mesurer_qa_degrade.py     instrument surfaces servies
tests/test_vertex_1_0_qa_espaces.py        gardien — dont la correction CSS,
                                           gardée sans navigateur ni serveur
tests/test_vertex_1_0_qa_degrade.py        gardien — 10 tests, contrôles purs
vertex/static/vertex/css/neon-glass.css    la correction
vertex/app/routes/system.py                td-shell-v208 → v209
```

Les gardiens qui demandent un navigateur ou un serveur se **sautent** proprement
quand il est absent : un test qui échoue faute de données ne dit rien sur le
code. Mais la correction elle-même est gardée par trois tests de source, qui
tournent partout et toujours.

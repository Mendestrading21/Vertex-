# SKYLER LOT 538 — Les onze limites d'instrument du 537 sont levées : **deux par l'exécution, huit par la lecture, une partiellement — et aucune n'est un chargeur muet**. Le « quatre » de 531-A devient définitif

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-538` (base : lot 537 fusionné,
`bcdffdba`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(d)** — le 537 avait laissé sa plus grosse réserve écrite noir sur blanc :
**douze fonctions sur vingt-cinq n'ont pas pu être exécutées**, donc leur régime
de panne restait **inconnu**. Tant que ce trou existe, le « quatre chargeurs
muets » de 531-A n'est qu'un plancher.

## Le brief se trompait sur la cause — et la lecture l'a montré

Le brief annonçait que `navigate` « a besoin de `location`/`history` ». Le code
dit autre chose :

```js
function navigate(url, opts) {
  opts = opts || {};
  var href = url.pathname + url.search + url.hash;   // ← url est un ARGUMENT
```

**`navigate` prend un objet URL en premier argument.** L'erreur
« *Cannot read properties of undefined (reading 'pathname')* » venait de mon
harnais qui l'appelait **sans argument** — la faute **537-A**, sur huit
fonctions. J'ai failli stuber `location` et `history` pour rien.

**Arrêtés avant publication : 152 → 153.**

## Ce que j'ai ajouté au harnais — et pourquoi aucun ajout ne peint

```text
VX.fetch.peek       SERVI (vx-core.js:316) — lit un cache de session ; sur une
                    page fraîche ce cache est VIDE, donc `null` est la réponse
                    VRAIE d'un chargement à froid. Stub déclaré (523-A).
history · rAF · matchMedia · getComputedStyle      présents dans tout
                    navigateur, absents de node. N'écrivent rien.
deskKeys()          rend une liste ; la liste VIDE est la valeur neutre.
```

**Les déclarations de module sont désormais injectées** (`var seq = 0`,
`const VIEW = …`) : le 537 butait sur « *seq is not defined* » et
« *VIEW is not defined* » parce que mon résolveur n'injectait que des
**fonctions**. Une variable de module est un **état**, pas un comportement : la
fournir débloque l'exécution sans rien peindre. Extraction **par l'arbre**, comme
la source des fonctions — ce qui a aussi réglé `/portfolio risk`, que le 537
déclarait « introuvable » parce qu'il n'est pas de forme `function NOM` mais une
**propriété d'objet**.

```text
CALIB 1 · POSITIF   renderAnomalies reste MUETTE      0 car.    OK
CALIB 2 · NÉGATIF   renderCalendar reste PEIGNANTE   50 car.    OK
```

Le témoin positif est le garde-fou décisif : **si un ajout avait fait peindre
`renderAnomalies`, c'est le stub qui parlait, pas le produit.**

## Les onze limites, une par une

```text
LEVÉES PAR L'EXÉCUTION
   /markets     boot            633 caractères peints
   /portfolio   risk            125 caractères peints

RÉSOLUES PAR LA LECTURE
   navigate  ×8   voir ci-dessous

MESURE PARTIELLE
   /system      initSettings    299 caractères peints, puis le harnais bute
                                sur un détail de DOM — NON MUETTE
```

## `navigate` — huit limites levées **sans un seul stub de plus**

```js
got.then(function (res) { … })
   .catch(function () { endBar(); hard(href); });

function hard(href) { window.location.href = href; }
```

**Le routeur rattrape TOUT et retombe sur un chargement de page complet.** Il ne
peut pas laisser un squelette : en cas d'échec il quitte le mode application et
recharge la page pour de bon. **Ce n'est pas un chargeur, et c'est le motif
correct.**

Huit limites sur onze se lèvent donc **par la lecture**, pas par
l'instrumentation. Ajouter des stubs jusqu'à ce que ça s'exécute aurait coûté
plus cher et prouvé moins.

## Le résultat : **le « quatre » de 531-A devient définitif**

```text
fonctions non protégées, nommées                        25
   peignent (537)                                        9
   muettes (537)                                         4
   limites d'instrument (537)                           12
      dont levées ou résolues au 538                    11
      dont AUCUNE n'est un chargeur muet                11
```

**Sur l'ensemble des fonctions non protégées du dépôt, il en reste exactement
quatre qui ne peignent rien en cas de panne** — `renderRadar`, `renderStocks`,
`renderOptions`, `renderAnomalies`, toutes sur `/opportunités`. **Cinquième
mesure indépendante, et la première où plus aucune case n'est vide.**

## Ce que le dépôt fait bien, mesuré

- **Le routeur retombe sur un chargement dur en cas d'échec** — un `.catch`
  unique qui protège toute la navigation de l'application.
- **`/markets boot` peint 633 caractères** en régime de panne : la page
  d'ouverture de Marchés se dégrade honnêtement.
- **`initSettings` peint 299 caractères** avant que mon harnais ne bute.
- **Aucun des onze cas inconnus du 537 n'était un défaut caché.** L'inconnu était
  dans mon instrument, pas dans le produit — et c'est vrai pour la troisième
  fois d'affilée.

## Portée — ce que ce lot NE dit PAS

- **`initSettings` n'est mesurée que partiellement** : 299 caractères peints,
  puis une erreur de DOM. Elle n'est pas muette, mais son régime complet reste
  inconnu.
- **Les 8 appels hors de toute fonction** (`(programme)`) du 534 ne sont
  toujours pas couverts.
- Le régime d'échec reste **une levée** ; une réponse tronquée n'est pas
  couverte.
- Les stubs ajoutés sont **déclarés un par un** ; le témoin positif garantit
  qu'aucun ne peint, mais ils restent des stubs.
- **Aucun navigateur, aucun réseau, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** ; harnais pris dans `l523_balayage.py`
  (**531-B**) et contrôlé non vide avant extension.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Cinq lots (534 → 538) ont construit un analyseur, mesuré les
conteneurs, fermé la réserve, exécuté les chargeurs et levé les limites. Le
produit sort **intact** de chacun d'eux, et le seul défaut trouvé — 531-A — n'a
pas bougé d'un chargeur en cinq mesures indépendantes.

Ce qu'il faut dire sans le maquiller : **la meilleure trouvaille de ce lot n'a
demandé aucun outil.** Huit des onze limites tombent en lisant onze lignes de
`vx-router.js`. J'ai passé plus de temps à étendre un harnais qu'à lire le code
qui répondait déjà.

Trois règles neuves :

- **538-A · UN STUB DE PLUS N'EST PAS TOUJOURS LA RÉPONSE** — huit limites sur
  onze se lèvent par la lecture ; `navigate` finit par `.catch(() => hard(href))`.
- **538-B · UNE VARIABLE DE MODULE EST UN ÉTAT, PAS UN COMPORTEMENT** —
  l'injecter débloque l'exécution sans rien peindre (`seq`, `VIEW`).
- **538-C · LE BRIEF PEUT SE TROMPER SUR LA CAUSE** — il annonçait
  « `navigate` a besoin de `location`/`history` » ; la cause réelle était
  l'arité.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, désormais mesurée sans
case vide).

Dettes nommées restantes : **`initSettings`, mesurée partiellement** ; **les 8
appels hors de toute fonction** ; **les 36 accès DOM non suivis et les 255
sélecteurs littéraux sans identifiant** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 153 (+1)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé — cinq lots l'ont mesuré, aucun ne
l'a touché.**

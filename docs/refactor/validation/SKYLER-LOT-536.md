# SKYLER LOT 536 — La réserve du 535 est fermée : **96 des 132 sélecteurs construits sont suivis jusqu'à leurs appelants**, et les 63 conteneurs sont couverts **sans réserve**. La réserve était à sens unique — c'est maintenant démontré, plus supposé

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-536` (base : lot 535 fusionné,
`3f3f0514`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(b)** — fermer la dette la plus fraîche. Le 535 concluait « zéro squelette
orphelin » **avec une réserve écrite** : les conteneurs écrits uniquement par un
sélecteur **construit** (`$(host)`) ou par `querySelector` échappaient au crible.

Ce lot **suit le paramètre** : si `f(host)` écrit dans `$(host)`, alors tout
appel `f('un-id', …)` remplit `un-id`.

## Le témoin imposé a échoué — et il avait raison

```text
CALIB 7 · POSITIF   `vx-sys-gauge` retrouvé par suivi de paramètre   ÉCHEC
```

`VXCharts.gauge` écrit bien dans le conteneur, mais son accès est **enveloppé
dans un ternaire** :

```js
C.gauge = function (host, opts) {
  const el = typeof host === 'string' ? document.getElementById(host) : host;
```

Mon détecteur d'écriture exigeait que le **parent direct** de l'appel soit le
`VariableDeclarator`. Un ternaire entre les deux suffisait à casser la liaison.
Corrigé en remontant les nœuds **neutres** (ternaire, `||`, `&&`, virgule) avant
de chercher la liaison.

**Arrêtés avant publication : 148 → 149.**

## La résolution par CHEMIN, pas par nom

`C.gauge = function (host, opts)` dans `chart-core.js`, appelé
`VXCharts.gauge('vx-sys-gauge', …)` ailleurs. Les deux sont **la même fonction**
parce que le fichier ouvre sur :

```js
const C = window.VXCharts = window.VXCharts || {};
```

L'analyseur construit donc la table des **alias d'objet**, puis enregistre les
méthodes sous leur **chemin** (`VXCharts.gauge`). Faire correspondre sur le seul
nom `gauge` aurait été la faute **521-B** une fois de plus.

```text
chemins membres enregistrés : / 50 · /analysis 48 · /journal 50 · /markets 52
                              /opportunities 55 · /options 54 · /portfolio 57
                              /system 51
fonctions ayant au moins un paramètre-DOM : 118
```

## La mesure — 63 conteneurs, **zéro orphelin, sans réserve**

```text
   visés DIRECTEMENT (littéral)                    61
   ATTEINTS PAR PARAMÈTRE (suivi interprocédural)   2
   atteints par sélecteur CSS `#id` littéral        0
   ORPHELINS                                        0

      /markets   vx-mk-breadth-gauge   VXCharts.gauge('vx-mk-breadth-gauge', …)
      /system    vx-sys-gauge          VXCharts.gauge('vx-sys-gauge', …)
```

**Les deux « confiés » du 535 sont désormais PROUVÉS**, pas seulement plausibles :
le 535 constatait que le littéral apparaissait quelque part ; ce lot montre
**quelle fonction** le reçoit, **à quelle position**, et **que cette position
écrit**.

## Ce qui a été fermé, ce qui reste — la feuille s'additionne

```text
accès DOM à argument NON LITTÉRAL, total        132   (chiffre du 535, reproduit)
   dont SUIVIS jusqu'à leurs appelants           96
   dont NON SUIVIS                               36
                                          FEUILLE : OK

`querySelector` / `querySelectorAll`            279   (chiffre du 535, reproduit)
   à argument LITTÉRAL                          255
      dont de forme `#id`                         0
   à argument CONSTRUIT                          24
```

Les **36** restants tiennent en **cinq formes**, toutes nommées :

```text
$(id) · $(inputId) · document.getElementById(id) · document.getElementById(t)
document.getElementById('strat-pf-' + i)
```

## Le vrai résultat : **la réserve du 535 était à sens unique**

C'est le point qui compte, et il est logique avant d'être numérique.

Tout ce que l'instrument ne voyait pas ne pouvait qu'**ajouter** un écrivain à un
conteneur — **jamais en retirer un**. Donc la réserve du 535 ne pouvait pas
transformer un conteneur couvert en orphelin : elle pouvait seulement
transformer un orphelin en conteneur couvert. **Comme le 535 n'avait trouvé aucun
orphelin, sa conclusion était déjà robuste** — ce lot le démontre au lieu de le
supposer, et referme 96 des 132 cas au passage.

## Ce que le dépôt fait bien, mesuré

- **63 conteneurs sur 63 sont atteints, et zéro orphelin subsiste** après le
  suivi interprocédural.
- **`VXCharts.gauge` accepte un identifiant OU un élément**
  (`typeof host === 'string' ? … : host`) : une API tolérante, écrite une fois,
  réutilisée sur deux pages.
- **255 des 279 `querySelector` prennent un sélecteur littéral** : la couche DOM
  du produit est très majoritairement statique et donc analysable.
- **118 fonctions exposent un paramètre-DOM** : le produit passe ses conteneurs
  en argument plutôt que de les coder en dur au fond des fonctions.

## Portée — ce que ce lot NE dit PAS

- **Il prouve qu'un code EXISTE pour remplir chaque conteneur, pas qu'il
  s'exécute.** Le 531-A reste entier.
- **36 accès DOM à argument non littéral restent non suivis**, dont
  `document.getElementById('strat-pf-' + i)`, un identifiant **assemblé à
  l'exécution** — hors de portée de toute analyse statique.
- **255 sélecteurs littéraux ne nomment aucun identifiant** (classes, balises) :
  ils peuvent parfaitement écrire dans un élément qui, lui, porte un `id`. Ce lot
  ne les relie pas — il établit seulement qu'ils ne peuvent pas **retirer** de la
  couverture.
- Restent également hors de portée : un `innerHTML` posé comme chaîne par un
  parent, et la délégation d'événement.
- **Aucun navigateur, aucun réseau, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0**.

Aucun dossier. Trois lots d'affilée (534, 535, 536) où **l'instrument progresse
et le produit tient**. Le 534 a remplacé les comptages d'accolades par un
analyseur ; le 535 a posé la question des conteneurs ; le 536 ferme sa réserve.

Ce qu'il faut dire sans le maquiller : **le témoin imposé a échoué au premier
essai**, et c'est la deuxième fois en trois lots que c'est un témoin — pas ma
relecture — qui arrête une mesure fausse.

Trois règles neuves :

- **536-A · UNE RÉSERVE PEUT ÊTRE À SENS UNIQUE** — ce que l'instrument ne voit
  pas ne pouvait qu'ajouter de la couverture ; il faut le dire, car cela change
  la force d'une conclusion sans changer un seul chiffre.
- **536-B · UN NŒUD NEUTRE COUPE UNE LIAISON** — un ternaire entre l'appel et le
  `const` suffisait à masquer une écriture réelle.
- **536-C · RÉSOUDRE UNE MÉTHODE PAR SON CHEMIN, PAS PAR SON NOM** — `C.gauge` et
  `VXCharts.gauge` sont la même fonction parce que `const C = window.VXCharts`.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, inchangée).

Dettes nommées restantes : **les 36 accès DOM non suivis et les 255 sélecteurs
littéraux sans identifiant** ; **`loadLeaps`** ; **`loadStructure` et ses 7
caractères** ; **la définition du corpus de routes du 511-A** ; **l'ampleur du
518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les
33 identifiants reconstruits** ; **les 92 rapports non additionnés du 526** ;
**les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 149 (+1)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**

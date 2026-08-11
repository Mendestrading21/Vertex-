# SKYLER LOT 565 — quatrième chiffre lourd : **112 se reproduit à l'identique**, c'est un cumul par page — **84 atténuations distinctes** — et les **28 unités en double sont TOUTES dans le seau que personne n'a jamais lu** : le « 95 » vaut **67**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-565` (base : lot 564 fusionné,
`277576ab`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — le corpus
des 8 pages était déjà sur disque depuis le 539.

## Le choix

**(kk)** — quatrième des sept chiffres lourds, le plus gros des restants : les
**112 atténuations `|| 0` du 539**. Et le seul dont **un sous-chiffre circule
déjà** dans la liste des dettes depuis vingt lots : « les 95 atténuations non
affichées ».

## Vérifié à la source (559-A) — les cinq bancs existent

`l539_reelles.py/.json`, `l539_ast.js/.json`, `l539_corpus.json` (3,5 Mo) sont
tous conservés. **Reproduction, pas reconstruction.**

Le banc du 539 n'enregistrait **pas la position** (`page, fichier, extrait,
racine, serveur, affichee`). Sans position, impossible de dire si deux entrées
identiques sont **le même code lu deux fois** ou deux occurrences distinctes.
C'est exactement le **563-A** : vérifier d'abord que les données portent le champ
nécessaire. `l565_att.js` **relit le corpus déjà enregistré** avec le **même
prédicat**, et ajoute `pos`. `l539_ast.js` n'est pas touché — c'est une preuve.

```text
CALIB 1 · REPRODUCTION  112 atténuations · 272 honnêtes · 2 072 neutres
                        · 105 programmes · 0 erreur                       OK
CALIB 2 · POSITIF       17 affichées et 6 racines serveur                 OK
CALIB 3 · NÉGATIF       une signature FABRIQUÉE                           OK
```

**Les cinq chiffres se reproduisent à l'identique.**

## Le premier constat — **le « 95 » est un complément légitime, mais il n'a jamais été mesuré**

```text
atténuations publiées au 539                  112
   dont AFFICHÉES (le « 17 »)                  17
   NON affichées, recomptées ici               95
le seau AFFICHÉES est-il inclus dans les 112  OUI
112 − 17                                       95
```

Le recouvrement est **prouvé, pas supposé** (564-C) : le 95 est bien le
complément du 17 dans les 112.

Mais **`SKYLER-LOT-539.md` n'écrit jamais « 95 »**. Le chiffre **naît au 540**
(`SKYLER-LOT-540.md:118`, « les 95 atténuations non affichées ne sont pas
innocentées, elles sont hors sujet »), **par soustraction**, et il circule depuis
dans la liste des dettes de **vingt rapports** sans avoir jamais été compté pour
lui-même.

## Le second — **112 est un cumul par page ; les atténuations distinctes sont 84**

```text
entrées (page, fichier, position) — le chiffre publié   112
signatures distinctes                                    84
   signatures vues sur plus d'une page                    4
   unités en double                                      28
   signatures dans un fichier `/static/**`               25
   signatures dans un script inline                      59
```

Le banc du 539 relit **le même fichier statique une fois par page** — 105
programmes pour 8 pages. Quatre signatures sont chargées par les 8 pages :

```text
/static/vertex/js/charts/chart-core.js   pos 46857   axes[domI].value || 0
/static/vertex/js/charts/chart-core.js   pos 47238   a.value || 0
/static/vertex/js/charts/chart-core.js   pos 50645   d.value || 0
/static/vertex/js/vx-entities.js         pos  9277   t.cost || 0
```

**4 × 7 = 28 unités en double. 112 − 28 = 84.**

## Le troisième — **les doublons sont TOUS dans le seau jamais lu**

```text
                       publié   distinct
affichées                  17         17
racine serveur              6          6
NON affichées              95         67
feuille distincte : 17 + 67 = 84  (attendu 84)
signatures à la fois affichées ET non affichées : 0
```

C'est le résultat qui compte. **Les deux seaux que le 539 et le 540 ont lus un
par un — les 17 affichées, les 6 à racine serveur — sont EXACTS** : aucun
doublon, aucune correction. **Les 28 unités en double se logent intégralement
dans le seau que personne n'a jamais ouvert.**

Conséquence directe : **la conclusion du 539 (« aucun chiffre inventé ») et celle
du 540 (« les dix-sept ont toutes été lues ») ne sont pas entamées d'un iota.**
Seule la dette bouge : **« les 95 atténuations non affichées » vaut 67.**

Les trois chiffres lourds précédents rétrécissaient le titre (178 → 94, 25 → 18,
11 → 4). Ici le titre est intact et **c'est la dette qui rétrécit** — parce que
le doublon se loge là où personne ne regarde.

**Interprétations retirées : 8 → 9 (+1).**

## L'arrêt du lot — **deux « 25 » dans mon propre écran, recouvrement zéro**

Mon relevé affiche **25 signatures statiques du produit**. Le second contrôle
affiche **25 signatures dans la bibliothèque exclue**. Deux fois vingt-cinq,
côte à côte, dans la même sortie.

```text
signatures statiques du PRODUIT     25
signatures de la BIBLIOTHÈQUE       25
recouvrement mesuré                  0
fichiers produit : chart-core.js · regime-aura.js · options-gex.js
                   options-intel.js · options-structure.js · vx-entities.js
fichiers biblio  : chart.umd.min.js
```

**Zéro.** Ce sont deux ensembles disjoints qui portent le même cardinal par
hasard. Le 564 avait rencontré ce piège entre **deux rapports** ; ici il naît
**dans ma propre sortie, au même écran**. Publier « 25, comme la bibliothèque »
aurait fabriqué un lien qui n'existe pas.

**Arrêtés avant publication : 190 → 191 (+1).**

## Second contrôle (481) — le cas que la restriction EXCLUT

Le 539 saute `chart.umd.min.js` (« bibliothèque, pas le produit »).

```text
entrées trouvées dans la bibliothèque    200
signatures distinctes                     25
dont AFFICHÉES                             0
```

L'exclusion est **légitime** — c'est du code tiers, personne ne le corrigera
ici. Mais **elle n'était pas gratuite**, et le 539 n'en donne jamais la taille :
25 atténuations `|| 0` distinctes vivent dans la bibliothèque, et **aucune n'est
affichée** au sens du crible. Un chiffre **mesuré** plutôt que tu (560-C).

## Ce que le dépôt fait bien, mesuré

- **Les deux seaux lus un par un sont exacts** — 17 et 6, sans un seul doublon.
  Le travail d'analyse du 539 et du 540 portait sur des objets propres.
- **Zéro chevauchement** entre affichées et non affichées : la partition est
  nette.
- **Aucune des 4 signatures partagées n'est affichée** — les atténuations
  mutualisées sur les 8 pages vivent dans la mécanique des graphiques
  (`chart-core.js`) et le store (`vx-entities.js`), pas à l'écran.
- **La bibliothèque tierce n'affiche rien** : ses 25 atténuations restent
  internes.

## Portée — ce que ce lot NE dit PAS

- **Les 67 ne sont pas innocentées** : elles restent non lues, exactement comme
  les 95. Le lot **recompte**, il n'arbitre pas.
- La signature est (fichier, position) : **deux fichiers statiques identiques
  servis sous deux URL différentes seraient comptés deux fois**. Le cas ne se
  présente pas ici, mais il n'est pas exclu par construction.
- **Le corpus reste celui du 539** — les 8 pages en DÉMO, telles qu'enregistrées.
  Un script chargé dynamiquement n'y figure pas.
- **Trois chiffres lourds restent** : 103 états (541), 53 refus (542), 156
  variables serveur (540).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 1` — **le déclencheur du 565 lui-même**,
  encore en attente au moment du relevé ; aucun autre. `pwd` =
  `/home/user/Vertex-` ; sorties en chemin **absolu**, aucun banc tronqué avant
  d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Quatre chiffres lourds sur sept sont reproduits et qualifiés**,
et les quatre étaient des cumuls par page.

Ce que je retiens de ce lot : **un chiffre né d'une soustraction hérite en
silence des défauts de ses deux termes.** Le « 95 » était juste comme
*complément* — le recouvrement le prouve — et faux comme *compte*, parce que le
112 dont il descend était un cumul. Personne ne l'a jamais recalculé : il a été
recopié tel quel dans vingt rapports. Et le détail qui donne sa valeur au lot est
ailleurs : **les doublons ne se sont pas répartis au hasard, ils sont tous tombés
dans le seul seau que personne n'avait ouvert.**

Trois règles neuves :

- **565-A · UN CHIFFRE NÉ D'UNE SOUSTRACTION HÉRITE DES DÉFAUTS DE SES DEUX
  TERMES** — le 95 est exact comme complément et faux comme compte ; il fallait
  recompter le 112 pour le voir.
- **565-B · UN CUMUL NE SE RÉPARTIT PAS UNIFORMÉMENT** — 28 unités en double,
  **zéro** dans les deux seaux lus un par un, **28** dans le seau jamais ouvert.
  Le doublon se loge où personne ne regarde.
- **565-C · LE PIÈGE DES NOMBRES ÉGAUX PEUT NAÎTRE DANS SA PROPRE SORTIE** — les
  deux 25 ne venaient pas d'un vieux rapport, mais de mon banc, au même écran ;
  recouvrement mesuré à zéro avant d'écrire quoi que ce soit.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **TROIS chiffres lourds encore NON RECOMPTÉS** — 103
états (541), 53 refus (542), 156 variables serveur (540) ; **les 67 atténuations
non affichées, toujours non lues** ; **les 25 atténuations de la bibliothèque
tierce** ; **`/options|chips`, douzième limite jamais levée ni nommée** ;
**`renderCalendar`, exécutée hors périmètre au 537** ; **les 4 limites distinctes
du 564** ; **les 12 signatures partagées du 562** ; **les 5 cas de réponse
absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10 cas non
tranchés du 559** ; **les 16 sous-clés du 558, dont 12 sur des routes au contrat
non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35
clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans lecture
observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions de nom** ;
**les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ; **les 14
candidates du 554, en attente d'un GO** ; **les 4 routes construites
`/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **`initSettings`** ; **les 8 appels
hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les 92 rapports non additionnés du 526** ; **les quinze lots exposés du 525** ;
**le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente
d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 191 (+1)** ; publiés
puis corrigés **30** ; interprétations retirées **9 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**

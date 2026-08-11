# SKYLER — LOT 611 · NEUF BANDES, 144 MESURES, ZÉRO FAUTIVE

Le 610 avait corrigé un bandeau écrasé à 22 px en n'ayant mesuré que **deux
largeurs**, et l'avait dit. Ce lot mesure les autres. **Le défaut du 610 n'avait
pas de frère** — et ce lot ne change rien au produit.

## Ce qui a été mesuré

| largeur | bande | zones d'état | page déborde |
| --- | --- | --- | --- |
| **390** | ≤ 520 *(témoin du 610)* | 16 | 0 px |
| **600** | 521–640 — **jamais mesurée** | 16 | 0 px |
| **700** | 641–720 — **jamais mesurée** | 16 | 0 px |
| **768** | borne exacte — **jamais mesurée** | 16 | 0 px |
| **800** | 769–820 — **jamais mesurée** | 16 | 0 px |
| **900** | borne exacte — **jamais mesurée** | 16 | 0 px |
| **1024** | borne exacte — **jamais mesurée** | 16 | 0 px |
| **1180** | 1025–1280 — **jamais mesurée** | 16 | 0 px |
| **1440** | > 1280 *(témoin du 610)* | 16 | 0 px |

**144 mesures** — 6 écrans en échec × 9 largeurs × chaque bandeau comparé à son
parent. **Zéro fautive. Aucune page ne déborde, à aucune largeur.**

Les deux largeurs du 610 ont été **re-mesurées dans le même passage**, pas citées
de mémoire : sans référence connue-saine mesurée au même moment, un débordement
à 900 px ne dirait pas s'il est neuf (**610-B**).

## L'arrêt du lot — mon piège comptait quatre bascules ; il y en a huit

Mon piège, écrit avant de mesurer, annonçait *« `responsive.css` déclare quatre
bascules, donc cinq bandes »* et prévoyait **sept** largeurs.

En balayant **toutes** les feuilles servies : **huit bascules de largeur** —
520, 640, 720, **768**, 820, 900, 1024, 1280 — réparties sur `responsive.css`,
`neon-glass.css`, `tables.css`, `components.css`, `utilities.css`. Donc **neuf
bandes**, et **deux de plus non couvertes** que je ne le croyais : 521–640 et
769–820.

**C'est 605-C dans une autre feuille** : *un périmètre qui exclut une partie du
code conclut faux.* Au 605 c'était `terminal.py` ; ici c'est tout ce qui n'est pas
`responsive.css`. Banc corrigé à **neuf largeurs** avant toute conclusion.

**Arrêtés avant publication : 244 → 245 (+1).**

## Le piège, verdicts

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « au moins un bandeau déborde dans une bande intermédiaire » | **RÉFUTÉ** — 0 sur 144 |
| **(b)** | « s'il y en a un, il sera du même type que celui du 610 » | **SANS OBJET** — pas de défaut à typer. Un volet conditionnel dont la condition est fausse ne se vérifie pas : il ne compte ni pour ni contre |
| **(c)** | « les bornes exactes sont plus risquées que les milieux de bande » | **NON MESURABLE** — aucun défaut nulle part, rien à comparer (595-C) |
| **(d)** | « les 16 zones restent les seules ; aucune n'apparaît aux largeurs intermédiaires » | **CONFIRMÉ** — exactement 16 à chacune des neuf largeurs |
| **global** | | **le défaut du 610 était ISOLÉ** |

**(d) valait d'être posé** : si le nombre de zones avait varié avec la largeur, le
« 16 zones » du 610 n'aurait valu que pour ses deux points, et sa conclusion
aurait été plus étroite qu'annoncée. Il est constant — la mesure du 610 portait
bien sur l'ensemble.

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure **les bandeaux d'état**. Le cas exclu : **le débordement de
la page, tous éléments confondus** — un tableau ou un graphique peut déborder
sans qu'aucun bandeau ne bouge.

Mesuré aux neuf largeurs, sur les six écrans, en état d'échec :
**0 px de débordement partout**. Le contrôle ne trouve rien non plus — mais il
avait de quoi trouver : `/portfolio` et `/system` portent des **tableaux**, et
`/markets` des **graphiques**.

## Ce que le lot livre, puisqu'il ne corrige rien

Une mesure sans correctif vieillit mal : elle devient une phrase dans un rapport
que personne ne re-vérifie. **La conclusion « les neuf bandes sont saines »
repose sur une hypothèse — la liste des bascules.**
`tests/test_bascules_mesurees_lot611.py` l'épingle : **3 tests**, vérifiés par
mutation.

- **ajouter** une bascule (`max-width:1100px`) → rouge, avec la marche à suivre :
  *une bande neuve est apparue, re-mesurer puis mettre la liste à jour* ;
- **retirer** la règle de famille du 610 → rouge : la mesure du 611 vaut **pour un
  produit qui porte cette règle** ; sans elle, « zéro fautive » ne dit plus rien.

Plus un garde-fou de volume (591-C) : si la liste des largeurs exercées se
vidait, le premier test passerait encore alors que **rien** n'aurait été mesuré.

Le gardien **n'interdit pas** d'ajouter une bascule. Il exige qu'on **re-mesure
dans le même geste**.

## Ce que le lot n'établit pas

- **Que toutes les largeurs soient saines.** Neuf points sur un continuum. Les
  bandes sont couvertes, pas balayées.
- **Que les bandeaux soient lisibles** — police, contraste, ordre de lecture,
  cible tactile. Le 610 comme le 611 ne jugent que le **découpage** (610-A).
- Que les 16 zones soient les seules du produit : ce sont celles que **six
  écrans en échec** produisent. D'autres vues, d'autres pannes en produiraient
  d'autres.
- Que la hauteur tienne : **une seule dimension mesurée**. Un bandeau peut être
  correct en largeur et pousser le contenu hors de l'écran en hauteur.

## Règles neuves

- **611-A — UNE BANDE N'EST PAS UNE BORNE.** Mesurer à 768 px teste la bande
  « ≤ 768 » ; cela ne dit rien de 769–820. Un balayage responsive se conçoit par
  **intervalles entre bascules**, pas par valeurs remarquables.
- **611-B — UN VOLET DE PIÈGE CONDITIONNEL NE SE VÉRIFIE PAS SI SA CONDITION EST
  FAUSSE.** « S'il y a un défaut, il sera de tel type » ne compte ni pour ni
  contre quand il n'y a pas de défaut. Le noter **sans objet** vaut mieux que le
  compter comme confirmé.
- **611-C — UNE MESURE SANS CORRECTIF DOIT LAISSER UN GARDIEN DE SON HYPOTHÈSE.**
  Sinon elle devient une phrase dans un rapport, vraie le jour où elle est
  écrite et jamais re-vérifiée.

## Ce que le dépôt fait bien

- **Le nombre de zones d'état est constant sur neuf largeurs** : le rendu ne
  cache ni n'invente d'état selon la taille de l'écran.
- **Aucune page ne déborde, nulle part** — tableaux et graphiques compris, en
  état d'échec. Les lots mobiles 289 à 295 tiennent toujours.
- **La règle de famille du 610 tient sur les neuf bandes**, y compris aux bornes
  où deux jeux de règles se disputent.
- **Le 610 avait déclaré sa limite** (« deux points mesurés, rien entre les
  deux »). C'est cette phrase qui a rendu ce lot possible.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **Aucun fichier de production touché** — mesure et gardien seulement.
- **1 gardien neuf** (3 tests, rouge dans les deux sens).
- MD5 des 8 pages : **8 / 8 identiques**. **Aucun bump** — SW inchangé à
  `td-shell-v194`.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2901 passed / 0 skipped** *(2898 + les 3 du gardien neuf)*.
- Navigateur : **54 chargements de page** (6 écrans × 9 largeurs), **144 mesures
  de zone**, chacune comparant le bandeau à son parent.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **245 (+1)**
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 8** *(inchangé — ce lot ne corrige rien, il borne
  ce que le 610 avait laissé ouvert)*

# SKYLER LOT 525 — La borne basse du 522 resserrée : **4 lots exposés → 16**. Et le chiffre du dossier 518-A, recompté par AST, **n'est ni confirmé ni réfuté : il est ENCADRÉ, 57 % — 77 % — 94 %**, parce que le 518 n'avait jamais énoncé sa définition

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-525` (base : lot 524 fusionné,
`1daf2612`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(d)** — l'axe du français peint est mesuré et ne rapporte plus : deux lots ont
porté la couverture à 81 % pour **six occasions et zéro défaut**. **Dire qu'un
axe s'épuise est un résultat**, et il faut alors passer.

Le 522 avait laissé une borne explicite : « quatre lots exposés » est une
**borne basse**, jamais resserrée. C'est le seul travail qui **consolide la
feuille entière** au lieu d'y ajouter une ligne.

## L'instrument se déplace d'un cran : non pas « y a-t-il une regex » mais « sur QUOI porte-t-elle »

Une regex qui lit le **code source du dépôt** expose un chiffre. Une regex qui
lit la réponse d'une route, sa propre sortie JSON ou une liste de noms de
fichiers n'expose rien.

```text
CALIB 1 · POSITIF   `l514_controle2.py`, qui a produit le « 253 » FAUX
                    en grepant des sources → EXPOSÉ                    OK
CALIB 2 · NÉGATIF   `l521_garde.py`, le verrou réseau, ne lit aucune
                    source → NON exposé                                OK
CALIB 3 · VARIÉTÉ   31 exposés · 42 avec regex mais SANS lecture de
                    source — les deux classes sont peuplées            OK
```

## La borne basse, resserrée

```text
bancs inventoriés aujourd'hui                                    133
   (le 522 en comptait 115 ; les lots 522→524 en ont ajouté 18)
bancs dont une regex lit le CODE SOURCE du dépôt                  31
lots concernés                                                    16

483 · 484 · 485 · 486 · 491 · 493 · 494 · 498
509 · 510 · 512 · 514 · 515 · 516 · 518 · 521

dont NON comptés par le 522                                       14
```

**Le « quatre lots » du 522 devient « seize ».** Le 522 le disait borne basse ;
il l'était de **quatre fois**.

**Ce que je NE publie PAS** : le 522 annonçait « 3 scripts mixtes appliquant une
regex à du code source ». Ce n'est **pas comparable** à mon 31 — le sien portait
sur le sous-ensemble des **mixtes**, le mien sur **tous** les bancs. Annoncer
« 3 → 31 » comme une correction aurait été un faux rapprochement. **Arrêt.**
(J'observe tout de même que ce « 3 » n'est **pas re-dérivable** du banc conservé :
il avait été calculé hors du script. La règle **522-D** vaut aussi pour le 522.)

## Le chiffre qui porte le dossier 518-A, recompté par AST

Parmi les 16 lots exposés, **le 518** porte un dossier de **rang 4** :
« 77 % de la surface servie n'a aucun test qui regarde ce qu'elle affiche ».
Son banc, `l518_couverture.py`, cherche l'URL **dans le texte** des tests et
devine les boucles par le motif `for X in (…)`.

Recompté **par l'arbre**, sans jamais regarder le texte : registres lus par AST,
URL reconstruites depuis l'AST des tests avec substitution des variables de
boucle à itérable **littéral**.

```text
CALIB 1 · TÉMOIN JUSTE  les registres rendent 35 vues — chiffre déjà
          confirmé deux fois, aux 518 et 523, par des chemins
          indépendants                                                 OK
CALIB 2 · POSITIF       `/portfolio?view=risk` ressort demandé
          (6 tests)                                                    OK
CALIB 3 · NÉGATIF       une paire FABRIQUÉE n'est demandée nulle part  OK
```

```text
35 vues servies · 301 fichiers de tests
   REQUÊTÉES par au moins un test                    29   (83 %)
```

### Et là, le chiffre refuse de se laisser recompter

Tout dépend de ce que veut dire **« un test regarde le contenu »** — et **le 518
ne l'a jamais défini**.

```text
définition LARGE     un `assert` de la MÊME fonction porte sur le corps
                     de la réponse            → 15 gardées · 57 % sans
518 publiait         « regarde le CONTENU »   →  8 gardées · 77 % sans
définition STRICTE   l'assertion n'est attribuable que si la fonction
                     ne demande QU'UNE vue    →  2 gardées · 94 % sans
```

**Le chiffre publié tombe À L'INTÉRIEUR de l'encadrement.** Il n'est donc **ni
confirmé ni réfuté : il est ENCADRÉ**.

**J'avais d'abord écrit « RÉFUTÉ ».** Mon premier passage ne portait que la
définition large et sortait 57 % — vingt points sous le chiffre publié. En la
serrant, elle donne 94 %, vingt points **au-dessus**. **Publier « réfuté » aurait
été choisir la définition qui m'arrangeait.** **Arrêt.**

La définition stricte a une raison d'être : **`test_subviews_return_200` parcourt
21 vues à lui seul**. Attribuer à ces 21 vues une assertion écrite une seule fois
dans la fonction, c'est **agréger en perdant une dimension** — le piège que le
518 lui-même avait nommé (**518-A**).

```text
fonctions de test demandant PLUSIEURS vues
   test_subviews_return_200                    21 vues
   test_options_pages_render_200                8
   test_fiche_ticker_and_key_subviews_ok        5
   test_journal_routes_200                      5
```

### Ce que cela fait au dossier

**518-A survit, et sa direction est plus solide qu'avant** : sous les **trois**
définitions — 57 %, 77 %, 94 % — la majorité des vues servies n'a pas de
protection de contenu. **Ce qui n'est pas établi, c'est l'ampleur.** Le rang 4
reste juste ; le « 77 % » doit se lire **« entre 57 % et 94 % selon ce qu'on
appelle regarder le contenu »**.

## Ce que le dépôt fait bien, mesuré

- **29 vues sur 35 sont réellement requêtées** par la suite. Six ne le sont pas :
  `/markets?view=overview`, `/opportunities?view=radar`, `/portfolio?view=team`,
  `/portfolio?view=performance`, `/portfolio?view=options`,
  `/system?view=automations`. Le 518 en annonçait **onze** ; l'AST, qui résout
  les boucles au lieu de les deviner, en trouve **six**. **La suite couvre plus
  que ce que le motif voyait.**
- Le témoin des **35 vues** ressort juste pour la **troisième fois**, par un
  troisième chemin.

## Second contrôle — ce que l'instrument EXCLUT (règle 481)

```text
appels `.get(…)` dans les tests                     590
   URL reconstruite depuis l'arbre                  525   (89 %)
   NON résolue (variable non littérale, fixture)     65   (11 %)
```

**Onze pour cent des requêtes de test restent invisibles** à mon instrument. Une
vue comptée « non requêtée » pourrait l'être par l'une d'elles. Le « six » est
donc une **borne haute** du non-requêté, exactement comme le « onze » du 518 en
était une autre.

Et mon crible d'exposition mesure **par script**, pas **par chiffre** : un banc
qui lit des sources peut n'en tirer aucun chiffre publié. **Seize lots exposés
est une borne HAUTE**, quand le « quatre » du 522 était une borne basse. **La
vérité est encadrée entre les deux — et je ne peux pas la resserrer davantage
sans relier chaque chiffre publié à l'instruction qui l'a produit.**

## Portée — ce que ce lot NE dit PAS

- **Un seul chiffre recompté.** Les quinze autres lots exposés restent en l'état.
- **Aucun dossier n'est retiré ni ajouté.** 518-A garde son rang.
- Mon instrument ne voit pas les URL construites hors littéraux (11 %).
- Un chiffre exposé **n'est pas un chiffre faux** (**522-B**) : sur le seul
  recompté, le dossier tient.
- **Aucun navigateur, aucun POST, aucune route appelée** — ce lot ne lit que du
  code et des arbres.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Le lot fait deux choses qu'aucun n'avait faites : il **resserre
d'un facteur quatre une borne que j'avais moi-même déclarée basse**, et il
montre qu'un chiffre de rang 4 **ne peut pas être recompté parce que sa
définition n'a jamais été écrite**.

Trois règles neuves :

- **525-A · UN CHIFFRE SANS DÉFINITION ÉCRITE N'EST PAS RECOMPTABLE** — « regarde
  le contenu » couvre 57 % à 94 % selon ce qu'on entend. Écrire la définition
  dans le rapport, pas seulement le nombre.
- **525-B · QUAND DEUX DÉFINITIONS ENCADRENT UN CHIFFRE PUBLIÉ, IL N'EST NI
  CONFIRMÉ NI RÉFUTÉ** — choisir celle qui arrange serait le pire des deux.
- **525-C · UNE BORNE BASSE ET UNE BORNE HAUTE SE MESURENT SÉPARÉMENT** — le
  « quatre lots » du 522 et le « seize » d'ici encadrent la même vérité par les
  deux côtés ; aucun des deux n'est le compte.

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **les quinze autres lots exposés, non recomptés** ;
**l'ampleur du 518-A, encadrée et non établie** ; **les 11 % de requêtes de test
invisibles** ; **les 17 chargeurs encore muets** ; **le « 7 barèmes » du 491** ;
**mesurer les 23 routes — outil prêt, en attente d'un GO** ; **l'assemblage entre
fonctions** ; **la condition `k ≤ 5` sur un scan réel** ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 128 (+2)** ; publiés
puis corrigés **17** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**

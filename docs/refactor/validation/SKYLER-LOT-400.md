# SKYLER LOT 400 — BILAN n°9, tranche 390 → 399

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-400` (base : lot 399 fusionné,
20a917f)

Dix lots. Ce bilan est fait **sur pièces** — les dix rapports relus, les chiffres
re-mesurés dans le dépôt, pas repris de mémoire.

## Ce qu'est cette tranche, sans enjoliver

**Elle n'a rien construit.** Elle a vérifié, mesuré, et réparé quelques défauts
de son propre outillage.

```text
lots ayant ajouté un gardien            3   (391, 392, 393 — 27 tests)
lots ayant réparé un fichier de test    3   (394, 398, 399)
lots n'ayant produit qu'une ligne       2   (390 bilan, 397)
lots n'ayant touché aucun fichier       2   (395, 396)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0
```

Le dernier chiffre est **mesuré**, pas affirmé :

```console
$ git diff --name-only <lot 389>..HEAD | grep -vE '^(tests|docs)/'
  (aucun)
```

Six fichiers de test et douze fichiers de documentation : c'est tout ce que dix
lots ont déposé dans le dépôt.

## Les chiffres

| | |
|---|---|
| Lots | 10 (390 → 399) |
| Suite | **2 835 / 2 skipped → 2 864 / 0 skipped** (+29 tests, −2 skips) |
| Tests ajoutés | 27 (gardiens 391/392/393) + 2 (réveillés au 398) = **29** — exactement le delta |
| PR | #422 → #431, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, **inchangé sur les 10 lots** |
| Fichiers de production modifiés | **0** |
| `main` | jamais touchée |

Pour mémoire, la tranche précédente ajoutait **+81** tests. Le rythme a été
divisé par près de trois — c'est cohérent avec une tranche de vérification, pas
un signe de ralentissement à cacher.

## Les six trouvailles réelles

1. **391 — un scan de DÉMO écrit dans `breadth_history.json`, servi comme réel.**
   16 points strictement identiques (`a50 50 · a200 45 · net −4 · health 37`) du
   21/07 au 08/08. Site d'écriture **inconditionnel** — aucun test de
   `DEMO_MODE` — et il **écrase** le point du jour s'il existe. La chaîne
   `/scan → internals.history → « Tendance de participation »` est servie sur
   `/markets`, dont le code dit lui-même « historique breadth **RÉEL** ». Le
   point persisté ne porte **aucune provenance**, alors que
   `market_context_last.json` en porte une : le mécanisme honnête existe, il
   n'est pas appliqué ici. **Reproduit à l'identique au lot 396.**

2. **392 — l'angle mort du lot 377 est propre, et un 22ᵉ fichier runtime.**
   30 routes à réponse construite en variable, sollicitées à l'exécution :
   **12 refus, 12 motivés, 0 muet**. Résultat négatif, mais mesuré. En chemin, une
   sonde a **créé** `desc_cache.json` — un fichier runtime que l'inventaire ne
   connaissait pas.

3. **394 — une docstring fausse dans un gardien historique.**
   `test_desk_sync_keys_single_source_of_truth` affirmait que « la source de
   vérité servie est `vx_kit` (kit global, présent sur toutes les pages) » : faux
   depuis le lot 381, qui a mesuré que ce JS n'atteint **aucune** des 8 pages. Un
   lecteur ouvrant ce test pour comprendre la règle n°1 y lisait le contraire de
   ce que le dépôt fait.

4. **397 — un chiffre affirmé dans le registre sans source dans le rapport.**
   L'index déclarait `v187` pour le lot 394 ; le rapport 394 ne l'écrivait nulle
   part, seul des 25 de la tranche. La valeur était juste, l'assertion n'était
   **adossée à rien**. Rien d'autre ne l'aurait révélé.

5. **398 — deux tests morts depuis leur création.**
   Les deux `skipped` que la suite affichait dans chaque rapport depuis des
   dizaines de lots. Skips **structurels** : aucun test de la suite ne déclenche
   de scan, et ce fichier est le **seul des 300** à appeler `/scan`. Réveillés
   après avoir prouvé par mutation qu'ils protègent quelque chose ; suite passée
   à **0 skipped**.

6. **399 — un test écrivait dans le dépôt de l'utilisateur.**
   `/desc/<sym>` écrit `desc_cache.json` **à la racine** quand le fetch yfinance
   réussit ; le test du lot 392 appelle cette route à chaque passe. Doublement
   invisible : le réseau échoue dans l'environnement d'agent, **et** le
   recensement du lot 389 ne pouvait pas le voir parce que l'écriture est
   conditionnée à la **réussite** du fetch. Corrigé. Au passage, un **23ᵉ**
   fichier runtime identifié (`constituents_cache.json`, gitignoré — vérifié).

## Les veines closes — closes, pas productives

Six pistes ont été fermées **par la mesure** pendant la tranche. Une veine close
est un résultat honnête ; ce n'est pas une livraison.

| veine | close au | résultat |
|-------|----------|----------|
| refus API construits en variable | 392 | 30 routes, 12 refus, 0 muet |
| promesses de retour imbriquées | 393 | 2 fonctions, 0 promesse fausse |
| rejeu des gardiens anciens | 394 | 7/8 mordent ; l'écart était une docstring |
| pistes fines restantes | 395 | rien qui mérite un lot, vérifié |
| octets servis | 396 | MD5 8/8 identiques |
| cohérence du registre | 397 | 25/25 présents, 1 écart corrigé |

## Ce que la tranche a appris sur la méthode

Toutes ces leçons portent sur **l'instrument, pas sur le code mesuré** — c'est le
motif dominant de la tranche.

- **391** — compter les occurrences avant de muter (`vx-demo-banner` apparaît
  4 fois ; une mutation locale ne faisait pas disparaître la bannière).
- **392** — un dénominateur non trié exagère le trou (393 « angles morts » dont
  359 sont des aides internes) ; et une sonde peut **créer** un fichier runtime.
- **393** — quand un rapport déclare qu'« il faudrait un analyseur d'un autre
  ordre », demander d'abord si l'**exécution** tranche. Elle tranchait.
- **394** — *une ancre absente n'est pas un résultat : c'est une mesure qui n'a
  pas eu lieu.*
- **395** — *un énoncé faux se corrige immédiatement là où c'est gratuit, et se
  verse aux dossiers là où cela coûte au produit* (le cache de tout le monde).
- **397** — *un détecteur qui ne connaît qu'UNE forme du document cherché
  fabrique de faux manquants.*
- **399** — *une écriture conditionnelle au réseau échappe à un recensement fait
  hors ligne* ; et *c'est le témoin positif qui donne sa valeur à un « 0 »*.
- **400, aujourd'hui** — pendant la rédaction de ce bilan, mon répertoire courant
  avait dérivé (le shell reste où un `cd` l'a laissé) et j'ai cru, six commandes
  durant, que `CLAUDE.md` avait disparu du dépôt. Il n'a jamais bougé.
  **L'instrument avant le document, encore — et cette fois l'instrument était le
  shell.**

## L'état du produit n'a pas bougé

Vérifié dans le dépôt, pas rappelé :

```console
$ git diff --name-only e3074e8..HEAD | grep -vE '^(tests|docs)/'
CLAUDE.md          (+15 −1, lots 381 et 382)
```

Depuis le correctif XSS du lot **372** — qui touchait 4 fichiers de
`vertex/ui/` — la seule modification hors tests et documentation est **deux
corrections de `CLAUDE.md`**, faites aux lots 381 et 382. **Sur la tranche
390-399, zéro.** Le MD5 des 8 pages servies a été re-prouvé identique aux lots
**390** et **396**.

Dit franchement : **la boucle entretient et vérifie, elle ne construit plus.**
Ce n'est pas un reproche à l'exécution — c'est la conséquence directe du point
suivant.

## La question de fond, reposée

**Aucun GO n'est arrivé depuis le lot 388.** Les dossiers du **rang 1** — ceux où
l'utilisateur voit du faux dans son terminal — sont tous à l'arrêt en attente
d'une décision qu'un agent ne peut pas prendre à sa place :

- les **7 points MSFT fabriqués** dans `gex_history_cache.json` (388) ;
- le **scan de démo écrivant dans `breadth_history.json`** (391, reproduit au 396) ;
- `context()` affirmant des verdicts sur un univers vide (379) et « points réels
  du scan » sur `/markets` (363) ;
- les replis `0` de `_followed_count` / `_positions_count` (378) ;
- le badge de provenance IBKR jamais affiché (386).

Trois issues, présentées sans détour :

**(a) Continuer les lots courts de vérification.** Rendement décroissant, et
c'est mesuré : sur les six derniers lots, deux n'ont trouvé strictement rien.
Il reste des points de contrôle non consommés, mais ils s'épuiseront.

**(b) Un GO groupé sur les dossiers de rang 1, puis exécution.** ← **recommandé.**
À commencer par la **purge des 7 points MSFT** : coût quasi nul, risque nul, et
c'est aujourd'hui la seule ligne où un chiffre inventé est servi comme une
mesure. Le dossier `breadth_history` suit, avec ses trois issues défendables à
trancher.

**(c) Arrêter la boucle et attendre.** Défendable : le produit est stable, la
suite est verte, et rien ne se dégrade pendant l'attente.

Ce qui ne serait **pas** honnête, c'est de continuer indéfiniment en (a) en
laissant croire que le travail avance sur ce qui compte. Il n'avance pas :
**il attend une décision.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — bilan documentaire. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Serveur DEMO **non lancé** (il fabriquerait un point dans `breadth_history`).
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; écart final
  **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Ce bilan mesure ce que la tranche a **déposé dans le dépôt** et ce que les dix
rapports affirment. Il ne re-vérifie pas les trouvailles une à une — 396 et 397
l'ont fait pour les octets servis et pour le registre ; le reste repose sur les
preuves consignées dans chaque rapport.

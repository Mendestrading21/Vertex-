# SKYLER V2 — EXECUTION STATUS

> Branche d’intégration : `integration/vertex-skyler-v2`  
> Base historique : `agent/vertex-neon-glass-graphs`  
> Statut : **Skyler V2 Core livré — phase Institutional+ ouverte**.

## BILAN — veille active, lots 410 → 419 (2026-08-09, bilan n°11)

Dix lots. Bilan **sur pièces** : les dix rapports relus, les chiffres re-mesurés
dans le dépôt. Serveur DEMO non lancé.

**La tranche a deux moitiés nettes.**

```text
410        bilan n°10
411 → 415  LES OCTETS SERVIS   provenances · cache SW · chemins client
                               · boutons · identifiants dupliqués
416 → 419  LES MOTEURS         RSI · track_record · multiplicateur · bornage
```

**Première moitié — produit sain, filet court.** Zéro défaut produit sur cinq
contrôles : 59 provenances dont 25 littéraux exacts (411) · 156 chemins client,
aucun mort (413) · 167 boutons servis, aucun sans écouteur (414) · 288
identifiants, aucun doublon (415). Mais **trois fois sur cinq, le gardien censé
protéger l'invariant s'arrête avant la fin** : le 412 **détecte sans imposer**, le
414 couvre **149 boutons sur 167**, le 415 visite **3 pages sur 8**.

**Seconde moitié — quatre lots, quatre trouvailles** : RSI = 100 sur série plate
(416) · `track_record`, le N affiché n'est pas le N du calcul, jusqu'à une seule
observation (417) · multiplicateur d'option assumé à 100 et `MULTIPLIER_INVALID`
mort deux fois (418) · bornage — 4 sites de détection sur 22 replis, et un **RSI
de 0 effacé** (419).

**Le fait le plus important : le changement de famille a payé immédiatement.**

```text
veine « octets servis »   5 lots   0 défaut produit, 3 filets courts
veine « moteurs »         4 lots   4 défauts produit
```

La note de cadence du 416 — *si le lot rend une quatrième fois « produit sain,
gardien à périmètre court », changer de famille* — était **le bon appel**, et la
décision est **reproductible : quand trois lots d'affilée rendent le même
diagnostic de forme, changer de famille.**

**Le motif technique, vérifié quatre fois** : la bonne pratique est écrite **à
quelques lignes du défaut** — 416 `pos = 50.0` quand `hi == lo`, trois lignes plus
bas · 417 `tp1_resolved` dans le même dictionnaire · 418 le `is None` explicite de
`quantity`, deux lignes plus haut · 419 le `is not None` du coût moyen, quatre
lignes plus haut. Le défaut n'est jamais l'ignorance de la règle : c'est son
**application incomplète**. *Chercher la règle que le fichier respecte ailleurs,
puis l'endroit où il l'oublie* — méthode la plus rentable depuis le lot 398, et
désormais formulable comme une **procédure**.

**Le résultat le plus parlant — deux fautes opposées sur le même indicateur :**

```text
416   RSI FABRIQUÉ à 100   série plate → 0/0 indéfini, rendu comme l'extrême
419   RSI EFFACÉ à 0       `float(d.get('rsi') or 50)` → 0.0 est falsy → neutre 50
```

Une seule cause : **traiter une valeur extrême légitime comme une donnée
manquante**. Dans un cas on invente, dans l'autre on gomme, et les deux se lisent
comme des mesures.

**Les gravités, distinguées et non gonflées** : un NOMBRE FAUX (407, hors
tranche) ≠ un ÉCHANTILLON MAL PRÉSENTÉ (417) ≠ une HYPOTHÈSE DOCUMENTÉE NON
VÉRIFIÉE (418) ≠ un TEXTE D'EXPLICATION INCOMPLET (419). **Trois lots ont resserré
leur propre diagnostic quand la mesure les contredisait** (416, 418, 419).

**L'instrument pris en défaut : 7 fois sur 10 lots**, toujours attrapé **avant
publication** — 413 deux fois (`/static` hors corpus ; `fetch(` sans ses
enveloppes), 414 deux fois (55 faux « boutons morts » ; 231 comptés au lieu de
167), 415 deux fois (heuristique de proximité 9→1 ; test d'englobement rendant
des lignes propres, alignées et fausses), 417 une fois. **La leçon des enveloppes
a été refaite trois fois — 409 `emptyCard`, 413 `get(…)`, 414 `$(…)` :** une règle
écrite ne suffit pas, c'est le témoin qui l'attrape ; la parade est structurelle
— exiger la **proximité** d'un accesseur quelconque.

**Ce qui n'a pas bougé, mesuré :**

```console
$ git diff --name-only bbd5f86..HEAD | grep -v '^docs/'
  (aucun)
```

| | |
|---|---|
| Fichiers de production modifiés | **0** |
| Fichiers de test modifiés | **0** (la tranche précédente en avait 1) |
| Tests ajoutés | **0** — délibérément |
| Suite | **2 864 / 0 skipped**, identique aux dix lots |
| PR | **#442 → #451**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, servi et enregistré, inchangé |

MD5 des 8 pages : prouvé aux lots **390** et **396**, **pas re-mesuré depuis** —
aucun octet de production n'ayant bougé, il est réputé inchangé : **inférence,
pas mesure fraîche.**

**La question, plus pressante qu'au bilan n°10.** Le rang 1 contient maintenant
**six dossiers**, dont **deux chiffres faux affichés comme réels** : HHI d'un
facteur 170 avec alerte fabriquée (407) et RSI = 100 sur un titre immobile (416) ;
plus la consigne impossible (406/409), l'échantillon mal présenté sur la page qui
parle de confiance (417), les 7 points MSFT fabriqués (388) et les replis `0`
(378). **Aucun GO n'est arrivé depuis le lot 388 — trente-deux lots.**

- **(a)** continuer les lots courts. La veine des moteurs paie encore (4/4) — mais
  elle produit des **constats**, pas des corrections.
- **(b) GO groupé sur le rang 1, puis exécution. ← recommandé.** Purge des 7
  points MSFT (coût et risque quasi nuls), puis `myCapital`, puis le RSI (deux
  lignes, deux moteurs).
- **(c)** arrêter la boucle et attendre. Défendable : rien ne se dégrade, la
  production n'a pas bougé depuis le lot 399.

Les bilans n°9 et n°10 posaient déjà cette question et **ne sont pas reformulés
ici** — s'y reporter. La seule chose qui a changé depuis le n°10 et qui compte :
**il y a désormais deux chiffres faux affichés, pas un.**

**Portée** : ce bilan mesure ce que la tranche a **déposé dans le dépôt** et ce
que les dix rapports affirment ; il ne rejoue pas les trouvailles une à une.
Aucun serveur DEMO lancé, aucun moteur rouvert. Écart runtime final **aucun**.

## BILAN — veille active, lots 400 → 409 (2026-08-09, bilan n°10)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
re-mesurés dans le dépôt.

**Cette tranche n'est pas la précédente.** Le bilan n°9 disait de la 390-399
qu'« elle n'a rien construit ». Celle-ci a **trouvé deux défauts visibles par
l'utilisateur**, puis les a **bornés**.

```text
lots ayant TROUVÉ un défaut             3   (401, 406, 407)
lots ayant BORNÉ une trouvaille         3   (402, 408, 409)
lots revenus NÉGATIFS                   3   (403, 404, 405)
bilan                                   1   (400)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0     ← mesuré
```

Un seul fichier non documentaire modifié en dix lots :
`tests/test_skyler_sweep_x1.py`, le correctif du 401.

| | |
|---|---|
| Suite | **2 864 / 0 skipped**, identique aux 10 lots |
| Tests ajoutés | **0** — délibérément (tranche précédente : +29) |
| PR | **#432 → #441**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, inchangé |

**Les trois trouvailles.** **401** — `test_sweep_route_and_no_journaling`
restaurait avec `if v is None: scan_state.pop(k)` ; or `market_ctx` est
initialisée à `None`, donc la clé **existe** et sa valeur légitime **est**
`None` : la remise en état la **supprimait** du dict partagé, et le gardien des
8 clés documentées tombait selon l'ordre d'exécution (repro à **deux fichiers**).
**406** — sur les 17 clés du contrat `DESK_KEYS`, **7 n'ont aucun écrivain** ;
deux sont **lues par `/portfolio`** (`myTradesEquity`, `myCapital`) → **courbe
d'équité et drawdown jamais affichables**, et l'état vide promet « *elle se
construit au fil des clôtures* » alors que clôturer n'écrit jamais cette clé.
Piège évité : élaguer `DESK_KEYS` serait une **perte de données** (last-writer-wins
total, mécanisme du 362). **407** — `cash: E().capital() || 0` envoyé avec
`simulated: false`, donc **déclaré réel** : `hhi` **0.5003 contre 0.0029** avec
un cash réel, **un facteur 170** ; et avec **une seule position** HHI = **1.0**,
donc le terminal affiche « **Concentration très élevée** » là où un portefeuille
réel n'aurait aucune alerte. Trois lignes plus bas, le fichier écrit la règle
qu'il enfreint : *« Manquant/insuffisant n'est jamais présenté comme zéro. »*

**Les trois bornages — aussi utiles que les trouvailles.** Savoir si un défaut
est isolé ou général **change la décision** :

```text
402   dépendance d'ordre     300 / 300 fichiers verts en isolation   → 401 était la seule
408   `|| 0` fautif          1 sur 25 charges utiles POST            → 407 est isolé
409   consigne impossible    1 sur 12 promesses (sur 88 états vides) → 406 est unique
```

Sans eux, la correction aurait pu passer pour une campagne. **Ce n'en est pas
une : une cause, un site, une carte.**

**Les trois lots négatifs** — 403 (2 tests sans assertion sur 2 563, tous deux
légitimes), 404 (0 assertion avalée sur 91 candidates), 405 (0 asset mort sur 54)
— sont des **résultats**, pas des échecs : dénominateur mesuré, instrument
prouvé. Mais ils **coûtent**, et leur rendement décroît ; trois d'affilée avaient
justifié de le dire au 405.

**LE POINT PRINCIPAL DE LA TRANCHE.** **L'instrument — ou son interprétation — a
été pris en défaut dans 6 lots sur 10**, dont **deux fois dans le même** (401),
et **chaque fois avant publication** :

```text
400   un `cd` oublié → j'ai cru six commandes durant que CLAUDE.md avait disparu
401   hook pytest mesurant AVANT les finalizers → 84 « fuites » dont 42 fausses
401   témoin `monkeypatch` écrivant une valeur DÉJÀ présente → idempotent, muet à tort
402   `nohup … &` → deux passes concurrentes, 195 fichiers couverts sur 300 annoncés
406   fichier exclu pour ce qu'il DÉCLARE → « 13 clés sans écrivain », dont `myTrades`
408   vivier trié par la FORME (53) pris pour une liste → le 1ᵉʳ candidat ouvert est sain
409   compter la DÉFINITION d'une aide au lieu de ses APPELS → le site du 406 introuvable
```

Ce n'est pas que la méthode soit mauvaise : c'est que **le contrôle de
l'instrument est la partie du travail qui rapporte le plus**. Chacune de ces
erreurs aurait produit un rapport faux, présenté avec les mêmes tableaux et la
même assurance.

**L'état du produit n'a pas bougé** : aucun fichier de production modifié sur la
tranche. Le MD5 des 8 pages a été re-prouvé identique aux lots **390** et
**396**, et **pas re-mesuré depuis** — c'est une inférence, pas une mesure
fraîche, et c'est écrit comme telle.

**LA QUESTION, PLUS COURTE QUE CELLE DU BILAN n°9.** Le rang 1 ne contient plus
seulement des inexactitudes discrètes. Il contient **un chiffre FAUX affiché
comme RÉEL** (HHI ×170, alerte de concentration fabriquée dès une seule
position), **une consigne que le trader ne peut pas suivre**, et depuis le 388
**7 points MSFT fabriqués** servis comme des mesures. La correction est **bornée
et petite** — une cause (`myCapital` jamais écrit), un site
(`portfolio_page.py:718`), une carte — et les lots 408 et 409 l'ont vérifié
exprès pour que la décision soit facile.
**Aucun GO depuis le lot 388 : vingt-deux lots.**
**(a)** continuer les lots courts — rendement décroissant, mesuré ;
**(b) GO groupé sur le rang 1, puis exécution — RECOMMANDÉ**, en commençant par
la purge des 7 points MSFT puis `myCapital` ;
**(c)** arrêter la boucle et attendre — défendable, rien ne se dégrade.
Ce qui ne serait pas honnête : continuer en (a) en laissant croire que le travail
avance sur ce qui compte. **Depuis le 406, il ne s'agit plus d'hygiène — un
chiffre faux est affiché comme réel.**

## BILAN — veille active, lots 390 → 399 (2026-08-09, bilan n°9)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
re-mesurés dans le dépôt, rien repris de mémoire.

**Ce qu'est cette tranche, sans enjoliver : elle n'a rien construit.** Elle a
vérifié, mesuré, et réparé quelques défauts de son propre outillage.

```text
lots ayant ajouté un gardien            3   (391, 392, 393 — 27 tests)
lots ayant réparé un fichier de test    3   (394, 398, 399)
lots n'ayant produit qu'une ligne       2   (390 bilan, 397)
lots n'ayant touché aucun fichier       2   (395, 396)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0     ← mesuré, pas affirmé
```

| | |
|---|---|
| Suite | **2 835 / 2 skipped → 2 864 / 0 skipped** (+29, −2 skips) |
| Tests ajoutés | 27 gardiens + 2 réveillés = **29** — exactement le delta |
| PR | #422 → #431, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, **inchangé sur les 10 lots** |
| `main` | jamais touchée |

Tranche précédente : **+81** tests. Le rythme est divisé par près de trois —
cohérent avec une tranche de vérification, et dit plutôt que caché.

**Les six trouvailles réelles.** **391** — un scan de DÉMO écrit dans
`breadth_history.json` : 16 points strictement identiques, site d'écriture
**inconditionnel** qui **écrase** le point du jour, servi sur `/markets` comme
« historique breadth RÉEL », et le point persisté ne porte **aucune provenance**
alors que `market_context_last.json` en porte une (reproduit au 396). **392** —
l'angle mort du 377 est **propre** : 30 routes, 12 refus, 12 motivés, 0 muet ;
et une sonde a **créé** un 22ᵉ fichier runtime. **394** — une docstring
**fausse** dans le gardien historique des clés desk, périmée depuis le lot 381.
**397** — un chiffre affirmé dans l'index **sans source** dans le rapport, que
rien d'autre n'aurait révélé. **398** — deux tests **morts depuis leur
création**, réveillés après preuve par mutation ; suite passée à **0 skipped**.
**399** — un test écrivait `desc_cache.json` **à la racine du dépôt de
l'utilisateur** ; doublement invisible, car le réseau échoue ici **et** parce que
l'écriture est conditionnée à la RÉUSSITE du fetch ; + un 23ᵉ fichier runtime
identifié (`constituents_cache.json`, gitignoré, vérifié).

**Six veines closes par la mesure** (392, 393, 394, 395, 396, 397). Une veine
close est un résultat honnête — **ce n'est pas une livraison.**

**Les leçons de méthode portent toutes sur l'INSTRUMENT, pas sur le code
mesuré** — c'est le motif dominant de la tranche : compter les occurrences avant
de muter (391) · un dénominateur non trié exagère le trou — 393 « angles morts »
dont 359 sont des aides internes (392) · quand un rapport réclame « un analyseur
d'un autre ordre », demander d'abord si l'**exécution** tranche (393) · *une
ancre absente n'est pas un résultat* (394) · *un énoncé faux se corrige
immédiatement là où c'est gratuit, et se verse aux dossiers là où cela coûte au
produit* (395) · *un détecteur qui ne connaît qu'UNE forme du document cherché
fabrique de faux manquants* (397) · *une écriture conditionnelle au réseau
échappe à un recensement fait hors ligne*, et *c'est le témoin positif qui donne
sa valeur à un « 0 »* (399) · **et aujourd'hui même, un `cd` oublié m'a fait
croire six commandes durant que `CLAUDE.md` avait disparu du dépôt : il n'avait
jamais bougé — l'instrument, cette fois, c'était le shell.**

**L'état du produit n'a pas bougé.** Vérifié dans le dépôt : depuis le correctif
XSS du lot **372** (4 fichiers de `vertex/ui/`), la seule modification hors tests
et documentation est **deux corrections de `CLAUDE.md`**, aux lots 381 et 382.
**Sur la tranche 390-399 : zéro.** MD5 des 8 pages servies re-prouvé identique
aux lots **390** et **396**. Dit franchement : **la boucle entretient et vérifie,
elle ne construit plus.**

**LA QUESTION DE FOND, REPOSÉE.** *Aucun GO n'est arrivé depuis le lot 388.* Les
dossiers du **rang 1** — ceux où l'utilisateur voit du faux dans son terminal —
sont tous à l'arrêt : 7 points MSFT fabriqués (388) · scan de démo dans
`breadth_history` (391) · `context()` sur univers vide (379) et « points réels du
scan » (363) · replis `0` de `_followed_count`/`_positions_count` (378) · badge
de provenance IBKR jamais affiché (386). Trois issues :
**(a)** continuer les lots courts — rendement décroissant, et c'est mesuré : deux
des six derniers n'ont trouvé strictement rien ;
**(b) un GO groupé sur le rang 1, puis exécution — RECOMMANDÉ**, en commençant
par la purge des 7 points MSFT (coût quasi nul, risque nul, seule ligne où un
chiffre inventé est aujourd'hui servi comme une mesure) ;
**(c)** arrêter la boucle et attendre — défendable, rien ne se dégrade.
Ce qui ne serait **pas** honnête, c'est de continuer indéfiniment en (a) en
laissant croire que le travail avance sur ce qui compte. Il n'avance pas :
**il attend une décision.**

## BILAN — veille active, lots 380 → 389 (2026-08-09, bilan n°8)

Dix lots. **Vérification refaite, pas rappelée** : **MD5 8/8 identiques** aux
références sur les 8 pages servies · navigateur réel, 8 pages hydratées,
**0 erreur console** · **les 7 gardiens de la tranche rejoués avec une faute
réelle : 7 sur 7 mordent encore**, témoin négatif muet.

### Les chiffres

Suite **2 754 → 2 835** (+81, soit exactement les 81 tests des 7 gardiens
ajoutés) · PR **#412 → #421** toutes fusionnées en squash · SW `td-shell-v187`
**inchangé sur les dix lots** · `main` jamais touchée · **zéro fichier de
production modifié**.

### Cinq trouvailles réelles

1. **381** — le repli de `deskKeys()` **servi** par `/system` n'était couvert par
   aucun test : y retirer une clé passait les 2 754 tests. Constat joint :
   `vx_kit.JS` (21 727 o) n'atteint aucune des 8 pages.
2. **382** — « aucun littéral couleur » était **faux** : 265 littéraux distincts
   dans `vertex/ui/**`, **53 atteignent une page servie**. La règle réellement
   tenue (aucun bleu non-marque) est la bonne ; la doc mentait.
3. **385** — le recensement des replis numériques s'arrêtait à `vertex/` :
   **31 % des handlers de production hors filet**, dont les 101 de `terminal.py`.
4. **387** — **un test pouvait effacer les notes du trader.** `myNotes` est une
   clé synchronisée ; le round-trip desk l'écrasait et restaurait **sans
   `finally`**. Une assertion en échec laissait `{"guard": "lot84-guard-…"}`
   **définitivement**.
5. **388** — **un point GEX fabriqué par jour sur MSFT**, un vrai titre, dans
   `gex_history_cache.json` que `/api/options/gex-radar` **sert**.

Les deux dernières sont d'une autre gravité : elles touchent les **données
réelles de l'utilisateur**, pas la documentation ni la couverture.

### Deux veines fermées par la mesure

**Audit des gardiens par mutation** (381-384) : 27 mutations, 2 trouvailles,
toutes deux dans les 2 premiers lots — fermée sur le rendement, pas la fatigue.
**Écritures runtime** (386-389) : 2 trouvailles ; 5 fichiers touchés au départ,
**4 à l'arrivée, tous sur un simple horodatage** (vérifié feuille à feuille).

### Le fil rouge — huit fois, la faute était dans MES instruments

Périmètre `vertex/` seulement (385) · chaîne présente 4× (386) · périmètre
4 → 15 → 17 fichiers **et un gardien accusant 2 fichiers sains** (387) ·
mutation portant sur le **message** de l'assertion (387) · exemption au fichier
(387) · détecteur rendant « ? », **8 sites comptés pour 12 réels** (388) ·
8 candidats pour **2 écrivains réels**, et **l'anti-vide creux REFAIT** (389) ·
mutation injectée dans une clé de nav jamais rendue (390).

**Avoir la règle écrite ne suffit pas à ne pas la re-violer** — le 389 a refait
mot pour mot la faute du 386. Ce qui l'attrape n'est pas la mémoire, **c'est la
preuve ROUGE**. Et le témoin a une valeur symétrique : au 389 il a mordu, et
c'était lui qui avait tort.

### Ce que la tranche n'a PAS prouvé

Les 81 tests sont **statiques** (ils lisent le code, n'observent pas
l'exécution) · les caractérisations sont **datées** · aucune couverture
exhaustive n'est démontrée · la **pollution historique n'est pas nettoyée**
(7 points MSFT, points SKYX/TSTQ) — donnée utilisateur, décision à prendre.

### Le vrai goulot — 18 dossiers, classés

**Rang 1, l'utilisateur voit du faux** : purge des points MSFT (388) ·
`context()` sur univers vide (379) + « points réels du scan » (363) · replis `0`
de `_followed_count`/`_positions_count` (378) · badge de provenance IBKR (386).
**Rang 2, risque de données** : filet desk option A (362).
**Rang 3, poids mort chiffré** : 604 Ko de `PAGE_*` (374, à trancher **avec** le
badge — elles contiennent son seul rendu) · `vx_kit.JS` (381) · purges É2/É3 et
fonctions de tête.
**Rang 4** : cosmétique, plus `vocab_js` (373) **déconseillé en l'état**.

**Si un seul GO : la purge des points MSFT** — coût quasi nul, risque nul, et
c'est la seule ligne où un chiffre inventé est aujourd'hui servi comme une
mesure.

## BILAN — veille active, lots 370 → 379 (2026-08-08, bilan n°7)

Dix lots de veille autonome sur la veine **sécurité & honnêteté des données**.
Vérifié au lot 380 : **MD5 8/8 identiques** aux références et **0 erreur console**
sur les 8 pages en navigateur réel — *les octets servis n'ont pas bougé d'un bit
sur toute la tranche*. Les **9 gardiens ajoutés ont été rejoués un par un avec une
faute réelle : les 9 mordent encore.**

### Ce que la tranche a apporté

- **Une vraie faille, sérieuse** (lot 372) : `/opportunities` laissait passer les
  valeurs de paramètres d'URL dans un bloc `<script>` via un `json.dumps` nu —
  XSS **déclenchable à distance par un simple lien**, dans une session ayant accès
  au desk local. Trouvée, corrigée, prouvée MD5-neutre, verrouillée.
- **Un danger latent verrouillé** (373) : `vocab_js`, `json.dumps` nu sur les
  8 pages, sûr seulement parce que son contenu est constant — désormais un
  invariant le garantit, sans durcissement inutile.
- **Une myopie de gardien corrigée** (377) : le gardien du 376 ne voyait que
  **13 refus sur 39** — il manquait tous les `return jsonify({...})`, c'est-à-dire
  les refus servis au navigateur. 33 % de couverture, au vert.
- **Deux pistes fermées par la mesure** (375, 376) plutôt que par un faux vert.
- **Chiffres** : suite **2610 → 2754** (+144 tests), jamais rouge · 9 gardiens ·
  **1 seul lot touchant la production** · SW `td-shell-v187` inchangé · 10 PR
  (#402→#411) · `main` jamais touchée.

### Le fil rouge — douze fois où l'outil était en cause, sous cinq formes

1. **L'outil accuse du code sain** (374 ×2, 375, 376) — *un gardien qui crie au
   loup finit désactivé*.
2. **Le périmètre de l'outil ment** (373 : `os.listdir` masquait le producteur
   HTML central ; 377 : `return <Dict>` manquait tous les `jsonify`) — *sous
   quelle ENVELOPPE la chose cherchée se présente-t-elle ?*
3. **L'outil empêche d'INNOCENTER** (378 : `s = 50.0` n'était pas le neutre, la
   fonction rend 76 à vide) — *le raisonnement élégant se vérifie sur valeurs
   réelles, dans les deux sens*.
4. **La borne trop lâche** (378) — *une borne qui absorbe la première régression
   n'est pas une borne*.
5. **La preuve elle-même est fautive** (379) — *un cas qui ne mord pas accuse
   d'abord la preuve*.

### Jugement franc — et il n'est pas flatteur partout

Après le lot 372, **sept lots n'ont trouvé aucune nouvelle faille exploitable** :
uniquement des dangers latents, des caractérisations et des « sain, rien touché ».
Sur la veine sécurité prise seule, **le rendement décroît nettement** — 1 faille
sur 6 lots, puis 0 sur 7. La creuser encore au même rythme donnerait des lots
honnêtes mais maigres.

Ce qui s'est révélé fertile, c'est le **méta-audit** : le lot 377 n'a pas audité
le code mais un **gardien déjà fusionné**. La suite compte **2 754 tests dont
personne n'a vérifié qu'ils voient ce qu'ils prétendent voir** ; un test au vert
qui ne mesure rien est plus dangereux qu'un test absent. C'est la piste
prioritaire de la tranche suivante.

### Le vrai goulot : quatorze dossiers attendent une décision humaine

Plusieurs sont chiffrés à l'unité — **604 Ko de HTML mort assemblés à chaque
import** (374), le **filet desk qui perd le travail de la journée** (362,
option A recommandée), et **deux questions d'honnêteté d'affichage jumelles**
(363 et 379 : sur univers vide, l'application affirme « NEUTRE » et
« participation 0 % » au lieu de dire qu'elle ne sait pas). Ce sont des décisions
produit : l'agent les a mesurées et documentées, il ne peut pas les trancher.
**Ce n'est plus le manque de pistes qui limite, c'est l'attente de ces GO.**

## BILAN — PROGRAMME 100 %, lots 71 → 75 (2026-08-06, bilan n°6)

Directive utilisateur : « Continue à tout développer et quand t'as tout à
100 tu me dis. » — exécuté en 5 lots prouvés, cadence resserrée.
**Le PROGRAMME 100 % est TERMINÉ : tout ce qui est prouvable est prouvé,
gardé par la suite, et vert. Déclaration 100 % faite à l'utilisateur.**

| Mesure | Avant (lot 70) | Après (lot 75) |
|---|---|---|
| Tests verts | 1 694 / 2 skipped | **1 706 / 2 skipped** (+12) |
| Service worker | v123 | **v124** |
| PR fusionnées | — | **5** (#104 → #108) |

### Les 5 lots et leurs verdicts

1. **Hygiène des références** (lot 71) : docstring du gateway IBKR
   citait un gardien INEXISTANT → corrigée (3 vrais gardiens READONLY)
   + contrat « toute référence tests/ citée existe » gardé à vie ;
2. **Performance** (lot 72) : mesures publiées — DCL < 300 ms, 0 doublon,
   vendor 160 kB lazy sur /analysis seul — SAIN + budgets 64 kB gardés ;
3. **Accessibilité** (lot 73) : 4 défauts réels — tickers cliquables
   inutilisables au clavier → tabindex+role + délégué clavier GLOBAL
   Enter/Espace ; re-balayage : 0 défaut sur 8 pages ;
4. **Robustesse** (lot 74) : entrées limites (injection, unicode, 120
   chars, POST malformés) → 0×5xx, 404 API JSON+nosniff, refus honnêtes
   live:false+ts — SAIN, contrat gardé ;
5. **RC FINALE** (lot 75) : suite + audit outillé + responsive + a11y
   re-prouvés sur base fraîche — 0 défaut partout.

Étapes humaines restantes : validation physique (TWS réel, iPhone —
vider le cache pour SW v124) ; merge vers `main` sur accord explicite.

## BILAN — programme AUDIT TOTAL, lots 66 → 70 (2026-08-06, bilan n°5)

Programme demandé par l'utilisateur (« audit totalement complet, tout
cohérent, tous les chiffres, chaque bouton, pousser au maximum ») —
exécuté en 5 volets prouvés. **L'audit total est TERMINÉ : l'application
est cohérente au maximum prouvable.**

| Mesure | Avant (lot 65) | Après (lot 70) |
|---|---|---|
| Tests verts | 1 688 / 2 skipped | **1 694 / 2 skipped** (+6, rouges d'abord) |
| Service worker | v121 | **v123** |
| PR fusionnées | — | **5** (#96 → #100) |

### Les 5 volets et leurs verdicts

1. **Routes** (lot 66) : 137 routes GET balayées — 0×5xx, un seul 400
   structuré ; **incohérence corrigée** : tuile Breadth du briefing sur
   `above50` non étiqueté vs Marchés `>MM200` → canonicalisée + étiquetée
   (preuve : 45 partout, nommé pareil) ;
2. **Vues profondes** (lot 67) : 30 vues × 2 viewports = 60 chargements —
   0 erreur, 0 débordement, 0 texte cassé (NaN/undefined) — SAIN ;
3. **IBKR lecture seule** (lot 68) : 4 verrous indépendants (readonly EN
   DUR, RequestTimeout=45, FORBIDDEN_TOOLS côté IA, config) + refus
   honnêtes prouvés route→UI (« aucun chiffre inventé ») + 34 gardiens —
   SAIN ;
4. **Cohérence fiche ↔ Opportunités** (lot 69) : divergence des moteurs
   DITE aux deux endroits (« un score ne déclenche jamais un ordre ») —
   SAIN ; **lacune corrigée** : scores shortlist sans échelle → « /100 »
   partout ;
5. **États dégradés** (lot 70) : /markets sans scan (10 états vides avec
   action), mémoire vide (branches honnêtes partout) — SAIN.

Invariants tenus sur tout le programme : READONLY absolu, données réelles
uniquement, moteur 0.9.0 jamais touché, `main` intacte. Retour aux RC
périodiques espacées (~30 min).

## BILAN — arc visuel & connexions, lots 51 → 60 (2026-08-05, bilan n°4)

Arc exécuté sur directive utilisateur (« visuel app 2026, esprit IBKR,
plus plus plus » puis « développe jusqu'au lot 60 et arrête-toi seule »).
Chaque chiffre est traçable vers son rapport `SKYLER-LOT-XX.md` et sa
ligne `SKYLER-INDEX.md`. **La boucle autonome est ARRÊTÉE après ce lot.**

| Mesure | Avant (lot 50) | Après (lot 60) |
|---|---|---|
| Tests verts | 1 627 / 2 skipped | **1 670 / 2 skipped** (+43, rouges d'abord) |
| Service worker | v107 | **v116** (9 bumps, 4 gardiens à chaque fois) |
| PR fusionnées | — | **10** (#78 → #87) |
| RC navigateur | — | **7 × GO — 0 défaut** (dont RC finale 8 pages × 3 viewports) |
| Moteur décisionnel | 0.9.0 | **0.9.0 — JAMAIS touché** |

### Livré sur l'arc

- **Signature graphique « app 2026 »** centrale (lots 51-54) : lissage
  monotone (jamais de faux extrêmes), dégradés riches, glow, pastille de
  dernier prix, crosshair de visée, chandeliers lisibles (défaut réel
  d'axe Y corrigé) — TOUT le tronc `chart-core.js` + prix d'Analyse ;
- **Connexions simplifiées** (lot 55) : fil d'Ariane cliquable (serveur
  + SPA, source unique), retour contextuel couvrant les 8 espaces ;
- **Polish prouvé page par page** (lots 56-59) : séries comparées
  contrastées (par la SOURCE palette.py), plus aucune info tronquée,
  ~75 fallbacks d'anciennes palettes purgés (dont 6 oranges bannis et
  2 tokens CSS inexistants qui rendaient RÉELLEMENT l'ancien thème),
  doc /design-system honnête, gardiens PROSPECTIFS transversaux ;
- **RC finale** (lot 60) : suite complète + audit outillé + responsive
  8×3 : 0 défaut ; cycle souverain re-prouvé une dernière fois.

Étapes restantes HUMAINES : validation physique (TWS réel, iPhone) ;
merge vers `main` sur accord explicite uniquement.

## BILAN — travail continu, lots 29 → 48 (2026-08-05, bilan n°3)

Synthèse des 20 lots + 3 RC périodiques livrés en mode continu (« go sans
validation humaine ») depuis la RC du lot 27, à l'intention de la
validation humaine. Remplace le bilan n°2 (lots 29-43) — chaque chiffre
reste traçable vers son rapport `SKYLER-LOT-XX.md` / `SKYLER-RC-…` et sa
ligne dans `SKYLER-INDEX.md`.

| Mesure | Avant (lot 28) | Après (lot 48) |
|---|---|---|
| Tests verts | 1 515 / 2 skipped | **1 627 / 2 skipped** (+112) |
| Moteur décisionnel | 0.8.0 | **0.9.0** (catalyst_kind émis + figé) |
| Service worker | v100 | **v107** (7 bumps, gardiens à jour) |
| RC navigateur | — | **6 × GO — 0 défaut** (dont 3 périodiques) |

### Capacités livrées

- **CYCLE SOUVERAIN COMPLET** (lots 29/42/45/46/47/48) : export intègre
  (`content_sha256` vérifiable hors ligne + `ledger_health` embarqué),
  RESTAURATION par rejeu append-only des TROIS magasins (l'historique
  local gagne toujours, empreinte vérifiée avant toute écriture),
  boutons Exporter/Importer côte à côte dans la carte Mémoire — et le
  cycle entier (export → altération refusée → restauration par le vrai
  bouton) est RE-PROUVÉ en navigateur À CHAQUE RC (lot 48) ;
- **Type de catalyseur figé** (lot 30) : `catalyst_kind` émis par le
  moteur + découpe `by_catalyst_type` en observation (non consommée) ;
- **Chaîne mémoire fermée** (lots 39/40) : badge → cellule (source
  unique d'appartenance) → décisions mesurées hit/miss → post-mortem —
  API JSON + vue HTML lisible (markupsafe prouvé sur contenu hostile) ;
- **Surfaçage UI** (lots 33/35/37) : badges contexte, `LEDGER :
  ANOMALIES` conditionnel, fraîcheur « dernière décision figée (J-N) » ;
- **Santé du ledger** (lot 35) : doublons/orphelins/mélanges de
  versions/corruption — DIT, jamais réparé en silence ;
- **RC courte outillée auto-prouvante** (lots 32/41/48) : 8 pages +
  parcours mémoire + cycle souverain à chaque exécution.

### Robustesse prouvée

- **11 crashs réels corrigés** en refus honnêtes (7 moteurs lot 31,
  4 HTTP 500 lot 34) ; couverture adversariale HTTP complète et exacte
  (lots 31/34/36/43) ;
- **2 défauts réels attrapés UNIQUEMENT par la preuve navigateur** :
  J-1 affiché pour une décision du jour (lot 37) et empreinte cassée au
  round-trip JS `100.0 → 100` (lot 47) — tous deux corrigés avec test
  rouge dédié ; **2 défauts d'outillage** corrigés et dits (lots 40/41).

### Invariants tenus sur les 20 lots

READONLY absolu · données réelles uniquement (absent → n/d) · `main`
jamais touchée · fichiers runtime jamais commités · gardiens prospectifs
· zéro aléatoire moteur · rouge d'abord quand le comportement change ·
preuve navigateur à chaque changement de shell · reports honnêtes dits.

### Étape suivante — dit franchement

Le cycle souverain est FERMÉ et auto-prouvé ; le backlog code est épuisé
en valeur réelle. **La validation humaine physique (TWS réel, pages,
iPhone — réserve n°1 de la RC du lot 27) est l'étape décisive du
programme.** Le mode continu bascule en RC périodiques espacées
(~30 min) — chaque RC re-prouvant suite complète, 8 pages, parcours
mémoire ET cycle souverain.


## Source de vérité

Skill : `.claude/skills/vertex-skyler-v2/SKILL.md`

Références avancées ajoutées :

- `references/DECISION_ENGINE.md`
- `references/ADVERSARIAL_COMMITTEE.md`
- `references/DECISION_PACKET_SCHEMA.md`
- `references/SCENARIO_CALIBRATION.md`
- `references/ANOMALY_INTELLIGENCE.md`

## Phase Core — historique validé

| Étape | Statut | Preuve principale |
|---|---|---|
| Audit convergence | ✅ GO | `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md` |
| Lot 0 — Baseline | ✅ GO | `docs/skyler/BASELINE.md` |
| Lot 1 — Correctness options | ✅ GO | `docs/refactor/validation/SKYLER-LOT-01.md` |
| Lot 2 — Constitution V2 | ✅ GO | `docs/refactor/validation/SKYLER-LOT-02.md` |
| Lot 3 — Market Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-03.md` |
| Lot 4 — News/catalyseurs/anomalies | ✅ GO | `docs/refactor/validation/SKYLER-LOT-04.md` |
| Lot 5 — Skyler Core | ✅ GO | `docs/refactor/validation/SKYLER-LOT-05.md` |
| Lot 6 — Options Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-06.md` |
| Lot 7 — Portfolio Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-07.md` |
| Lot 8 — Neon Glass | ✅ GO | `docs/refactor/validation/SKYLER-LOT-08A.md` à `08E.md` |
| Lot 9 — Calibration infrastructure | ✅ GO infrastructure | `docs/refactor/validation/SKYLER-LOT-09.md` |

État observé avant l’expansion : environ 1 300 tests verts, service worker v94, IBKR READONLY intact, `main` non modifiée.

## Phase Institutional+ — nouvelle expansion

### Gouvernance installée

- [x] moteur de décision institutionnel documenté ;
- [x] comité contradictoire de 12 rôles documenté ;
- [x] Président Skyler unique producteur du verdict final ;
- [x] avocat du diable obligatoire ;
- [x] red-team obligatoire pour S/S+ ;
- [x] schéma canonique `SkylerPacket` défini ;
- [x] scénarios/probabilités/calibration renforcés ;
- [x] intelligence des anomalies renforcée ;
- [x] agents spécialisés installés ;
- [x] runbook et checklist étendus.

### Lots Institutional+

| Étape | Statut | Objectif | Rapport attendu |
|---|---|---|---|
| Lot 10 — Mémoire et discipline décisionnelle | ✅ FAIT — validé (« go sans validation humaine ») et fusionné | décisions immuables, classification des erreurs, biais récurrents, amélioration humaine contrôlée | `docs/refactor/validation/SKYLER-LOT-10.md` |
| Lot 11 — Knowledge Graph institutionnel | ✅ FAIT — en attente de validation | relations sociétés/secteurs/catalyseurs/portefeuille prouvables, propagation explicable, questions de recherche | `docs/refactor/validation/SKYLER-LOT-11.md` |
| Lot 12 — Red-team et RC finale | ✅ FAIT — GO AVEC RÉSERVES (validation physique restante) | stress adversarial, audit math/données/sécurité, release candidate | `docs/refactor/validation/SKYLER-LOT-12.md` |

## Agents Institutional+

- `.claude/agents/skyler-chair.md`
- `.claude/agents/skyler-devils-advocate.md`
- `.claude/agents/skyler-market-regime.md`
- `.claude/agents/skyler-options-risk.md`
- `.claude/agents/skyler-data-auditor.md`
- `.claude/agents/skyler-portfolio-risk.md`

Aucun sous-agent ne peut publier `final_decision`. Le Président Skyler est l’unique source canonique.

## Décisions établies

- `main` ne bouge pas sans accord explicite.
- Neon Glass/Skyler reste la base fonctionnelle.
- Une invocation Claude = une mission ou un lot.
- Aucun lot Institutional+ ne commence sans validation du précédent.
- Les calculs et décisions canoniques restent déterministes.
- Claude rédige mais ne crée ni ne modifie les chiffres.
- IBKR reste strictement READONLY.
- Aucune note S/S+ sans red-team indépendante.
- Aucune recalibration ou modification de Constitution automatique.

## Lot 10 — livré (2026-08-05)

- moteur `vertex/engines/decision_memory.py` : ledger immuable par version de
  moteur (gel de 31 champs), anti-look-ahead par empreinte de série, résultats
  aux horizons déclarés (5/20/60 séances, catalyseur estimé étiqueté, thèse et
  option honnêtement NON_APPLICABLE), taxonomie d'erreurs déterministe,
  10 biais surveillés, recommandations `EN_ATTENTE_VALIDATION_HUMAINE` ;
- routes : gel fail-safe dans `/api/skyler/<sym>` + `GET /api/skyler/memory` ;
- persistance runtime `skyler_memory.json` (gitignorée, bornée) ;
- 1332 tests verts / 2 skipped (+32) ; SW inchangé v94 (aucune UI touchée) ;
- interdictions respectées : pas de Knowledge Graph, pas d'UI, pas de
  modification automatique des poids/Constitution, `main` intacte, aucun ordre.

## Lot 11 — livré (2026-08-05)

- moteur `vertex/engines/knowledge_graph.py` : 4 relations prouvables
  (secteur F1 sourcé, co-mouvement F2 fenêtré, catalyseur daté F1, détention
  desk F1), provenance obligatoire par arête, propagation explicable saut par
  saut, dépendances cachées ≥ 2 liens indépendants, questions de recherche
  `NON_DOCUMENTE` — fournisseurs/clients/concurrents JAMAIS inventés ;
- routes lecture seule : `GET /api/skyler/graph` + `GET /api/skyler/graph/<sym>` ;
- 1350 tests verts / 2 skipped (+18) ; SW inchangé v94 (aucune UI touchée).

## Lot 12 — livré (2026-08-05)

- règle red-team du comité appliquée par le moteur : S/S+ sans red-team
  complétée = plafonné à A — `ENGINE_VERSION` 0.1.0 → **0.2.0** (règle changée
  = version changée), historique 0.1.0 séparé en mémoire, Constitution
  intouchée (proposition de gate profil V3 documentée, en attente humaine) ;
- trouvaille adversariale corrigée : NaN/infini refusés par la mémoire ;
- batterie adversariale : séries hostiles, prix extrêmes, attaque look-ahead,
  déterminisme, labels hostiles, verbes d'ordre, fichiers runtime/secrets,
  performance bornée — 17 tests ;
- 1367 tests verts / 2 skipped (+17) ; SW v94 inchangé.

## Lot 13 — livré (2026-08-05, travail continu autorisé)

- moteur **0.3.0** : `operational_state` déterministe (8 états DECISION_ENGINE
  §2.2, base explicite, jamais une décision finale) + `confidence` factorisée
  §7 (4 facteurs bornés avec base, plafonds UNKNOWN ≤ 0,55 / conflit ≤ 0,50 /
  contradiction ≤ 0,60, calibration figée à 0,50 sans historique — jamais
  100 %) ;
- le ledger mémoire fige désormais ces champs (31/31 champs vivants) ;
- 1386 tests verts / 2 skipped (+19).

## Lot 14 — livré (2026-08-05, travail continu)

- moteur **0.4.0** + `vertex/engines/red_team.py` (1.0.0) : les 10 questions
  d'ADVERSARIAL_COMMITTEE §8 évaluées depuis les données réelles du packet —
  réponse fondée (F1/F2, données citées) ou UNANSWERED avec raison, jamais
  inventée ; `complete=True` seulement à 10/10 ; revue servie dans
  `/api/skyler/<sym>` (`red_team_review`) et injectée dans la décision ;
- le chemin S/S+ a désormais sa clé — mais reste fermé par les blocs
  insuffisants tant que les fondamentaux ne sont pas branchés (voulu) ;
- 1398 tests verts / 2 skipped (+12).

## Lot 15 — livré (2026-08-05, travail continu)

- `vertex/engines/session_log.py` : UNE clôture par symbole et par jour de
  scan RÉEL (date d'observation UTC, jamais inventée ; dédup par date ; borné ;
  NaN/dates malformées refusés) — `skyler_sessions.json` runtime gitignoré ;
- la mémoire fige `session_date` et les horizons 5/20/60 comptent des séances
  RÉELLES (log autoritaire, empreinte de série en secours pour les anciens
  records) — limite n° 1 du lot 10 levée ;
- 1410 tests verts / 2 skipped (+12).

## Lot 16 — livré (2026-08-05, travail continu)

- surfaçage UI : carte « Mémoire décisionnelle » sur Performance (ledger par
  version de moteur, biais badgés, propositions en attente humaine, état vide
  honnête) + section « Dépendances cachées » sur Portefeuille → Risque
  (paires ≥ 2 liens, questions de recherche) ;
- SW **v95** + 4 gardiens à jour ; preuve navigateur 390/1440 : 0 erreur
  console, 0 overflow, captures `docs/skyler/baseline/lot16-*.png` ;
- 1416 tests verts / 2 skipped (+6).

## Lot 17 — livré (2026-08-05, travail continu)

- co-mouvement du graphe en **corrélation partielle** (résidus OLS vs SPY,
  `method: residual_vs_SPY` + R² par titre) — le faux co-mouvement « les deux
  suivent le marché » est filtré (prouvé par test) ; sans SPY, fallback
  `method: raw` ÉTIQUETÉ + limite dite, jamais silencieux ; SPY exclu des
  paires ;
- `hidden_groups` : composantes connexes ≥ 3 titres synthétisées dans l'API
  et affichées sur Portefeuille → Risque ;
- SW **v96** + gardiens (lot 16 rendu prospectif ≥ 95) ; navigateur 390/1440 :
  0 erreur console, captures lot17-*.png ;
- 1427 tests verts / 2 skipped (+11).

## Lot 18 — livré (2026-08-05, travail continu)

- moteur **0.5.0** : `robustness` MESURÉE par analyse de perturbation — 11
  variations fixes documentées (score ±10, R:R ±0,5, régime ±0,2, un contexte
  retiré à la fois), fraction stable bornée, bascules listées, non applicable
  exclu (jamais compté stable) ; cœur de verdict partagé anti-divergence ;
  aucun aléatoire (gardien) ; prouvé : un ACHETER frontière bascule sous
  −10 points techniques (fragilité détectée) ;
- 1438 tests verts / 2 skipped (+11) ; SW v96 inchangé.

## Lot 19 — livré (2026-08-05, travail continu)

- moteur **0.6.0** : la boucle décision → mémoire → confiance est FERMÉE —
  `calibration_factor` = scenario hit rate des résultats MESURÉS de la mémoire
  pour la version courante uniquement (0,50 + 0,40 × hit rate, borné
  [0,50, 0,90], jamais 1,0) ; échantillon < 20 mesures → 0,50 « insuffisant »,
  jamais inventé ; route fail-safe ; versions jamais mélangées (testé) ;
- 1450 tests verts / 2 skipped (+12) ; SW v96 inchangé.

## Lot 20 — livré (2026-08-05, travail continu)

- drill-down `GET /api/skyler/memory/<decision_id>` : record figé complet +
  résultat mesuré + **post-mortem déterministe** (classification par horizon,
  scénario ayant contenu le résultat : HORS_FOURCHETTE_BASSE / PESSIMISTE /
  PROBABLE / EXCEPTIONNEL_ATTEINT, MFE/MAE, résumé) — honnête si rien n'est
  mesuré, discipline jamais devinée ; 404 structuré sur id inconnu ;
- carte Mémoire : tableau « Dernières décisions figées » avec lien détail ;
  SW **v97** + gardiens prospectifs ; navigateur 390/1440 : 0 erreur console ;
- 1463 tests verts / 2 skipped (+13).

## Lot 21 — livré (2026-08-05, travail continu)

- red-team **1.1.0** : Q05 chiffrée (repricing Black-Scholes CANONIQUE du
  candidat à IV −10 pts — en démo réelle : « IV 34 % → 24 % : −30,6 % », F3
  avec modèle et hypothèses) ; Q08 en grille stop/TP2/TP3 × IV −10/0/+10 avec
  convexité vs action ; fallbacks F2 et UNANSWERED intacts ; entrées invalides
  jamais chiffrées ; cas manuel BS gardé par test (ATM 1 an vol 20 % ≈ 7,97 %) ;
- 1472 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 22 — livré (2026-08-05, travail continu)

- moteur **0.7.0** : calibration PAR CONTEXTE (§13) — découpe par niveau et
  par décision, chaque cellule avec son propre hit rate seulement si ≥ 20
  mesures (sinon INSUFFISANT dit, valeur None) ; sélection à portée explicite
  contextuel → global → 0,50 ; la route sert la cellule du niveau courant
  (prouvé bout en bout : cellule REFUS_WATCH 0,90 servie au moteur) ;
  `/api/skyler/memory` expose la découpe ; versions jamais mélangées ;
- 1481 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 23 — livré (2026-08-05, travail continu)

- vue lisible `GET /memory/<decision_id>` : record figé, résultat mesuré et
  post-mortem rendus dans le shell produit — contenu de la mémoire ÉCHAPPÉ
  serveur (XSS testé avec script hostile), états honnêtes, 404 lisible ;
  lien de la carte Mémoire mis à jour ; SW **v98** ; parcours prouvé en
  navigateur (clic carte → vue, 0 erreur console) ;
- **`docs/refactor/validation/SKYLER-INDEX.md`** : index consolidé des lots
  10 → 23 (objectifs, versions moteur/SW, tests, verdicts) + architecture ;
- 1488 tests verts / 2 skipped (+7).

## Lot 24 — livré (2026-08-05, travail continu)

- `sector_exposure` dans le graphe : positions réelles agrégées par secteur
  déclaré, poids en % SEULEMENT si toutes les positions sont cotées (sinon
  None avec raison — jamais estimé), hors watchlist étiqueté ; groupes cachés
  mono-secteur flaggés **CONCENTRATION SECTORIELLE** ; affiché sur
  Portefeuille → Risque ; SW **v99** ; navigateur prouvé (0 erreur console) ;
- 1498 tests verts / 2 skipped (+10).

## Lot 25 — livré (2026-08-05, travail continu)

- revue de simplification SANS changement de comportement (suite identique
  1498/2, aucun test modifié) : docstrings resynchronisées sur 0.7.0,
  formule de calibration unique (`_hit_factor`), boucle de mesure réutilisée
  (`_measured_hits`), fallbacks red-team dédupliqués ; dette restante
  documentée et assumée.

## Lot 26 — livré (2026-08-05, travail continu)

- moteur **0.8.0** : calibration par RÉGIME — le record mémoire fige le label
  du régime au moment de la décision (None honnête, anciens records
  compatibles) ; découpe `by_regime` (mêmes règles d'échantillon, régime
  inconnu ≠ cellule) ; sélection prioritaire documentée niveau → régime →
  global avec portée explicite ; route passe le régime courant ; badges de
  calibration par contexte dans la carte Mémoire (masqués sans mesures —
  honnête) ; SW **v100** ;
- 1508 tests verts / 2 skipped (+10).

## Lot 27 — livré (2026-08-05, RC courte du travail continu)

- AUDIT complet des lots 13 → 26 (aucun code moteur) : 8 espaces en 200 aux
  deux tailles, 0 overflow, 0 erreur JS applicative (client-log = 0 ; les
  resets du tour = requêtes coupées par la navigation + Google Fonts
  injoignable dans la sandbox — investigué, documenté) ; 9 endpoints Skyler
  en 200 avec versions cohérentes (décision 0.8.0, red-team 1.1.0 complète,
  graphe 0.1.0 distinct) ; sécurité propre (no_orders, aucun runtime/secret
  suivi, aucun verbe d'ordre, readonly intact) ;
- verdict **GO AVEC RÉSERVES** — réserve n° 1 inchangée : validation humaine
  sur appareil physique ; bilan : +141 tests depuis le lot 12, moteur
  0.2.0 → 0.8.0, SW v94 → v100, 4/4 facteurs de confiance mesurés.

## Lot 28 — livré (2026-08-05, travail continu)

- `by_catalyst` dans la calibration par contexte : cellules avec/sans
  catalyseur dérivées du ledger existant, mêmes règles d'échantillon —
  découpe d'OBSERVATION uniquement, jamais consommée par la sélection
  (aucun bump moteur, prouvé par test) ;
- propagation du graphe 1–3 sauts (`?hops=`, clampé) avec garde de volume
  dure MAX_PATHS=200 — troncature déterministe et TOUJOURS DITE ;
- 1515 tests verts / 2 skipped (+7) ; SW v100 inchangé (API seulement).

## Lot 29 — livré (2026-08-05, travail continu)

- `GET /api/skyler/memory/export` : bundle JSON lecture seule (mémoire +
  séances + journal + versions moteur/schéma, horodatage UTC réel,
  `Content-Disposition` téléchargement) — l'historique décisionnel
  devient SOUVERAIN (les fichiers runtime sont gitignorés/périssables) ;
- lecture seule PROUVÉE (octets identiques avant/après l'appel) ;
  magasins vides → formes vides honnêtes ;
- bouton « Exporter → » dans la carte Mémoire (Performance) ; SW v101 ;
- 1522 tests verts / 2 skipped (+7) ; moteur 0.8.0 inchangé.

## Lot 30 — livré (2026-08-05, travail continu)

- `catalyst_kind` émis par le moteur (0.9.0) : le `kind` EXPLICITE
  (`earnings`/`macro`/`news`…) du même événement daté le plus proche qui
  produit `catalyst` — fait du moteur events, source unique, jamais
  re-parsé depuis le label ; figé au freeze (ancien record → None
  honnête, jamais rétroactif) ;
- découpe `by_catalyst_type` dans la calibration par contexte — mêmes
  règles d'échantillon, bucket `inconnu` honnête, OBSERVATION uniquement
  (non-consommation par la sélection prouvée par test) ;
- 1531 tests verts / 2 skipped (+9) ; SW v101 inchangé (moteur/API).

## Lot 31 — livré (2026-08-05, travail continu)

- batterie de fuzz DÉTERMINISTE (listes fixes, zéro aléatoire) sur les
  chemins des lots 26–30 : propagate, calibration (globale/contexte/
  sélection), freeze + catalyst_kind, export souverain ;
- **7 crashs réels trouvés** (TypeError unhashable, AttributeError sur
  magasins corrompus) et corrigés en REFUS HONNÊTES : nœud/contexte/kind
  non-chaîne → []/scope global/bucket `inconnu`, entrées de magasin
  non-dict ignorées, garde MAX_PATHS jamais désactivée ;
- aucun bump de version (aucune règle ne change sur données valides —
  prouvé par la suite inchangée) ; SW v101 inchangé ;
- 1543 tests verts / 2 skipped (+12).

## Lot 32 — livré (2026-08-05, travail continu)

- RC courte OUTILLÉE : `tools/rc_short_audit.js` (Playwright, versionné,
  ré-exécutable en périodique) — 8 espaces canoniques, 0 erreur console
  au repos, 0 pageerror, HTTP 200 partout, `/healthz` 200,
  `/api/client-log` à 0, SW `td-shell-v101` servi ;
- vérification live du chemin neuf : `/api/skyler/memory/export` → 200 +
  Content-Disposition téléchargement ;
- verdict **GO — 0 défaut produit** ; la validation sur appareil physique
  (TWS réel) reste l'étape humaine (réserve n°1 du lot 27, inchangée) ;
- 1543 tests verts / 2 skipped (inchangé — audit sans changement de
  comportement) ; SW v101 inchangé.

## Lot 33 — livré (2026-08-05, travail continu)

- carte Mémoire : les découpes d'OBSERVATION `by_catalyst` et
  `by_catalyst_type` rejoignent les badges de calibration par contexte —
  MÊME mécanique que niveau/régime/décision (une seule boucle, gardé par
  test), libellé explicite « catalyseur/type = observation, jamais
  consommés » ;
- SW v101 → v102 + 4 gardiens ; preuve navigateur : RC courte
  (tools/rc_short_audit.js) GO — 8 pages, 0 erreur console, client-log 0,
  v102 servi ; en démo 0 cellule mesurée → aucun badge (honnête, lot 26) ;
- 1547 tests verts / 2 skipped (+4) ; moteur 0.9.0 inchangé.

## Lot 34 — livré (2026-08-05, travail continu)

- batterie de fuzz HTTP à listes FIXES sur les routes graphe/mémoire :
  ?hops= dégénérés (clamp 1..3 toujours appliqué, troncature toujours
  dite), symboles/ids dégénérés (404 structuré, jamais nu), traversée
  (jamais un fichier système), XSS (id hostile jamais réfléchi brut) ;
- **4 crashs 500 réels trouvés** sur magasin mémoire corrompu (passe de
  mesure, find_decision/find_outcome, detect_patterns, aggregates) et
  corrigés : entrées non-dict ignorées, entrées valides toujours
  servies — refus honnête, jamais 500 ;
- aucun bump de version (données valides inchangées) ; SW v102 inchangé ;
- 1555 tests verts / 2 skipped (+8).

## Lot 35 — livré (2026-08-05, travail continu)

- `decision_memory.ledger_health` : contrôle de cohérence du ledger
  multi-versions — doublons d'id, outcomes orphelins, mélanges de
  versions décision/outcome, entrées corrompues ; statut SAIN/ANOMALIES
  avec basis chiffrée ; le contrôle DIT, ne répare JAMAIS (l'historique
  original gagne) ; robuste aux mémoires dégénérées d'entrée ;
- servi dans `/api/skyler/memory` (`ledger_health`) ; badge rouge
  « LEDGER : ANOMALIES » dans la carte Mémoire SEULEMENT si anomalie ;
- SW v102 → v103 + 4 gardiens ; RC courte GO (8 pages, 0 erreur,
  client-log 0, v103 servi) ; vérif live : status SAIN ;
- 1565 tests verts / 2 skipped (+10) ; moteur 0.9.0 inchangé.

## Lot 36 — livré (2026-08-05, travail continu)

- batterie de fuzz à listes FIXES sur `/api/skyler/<sym>` (le cœur
  décisionnel HTTP) : 14 symboles dégénérés, 6 corruptions de magasins
  (une par une puis simultanées, double appel dédupliqué), honnêteté du
  titre inconnu (blocs INSUFFISANTS, jamais un achat sans données),
  déterminisme, calibration fail-safe 0,50 — magasins réels jamais
  touchés (fixture isolée) ;
- **0 défaut produit** : la route était déjà robuste (gardes lots 31/34
  + hooks fail-safe) ; le contrat de réponse `{symbol, decision:{…},
  packet, red_team_review, demo}` est désormais DOCUMENTÉ par les tests ;
- couverture HTTP adversariale complète des chemins Skyler ;
- 1572 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v103 inchangés.

## Lot 37 — livré (2026-08-05, travail continu)

- carte Mémoire : fraîcheur du ledger dans l'en-tête — « dernière
  décision figée : YYYY-MM-DD (J-N) », trois états honnêtes (ledger vide
  → « aucune décision figée », date absente → n/d, date réelle → J-N en
  différence de dates calendaires UTC, J-0 = aujourd'hui) ;
- **défaut réel attrapé par la preuve navigateur** : la première version
  affichait J-1 pour une décision d'aujourd'hui (arrondi d'heures) —
  corrigé en différence de minuits UTC, re-vérifié live « J-0 » ;
- SW v103 → v104 + 4 gardiens ; RC courte GO (8 pages, 0 erreur,
  client-log 0, v104 servi) ;
- 1576 tests verts / 2 skipped (+4) ; moteur 0.9.0 inchangé.

## Lot 39 — livré (2026-08-05, travail continu)

- drill-down cellule de calibration : `decision_memory.cell_decisions` —
  les décisions MESURÉES qui composent une cellule (id, titre, séance,
  contextes figés, hit/miss), avec la règle d'appartenance extraite en
  SOURCE UNIQUE (`_cell_key`, consommée par calibration_by_context ET le
  drill-down — anti-divergence prouvée sur toutes les cellules
  publiées) ;
- route `GET /api/skyler/memory/cell/<group>/<key>` : 404 structurés
  (groupe_inconnu avec liste des groupes, cellule_inconnue), résumé de
  cellule joint, jamais 500 ; badges de la carte Mémoire cliquables ;
- SW v104 → v105 + 4 gardiens ; RC courte GO (v105 servi) + 404 live
  vérifiés ; 1586 tests verts / 2 skipped (+10) ; moteur 0.9.0 inchangé.

## Lot 40 — livré (2026-08-05, travail continu)

- vue HTML lisible d'une cellule de calibration : `/memory/cell/<group>/
  <key>` — résumé (facteur, hit rate, n, basis), table des décisions
  MESURÉES avec hit/miss honnêtes et lien post-mortem par record,
  404 lisibles ; markupsafe PROUVÉ sur contenu hostile figé (affiché
  échappé, jamais exécuté ni caché) ; la vue lit `cell_decisions`
  (source unique lot 39), ne recalcule rien ;
- badges de la carte Mémoire → vue lisible (l'API JSON reste servie
  pour l'audit) ; boucle complète : badge → cellule → record →
  post-mortem ;
- SW v105 → v106 + 4 gardiens ; RC courte GO (v106 servi) + 404 live ;
- 1593 tests verts / 2 skipped (+7) ; moteur 0.9.0 inchangé.

## Lot 41 — livré (2026-08-05, travail continu)

- `tools/rc_short_audit.js` étendu au PARCOURS MÉMOIRE : après les
  8 pages, l'audit fige une décision démo (/api/skyler/AAPL), vérifie
  `/memory/<id>` en vrai navigateur (200, « Décision figée », 0 erreur
  console) puis la vue cellule — cellule existante → 200, sinon le 404
  LISIBLE est vérifié et DIT (démo : aucune cellule mesurée, honnête) ;
- défaut d'OUTIL trouvé et corrigé : innerText reflète la casse CSS
  (uppercase) → comparaison insensible à la casse, documentée ;
- RC courte GO — 0 défaut produit ; 1593 tests verts / 2 skipped
  (inchangé — outil seulement) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 42 — livré (2026-08-05, travail continu)

- intégrité de l'export souverain : le bundle embarque `ledger_health`
  calculé AU MOMENT de l'export (l'archive dit elle-même si le ledger
  était cohérent — un magasin corrompu est fidèlement empreinté et son
  incohérence DITE, jamais maquillée) et `content_sha256` (sha256 du
  JSON canonique, clés triées — vérifiable HORS LIGNE sans le serveur,
  méthode documentée dans la note du fichier même) ;
- lecture seule stricte re-prouvée (octets identiques) ; gardiens de
  l'export lot 29 verts inchangés ; biais par type de catalyseur
  vérifié et REPORTÉ honnêtement (aucune information nouvelle sans
  échantillons mesurés réels) ;
- 1599 tests verts / 2 skipped (+6) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 43 — livré (2026-08-05, travail continu)

- fuzz à listes FIXES des DEUX routes cellule (JSON + HTML, postérieures
  à la batterie du lot 34 — trou de couverture fermé) : traversée
  percent-encodée, 500 chars, XSS, unicode NFD, groupes dégénérés,
  traversée brute ; **0 défaut** — gardes des lots 31/34/39/40 déjà
  couvrantes ;
- non-interférence prouvée (cellule réelle servie entre deux salves
  hostiles) ; pas de normalisation cachée (clé NFD ≠ cellule NFC, 404) ;
- l'affirmation « couverture adversariale HTTP complète » (lot 36) est
  désormais exacte (lots 31/34/36/43) ;
- 1606 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 45 — livré (2026-08-05, développement repris sur directive utilisateur)

- restauration souveraine : `POST /api/skyler/memory/import` — l'export
  a désormais un chemin de retour ; `content_sha256` VÉRIFIÉ AVANT toute
  écriture (archive altérée → 400 dit, rien touché) ;
- `merge_memory` : REJEU APPEND-ONLY — un decision_id existant n'est
  JAMAIS remplacé (l'historique local gagne, prouvé contre archive
  falsifiée), outcomes monotones, entrées corrompues comptées ;
- périmètre honnête : ledger mémoire uniquement (séances/journal au
  backlog, dit dans la réponse) ; round-trip export→import prouvé ;
- 1615 tests verts / 2 skipped (+9) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 46 — livré (2026-08-05, développement continu)

- restauration ÉTENDUE : le même bundle restaure désormais les TROIS
  magasins (mémoire + séances + journal) — périmètre partiel du lot 45
  complété, le mot « backlog » a disparu de la note (gardé par test) ;
- `session_log.merge_log` : seules les séances (symbole, date) absentes
  sont ajoutées — la clôture LOCALE n'est jamais remplacée (filtrage
  AVANT rejeu, car record_close seul aurait laissé l'archive écraser) ;
- `skyler_journal.merge_journal` : même triple de dédup que `record`
  (source unique), l'entrée locale gagne, borné MAX_ENTRIES ;
- empreinte vérifiée avant TOUTE écriture : falsification → 400 et
  AUCUN des trois magasins écrit (prouvé) ; stats par magasin ;
- 1622 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 47 — livré (2026-08-05, développement continu)

- bouton « Importer ← » à côté d'« Exporter → » dans la carte Mémoire :
  FileReader → POST import → affichage HONNÊTE des deux chemins (stats
  exactes par magasin avec « la donnée locale gagne », ou l'erreur
  serveur telle quelle — jamais maquillée) ; XSS échappé, apostrophes
  en entités ;
- **DÉFAUT RÉEL attrapé par la preuve navigateur** : JSON.stringify
  replie 100.0 → 100, l'empreinte canonique ne matchait plus au
  round-trip JS (invisible aux tests Python) — corrigé par
  `_canonical_bundle_json` (source unique export+import, flottants
  entiers normalisés, recette documentée dans le bundle), test rouge
  dédié simulant le round-trip ;
- SW v106 → v107 + 4 gardiens ; preuve navigateur : upload du VRAI
  fichier → « Restauration terminée … ledger : SAIN », 0 erreur
  console ; RC courte GO (v107 servi) ;
- 1627 tests verts / 2 skipped (+5) ; moteur 0.9.0 inchangé.

## Lot 48 — livré (2026-08-05, développement continu)

- CYCLE SOUVERAIN dans la RC outillée (`tools/rc_short_audit.js`) :
  chaque RC exporte le bundle, prouve le REFUS d'une copie altérée
  (400 empreinte_invalide exigé) puis la RESTAURATION via le VRAI
  bouton « Importer » (setInputFiles — le chemin utilisateur, pas un
  raccourci d'API), message « Restauration terminée … ledger SAIN »
  exigé ;
- rationale : le mécanisme le plus critique du desk (survie de
  l'historique) est re-prouvé à CHAQUE RC — 2 défauts réels n'avaient
  été visibles qu'en navigateur (J-1 lot 37, empreinte JS lot 47) ;
- exécuté : GO — 0 défaut ; 1627 tests verts / 2 skipped (inchangé —
  outil seulement) ; moteur 0.9.0 et SW v107 inchangés.

## Lot 50 — livré (2026-08-05, axe optimisation — demande utilisateur)

- profilage OUTILLÉ (`tools/profile_hot_routes.py`, reproductible) :
  p50/p95 des 5 routes chaudes + 8 pages — **toutes sous 15 ms p95**
  (seuil « RAS » fixé d'avance : 100 ms) ;
- hypothèse du double build_packet/score40 dans `/api/skyler/<sym>` :
  VÉRIFIÉE (0,667 ms/appel) puis RELATIVISÉE — 7,4 % d'un decide à
  9 ms dont l'essentiel est l'analyse de perturbation PAR CONSTRUCTION
  (robustesse mesurée, pas du gaspillage) ; route entière ~14 ms ;
- **décision documentée : NO-GO pour le lot d'optimisation** (gain ~1 ms
  imperceptible vs risque de toucher le cœur décisionnel) — l'axe
  optimisation est épuisé en valeur réelle, baseline chiffrée publiée
  pour re-mesurer si la latence réelle dégrade un jour ;
- 1627 tests verts / 2 skipped (inchangé) ; moteur 0.9.0 et SW v107
  inchangés ; retour aux RC périodiques espacées.

## Lot 51 — livré (2026-08-05, axe visuel — direction utilisateur)

- direction utilisateur : graphiques niveau app de courtage 2026 (esprit
  app IBKR) — livré CENTRALEMENT dans `chart-core.js` (`C.area`) : toutes
  les cartes `areaCard` upgradées d'un coup, zéro fork de renderer ;
- signature : lissage `cubicInterpolationMode 'monotone'` (ne dépasse
  JAMAIS les données réelles — pas de faux extrêmes), dégradé d'aire
  3 arrêts, glow subtil (`vxGlow`), pastille de dernier prix (`vxLastDot` :
  halo + point sur le dernier point RÉEL + pilule de prix au bord droit),
  ligne 2 px, survol mode index ;
- palette : AUCUN littéral couleur nouveau (gardien à inventaire exact) —
  `C.colors` + suffixes alpha sur la couleur reçue (idiome existant) ;
- preuves : 6 tests rouges→verts ; suite 1633/2 skipped ; RC outillée GO
  0 défaut sous SW v108 (cycle souverain inclus) ; preuve navigateur
  visuelle (capture /markets : pastille « 413,00 » rendue, roundRect
  supporté, 0 erreur console) ; moteur 0.9.0 inchangé.

## Lot 52 — livré (2026-08-05, axe visuel — suite)

- CROSSHAIR type app de courtage, central dans `chart-core.js` : plugin
  `vxCrosshair` (ligne de visée verticale pointillée suivant le point
  ACTIF du tooltip — jamais dessinée hors survol — + point surligné),
  câblé par défaut dans `C.area`, désactivable ;
- `C.multiLine` HARMONISÉ sur la signature 2026 du lot 51 : lissage
  monotone (jamais de faux extrêmes), ligne 2 px, crosshair ;
- palette : AUCUN littéral couleur nouveau (même gardien à inventaire
  exact que lot 51) ; le crosshair ne fait que POINTER un point réel ;
- preuves : 5 tests rouges→verts ; suite 1638/2 skipped ; RC outillée GO
  0 défaut sous SW v109 (cycle souverain inclus) ; preuve navigateur au
  SURVOL RÉEL (visée + point actif + tooltip + pastille lot 51 rendus,
  0 erreur console) ; moteur 0.9.0 inchangé.

## Lot 53 — livré (2026-08-05, axe visuel — suite)

- les trois primitives restantes de `chart-core.js` rejoignent la
  signature 2026 (livraison centrale, zéro fork) : `C.sparkline`
  (monotone + mini-aire dégradée, muette), `C.bars` (coins arrondis
  complets, translucides → pleines au survol, alpha appliqué SEULEMENT
  aux hex 6 digits — garde regex, jamais de couleur corrompue),
  `C.donut` (arcs arrondis espacés, hoverOffset, cutout 70 %) ;
- le tronc commun est maintenant ENTIÈREMENT sur la signature 2026
  (area/multiLine/sparkline/bars/donut + vxGlow/vxLastDot/vxCrosshair) ;
- preuves : 5 tests rouges→verts ; suite 1643/2 skipped ; RC outillée GO
  0 défaut sous SW v110 (cycle souverain inclus) ; l'état démo n'affiche
  ni donut ni bars (dit) → preuve par HARNAIS sur les primitives
  réellement servies dans la vraie page (capture, 0 erreur console) ;
  moteur 0.9.0 inchangé.

## Lot 54 — livré (2026-08-05, axe visuel — arc « jusqu'au lot 60 »)

- `price-chart.js` (graphique PRINCIPAL de la fiche Analyse) : signature
  2026 complète — monotone, 2 px, dégradé 3 arrêts, glow, visée,
  pastille de dernier prix ; plan moteur et earnings conservés ;
- `candlestick-chart.js` (repli honnête) : mèches 1 px, corps arrondis,
  visée ; DÉFAUT RÉEL attrapé en preuve navigateur — axe Y forcé à 0
  écrasait les bougies (échelle 0-150 pour des prix ~100) → corrigé
  (`beginAtZero:false` + grace 5 %), test rouge figé ;
- equity/drawdown héritent déjà via `C.area` (dit) ; candlestick-lwc
  (moteur LWC pro) inchangé (dit) ; aucun littéral hex nouveau ;
- preuves : 7 tests rouges→verts ; suite 1650/2 skipped ; RC outillée GO
  0 défaut sous SW v111 ; harnais navigateur : pastille « 110,40 »,
  bougies lisibles échelle 95-115, visée + tooltip OHLC (capture) ;
  moteur 0.9.0 inchangé.

## Lot 55 — livré (2026-08-05, arc « jusqu'au lot 60 » — connexions)

- audit honnête d'abord : l'infrastructure de connexions était déjà bonne
  (openAnalysis + délégation globale + contexte + tuiles KPI en liens) —
  deux trous RÉELS trouvés et fermés centralement ;
- fil d'Ariane CLIQUABLE : « Vertex » → `/`, segment d'espace → racine de
  l'espace — rendu serveur (`_topbar`, href depuis PRIMARY_NAV) ET crumb
  reconstruit par le routeur SPA (href dérivé du menu latéral rendu,
  zéro duplication) ; CSS survol discret ;
- retour contextuel §15 complété : les 8 espaces canoniques couverts
  (`/options` et `/journal` manquaient — chemin brut affiché avant) ;
- preuves : 5 tests rouges→verts ; suite 1655/2 skipped ; RC outillée GO
  0 défaut sous SW v112 ; parcours navigateur RÉEL : fiche AAPL → clic
  « Analyse » → /analysis ; crumb SPA (MSFT) garde ses liens ; 0 erreur
  console ; moteur 0.9.0 inchangé.

## Lot 56 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 1/4)

- inspection réelle d'abord (captures 1440+390, audit débordements : 0,
  0 erreur console) — deux défauts RÉELS corrigés, rien de gratuit ;
- séries comparées : les 3 premiers gris-blancs de SERIES étaient
  indistinguables sur « Indices — performance comparée » → réordonné
  marque/cyan technique/sable/violet/jaune/gris via la SOURCE
  (`palette.py`, constante TECHNICAL nommée) + miroirs thème JS et
  chart-core alignés — le gardien de cohérence a attrapé l'essai
  JS-seul, la source a été alignée, pas contournée ; zéro littéral
  nouveau ; non-bleu vérifié pour le garde-fou ;
- crumb mobile : slash orphelin (racine masquée, séparateur restant) →
  séparateur adjacent masqué avec elle ;
- preuves : 3 tests rouges→verts ; suite 1658/2 skipped ; RC outillée GO
  0 défaut sous SW v113 ; captures APRÈS (4 séries distinctes, crumb
  mobile propre vérifié programmatiquement) ; moteur 0.9.0 inchangé.

## Lot 57 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 2/4)

- inspection réelle (6 captures, audit : 0 débordement, 0 erreur
  console) — verdict honnête : pages SAINES (table mobile défile
  conformément, pairs déjà cliquables, états vides honnêtes) ;
- deux défauts réels de la fiche corrigés : libellés clé/valeur tronqués
  par ellipse (« Politique … ») → retour à la ligne, information jamais
  perdue (vérifié programmatiquement APRÈS) ; littéral hors palette
  `#FFD27A` (étoile favori) → token `var(--vx-warning)` — le littéral
  analogue de scorecard.py est côté MOTEUR, dit et non touché ;
- preuves : 3 tests rouges→verts ; suite 1661/2 skipped ; RC outillée GO
  0 défaut sous SW v114 ; moteur 0.9.0 inchangé.

## Lot 58 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 3/4)

- défaut ACTIF trouvé sur /options : le token `--vx-text-dim` n'existe
  pas dans tokens.css → son fallback `#8a837a` (ancienne palette chaude)
  se rendait réellement sur tous les textes atténués ; ~28 fallbacks
  périmés au total dont l'ORANGE BANNI `#cf6128` (tag démo) et le cuivre
  `#b9683d` — tous réalignés sur les tokens réels et leurs valeurs
  actuelles ; tag démo → var(--vx-warning) ;
- /portfolio : 4 fallbacks périmés réalignés + `title` sur le libellé de
  scénario ellipsé (info complète au survol, aria-label déjà présent) ;
- preuves : 5 tests rouges→verts ; suite 1666/2 skipped ; RC outillée GO
  0 défaut sous SW v115 ; balayage APRÈS des couleurs CALCULÉES (14
  valeurs périmées recherchées sur tout #vx-content) : « palette OK »
  sur les deux pages, 0 erreur console ; moteur 0.9.0 inchangé.

## Lot 59 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 4/4, transversal)

- balayage du lot 58 GÉNÉRALISÉ : ~45 fallbacks d'anciennes palettes
  purgés dans 7 pages (3 oranges bannis de plus sur Système, un
  `--vx-brand,#84aa31` vert aberrant sur /journal, tracking, analysis,
  markets, opportunities, design_system_demo) ;
- 2e token INEXISTANT : `--vx-neutral` (Opportunités — son fallback
  `#9d978e` se rendait) → `--vx-neutral-chart` ; gardien PROSPECTIF :
  tout token référencé avec fallback doit exister dans les CSS ;
- /design-system : étiquettes hex mensongères (valeurs de l'ancien
  design à côté de pastilles LIVE justes) réalignées sur les valeurs
  effectives, section retitrée honnêtement ; rrLadder : 3 fallbacks
  runtime réalignés ;
- vérifié SAIN (dit) : VX.states.empty/error sur les 8 pages ;
- preuves : 4 tests rouges→verts ; suite 1670/2 skipped ; RC outillée GO
  0 défaut sous SW v116 ; balayage APRÈS couleurs calculées : « palette
  OK » sur /journal, /system, /design-system ; moteur 0.9.0 inchangé.

## Lot 61 — livré (2026-08-06, reprise du travail continu)

- Catalyst Runway (briefing) : les étiquettes se chevauchaient sur les
  DTE proches (capture lot 56) — anti-collision DÉTERMINISTE à deux
  rangées par côté, place calculée sur la position bornée au viewBox ;
  le harnais de preuve (chevauchements MESURÉS par bounding boxes) a
  attrapé un défaut résiduel au premier essai, corrigé avant livraison :
  0 chevauchement, 0 hors-limites sur le calendrier dense ;
- gardien anti-palette du lot 59 ÉTENDU aux JS de charts : 25 fallbacks
  périmés purgés (chart-core, runway, anomaly-scan — `--vx-text-dim`
  actif —, regime-aura) + 3e token fantôme `--vx-bg-app` → `--vx-bg-0` ;
- preuves : 5 tests rouges→verts ; suite 1675/2 skipped ; RC outillée GO
  0 défaut sous SW v117 ; moteur 0.9.0 inchangé.

## Lot 62 — livré (2026-08-06, travail continu)

- dernier angle mort de la classe « ancienne palette » fermé :
  19 fallbacks périmés dans `js/pages/` (options-gex — orange banni +
  `--vx-text-dim` ACTIF —, options-intel, options-structure) + 2
  littéraux runtime de tracking.js réalignés ;
- gardien prospectif ÉTENDU à TOUT `vertex/static/vertex/js/`
  récursivement (vendor exclu) : fallback ∈ valeurs actuelles + token
  existant + zéro orange banni — la classe de défauts est FERMÉE sur
  tout le dépôt UI (pages Python lot 59, charts lot 61, reste lot 62) ;
- preuves : 4 tests rouges→verts ; suite 1679/2 skipped ; RC outillée GO
  0 défaut sous SW v118 ; balayage couleurs calculées « palette OK » sur
  /options structure+gex et /tracking ; moteur 0.9.0 inchangé.

## Lot 63 — livré (2026-08-06, travail continu)

- écart de cohérence réel (capture lot 56) : mini-aires des cartes
  d'indices en POLYLIGNES anguleuses au-dessus du grand C.area lissé →
  `sparkArea` trace désormais un chemin lissé MONOTONE Fritsch-Carlson
  (jamais de dépassement des données, points exacts, déterministe),
  dégradé + point actif conservés ; le langage visuel 2026 est uniforme
  sur tous les graphiques (Chart.js + SVG locaux) ;
- `sparkSvg` : zéro consommateur (grep) — code mort supprimé ;
- preuves : 5 tests rouges→verts ; suite 1684/2 skipped ; RC outillée GO
  0 défaut sous SW v119 ; navigateur : 4/4 mini-aires en courbes
  cubiques, zéro polyligne, 0 erreur console ; moteur 0.9.0 inchangé.

## Lot 64 — livré (2026-08-06, travail continu — tour d'inspection)

- audit élargi 8 pages × 2 viewports (débordements 0, boutons sans nom
  0, erreurs console 0) + nouveau critère : éléments RÉELLEMENT tronqués
  sans `title` → 3 occurrences vues en navigateur, 8 points d'appel
  `vx-truncate` sans title au grep (6 fichiers) — tous corrigés, le
  texte entier reste lisible au survol (même échappement esc()) ;
- gardien PROSPECTIF « vx-truncate ⇒ title » : classe fermée ;
- preuves : 2 tests rouges→verts ; suite 1686/2 skipped ; RC outillée GO
  0 défaut sous SW v120 ; re-balayage APRÈS : 0 élément tronqué sans
  title (desktop + mobile) ; moteur 0.9.0 inchangé.

## Lot 65 — livré (2026-08-06, travail continu — bascule RC espacées)

- angles NEUFS audités en navigateur : doublons d'id 0, liens internes
  morts 0/13, focus clavier visible 8/8 sur chaque page, SVG informatifs
  sans aria → 1 seul cas réel : le Catalyst Runway (le Regime Aura était
  déjà couvert) — corrigé en une ligne (role img + aria-label reprenant
  le verdict réel, échappé) ; re-balayage APRÈS : 0 restant ;
- CONSTAT HONNÊTE : 7 tours de qualité consécutifs (58→65) ont fermé
  toutes les classes par gardiens ; ce tour n'a produit qu'un
  micro-défaut → BASCULE en RC périodiques espacées (~30 min), dit ;
- preuves : 2 tests rouges→verts ; suite 1688/2 skipped ; RC outillée GO
  0 défaut sous SW v121 ; moteur 0.9.0 inchangé.

## RC périodique n°5 — GO (2026-08-06, surveillance espacée)

- première RC du mode espacé acté au lot 65 : suite 1688/2 skipped,
  compileall exit 0, audit outillé GO 0 défaut sous SW v121 (8 pages,
  client-log 0, parcours mémoire, CYCLE SOUVERAIN re-prouvé : altération
  refusée + restauration bouton), responsive 8×3 : 0 débordement,
  0 erreur console ; moteur 0.9.0 et main intacts ; prochaine RC ~30 min.

## RC périodique n°6 — GO (2026-08-06, surveillance espacée)

- suite 1688/2 skipped, compileall exit 0, audit outillé GO 0 défaut
  sous SW v121 (cycle souverain re-prouvé), responsive 8×3 :
  0 débordement, 0 erreur console ; moteur 0.9.0 et main intacts ;
  prochaine RC ~30 min.

## RC périodique n°7 — GO (2026-08-06, surveillance espacée)

- suite 1688/2 skipped, compileall exit 0, audit outillé GO 0 défaut
  sous SW v121 (cycle souverain re-prouvé), responsive 8×3 :
  0 débordement, 0 erreur console ; moteur 0.9.0 et main intacts ;
  prochaine RC ~30 min.

## Lot 66 — livré (2026-08-06, AUDIT TOTAL relancé par l'utilisateur)

- programme utilisateur « audit totalement complet, tout cohérent,
  pousser au maximum » traduit en volets PROUVABLES ; RC espacées
  suspendues, développement continu relancé ;
- volet routes : 137 routes GET balayées — 94×200, 41 redirections
  voulues, un seul 400 STRUCTURÉ, AUCUN 5xx ;
- volet cohérence : VIX et meilleure opportunité cohérents partout ;
  UNE incohérence réelle — tuile Breadth du briefing sur `above50`
  (50 %) NON étiquetée vs Marchés `>MM200` (45 %), et diff interne sur
  above200 → canonicalisée >MM200 + ÉTIQUETTE de métrique sur la tuile ;
  preuve APRÈS : 45 partout, nommé pareil ;
- volet boutons/console : 0 non câblé, 0 erreur ;
- preuves : 4 tests rouges→verts ; suite 1692/2 skipped ; RC outillée GO
  0 défaut sous SW v122 ; moteur 0.9.0 inchangé ;
- volets suivants (67+) : vues profondes (tous les onglets), couverture
  IBKR lecture seule, cohérence fiche ↔ opportunités, états dégradés.

## Lot 67 — livré (2026-08-06, AUDIT TOTAL volet 2 — vues profondes)

- inventaire COMPLET des vues depuis les registres `_VIEWS` (source de
  vérité) : 30 vues (Marchés ×5, Opportunités ×5, Options ×9 dont
  3 legacy servies, Journal ×5, + 6 pages/fiches) × 2 viewports =
  60 chargements ;
- critères : 0 erreur console, 0 débordement, AUCUN texte cassé
  (NaN/undefined/[object]/null — proxy de donnée mal branchée) ;
- résultat : **0 défaut sur 60 chargements** — constat honnête, aucun
  correctif requis (effet des gardiens des lots 51→66) ; lot
  documentaire, pas de bump SW ;
- suite 1692/2 skipped tenue ; moteur 0.9.0 inchangé.

## Lot 68 — livré (2026-08-06, AUDIT TOTAL volet 3 — IBKR lecture seule)

- les 4 verrous READONLY en place : `readonly=True` EN DUR dans le
  gateway (non paramétrable), `RequestTimeout=45` (gateway + scheduler),
  registre IA `FORBIDDEN_TOOLS` (tous les verbes d'ordre bloqués),
  `READONLY=True` config — aucun verbe d'ordre actif dans vertex/ ;
- refus honnêtes prouvés sous NO_IBKR : /api/ibkr/positions ok:false +
  erreur claire (jamais de position inventée), /api/pos-quotes
  live:false + ts (fraîcheur toujours portée, cache borné purgé) ;
- UI dégradée exemplaire : « P&L latent indisponible (marques IBKR hors
  ligne — aucun chiffre inventé) », n/d partout, 0 erreur console ;
- 34 gardiens dédiés verts (no_orders, ibkr_honesty, order_ticket) ;
  note doc : la docstring du gateway cite un nom de fichier de test
  obsolète (divergence documentaire, dite) ;
- verdict : SAIN, aucun correctif — lot documentaire, suite 1692/2
  skipped tenue, SW v122, moteur 0.9.0.

## Lot 69 — livré (2026-08-06, AUDIT TOTAL volet 4 — fiche ↔ Opportunités)

- croisement réel ACN/AOS/MMM (endpoints ↔ Opportunités ↔ fiche) : les
  deux moteurs divergent LÉGITIMEMENT (command ACHETER/RENFORCER vs
  Skyler canonique REFUSER 18-19/40 — gates honnêtes) et la hiérarchie
  est DITE aux deux endroits (« un score ne déclenche jamais un ordre » ;
  « la décision finale unique reste REFUSER — les verdicts techniques
  sont des entrées du moteur exécutif ») ; aucun même champ à deux
  valeurs — SAIN, vérifié ;
- UNE lacune de traçabilité corrigée : score shortlist nu → « /100 »
  (preuve APRÈS : 81 /100, 74 /100, 73 /100) — tout score affiché porte
  son échelle, partout ;
- preuves : 2 tests rouges→verts ; suite 1694/2 skipped ; RC outillée GO
  0 défaut sous SW v123 ; moteur 0.9.0 inchangé.

## RC périodique n°8 — GO (2026-08-06, surveillance espacée)

- première RC après la clôture de l'AUDIT TOTAL (bilan n°5) : suite
  1694/2 skipped tenue, compileall exit 0, audit outillé GO 0 défaut
  (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle souverain :
  altération refusée 400 + restauration bouton), responsive 8×3 = 24
  chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°9 armée (~30 min).

## RC périodique n°9 — GO (2026-08-06, surveillance espacée)

- suite 1694/2 skipped tenue, compileall exit 0, audit outillé GO 0
  défaut (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle
  souverain : altération refusée 400 + restauration bouton), responsive
  8×3 = 24 chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°10 armée (~30 min).

## RC périodique n°10 — GO (2026-08-06, surveillance espacée)

- suite 1694/2 skipped tenue, compileall exit 0, audit outillé GO 0
  défaut (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle
  souverain : altération refusée 400 + restauration bouton), responsive
  8×3 = 24 chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°11 armée (~30 min).

## PROGRAMME 100 % — TERMINÉ (lots 71 → 75, voir bilan n°6 en tête)

Directive utilisateur : « Continue à tout développer et quand t'as tout à
100 tu me dis. » → sortie de la surveillance espacée, cadence resserrée
(~2 min entre lots), clôture prévue au lot 75 (RC finale + BILAN n°6 +
déclaration 100 % à l'utilisateur).

- **Lot 71 — livré** : hygiène des références. Docstring du gateway IBKR
  citait un gardien inexistant (`test_readonly_gateway`) → corrigée (cite
  les 3 vrais gardiens READONLY) + gardien prospectif « toute référence
  `tests/test_*.py` citée dans vertex/ doit exister » (balayage complet :
  1 seule vraie divergence, le reste = faux positifs chemins d'URL).
  Suite 1696/2 skipped (+2 rouges d'abord), RC outillée GO, SW v123
  (pas de bump — rien de visible).
- **Lot 72 — livré** : audit PERFORMANCE. Mesures réelles 8 pages (cache
  froid) : DCL < 300 ms en régime établi, 0 doublon, 0 ressource en
  erreur, vendor 160 kB lazy sur /analysis seul, plus gros fichiers 39-46
  kB — SAIN. 3 gardiens prospectifs de budget (64 kB/fichier, vendor
  jamais dans le shell). Suite 1699/2 skipped.
- **Lot 73 — livré** : accessibilité, angles restants. Balayage outillé
  8 pages (noms accessibles, labels, focusabilité) : 4 défauts réels sur
  /opportunities — tickers cliquables non focusables au clavier et
  délégation limitée au clic → tabindex+role sur les 3 gabarits +
  délégué clavier global Enter/Espace (vx-entities.js, prospectif).
  Balayage APRÈS : 0 défaut. Suite 1702/2 skipped, SW v124 + 4 gardiens.
- **Lot 74 — livré** : robustesse données limites. Sondes réelles :
  symboles invalides/injection/unicode/120 chars sur analysis+skyler,
  vues inconnues sur 8 pages, POST malformés sur pos-quotes — 0×5xx
  partout, 404 API JSON+nosniff (faux positif XSS de ma sonde vérifié
  aux en-têtes, dit), refus honnêtes live:false+ts. SAIN — 4 gardiens
  prospectifs. Suite 1706/2 skipped, SW v124.
- **Lot 75 — livré** : RC FINALE sur base fraîche (suite 1706/2, audit
  outillé GO, responsive 0 défaut, a11y 0 défaut) + BILAN n°6 en tête +
  déclaration 100 % faite à l'utilisateur. Retour RC espacées (~30 min).

## BOUCLE CONTINUE — EN COURS (ré-ouverte au lot 76, 2026-08-06)

Directive utilisateur : « Continue encore et encore ne t'arrête pas. »
Cadence resserrée (~2 min), tournée d'inspection perpétuelle : chaque lot
mesure un angle, corrige les défauts réels trouvés, garde la classe.

- **Lot 76 — livré** : hygiène JS/HTML. Débogage/duplications/TODO : 0
  partout ; 1 défaut réel — onglets démo design-system en `href="#"`
  (saut en haut de page) → ancres non-navigantes + gardien « plus jamais
  de href=# ». Suite 1708/2 skipped, SW v125 + 4 gardiens.
- **Lot 77 — livré** : sécurité en-têtes/contenu servi. 4 en-têtes
  présents partout (pages, API, statiques), contenu 0 email/secret/
  chemin/nom ; 1 défaut réel — `/api/desk` (données personnelles) sans
  Cache-Control → `no-store` par le middleware + gardiens. Suite 1710/2
  skipped, SW v125 (pas de bump — serveur).
- **Lot 78 — livré** : libellés français. Texte affiché 8 pages +
  sources : 0 anglais d'interface, 0 accent manquant, ponctuation
  conforme (l'espace avant « ; » est la norme FR — faux positif de la
  sonde, dit). SAIN — 2 gardiens prospectifs. Suite 1712/2 skipped.
- **Lot 79 — livré** : fraîcheur des données affichées. 2 passes
  navigateur : aucun chiffre marché sans fraîcheur accessible — les 5
  signalements stricts étaient des faux positifs (héritage de
  l'indicateur d'en-tête « Il y a X min · source » + troncature de
  sonde), vérifiés un à un. SAIN — 2 gardiens. Suite 1714/2 skipped.
- **Lot 80 — livré** : 5 parcours bout-en-bout « du réveil à la
  décision » : 14 étapes, 0 échec (outil versionné
  `tools/user_journeys.js`). Constat réel : polices sur CDN Google
  (offline + vie privée) → lot 81 = auto-hébergement. Mini-bilan
  76-80 : 2 défauts corrigés, 8 gardiens, suite 1706→1714.
- **Lot 81 — livré** : polices AUTO-HÉBERGÉES. 2 woff2 variables locaux
  (78 kB, dédupliqués aux empreintes), fonts.css local, 7 blocs CDN
  remplacés (shell + legacy), SW v126 précache les polices. Preuves :
  0 requête externe sur 8 pages, Inter/JBM chargées localement,
  parcours 14/14 avec 0 erreur console. Suite 1718/2 skipped.
- **Lot 82 — livré** : offline RÉEL. Défaut majeur — le shell canonique
  n'enregistrait JAMAIS le service worker (0 précache, offline = page
  d'erreur sur les 8 espaces) → enregistrement dans vx-shell.js (pas
  d'inline : gardien anti-reflet du fuzz 43, attrapé et dit). Preuve
  APRÈS : reload OFFLINE rendu depuis le cache, Inter offline, états
  honnêtes. Suite 1720/2 skipped, SW v127 + 4 gardiens.
- **Lot 83 — livré** : contrôles interactifs. 26 tris/onglets/selects
  cliqués en vrai sur 8 vues : l'ordre change, les vues basculent avec
  leur état visuel, 0 inerte, 0 erreur console. SAIN — outil
  tools/controls_audit.js versionné. Suite 1720/2 skipped.
- **Lot 84 — livré** : cycle desk bout-en-bout. 6/6 en navigateur :
  push (17 clés) → serveur porte le marqueur → pull restitue → 3
  backups listés → restore PAR LA ROUTE → remise en état
  last-writer-wins. Aucune perte possible constatée ; 4 listes de clés
  alignées (gardien vert). 2 gardiens API. Suite 1722/2 skipped.
- **Lot 85 — livré** : alertes + flux live. Cycle alerte 4/4 (création
  API client → localStorage → sync serveur → suppression propre) ; SSE
  sain — mes 2 sondes initiales étaient des faux positifs (pipe
  bufferisé ; onmessage vs événements nommés), vérifiés au socket brut
  puis addEventListener, dits. 3 gardiens. Suite 1725/2 skipped.

- **Lot 86 — livré** : cas limites du decision stack. 10 branches non
  couvertes identifiées (lecture complète du moteur vs 21 tests
  existants) et FIGÉES par caractérisation, nées vertes : detail=None
  honnête, score illisible jamais inventé, bornes exactes 56/66/80,
  verdict inconnu → WAIT, frontière rassis 900 s, CHOP, distribution,
  démo étiquetée, R:R absent ne punit pas, véhicule ACTION hors achat.
  Moteur 0.9.0 INTACT (diff = tests + docs). Suite 1735/2 skipped.

- **Lot 87 — livré** : façade recommendation + __VXVOCAB figées. La
  façade unique (212 lignes) n'avait AUCUN test dédié (homonyme testé
  ailleurs) → 10 caractérisations nées vertes : vocabulaire client sans
  trou (9 décisions + 7 verdicts de gestion), normalize honnête,
  discipline -20 % action / -25 % option exacte, thêta ≤14 j, cible,
  ADD/TRIM selon sous-jacent, board vide honnête. Moteur intact.
  Suite 1745/2 skipped.

- **Lot 88 — livré** : evidence + reasoning figés. 24 tests dédiés
  existants (nominal) + 10 caractérisations nées vertes sur les
  limites : gather(None) honnête, analystes sans entrée → [], force
  bornée 0-100, bornes catalyseur exactes, fondamental 0 = absent
  (jamais puni), UNKNOWN prime, contradiction CHAOS+empilées exposée,
  scénarios sans prix jamais un % inventé, comité absent sans biais,
  invalidations plafonnées. Moteurs intacts. Suite 1755/2 skipped.

- **Lot 89 — livré** : track_record figé. Le moteur d'auto-notation
  (181 lignes) n'avait aucun test dédié → 6 caractérisations nées
  vertes (ledger simulé, fichiers runtime jamais touchés) : record sans
  lignes → 0, bords _fwd/_hit_tp1 honnêtes, ledger vide → zéros,
  n<5 jamais publié, division par zéro impossible, mémo 30 min.
  Moteur intact. Suite 1761/2 skipped.

- **Lot 90 — livré** : persist + connections figés (10 tests — persist
  tolérant/fidèle sans toucher au runtime ; connections « configuré ≠
  connecté », jamais LIVE sans preuve, READONLY dit même en LIVE,
  démo étiquetée partout). Suite 1771/2 skipped.

- **Lot 91 — livré** : decide.py figé (9 caractérisations — un seul
  test existait, le gate R:R). {} → None refus honnête (hypothèse de ma
  sonde corrigée, dit), hard gates stop/régime/R:R borne 2.0 exacte,
  CHOP jamais d'achat, sur-étendu → « attendre un repli », IV-crush
  ≤ 14 j cité. Moteur intact. Suite 1780/2 skipped.

- **Lot 92 — livré** : committee.py — DÉFAUT RÉEL trouvé par la
  caractérisation : la branche « DANS LA ZONE D'ACHAT » était du code
  mort (le garde `ez < price` contredisait `in_zone`) — la fenêtre
  promise par la note ne s'ouvrait JAMAIS au repli. Corrigé
  minimalement (nominal inchangé, prouvé : 110 → ATTENDRE avec zone ;
  100 → ACHETER « DANS LA ZONE »). skyler_core 0.9.0 non touché.
  9 tests (le rouge + 8 caractérisations). Suite 1789/2 skipped.

- **Lot 93 — livré** : pivots/structure figé (8 caractérisations — il
  nourrit committee et la zone d'achat du lot 92, aucun test dédié
  n'existait). Cassure fraîche confirmée avec measured move exact,
  cassure étendue jamais poursuivie, rebond baissier = piège refusé,
  repli repris confirmé, ATR 0 sans division par zéro. Moteur intact.
  Suite 1797/2 skipped.

- **Lot 94 — livré** : contrat des routes POST figé. 12 routes sondées
  avec payloads limites : 0×5xx, refus structurés honnêtes partout
  (« symbol requis », « question vide », « scan pas encore prêt ») ;
  télémétrie client bornée (troncatures 120/300/160 exactes, line
  non-entier → None, tampon circulaire plafonné à 100). 4 tests.
  Suite 1801/2 skipped.

- **Lot 95 — livré** : filtres durs options figés (6 caractérisations
  directes — bornes DTE inclusives, delta inconnu jamais classé, refus
  documentés, PUT hors périmètre, annotations _liquidity/_anomalies).
  Repérage honnête : indicators/anomaly/events/call_selector déjà
  couverts (dit). Suite 1807/2 skipped.

- **Lot 96 — livré** : socle math du lab options figé (7 tests —
  _ncdf CDF de table, _bs dégénéré → intrinsèque jamais NaN, PARITÉ
  PUT-CALL exacte à 1e-9, golden BS 10,19 recalculé à la main : mon
  premier golden mémoire 10,27 était faux, LE MOTEUR AVAIT RAISON,
  dit ; _pct jamais de division par zéro, _star qualité d'abord, _rr
  jamais inventé). Moteur intact. Suite 1814/2 skipped.

- **Lot 97 — livré** : scoring pur figé (8 tests — tous les sous-scores
  bornés 0-100, neutres exacts sur dict vide, ROC borné ±25, fondamental
  réel vs proxy figés avec drapeau d'honnêteté, options_score(None) →
  None jamais 0 inventé, −10 IV-crush exact, double peine court+IV
  chère, confiance auto-cohérente). Moteur intact. Suite 1822/2 skipped.

- **Lot 98 — livré** : earnings + barème stratégie figés (8 tests —
  date inconnue honnête, réaction ≤2 j vs drift, run-up avec sortie
  avant annonce, refus avec chaque exigence NOMMÉE, langage de
  certitude neutralisé, bornes grade exactes, CHOP jamais un BUY,
  poids = 100). option_anomalies déjà couvert (21 tests, dit).
  Moteurs intacts. Suite 1830/2 skipped.
- **Lot 99 — livré** : broker SSE + états système figés (9 tests —
  live_stream n'avait AUCUN test direct : canal inconnu reclassé
  system, replay Last-Event-ID exact, tampon circulaire borné, client
  lent jamais bloquant (501 événements), unsubscribe idempotent,
  framing SSE nommé exact (leçon lot 85) ; status_service :
  ok/warming/degraded, rassis = avertissement pas panne, pas de
  timestamp → unknown honnête, mode demo>ibkr>cloud). Moteurs
  intacts. Suite 1839/2 skipped.

### BILAN CONSOLIDÉ n°7 — tournée « continue encore et encore » (76-100)

24 lots, PR #109 → #132 (une par lot, squash, `main` intacte),
suite **1706 → 1839 passed / 2 skipped** (+133 tests), SW v124 → v127,
skyler_core 0.9.0 JAMAIS touché, RC outillée GO à chaque lot.

- **4 défauts réels corrigés** : onglets démo `href="#"` (76) ·
  `/api/desk` sans Cache-Control → `no-store` (77) · **DÉFAUT MAJEUR :
  le shell n'enregistrait JAMAIS le service worker** — zéro offline
  depuis toujours → enregistrement vx-shell.js + précache, reload
  hors-ligne prouvé (82) · code mort « DANS LA ZONE D'ACHAT » de
  committee — seule modification moteur de la tournée (92).
- **2 chantiers** : polices auto-hébergées, 0 requête externe (81) ·
  PWA offline réel (82).
- **Programme « moteurs blindés » 86-99 : 114 caractérisations** figeant
  toute la chaîne — decision_stack, recommendation/__VXVOCAB, evidence,
  track_record, persist/connections, decide, committee, pivots, routes
  POST, contract_filter, math Black-Scholes du lab, scoring,
  earnings+barème, broker SSE + états système.
- Leçons encodées : couverture réelle = grep du NOM de module ; golden
  recalculés à la main ; sondes SSE au socket brut + événements nommés ;
  aucun `<script>` inline (fuzz anti-XSS).

Détail complet : `docs/refactor/validation/SKYLER-LOT-100.md`. Étapes
humaines restantes : validation physique TWS réel + iPhone (cache vidé,
SW v127) ; merge vers `main` sur accord explicite uniquement.

- **Lot 101 — livré** : entonnoir de chaîne options figé (8 tests —
  chain_loader n'avait qu'UN test indirect : bornes DTE constitution
  INCLUSIVES, préférées d'abord triées par distance au centre 150,
  _dist jamais fui, fenêtre strikes ±35 % exacte, spot ≤ 0 → [],
  échantillonnage à 14 pile gardant les 2 extrêmes, expiration sans
  strike plausible jamais envoyée au broker, contrat d'entrée du
  plan). market_clock déjà figé (dit). Moteur intact. Suite 1847/2
  skipped.
- **Lot 102 — livré** : gardien XSS des news figé (9 tests — la règle
  n°5 n'était testée qu'au point de sortie d'une route : balises
  retirées PUIS échappement complet, balise jamais fermée inerte,
  javascript:/data: supprimés, http(s) seul (insensible casse),
  quotes pourcent-encodées ; sentiment lexical FR/EN ; parse_rss sans
  exception + suffixe éditeur retiré ; dedupe titre normalisé/lien
  premier conservé). Moteur intact. Suite 1856/2 skipped.
- **Lot 103 — livré** : barème de liquidité figé (8 tests —
  liquidity.assess n'avait qu'un test superficiel : refus bid/ask
  nommé score 0, contrat parfait 100 zéro grief, pénalité dégressive
  4-10 % exacte sans grief, spread > 10 % jamais traitable même à
  score ≥ 40, mid absent = prudence 100 %, OI inconnu (−15) < OI
  faible (−30), volume None silencieux vs faible nommé, cumul exact
  100−45−30−10=15). expected_move/event_risk déjà figés (dit).
  Moteur intact. Suite 1864/2 skipped.
- **Lot 104 — livré** : environnement options figé (8 tests —
  score_environment n'avait que 3 tests de surface : formules exactes
  des 5 dimensions (IV médiane 20 %→100/60 %→0, IV rank inversé
  borné, spread 1 %→100/8 %→0, event risk fraction ≤7 j), IV
  textuelle jamais convertie en silence, verdict 66/45 exact,
  dimension inconnue EXCLUE de la moyenne (jamais zéro) et NOMMÉE en
  incertitude, confiance = connues/5 ; 1 sonde corrigée (valeur non
  parsable = connue mais jamais imminente — réalité figée, dite).
  Moteur intact. Suite 1872/2 skipped.
- **Lot 105 — livré** : séquence de démarrage figée (8 tests — ordre
  §10 EXACT des 8 étapes, _step jamais bloquant (ERROR + détail 200 +
  ms), ibkr jamais CONNECTED sans preuve, tradingview MISSING « 503
  honnête » vs CONFIGURED, rapport readonly/disabled-by-design,
  startup_report copie infalsifiable, ran False avant séquence).
  interpretation/overview/pulse déjà couverts (dit). Moteur intact.
  Suite 1880/2 skipped.

### MINI-BILAN tournée 101-105

5 lots, 41 tests, suite **1839 → 1880 passed / 2 skipped**, 0 défaut
moteur trouvé (les moteurs tiennent), 2 sondes à moi corrigées (dites),
SW v127 stable, skyler_core 0.9.0 intact, PR #134 → #138 : chain_loader
(entonnoir §14 — jamais toute la chaîne au broker) · news_plus (gardien
XSS règle n°5 enfin figé en direct) · liquidity (barème complet — OI
inconnu < OI faible) · environment (5 dimensions exactes — inconnue ≠
zéro) · startup (ordre §10, démarrage jamais bloquant).

- **Lot 106 — livré** : score contextuel des contrats figé (8 tests —
  contract_scorer §20 n'avait qu'une assertion de constante : score
  MULTIPLICATIF (aucun facteur ne rachète un défaut fatal), R:R < 2
  plafonné à 10, non calculable plancher 5, liquidité multiplicateur
  ≤ 1, DTE hors fenêtre ×0.75 nommé, IV rank ≥ 85 taxée ×0.6 « DTE
  long ou pas », ULTRA_CONVEX score 0 sans setup EXCEPTIONAL et
  moitié si convexité < 80 %, prime < 0.10 ×0.3). Moteur intact.
  Suite 1888/2 skipped.
- **Lot 107 — livré** : courbe de taux figée (8 tests — RateCurve
  servait de fixture partout sans test direct : repli plat 0.045 qui
  SE DIT (jamais présenté comme du marché), interpolation linéaire
  exacte, clamp aux extrémités sans extrapolation, points désordonnés
  triés, tenor exact → taux exact, contrat to_dict, rate_sensitivity
  ±50 bp exacte avec plancher 0 et None honnête). double_prob déjà
  figé (dit). Moteur intact. Suite 1896/2 skipped.
- **Lot 108 — livré** : surface de volatilité figée (8 tests —
  vol_surface n'avait que 3 tests d'intégration : realized_vol 0
  exact sur prix constants et None sur série courte, spot invalide →
  surface vide + note, IV pourries filtrées, ATM = strike le plus
  proche du spot, skew jamais inventé sans put ~10 % OTM,
  STRIKE_IV_DISLOCATION + SMILE_DISCONTINUITY nommées, IV
  rank/percentile exacts, IV_SPIKE > 1.3× médiane récente, historique
  plat → rank None jamais 0). horizon_scanners déjà couvert (dit).
  Moteur intact. Suite 1904/2 skipped.
- **Lot 109 — livré** : registre des jobs figé (8 tests —
  scheduler/registry §24 n'avait aucun test direct : snapshot ordonné
  par priorité produit (positions avant univers), jamais exécuté →
  aucune ETA inventée, job non canonique enregistré mais jamais
  exposé en UI, beat ok/erreur tronquée à 200, ETA bornée jamais
  négative (boucle en retard → 0), façade = délégation pure, snapshot
  copie infalsifiable). Moteur intact. Suite 1912/2 skipped.
- **Lot 110 — livré** : cas limites du flux figés (8 tests — repli
  mid×100 avec cost prioritaire, clé volume alternative, NaN/inf
  rejetés, OI absent → jamais un badge « frais », frontières skew
  60/40 exactes, top borne l'affichage jamais le décompte, type
  inconnu → CALL, non-dicts filtrés). Moteur intact. Suite 1920/2
  skipped.

### MINI-BILAN tournée 106-110

5 lots, 40 tests, suite **1880 → 1920 passed / 2 skipped**, 0 défaut
moteur trouvé, 2 sondes à moi ajustées (dites), SW v127 stable,
skyler_core 0.9.0 intact, PR #139 → #143 : contract_scorer (score
multiplicatif — rien ne rachète un défaut fatal) · rates (fallback
documenté, jamais d'extrapolation) · vol_surface (ATM au plus proche,
skew jamais inventé, dislocations nommées) · scheduler/registry
(priorité produit, ETA jamais négative) · flow edges (jamais « frais »
sans OI). Note d'exploitation : lot 108 livré en avance sur
« Continue » utilisateur ; renommage MCP absorbé.

- **Lot 111 — livré** : validation de configuration figée (8 tests —
  config_validation §11 n'avait aucun test direct : MISSING avec
  conséquence exacte nommée, INVALID nommé, AUCUN secret jamais exposé
  dans le rapport, alias historique TRADINGVIEW_SECRET accepté,
  espaces = MISSING, enum broker insensible à la casse, compteurs
  _summary exacts, aucune variable obligatoire — l'app démarre
  toujours en mode sûr READONLY). Moteur intact. Suite 1928/2
  skipped.
- **Lot 112 — livré** : santé du runtime IA figée (8 tests —
  ai/health §10 n'avait qu'un usage superficiel : sans clé MISSING
  avec note honnête exacte, clé ≠ preuve (CONFIGURED jamais CONNECTED
  sans appel réel), succès → CONNECTED, échec après succès → DEGRADED
  tronqué 200, le dernier appel réel fait foi, modèle défaut
  claude-sonnet-5 + override strip, clé espaces non configurée, la
  valeur de la clé jamais dans le rapport). Moteur intact. Suite
  1936/2 skipped.
- **Lot 113 — livré** : types de provenance figés (8 tests —
  data_sources/models n'avait aucun test direct : missing() honnête
  par défaut, usable exige valeur ET qualité vivante (STALE reste
  utilisable, EXPIRED/MISSING non, None jamais), 0.0/False = vraies
  valeurs (piège falsy évité), to_dict complet, warnings jamais
  partagés entre instances, AnalyticsPacket 5 familles + as_of ISO
  auto, set_source stocke un snapshot dict, aucun état partagé entre
  paquets). engines/backtest déjà couvert (dit). Moteur intact.
  Suite 1944/2 skipped.
- **Lot 114 — livré** : frontière d'unités IV figée (8 tests —
  iv_units (né du grand défaut IV %/décimal) n'avait que 4
  assertions : unité inconnue = ValueError (une unité devinée est un
  bug), NaN/inf/≤0 → None dans les deux unités, conversions exactes,
  porte legacy DÉTECTÉE ET ÉTIQUETÉE jamais muette, seuil 1.5 exact
  (1.5 pile = décimal, 1.51 = pourcentage averti), ordure → triple
  None, exports limités aux deux portes). Moteur intact. Suite
  1952/2 skipped.
- **Lot 115 — livré** : backtest recherche figé (8 tests —
  research/backtest §29 + factory.apply_costs n'avaient aucun test
  direct : rotation 0 = coût 0, chaque aller-retour se paie
  (formule exacte (spread+slippage)/100 × rotation), position 0 =
  équité plate, vide = None honnête, avertissement « walk-forward
  requis » sur CHAQUE résultat, longueurs tronquées au plus court,
  demi-position = moitié d'exposition). Moteur intact. Suite 1960/2
  skipped.

### MINI-BILAN tournée 111-115

5 lots, 40 tests, suite **1928 → 1960 passed / 2 skipped**, 0 défaut
moteur trouvé, 0 sonde corrigée (premier passage partout), SW v127
stable, skyler_core 0.9.0 intact, PR #144 → #148 : config_validation
(conséquence exacte par absence, secrets jamais exposés) · ai/health
(clé ≠ preuve — jamais CONNECTED sans appel réel) · provenance models
(STALE utilisable, 0/False vraies valeurs) · iv_units (unité devinée =
bug, legacy étiquetée) · research/backtest (un backtest n'est jamais
une preuve). Note d'exploitation : le serveur MCP des réveils a changé
deux fois de nom — absorbé, repli encodé au canevas.

- **Lot 116 — livré** : catalyseurs non-earnings figés (8 tests —
  event_engine §21/§23 n'avait aucun test : non confirmé JAMAIS dans
  l'horizon actionnable même à 5 j, type inconnu reclassé OTHER et
  dénoncé, horizon 0-30 j bornes incluses trié par proximité, fenêtre
  earnings 45 j incluse/46 exclue/passé exclu, next_events cap 3,
  avertissement nommé avec compte exact « jamais utilisés pour tenir
  une position à travers un événement »). Moteur intact. Suite
  1968/2 skipped.
- **Lot 117 — livré** : Research Factory figée (8 tests —
  factory §29 n'avait que 2 tests nominaux : transitions interdites
  refusées (IDEA ne saute jamais DEFINED, APPROVED ne redevient
  jamais une idée, RETIRED terminal), REJECTED renaît en IDEA, état
  inconnu nommé, DEFINED exige 11 champs nommés, APPROVED exige les
  12 contrôles de biais nommés + walk-forward (« un beau backtest ne
  suffit jamais »), transitions historisées, embargo réel des splits
  avec bornes exactes, passed ≥ max(2, n−1) folds positifs).
  Moteur intact. Suite 1976/2 skipped.
- **Lot 118 — livré** : lecture graphique figée (8 tests —
  chart_read (169 lignes) n'avait aucun test direct : {} → None
  honnête (sonde corrigée, dite), hiérarchie de tendance, seuils RSI
  78/60/48 exacts, indices chiffrés, accumulation prime sur
  distribution, chart_verdict 4 issues, thesis où la MÉFIANCE prime
  (distribution avant cassure), plays par profil + R:R + vent MTF).
  Moteur intact. Suite 1984/2 skipped.
  NOUVELLE DIRECTIVE reçue : lots 119+ orientés amélioration
  visuelle des graphiques page par page (« plus propres, plus beaux,
  plus développés »), en alternance avec les caractérisations.
- **Lot 119 — livré** : amélioration graphique n°1 (Aujourd'hui) —
  Catalyst Runway développé : zone d'imminence ≤ 5 j teintée
  (l'urgence se voit avant de se lire), points dimensionnés par
  impact avec halo doux, anneau de focalisation sur le prochain
  catalyseur, graduations hebdomadaires, bornes « aujourd'hui /
  horizon » nommées, étiquettes élargies, anti-collision conservé,
  tokens uniquement. SW v127 → v128 + 4 gardiens. Captures 1440
  avant/après envoyées à l'utilisateur. Suite 1984/2 skipped, RC GO.
  DIRECTIVE ESTHÉTIQUE renforcée reçue : priorité aux dégradés
  propres, traits fins, points propres, moins de chiffres empilés,
  lecture éducative et efficace — chaque page développée au max.
- **Lot 120 — livré** : amélioration graphique n°2 (Marchés) —
  lignes ultra propres au CŒUR des charts (chart-core.js) :
  endDotsPlugin (chaque série finit par un point net + son nom dans
  sa couleur — fini l'aller-retour vers la légende), softGlowPlugin
  (halo néon doux), traits affinés 1.6, dégradé area 4 arrêts.
  Bénéfice transversal : toutes les pages qui utilisent
  multiLine/area héritent de la finition. Gardien lot 52 mis à jour
  vers la nouvelle signature (délibéré). SW v128 → v129 + 4
  gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 116-120

5 lots (3 caractérisations + 2 graphiques), 24 tests, suite
**1960 → 1984 passed / 2 skipped**, 0 défaut moteur, PR #149 → #153,
SW v127 → v129 : event_engine (non confirmé jamais actionnable) ·
factory (un beau backtest ne suffit jamais) · chart_read (la méfiance
prime) · GRAPHIQUE Aujourd'hui (Catalyst Runway développé) · GRAPHIQUE
Marchés (lignes ultra propres transversales). Pivot de la boucle vers
l'esthétique sur directive utilisateur — chaque page au maximum,
sans autorisation demandée.

- **Lot 121 — livré** : amélioration graphique n°3 (Opportunités) —
  entonnoir « ultra propre » dans chart-core (un seul ton de marque
  en dégradé vertical brand → cyan, opacité qui décroît avec la
  profondeur, UN chiffre par étage — les % doublés supprimés —, la
  plus forte perte marquée −N discret) + zone actionnable du scatter
  teintée en dégradé positif léger. Aucun littéral couleur nouveau.
  SW v129 → v130 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 122 — livré** : amélioration graphique n°4 (Analyse) —
  radar en dégradé RADIAL dans chart-core (centre quasi transparent
  → bord de marque : la surface respire), points sommets nets avec
  halo, grille en opacité dégressive (l'extérieur guide, l'intérieur
  murmure), trait 1.6 jointures arrondies, id de dégradé unique par
  hôte. Bénéficiaires : scorecard des fiches Analyse + dossier
  analyste. SW v130 → v131 + 4 gardiens. Captures fiche ACN
  avant/après envoyées. Suite 1984/2, RC GO. (Démarré sur « Go »
  utilisateur sans attendre le réveil.)
- **Lot 123 — livré** : amélioration graphique n°5 (Portefeuille) —
  treemap matière VERRE dans chart-core : dégradé diagonal par tuile
  (dense → doux ; même le neutre honnête des marques hors ligne
  gagne de la profondeur), liseré fin de la couleur de la tuile au
  lieu du trait noir épais, coins arrondis, part du TOTAL (%) sur
  les grandes tuiles (le chiffre éducatif du treemap, aussi dans
  l'aria). SW v131 → v132 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.
- **Lot 124 — livré** : amélioration graphique n°6 (Options) —
  payoff éducatif : le BREAKEVEN est enfin tracé (ligne warning
  « BE $X » — le chiffre éducatif d'un payoff), le SPOT aussi (ligne
  info), zones gain/perte migrées des hex en dur vers les tokens,
  trait 1.6 + halo doux (softGlowPlugin réutilisé). Arithmétique du
  contrat inchangée. SW v132 → v133 + 4 gardiens. Captures
  avant/après envoyées. Suite 1984/2, RC GO. (12 captures desktop
  de toutes les pages envoyées entre-temps sur demande.)
- **Lot 125 — livré** : amélioration graphique n°7 (Journal) —
  barres matière VERRE dans chart-core (chaque barre = dégradé de sa
  propre couleur, dense à l'extrémité de la valeur → doux vers la
  base, liseré fin, pleine au survol — TOUS les graphiques à barres
  de Vertex héritent) ; famille `.vx-stat` enfin stylée dans
  cockpit.css (les stats du Post-mortem s'affichaient COLLÉES —
  « Trades3 » — car les classes utilisées par 5 pages n'avaient
  aucun CSS : tuiles de verre, chiffres mono tabulaires, halo
  positif/négatif) ; hex en dur du track record → tokens. Aucun
  littéral couleur nouveau. SW v133 → v134 + 4 gardiens. Captures
  avant/après + preuve barres verre envoyées. Suite 1984/2, RC GO.

- **Lot 422 — livré** : **le R:R affiché repose sur un mouvement attendu que le
  moteur s'invente, et c'est le seul repli qu'il n'étiquette pas.** Sixième lot
  dans la veine des moteurs. Cible : `vertex/options/scenario_pricer.py`, qui
  produit le **R:R du plan** et le **gain attendu** affichés sur `/options`,
  `/analysis` et `/opportunities`.
  **La règle est écrite partout dans ce fichier.** Le docstring l'annonce
  (*« honnêteté §6.8 : … ESTIMATION … étiquetée MODEL_ESTIMATE, jamais présentée
  comme vérité broker »*) et le corps la tient **trois fois** : données
  insuffisantes → **simulation refusée** (« pas de chiffre inventé ») · IV
  absente → recalculée **et** `limitations.append('IV recalculée depuis le mid
  (FALLBACK_ESTIMATE)')` **et** `model_source = 'FALLBACK_ESTIMATE'` ·
  `worst_planned_loss_pct` calculé **seulement** `if stop:`, jamais sur un stop
  inventé.
  **Trois lignes au-dessus du repli IV étiqueté, un quatrième repli — muet :**
  ```python
  em_pct = setup.expected_move_pct
  if em_pct is None:
      em_pct = iv * math.sqrt(holding_days / 365.0) * 100     # aucune limitation ajoutée
  ```
  **Ce n'est pas un cas de bord : c'est le seul chemin.** Les **deux**
  constructeurs d'`UnderlyingSetup` du dépôt (`options_intel_api.py:107` et
  `redesign.py:226`) **omettent le champ** — `expected_move_pct` vaut donc `None`
  **à chaque simulation**, et le mouvement attendu est **toujours fabriqué par le
  moteur lui-même**.
  **Mesuré**, contrat identique, seul le mouvement varie :
  ```text
                                      gain BASE    pire perte    R:R
  expected_move_pct = None (PROD)       145.7 %      -40.8 %     3.57
  expected_move_pct =  3.0 %            104.7 %      -40.8 %     2.57
  expected_move_pct =  8.0 %            213.7 %      -40.8 %     5.24
  expected_move_pct = 12.0 %            309.6 %      -40.8 %     7.59
  ```
  Le moteur fabrique **4,97 %**, d'où le R:R de **3,57**. Le même contrat
  afficherait **2,57** ou **7,59** selon l'hypothèse : **le R:R du plan est
  entièrement déterminé par une hypothèse que le moteur prend pour lui-même.**
  Et les limitations servies sont exactement les trois constantes du fichier (BS
  européen, dividendes, smile) — **aucune ne mentionne le mouvement attendu**,
  vérifié sur la liste servie.
  **Où ça s'affiche** : `analysis_page.py:631` (« R:R ») ·
  `opportunities_page.py:553` (« R:R simulé … perte planifiée ») ·
  `options-intel.js:439` (« R:R du plan »). Et `options-intel.js:431` **rend la
  liste « Limites méthodologiques »** : **la carte affiche ses limites, et
  celle-là n'y figure pas.** Le trader lit une méthodologie qui se présente comme
  complète.
  **Classement — famille du 417, pas du 407.** Ce n'est **pas un chiffre faux** :
  un mouvement attendu déduit de l'IV est l'estimation standard, probablement la
  meilleure disponible. Ce qui manque, c'est **l'étiquette** — dans un fichier
  dont c'est le sujet, à trois lignes d'un repli qui, lui, est étiqueté et dégrade
  `model_source`. **Rang 1** ; correction pressentie minuscule et déjà écrite
  juste au-dessus : une ligne de limitation, et au choix la dégradation de
  `model_source`. **Aucun GO, rien d'engagé.**
  **Portée** : la question de ce lot est l'**étiquetage**, pas la formule — je n'ai
  pas vérifié que le mouvement déduit de l'IV soit numériquement le bon
  estimateur. `capital_free_analysis` n'a pas été ouvert au-delà d'un constat : il
  applique lui aussi un **multiplicateur 100 en dur** (`mid * 100`), même
  hypothèse qu'au lot 418 dans un autre fichier — **signalé, non mesuré ici**.
  **Motif de la veine vérifié une cinquième fois, sous sa forme la plus nette** :
  le fichier étiquette un repli, refuse une simulation faute de données, garde un
  calcul derrière un vrai stop — **et laisse passer le seul repli qui s'exécute à
  chaque appel**. Le compteur annoncé au 421 (deux négatifs d'affilée → le dire ;
  trois → changer de famille) **repart à zéro**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 421 — livré** : **le scoring note un dict vide « D, confiance 58 » — mais
  la mesure a réfuté mon hypothèse, et la chaîne a fermé le dossier.** Cinquième
  lot dans la veine des moteurs, cible `vertex/quant/scoring.py` (score global,
  note, confiance). **Lot négatif sur le produit, et c'est le résultat.**
  **La règle que le fichier respecte, et où il ne la tient qu'à moitié.** Ligne
  136 : `out['fundamental_is_proxy'] = not fund_real  # honnêteté : signale si le
  fondamental est un proxy`. Le fichier **sait** qu'un sous-score peut être une
  hypothèse plutôt qu'une mesure, et il le **déclare** — **pour un sous-score sur
  quatre**. Les trois autres prennent des défauts silencieux (`rsi=50`,
  `volx=1.0`, `atr_pct=2.0`) sans aucun drapeau.
  **Mesuré :**
  ```text
  compose({})   global=40  grade=D  confidence=58
                technical=18  momentum=50  fundamental=45  risk=64
                fundamental_is_proxy=True     ← le seul drapeau, et il est correct
  ```
  Un verdict complet, noté et chiffré, **sur rien du tout**. Points gagnés par
  les seules valeurs par défaut : `technical_score({}) = 18` (rsi 50 → +12 dans
  la bande 45-70 · volx 1.0 → +6), contre **0.0** avec les mêmes clés fournies au
  pire réel. Booléens tous `False` dans les deux cas :
  ```text
  mesures RÉELLES au pire (rsi 10, roc −25, rs 0, atr 10 %)   global=11  tech=0   mom=0   risk=42
  mesures ABSENTES (clés retirées)                            global=40  tech=18  mom=50  risk=64
  ```
  **L'absence de mesure vaut 29 points de plus que la pire mesure réelle.**
  **Mon hypothèse était que la confiance s'inversait. La mesure l'a réfutée.**
  Je supposais que `confidence = 100 − min(std × 2.5, 60)` serait **maximale** sur
  un dict vide, les défauts étant peu dispersés. Mesuré : **aucune donnée 58 ·
  cas réel cohérent 66 · cas réel contradictoire 40**. La confiance se comporte
  **correctement**. **Je ne publie donc pas ce défaut, parce qu'il n'existe pas.**
  *Une hypothèse d'explication doit être testée, pas narrée* — la règle a coûté
  ici une trouvaille annoncée.
  **La chaîne ferme le dossier.** Un **seul appelant** dans tout le dépôt,
  `vertex/engines/analysis.py:203`, et le `ind` construit deux lignes plus haut
  porte **les douze clés, toujours**, calculées inconditionnellement depuis la
  série de prix. **Les valeurs par défaut de `scoring.py` ne sont jamais utilisées
  en production** : le comportement mesuré est **inatteignable aujourd'hui**.
  **Ce qui reste est une caractérisation, pas un défaut.** Le module se présente
  comme **pur et réutilisable** (« Pures = testables », liste des clés attendues
  en tête) — une invitation à un second appelant, qui recevrait une note sans
  savoir qu'elle repose sur des défauts. **Classé rang 4**, piège latent, aucune
  conséquence actuelle. **Aucun GO, rien d'engagé.**
  **Portée** : la vérification de chaîne établit que les douze clés sont
  **toujours présentes**, pas qu'elles soient **numériquement saines** ;
  `options_score` n'a pas été ouvert (il reçoit `None` sur ce chemin).
  **Troisième fois d'affilée dans cette veine que la mesure RÉDUIT ce que j'allais
  écrire (416, 418, 419) — et la première où elle l'ANNULE.**
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 419 — livré** : **la forme du 418 bornée — 22 replis, 18 légitimes, 4
  aveuglants, et un RSI de 0 effacé.** Dernier lot de mesure de la tranche : il
  **borne** au lieu d'ouvrir. Le 418 avait trouvé une condition de validation qui
  teste son propre repli ; **ce site est-il isolé ?**
  **Recensement par AST** (`vertex/**/*.py` + `terminal.py`) :
  ```text
  comparaisons de `if` contenant un repli `or CONSTANTE`      25
     dont SANS garde `is None` dans la même condition         22
  ```
  **Témoins, les trois passent** : le site du 418 est retrouvé · la ligne
  `quantity` du même fichier est vue par le détecteur · **et écartée** grâce à
  son `is None`. Le détecteur distingue la forme fautive de la forme correcte
  écrite deux lignes plus haut.
  **Les 22 ouverts un par un, triés par RÔLE et non par forme** : **18 =
  sélection/classement, repli honnête** (« absent → 0 » veut dire « ne qualifie
  pas » : `(fund.get('score') or 0) >= 65`, `(c.get('quality') or 0) > (best…)`,
  comparaisons de chaînes, `or 'UNKNOWN'` volontaire…) ; **4 =
  détection/validation**, où le repli masque ce qu'on cherche.
  **La trouvaille — `vertex/scanner/daily.py:62`, un RSI de 0 est EFFACÉ.**
  `if float(d.get('rsi') or 50) < 45: bits.append('momentum faible')` — `0.0` est
  *falsy*, donc la valeur la plus baissière qui existe devient le neutre **50**.
  Mesuré sur `_avoid_reason`, toutes autres entrées identiques :
  ```text
  rsi = 40  (momentum faible)      → « … · momentum faible »
  rsi = 1   (quasi extrême bas)    → « … · momentum faible »
  rsi = 0   (extrême bas RÉEL)     → « … »        ← la raison DISPARAÎT
  rsi ABSENT                       → « … »        ← même sortie que rsi = 0
  ```
  Le trader reçoit **la même explication** pour « je n'ai pas la donnée » et pour
  « le momentum est au plus bas possible » — et la fonction est **non monotone à
  sa propre frontière** (listée à 1, absente à 0). **Ironie avec le 416** : le
  même indicateur y était **fabriqué à 100** là où il est indéfini ; il est ici
  **effacé à 0** là où il est réel. Deux fautes opposées, une seule cause :
  traiter un extrême légitime comme une donnée manquante.
  **Les deux autres.** `reconciler.py:82` compare
  `(loc.get('multiplier') or 100)` à `(b.get('multiplier') or 100)` ; le 418
  ayant mesuré que le côté courtier ne porte **jamais** de multiplicateur, la
  comparaison oppose toujours le local à un **100 fabriqué** — cohérent avec le
  418, pas un dossier neuf. Le contraste est **quatre lignes plus haut, même
  bloc** : le coût moyen est gardé par `is not None` **et** un dénominateur non
  nul. `portfolio_guard.py:19` compte une exposition **inconnue** comme **zéro**,
  donc `MAX_OPTIONS_REACHED` ne se déclenche pas — **lu, pas mesuré**, et dit
  comme tel.
  **Ce que le lot établit** : la forme du 418 est **rare et le plus souvent
  inoffensive** — 4 sites de détection sur 22 replis, dont 1 défaut réel nouveau,
  1 déjà connu, 1 conséquence d'un défaut connu, 1 signalé sans mesure. **Aucune
  campagne à lancer, et c'était la question.**
  Le nouveau défaut est **rang 2** : la conséquence est un **texte d'explication
  incomplet**, pas un chiffre faux, et seulement sur un RSI exactement nul —
  lequel, mesuré au 416, demande une baisse sans un seul jour de hausse. Rare,
  mais c'est le cas où l'avertissement compte le plus. **Aucun GO.**
  **Portée** : le détecteur ne voit que les replis **littéraux dans une
  comparaison de `if`** ; un repli passé par une variable intermédiaire lui
  échappe et **n'a pas été quantifié**. Les 18 « légitimes » sont classés par
  lecture du rôle, pas par exécution.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 418 — livré** : **le multiplicateur d'option vaut 100 partout, et le seul
  contrôle qui le surveille ne peut pas mordre.** Troisième lot dans la veine des
  moteurs. Cible : `vertex/positions/calculator.py`, dont le docstring pose une
  règle testable — *« donnée absente → None (jamais 0) »*.
  **La règle est tenue partout, sauf sur un champ.** Moteur exécuté en mémoire,
  mêmes entrées, seul le multiplicateur change :
  ```text
  multiplicateur          market_value   P&L      delta   theta   data_quality  issues
  ABSENT / = 100 / = 0       1000.0     +100.0   110.0   -16.0        OK          []
  = 10  (mini-option)         100.0     -800.0    11.0    -1.6        OK          []
  = 22  (ajusté après split)  220.0     -680.0    24.2    -3.52       OK          []
  ```
  Même position : **P&L +100 avec l'hypothèse 100, −800 avec le vrai
  multiplicateur** — changement de signe sur l'argent, Greeks divisés par dix, et
  `data_quality` reste **OK** sans la moindre alerte. **Témoins dans le même
  fichier** : Greeks absents → `delta = None` · `cost_basis = 0` →
  `unrealized_pnl_pct = None` · `mark` absent → `market_value = None` +
  `MISSING_MARK`. **La règle est appliquée partout sauf sur le seul champ qui
  multiplie tout le reste.**
  **Mais la chaîne resserre le diagnostic.**
  ```text
  ibkr_positions.fetch_positions   ne lit QUE symbol, position, avgCost, secType, currency
                                   → `contract.multiplier` n'est JAMAIS demandé à IBKR
  repository.load_positions        construit le dict IBKR sans clé `multiplier`
  models.option_position           `_f(trade.get('multiplier')) or 100.0`  ← le vrai défaut
  calculator.enrich_option         `p.get('multiplier') or 100.0`          ← repli sur un défaut
  ```
  Toute position arrivant au calculateur porte **déjà** 100 : ce n'est pas
  improvisé, c'est une **convention produit assumée**, écrite dans le docstring
  d'`option_position` (« cost = qty × prime × 100 »). Ce que la chaîne montre
  vraiment : **le multiplicateur réel n'est jamais demandé au courtier**. Pour un
  contrat non standard — mini-option, contrat ajusté après un split — le coût
  moyen, la valeur, le P&L et les quatre Greeks sont faux, **sans signal**. Or le
  système **connaît** ce risque : `reconciliation.py:134` lève
  `MULTIPLIER_MISMATCH` (sévérité 3) dès qu'un contrat annonce autre chose que
  100 — mais ce détecteur travaille sur les **contrats**, jamais sur les
  **positions**.
  **Le contrôle qui ne peut pas mordre.** `audit.py:30` :
  `if (p.get('multiplier') or 100) <= 0: errs.append('MULTIPLIER_INVALID')`.
  Exécuté sur toutes les valeurs invalides :
  ```text
  ABSENT → rien · None → rien · 0 → rien (la valeur même que « <= 0 » vise)
  0.0 → rien · -100 → MULTIPLIER_INVALID   ← seul cas qui mord
  ```
  Cause : `or 100` remplace `None` **et** `0` (tous deux falsy) **avant** la
  comparaison — **le contrôle teste son propre repli, pas la donnée**. **Le
  témoin est deux lignes plus haut** : `if p.get('quantity') is None or
  (p.get('quantity') or 0) <= 0` — le `is None` explicite y est, et
  `QUANTITY_INVALID` **mord** (vérifié par exécution), comme `STRIKE_MISSING` et
  `COST_BASIS_INVALID`. **Deux lignes d'écart, la même forme, une seule écrite
  correctement.** Et `MULTIPLIER_INVALID` **n'apparaît dans aucun test** — zéro
  occurrence sur `tests/**`.
  **Classement calibré, pas gonflé — moins grave que le 416 et le 417** :
  l'hypothèse « multiplicateur = 100 » est **juste pour l'écrasante majorité** des
  contrats américains, et elle est **documentée**. **Rang 2** : le multiplicateur
  réel n'est jamais lu chez le courtier alors que le système sait le contrôler
  ailleurs — erreur **silencieuse et multiplicative**, bornée aux contrats non
  standard. **Rang 4** : `MULTIPLIER_INVALID` ne détecte ni l'absence ni le zéro,
  et ne peut de toute façon jamais se déclencher puisque la valeur est fixée à
  100 en amont — **contrôle mort, deux fois**. **Aucun GO, rien d'engagé.**
  **Portée** : un seul moteur, plus la chaîne d'alimentation nécessaire pour
  savoir si le défaut est atteignable — ce parcours a **réduit** le diagnostic.
  `fetch_positions` ne transmet ni `right`, ni `strike`, ni `exp` ; ce qui en
  résulte n'a **pas** été mesuré ici.
  **Motif confirmé sur trois lots** : la bonne pratique est écrite **à quelques
  lignes du défaut** — 416 `pos = 50.0` quand `hi == lo` ; 417 `tp1_resolved` dans
  le même dictionnaire ; 418 le `is None` explicite deux lignes au-dessus.
  *Chercher la règle que le fichier respecte ailleurs, puis l'endroit où il
  l'oublie* est la méthode la plus rentable trouvée depuis le lot 398.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 417 — livré** : **« Rendement +20 séances » — le N affiché n'est pas le N
  du calcul.** Deuxième lot dans la veine des moteurs. Cible :
  `vertex/engines/track_record.py`, **le moteur qui note Vertex lui-même**, dont
  le docstring annonce *« Aucune promesse, que du mesuré »* — d'où la question :
  le mesuré est-il présenté avec son échantillon ?
  **Le mécanisme.** `evaluate()` ne publie un paquet que si `b['n'] >= 5`, mais
  `n` compte les entrées résolues **à au moins un horizon**, alors que chaque
  statistique se calcule sur sa propre liste. Un verdict émis il y a 6 séances
  alimente `n` et `f5`, **pas** `f20`. Le filtre protège le **paquet**, pas
  chaque **nombre publié**.
  **Mesuré — moteur exécuté en mémoire** (ledger fabriqué, `persist._BASE_DIR`
  redirigé, mémo réinitialisé) :
  ```text
  TÉMOIN −  4 entrées                        AUCUN PAQUET (filtre n≥5)   ✔
  TÉMOIN +  5 entrées anciennes              n=5 win_1j=100 win_5j=100 win_20j=100 avg_20j=15.73
  CAS       1 ancienne + 4 à horizon court   n=5 win_1j=20  win_5j=20  win_20j=100 avg_20j=20.0
  ```
  Troisième ligne : le terminal annonce **N = 5**, **20 % de gagnants à 1 et 5
  séances**, et dans la même ligne **100 % de gagnants et +20,0 % de rendement
  moyen à 20 séances** — **assis sur une seule observation**.
  **Ce n'est pas un cas de bord : c'est l'état normal du registre.** Un registre
  qui tourne contient toujours des verdicts trop récents pour +20. Sur un cas
  réaliste — un verdict par séance sur les 40 dernières :
  ```text
  N annoncé                                     39
  observations derrière « +1 séance »           39   (100 % de N)
  observations derrière « +5 séances »          35   ( 90 % de N)
  observations derrière « +20 séances »         20   ( 51 % de N)
  ```
  La colonne « +20 séances » repose **structurellement** sur un sous-ensemble
  strict de `N`, proportion **jamais affichée**. Le cas à une observation est
  l'extrême ; le biais est **permanent**.
  **Où ça s'affiche, et la phrase qui promet ce que le chiffre n'a pas.** Dans la
  **même ligne** de `performance_page.py:443`, `TP1 avant stop` **affiche son
  dénominateur entre parenthèses** (`tp1_resolved`) tandis que `Rdt +20 s`
  n'expose rien et se lit sous le `N` de la ligne — **la bonne pratique existe
  déjà, appliquée à une métrique sur quatre**. Et la légende du graphique dont
  c'est le sujet (L459) déclare *« moyenne réelle des verdicts résolus **(n≥5)**
  — mesure, pas une promesse »* : **faux pour ce chiffre**, `n≥5` filtre le
  paquet, pas l'échantillon de la moyenne à 20 séances. **La phrase promet
  exactement la garantie qui manque.**
  **Le gardien.** `test_evaluate_min_sample_and_no_division_by_zero` (lot 89)
  vérifie le minimum **du paquet** ; sa fixture n'a que **7 cours**, donc `f5` et
  `f20` valent `None` partout et **le cas « un horizon a moins d'observations que
  n » n'est jamais exercé**. À son crédit, il assert `tp1_resolved == 0` : le
  dénominateur est surveillé **là où il est exposé**.
  **Rang 1, sans le gonfler.** Contrairement au 407, **le nombre n'est pas faux**
  — c'est une moyenne réelle d'observations réelles. Ce qui est faux, c'est
  l'**échantillon suggéré** et la **légende**. Défaut d'**honnêteté de
  présentation**, sur la page dont le sujet est la confiance accordée au moteur.
  Correction pressentie, petite : publier le compte par horizon comme le moteur
  le fait **déjà** pour TP1, l'afficher entre parenthèses comme le fait **déjà**
  la colonne TP1, corriger la légende. **Aucun GO, rien d'engagé.**
  **Portée** : un seul moteur, une seule fonction. **`edge_ledger.jsonl` n'existe
  pas sur ce poste** — rien n'est dit de l'ampleur sur les données réelles de
  l'utilisateur ; les proportions viennent d'un registre fabriqué, réaliste mais
  fabriqué.
  **Motif des deux lots de la veine** : dans les deux cas, le code contenait
  **déjà la bonne pratique à côté du défaut** — 416, `pos = 50.0` quand
  `hi == lo` trois lignes plus bas ; 417, `tp1_resolved` dans le même
  dictionnaire. Le défaut n'est pas l'ignorance de la règle, c'est son
  **application incomplète**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 416 — livré** : **un titre qui n'a pas bougé affiche « RSI 100 », et le
  gardien qui dit « neutre » accepte l'extrême.** **Changement de famille
  assumé** : après trois lots sur la couverture des gardiens (413-415), descente
  dans les **moteurs de calcul**.
  **La prémisse, mesurée et fausse.** Le docstring de
  `vertex/engines/indicators.py:13` justifie son choix : *« dn==0 → 100, jamais
  NaN (casserait le JSON) »*. Or :
  ```text
  jsonify({'x': float('nan'), 'y': float('inf')})  →  {"x":null,"y":null}
  ```
  **Flask assainit déjà** — `null` est du JSON valide, que le client rend en
  `—`/`n/d`. *Le témoin a fermé la sonde prévue avant même la mesure.*
  **Ce que rend le moteur, en mémoire** :
  ```text
  série NORMALE (marche aléatoire)            RSI  63.1
  baisse MONOTONE                             RSI   0.0
  hausse MONOTONE (aucune baisse)             RSI 100.0   ← Wilder, CORRECT
  série PLATE (aucun mouvement)               RSI 100.0   ← 0/0 rendu comme l'extrême
  ```
  Deux situations opposées, **même valeur** : un titre halté ou illiquide est
  présenté aussi suracheté qu'une envolée sans un jour de repli. Même choix dans
  la seconde implémentation, `vertex/market/indicators.py:85` (`else 100.0`).
  **Où la valeur arrive** : `analysis.py:40` calcule, L304 place `'rsi':
  round(r)`, `analysis_page.py:472` affiche `kv('RSI', d.rsi)` — **le 100 est
  montré tel quel**.
  **Ce que la mesure a corrigé dans mon propre diagnostic.** `committee.py:97`
  produit la phrase « *Timing défavorable : RSI 100 (suracheté). On patiente.* ».
  Mesuré, elle **est** atteignable sur un plateau de 3 à 45 jours (`dernier >
  MM50` vrai, RSI 100) — **mais dans ces séries il n'y a aucun jour de baisse
  depuis le début**, et « aucune baisse ⇒ 100 » **est** la définition de Wilder :
  contre-intuitif, pas faux. Sonde : neutraliser le seul cas `up == 0 ET dn == 0`
  laisse le plateau-après-hausse à 100, la moyenne des hausses gardant la mémoire
  de la montée. **Le défaut est donc plus étroit que je ne l'ai cru** — titre
  **plat depuis toujours** : RSI indéfini rendu **100**, faux et **affiché** ;
  plateau après hausse : **correct**. Et sur une série parfaitement plate
  `dernier > MM50` est faux, donc la phrase dit « sous la MM50 » : **le nombre
  ment à l'écran, la phrase non.**
  **Le gardien.** `tests/test_calculations_golden.py:193` s'appelle
  `test_rsi_flat_series_is_neutral_not_zero` et assert `30 <= val <= 100` : le
  **nom** promet la neutralité, l'**assertion** admet l'extrême. Il garde contre
  le `0` (baissier extrême), pas contre le `100`. **Il ne bloque pas la
  correction** : sonde rendant `50.0` sur le cas sans mouvement → **31 tests
  golden passent**.
  **Classé rang 1**, mais **nettement moins grave que le 407** : là le HHI était
  faux d'un facteur 170 dans le cas *nominal* ; ici la valeur est juste dans le
  cas dominant et fausse au bord. Correction pressentie : rendre `None` quand il
  n'y a **ni hausse ni baisse** sur la fenêtre — 2 lignes, 2 moteurs, plus le nom
  du gardien à accorder à son assertion. **Aucun GO, rien d'engagé.**
  **Portée** : **un seul** indicateur ouvert. Le recensement statique donne
  **641 divisions dans `vertex/**` hors UI, dont 481 à dénominateur non constant
  et non protégé** — c'est un **vivier trié par la forme**, pas une liste de
  défauts (leçon du 408) ; **aucune campagne lancée**, rien mesuré sur les 480
  autres.
  **Note de cadence tranchée** : la veine « couverture des gardiens sur les
  octets servis » reste **close en rendement** ; celle des **moteurs de calcul**
  vient de s'ouvrir et paie mieux.
  Suite **2864 passed / 0 skipped**, inchangée. Sonde **restaurée à l'octet** et
  moteur ré-interrogé après restauration ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 415 — livré** : **288 identifiants servis, aucun doublon ; le gardien
  n'en surveille que 3 pages sur 8.** Deux éléments qui portent le même `id`,
  c'est un défaut **silencieux** : `getElementById` rend **le premier**, le
  second n'est jamais mis à jour — carte figée, aucune erreur en console. Le
  trader voit une donnée qui ne bouge plus et n'a aucun moyen de le savoir.
  Périmètre : les octets servis (8 pages + 26 scripts), `<script>` **retirés du
  marquage** — une chaîne dans du JS n'est pas un nœud.
  ```text
  1. doublon dans le marquage servi        288 identifiants → 0 doublon
  2. collision marquage × gabarit JS       1 candidat  → ouvert
  3. id littéral émis DANS une répétition  1 sur 113   → ouvert
  ```
  **Le candidat n°2** (`#op-compare`, `/opportunities`) : les deux porteurs sont
  dans des **vues mutuellement exclusives** — `renderRadar()` (L240) émet
  `<div id="op-compare">`, `renderOptions()` (L509) émet
  `<button id="op-compare">`, et **les deux écrasent le même
  `$('op-body').innerHTML`**. Ils ne coexistent jamais. Mieux : `renderCompare()`
  n'a **qu'un seul appelant**, L256, dans `renderRadar` — la fonction qui vient
  de créer le `div`. **Aucune conséquence.** (L'`id` du bouton n'est cherché par
  personne, son handler est un `onclick` inline : nom en double sans effet,
  rang 4.)
  **Le candidat n°3** est la forme qui fabrique vraiment des doublons — un `id`
  fixe dans un gabarit passé à `.map()`. Ouvert : `'<div id="strat-pf-' + i + '"'`,
  relu par `getElementById('strat-pf-' + i)` — **interpolé avec l'indice de
  boucle**, unique par élément, code correct ; mon extracteur tronquait au `+`.
  **Zéro doublon réel sur les trois classes.**
  **L'instrument, deux fois.** Une heuristique de proximité (« un `.map(` dans
  les 700 caractères précédents ») donnait **9 candidats** ; remplacée par un
  vrai **appariement de parenthèses** — le `.map(` doit se **fermer** après
  l'identifiant → **1**. Témoins des deux côtés : un `id` dans un `.map()`
  fabriqué est détecté, un `id` hors `.map()` ne l'est pas. Et une version
  intermédiaire du test d'englobement remontait jusqu'au premier guillemet
  rencontré : elle tombait sur `class="` et jugeait le mauvais contexte. Elle
  produisait des lignes propres, alignées, et fausses. Jetée.
  **Ce que le filet couvre, mesuré par mutation.** `test_no_duplicate_ids` ne
  visite que **3 pages sur 8** (`/`, `/portfolio`, `/system`) :
  ```text
  doublon posé sur /markets  (page NON visitée)  →  suite complète : 2864 passed
  doublon posé sur /         (page visitée)      →  test_no_duplicate_ids : FAILED
  ```
  **Le gardien mord — là où il regarde.** Sur `/markets`, `/opportunities`,
  `/analysis`, `/options`, `/journal`, un identifiant dupliqué serait servi au
  navigateur sans qu'aucun des 2 864 tests ne le signale. **Non comblé**
  (invariant non violé, mesuré 8/8 ; gardien-pour-faire-un-lot interdit depuis le
  384) — **rang 3**. **Avertissement pour qui étendra** : la regex du gardien,
  `id="([^"]+)"`, **ne retire pas les `<script>`** et compte donc les
  identifiants des gabarits JS comme des nœuds ; élargir sans corriger ce point
  ferait remonter des doublons qui n'existent pas dans le DOM — exactement le
  `#op-compare` ci-dessus.
  **Portée** : identifiants **statiquement observables** ; un `id` entièrement
  calculé échapperait, et le DOM final n'a pas été rejoué en navigateur — la
  classe 3 est une **borne statique**, pas une observation.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  (`git status` vide, suite de référence rejouée après restauration) ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 414 — livré** : **les 167 boutons servis sont tous câblés ; un bouton
  mort fabriqué par le JS servi ne serait vu par aucun test.** Un bouton qui ne
  fait rien est le défaut le plus banal d'une interface, et le plus humiliant :
  le trader clique, rien ne se passe, il ne sait pas si c'est l'application ou
  lui. Trois tests déclarent l'invariant ; personne n'avait mesuré ce qu'ils
  couvrent **des octets servis**.
  ```text
  boutons dans le HTML rendu (scripts retirés)   85
  boutons fabriqués par le JS servi              82   (inline de page 64 · /static 18)
  total                                         167
  ```
  **Correction de cohérence interne** : une première passe annonçait **231** — 
  elle comptait deux fois les boutons vivant dans un `<script>` inline.
  **Verdict, avec un critère durci** (l'id doit être un **littéral cité** ET à
  moins de 70 caractères d'un accesseur) : **inline 18 · id 87 · `data-*` 62 ·
  SANS ÉCOUTEUR 0**. Les 62 `data-*` ont été **ouverts** : 16 attributs
  distincts, chacun avec son site de consommation nommé (`data-open-analysis` 53,
  `data-entity-menu` 10, `data-close-drawer`/`data-close-modal`,
  `data-filter-key`, `data-i` → `btns.forEach(b => b.addEventListener(…))`).
  **Cinq témoins** : bouton nu, `data-zzz-lot414` inconnu, id inexistant → morts ;
  `onclick` réel et `id="vx-collapse-btn"` (accroché via l'aide `$()`) → câblés.
  **L'instrument s'est encore trompé, et c'est la même faute.** Un premier
  durcissement exigeant `getElementById('id')` donnait **55 boutons « morts »**,
  dont `vx-collapse-btn` et `vx-notifs-btn` — manifestement vivants. Cause :
  `vx-shell.js` accroche par une **aide locale**, `$('vx-collapse-btn')`.
  **Troisième répétition** (409 `emptyCard`, 413 `get(…)`, 414 `$(…)`) → le
  critère est devenu agnostique à l'accesseur.
  **Ce que les trois gardiens couvrent, mesuré par mutation.** Un bouton mort
  déposé **dans le shell** : `test_every_button_has_handler` **MORD** ;
  `test_ui_v3::test_no_dead_buttons` **passe**, car il **court-circuite** dès
  qu'un attribut `data-` existe — ce qui **exempte 62 des 167 boutons** ; le
  troisième passe aussi. Le même bouton déposé **dans un fichier JS servi**
  (`vx-entities.js`) : **les trois passent**, et la suite complète ne rend
  **qu'un** échec — **l'empreinte `/static` du 361**, qui ne dit rien du bouton.
  Empreinte mise à jour comme le flux de travail l'impose de toute façon :
  ```text
  octet /static modifié · empreinte mise à jour · bouton mort servi
  suite complète →  2864 passed
  ```
  **Entièrement verte, avec un bouton inerte servi sur les 8 pages.** Raison :
  `test_every_button_has_handler` balaie `vertex/ui/pages/*.py` et le shell,
  **pas `vertex/static/**/*.js`** — où vivent **18 des 167** boutons. Même défaut
  de périmètre que le **385** (recensement s'arrêtant à `vertex/`) et le **381**
  (liste gardée qui n'est pas celle qui est servie), sur un troisième objet.
  **Bilan : le produit est sain (0 mort sur 167), le filet ne couvre que
  149/167.** Trou **non comblé** : livrer un gardien « parce qu'un trou existe »
  est interdit depuis le 384, et l'invariant n'est pas violé aujourd'hui.
  **Classé rang 3** — élargir le périmètre demande d'accepter la délégation
  inter-fichiers, c'est une décision de conception.
  **Portée** : le contrôle établit qu'un écouteur **existe**, pas que le clic
  produise le bon effet ; l'analyse est statique, et un attribut calculé au vol
  échapperait — mesuré à **0** occurrence dans le corpus servi.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  et vérifiées **par l'instrument lui-même** (361 → 5 passed, `git status`
  vide) ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 413 — livré** : **les 156 chemins que le client peut demander — aucun ne
  pointe dans le vide.** Un chemin d'API mal écrit côté client ne casse rien de
  visible : la requête part, le serveur répond 404, la carte reste sur son état
  vide — **honnête en apparence, mais pour une mauvaise raison**. Personne
  n'avait vérifié la correspondance.
  **Périmètre = les octets servis**, pas les sources : les 8 pages demandées au
  serveur en mémoire (8 × HTTP 200), puis **chaque `<script src>` demandé au
  serveur à son tour**.
  ```text
  pages 8 · scripts externes servis 26 · blocs inline 15 · corpus 1 243 931 octets
  résolution par app.url_map.match() → les 190 routes réellement enregistrées
  ```
  **L'instrument s'est trompé deux fois, et c'est mesuré.** (1) Les 26 fichiers
  `/static` n'étaient pas dans le corpus — recherche disque avec un chemin faux :
  `515 108` octets / 42 chemins, contre `798 881` / 52 une fois **demandés au
  serveur**. (2) Le détecteur ne connaissait que `fetch(`, alors que
  `options-intel.js:466` appelle `get('/api/options/strategies/'+sym)` via une
  **aide locale** — **répétition exacte de la leçon du lot 409**, avec une autre
  enveloppe. (3) Trois faux morts par normalisation : la concaténation **en
  queue** (`'/api/options/gex/' + encodeURIComponent(sym)`) est désormais
  reconnue comme segment dynamique.
  **Témoins** : route réelle → OK · route inventée → `NotFound` · segment
  dynamique → OK ; et **de bout en bout** sur les trois formes d'écriture (appel
  direct, aide locale, concaténation en queue), les trois chemins sont retrouvés.
  Un `fetch('/api/reco-inexistante-413')` déposé dans un fichier servi **serait**
  rapporté.
  ```text
  chemins distincts confrontés à l'url_map     156
     résolvent                                 149   (dont 8 par segment dynamique)
     ne résolvent pas                            7   ← ouverts un par un
  appels /api distincts                          55   tous résolus
  ```
  **Les 7 sont 7 faux positifs de l'extracteur, aucune requête** : `/1%IV` et
  `/100` (unités affichées), `/api` et `/static` (tests de préfixe,
  `vx-router.js:42`), `/api/ibkr`, `/api/positions`, `/api/account` (préfixes de
  politique de cache, `vx-core.js:228/272`). **Zéro chemin mort**, et le zéro est
  **substantiel** : 156 littéraux confrontés à un `url_map` exécuté, les 7
  restants lus dans leur ligne.
  **Trouvaille annexe, triviale — dite comme telle.** `/api/account` figure dans
  **les deux** listes de cache du client (`PERSIST_DENY`, `LIVE_TTL`) alors que
  **0 route sur 190**, **0 appel sur 55** et **0 occurrence ailleurs dans le
  dépôt** ne lui correspondent : **entrée morte**, elle ne dénie rien et ne
  raccourcit aucun TTL. **Aucune conséquence visible pour le trader** — classée
  **rang 4**, non corrigée : ce serait exactement le « changement gratuit » que la
  boucle s'interdit. Les 5 autres préfixes **mordent**, ce qui rend le `0` lisible.
  **Portée mesurée, pas affirmée** : l'extraction est statique, donc un chemin
  entièrement calculé lui échapperait — sur **91** appels `fetch(` du corpus
  servi, **85** ont un littéral en premier argument et **6** une variable
  (`url`, `u`, `href`) ; les 6 sont ouverts : ce sont **les tuyaux eux-mêmes**
  (implémentation de `VX.fetch`, `fetch` de fragment du routeur), qui reçoivent
  les URL construites aux 85 sites littéraux — **aucun endpoint distinct ne s'y
  cache**. Le lot établit que les routes **existent**, pas ce qu'elles renvoient.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** (la
  sonde vit dans le scratchpad) ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 412 — livré** : **le gardien de la règle n°3 détecte le changement
  d'asset, mais n'impose pas le bump.** La règle critique n°3 protège le **repli
  hors-ligne** : si un octet de `/static` change sans bump du service worker, un
  visiteur déjà venu et hors ligne garde l'ancienne copie. Le gardien du lot 361
  est censé l'imposer — **personne n'avait vérifié qu'il l'impose vraiment**.
  **D'abord la concordance** : version SERVIE (`system.py`) `v187` = version
  ENREGISTRÉE (`test_sw_cache_scope_lot361.py`) `v187`, et l'empreinte
  enregistrée `f83645b51509…` **égale** celle recalculée sur les 54 fichiers de
  `/static`. Le contrat décrit bien l'état servi.
  **L'expérience — le scénario du développeur pressé.** Le message d'aide du
  gardien demande deux choses : *« 1. bumper `const CACHE='td-shell-vN'` … ;
  2. remettre à jour `_EMPREINTE` et `_SW_VERSION` »*. Simulé exactement : un
  octet ajouté à `vertex/static/vertex/css/tokens.css`, `_EMPREINTE` mise à jour
  **comme demandé**, `CACHE='td-shell-v187'` **laissé tel quel**.
  ```text
  asset modifié · empreinte mise à jour · CACHE inchangé (v187)
  suite complète →  2864 passed
  ```
  **Verte.** Un fichier servi a changé, le repli hors-ligne n'a pas été purgé, et
  rien dans les 2 864 tests ne le signale. Pourquoi :
  `test_les_assets_servis_correspondent_a_la_version_enregistree` compare
  l'empreinte — satisfaite dès qu'on la réécrit ; et
  `test_la_version_enregistree_n_est_jamais_en_avance_sur_le_service_worker`
  n'exige que `_SW_VERSION <= _version()`, soit `187 <= 187`. **Aucun test
  n'exige que la version AUGMENTE quand l'empreinte change.**
  **Ce qui atténue, et qu'il faut dire** : le trou n'est **pas silencieux**.
  Seconde sonde : sans réécrire l'empreinte, le gardien **échoue d'abord**, avec
  l'instruction en toutes lettres (`E   1. bumper \`const CACHE='td-shell-vN'\`
  …`). Il faut donc **obéir à la moitié de la consigne** pour produire le défaut,
  pas simplement l'oublier. Le gardien **informe**, il n'**automatise** pas.
  **Pourquoi je ne corrige pas** : « exiger que `_SW_VERSION` augmente quand
  `_EMPREINTE` change » **n'est pas implémentable dans le fichier lui-même** —
  les deux constantes sont éditées par le commit qu'on veut contrôler, donc
  l'ancienne valeur a déjà disparu à l'exécution du test. Un registre append-only
  déplace le problème sans le fermer. **La seule vérification robuste lit
  l'historique git** (aucun test ne lit git aujourd'hui) : instrument d'un autre
  ordre, **décision de conception**, pas réparation d'agent. **Classé rang 3.**
  *Un contrat écrit dans le fichier qu'il contrôle ne peut pas s'imposer à qui
  édite ce fichier.*
  **Portée** : ce lot teste **une** faille précise — mettre à jour l'empreinte
  sans bumper. Il ne dit pas le gardien faible ailleurs : le lot 394 avait rejoué
  la règle n°3 avec une faute réelle (fichier `/static` modifié, rien d'autre
  touché) et **elle mordait**. Le gardien **détecte** le changement d'asset ; il
  **n'impose pas** la conséquence.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  (`git status` vide, empreinte recalculée = enregistrée, v187 = v187) ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 411 — livré** : **les 59 provenances déclarées — 2 nomment une origine
  sans producteur, et elles ne s'affichent jamais.** Chaque carte de Vertex
  déclare sa provenance (`source:`) : c'est le contrat d'honnêteté visible par le
  trader — *d'où vient ce que je regarde ?* Personne n'avait vérifié que
  l'étiquette corresponde à la donnée réellement tracée.
  ```text
  champs `source:`                          59   (dans 26 fichiers)
     EXPRESSION (variable, ternaire)        32   ← propage la provenance réelle
     LITTÉRAL (chaîne fixe)                 27   ← peut dériver
  ```
  Les 32 expressions sont **honnêtes par construction** : elles transportent ce
  que le serveur a déclaré. Seuls les 27 littéraux peuvent mentir. **Témoin de
  l'instrument** : les deux étiquettes connues du 407 sont bien retrouvées parmi
  eux.
  **Les 27 confrontés un par un** à l'existence **et** au producteur de l'origine
  nommée : `scenario_pricer` ×6 (module présent) · `SCAN` ×5 — l'étiquette du
  client **duplique la déclaration du serveur** (`source='SCAN'`, 3 sites) au
  lieu d'en inventer une · `board options` · `calendrier moteur` ×3 (`/cal-feed`,
  7 réf.) · `moteur track-record` · `Moteur de régimes` · `journal local` ×2
  (`set('vxJournal')` ×2) · « clôtures déclarées » L642 (`set('myTradesClosed')`,
  carte **rendue**, étiquette exacte). **→ 25 sur 27 exactes**, et les **2**
  seules sans producteur sont celles du dossier 406/407.
  **Le détail qui change la description du dossier.** Trois cartes de
  `/portfolio` portent « clôtures déclarées », et elles ne se valent pas :
  ```text
  L610  equityCard    ← E().equity() → myTradesEquity → 0 écrivain → JAMAIS rendue
  L617  drawdownCard  ← même série                                 → JAMAIS rendue
  L642  heatmapCard   ← withPl (myTradesClosed)                    → RENDUE, exacte
  ```
  Donc **ces deux étiquettes ne sont jamais affichées** : elles vivent sur une
  branche inatteignable. Le préjudice du 406/407 est bien **le graphique absent
  et la consigne impossible**, *pas* une provenance mensongère à l'écran. C'est
  une précision, pas une atténuation — **le HHI faux du 407, lui, est affiché**.
  **Quatrième bornage consécutif** (402, 408, 409, 411). Le zéro est
  **substantiel** : 27 littéraux confrontés un par un, pas comptés.
  **Portée** : le contrôle porte sur la correspondance étiquette ↔ origine
  nommée (existe-t-elle, produit-elle) ; il ne dit rien de la **justesse de la
  valeur** tracée. Et les 32 expressions n'ont pas été suivies jusqu'à leur
  source : elles sont réputées honnêtes parce qu'elles propagent — raisonnement
  de conception, pas mesure.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 409 — livré** : **les 8 pages balayées — une seule consigne impossible,
  celle du 406.** Le lot 406 avait trouvé **un** état vide qui donne au trader une
  consigne que le code ne peut pas honorer ; les 8 pages n'avaient pas été
  balayées.
  **L'instrument s'est trompé, et le témoin l'a montré.** Premier détecteur :
  compter les appels `states.empty(` → 85 trouvés, **mais pas le site du 406**.
  Raison : `portfolio_page.py` et `performance_page.py` passent par une **aide
  locale** (`emptyCard(host, reason, action)`) et mon détecteur comptait la
  **définition** de l'aide, jamais ses appels. *Compter les appels d'une fonction
  sans compter ceux de ses enveloppes, c'est mesurer la mécanique et rater
  l'usage.* Corrigé :
  ```text
  sites d'état vide réellement affichés   88   (direct 83 · via une aide 5)
  ```
  Témoin après correction : `portfolio_page.py:623` **est retrouvé**.
  **Le filtre** : un état vide qui **décrit** une absence (« VIX non fourni par le
  dernier scan ») n'est pas un état vide qui **promet**. Le défaut du 406 a une
  forme précise — *le message dit de faire quelque chose, et le faire ne produira
  pas le résultat annoncé*. Sur tournures d'instruction (« se construit »,
  « renseigne », « marque une », « ajoutez », « créez », « lancer un scan », « au
  fil des »…) : **12 / 88**.
  **Les 12 vérifiés un par un**, mécanisme cherché dans le code et non supposé :
  ```text
  « lancer un scan depuis Système » ×3     /api/rescan (7 réf.)            TENABLE
  « Marque une idée Suivre »               followStock() + bouton servi    TENABLE
  « créez un suivi depuis une analyse »    followStock(entry/stop/tgt)     TENABLE
  « ajoutez les titres à surveiller »      set('vxWatchlist') ×2           TENABLE
  « ouvrir une analyse pour le détail »    route /analysis                 TENABLE
  « le flux se remplit au rythme… »        flux d'événements live          TENABLE
  « renseigne le champ erreur »            j-mistake → e.mistake           TENABLE
  « renseigne le champ leçon »             j-lesson  → e.lesson            TENABLE
  « renseigne état émotionnel »            j-emo     → e.emo               TENABLE
  « elle se construit au fil des clôtures » set('myTradesEquity') → 0 site ★ IMPOSSIBLE
  ```
  Les trois consignes du Journal méritaient l'examen car elles nomment des champs
  précis : vérifié, `performance_page.py` L338-341 construit `j-lesson`,
  `j-mistake`, `j-emo` **et** L355 les écrit dans l'entrée. Le trader peut les
  renseigner ; les cartes se rempliront.
  **Une seule consigne est impossible sur les 8 pages : celle du 406.** Comme le
  408 pour le `|| 0` du 407, ce lot **borne** le dossier au lieu de l'élargir —
  la correction reste **un texte ou un mécanisme, sur une seule carte**. Le zéro
  est **substantiel** : 12 promesses examinées une par une, pas un comptage
  global.
  **Portée** : le filtre repose sur une liste de tournures françaises, écrite
  dans le rapport pour qu'elle soit contestable ; une consigne formulée
  autrement passerait au travers. Et « TENABLE » signifie *le mécanisme existe et
  écrit la donnée lue* — pas que le parcours soit ergonomique.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun. **Prochaine échéance : bilan n°10
  au lot 410.**

- **Lot 408 — livré** : **le `|| 0` du lot 407 est isolé, pas une famille.**
  Question laissée ouverte par le 407 : cas isolé ou premier d'une famille ? La
  réponse change la **taille du dossier de rang 1**, donc la décision.
  **Recensement brut** — périmètre servi (`vertex/**` `.py`+`.js` et
  `terminal.py`, les six modules reliques exclus) :
  ```text
  lignes portant `|| 0` / `?? 0` / `or 0`      440   (dans 70 fichiers)
  occurrences (plusieurs par ligne possible)   606
     dont terminal.py                          206
  ```
  Instrument validé : le site du 407 est retrouvé, un fichier sans motif ne rend
  rien. **Ce chiffre ne prouve rien et n'est pas présenté comme un problème** :
  `(r.get('change') or 0)` dans une somme est un choix de modélisation. Un
  `|| 0` n'est un défaut que si l'opérande peut être **absent** *et* que le zéro
  est ensuite **présenté comme une mesure**.
  **Le filtre décisif — les charges utiles envoyées aux moteurs.** C'est
  exactement la forme du 407 : un `null` transformé en `0`, transmis à une API et
  **déclaré réel**.
  ```text
  appels POST sur chemin servi                          25
     dont un `|| 0` / `?? 0` dans la charge utile        1
  ```
  **Un seul — celui du 407.** Aucune autre page n'envoie une absence maquillée en
  zéro à un moteur. **Le défaut est isolé** : le dossier reste un site, une page,
  une décision.
  **Le filtre de forme, et ce qu'il vaut vraiment.** Un `|| 0` sur un **appel**
  dont le résultat est, ailleurs dans le même fichier, comparé à `null` : 128
  appels, **53 candidats**. **Ce ne sont pas des trouvailles, c'est un vivier
  d'hypothèses** — montré plutôt qu'affirmé en ouvrant le candidat le plus
  sensible, celui qui toucherait le P&L d'une position IBKR :
  `positions/repository.py:63` — `'cost': (raw.get('avgCost') or 0) * (qty or 0)
  if raw.get('avgCost') is not None and qty else None`. **Il est sain** : le
  `or 0` est gardé, `cost` vaut `None` quand `avgCost` manque. Faux positif de
  forme, résolu en le lisant. *Un vivier trié par la forme ne devient une liste
  de défauts qu'après lecture, un par un ; publier les 53 comme des trouvailles
  aurait été malhonnête.*
  **Conséquence pratique pour la décision** : corriger 406/407 ne demande **pas
  une campagne** — un seul site à changer, une seule cause (`myCapital` jamais
  écrit).
  **Portée** : le filtre décisif ne voit que les payloads construits à moins de
  12 lignes d'un `method:'POST'` ; une charge utile assemblée plus loin
  échapperait au comptage. Le recensement large est purement textuel : il ne
  distingue pas un opérande qui peut manquer d'un compteur qui vaut réellement
  zéro. C'est dit, pas contourné.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 407 — livré** : **le `|| 0` qui fabrique une alerte de concentration.**
  Le lot 406 avait trouvé deux clés lues mais jamais écrites, et suivi **une**
  conséquence (la courbe d'équité qui ne s'affiche jamais). Ce lot suit **la
  seconde — et elle est plus grave**.
  **D'abord borner.** `vx-entities.js` lit **11** clés et en écrit **9** :
  **exactement deux orphelines**, `myCapital` et `myTradesEquity`, pas une de
  plus. Et sur les 8 pages servies, **un seul module** les consomme —
  `portfolio_page.py` (L296, L586, L718). Le périmètre du dossier 406 est
  **confirmé et clos** : 2 accesseurs, 1 page.
  **La conséquence non suivie.** L718 envoie
  `cash: E().capital() || 0` avec `simulated: false`. Or `capital()` vaut
  **toujours `null`** : le `|| 0` **convertit silencieusement une donnée absente
  en un zéro**, transmis à `/api/portfolio/team` et **déclaré réel**
  (`provenance='REAL'`). Trois lignes plus bas, le fichier écrit lui-même la
  règle qu'il enfreint : *« Manquant/insuffisant n'est jamais présenté comme
  zéro. »*
  **Ce que ce zéro change, mesuré** — moteur exécuté deux fois sur les **mêmes**
  positions :
  ```text
  mesure          cash = 0        cash = 50 000    verdict
  equity          4 100           54 100           DIFFÈRE
  hhi             0.5003          0.0029           DIFFÈRE  (×170)
  issue_gardien   True            False            DIFFÈRE
  ```
  `hhi` est calculé sur l'équité **cash compris** ; envoyer 0 gonfle la
  concentration de deux ordres de grandeur. Et la page **affiche** ce chiffre :
  `if (risk.hhi >= 0.66) → « Concentration très élevée (HHI …) »`.
  **Le seuil est-il franchi ? Oui, mesuré** :
  ```text
  1 position    HHI cash=0  1.0     → ALERTE       | cash=50k 0.0015 → aucune   ★ FABRIQUÉE
  2 positions   HHI cash=0  0.5003  → aucune       | cash=50k 0.0029 → aucune
  4 positions   HHI cash=0  0.3019  → aucune       | cash=50k 0.0073 → aucune
  ```
  **Avec une seule position déclarée, le terminal affiche « Concentration très
  élevée (HHI 1) » — un artefact du `|| 0`, pas une lecture du portefeuille.**
  Le blob actuel porte 2 positions, donc l'alerte ne part pas aujourd'hui ; mais
  **le HHI affiché reste faux d'un facteur ~170** et servi comme mesure réelle.
  **Une conséquence qui, elle, n'atteint pas l'écran — dite quand même.**
  `team_view` conclut **toujours** « pas de gardien (cash/monétaire) »
  (`ROLE_TARGETS[GOALKEEPER] = (1,1)`, `if snapshot.cash > 0` jamais vrai). Mais
  la page **ne consomme pas** `d.team` — `team` n'y désigne que le nom de la vue
  « Synthèse ». Vérifié : calculé, **pas affiché**. Je le dis plutôt que de
  grossir le dossier.
  **Trois issues, aucune engagée** (toutes touchent un octet servi ou un moteur) :
  (1) ne pas envoyer un zéro pour une absence ; (2) **alimenter `myCapital`** —
  même décision que le volet 1 du 406, elle règle les deux d'un coup,
  **RECOMMANDÉ** ; (3) a minima masquer le HHI et son alerte quand le cash est
  inconnu.
  **Portée** : les chiffres viennent d'une exécution directe de `risk_engine` et
  `stress_tests` sur des positions **fabriquées pour la mesure** — c'est la
  méthode qui est démontrée, pas le portefeuille du trader ; `beta` et
  `pire_stress` ressortent `None` faute d'entrées, leur sensibilité au cash
  **n'est pas affirmée**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ;
  moteurs exécutés en mémoire, sans serveur ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 406 — livré** : **sept clés synchronisées que rien n'écrit, et une
  promesse intenable sur `/portfolio`.** Après trois lots négatifs (403, 404,
  405), celui-ci trouve — et c'est **visible par l'utilisateur**.
  **La question** : le contrat `DESK_KEYS` (règle critique n°1) liste **17 clés**
  synchronisées. Jamais posée : ces 17 clés sont-elles réellement **produites**
  par le client ? Une clé listée que rien n'écrit, c'est la synchronisation d'un
  fantôme.
  **L'instrument s'est trompé d'abord.** Première passe : « 13 clés sur 17 sans
  écrivain », dont `myTrades` — la clé des positions du trader. Absurde. J'avais
  exclu `vx-entities.js` du corpus parce qu'il porte la **liste** `DESK_KEYS`,
  sans voir qu'il porte aussi **les écrivains** (`set('myTrades', list)` et
  quinze autres). *Exclure un fichier pour ce qu'il déclare, c'est se priver de
  ce qu'il fait.* Corrigé : exclusion des **lignes** de déclaration, pas des
  fichiers. Témoin négatif : une clé inventée ne trouve aucun site.
  ```text
  clés du contrat DESK_KEYS                              17
     avec au moins un site d'écriture en production      10
     SANS aucun site d'écriture                           7
  ```
  Les sept : `myTradesEquity` · `myRecosClosed` · `myCapital` · `simCash` ·
  `simStart` · `simTrades` · `simClosed`. Vérification exhaustive des écritures
  littérales sur tout `vertex/**` et `terminal.py` : **aucune** ne les vise.
  Blob desk **réel** : **6 clés sur 17** portent des données, **aucune des sept**
  n'y figure, et aucune clé hors contrat.
  **LE DÉFAUT VISIBLE.** `portfolio_page.py` L296/L586/L718 lisent
  `E().capital()` et `E().equity()`, soit `myCapital` et `myTradesEquity` —
  **jamais écrits**. Donc `eq` vaut **toujours `[]`** : la branche
  `if(eq.length>=2…)` est **inatteignable**, la **courbe d'équité** et le
  **drawdown** ne peuvent **jamais** s'afficher, et `cash` vaut toujours
  `null`/`0`.
  **Le problème n'est pas la carte vide — c'est ce qu'elle promet** : « *Courbe
  d'équité indisponible — elle se construit au fil des clôtures de positions
  déclarées.* » Or clôturer une position exécute `set('myTrades', list);
  set('myTradesClosed', closed);` (`vx-entities.js:171`) — **jamais**
  `myTradesEquity`. Le trader peut déclarer autant de clôtures qu'il veut : la
  courbe n'apparaîtra pas. **L'état vide donne une consigne qui ne peut pas
  aboutir** — pas un chiffre inventé, mais son cousin : une promesse que le code
  ne peut pas tenir.
  **L'« évidence » à NE SURTOUT PAS FAIRE.** Élaguer `DESK_KEYS` de 17 à 10
  serait une **perte de données**, pas un nettoyage : le push desk est
  **last-writer-wins total** (mécanisme du lot 362), et un profil de navigateur
  détenant encore `simCash`/`simTrades`/`simClosed` (l'ère du simulateur) les
  verrait **cesser d'être synchronisées puis disparaître du serveur** au premier
  push suivant. Le blob mesuré ici ne les contient pas — mais il ne dit rien des
  autres profils, et il n'y a pas de retour en arrière.
  **Dossier de rang 1, deux volets, aucun engagé** : (1) **la promesse de
  `/portfolio`** — soit alimenter `myTradesEquity` à la clôture (le comportement
  que le texte promet), soit réécrire l'état vide ; **les deux touchent un octet
  servi** (bump SW, MD5, gardiens), c'est une décision. (2) **Les 7 clés** —
  recommandation : **les garder** (coût nul, le push n'envoie que les clés
  réellement présentes ; le retrait, lui, est irréversible).
  **Portée** : la recherche porte sur les écritures **littérales** ; les 53 sites
  `set(<variable>, …)` du dépôt ont été vérifiés — aucun ne concerne le magasin
  desk. Et « présente dans le blob » vaut pour **un** profil, celui de cette
  machine — c'est précisément pourquoi l'élagage est déconseillé.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ;
  `desk_data.json` **lu seulement**, jamais écrit ; SW `td-shell-v187` ; écart
  runtime final aucun.

- **Lot 405 — livré** : **aucun octet mort dans `/static` — 54 sur 54 réellement
  référencés.** Balayage textuel, quelques secondes.
  **Pourquoi ça compte** : le service worker met en cache **tout `/static`**
  (règle n°3). Un fichier statique mort n'est donc pas du poids de dépôt — ce
  sont des **octets téléchargés et conservés sur l'appareil de l'utilisateur**,
  plus une entrée de plus dans l'empreinte que le gardien du lot 361 doit
  suivre. Périmètre : **54 fichiers · 824 Ko** (34 `.js`, 17 `.css`, 2 `.woff2`,
  1 `.md`).
  **Instrument validé avant emploi** : recherche du **nom de base** dans tout le
  texte du dépôt (1 218 fichiers), volontairement **large** — `<script src>`,
  `url()` CSS, `@import`, chaîne Python composant le chemin ; chercher un chemin
  exact aurait fabriqué de faux morts. **Témoin positif** :
  `zz-temoin-mort-405.css` déposé dans `vertex/static/vertex/css/` → **seul
  signalé**, aucun des 54 fichiers réels. Témoin supprimé aussitôt, arbre
  vérifié propre.
  **Le zéro rendu substantiel plutôt que décoratif — trois filtres** :
  ```text
  fichiers statiques                                        54
     cités depuis la PRODUCTION (vertex/**, terminal.py)    54
     cités seulement depuis un AUTRE fichier static          0
     cités seulement dans docs/ ou tests/                    0
     cités NULLE PART                                        0
  ```
  Puis le **contrôle de second ordre**, celui qui distingue vraiment : un fichier
  référencé uniquement par un module lui-même mort est mort par transitivité.
  `CLAUDE.md` et les lots 327/381 nomment six modules `vertex/ui/` sans aucun
  consommateur en production. Sur **302 modules de production examinés (dont 6
  connus morts)** : **0 fichier statique n'est cité que par un module mort**.
  Les 54 sont donc tous atteints depuis du code vivant.
  **Ce que ce lot dit du dossier « code mort »** : le poids mort est **dans le
  monolithe Python** — 604 Ko de `PAGE_*` jamais servis (374), `vx_kit.JS` qui
  n'atteint aucune page (381), cinq modules reliques (327) — **pas dans les
  octets servis**. `/static` est propre ; inutile d'y chercher un gain de poids
  en arbitrant les dossiers de rang 3.
  **Portée** : recherche **textuelle par nom de base**. Elle prouve qu'un nom
  apparaît dans du code vivant, pas que la ligne qui le contient soit
  **exécutée**. Aller plus loin supposerait de relever les requêtes réelles d'un
  navigateur sur les 8 pages — donc de lancer le serveur DEMO, donc de fabriquer
  un point dans `breadth_history.json` : coût non justifié pour confirmer un
  zéro déjà filtré trois fois.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** — le
  témoin créé par la sonde a été supprimé par la sonde, `git status` vide de
  bout en bout ; empreinte SW inchangée ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 404 — livré** : **les assertions avalées par un `except` — zéro, et le
  zéro est substantiel.** Symétrique exact du lot 403 : celui-ci cherchait les
  tests qui **n'affirment rien**, celui-là ceux qui **affirment, mais dont
  l'affirmation ne peut pas les faire tomber** parce qu'un `except` l'attrape
  (`try: assert … except Exception: pass`). Balayage AST, quelques secondes.
  **Le détecteur** ne signale un `assert` que si les trois conditions tiennent :
  il est dans le **`body`** d'un `try` ; un handler attrape `AssertionError`
  (`except:` nu, `Exception`, `BaseException`, `AssertionError`, ou un tuple en
  contenant un) ; ce handler ne **relance pas** et n'appelle pas `pytest.fail`.
  Exclus à dessein : `except ValueError`, handler qui relance, `try/finally`
  sans handler, `assert` situé **dans** le handler. **Témoin avant emploi** :
  3 fautes plantées signalées, **6 cas légitimes muets**.
  ```text
                          assert au total   dans un `try`   AVALÉS
  tests/                          5 663             91         0
  vertex/                             2              0         0
  terminal.py                         1              0         0
  ```
  **Côté tests, le zéro est substantiel** : 91 assertions vivent réellement dans
  un `try`, et la répartition est sans exception — **91 en `try/finally` SANS
  handler**, le motif de remise en état imposé depuis le lot 387, **0** sous un
  handler attrapant `AssertionError`. Aucun `except` de la suite n'est en
  position de bâillonner une assertion.
  **Côté production, le zéro est trivial — et il faut le dire** : `vertex/`
  contient **2** `assert` en tout, `terminal.py` **1**. Un « 0 avalé » sur
  3 assertions ne prouve presque rien ; le présenter comme un succès serait un
  zéro décoratif.
  **Ce que font ces 3 assertions**, puisqu'on les a comptées : extraction de
  l'Opportunity Brief JS vérifiée à l'import (`terminal.py:5887`) · précondition
  direction LONG (`call_selector.py:21`) · **`assert decision in
  FINAL_DECISIONS`** (`executive_engine.py:161`), qui garde le **vocabulaire
  canonique du verdict final**. Or un `assert` **disparaît** sous `python -O`.
  Vérifié plutôt que supposé : **aucun lanceur n'utilise `-O`** et
  `PYTHONOPTIMIZE` n'apparaît nulle part dans le dépôt — les trois sont actives
  sur tous les chemins de lancement documentés. Ce n'est pas un défaut mais une
  **fragilité latente** ; **classée rang 4**, non corrigée : ajouter une garde
  ici serait le changement gratuit que la boucle s'interdit depuis le 384.
  **Portée** : le détecteur raisonne sur la structure syntaxique — une assertion
  neutralisée par un `xfail`, un `contextlib.suppress` ou une aide capturant
  l'exception ne serait pas vue ; et rien n'est dit de la **justesse** des
  5 663 assertions, seulement qu'aucune n'est muselée.
  Avec le 403, la question « la suite peut-elle échouer ? » est traitée sous ses
  deux angles — assertions **absentes** et assertions **muselées** — les deux
  réponses négatives, les deux dénominateurs mesurés.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** — ni
  production, ni test, `git status` vide de bout en bout ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 403 — livré** : **les tests qui n'affirment rien — deux, et tous deux
  légitimes.** Point de contrôle **peu coûteux** délibérément choisi après les
  35 minutes du lot 402 : un balayage AST, quelques secondes. Question : la
  suite contient-elle des tests qui **ne peuvent pas échouer** ?
  Trois familles cherchées : **A** test sans aucune assertion (ni `assert`, ni
  `pytest.raises`, ni appel à une aide locale qui assère) · **B** `assert` sur un
  littéral toujours vrai (`assert True`, `assert 1`) · **C** `assert (cond,
  'message')` — **le tuple**. Un tuple non vide est toujours vrai : la
  parenthèse de trop **annule l'assertion**, et le code se lit comme correct.
  C'est la plus dangereuse des trois.
  **Instrument validé avant emploi** : quatre fautes plantées, toutes détectées ;
  **trois témoins légitimes muets** — un `assert` normal, un test qui délègue à
  une aide assérante, un test à `pytest.raises`. Le détecteur suit **un niveau
  d'indirection**, sans quoi tout test délégant sa vérification aurait été
  faussement accusé.
  ```text
  fonctions test_* analysées                    2 563
     A. sans AUCUNE assertion                       2
     B. assert sur un littéral toujours vrai        0
     C. assert sur un TUPLE                         0
  ```
  **Zéro `assert True`, zéro assertion annulée par une parenthèse.** Résultat
  négatif, mais dénominateur mesuré et instrument prouvé.
  *Note de dénominateur* : 2 563 fonctions pour **2 864** tests collectés —
  l'écart vient des **55 fonctions paramétrées** (59 décorateurs `parametrize`,
  33 à liste littérale soit 152 cas, et **26 dont les cas sont calculés**, non
  énumérables sans exécuter). Je ne prétends pas reconstituer 2 864 par
  l'analyse statique ; je dis d'où vient l'écart.
  **Les deux tests sans assertion** — `test_save_failure_is_silent` et
  `test_save_failure_is_silent_by_contract` — vérifient que `persist.save_json`
  **ne lève pas** quand l'écriture échoue. L'assertion est implicite et
  légitime. Mais ils ont un **angle mort** : ils passeraient aussi si
  `save_json` devenait un **no-op**. Plutôt que de l'affirmer, mesuré —
  `save_json` remplacé par un `return` nu : les **2 tests passent** (aveugles,
  confirmé) tandis que **leurs voisins de fichier tombent**
  (`test_round_trip`, `test_save_load_roundtrip_faithful`). L'angle mort est
  **réel et couvert dans le même fichier** : les durcir n'ajouterait aucune
  protection que la suite n'ait déjà. *Un test sans assertion n'est pas
  nécessairement creux — encore faut-il vérifier qui couvre ce qu'il ne voit
  pas.* Production restaurée à l'octet.
  **Portée** : le détecteur voit les assertions écrites dans le fichier, avec un
  seul niveau d'indirection ; et « 0 littéral toujours vrai » ne dit rien des
  assertions fausses mais non littérales — `assert x == x` passerait au travers.
  Suite **2864 passed / 0 skipped**, inchangée. Aucun fichier touché — ni
  production, ni test ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 402 — livré** : **les 300 fichiers rejoués seuls — la suite ne dépend
  pas de son ordre.** Le lot 401 avait prouvé qu'**une** dépendance d'ordre
  existait et l'avait corrigée ; il n'avait pas dit s'il y en avait d'autres.
  Ce lot balaie le périmètre entier : **chaque fichier de test rejoué seul**,
  dans un interpréteur neuf. Aucun code, aucun gardien, aucun test — résultat
  **négatif et mesuré**.
  ```text
  fichiers rejoués SEULS                    300 / 300
     échecs                                   0
     skips                                    0
     tests exécutés en isolation          2 864
     tests de la suite complète           2 864   ← identique
  ```
  L'égalité des deux totaux est le contrôle qui compte : elle prouve qu'aucun
  test n'a été **perdu** en chemin (fichier non collecté, import silencieusement
  cassé). Chaque test a tourné dans les deux régimes, même verdict.
  **L'instrument a échoué une fois — et je l'ai vu avant de conclure.** Le
  premier balayage, lancé en `nohup … &`, n'était **pas mort** quand j'ai cru
  l'avoir arrêté ; un second a écrit dans le même fichier de sortie →
  **339 lignes pour 195 fichiers distincts sur 300**. Un rapport écrit à ce
  moment-là aurait annoncé « 0 échec » sur un périmètre **incomplet de 35 %**,
  en le présentant comme complet. Ce qui l'a révélé n'est pas une intuition mais
  un **contrôle de cohérence interne** : lignes, fichiers distincts et
  dénominateur attendu devaient coïncider — ils ne coïncidaient pas.
  *Un « 0 » n'a de valeur que si le dénominateur est vérifié, pas supposé.*
  Bénéfice secondaire de l'incident : les 202 fichiers passés deux fois donnent
  une mesure gratuite de reproductibilité — **202 verdicts identiques sur 202**.
  Harnais validé avant emploi par un **témoin positif** (fichier délibérément
  faux → `1 failed`).
  **Portée assumée** : ce balayage teste UNE direction — *un fichier a-t-il
  besoin des autres pour passer ?* Il ne teste pas l'inverse (*un fichier
  casse-t-il les suivants ?*, celle du 401, trouvée par un autre chemin), ni les
  ordres intermédiaires. Établi exactement : **isolation complète → vert
  partout**, **ordre nominal → vert**.
  **Un chiffre trouvé en chemin.** Les 300 exécutions isolées tournent avec un
  `persist._BASE_DIR` **réel** — la redirection accidentelle du lot 392 ne
  s'applique pas hors de son module. Effet mesuré :
  `skyler_decisions.json` **11 → 18 entrées**, soit **7 décisions journalisées
  dans le journal réel de l'utilisateur** pour une passe isolée complète ;
  `skyler_memory.json` réécrit, taille stable. Ce n'est pas une piste nouvelle :
  c'est le **dossier de rang 2 du lot 401, désormais chiffré**. Restauré à
  l'octet.
  Suite **2864 passed / 0 skipped**, inchangée. Aucun fichier touché — ni
  production, ni test ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 401 — livré** : **un gardien qui passait selon l'ordre d'exécution.**
  Point de contrôle **jamais balayé** : les tests qui mutent un état global sans
  le remettre en état. Le lot 387 en avait trouvé **un**, par hasard ; le
  périmètre entier n'avait jamais été mesuré.
  **Deux instruments, tous deux corrigés avant de servir.** Statique (AST) :
  3 034 fonctions, 50 mutent un global, 36 protégées (`monkeypatch`/`finally`/
  teardown), **14 nues** — mais ce ne sont que des **hypothèses**, une fonction
  d'aide mutante pouvant être appelée depuis un test protégé. Exécution :
  empreinte de l'état global avant/après **chaque** test. Première version :
  **84 « fuites » dont 42 fausses**, parce que `pytest_runtest_teardown`
  s'exécute **avant** les finalizers de `monkeypatch` — corrigé en enveloppant
  `pytest_runtest_protocol`. Témoin négatif qui mordait aussi :
  `PYTEST_CURRENT_TEST` est réécrit à chaque phase, exclu de l'empreinte. Et le
  premier témoin « monkeypatch » écrivait une **valeur déjà présente** —
  écriture idempotente, donc invisible, donc concluante à tort (leçon du 389) :
  rejoué avec une valeur réellement différente et une assertion prouvant la
  mutation effective. **84 → 8 fuites réelles sur 2 864 tests.**
  **La trouvaille.** `test_skyler_sweep_x1.py::test_sweep_route_and_no_journaling`
  restaurait avec `if v is None: scan_state.pop(k, None)`. Or
  `vertex/app/state.py` initialise `'market_ctx': None` : **la clé existe et sa
  valeur légitime EST `None`**. La remise en état la **supprimait** donc du dict
  partagé, pour tout le reste de la session. Prouvé par la plus petite
  reproduction possible — **deux fichiers** : `pytest test_skyler_sweep_x1.py
  test_state.py` → **1 failed**, chacun seul → vert ; idem sur la queue de
  66 fichiers (1 failed / 664 passed). Le test qui tombe est
  `test_scan_state_has_expected_keys` — **le gardien dont le métier est
  exactement de vérifier que les 8 clés documentées existent**. Son verdict
  dépendait de l'ordre d'exécution.
  *Une hypothèse testée et écartée* : j'ai cru que la suite complète passait
  grâce à une seconde fuite laissant `market_ctx` non-`None` ; placer ce fichier
  devant laisse l'échec. Je ne sais pas quel test recrée la clé dans la suite
  complète, et je le dis plutôt que de l'inventer.
  **Corrigé** en mémorisant la **présence** de la clé et non sa vérité. Rouge →
  vert sur les deux périmètres ; **témoin** : ancienne logique remise → rouge à
  nouveau, c'est bien elle qui décidait.
  **Les 7 autres fuites** (gamma_surveillance ×3, market_context, options_routes,
  portfolio_stress, pretrade) : vérifié qu'**aucune ne retire une clé
  documentée** — rejouées ensemble puis suivies du gardien, `72 passed`.
  Pollutions **latentes**, pas défauts actifs ; les corriger à l'aveugle
  changerait ce qu'elles mesurent. **Classées.**
  **Un dossier ouvert, non exécuté (rang 2).** La fixture de portée module de
  `test_refus_variable_lot392.py` — mon propre lot 392 — assigne
  `persist._BASE_DIR = tempfile.mkdtemp(...)` **sans restaurer** : la
  persistance est redirigée pour **678 tests**, 24 % de la suite. Et ce défaut
  **protège** aujourd'hui : rejouée seule avec un `_BASE_DIR` réel, cette queue
  écrit dans `skyler_decisions.json` et `skyler_memory.json`. **Restaurer
  naïvement réintroduirait des écritures réelles dans le stockage de
  l'utilisateur.** Le bon correctif est de décider **où** la persistance doit
  pointer pendant la suite — et ce n'est pas neutre :
  `test_funnel_positions_match_desk` lit délibérément le **vrai**
  `desk_data.json`. Décision, pas réparation.
  Suite **2864 passed / 0 skipped**, inchangée — aucun test ajouté, délibérément.
  Un seul fichier de test modifié ; aucune production ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 399 — livré** : **qui, dans la suite, sort sur Internet ?** Le lot 398
  avait neutralisé deux sorties réseau au passage, sans savoir s'il en restait.
  Ce lot mesure au lieu de supposer.
  **L'instrument, validé avant emploi.** Plugin pytest à deux capteurs : un
  **faux proxy local** — `HTTPS_PROXY` pointe dessus pendant la session, donc
  tout `CONNECT` y atterrit, **y compris ceux de libcurl/`curl_cffi`**, le
  transport de yfinance, qu'un patch de `socket` **ne verrait pas** — plus un
  patch de `socket.connect` pour les connexions directes. Réponse `502`, aucun
  blocage : la sortie échoue comme hors ligne, le verdict des tests ne change
  pas. **Témoin positif obligatoire** : yfinance capté, `requests` capté, test
  sans réseau muet. *Sans ce contrôle, un « 0 sortie » n'aurait rien valu.*
  **Mesure : 3 sorties sur 2 864 tests.** Test le plus lent : 1,52 s, aucun
  au-delà — mais c'est parce que le proxy échoue vite ; sur une machine
  connectée, les trois aboutissent.
  **(1) `en.wikipedia.org`, à l'IMPORT** — `vertex/data/universe.py` L16 appelle
  `get_index_members()` au niveau module ; sans cache frais, `constituents.py`
  va chercher 3 listes d'indices (**15 s de timeout par requête**) et écrit
  `constituents_cache.json`, soit un **23ᵉ fichier runtime**. Vérifié : couvert
  par `*_cache.json` dans `.gitignore`, **aucun risque de commit**. C'est un
  comportement de **produit**, voulu et documenté — mais il s'applique aussi à
  `pytest`. Je ne touche pas à la production de ma propre initiative :
  **classé en dossier (rang 4)**.
  **(2) `test_company_twin_never_invents`** → yfinance via `_fetch_profile`,
  **qui n'entre dans aucune de ses assertions**. Sortie inutile : neutralisée,
  verdict identique (hors ligne le fetch échouait déjà).
  **(3) `/desc` — le test écrivait dans le dépôt de l'utilisateur.** Et c'est un
  test que **j'ai écrit moi-même au lot 392**. `terminal.py` L1983 : quand le
  fetch yfinance **réussit**, la route écrit `desc_cache.json` **à la racine du
  dépôt** ; le test appelle cette route à chaque passe. Le défaut était
  **doublement invisible** — le réseau échoue ici, et le recensement du lot 389
  ne pouvait pas le voir parce que **l'écriture est conditionnée à la RÉUSSITE
  du fetch** : un recensement statique fait hors ligne ne pouvait pas la relier
  à ce test. *Une écriture conditionnelle au réseau échappe à un recensement
  fait hors ligne.* **Preuve directe sans réseau** (`yf.Ticker` remplacé par un
  faux qui réussit) : sans isolation → racine écrite ; avec l'isolation du
  399 → tmp seulement, racine intacte ; le fichier créé par la sonde a été
  supprimé par la sonde.
  **Corrigé** : `_DESC_PATH` et `_desc_cache` isolés dans ce seul test — la
  route reste la vraie, seule sa destination change. La sortie réseau est
  **conservée délibérément** : ce test existe pour vérifier qu'une réponse
  yfinance réelle sur un symbole inexistant ne remplit aucun champ ; la
  supprimer le réduirait à sa branche hors ligne.
  **Résultat : sorties réseau 3 → 2, écritures dans le dépôt depuis la suite
  1 → 0.** Suite **2864 passed / 0 skipped**, inchangée — aucun test ajouté, et
  c'est délibéré. Aucun fichier de production touché ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 398 — livré** : **les 2 tests skippés étaient morts depuis leur
  naissance.** Quatrième lot court. Point de contrôle **jamais examiné en
  26 lots** : la suite affiche `2 skipped` depuis des dizaines de rapports —
  personne n'a jamais regardé **lesquels**.
  Ce sont les deux tests de `tests/test_cross_page_consistency.py`, créé le
  **2026-07-12** (`fa234ca`) et **jamais modifié depuis**. Leurs skips sont
  **structurels, pas environnementaux** : `/scan` sérialise `scan_state`, vide
  sous pytest parce qu'**aucun test de la suite ne déclenche de scan** —
  mesure : ce fichier est le **seul des 300** à appeler `/scan`, et ses deux
  appels sont dans le test skippé lui-même. Même mécanique pour
  `options_board`. **Ces deux tests n'ont jamais tourné une seule fois** ; ils
  étaient comptés dans la suite et ne protégeaient rien.
  **Valaient-ils d'être réveillés ?** Mesuré avant de toucher quoi que ce soit,
  par trois mutations de **production** + un témoin, rejouées dans
  l'environnement pytest réel sur le fichier final : filtre `CALL → CALLS` de
  `pulse.py` — le filtre est écrit **deux fois**, `overview.py` L42 et
  `pulse.py` L34, sur le même board → **T2 mord** ; `/api/ticker` servant un
  prix autre que le `detail` du scan → **T1 mord (A)** ; `/scan` transformant
  `rows` sans transformer `detail` → **T1 mord (B)** ; témoin (docstring
  reformulée) → muet. Production restaurée à l'octet entre chaque.
  **Réparés** : une fixture alimente `scan_state` **en place** puis restaure
  dans un `finally` (convention de `test_options_intelligence_lot6.py`, leçon
  du 387) ; les `pytest.skip` conditionnels deviennent des **assertions** — une
  entrée manquante est désormais un échec, plus un silence. Deux effets de bord
  neutralisés dans T1 par `monkeypatch` : `options_pack` (**sortie réseau**) et
  `_company.get` (**écriture de `company_cache.json` depuis la suite**) —
  aucun des deux ne participe à l'invariant, et les laisser aurait réintroduit
  le défaut fermé au lot 389.
  **Résultat : 2862 passed / 2 skipped → 2864 passed / 0 skipped.** La suite
  n'a plus un seul test inerte. Aucun fichier de production touché ; snapshot
  runtime 22 fichiers, écart final aucun ; SW `td-shell-v187`.
  *Limite assumée : T1 tourne sur une entrée injectée — il prouve que les
  routes ne déforment pas ce que le scan produit, pas que le scan produise des
  prix justes.*

- **Lot 397 — livré** : **le registre confronté à lui-même.** Troisième lot
  court — aucun code, aucun gardien, aucun test ; une seule ligne corrigée dans
  un rapport.
  **Point de contrôle jamais fait en 25 lots** : la mémoire de la boucle
  elle-même. Rien ne vérifie le registre, et c'est pourtant lui qu'on relit
  pour décider — une omission y serait **invisible autrement**.
  **Présence : 25 sur 25.** Chaque lot 372→396 a son rapport, sa ligne d'index
  et son bloc STATUS. Mon premier détecteur en signalait **deux manquants** —
  **faux** : les lots 380 et 390 sont des **bilans**, dont le bloc prend la
  forme `## BILAN — veille active, lots N → M` et non `**Lot N — livré**`. Le
  détecteur ne connaissait qu'une forme. *Encore l'instrument avant le
  document.*
  **Exactitude : un écart réel.** La présence ne dit rien de la justesse. La
  chaîne des 25 comptes de suite est **strictement monotone et exacte** — 2645
  au lot 372, 2862 aujourd'hui — sans une seule erreur de transcription en
  25 lots de tenue de registre ; c'est la première fois que c'est vérifié
  plutôt que supposé. Mais **le lot 394 : l'index affirme `v187` alors que le
  rapport ne l'écrit nulle part**, quand les 24 autres l'enregistrent dans
  leurs « Vérifications du cycle ». L'assertion du registre n'était **adossée à
  rien** — vraie par ailleurs, puisque le lot n'a touché aucun octet servi,
  mais invérifiable depuis sa source. **Cette fois ce n'était pas le
  détecteur** : la ligne manquait réellement. Corrigée → **0 écart sur 25**.
  L'écart trouvé est du genre le plus discret qui soit : *un chiffre affirmé
  dans le registre sans source dans le rapport*. Ni la suite, ni les gardiens,
  ni une relecture ne l'auraient révélé, puisque la valeur était juste.
  **Portée** : deux des quatre colonnes confrontées (suite, SW) ; la version du
  cœur est constante et le verdict est déclaratif. Et le contrôle porte sur la
  **concordance interne** du registre, pas sur sa fidélité aux faits.
  Aucun fichier de production touché, écart runtime aucun. Suite **2862 /
  2 skipped, inchangée**. SW v187.

- **Lot 396 — livré** : **les octets servis n'ont pas bougé.** Deuxième lot
  court consécutif — aucun code, aucun gardien, aucun test — et c'est encore
  le bon résultat.
  **Point de contrôle différent de celui du 395**, conformément à la règle
  *un constat se vérifie, il ne se répète pas* : la preuve la plus forte de la
  boucle, non refaite depuis le **lot 390** — le MD5 des 8 pages servies.
  **8/8 IDENTIQUES.** Six lots plus tard, dont deux ayant modifié des fichiers
  de test et un ayant corrigé une docstring, **pas un octet servi n'a bougé**.
  La discipline « aucun fichier de production touché depuis le lot 372 » est
  désormais vérifiée par la mesure, pas seulement affirmée.
  **La sonde a reproduit le dossier de rang 1 du 391 à l'identique** : lancer
  le serveur DEMO pour ce contrôle a ajouté un **17ᵉ point** à
  `breadth_history.json` — `2026-08-09`, `a50 50 · a200 45 · net −4 ·
  health 37`, mêmes valeurs que les seize précédentes. **Le dossier n'est pas
  théorique : il se reproduit à chaque démarrage en mode démo**, y compris
  celui de l'agent. Restauré à l'octet (retour à 16 points).
  Trois fichiers runtime touchés cette fois contre huit au lot 390 — l'écart
  tient à la durée du scan, pas à un changement de comportement ; je ne
  l'interprète pas plus loin.
  **Portée** : le MD5 prouve que le HTML servi est identique, il ne dit rien
  des fichiers `/static` (couverts par l'empreinte du gardien SW, rejouée au
  394), et il vaut pour l'état du dépôt, pas pour ce qu'un utilisateur a en
  cache.
  Serveur arrêté (port 5002 fermé), écart runtime final aucun, arbre propre.
  Suite **2862 / 2 skipped, inchangée**. SW v187.

- **Lot 395 — livré** : **rien à faire, vérifié.** Aucun code, aucun gardien,
  aucun test ajouté — **c'est le résultat, pas un défaut d'exécution**.
  Le 393 a constaté l'épuisement des pistes fines, le 394 l'a confirmé en
  allant vérifier ailleurs. Toutes les veines sont closes **par la mesure** :
  audit des gardiens par mutation (384, 27 mutations → 2 trouvailles) ·
  écritures runtime par la suite (389, 2 trouvailles) · refus API littéraux
  (377, 39 refus / 39 motivés) et construits en variable (392, 30 routes,
  0 muet) · promesses de retour littérales (375) et imbriquées (393, 0 fausse)
  · rejeu des gardiens anciens (394, 7/8 mordent, l'écart était une docstring).
  Un gardien de plus serait le changement gratuit que la boucle s'interdit
  depuis le 384.
  **Mais un constat se vérifie, il ne se répète pas.** Reprendre la liste des
  pistes sans la contrôler serait exactement la faute commise huit fois dans
  cette tranche : faire confiance à ce qu'on transporte. Les deux items
  restants ont donc été re-mesurés. Le commentaire
  « MIROIR EXACT de `__DESK_KEYS` (terminal.py) » est **toujours présent**
  (`vx-entities.js:18`) et **toujours faux** — `__DESK_KEYS` n'existe plus
  depuis la purge É1. Les sites de concaténation sont **conformes** au
  décompte du 374 (4 appels `_extract(PAGE_DAILY, …)`, dont 3 à constantes).
  Aucune dérive entre la mémoire de la boucle et le dépôt.
  **Une asymétrie assumée plutôt que cachée.** Le lot 394 vient de corriger une
  docstring fausse dans un fichier de test ; ce commentaire-ci, du même genre,
  reste différé. La raison n'est pas le coût d'édition mais **l'invalidation de
  cache** : `vx-entities.js` est SERVI, donc le corriger impose un bump de
  service worker, la mise à jour de `_EMPREINTE`, et purge la copie hors-ligne
  de l'utilisateur. Pour un commentaire, c'est disproportionné — et c'est une
  décision, pas un effet de bord de lot. **Règle qui en sort : un énoncé faux
  se corrige immédiatement là où c'est gratuit, et se verse aux dossiers là où
  cela coûte au produit.**
  Arbre propre, **aucun fichier touché** (ni production ni test), écart runtime
  aucun. Suite **2862 / 2 skipped, inchangée**. SW v187.
  **La matière utile n'est plus technique, elle est décisionnelle** : purge des
  7 points MSFT (388) et scan de démo dans `breadth_history` (391) en tête.

- **Lot 394 — livré** : **les gardiens anciens, jamais rejoués — 7 sur 8
  mordent encore.** Une vérification plutôt qu'une piste : le lot 393 ayant
  constaté l'épuisement des pistes fines, ce lot répond à une question laissée
  ouverte par le **bilan n°8** — *« les gardiens non ciblés restent non
  vérifiés »*. **Aucun gardien ajouté**, une seule correction, dans un fichier
  de test.
  **Le dénominateur** : sur 300 fichiers de test, **290 n'ont jamais été
  confrontés à une faute réelle** (179 estampillés d'un lot < 380, 111 sans
  numéro) ; seuls les 10 de la tranche 380-393 l'avaient été au lot 390.
  **L'échantillon, choisi par un critère et non au hasard** : les gardiens que
  `CLAUDE.md` désigne nommément pour ses règles critiques — si l'un d'eux a
  pourri, c'est une règle du produit qui n'est plus tenue. **Mordent** : clé
  retirée de l'ancre `vx_kit` · JS servi rendu syntaxiquement invalide ·
  fichier `/static` modifié sans bump d'empreinte · `sanitize_news` retiré de
  la sortie IBKR · filtre d'URL de la sortie IA neutralisé · rotation des
  sauvegardes desk à 0 · bleu non-marque injecté dans un octet servi. Témoin
  muet, état runtime sans écart.
  **Le huitième ne mord pas — et ce n'est pas un gardien pourri.**
  `test_desk_sync_keys_single_source_of_truth` compare `vx_kit.JS` et
  `journal.JS` et **n'a jamais regardé le fichier statique servi**. Le lot 381
  avait déjà comblé ce trou de couverture avec
  `test_desk_keys_servies_lot381.py`. Ce qu'il n'avait **pas** corrigé, c'est
  la **docstring**, qui affirmait « la source de vérité servie est vx_kit (kit
  global, présent sur toutes les pages) » — **faux depuis le 381**, qui a
  mesuré que ces 21 727 o n'atteignent aucune des 8 pages et que `journal.py`
  est un module mort. Un lecteur ouvrant ce test pour comprendre la règle n°1 y
  lisait le contraire de ce que le dépôt fait. **Corrigée** : elle dit
  désormais ce que le test couvre, ce qu'il ne couvre pas, et renvoie au
  gardien du 381 — les deux sont complémentaires, l'un verrouille l'ancre de
  comparaison, l'autre ce que le navigateur reçoit.
  **Deux ancres fautives corrigées avant de conclure** : `--vx-radius`
  n'existe pas dans `tokens.css`, la première tentative sur la règle n°3 n'a
  donc rien mesuré ; rejouée sur `--vx-canvas`, elle mord. *Une ancre absente
  n'est pas un résultat : c'est une mesure qui n'a pas eu lieu.* Sans cette
  reprise j'aurais annoncé un trou sur le service worker.
  **Portée** : 8 gardiens sur 290, c'est un **sondage**. Ce que le lot établit
  précisément : les gardiens des règles critiques n'ont pas pourri, et le seul
  écart trouvé est une **documentation périmée**, pas une protection perdue.
  Suite **2862 / 2 skipped, inchangée** — aucun test ajouté, délibérément.
  SW v187.

- **Lot 393 — livré** : **les promesses de retour imbriquées — il ne fallait
  pas d'analyseur.** Dernier angle mort déclaré du lot 375, qui écrivait :
  *« vérifier les formes IMBRIQUÉES demanderait un analyseur d'un autre
  ordre »*. **C'était chercher du mauvais côté** : une promesse de retour se
  vérifie en **appelant** la fonction — l'exécution tranche ce que l'analyse
  statique ne sait pas suivre. C'est la vraie trouvaille du lot, et elle porte
  sur la méthode plutôt que sur le code.
  **Dénominateur** : 7 fonctions portent une promesse « Retourne {…} », dont
  **5 couvertes par le 375** (au moins un retour littéral) et **2 déléguées**.
  Le trou déclaré était réel mais **étroit** — le dire évite de faire passer un
  lot mince pour une percée.
  **Verdict, prouvé par exécution** avec les fixtures de la suite et non des
  entrées fabriquées : `grade_packet` promet `{overall, warnings,
  actionable_allowed}` et les rend toutes · `select_calls` promet
  `{per_category, primary, rejected, notes}` et les rend toutes. **Zéro clé
  manquante.**
  **Troisième cas, déjà connu, re-mesuré** : `options_for_position` énumère
  **12 identifiants nus** et son `pack()` interne en rend **13** — `delta` non
  déclaré : **sous-déclaration, pas promesse fausse**. Identique au 375.
  Détail de méthode : ma première extraction cherchait des clés **entre
  quotes** alors que la docstring les écrit **nues** — l'instrument avant le
  code, encore.
  Gardien `tests/test_promesses_imbriquees_lot393.py` (6 tests) : dénominateur
  (si une promesse perdait son retour littéral, elle basculerait dans l'angle
  mort du 375 sans signal) · les deux déléguées **par exécution** · la
  troisième **statiquement** · anti-péremption de la sous-déclaration. ROUGE
  ×3, et **le témoin vaut plus que les trois** : déclarer `delta` — la
  correction que quelqu'un fera un jour — **ne casse pas le gardien**. *Un
  gardien qui punit la correction est pire qu'aucun gardien.*
  **Portée** : lot mince, assumé. Il ne prouve rien sur les promesses formulées
  autrement, et la vérification par exécution ne couvre **qu'un chemin par
  fonction**.
  **Les pistes fines sont épuisées** : refus API littéraux (377) et en variable
  (392), écritures runtime par la suite (389), promesses de retour littérales
  (375) et imbriquées (393) — toutes closes. Ne restent que la concaténation à
  constantes (374, sans enjeu d'honnêteté) et le commentaire périmé de
  `vx-entities.js` (différé : un octet servi pour un gain nul). **Aucune ne
  mérite un lot** ; la matière utile est dans les dossiers du rang 1, en
  attente de décision.
  Suite 2856 → **2862** / 2 skipped. SW v187.

- **Lot 392 — livré** : **les refus construits en variable — l'angle mort
  déclaré du lot 377, mesuré, et PROPRE.** Le détecteur du 377 déballe
  `jsonify(...)` puis exige un dict **littéral** : une réponse assemblée dans
  une variable lui échappe. Il le disait ; ce lot le mesure.
  **Dénominateur resserré par la mesure.** 417 retours littéraux couverts par
  le 377 · **393 par variable** dans l'angle mort — mais **359 sont des aides
  internes** : seuls **34 sont dans une route**, **31 servis**, soit **30
  routes**. *Un dénominateur non trié aurait fait croire à un trou deux fois
  plus grand qu'il n'est.*
  **Verdict prouvé à l'exécution.** Les 30 routes sollicitées avec des entrées
  que le serveur doit refuser — symbole inexistant, corps vide, identifiant
  inconnu — et c'est la **réponse réellement servie** qui est lue, pas le
  code : **12 refus, 12 motivés, 0 MUET**. Les motifs prennent plusieurs
  formes honnêtes (`reason`, `error`, `available: false`, `empty` +
  `generator`, `audit_trail`). Trois réponses sans clé de motif ne sont **pas**
  des refus et n'inventent rien : `/desc` rend des chaînes vides et
  `employees: null`, `/api/positions/state` des zéros avec la note « jamais
  estimés en agrégat », `/api/desk` un `{}`. Une absence rendue comme une
  absence.
  **Deux fois l'instrument en cause.** (a) Ma sonde accusait
  `run_startup_sequence` d'être un refus muet — son motif vit **entièrement
  dans `steps`**, chaque étape portant son statut et son message ; ma liste de
  clés ne contenait pas `steps`. Neuvième fois de la tranche. (b) **Trois
  mutations fautives** sur la preuve ROUGE : `greeks_note` vit dans
  `recalculator.py` et non `positions_api`, `reason` ne vient pas
  d'`analysis_api`, et pour `/desc` j'avais muté une branche **non atteinte**
  — sans réseau, `yf.Ticker` échoue et le chemin servi est l'initialisation du
  dict.
  **Et la mutation corrigée a sali un cache.** Elle a écrit une description
  inventée dans `desc_cache.json`, que le code restauré relisait ensuite : la
  suite restait rouge après restauration. *Restaurer le code ne suffit pas
  quand la mutation a écrit sur disque — il faut vérifier l'état runtime, pas
  seulement l'arbre git.* Fichier supprimé (il n'existait pas avant), écart
  final aucun.
  **Un 22ᵉ fichier runtime découvert par cet incident** : `desc_cache.json`
  n'apparaît qu'après une récupération réussie et manquait aux 21 inventoriés
  depuis le 388. Le gardien livré ne l'écrit pas (avec le code sain, `summary`
  reste vide). Versé aux dossiers.
  Gardien `tests/test_refus_variable_lot392.py` (14 tests) : dénominateur ·
  anti-double-emploi avec le 377 · **LA propriété vérifiée à l'exécution sur la
  réponse servie**, avec une liste large de clés de motif pour ne pas accuser
  un simple renommage (leçon du 383) · rien n'est inventé. ROUGE ×4.
  **Portée** : les 10 routes testées sont celles **prouvées refuser
  aujourd'hui** ; les 20 autres ne sont couvertes que par le dénominateur. Et
  « 0 muet » vaut pour les entrées invalides choisies — un refus déclenché par
  une panne réseau ou l'absence d'IBKR n'a pas été sollicité.
  Suite 2842 → **2856** / 2 skipped. SW v187.

- **Lot 391 — livré** : **un scan de démo écrit dans l'historique breadth
  réel, et servi.** Piste ouverte par une observation non engagée du lot 390.
  **Les données parlaient avant toute manipulation** : `breadth_history.json`
  portait **16 points strictement identiques** — `a50 50 · a200 45 · net −4 ·
  health 37` — du 21/07 au 08/08. La participation réelle d'un marché ne
  reste pas figée seize séances de suite : **signature exacte de la pollution
  GEX du lot 388**, sur un autre fichier.
  **Lien causal prouvé** : scan DEMO → 16 puis 17 points, date ajoutée
  `2026-08-09`, valeurs identiques aux seize précédentes. Le site d'écriture
  est **inconditionnel** — aucun test de `DEMO_MODE` — et il ne fait pas
  qu'ajouter : `if _bh[-1]['d'] == _today: _bh[-1] = _snap` **écrase** le
  point du jour. Une démo lancée après un scan réel **remplace la mesure du
  jour**.
  **Et c'est servi** : `/scan` rend 17 points dans `internals.history`, que
  `markets_page.py` consomme pour « Tendance de participation » — dont le
  commentaire du code dit « historique breadth **RÉEL** ». Pendant une
  session de démo l'utilisateur est prévenu (`vx-demo-banner`,
  `source = 'demo'`), **mais le point persisté ne porte aucune provenance** :
  lors d'une session réelle ultérieure, sans bannière, les points de démo
  sont servis au milieu des vrais, indistinguables. Le contre-exemple honnête
  existe dans le dépôt : `market_context_last.json` **est** écrit avec un
  champ `demo`.
  **Aucun fichier de production modifié, délibérément.** Mesuré : **aucune**
  persistance du dépôt ne garde `DEMO_MODE`. Ajouter ce garde serait une
  **décision de conception** — ne pas persister en démo, marquer le point, ou
  assumer que la démo peuple l'historique — pas la réparation d'une
  incohérence. Le dossier part au **rang 1**. La purge des 16 points déjà
  accumulés relève de la même décision.
  **Une part de cette pollution vient de la boucle** : ses vérifications de
  tranche lancent le serveur DEMO. Le rituel de copie de sûreté et de
  restauration adopté aux lots 388-390 **a arrêté cette contribution** — le
  point du 09/08 créé par la mesure a été restauré, retour à 16 points. Ce qui
  demeure n'en dépend pas.
  Gardien `tests/test_persistance_demo_lot391.py` (7 tests) : il verrouille
  les **mécanismes de distinction qui existent** — jamais le défaut, car un
  gardien figeant l'absence de marqueur accuserait la correction future
  (leçon du 383). ROUGE ×6, et **le témoin est le test le plus important du
  lot** : ajouter `'demo': DEMO_MODE` au point persisté — *la correction
  probable* — **ne casse pas le gardien**. Une ancre a dû être corrigée
  (`vx-demo-banner` apparaît 4×).
  **Portée** : le gardien est statique ; les autres caches touchés par une
  démo (`daily_prev`, `skyler_memory`) **n'ont pas été analysés** — ce lot
  traite le cas le plus grave, pas la famille.
  Suite 2835 → **2842** / 2 skipped. SW v187.

- **Lot 389 — livré** : **les deux dernières écritures de test, et une
  mesure qui piégeait.** Deux questions laissées ouvertes au 388.
  **(1) Vérifier mon propre énoncé.** J'avais écrit que les 3 fichiers
  restants « ne changent qu'un horodatage » — contrôlé seulement au
  **premier niveau de clés**. Diff **feuille à feuille** (aplatissement
  récursif) après la suite complète : **exactement une feuille modifiée
  par fichier** — `.as_of`, `.ts`, `.age_s`, `.generated_at` — aucune
  perdue, aucune ajoutée. L'énoncé tient ; il repose désormais sur la
  bonne mesure.
  **(2) Le piège.** `skyler_sessions.json` **n'a pas bougé** de
  l'exécution. Conclusion tentante : « personne n'écrit ». **Fausse.** Le
  point du jour existait déjà : l'écriture est **idempotente**, et la
  croissance est d'un point **par JOUR**, pas par exécution. En retirant
  le point du jour avant chaque essai, elle redevient observable — la
  règle du 387 appliquée à l'envers : *« rien ne bouge » ne vaut que si
  l'on s'assure qu'il y avait quelque chose à observer.*
  **Le périmètre était encore quatre fois trop large** : 8 fichiers
  mentionnent SKYX/TSTQ, **2 seulement écrivent** — `test_skyler_core` et
  `test_xss_exits_lot177`, tous deux via `/api/skyler/<sym>` qui
  journalise une séance. Corriger les 8 aurait été six changements
  gratuits.
  **Correction** : redirection de `persist._BASE_DIR` dans les deux tests
  concernés. **Aucune production touchée.** Effet vérifié : **5 → 4
  fichiers runtime touchés**, `skyler_sessions.json` sort de la liste ; les
  4 restants sont exactement ceux dont le diff récursif prouve qu'ils ne
  changent qu'un horodatage.
  **Gardien étendu, pas dupliqué** : `test_caches_runtime_lot388.py`
  passe de 5 à **9 tests** — même propriété qu'au 388, un fichier jumeau
  aurait été du bruit. Ajouts : les 2 entrées au recensement, un anti-vide
  sur la journalisation de séance, et la borne `MAX_SESSIONS = 400`.
  ROUGE ×4 + témoin muet.
  **Deux fois l'outil en cause.** (a) **Mon témoin a mordu** : je
  renommais `SESSIONS_FILE` en croyant faire un changement anodin — c'est
  une `AttributeError` en production, et le recensement l'a signalée comme
  un **13ᵉ site**. Le gardien avait raison, le témoin était faux. (b)
  **Mon anti-vide était creux — la faute du lot 386, refaite** :
  `'SESSIONS_FILE' in src` alors que la chaîne apparaît **6 fois** pour
  **2 sites** d'écriture ; en retirer un laissait le test vert. Réécrit
  par AST. *Avoir la règle écrite ne suffit pas à ne pas la re-violer ;
  c'est la preuve ROUGE qui l'attrape.*
  **Portée** : les 4 fichiers encore touchés le sont **aujourd'hui** sur un
  horodatage — caractérisation datée, rien ne l'impose au code. La
  pollution historique (7 points MSFT, points SKYX/TSTQ déjà accumulés)
  n'est **pas** nettoyée : donnée runtime de l'utilisateur, sa purge est
  une décision.
  **La veine « écritures runtime par la suite » est close** : ouverte au
  386, mesurée au 387, élargie au 388, terminée ici — deux trouvailles
  réelles sur trois lots. Suite 2831 → **2835** / 2 skipped. SW v187.

- **Lot 388 — livré** : **la suite écrivait un point fabriqué par jour dans
  l'historique GEX réel.** Le lot 387 avait traité `desk_data.json` et
  n'avait regardé que celui-là. Ce lot applique la même méthode aux **vingt**
  fichiers runtime du dépôt — pas aux quatre supposés.
  **Mesure : 7 sur 20 touchés par la suite.** Trois horodatages seuls
  (`ai_enrichment`, `session_digest_cache`, `weekly_snapshot`) ·
  `desk_data.json` (connu du 387, `data` byte-identique) ·
  **`desk_backup_20260809.json` CRÉÉ** — ce que le 387 n'avait qu'annoncé
  (« la suite consomme le créneau quotidien ») est désormais **mesuré** ·
  `skyler_sessions.json` (tickers synthétiques) · et
  **`gex_history_cache.json`, sur MSFT — un VRAI titre**.
  **La faute.** `test_options_gex_route_real_numbers` sème un board
  d'options **fabriqué** (MSFT, strikes 460/420, spot 440) puis appelle
  `/api/options/gex/MSFT` ; la route **journalise le profil** via
  `gex_history.record()` dans le vrai fichier, la fixture ne redirigeant
  rien. Mesuré : **8 points MSFT strictement identiques** (net_gex
  36 784 000, spot 440.0, zero_gamma 429.6), un par exécution de la suite —
  alors qu'ACN et ADBE portent des valeurs variées et n'ont pas bougé. La
  comparaison interne au fichier suffit à distinguer le fabriqué du mesuré.
  **Ce fichier est SERVI** : `options_intel_api.py` le lit pour
  `/api/options/gex-radar`. Des chiffres de test étaient donc rendus comme un
  historique mesuré, **sur un titre réellement détenu** — invariant n°4, cette
  fois sur un vrai symbole et non un ticker de test.
  **Correction** : redirection de `persist._BASE_DIR` vers un dossier
  temporaire dans **le seul test concerné** — périmètre établi en rejouant
  les 19 tests du fichier **un par un** depuis un état restauré à l'octet,
  pas par intuition. **Aucune production touchée.**
  **Effet vérifié : 7 → 5 fichiers runtime touchés, MSFT 7 → 7 points.**
  Gardien `tests/test_caches_runtime_lot388.py` (5 tests) : anti-vide sur la
  journalisation (sinon la redirection n'a plus d'objet), bornes
  anti-croissance (`_MAX_SYMBOLS` évince les plus anciens : un symbole
  réinjecté en boucle chasserait un vrai symbole), propriété de redirection,
  anti-péremption, **recensement des 12 sites de production**. ROUGE ×4 +
  témoin muet.
  **Un recensement opaque ne recense rien** : mon premier détecteur rendait
  « ? » pour toute cible non triviale et comptait **8** sites ; rendu
  explicite il en trouve **12**, et surtout il nomme `SESSIONS_FILE` — le
  fichier même qui accumule les tickers de test. Borne fixée sur la vraie
  mesure. Même leçon qu'aux 385 et 387 : *un dénominateur mesuré par un outil
  myope est un faux dénominateur.*
  **Non corrigé, versé aux dossiers** : SKYX/TSTQ dans `skyler_sessions.json`
  (8 fichiers, tickers synthétiques non confondables, bornés à 400 — dégât
  d'une autre nature) et la **purge des 7 points MSFT pollués**, qui est une
  décision de l'utilisateur et non un effet de bord de lot.
  Suite 2826 → **2831** / 2 skipped. SW v187.

- **Lot 387 — livré** : **un test pouvait effacer les notes du trader.**
  Le 16ᵉ dossier ouvert au lot 386 est traité — et son verdict prudent
  (« la suite réécrit `desk_data.json` mais sans perte ») était incomplet.
  **Le dénominateur a été trois fois trop étroit avant d'être juste** :
  `grep desk/push` → 4 fichiers, `grep desk_data` → 15, et c'est **mon
  propre gardien** qui en a trouvé **17** (les deux manquants postent sur
  `/api/desk` sans jamais nommer `desk_data`). Mesure empirique, chaque
  fichier rejoué depuis un état de référence restauré à l'octet :
  **16 sur 17 n'écrivent pas** dans le vrai desk — 12 redirigent
  (`persist.cache_path` **ou** `persist._BASE_DIR`), 1 pousse 3 Mo rejetés
  en 413 avant la route, 3 ne font que lire — et **un seul écrit**.
  **La faute.** `test_desk_roundtrip_is_faithful` lit le desk réel,
  **écrase `myNotes`** par un marqueur, pousse, vérifie, puis restaure.
  `myNotes` n'est pas une clé de test : c'est une **clé synchronisée**,
  `{"NVDA": "note"}`, les **notes par titre du trader**, présente dans les
  trois listes de sync avec ses accesseurs. La restauration n'était **pas**
  protégée. Prouvé par mutation, l'assertion de fidélité inversée :
  `note rendue = False`, contenu laissé `{"guard": "lot84-guard-…"}` —
  **définitivement**, et le filet ne rattraperait rien puisque le lot 362 a
  établi que le snapshot quotidien est pris avant la première écriture,
  créneau que la suite consomme.
  **Pourquoi le lot 386 n'avait rien vu** : l'utilisateur n'a **aujourd'hui
  aucune note** (6 clés, `myNotes` absente). Le chemin de perte existait
  sans matière à perdre. *Un « aucune perte constatée » ne vaut que si l'on
  vérifie qu'il y avait quelque chose à perdre* — le pendant exact de la
  règle du dénominateur.
  **Correction** : un `try/finally` dans `tests/test_desk_cycle_lot84.py`
  — **fichier de test, aucune production touchée**.
  Gardien `tests/test_desk_ecritures_lot387.py` (9 tests) : dénominateur ·
  aucune écriture du vrai desk sans redirection · anti-péremption ·
  **`finally` verrouillé par AST** et remise en état devant repousser `d0` ·
  exemption **vérifiable et bornée au nombre de sites** · `myNotes` doit
  rester une clé servie. Preuve ROUGE ×4 + témoin muet.
  **Trois fois l'outil était en cause.** (a) Ma première mutation ne mordait
  pas : `assert cond, ('msg' and False)` — le `and False` portait sur le
  **message**, pas la condition. (b) Mon premier gardien **accusait deux
  fichiers sains** — `test_desk_routes.py` redirige par `_BASE_DIR`, un
  second mécanisme valide que mon détecteur ignorait, et
  `test_production.py` est rejeté en 413 avant la route ; *un gardien qui
  accuse du code sain finit désactivé*. (c) Mon exemption portait sur le
  **fichier** : la preuve ROUGE a montré qu'un écrivain ajouté après coup y
  passait — resserrée au **nombre de sites**, gelé à la mesure.
  **Portée** : le risque était conditionnel (assertion en échec **et**
  utilisateur ayant des notes) ; aucune perte réelle n'a eu lieu. Ce lot
  supprime le **chemin**, pas un dégât constaté. Le gardien est **statique**
  — il lit le code des tests, il n'observe pas leurs écritures.
  Desk vérifié après la suite : `data` **identique à la référence**, seul
  `ts` diffère. Suite 2817 → **2826** / 2 skipped. SW v187.

- **Lot 386 — livré** : **les 38 `except: pass` de `terminal.py`, lus un
  par un** — le lot 379 l'avait fait pour les 46 de `vertex/`, le 385 avait
  montré que le recensement s'arrêtait à cette frontière. Classement par ce
  que le `try` ENTOURE : nettoyage/fermeture 6 · journal/persistance 10 ·
  import/config optionnel 2 · infra thread 2 · **absence honnête 16** ·
  examinés de près 2. Les trente-six premiers sont sans danger pour
  l'invariant n°4 : un échec y produit une **absence**, jamais une valeur
  inventée.
  **L621 — l'overlay IBKR : honnête au moteur, muet au produit.**
  `_apply_ibkr_indices()` écrase les indices différés yfinance par les
  valeurs temps réel et marque chaque entrée `src = 'ibkr'` — le
  commentaire dit même « provenance temps réel (honnêteté §4) ». Le
  mécanisme est complet et correct. **Mais il n'atteint aucune surface
  servie** : mesuré, `markets_page.py` et `briefing.py` lisent
  `.price/.change/.spark` et **jamais `.src`** ; le seul rendu de « TEMPS
  RÉEL IBKR » vs « yfinance différé » du dépôt est dans `PAGE_ME`,
  **l'une des 7 constantes `PAGE_*` MORTES du lot 374** ; et
  `indices_live` part au client via `/scan` mais **aucun code ne le lit**.
  Ce n'est pas une malhonnêteté — un cours différé reste un cours réel —
  c'est la catégorie du lot 382 : **un énoncé du code plus large que ce
  que le produit délivre**. La pièce réellement fragile est **la fenêtre
  de fraîcheur de 75 s** : l'élargir servirait des valeurs périmées comme
  du temps réel. Verrouillée, avec le marqueur, pour qu'un affichage
  futur ait quelque chose de vrai à lire.
  **L1342 — `bret = 0.0` : mesuré, pas excusé.** J'allais l'innocenter en
  disant que 0 est le neutre. `analysis.py:54` dit le contraire :
  `rs = clip(50 + (sym_ret − bench_ret) × 200, 0, 100)` → 40 devient 70,
  16 devient 40, 50 devient 90. **La force RELATIVE devient une
  performance ABSOLUE** — exactement le piège du lot 378 avec
  `entry_quality`. Trois faits l'empêchent d'être une faute : `0.0` est le
  défaut **déclaré** (atteint aussi sans exception si `bi <= 63`), le
  chemin de scan **vivant** passe un `bench_ret` réel, et aucune page
  servie ne lit `scan_state['edge']`. **Caractérisation, pas correction**
  — jumelle du dossier `context()` du 379.
  Gardien `tests/test_pass_terminal_lot386.py` (11 tests) ; preuve
  ROUGE ×5. **Un test creux démasqué par sa propre preuve ROUGE** : mon
  anti-dérive testait `'< 75' in src`, or la chaîne apparaît **4 fois**
  dans `terminal.py` — élargir la fenêtre à une heure laissait le test
  vert. Réécrit pour lire la constante **dans le corps de la fonction,
  par AST**.
  **Trouvaille adjacente — la suite de tests écrit dans les données du
  desk.** Mesuré : `desk_data.json` est **réécrit** par la suite complète
  (md5 f30f5d7da49a → c6beebcf97f0). **Aucune donnée perdue** — 6 clés
  avant et après, `data` byte-identique, seul `ts` change. Mais le lot 362
  a montré qu'un push **partiel** remplace le blob entier et qu'un push
  `data: {}` est **accepté** : un futur test effacerait des clés en
  silence, et le filet ne rendrait que l'état d'avant la première écriture
  du jour. **16ᵉ dossier**, non engagé — et piste recommandée pour le 387.
  Aucun fichier de production touché. Suite 2806 → **2817** / 2 skipped.
  SW v187.

- **Lot 385 — livré** : **le recensement des replis s'arrêtait à
  `vertex/`**. Parti compter les 38 `except: pass` « autres » du lot 379,
  je suis tombé sur la frontière avant de tomber sur les handlers. Le
  gardien 378 tient l'invariant n°4 — *un `except` qui renvoie un nombre
  substitue une valeur plausible à une donnée manquante* — avec un
  `RACINE = 'vertex'` en dur. **Mesure : 254 handlers dans `vertex/`,
  113 hors, dont 101 dans `terminal.py`** : **31 % des handlers de
  production hors du filet**, dont tout le monolithe qui sert encore des
  routes.
  **Trou prouvé, et distingué d'un gardien inutile.** Un
  `except: return 50` NEUF dans `terminal.py` — exactement ce que la
  propriété 378 interdit — passe les 2 793 tests. Le témoin seul ne
  suffisait pas (deux « AUCUN » côte à côte pourraient vouloir dire que
  le gardien ne sert à rien) : **contrôle décisif**, le même défaut mot
  pour mot dans `vertex/engines/stats.py` **MORD**. Le gardien fait donc
  précisément ce que son code dit — **ce n'est pas une myopie, c'est sa
  frontière**, la catégorie exacte du trou du lot 381.
  **Les trois replis existants de `terminal.py` sont honnêtes, pour deux
  raisons différentes.** `_seed_fund_from_company` → `0` est un compteur
  exact (le nombre EST la mesure). `_i` → `0` et `_f` → `0.0` sont de
  vrais substituts — vérifié sur valeurs réelles,
  `_i(None) = _i('abc') = _i(NaN) = 0` — mais **le site d'appel les
  écarte** : `if iv <= 0 or oi <= 0: continue`. **C'est ce garde-fou, et
  non la coercition, qui tient l'invariant** ; s'il disparaissait, un
  repli entrerait dans la médiane d'IV ATM et le GEX **servis**. C'est la
  seule pièce fragile des trois, désormais verrouillée — ainsi que le
  fait que les coercitions n'aient pas essaimé, puisque toute la
  démonstration repose là-dessus.
  Gardien `tests/test_replis_racine_lot385.py` (13 tests) : dénominateur
  d'abord, LA propriété portée hors `vertex/`, anti-péremption, borne de
  dérive **fixée À la mesure** (38), **anti-rot du périmètre** forçant la
  décision sur tout nouveau module racine, exclusions vérifiées non
  importées par la production. Preuve ROUGE ×3, toutes sur le **vrai
  fichier de production** — la faute du lot 383 ne s'est pas reproduite.
  **Un risque de test évité** : ma première version appelait
  `_seed_fund_from_company()`, sans écriture ici *parce que le cache est
  plein sur cette machine* ; sur un cache incomplet elle aurait sauvegardé
  un fichier runtime depuis un test. `_save_json` est interceptée et le
  test échoue si une écriture est tentée.
  Aucun fichier de production touché, aucun fichier runtime muté
  (`fund_cache.json` inchangé, vérifié par `mtime`). Suite 2793 →
  **2806** / 2 skipped. SW v187. Suite : les 38 `except: pass` de
  `terminal.py` lus un par un, seule piste fine portant encore une
  question d'honnêteté non tranchée.

- **Lot 384 — livré** : audit des gardiens par mutation, **quatrième et
  dernière passe — 6 sur 6, aucun trou**, et la veine se ferme sur ce
  résultat. **Mordent** : snapshot quotidien du desk désactivé ·
  garde-fou de taille du snapshot neutralisé · redirection héritée
  `/heatmap` supprimée · entrée Options retirée de `PRIMARY_NAV` ·
  `/healthz` vidé de son contenu réel · collecte de `/api/client-log`
  neutralisée. Le **témoin négatif** (commentaire reformulé) reste muet,
  ce qui donne son sens au 6/6.
  **Bilan honnête de la veine, quatre lots, ~27 mutations utiles** :
  381 → 1 trou + 1 constat · 382 → 1 écart · 383 → 0 · 384 → 0. **Les
  deux trouvailles sont concentrées dans les deux premiers lots**, avec
  un protocole pourtant plus rigoureux à chaque passe : c'est le signal
  convenu au 383, **la veine est épuisée, je la ferme plutôt que de m'y
  acharner**.
  **L'actif réel** : dix-sept invariants sont désormais **prouvés tenus
  par mutation**, non plus supposés — READONLY, service worker (recul de
  version ET fichier `static` sans bump), les trois listes de clés de
  sync, `sanitize_news` sur deux sorties, filet desk (rotation, snapshot,
  garde-fou), navigation (redirection héritée, registre), observabilité
  (`/healthz`, `/api/client-log`), vocabulaire des verdicts, apostrophes
  françaises servies, nom personnel, `scan_state`, plancher de version du
  cœur. Avant cette tranche, aucun de ces énoncés n'avait été vérifié
  autrement que par la présence d'un test au vert — **et un test au vert
  qui ne mesure rien est plus dangereux qu'un test absent**.
  **Rien touché, délibérément** : aucun fichier de production, **aucun
  test ajouté** — il n'y a rien à corriger, et ajouter un gardien là où
  6 mutations sur 6 sont déjà attrapées serait le changement gratuit que
  la boucle s'interdit. Un seul item mineur **volontairement différé** :
  le commentaire « MIROIR EXACT de `__DESK_KEYS` (terminal.py) » en tête
  de `vx-entities.js`, faux depuis la purge É1 — le corriger changerait
  un octet **servi**, donc imposerait bump SW, invalidation de cache,
  `_EMPREINTE` et preuve MD5 complète. Disproportionné pour un
  commentaire.
  **Portée** : 27 mutations sur 2 793 tests restent un **sondage**.
  « MORD » = « attrape CETTE faute-là ». Ce que je conclus, c'est que
  *cibler les invariants critiques ne rend plus rien*, pas que la suite
  entière est saine. Suite **2793 / 2 skipped inchangée**. SW v187.
  **Le vrai goulot reste les quinze dossiers en attente de décision
  humaine** — 604 Ko de HTML mort assemblés à chaque import, le filet
  desk qui perd le travail de la journée, les deux questions d'honnêteté
  jumelles (363 et 379), `vx_kit.JS` servi nulle part.

- **Lot 383 — livré** : audit des gardiens par mutation, **troisième
  passe** — et cette fois **aucun trou**. C'est un résultat, pas une
  absence de résultat. **Mordent** : apostrophes déséchappées dans un
  bloc JS **servi** · nom personnel injecté dans une page servie ·
  `scan_state` réassigné dans un **consommateur** · **recul** de version
  du cœur (0.9.0 → 0.8.0). Le **témoin négatif** ne mord pas, comme
  attendu.
  **Deux « AUCUN GARDIEN » qui accusaient à tort.** (a) Ma première
  mutation `scan_state` visait `vertex/app/state.py` — or c'est le
  `HOME` déclaré du gardien, **exclu du scan par conception** puisque
  c'est le domicile légitime de l'affectation ; rejouée dans un
  consommateur, la violation tombe immédiatement. (b) Passer
  `demo_mode=DEMO_MODE` à `False` ne change **aucun octet servi** —
  `/system` rend le même MD5 (73e917c0f2d0, 82 837 o) — alors que
  `DEMO_MODE` vaut bien `True` au runtime : la mutation était effective
  dans la source mais n'atteint pas la page. Mutation invalide, pas un
  trou. Deux fois sur trois le « AUCUN » initial était faux : *un cas
  qui ne mord pas accuse d'abord la mutation*.
  **Seul écart relevé : un PLANCHER, pas une égalité.** « skyler_core
  0.9.0 intact » suggère l'égalité ; le gardien impose `>= (0, 9, 0)` —
  un recul échoue, un bond en avant passe. C'est la catégorie « gardien
  plus étroit que l'énoncé » du lot 383, **mais ici la règle réelle est
  la bonne** : monter est légitime, régresser ne l'est pas. Rien à
  corriger dans le code ; l'énoncé gagne à être dit précisément, et le
  gardien le fixe.
  **Un faux gardien écarté avant livraison.** Ma première version
  testait la parité des quotes simples dans le JS servi : elle échouait
  sur **5 pages sur 8** alors que le code est sain (les quotes vivent
  aussi dans des chaînes doubles, des regex, des commentaires). Un
  gardien qui accuse du code sain finit désactivé — remplacé par la
  vérification que le vrai parseur `node --check` couvre encore les
  8 pages servies. Le bon outil existait déjà.
  Gardien `tests/test_invariants_reellement_imposes_lot383.py`
  (14 tests) ; preuve ROUGE ×3, dont un cas d'abord **non mordant parce
  que j'avais muté mon propre fichier de test** au lieu du gardien
  historique. Aucun fichier de production touché. Suite 2779 → **2793** /
  2 skipped. SW v187. **Bilan de la veine : deux écarts sur trois lots,
  et zéro ici — si un lot de plus ne trouve rien, changer de veine.**

- **Lot 382 — livré** : audit des gardiens par mutation, **seconde
  passe**, protocole durci après les trois mutations fautives du 381
  (ancre unique, mutation vérifiée effective, code muté vérifié SERVI).
  J'ai ajouté un **témoin négatif** — une modification anodine qui ne
  doit PAS faire tomber la suite — pour que les « MORD » veuillent dire
  quelque chose : il se comporte comme attendu.
  **Quatre protections lourdes tiennent** : `sanitize_news` retiré de
  `/news-feed` **et** de la construction des événements, rotation des
  sauvegardes desk ramenée à 0, et un fichier `vertex/static` modifié
  **sans bump d'empreinte** — tous mordent.
  **Un trou** : un `#ff00ff` en dur dans le shell **servi** passe les
  2 767 tests. Tentation immédiate d'accuser le gardien couleur de
  myopie — **vérifié avant d'accuser**, par mutation ciblée : `#1e6fd9`
  (bleu non-marque) MORD, `#ff00ff` et `#c0392b` passent. Le gardien
  balaie bien `vertex/ui/**`, shell compris, et fait **exactement ce que
  son nom annonce**. Ce n'est pas lui qui ment : c'est `CLAUDE.md` qui
  annonçait « tokens/VXChartTheme uniquement, **aucun littéral
  couleur** ».
  **Mesure : 265 littéraux `#RRGGBB` distincts dans `vertex/ui/**`, dont
  53 atteignent une page SERVIE** (répartis sur une dizaine de modules).
  L'énoncé était donc faux depuis longtemps, et exiger zéro casserait la
  suite sans rien améliorer. **Verdict : le code respecte la règle
  réelle — c'est l'énoncé qui était faux, et le contrat qui n'était
  verrouillé nulle part.**
  Livré : gardien `tests/test_litteraux_couleur_servis_lot382.py`
  (12 tests — anti-vide avec dénominateur, **borne de dérive fixée À la
  mesure** (55 pour 53), règle réelle vérifiée sur les **octets servis**
  là où le gardien historique lit les sources, anti-péremption du
  périmètre) ; plus une section « Couleurs — la règle réellement tenue »
  dans `CLAUDE.md`, chiffres à l'appui. Preuve ROUGE ×4 — les quatre
  fautes passaient toutes la suite avant ce lot. Aucun fichier de
  production touché. Suite 2767 → **2779** / 2 skipped. SW v187.
  **Deux lots, deux écarts doc/réalité au même endroit** : les
  invariants annoncés dans `CLAUDE.md`. La piste suivante s'impose —
  vérifier systématiquement chaque règle critique contre ce qu'un
  gardien impose vraiment.

- **Lot 381 — livré** : ouverture de la veine décidée au bilan 380 —
  **auditer les GARDIENS eux-mêmes, par mutation**. 291 fichiers de test,
  2 756 tests dont nul n'avait vérifié qu'ils voient ce qu'ils prétendent.
  Protocole : muter le code protégé puis lancer **toute la suite** — la
  question n'est pas « ce gardien-ci mord-il ? » mais « **un** gardien
  mord-il ? ». Sept sondages sur les gardiens que `CLAUDE.md` nomme comme
  protégeant les règles critiques.
  **Bonne nouvelle d'abord** : **READONLY**, le **service worker**, le
  **vocabulaire des verdicts** et **DESK_KEYS de vx_kit** mordent tous.
  Les invariants lourds sont réellement tenus, et ce n'était pas acquis.
  **Mais un trou, sur la règle critique n°1** — celle dont `CLAUDE.md`
  dit « sinon un push l'efface côté serveur » : retirer `vxAlerts` du
  **repli servi** de `/system` passe **les 2 754 tests**.
  **Et en cherchant pourquoi, le constat le plus grave.** Mesure page par
  page : **`vx_kit.JS` (21 727 octets) n'est servi sur AUCUNE des
  8 pages**, alors que la doc le décrivait comme « kit global présent sur
  toutes les pages » et **source de vérité** des clés. Tableau réel : sur
  les **deux listes réellement servies** — `vx-entities.js` (statique,
  32 464 o, chargé par les 8 pages) et le repli inline de `/system` —
  **une seule était gardée** ; les deux autres listes gardées (`vx_kit`,
  `journal`) n'atteignent pas le navigateur. La chaîne tient encore par
  comparaison, mais elle est **ancrée sur un module candidat à la
  purge** : le jour où il part, la référence s'en va et la liste servie
  non gardée reste.
  **Trois fausses pistes en chemin, toutes de mon fait** : `.replace(…,1)`
  a frappé la mauvaise occurrence deux fois, et une mutation visait un
  bloc **servi nulle part**. Dans un lot dont le sujet est « les gardiens
  mentent-ils ? », c'est l'outil qui a menti trois fois — *un cas qui ne
  mord pas accuse d'abord la mutation*. La passe corrigée exige une ancre
  **unique** et vérifie que la ligne visée a changé.
  **Livré** : gardien `tests/test_desk_keys_servies_lot381.py` (13 tests)
  qui garde les listes **par ce qu'elles SERVENT** (contrat complet et
  aucune clé inventée dans le repli, `vx-entities.js` vérifié tel que
  servi, les 8 pages le chargent, les deux listes servies identiques, et
  le fait `vx_kit` non servi **ancré**) ; plus la **correction de la
  règle n°1 de `CLAUDE.md`**, qui annonçait trois listes servies dont
  deux ne le sont pas. Preuve ROUGE ×4 — les quatre fautes passaient
  toutes la suite avant ce lot ; un cas d'abord **sauté** (espaces après
  virgules), signalé puis corrigé. Aucun fichier de production touché
  (`CLAUDE.md` est de la documentation, non servie) : pas de preuve MD5
  requise, pas de bump. Suite 2754 → **2767** / 2 skipped. SW v187.

- **Lot 379 — livré** : les 46 `except: pass` **jugés** — le lot 378 les
  avait comptés en déclarant explicitement ne pas les juger — **plus les
  matériaux du bilan 380**. Classement par ce que le `try` ENTOURE :
  3 nettoyage, 5 journal/persistance, 38 lus un par un (imports
  optionnels, lecture du `.env`, écritures de cache, calculs métier).
  Mon classificateur automatique en laissait 38 sur 46 « à lire » : il
  n'a pas fait le travail, et je le dis plutôt que de maquiller le
  résultat. Les cinq blocs de `market/context.py` n'écrivent que dans
  `out[...]` et des locales → un échec produit une **absence**, jamais
  une valeur périmée servie.
  **Hypothèse sérieuse formée, puis RÉFUTÉE par la mesure.**
  `analysis.py:229` recalcule `grade` après que `score` a été ajusté,
  sous `except: pass` : en cas d'échec, un grade calculé sur l'ANCIEN
  score serait servi à côté du NOUVEAU — deux champs incohérents, qu'aucun
  gardien existant n'attraperait. Vérification : `config.grade` ne lève
  pour **aucun** nombre (0, 1, 50, 99, 100, −5, 105, 50.5, NaN, ∞) et la
  ligne 228 garantit un `int` : **le handler est inatteignable**,
  l'incohérence ne peut pas se produire.
  **Et la sonde a trouvé à côté ce qui vaut plus que la piste.** En
  vérifiant que `context()` dégrade bien par absence, j'ai mesuré son
  comportement sur univers vide : il est **mixte**. `vix`, `vix_band`,
  `vix_chg`, `spy_regime`, `spy_adx`, `spy_trend_txt` valent `None` —
  honnête. Mais `roro` affirme **'NEUTRE'**, `roro_gap` vaut **0**,
  `breadth` sort tout à zéro et `verdict` annonce « MARCHÉ · NEUTRE ·
  participation 0% au-dessus MM50 ». Ce n'est PAS un `except` qui
  avale : le bloc **réussit**, parce que ses propres défauts
  (`ro = np.mean(…) if any(…) else 50`) le font aboutir sur zéro donnée.
  Sur un univers vide, l'application **affirme** donc un régime au lieu
  de dire qu'elle ne sait pas. **Caractérisation GELÉE, pas corrigée** —
  toucher au moteur de contexte sans accord serait le changement gratuit
  que la boucle s'interdit, et la question est **jumelle du dossier
  ouvert au lot 363**. Versée aux dossiers en attente.
  **Verdict : sain, rien touché.** Gardien
  `tests/test_pass_et_contexte_lot379.py` (24 tests : périmètre,
  anti-vide et borne de dérive, écriture dans `out[...]` seulement,
  `config.grade` total sur 10 valeurs, anti-dérive de la garantie `int`,
  6 champs honnêtes en `None`, 4 champs affirmatifs gelés) ; preuve
  ROUGE ×4 — le premier cas d'abord **non mordant**, mais c'était **ma
  mutation** qui était inopérante (définition écrasée par la vraie), pas
  le gardien : *un cas qui ne mord pas accuse d'abord la preuve*.
  Aucun fichier de production touché. Suite 2730 → **2754** / 2 skipped.
  SW v187 inchangé. **Matériaux du bilan 380 consignés** : tableau des
  dix lots, +144 tests sur la tranche, 9 gardiens, 1 seule faille réelle
  (372) et 1 seul lot touchant la production (MD5 0/8), SW v187 sur les
  dix lots, et le fil rouge des **douze fois où l'outil était en cause**.

- **Lot 378 — livré** : les **exceptions comme convention de refus**,
  angle mort déclaré au lot 377. Risque produit : un `except` qui avale
  une erreur transforme une donnée manquante en **blanc muet**, ou pire
  en **chiffre plausible**. Mesure : **254 handlers** — 124 replis nus
  (48,8 %), 66 autres, **46 `except: pass`**, 17 marqués, 1 avec trace.
  Le chiffre de 124 fait peur mais mon classement confondait deux choses
  opposées : ce que le handler **renvoie** tranche — **`None` 70**
  (contrat « valeur ou None » : parfaitement HONNÊTE, l'appelant affiche
  `—`), et seulement **12 NOMBRES**, seule famille qui menace
  l'invariant n°4.
  **Première correction, et elle est d'un genre nouveau.** Deux des
  douze renvoient **50** (`quant_engine.entry_quality`). J'allais les
  innocenter : 50 est le point de départ de la fonction (`s = 50.0`) et
  le défaut de ses entrées, donc « le neutre déclaré de l'échelle ».
  **Exécution faite, c'est FAUX** : à entrée vide la fonction rend
  **76**, pas 50. `s = 50.0` est un point de départ interne, pas une
  sortie naturelle — le repli est bien un score plausible,
  **indiscernable d'une mesure**. C'est la **première fois de la boucle
  que la vérification sur valeurs réelles m'empêche d'INNOCENTER du
  code** ; d'habitude elle m'empêche d'en accuser.
  **Verdict : CARACTÉRISATION, pas de faute prouvée.** Le chemin est
  défensif (il exige un `d` non-dict, alors que les appelants passent
  des lignes de scan) et je n'ai trouvé aucune entrée réelle qui
  l'atteigne — modifier un moteur de scoring sur un défaut non démontré
  serait le changement gratuit que la boucle s'interdit. Ce que le lot
  livre, c'est le **recensement gelé** : aucun nouveau repli numérique
  ne pourra apparaître en silence.
  **Seconde correction, sur mon propre gardien.** La preuve ROUGE a
  d'abord répondu **NE MORD PAS** au cas « `raise` privé de son
  message » : ma tolérance de 3 muets reposait sur un chiffre annoncé de
  2, quand la mesure au critère du gardien donne **39 `raise`, 1 seul
  muet**. Borne ramenée à la mesure. **Une borne qui absorbe la première
  régression n'est pas une borne** — c'est la même illusion de confort
  que la myopie découverte au lot 377.
  Observation versée aux dossiers : `opportunities_api._followed_count`
  et `_positions_count` renvoient `0` sur exception, rendant « desk
  illisible » et « desk vide » indiscernables (portée limitée : la route
  consommatrice marque bien ses propres erreurs, 500 + `error`).
  Gardien `tests/test_replis_exception_lot378.py` (9 tests : périmètre,
  anti-vide, recensement gelé et justifié, anti-péremption, bornes de
  dérive qui rendent visible sans juger, caractérisation vérifiée **en
  exécution**, `raise` muets ≤ 1) ; preuve ROUGE ×5, restauration
  identique à l'octet — deux cas d'abord **sautés** puis corrigés sur
  les vraies lignes, un troisième d'abord **non mordant**, ce qui a
  révélé la borne trop lâche. Aucun fichier de production touché, donc
  pas de preuve MD5 requise. Suite 2721 → **2730** / 2 skipped. SW v187
  inchangé.

- **Lot 377 — livré** : les autres conventions de refus — **et la
  découverte que le gardien du lot 376 n'en voyait qu'un TIERS.**
  Volume mesuré sur 1321 fonctions : `return None` **242** (absence de
  valeur ordinaire, PAS un refus — non décidable, et je ne prétends pas
  le trancher), `return []` 28, `return {}` 13,
  `{available: False}` 13, `{ok: False}` 4.
  **Le vrai défaut n'était pas dans le code mais dans le PÉRIMÈTRE du
  gardien précédent.** Il ne regardait que `return <Dict>` ; or la
  majorité des refus d'API sont **enveloppés** —
  `return jsonify({...})`, souvent `jsonify({...}), 400` — donc portés
  par un `Call` ou un `Tuple`, jamais un `Dict`. Ils étaient **tous**
  invisibles : **13 vus sur 39 réels, soit 33 % de couverture**. Et les
  26 manquants sont précisément **les plus exposés** : les refus servis
  en JSON au navigateur, ceux que l'interface montre à l'utilisateur.
  **12ᵉ fois de la boucle que le périmètre de l'outil ment, et la
  première où c'est un gardien DÉJÀ FUSIONNÉ qui se révèle myope** — le
  code était sain, le test au vert, et le vert ne voulait pas dire ce
  qu'on croyait. Un gardien myope est plus dangereux qu'une absence de
  gardien, puisqu'il rassure. Périmètre corrigé : **39 refus,
  39 motivés, 0 muet**, confirmé sur les réponses réellement servies
  (`error='question vide'`, `err='nom invalide'`). Cas voisin vérifié
  avant de crier au loup : `/api/skyler/<sym>` répond 200 sans clé
  d'état pour un symbole inconnu, mais sert une décision complète avec
  un `audit_trail` énumérant ce qui manquait — **la traçabilité EST le
  motif**, pas un refus muet. Discipline des contrats à deux visages
  mesurée avec son dénominateur : **37 fonctions mixtes existent, 0 ne
  porte de clé d'état** dans sa branche riche. **Verdict : sain, rien
  touché** — ce que ce lot corrige, c'est la **couverture**. Gardien
  `tests/test_refus_api_lot377.py` (9 tests, dont celui qui verrouille
  la leçon : **le déballage doit voir strictement plus que le détecteur
  naïf, écart ≥ 10** — si l'écart tombe, c'est le gardien qui est
  redevenu myope, pas le code qui a changé) ; preuve ROUGE ×5,
  restauration identique à l'octet, dont **la myopie elle-même rejouée**
  en retirant le déballage. Aucun fichier de production touché, donc pas
  de preuve MD5 requise. Suite 2712 → **2721** / 2 skipped. SW v187
  inchangé.

- **Lot 376 — livré** : les docstrings qui décrivent leur retour **en
  prose** — angle mort déclaré au lot 375. Consigne appliquée :
  **mesurer le volume AVANT de promettre un verdict**, précisément parce
  que le lot 375 s'était fait piéger par un « 0 » sans dénominateur.
  Mesure : 1321 fonctions, 674 avec docstring, 51 parlant de retour,
  6 structurées (lot 375), **45 en prose**, dont **2 seulement**
  mécaniquement vérifiables — et **les deux sont de faux positifs** :
  `premium`, `model`, `iv` sont des **paramètres d'entrée**, `cost` un
  champ du board ; mon heuristique prenait tout mot entre backticks pour
  une clé de retour. **11ᵉ fois de la boucle que l'outil est le premier
  suspect, et 4ᵉ d'affilée où mon détecteur accuse du code sain.** Une
  docstring en prose ne marque pas ce qu'elle décrit : **piste close par
  la mesure**, pas par un vert de complaisance.
  **Mais la lecture a exhibé un contrat autrement plus utile, et lui
  parfaitement décidable** : `analyze_strategy` promet « entrée
  insuffisante ou invalide => `{'available': False, 'reason',
  'refusals': [{field, value, why}]}` ». C'est **l'invariant produit n°4
  de Vertex sous sa forme code** — donnée absente → motif honnête,
  jamais un blanc. Un `available: False` sans motif est un refus
  **muet** : l'interface affiche un vide que l'utilisateur risque de
  lire « rien à signaler » au lieu de « je ne sais pas ». Mesuré :
  **13 refus dans le paquet, 13 motivés, 0 muet**, et confirmé sur
  **valeurs réelles** (leçon du lot 374) — motifs français explicites,
  dont « prime manquante sur une jambe — pas de P&L inventé ».
  **Verdict : sain, rien touché** ; ce que le lot ajoute, c'est
  l'invariant : aucun refus futur ne pourra être muet. Gardien
  `tests/test_refus_honnete_lot376.py` (9 tests : périmètre, anti-vide
  avec dénominateur explicite, la propriété avec un message d'échec qui
  dit POURQUOI c'est grave, 4 refus provoqués en réel avec exigence d'un
  motif d'au moins 12 caractères et non numérique, anti-dérive de la
  docstring qui fait de ce comportement une promesse, pas-trop-strict
  avec anti-péremption) ; preuve ROUGE ×4, restauration identique à
  l'octet — le cas décisif étant le **motif vidé en chaîne vide**, qui
  passe un contrôle de présence de clé et n'est attrapé que par le test
  sur valeurs réelles. Aucun fichier de production touché, donc pas de
  preuve MD5 requise. Suite 2703 → **2712** / 2 skipped. SW v187
  inchangé.

- **Lot 375 — livré** : les promesses des docstrings de **FONCTIONS** —
  le gardien du lot 366 ne couvrait que celles des **modules**. Même
  veine que les lots 365 (PORTFOLIO_FIT annoncé, jamais évalué) et 368
  (promesse d'échappement fausse). **Deux volets, deux résultats
  différents — et le second est le plus instructif.**
  **Volet 1, les promesses de forme de retour : SAINES, prouvé.** Six
  fonctions portent un contrat `Retourne {…}` ; sur **toutes** leurs
  branches `return {littéral}` — 14 au total — **aucune clé annoncée ne
  manque**. La collecte statique de CHAQUE branche s'est révélée plus
  forte qu'un test d'exécution : `assess` a une **sortie anticipée**
  (bid/ask absent) qui renvoie 3 clés là où le chemin normal en renvoie
  4 — un appel unique n'aurait jamais visité cette branche, et c'est
  précisément elle que la preuve ROUGE fait échouer. Trois
  sous-déclarations relevées (`spread_pct`, `entry`, et `delta` dans la
  forme imbriquée de `pack()`) et **volontairement non corrigées** : ce
  sont des enrichissements, pas des promesses fausses. Le gardien
  n'exige donc PAS l'égalité exacte — l'imposer le rendrait intenable
  dès qu'une branche d'erreur renvoie le socle minimal, et un gardien
  qui crie au loup finit désactivé (leçon du lot 374).
  **Volet 2, les promesses en un seul mot majuscule : NON DÉCIDABLES.**
  359 mots majuscules distincts cités en docstring de fonction, **0
  introuvable** dans le paquet — mais ce zéro est **vide de sens** :
  l'échantillon (`ACHETER`, `ATTENDRE`, `ATTAQUE`, `ARBITRAIRE`) montre
  que sans underscore, un mot majuscule dans une docstring française est
  presque toujours une **emphase**, pas un identifiant, et le filet les
  déclare tous « trouvés ». Le lot 366 avait heurté le même mur dans
  l'autre sens (139 faux positifs). Annoncer « 0 problème » ici serait
  un faux vert : **piste close par la mesure**, pas par un vert.
  **10ᵉ correction de méthode, et 3ᵉ d'affilée où c'est MON détecteur
  qui accuse du code sain** : `ast.walk` descendait dans la fonction
  imbriquée `pack()` et attribuait ses 13 clés à
  `options_for_position`, qui en annonce 4 — une violation de trois clés
  entièrement imaginaire. Règle retenue : quand un audit signale une
  faute grossière dans du code mûr, **l'outil est le premier suspect**.
  Gardien `tests/test_promesses_retour_lot375.py` (10 tests : périmètre,
  2 anti-vide, la propriété, pas-trop-strict avec anti-péremption,
  **anti-ré-attribution verrouillant ma propre faute**, 4 contrats
  épinglés nommément contre la dérive silencieuse d'une docstring) ;
  preuve ROUGE ×4, restauration identique à l'octet — le premier cas
  d'abord **sauté** faute de motif, signalé par le script puis corrigé
  sur la vraie ligne. Aucun fichier de production touché, donc pas de
  preuve MD5 requise. Suite 2693 → **2703** / 2 skipped. SW v187
  inchangé.

- **Lot 374 — livré** : les blocs `<script>` **assemblés par
  concaténation** — l'angle mort que le lot 373 avait lui-même déclaré.
  **Il existe bel et bien** : 15 chaînes littérales déséquilibrées, soit
  4 points de concaténation. Trois n'assemblent que des constantes de
  module (`_OPP_BRIEF_JS`, `_sync_ui.JS`, `_VX_JS_FULL`, `ART_JS`) ; le
  quatrième — `terminal.py::_vpage`, qui fait
  `'…</div><script>' + js + '</script>…'` — est le seul à recevoir un
  **paramètre**. **Verdict : sain, rien touché — mais pour une raison de
  ROUTAGE, pas de code.** Ses 7 appelants passent tous une constante
  évaluée à l'import, et surtout **les 7 pages ainsi construites ne sont
  plus servies** : `/bordel`, `/review`, `/research`, `/heatmap`,
  `/equipe`, `/settings`, `/health` renvoient un **301** vers les pages
  du redesign (table `_LEGACY` de `redesign.py`). Contrôle croisé sur
  les octets servis : balises équilibrées sur les 8 pages (10 à
  18 paires). Comme la sûreté dépend d'un fait de routage et non d'une
  propriété du code, le gardien **ancre explicitement ce fait**.
  **Deux corrections de méthode, et les deux portaient sur MON PROPRE
  GARDIEN** (8ᵉ et 9ᵉ de la boucle). Ma première version exigeait que
  `js` soit un littéral : elle accusait `_BORDEL_JS`, qui concatène en
  fait trois constantes de module — détecteur trop étroit, corrigé en
  résolution transitive. Toujours rouge : deux de ces constantes sont
  produites par `_extract(PAGE_DAILY, …)`, donc constantes **à
  l'import** mais pas littérales au sens statique. J'ai alors compris
  que l'invariant syntaxique était le **mauvais outil** — la propriété
  qui protège n'est pas « `js` est un littéral » mais « **la valeur de
  `js` ne contient pas de balise fermante** », vérifiée sur les valeurs
  réelles. Les deux fois, mon gardien accusait du code sain : l'erreur
  **symétrique** de celle qu'on redoute d'habitude, et tout aussi
  coûteuse — un gardien qui crie au loup finit désactivé. **Constat de
  poids mort, mesuré et NON engagé** : ces 7 constantes représentent
  **618 527 octets (604 Ko) de HTML assemblés à chaque import** de
  `terminal.py` pour n'être jamais renvoyés (import : 1,91 s) —
  candidat naturel pour les purges É2/É3, **dossier en attente de GO**.
  Gardien `tests/test_script_concatene_lot374.py` (21 tests : 3
  anti-vide, la vraie propriété sur les valeurs réelles, complément
  statique interdisant un `js` calculé par requête, équilibre des
  balises sur les 8 pages servies avec exigence de ≥ 8 blocs, le fait de
  routage dont dépend le verdict, anti-péremption si la purge a lieu) ;
  preuve ROUGE ×4, restauration identique à l'octet — avec la précision
  honnête que le cas 2 remonte en **erreur de collecte**, pas en échec
  d'assertion. Aucun fichier de production touché, donc pas de preuve
  MD5 requise. Suite 2672 → **2693** / 2 skipped. SW v187 inchangé.

- **Lot 373 — livré** : la faute du lot 372 sous ses **autres habillages**
  — f-strings, `%`-format, et tous les producteurs de HTML, pas seulement
  les gabarits `%%…%%` de trois pages. **Verdict : aucune faille
  exploitable, rien touché — mais un danger latent trouvé et verrouillé.**
  **7ᵉ correction de méthode de la boucle, et la plus instructive** : ma
  première passe listait les fichiers avec `os.listdir`, qui **ne descend
  pas dans les sous-dossiers**. `vertex/ui/shell/__init__.py` — le
  producteur HTML **central**, celui qui assemble les 8 pages — n'a
  jamais été lu, et c'est exactement là que se trouvait la trouvaille.
  Première fois que c'est mon **périmètre de balayage**, et non ma
  logique, qui mentait. Passe corrigée en `os.walk` :
  `vertex.engines.recommendation.vocab_js()` est un `json.dumps` **nu**
  injecté dans `<script id="vx-vocab">window.__VXVOCAB={…}</script>`,
  donc **sur les 8 pages** — l'endroit le plus exposé de l'application.
  Il ne tient aujourd'hui que parce que `_labels_map()` n'assemble que
  des tables littérales du module (`DECISIONS`, `HELD`, `_ALIAS`) : les
  3 689 octets servis ne contiennent **ni `<`, ni `>`, ni `&`**, et
  **rien ne le vérifiait**. Une seule étiquette future avec un `<`
  ferait sortir le script sur les huit pages à la fois. **Durcissement
  mesuré puis écarté avec raison** : `vocab_js` sérialise en
  `ensure_ascii=False` alors que `json_for_script` laisse la valeur par
  défaut — l'appliquer transformerait tous les accents en `\uXXXX`,
  changerait les octets servis sur les 8 pages et imposerait un bump SW,
  pour **zéro gain** puisque le contenu n'a aucun caractère de balise.
  C'est l'**invariant** qui protège ici, pas le durcissement. Les deux
  `%%VIEW%%` restés bruts (`markets_page`, `performance_page`) vivent
  dans `const VIEW='%%VIEW%%'` — une chaîne JS entre apostrophes, dont
  une charge s'échapperait — mais tiennent par la **liste blanche
  appliquée avant la substitution** ; sondés 4 charges × 2 routes sur
  des rendus réels de 55-70 Ko : 0 fuite, `VIEW='overview'` partout.
  Gardien `tests/test_contexte_js_lot373.py` (27 tests : anti-vide,
  **anti-angle-mort verrouillant la faute de mon propre outil**,
  exceptions justifiées **et** anti-péremption, invariant vocab sur les
  8 pages, gardien pas-trop-strict) ; preuve ROUGE ×3 (étiquette avec
  `<`, liste blanche retirée, `json_for_script` remplacé par un
  `json.dumps` nu), restauration identique à l'octet — le 1ᵉʳ cas a
  d'abord été **sauté** faute de motif correspondant, signalé plutôt que
  tu. Aucun fichier de production touché, donc pas de preuve MD5
  requise. Suite 2645 → **2672** / 2 skipped. SW v187 inchangé.

- **Lot 372 — livré** : les **interpolations serveur** dans le `page_js`
  des pages, dernière grande surface non auditée de la veine sécurité.
  **VRAIE FAILLE XSS TROUVÉE ET CORRIGÉE — la plus grave de la boucle.**
  Audit AST : 35 interpolations dans les `render*`, dont 4 envoient du
  JSON dans un bloc `<script>`. `/opportunities` reçoit
  `params=request.args` et n'en filtre que les **CLÉS** (`sym`, `sector`,
  `setup`, `decision`) ; les **VALEURS** partaient nues dans
  `json.dumps`, qui échappe `"` et `\` mais **ni `<` ni `/`**. Donc
  `?sym=</script><img src=x onerror=…>` **ferme le script et injecte du
  HTML actif** : 8 injections confirmées sur un rendu réel (4 clés ×
  2 charges, HTTP 200, pages de 66 Ko). Contrairement à la faille du
  lot 368 — qui exigeait que le moteur produise un symbole hostile —
  celle-ci est **déclenchable à distance par un simple lien**, dans une
  session qui a accès au desk local. Les 6 autres pages recevant des
  paramètres d'URL : aucune fuite. Corrigé par
  `vertex.ui.shell.json_for_script` (`<`, `>`, `&` → `\uXXXX`, relus à
  l'identique par un moteur JS, donc comportement client inchangé),
  appliqué aux **4** sites pour rendre le contrat vérifiable
  statiquement ; sonde rejouée **16/16 saines**. **6ᵉ correction de
  méthode** de la boucle : mon premier détecteur comptait comme
  « actif » un `<img>` resté **à l'intérieur** d'un `<script>` non
  refermé — où il est inerte — et gonflait le résultat. Gardien
  `tests/test_json_script_lot372.py` (35 tests : anti-vide, charges ×
  clés, préservation du comportement, gardien pas-trop-strict, contrat
  statique dont un test qui vérifie que le détecteur mord) ; preuve
  ROUGE ×2 (faute historique rejouée, correctif affaibli), restauration
  identique à l'octet. **MD5 0/8 divergence** malgré 3 fichiers de
  production touchés ; navigateur réel 0 erreur console sur filtre
  légitime, filtre secteur et charge hostile. Tranché au passage : les
  plages « smoke » de ces scripts mesurent le **DOM hydraté** (4662 pour
  `/opportunities`) alors que le script mesure le **HTML brut** (410) —
  deux grandeurs sans rapport ; ce smoke n'a jamais rien prouvé, seul le
  MD5 porte la preuve. Suite 2610 → **2645** / 2 skipped. SW v187
  inchangé.

- **Lot 371 — livré** : `/memory/cell/<group>/<key>`, la **route sœur**
  de la faille du lot 368 — même fichier, même auteur, même motif de
  rendu, donc forte probabilité du même défaut. **Verdict : SAINE, et
  prouvé sur des cellules réelles.** **Correction de méthode d'abord
  (la 5ᵉ de la boucle)** : ma première sonde écrivait les résultats sous
  la forme `{'hit': bool}` → **aucune cellule formée**, 404 partout,
  donc des « non » rassurants et **vides** — exactement le piège du
  lot 368. La vraie forme d'un résultat mesuré est
  `{'horizons': {'H5'|'H20'|'H60': {'status': 'MESURE', 'return_pct'}}}`
  (cf. `_measured_class`) ; sans horizon MESURE, aucune cellule n'existe.
  Sonde corrigée : **4 cellules rendues en 200 (~19 Ko)** avec des
  records hostiles, dont `by_regime` **dont la clé EST la charge**
  — elle traverse alors **à la fois l'URL et la donnée** : 0 charge
  brute, 0 balise active, `<title>` unique et clos, version échappée
  présente. **Pourquoi cette route tient là où l'autre a cédé** : son
  `title=` est une **constante** (`'Cellule de calibration'`) alors que
  la faille du lot 368 venait d'un titre nourri par la donnée, et chaque
  valeur du corps passe par `markupsafe.escape`, y compris la clé
  reconstruite. **Rien touché.** Gardien
  `tests/test_memoire_cellule_lot371.py` (5 tests) sur une mémoire
  **temporaire** — dont un **anti-vide** qui exige ≥4 cellules formées,
  pour que la fixture ne puisse plus tourner à vide en silence — et un
  test qui exige que le titre **reste** une constante. Preuve ROUGE ×2,
  dont la faute du lot 368 **transplantée** dans cette route (titre
  nourri par la donnée → 3 tests rouges). Aucun fichier de production
  touché → pas de preuve MD5 requise, pas de bump (`td-shell-v187`).
  Suite 2605 → **2610 / 2 skipped** verte (+5). Piste (a) — les
  interpolations serveur dans le `content=` de chaque page — reste
  ouverte et demande son propre lot.

- **Lot 370 — livré** : CHECKPOINT de la tranche 360-369. Serveur DEMO
  (`/scan` 20 lignes, `source=demo`) : **les 8 MD5 sont identiques aux
  références** — aucun octet servi n'a bougé de toute la tranche,
  cohérent avec dix lots dont **un seul** a touché un fichier de
  production (lot 368, une ligne d'échappement, dans une route hors des
  8 pages). Navigateur réel (Chromium 1194, 1440×900, après
  hydratation) : **0 erreur console, 0 `pageerror`** sur les 8 pages.
  **Unique écart, et c'est ma plage qui était fausse** : `/markets`
  mesure **2794**, soit exactement la **référence historique** — la
  plage `2795-2835` que j'avais construite autour des 2814 du lot 360
  excluait la référence elle-même. Erreur de construction, pas une
  régression (le MD5 identique le prouve) ; plage corrigée en
  **2790-2835**. Au passage, cela reconfirme la conclusion du lot 360 :
  le smoke dépend du jeu DEMO régénéré par session (2814 puis 2794 pour
  des octets identiques). **Bilan de tranche** : **1 vraie faille XSS
  trouvée et corrigée** (368 — titre du post-mortem non échappé), 3 trous
  (361 périmètre du SW, 364 gardiens emportés par la purge É1, 367 liste
  blanche non gardée), 1 divergence doc-vs-code (365 PORTFOLIO_FIT), et
  **3 verdicts « sain » étayés** (363 règle n°4 prouvée en navigateur,
  366 isolée sur 110 moteurs, 369 18/18 étiquettes sûres).
  **9 gardiens neufs**, suite **2530 → 2605 / 2 skipped (+75)**,
  **10 PR fusionnées** (#392 → #401), SW **`td-shell-v187` inchangé**
  toute la tranche, `main` jamais touchée. **Leçon dominante** :
  vérifier l'outil avant de conclure a changé le résultat **quatre
  fois** (367 le diff, 368 les charges avec `/` bloquées en 404
  Werkzeug, 369 la page d'erreur au même MD5, et ce lot-ci la plage mal
  construite).

- **Lot 369 — livré** : ÉTIQUETTES DU SHELL — suite directe de la faille
  du lot 368. Audit de **tous** les appels `render_shell` : **44
  étiquettes constantes** (sûres par construction) et **18
  interpolées**, tracées **une par une** jusqu'à leur source →
  **18/18 sûres** : `analysis_page` filtre explicitement les caractères
  (`safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')`),
  toutes les autres lisent `label`/`sub` dans un **dict de vues** après
  normalisation, et `options_intel` normalise `view` dès la première
  ligne. **La faille du lot 368 était isolée.** Asymétrie structurelle
  documentée : le chemin **fragment** échappe les 4 étiquettes
  (`escape(…, quote=True)`), le chemin **page complète** n'en échappe
  **aucune** — `<title>{title}`, `<b>{space_label}</b>`,
  `<span>{sub_label}</span>` et surtout
  `data-page-label="{page_label or space_label}"`, **dans un attribut**,
  où un simple guillemet suffirait à sortir. Cause identifiée :
  `from html import escape` est un import **local à
  `_render_fragment`** — l'échappement n'existe que là où l'import
  existe. **Le dossier en attente de GO est désormais CHIFFRÉ** :
  durcissement appliqué temporairement puis restauré (MD5 du fichier
  vérifié) → **7 pages sur 8 inchangées à l'octet près**, seule `/`
  bouge parce que son titre est `"Aujourd'hui"` et que l'apostrophe
  devient `&#x27;` — **visuellement identique**, coût réel = un bump SW
  + une nouvelle référence MD5 pour `/`. **Rien engagé** : la décision
  reste vôtre, mais avec le chiffre. **Correction de méthode (encore
  une)** : ma première mesure annonçait « 8/8 pages changeraient » avec
  le **même MD5 sur les 8** — absurde pour 8 pages différentes ; c'était
  une page d'erreur (`NameError`, `escape` hors de la portée de son
  import local). Sans ce doute, j'aurais rapporté un chiffre faux et
  peut-être fait renoncer à un durcissement quasi gratuit. Gardien
  `tests/test_etiquettes_shell_lot369.py` (**27 tests**) : 3 charges ×
  7 routes via `?view=` et via le segment, `<title>` reste unique et
  clos, aucun `data-page-label` ne contient `"` ni `<`, plus deux tests
  de contrat (le fragment échappe ; la page complète reste le seul
  chemin non échappé — à mettre à jour le jour du durcissement). Aucun
  fichier de production touché → pas de preuve MD5 requise, pas de bump
  (`td-shell-v187`). Suite 2578 → **2605 / 2 skipped** verte (+27).

- **Lot 368 — livré** : SEGMENTS DE CHEMIN — **une vraie faille XSS
  trouvée et corrigée**. Jumelle du lot 367, mais sur les segments
  (`/analysis/<sym>`, `/memory/<id>`), du texte libre donc plus exposé.
  **Correction de méthode d'abord** : ma première sonde envoyait des
  charges contenant `/` — Werkzeug refuse `%2F` dans un segment et rend
  son 404 par défaut (701 octets), la charge n'atteignait **jamais** le
  rendu ; 28 lignes de « non » rassurants et vides. Refaite sans barre
  oblique : 18 requêtes sur 42 rendent alors une vraie page.
  **(1) Le symbole est sain, doublement protégé** :
  `/analysis/"><img src=x onerror=alert(1)>` → 200, 75 216 octets,
  `const SYM="IMGS"` (non-alphanumériques **retirés** avant injection JS)
  et texte **échappé** (`&lt;`, `&quot;`, `&gt;`) ; redirections
  `/titre/` et `/company/` **relatives** (pas de redirection ouverte) ;
  CRLF refusé par Werkzeug. 0 fuite sur 6 charges × 7 gabarits.
  **(2) `/memory/<decision_id>` : FAILLE RÉELLE.** La page (200,
  19 371 o, 1 bloc inline qui parse, 35 `id` sans doublon) est celle que
  le lot 359 signalait comme non couverte. Sa docstring promet « TOUT
  contenu de la mémoire est ÉCHAPPÉ (XSS) » — **c'était faux pour le
  titre** : le corps utilisait bien `markupsafe.escape`, l'argument
  `title=` de `render_shell` l'avait oublié. Mesuré : un symbole
  `</title><script>alert(1)</script>` **sort de la balise** et injecte
  un **`<script>` actif dans le `<head>`**. **Portée dite franchement** :
  le `symbol` vient du moteur de décision (univers contrôlé), pas d'une
  saisie utilisateur ; l'exploitation suppose d'écrire dans
  `skyler_memory.json`, fichier local — **pas exploitable à distance**,
  mais défense en profondeur absente et **promesse fausse dans la doc du
  code**. **Corrigé en une ligne** (`_e(rec.get('symbol'))` dans le
  titre) : ce n'est pas implémenter une fonctionnalité manquante
  (règle du lot 365), c'est faire tenir au code une promesse qu'il
  affichait déjà. Gardien `tests/test_segments_url_lot368.py`
  (**12 tests**, record hostile injecté dans une mémoire **temporaire** —
  le vrai `skyler_memory.json` jamais touché) ; **une assertion du
  gardien était elle-même trop stricte** (elle refusait `onerror=alert`
  même échappé, donc inerte) → corrigée pour ne viser que la forme
  exécutable. Preuve ROUGE sur la faute réelle (correctif retiré →
  2 tests rouges). Fichier de production modifié → preuve exigée :
  **MD5 des 8 pages, 0 écart / 8** → pas de bump (`td-shell-v187`).
  Suite 2566 → **2578 / 2 skipped** verte (+12). Piste ouverte : auditer
  **tous** les `render_shell(title=…)`, même classe de défaut ; le
  durcissement de fond (échapper le titre dans `render_shell`) toucherait
  toutes les pages servies — en attente de GO.

- **Lot 367 — livré** : VARIANTES `?view=` — les gardiens JS ne balayent
  que les routes **nues** ; les variantes servent-elles du JS jamais
  parsé (le trou du lot 359, en plus grand) ? **37 variantes découvertes
  en lisant les onglets du HTML servi** — ma liste tirée d'un grep du
  code n'en voyait que **25** (elle manquait `?view=learnings`,
  `progression`, `events`, `positioning`, `impacts`, `macro`) :
  première correction de méthode, **découvrir depuis le servi, pas
  depuis la source**. Ces variantes servent **16 blocs `<script>`
  inline absents des routes nues** — soit un trou 4× celui du lot 359.
  **Puis le diff a démenti la piste** : entre une route nue et sa
  variante, **2 lignes d'écart** — `const VIEW="team"` → `const
  VIEW="risk"` — le JavaScript est identique au reste près. Une faute de
  syntaxe s'y verrait sur la route nue, déjà balayée par le lot 182.
  **Il n'y a pas de trou** ; un gardien qui reparse 16 quasi-doublons
  aurait coûté du temps pour rien. (`/intelligence`, `/system`,
  `/options` servent même des blocs strictement identiques entre leurs
  vues.) **Le constat utile est ailleurs** : ce paramètre d'URL atteint
  les octets servis — constante `const VIEW=…` dans le JS de 4 pages,
  attribut `data-view` sur 2 autres — et sa sûreté ne tient qu'à une
  **liste blanche serveur que rien ne testait**. Sondée avec 3 charges
  hostiles (sortie de chaîne JS, sortie d'attribut, fermeture de
  `<script>`) × 8 routes : **aucune fuite**, la valeur inconnue retombe
  partout sur la vue par défaut. Livré : gardien
  `tests/test_vues_parametre_lot367.py` (**33 tests**, dont un anti-vide
  exigeant qu'une vue légitime change bien la page), preuve ROUGE en
  retirant la liste blanche de Portefeuille. Aucune vulnérabilité
  trouvée : le lot ferme une **fenêtre de non-détection sur un chemin
  d'injection**, il ne répare rien. Aucun fichier de production touché →
  pas de preuve MD5 requise, pas de bump (`td-shell-v187`). Suite
  2533 → **2566 / 2 skipped** verte (+33). **La conclusion la plus utile
  est négative** : sans le diff, ce lot aurait posé un gardien inutile
  et annoncé une faille imaginaire.

- **Lot 366 — livré** : GÉNÉRALISATION DU LOT 365 — la trouvaille
  (`thesis_health` annonçant PORTFOLIO_FIT sans le calculer) était-elle
  isolée ou un motif ? Les **110 modules** de `vertex/engines`,
  `positions`, `options`, `scanner`, `strategy` et `ai` passés à la même
  question. **Verdict : ISOLÉE**, aucune autre promesse non tenue. Les
  10 candidats triés : contrats de gouvernance (`SKYLER_ARCHITECTURE`,
  `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS` — vérifiés présents
  dans le SKILL et les rapports), notation mathématique (`S_T`),
  constantes produites par un **module frère** (`ULTRA_CONVEX` et
  `MODEL_ESTIMATE` viennent d'`options/models.py`, via `CALL_CATEGORIES`
  et `GREEKS_MODEL`), et la note du lot 365 elle-même. **Deux erreurs de
  méthode payées comptant et signalées** : (1) un premier filtre « tout
  jeton majuscule ≥4 lettres » a produit **139 faux suspects** noyés
  dans les mots français en capitales — corrigé en exigeant un
  **souligné** (identifiant machine, pas prose) : 139 → 10 ; (2) chercher
  l'identifiant dans le **seul module** qui l'annonce produit des faux
  positifs — la recherche doit couvrir le **paquet**. **Rien touché**
  (« sain » est un verdict, pas un aveu). Ce qui manquait n'était pas un
  correctif mais la **permanence** de la vérification, deux lots l'ayant
  posée avec un script jetable : gardien
  `tests/test_promesses_docstrings_lot366.py` (3 tests, dont « une
  tolérance de gouvernance sans justification dans le SKILL ou les
  rapports est un trou »), dont le message d'échec rappelle la règle du
  lot 365 — corriger la DOC, jamais implémenter à la volée. Preuve ROUGE
  ×2, dont la faute du lot 365 **transplantée dans `anomaly.py`**
  (anomalie `GAP_RUPTURE` annoncée, jamais produite) : attrapée.
  Limite dite : une promesse en un seul mot majuscule échappe au filtre,
  et les docstrings de fonctions ne sont pas balayées. Aucun fichier de
  production touché → pas de preuve MD5 requise, pas de bump
  (`td-shell-v187`). Suite 2530 → **2533 / 2 skipped** verte.

- **Lot 365 — livré** : IDENTIFIANTS CITÉS EN PROSE (piste (a) laissée
  ouverte par le lot 364). Extraction depuis les docstrings/commentaires
  de `vertex/` + `terminal.py` de deux formes calibrées (constantes
  `CAPS_SNAKE`, appels `nom()`), confrontées au code réel du dépôt :
  **23 appels cités, 0 mort** ; 117 constantes citées dont 16
  « introuvables » — examinées **une par une** et toutes légitimes :
  noms de contrats de gouvernance (`SKYLER_ARCHITECTURE`,
  `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS`,
  `SCENARIO_CALIBRATION`, présents dans le SKILL et les rapports),
  notation mathématique (`S_T`), nom de document
  (`VERTEX_WIDGET_LIBRARY.md`, qui **existe** — ma première vérification
  cherchait la chaîne dans le CONTENU des docs, pas dans les noms de
  fichiers ; faux positif corrigé en cours de lot et signalé), et codes
  d'anomalie écrits en majuscules alors que le moteur émet
  `'vol_shift'` (convention, pas divergence). **UNE divergence réelle** :
  `vertex/positions/thesis_health.py` annonçait **7 dimensions** dont
  **PORTFOLIO_FIT**, alors que son code (97 lignes, vérification
  exhaustive) n'a que **5 sections** — `# FUNDAMENTAL`, `# CATALYST`,
  `# TECHNICAL`, `# SENTIMENT`, `# RISK / DATA_QUALITY` : **aucune ligne
  ne regarde l'adéquation au portefeuille**. Piège aggravant :
  `portfolio_fit` existe vraiment ailleurs (`scanner/stages.py`,
  `strategy/executive_engine.py`), donc on pouvait croire que la santé
  de thèse — qui alimente l'état de thèse affiché sur Portefeuille — en
  tenait compte. Correctif : la docstring dit désormais ce que le module
  évalue ET ce qu'il n'évalue pas, avec le renvoi vers les modules qui
  produisent réellement `portfolio_fit`. **Aucune dimension ajoutée** :
  implémenter à la volée une adéquation au portefeuille aurait mis un
  chiffre inventé dans un verdict de santé — c'est une décision produit,
  en attente de GO. Gardien `tests/test_thesis_health_dimensions_lot365.py`
  (3 tests, dont « PORTFOLIO_FIT reste écrit comme non évalué » qui
  réclamera sa mise à jour le jour où il sera implémenté) ; preuve ROUGE
  ×2 dont **la faute rejouée**. Un fichier de production ayant changé
  (docstring seule), preuve exigée : serveur DEMO + **MD5 des 8 pages,
  0 écart / 8** → pas de bump (`td-shell-v187`). Suite 2527 →
  **2530 / 2 skipped** verte.

- **Lot 364 — livré** : AUTO-RÉFÉRENCES — « ce que le projet dit de
  lui-même est-il vrai ? », suite du lot 71 (qui avait trouvé une
  docstring citant un gardien inexistant et posé le contrat pour
  `vertex/`). Deux angles morts restaient : `terminal.py` et les
  documents. Mesure : **0** chemin de module `vertex/**.py` mort,
  **0** route sur les **29** routes `/api/…` citées en commentaire
  (toutes dans l'`url_map`), mais **7 références de tests inexistants,
  toutes dans `docs/`**. Enquête git : trois gardiens créés aux
  lots 183/184/185 ont été **supprimés par la purge É1 du lot 323**
  (`80a1729`, PR #355) — comme le plan le prévoyait, sa catégorie B
  s'appelant littéralement « retrait avec leurs tests » — mais **rien
  ne l'écrivait**. `ANNEXE-E1-RETRAITS.md`, qui est le document de
  PREUVE de la purge, laissait donc sa piste de vérification rompue :
  un lecteur cherchant ces gardiens ne les trouvait pas et ignorait
  pourquoi. **C'est mon propre travail (lot 323) qui a créé l'écart.**
  La 7ᵉ référence est la citation historique du défaut du lot 71
  lui-même, légitime. Livré : **statut d'exécution** ajouté à l'annexe
  (commit, PR, ampleur, les 3 gardiens marqués RETIRÉ avec leur lot de
  création) — les rapports `SKYLER-LOT-183/184/185.md` ne sont PAS
  touchés, ce sont des archives et les réécrire falsifierait
  l'histoire ; et gardien `tests/test_references_vivantes_lot364.py`
  (7 tests) : contrat du lot 71 **étendu à `terminal.py`**, même
  contrat sur les chemins de modules, et pour les **documents vivants**
  — citer un gardien disparu est permis **à condition de dire qu'il a
  été retiré** sur la ligne qui le nomme. Preuve ROUGE ×2, dont la
  faute historique du lot 71 rejouée dans le fichier que son gardien ne
  regardait pas ; fichiers restaurés MD5 identique. Aucun code n'était
  faux : le défaut était une piste de preuve rompue. Aucun octet servi
  → pas de bump (`td-shell-v187`). Suite 2520 → **2527 / 2 skipped**
  verte.

- **Lot 363 — livré** : RÈGLE N°4 (« données RÉELLES uniquement ; le mot
  démo ne s'affiche que si le serveur le confirme ») — **SAINE, et
  prouvé plutôt que supposé**. (1) Les données DEMO sont bien
  synthétiques et le serveur le dit (`_demo_universe`,
  `scan_state['source']='demo'` ; mesuré : taux 3 mois à **35,6 %**,
  manifestement fabriqué). (2) Les **8 pages préviennent** en navigateur
  réel après hydratation : « DÉMO — Données synthétiques clairement
  identifiées, jamais présentées comme réelles » sur `/`, `/markets`,
  `/opportunities`, `/portfolio`, `/journal` ; « board démo » sur
  `/options` (correctif du lot 296, toujours en place) ; « Mode global
  demo » sur `/system`. `/analysis` n'a que le chip de nav — c'est une
  page de **recherche** sans donnée de marché, cohérent. (3) Recensement
  des couples `source:`/`mode:` servis, seul endroit où une chaîne peut
  mentir sur la réalité d'un chiffre : **31 dérivés du serveur,
  59 constants, 0 affirmant réel/live** — les constants valent `delayed`
  / `index` ou nomment un moteur. Mais la règle s'était **déjà perdue
  deux fois** (lot 296 « board réel » en dur, lot 297 chip « Live » en
  dur) et rien n'empêchait une troisième : gardien neuf
  `tests/test_honnetete_provenance_lot363.py` (4 tests, dont un
  anti-vide). **Preuve ROUGE : les deux fautes historiques rejouées sont
  attrapées**, fichiers restaurés MD5 identique. Observation laissée
  telle quelle : « 4 maturités réelles » / « points réels du scan » sur
  `/markets` parlent de méthode, pas de provenance — ambigu à côté d'un
  badge démo, mais pas faux ; reformuler serait un octet servi modifié
  pour du style, décision humaine. Aucun octet servi → pas de bump
  (`td-shell-v187`). Suite 2516 → **2520 / 2 skipped** verte.
  **Bilan des 5 règles passées à la question : 4 trouvailles** (n°2, n°3,
  n°5 = trous ; n°6 = promesse plus étroite ; n°4 = saine).

- **Lot 362 — livré** : RÈGLE N°6 (celle qui protège les données réelles
  de l'utilisateur) passée à la même question. **Sain** : la chaîne de
  sauvegarde tient (snapshot quotidien avant écrasement, rotation à 7,
  restore au nom strictement validé — traversée refusée, `ts` neuf pour
  que tous les appareils re-tirent), et le client se protège bien
  (`vx_kit.py` ne pousse qu'après hydratation réussie, s'abstient si
  `bootSync` échoue, re-remplit toute clé absente). **Trois faits
  mesurés** que la règle ne disait pas, sonde isolée dans un dossier
  temporaire (le vrai `desk_data.json` jamais touché) : (1) un push
  `data: {}` est **accepté en 200** et vide le blob — la validation
  porte sur le TYPE, `{}` est un dict, donc l'écrasement n'a pas besoin
  d'être « à la main » ; (2) le last-writer-wins est **total**, un push
  partiel efface les clés absentes ; (3) **aucun snapshot
  supplémentaire** n'est pris à ce moment-là → un restore rend l'état
  d'**avant la 1ʳᵉ sync du jour** et **perd le travail de la journée**,
  avec au plus **7 jours** de profondeur. Scénario résiduel réaliste :
  navigateur dont l'écriture localStorage échoue en silence (navigation
  privée, quota). Livré : gardien de **caractérisation**
  `tests/test_desk_perte_lot362.py` (5 tests, messages d'échec = « mettre
  à jour ce gardien ») + règle n°6 corrigée dans `CLAUDE.md`. Preuve que
  le gardien ALERTE : durcissement simulé (refus du push vide) → ROUGE,
  fichier restauré MD5 identique, 5 verts après restauration.
  **Rien durci** — refuser un push vide changerait le contrat de sync
  assumé ; 3 options en attente de GO humain (A : snapshot
  supplémentaire avant perte, **recommandée**, purement additive ;
  B : refus 409 ; C : fusion par clé). Aucun octet servi modifié → pas
  de bump (`td-shell-v187`). Suite 2511 → **2516 / 2 skipped** verte.

- **Lot 361 — livré** : RÈGLE N°3 passée à la question qui a donné les
  lots 358 et 359. La règle disait « tout changement de **shell visible
  utilisateur** → bump `td-shell-vN` ». Le service worker, lui, met en
  cache **tout `/static`** (54 fichiers servis : 34 JS, 17 CSS,
  2 polices) **plus** les navigations et le manifeste ; il est
  *network-first* (`Promise.race([fetch, timeout 4500])`), le cache ne
  sert qu'en repli ; `activate` supprime tous les caches dont la clé
  diffère. Deux vérités absentes de la règle : le périmètre est **plus
  large que « le shell »**, et le bump ne sert pas à « faire voir » la
  nouvelle interface (le network-first s'en charge) mais à **purger la
  copie de repli hors-ligne**. Fenêtre d'exposition : visiteur déjà
  venu, hors-ligne ou réseau > 4,5 s, servi depuis un cache assemblé au
  fil de visites différentes. Mesure de l'historique : **27 commits sur
  144** touchant `vertex/static` sans bump — **conformes à la règle
  écrite**, donc le défaut est dans la règle, pas dans la discipline.
  Livré : gardien `tests/test_sw_cache_scope_lot361.py` (5 tests —
  sémantique du SW figée + contrat empreinte SHA-256 des assets ↔
  version enregistrée, daté d'aujourd'hui, ne juge pas l'historique) et
  règle n°3 corrigée dans `CLAUDE.md`. Preuve ROUGE sur les 4
  propriétés, fichiers restaurés MD5 identique. Aucun bug utilisateur
  observé (en ligne le frais gagne toujours) : le lot rend la règle
  exacte et applicable, au prix d'une **friction assumée** (tout
  changement d'asset exigera un bump + 2 constantes). Solution de fond
  non engagée : empreinte dans les URL d'assets — demande un GO humain.
  Aucun octet servi modifié → pas de bump (`td-shell-v187`). Suite
  2506 → **2511 / 2 skipped** verte.

- **Lot 360 — livré** : CHECKPOINT de la tranche 350-359. Serveur DEMO
  (`/scan` 20 lignes) : **les 8 MD5 sont identiques aux références** —
  aucun octet servi n'a bougé depuis le lot 350. Navigateur réel
  (Chromium, 1440×900, après hydratation) : **0 erreur console** sur les
  8 pages. Toutes les tailles smoke sauf `/analysis` (923, exact)
  s'écartaient : deux vérifications avant de conclure. (a) La mesure hors
  navigateur n'est pas comparable (les pages s'hydratent côté client :
  `/` 510 en HTML brut). (b) **À MD5 identique, le smoke bouge** — deux
  passes à 90 s d'écart : `/` 3367 → 3385 (**+18 caractères, MD5
  stable**), les 5 autres pages à delta 0. Les libellés de fraîcheur
  changent de longueur. Conclusion d'instrument : **le MD5 est la seule
  preuve stricte inter-sessions ; le smoke mesure le contenu hydraté**
  (horloge, jeu DEMO régénéré par session, `desk_data.json` local) et
  est donc requalifié en **plage indicative**, jamais opposable au MD5.
  Chaque écart tracé dans le rapport : `/markets` +20 et
  `/opportunities` −93 = jeu DEMO de la session (stables en session) ;
  `/system` +2/+3 = plage du lot 340 structurellement trop étroite pour
  une page qui imprime des âges ; `/journal` +1010 = sondes locales du
  lot 305 (documenté depuis le lot 330). Bilan de tranche : 8 lots
  « sain, rien touché », 2 trouvailles (358 : 2ᵉ famille de sorties de
  news ; 359 : `/analysis` hors gardiens JS) — les deux nées de la même
  question, « la règle écrite décrit-elle vraiment le code servi ? ».
  Suite 2501 → **2506 / 2 skipped**, SW `td-shell-v187` inchangé sur
  toute la tranche, 10 PR fusionnées (#382 → #391), `main` intacte.

- **Lot 359 — livré** : GARDIENS JS — même question qu'au lot 358 appliquée
  à la règle critique n°2 (« tout JS généré doit être syntaxiquement
  valide ») : ses gardiens (lots 182 et 186) travaillent sur une **liste
  de routes figée**. Inventaire complet de l'`url_map` (chaque règle GET
  appelée sans suivre les redirections) : les 40 routes hors liste sont
  des **301** vers des pages canoniques, mais **`/analysis`** (index,
  `analysis_page.render_index` — fonction distincte de `render(sym)` qui
  sert `/analysis/<sym>`) est une **page HTML 200 servie, 22 248 o,
  2 blocs `<script>` inline**, absente des DEUX gardiens. Sa syntaxe JS
  et ses liens d'assets n'ont jamais été vérifiés — alors qu'elle est
  l'une des 8 pages de la référence smoke. Ajoutée aux deux listes.
  Preuve ROUGE en rejouant le bug historique de la règle n°2 (apostrophe
  française non échappée dans une chaîne JS simple) : **ancienne liste
  0 erreur — totalement aveugle ; nouvelle liste attrape**, fichier
  restauré MD5 identique. Aucune faute n'existait : le lot ferme une
  fenêtre de non-détection, il ne répare rien. Aucun octet servi modifié
  → pas de bump (`td-shell-v187`). Suite **2506 / 2 skipped** verte.

- **Lot 358 — livré** : SORTIES DE NEWS — la règle critique n°5 décrivait
  UNE famille de sorties ; il y en a **deux**. `/api/ai/enrichment`
  (cerveau Claude+web) sert le titre d'actualité **non neutralisé**
  (mesuré : `<script>alert(1)</script>Titre`) et n'était couvert par
  aucun gardien. Ce n'est pas un trou — son unique rendu
  (`system_page.py::loadBrain`) échappe via `esc()`, les citations sont
  filtrées http(s), la forme est reconstruite et bornée — mais rien ne
  figeait ces trois propriétés, et y ajouter `sanitize_news`
  **double-échapperait** les titres légitimes. Livré : gardien neuf
  `tests/test_ai_news_exit_lot358.py` (5 tests, preuve ROUGE sur les
  3 défenses, fichiers restaurés MD5 identique) + règle n°5 de
  `CLAUDE.md` corrigée (deux familles, deux contrats, leurs gardiens).
  Première rédaction du gardien `esc()` **ne mordait pas** (fenêtre de
  30 caractères) → refaite en analyse des appels englobants, re-prouvée.
  Aucun octet servi modifié → pas de bump (`td-shell-v187`).
  Suite **2501 → 2506 / 2 skipped** verte.

- **Lot 357 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour e19305a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 356 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 63b9559, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 355 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 91b0d6c, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 354 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 92eec8f, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 353 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 6aadd19, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 352 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 51ff1ec, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 351 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 843b21a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (le lot 350 vient de tout mesurer, aucun octet n'a bougé).
  Docs seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine.

- **Lot 350 — livré** : **ÉCHÉANCE PÉRIODIQUE (10e mesure) + BILAN
  340-349**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** — et pour la première fois **les 8 tailles de texte
  tombent TOUTES dans leurs références**, y compris les deux qui avaient
  demandé une explication au lot 340 : `/journal` 3 690 (desk local de
  la session) et **`/system` 4 123**, qui confirme par une seconde
  observation la fourchette rebasée (4 122-4 124). Le rebasage du lot
  340 n'était pas un ajustement de confort : il décrivait la réalité.
  **Les 8 MD5 conformes** ; `/sw.js` sert `td-shell-v187` ; suite
  **2501 / 2**.
  **BILAN de la tranche — « la croisière tenue »** : dix lots, **zéro
  changement produit, zéro défaut détecté**, et c'est le résultat
  correct, pas un aveu d'inaction — les filons « code mort » et « textes
  périmés » ont été épuisés dans la tranche précédente, et fabriquer du
  travail pour remplir un rapport aurait été la seule vraie faute
  possible. 340 = échéance 9e mesure + bilan 330-339 avec le **rebasage
  de la fourchette `/system`** (le lot 328 avait retiré deux caractères,
  la référence ne l'avait jamais enregistré) ; 341-349 = neuf cycles de
  veille, règle appliquée sans exception : **ne pas re-mesurer ce qui
  n'a pas bougé**. Chiffres : suite **2501 constante sur les 10 lots**,
  SW **v187 constant**, terminal.py **inchangé à 7 153 l.**, **10 PR
  fusionnées (#372 → #381)**. Prochaine échéance ~lot 360. Pas de bump.

- **Lot 349 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 30f62ec, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (la 10e mesure est pour le lot 350). Docs seulement, pas de
  bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 348 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 09246b2, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 347 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 72c13c7, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 346 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 26e1910, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 345 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 59dcdf6, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 344 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 985db84, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 343 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 593208a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 342 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5498b86, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 341 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 0b37527, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (le lot 340 vient de tout mesurer, aucun octet n'a bougé).
  Docs seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine.

- **Lot 340 — livré** : **ÉCHÉANCE PÉRIODIQUE (9e mesure) + BILAN
  330-339**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** ; 6 tailles sur 8 identiques aux références. Les deux
  écarts sont expliqués, pas arrondis : `/journal` 3 690 (le desk local
  porte les trades de la sonde du lot 305 ; MD5 du HTML servi inchangé
  — tranché au lot 330) et **`/system` 4 123 au lieu de 4 124-4 126 :
  conséquence attendue du lot 328**, qui a retiré les deux caractères
  `__` du libellé `__DESK_KEYS`. La référence n'avait pas été rebasée →
  **nouvelle fourchette 4 122-4 124**. Ce n'est pas une dérive, c'est le
  lot 328 qui devient enfin visible dans la mesure de taille.
  **Les 8 MD5 conformes** ; `/sw.js` sert `td-shell-v187` ; suite
  **2501 / 2**.
  **BILAN de la tranche — « le retour au régime de croisière »** : une
  échéance (330) puis neuf cycles de veille (331-339) où le travail
  consistait surtout à **ne pas en inventer**. Une règle les a
  structurés : **ne pas re-mesurer ce qui n'a pas bougé** — le lot 330
  avait tout mesuré, aucun octet n'a changé ensuite ; refaire le smoke à
  chaque réveil aurait produit neuf pages de chiffres identiques, du
  bruit déguisé en preuve. Les rapports le disent au lieu de faire
  semblant d'avoir vérifié. Chiffres : suite **2501 constante sur les
  10 lots**, SW **v187 constant**, terminal.py **inchangé à 7 153 l.**,
  **10 PR fusionnées (#362 → #371)**, 0 changement produit, 0 défaut
  détecté. Prochaine échéance ~lot 350. Pas de bump.

- **Lot 339 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ea14e1d, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (la 9e mesure est pour le lot 340). Docs seulement, pas de
  bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 338 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 780ec58, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 337 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 07171f7, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 336 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ec8444d, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 335 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 9c61b24, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 334 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 96e4fc5, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 333 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour e9108ed, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 332 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 9f466cd, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 331 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5e6809e, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle. Pas de
  re-mesure : le lot 330 vient de mesurer l'état complet et aucun octet
  n'a bougé depuis — re-mesurer serait du bruit, pas une preuve. Docs
  seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine (É2, É3, les 24 fonctions, les 5 modules reliques).

- **Lot 330 — livré** : **ÉCHÉANCE PÉRIODIQUE (8e mesure) + BILAN
  320-329**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** ; 7 tailles sur 8 identiques aux références.
  **`/journal` à 3 690 au lieu de 2 676 — expliqué, pas masqué** : le
  `desk_data.json` local porte les 3 trades laissés par la sonde du lot
  305, et le texte rendu le dit mot pour mot (« 3 trade(s) clôturé(s) :
  33 % de réussite, P&L cumulé -700 »). Preuve que ce n'est pas une
  régression : **le MD5 du HTML servi pour `/journal` est INCHANGÉ**
  (243699ace2d5) — le serveur envoie les mêmes octets, tout l'écart
  naît de l'hydratation locale. **Les 8 MD5 conformes** (dont `/system`
  73e917c0f2d0) ; `/sw.js` sert `td-shell-v187` ; suite **2501 / 2**.
  **BILAN de la tranche — « celle qui a enfin coupé »** : après dix lots
  de croisière, le blocage de permissions est tombé et la tranche est
  passée au travail de fond — purge É1 (**-33 % de terminal.py**, 82
  défs), hygiène des imports (terminal.py puis les 183 modules de
  vertex/, 2 gardiens AST posés), 3 pistes instruites dont une laissée à
  l'humain, `CLAUDE.md` remis au vrai avec correction de ma propre
  erreur du 323, libellé périmé corrigé avec bump SW assumé, puis
  vérification que c'était un cas isolé. Chiffres : suite **2516 →
  2501** (les 17 tests retirés étaient écrits POUR la purge), SW **v186
  → v187**, **10 PR fusionnées (#352 → #361)**, terminal.py **-3 590
  lignes**. Leçon de fond : **trois fois le réflexe évident aurait été
  une erreur** (l'import `BROKER` qui EST un diagnostic, les 24 façades
  IBKR qui sont le chemin de lecture du compte réel, ma propre règle qui
  citait un fichier mort) — un compteur ne distingue pas le mort de
  l'endormi. Prochaine échéance ~lot 340. Pas de bump.

- **Lot 329 — livré** : LE LOT 328 ÉTAIT-IL UN CAS ISOLÉ ? **Oui — SAIN,
  rien touché.** Après le retrait de 82 définitions, d'autres libellés
  pouvaient citer des noms qui n'existent plus. La mesure est faite
  **dans le navigateur, sur le texte RENDU** (`document.body.innerText`)
  et non sur le HTML brut — une bonne part des libellés est écrite par
  le JS après hydratation. **16 vues** balayées : les 8 racines, la
  fiche `/analysis/NVDA`, les 3 sous-vues Système (données, réglages,
  archive), Marchés → ampleur, Opportunités → anomalies, Portefeuille →
  risque, Journal → track-record. Extraction des jetons ressemblant à un
  identifiant technique (snake_case, noms de fichiers), puis
  confrontation au code réel : **30 identifiants affichés, 0
  introuvable**. `__DESK_KEYS` était bien un cas isolé, corrigé au lot
  328. MD5 des 8 pages identiques aux références (dont `/system`
  73e917c0f2d0), `/sw.js` sert `td-shell-v187`, suite **2501 / 2
  skipped**. Pas de bump.

- **Lot 328 — livré** : HONNÊTETÉ D'AFFICHAGE. La page Système annonçait
  à l'utilisateur « Clés synchronisées — 17 (contrat **`__DESK_KEYS`** —
  aucune clé renommée) ». Ce symbole a **disparu avec la purge É1** : il
  nommait la liste qui vivait dans le JS des pages mortes. Le contrat
  existe toujours, il s'appelle `DESK_KEYS` (vx_kit + vx-entities).
  L'affirmation n'était pas fausse sur le fond, mais elle nommait un
  symbole **introuvable dans le code** — un trader qui irait vérifier ne
  trouverait rien. Invariant n°4. Repéré au lot 327, mis en réserve
  parce qu'il change un octet servi ; traité ici avec le protocole
  complet. Correctif = **une chaîne**. Preuve chirurgicale : **7 MD5
  identiques, seul `/system` change** (85d1cb065d2e → **73e917c0f2d0**,
  nouvelle référence) ; le HTML servi contient `contrat DESK_KEYS` et
  **0 occurrence de `__DESK_KEYS`** ; smoke 8×200, 0 erreur console,
  client-log 0. **Bump SW `td-shell-v186` → `td-shell-v187`** + les
  5 gardiens SW mis à jour. Suite **2501 / 2 skipped**.

- **Lot 327 — livré** : **`CLAUDE.md` REDEVIENT VRAI**. Les lots 323-325
  ont retiré 33 % de terminal.py ; la documentation de pilotage — le
  fichier que chaque session lit en premier — décrivait encore l'état
  d'avant. Trois affirmations vérifiées, trois fausses.
  (1) « Monolithe ~10 500 lignes » → **7 153** (historique 10 743
  conservé pour que le chiffre reste interprétable).
  (2) « Pages extraites : nav, options_lab, journal, vault, signals,
  sync_center, vx_kit, design_system » — vérification consommateur par
  consommateur : `nav`, `vx_kit`, `sync_center`, `design_system` et
  `home_art` sont servis ; **`options_lab`, `journal`, `vault`,
  `signals` et `strategy_os` ont 0 consommateur en production**. Ce sont
  des reliques — **non supprimées**, elles rejoignent le dossier ouvert
  du lot 326.
  (3) **Correction de ma propre erreur du lot 323** : j'y avais annoncé
  `vertex/ui/journal.py` comme l'une des « 3 listes servies » de clés de
  sync desk. Il **n'est pas servi** — je l'avais repris du gardien sans
  vérifier. Les listes réellement servies sont `vx_kit.py` (source de
  vérité), `vx-entities.js`, et **le repli `deskKeys()` de
  `system_page.py`** — cette troisième n'était citée nulle part, c'est
  celle qu'on aurait pu oublier. Aucune donnée utilisateur en jeu :
  `vxJournal` est géré en production par `vx-entities.js`.
  Mis en réserve pour un lot dédié : la page Système affiche « contrat
  `__DESK_KEYS` », symbole disparu avec la purge É1 — le corriger change
  un octet servi, donc bump SW + 5 gardiens assumés.
  Suite **2501 / 2 skipped**, pas de bump (docs seulement).

- **Lot 326 — livré** : TROIS PISTES INSTRUITES, **aucun code touché**.
  (a) Fichiers statiques : 51 CSS/JS, chacun cherché par nom dans tout
  le dépôt → **0 non référencé**, SAIN. (b) Routes : **186 routes**
  d'`app.url_map`, préfixe statique cherché dans le JS servi et les
  modules qui construisent l'UI → **0 orpheline**, SAIN.
  (c) Fonctions top-level jamais citées ailleurs (décorateurs exclus) :
  **24 fonctions / 258 lignes** — data_sources 9, research 5, scanner 1,
  anomalies 2, observability 3, strategy 4. **DOSSIER OUVERT, rien
  retiré** : le gros est constitué des façades d'intégration IBKR
  (`fetch_positions`, `fetch_snapshot`, `fetch_daily_bars`,
  `fetch_expirations`, `qualify_stock`…), c'est-à-dire le chemin de
  lecture du compte réel via TWS. « Jamais citée » ne veut pas dire
  « morte » : ça peut vouloir dire « porte d'une intégration pas encore
  recâblée », et supprimer serait détruire du travail d'intégration, pas
  nettoyer. C'est la leçon du lot 325 (`BROKER`) à plus grande échelle :
  **un compteur ne distingue pas le mort de l'endormi.** Trancher demande
  une décision produit — elle appartient à l'utilisateur, comme É2 et É3.
  Suite **2501 / 2 skipped**, pas de bump.

- **Lot 325 — livré** : L'AUDIT D'IMPORTS ÉTENDU À TOUT `vertex/`
  (183 modules). Premier chiffre trompeur : 192 « orphelins », dont
  **180 sont `from __future__ import annotations`** — une directive du
  compilateur, jamais référencée par un nom. Faux positif écarté ; il
  restait **12 suspects**, chacun vérifié individuellement (0 ré-import
  ailleurs, 1 seule occurrence dans son fichier).
  **1 des 12 n'était pas mort** : `from vertex.services.live_stream
  import BROKER` dans `services/startup.py` — **l'import EST le
  diagnostic** : s'il échoue, l'étape de démarrage bascule en DEGRADED.
  Le retirer aurait produit un « READY » inconditionnel, donc un
  mensonge sur l'état du flux SSE. Conservé, marqué `# noqa: F401` et
  commenté pour qu'aucun nettoyage futur ne le reprenne. C'est le seul
  intérêt réel du lot : la différence entre un import mort et un import
  qui travaille sans être lu ne se voit pas dans un compteur.
  **11 retraits** effectifs (SEV_INFO, time, Iterable, os,
  CATEGORY_BALANCED, CATEGORY_BEARISH_TACTICAL, vol, np,
  LifecycleError, any_blocking, STATUSES) — tous ces symboles restent
  définis et utilisés ailleurs. **MD5 des 8 pages identiques aux lots
  323/324** → zéro octet servi modifié, **pas de bump SW** ; smoke
  8×200, 0 erreur console, client-log 0. **Gardien étendu** :
  `test_no_orphan_imports_in_vertex_package`, exclusions minimales et
  documentées (`import *`, `# noqa`, `annotations`, `__init__.py`).
  Suite **2501 / 2 skipped**.

- **Lot 324 — livré** : HYGIÈNE POST-PURGE. Une purge de -33 % laisse
  des résidus : audit AST de `terminal.py` → **11 imports orphelins**
  (10 créés par É1 — leurs consommateurs étaient dans les 82 défs
  retirées — et 1 antérieur, `strategy.config`). Retirés après trois
  vérifications faites AVANT de toucher : aucun effet de bord d'import
  perdu (les 5 modules `vertex/ui/*` concernés sont des bibliothèques
  de rendu pures, sans route ni blueprint), **0 consommateur en
  production** (les tests les importent directement), et les 4 modules
  moteur/service restent importés ailleurs dans `vertex/`. Les
  ré-exports déclarés (`import *`, `# noqa: F401`) sont volontairement
  épargnés — y toucher serait un pari. terminal.py 7 164 → **7 153
  lignes**. **MD5 des 8 pages identiques au lot 323** → zéro octet
  servi modifié, **pas de bump SW** ; smoke 8×200, 0 erreur console,
  client-log 0. **Gardien neuf** : `test_terminal_imports_lot324.py`
  (AST — le monolithe ne réaccumulera plus d'imports morts en
  silence). Suite **2500 / 2 skipped**.

- **Lot 323 — livré** : **PURGE É1 FAITE** — le blocage de permissions
  qui durait depuis le lot 285 est levé (il visait la commande
  composée, pas le retrait). Les **82 définitions mortes** sont
  retirées de `terminal.py` : **10 743 → 7 164 lignes (-3 579,
  -33,3 %)**, **-415 573 octets**, diff **100 % soustractif**.
  Preuves : outil de chiffrage rejoué → **borne basse 0 déf / 0 ligne**
  (É1 close) ; **MD5 des 8 pages servies IDENTIQUES avant/après** —
  zéro octet servi modifié, donc **pas de bump SW** ; smoke navigateur
  8×200, 0 erreur console, client-log 0 ; `compileall` 0 ; import à
  chaud 1 805 → 1 981 ms = **aucun gain mesurable, dit honnêtement**
  (l'import est dominé par pandas/yfinance ; le gain est de
  lisibilité). Effet de bord traité : les 3 copies de la liste de clés
  de sync desk que `terminal.py` portait vivaient dans le JS des pages
  mortes → parties avec ; la sync réelle est intacte (vx_kit /
  journal / vx-entities), règle critique n°1 de CLAUDE.md passée de
  « 4 listes » à « 3 listes servies », **5 gardiens re-ciblés et
  durcis** (dont un qui exige désormais que terminal.py ne ressuscite
  aucune liste). Nouvelle référence de suite : **2499 / 2 skipped**
  (-17 = tests de caractérisation retirés par la moitié 1/2, écrits
  pour ce moment). Reste É2 (25 défs, 1 866 l., boucles d'injection
  par chaîne) et É3 (dépendances croisées) — décisions humaines.

- **Lot 322 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5ced46e, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 321 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 2e5c14b, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 320 — livré** : ÉCHÉANCE PÉRIODIQUE (7e mesure) — SMOKE
  PARFAIT (2e consécutif) : 8×200, 0 erreur, client-log 0, **les 8
  tailles STRICTEMENT identiques aux références 300/310** — la base
  sert des octets stables sur 3 échéances ; suite 2516/2. MINI-BILAN
  310-319 : « régime de croisière » — 1 smoke parfait (310) + 9
  cycles de veille active honnête (311-319), suite 2516/2 constante,
  SW v186 constant, 10 PR fusionnées (#342→#351), 0 changement,
  0 défaut. Prochaine échéance ~lot 330. Docs seulement, pas de
  bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 319 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour d9b23d5, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.
  Prochain lot : ÉCHÉANCE PÉRIODIQUE (7e mesure + bilan 310-319).

- **Lot 318 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 48a44f5, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 317 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b692aac, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 316 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 3eeca4d, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 315 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 05d06a4, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 314 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b7debb0, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 313 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 7441a7b, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 312 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b366fae, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 311 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 286a506, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 310 — livré** : ÉCHÉANCE PÉRIODIQUE (6e mesure) — SMOKE
  PARFAIT : 8×200, 0 erreur console/pageerror, client-log 0, **les 8
  tailles STRICTEMENT identiques aux références du lot 300** (outil
  commité probe_smoke.py, scan terminé avant mesure — piège du froid
  évité, vertex_ready=20) ; suite 2516/2. MINI-BILAN 300-309 :
  « prouver que tout est sain, puis assumer la veille » — robustesse
  outillée (301), fix clavier topbar SW v186 (302), première
  baseline « contenu utile » (304), round-trip desk + CAMPAGNE
  D'AUDITS CLOSE (305), cartographie moteur→UI complète (306),
  veille honnête (307-309). 10 PR fusionnées (#332→#341), 1 défaut
  réel corrigé, 3 outils de validation commités, 0 changement
  gratuit. Prochaine échéance ~lot 320. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 309 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour c38c903, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.
  Prochain lot : ÉCHÉANCE PÉRIODIQUE (smoke + mini-bilan 300-309).

- **Lot 308 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ca944e1, arbre propre, suite 2516/2
  verte) ; aucun signal utilisateur, aucune piste calibrée nouvelle ;
  rapport minimal. Docs seulement, pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions. Prochain jalon :
  échéance périodique au lot 310.

- **Lot 307 — livré** : VEILLE ACTIVE — état vérifié : 0 doublon
  trigger, integration à jour (51e3874), arbre propre, suite 2516/2
  verte sur base fraîche, PR ouvertes = uniquement les 3 brouillons
  intentionnels historiques (#15/#13/#5). Posture assumée : audits
  292-305 clos + cartographie moteur→UI complète → veille honnête
  plutôt que travail fabriqué (œil sur déblocage É1, signaux
  d'usage, échéance périodique ~lot 310). Docs seulement, pas de
  bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 306 — livré** : CARTOGRAPHIE moteur → UI (calibrage strict :
  payloads réels des API en DEMO vs code des pages). 6 pistes
  « donnée servie mais non affichée » vérifiées : adjustments du
  régime AFFICHÉS (Marchés chips + Aujourd'hui), notes[] toujours
  vides en régime connu / déjà éditorialisées en inconnu,
  top_stocks + bloc vertex (p_win, edge) AFFICHÉS (Opportunités),
  vx_* AFFICHÉS, validation (DSR/PBO/dégradation) AFFICHÉE
  (Intelligence), portfolio_score consommé UNIQUEMENT par les pages
  legacy ORPHELINES de terminal.py — un argument de PLUS pour la
  purge É1 (données calculées pour du code mort). **Couverture
  moteur → UI complète — aucune lacune ne justifie un changement.**
  Suite **2516 passed / 2 skipped**. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 305 — livré** : ROUND-TRIP DESK prouvé de bout en bout
  (dernier angle d'audit) — par le chemin RÉEL du store :
  VXEntities.toggleFavorite → localStorage → push débouncé → serveur
  /api/desk data.myFavs=["AAPL"] (6 clés intactes) →
  localStorage.clear + reload → **le pull au boot RESTAURE le
  favori** → nettoyage → serveur []. 0 erreur ; 2 imprécisions de MA
  sonde corrigées en route. Verdict SAIN — le contrat desk
  (last-writer-wins) tient. **CAMPAGNE D'AUDITS CLOSE (292-305)** :
  tactile, honnêteté, a11y, clavier, robustesse API, textes FR,
  performance, écriture locale — tous sains après 8 défauts corrigés
  et 3 sondeurs outillés → retour aux améliorations produit
  calibrées. Suite **2516 passed / 2 skipped**. Docs seulement, pas
  de bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 304 — livré** : PERFORMANCE PERÇUE mesurée (pas supposée) —
  DCL 264-341 ms sur les 8 pages (baseline lot 72 <300 ms tenue,
  /system 311 marginal ; le 630 ms initial de / était un artefact de
  FROID, re-mesuré isolément 341/300/188 ms) ; **PREMIÈRE baseline
  « temps avant contenu utile »** : 362-1055 ms selon la page (méthode
  : texte ≥60 % du final ET 0 squelette, échantillonnage 250 ms) ;
  0 squelette visible à 1 s partout. Verdict SAIN → 0 changement
  produit ; livrable = outil commité tools/probe_perceived_perf.py
  (usage, piège du froid, baselines en en-tête — les prochaines
  mesures ont un point de comparaison). compileall vert. Suite
  **2516 passed / 2 skipped**. Pas de bump. É1 : GO acquis, toujours
  en attente de déblocage permissions.

- **Lot 303 — livré** : DOUBLE AUDIT sain. (1) Clavier PROFOND :
  Entrée sur un bouton ticker de la shortlist → navigation réelle
  vers /analysis/ABNB (vrais boutons, activation native) ; délégués
  d'Aujourd'hui tous tabbables ; pairs de la fiche câblés (le seul
  sous-test ambigu = flake de sonde sur re-rendu, pas un défaut).
  (2) Qualité des textes FR (jamais balayé) : motifs typos sur le
  texte servi de 10 pages — 9 occurrences remontées, TOUTES fausses
  au tri (« réécrites »/« réévaluation » = français correct ;
  frontières d'éléments innerText ; artefact DEMO ticker=nom).
  0 défaut sur les deux angles → 0 changement (gratuit refusé).
  Suite **2516 passed / 2 skipped**. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 302 — livré** : LOT PRODUIT — CLAVIER desktop (jamais
  balayé). Sondeur 25 tabulations sur / : skip-link premier arrêt et
  fonctionnel, focus visible 100 %, ordre logique — MAIS le Tab sur
  le champ de recherche ouvrait la palette DE FORCE (gestionnaire
  focus → blur+openPalette) : les 4 boutons du topbar (Ajouter,
  Connexions, Notifications, Actualiser) étaient INATTEIGNABLES au
  clavier. Corrigé dans vx-shell.js : plus d'ouverture au focus ;
  clic/tap inchangé (chemin tactile lot 288 préservé) + FRAPPE dans
  le champ (caractère/Entrée/↓) → palette ouverte et AMORCÉE avec le
  caractère saisi. Gardien 288 évolué (documenté) + gardien neuf
  test_keyboard_topbar_lot302 (2 tests). Preuves : 24 tabs sans
  ouverture forcée, les 4 boutons ATTEINTS, frappe « a » → palette
  amorcée « a », tap 390 OK (non-régression), 0 erreur, capture
  envoyée. Bump SW v185 → v186 + 5 gardiens. Suite **2516 passed /
  2 skipped (+2)**. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 301 — livré** : ROBUSTESSE (angle neuf) — 7 cas « API coupée
  en vol » (abort réseau + 9 s d'attente) : **SAIN partout**. États
  honnêtes quand la donnée manque (« indisponible », « ERREUR »),
  0 squelette éternel, 0 texte cassé, 0 erreur console inattendue.
  2 faits d'architecture mesurés : /markets n'appelle PAS
  /api/market/summary au chargement ; /opportunities privée de
  /scan reste complète (le radar vit de /api/command) — résilience
  par endpoint réel. Aucun défaut → 0 changement produit ; livrable
  = sondeurs OUTILLÉS et commités (tools/probe_smoke.py protocole
  251 + tools/probe_error_states.py, en-têtes d'usage + références
  — le scratchpad s'efface entre conteneurs). compileall vert.
  Suite **2514 passed / 2 skipped**. Pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions.

- **Lot 300 — livré** : ÉCHÉANCE PÉRIODIQUE (5e mesure) — SMOKE-CHECK
  SAIN + MINI-BILAN 288-299. Smoke : 8×200, 0 erreur, client-log 0,
  healthz ok ; 5 tailles identiques, 3 écarts EXPLIQUÉS (/options
  +5 = lot 296 « board d'options » ; / +1 = calendrier daté DEMO ;
  /system 4124↔4126 = bruit d'horodatage) ; mesuré 2 fois — la 1re
  mesure était partie avant la fin du scan, refaite à conditions
  égales. Bilan de tranche : « le terminal devient utilisable au
  pouce et ne ment plus » — palette tactile complète (288/289/291),
  audit shell sain (292), 18 vues sans cible <32px (293-295), 2
  mensonges corrigés + gardien transversal (296-298), a11y 26 vues
  (299) ; suite 2496→2514 (+18, 9 gardiens neufs), SW v177→v185 (8
  bumps réels), 12 PR (#320→#331), 0 changement gratuit. Prochaine
  échéance ~lot 310. Docs seulement, pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions.

- **Lot 299 — livré** : LOT PRODUIT — A11Y. Balayage des noms
  accessibles sur 26 vues (8 racines + 18 profondes ; dernier
  balayage a11y = lot 73) : 25/26 PARFAITES (0 bouton/lien/champ
  sans nom — l'hygiène des lots 73/209 a tenu). 2 défauts réels sur
  la fiche Analyse : #an-cp-q (question du copilote) et #an-pt-amt
  (montant du ticket pré-trade) n'avaient qu'un placeholder — pas
  une étiquette (disparaît à la saisie, lecture inconstante par les
  lecteurs d'écran) → aria-label FR sur les deux. Gardien neuf
  test_analysis_inputs_a11y_lot299 (2 tests). Preuves : aria-labels
  lus dans le DOM, 0 champ sans étiquette restant, 0 erreur,
  capture envoyée. Bump SW v184 → v185 + 5 gardiens. Suite
  **2514 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 298 — livré** : GARDIEN TRANSVERSAL — plus jamais un
  « live » menteur. La leçon des lots 296/297 (mode de fraîcheur
  codé en dur pour des données qui ont un repli/une variante démo)
  codifiée à l'échelle de l'app : inventaire complet (`,'live')` +
  `mode:'live'` sur terminal.py + vertex/ui/** + static/js/**) → 2
  sites restants dans system_page, jugés HONNÊTES (état interne du
  serveur : registre des jobs, rapport de démarrage — ni repli ni
  variante démo possible). Gardien neuf
  test_freshness_mode_guard_lot298 (2 tests) avec exceptions
  DOCUMENTÉES (system_page + widget_lab, bibliothèque figée =
  spécimens d'exposition). 1er run rouge — le gardien a attrapé
  widget_lab, exception ajoutée avec justification. Suite
  **2512 passed / 2 skipped (+2)**. Tests seuls, pas de bump. É1 :
  GO acquis, toujours en attente de déblocage permissions.

- **Lot 297 — livré** : LOT PRODUIT — HONNÊTETÉ des 18 vues
  profondes. Sondeur du lot 296 étendu (étiquette démo, .vx-update,
  chasse aux revendications « réel » en DEMO) : ~30 occurrences
  triées, presque toutes légitimes. UN défaut de la même classe que
  le 296 : /portfolio?view=risk affichait « risk_engine (positions
  réelles) · Live » en plein DEMO — le mode « live » était codé EN
  DUR (portfolio_page.py L801) alors que les 4 cartes jumelles
  suivent window.__pfLive. Corrigé (live/fallback selon
  /api/pos-quotes) ; « positions réelles » conservé (vocabulaire
  établi : positions déclarées vs candidats du scanner). Gardien
  neuf test_risk_footer_mode_lot297 (2 tests — plus aucun ,'live')
  en dur dans la page). Preuves : « Secours » affiché en DEMO
  (__pfLive:false), 0 erreur, capture envoyée. Bump SW v183 → v184
  + 5 gardiens. Suite **2510 passed / 2 skipped (+2)**. É1 : GO
  acquis, toujours en attente de déblocage permissions.

- **Lot 296 — livré** : LOT PRODUIT — HONNÊTETÉ des données. Audit
  des lignes source/fraîcheur des 8 pages en DEMO : étiquette démo
  visible partout, toutes les lignes .vx-update renseignées, 0
  placeholder — SAUF un mensonge : /options affichait « À l'instant
  · multileg_lab (board réel) » en plein mode DEMO (étiquette codée
  EN DUR dans options-structure.js, alors que d.demo était connu
  juste à côté). Corrigé sur 4 sites : source du payoff + pied de
  Carte-Verdict → ternaires démo/réel ; 2 textes statiques
  d'options_intel_page (servis identiques dans les deux modes) →
  « depuis le board d'options », sans revendiquer « réel ». Gardien
  neuf test_options_board_label_lot296 (2 tests ; 1er run rouge sur
  mon propre décompte — corrigé, re-prouvé). Preuves : « board
  démo » affiché en DEMO, « board réel » absent, 0 erreur, capture
  envoyée. Bump SW v182 → v183 + 5 gardiens. Suite **2508 passed /
  2 skipped (+2)**. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 295 — livré** : LOT PRODUIT — balayage tactile TERMINÉ. Les
  12 vues profondes restantes sondées à 390 (rotation, indices,
  shortlist, positions, performance, journal, hypotheses, lab,
  screener, connections, health, /tracking) : 10/12 SAINES ;
  2 défauts réels : boutons tickers `.vx-link` de la shortlist à
  **21px** (cibles principales de la table, classe sans aucun CSS) →
  min-height:40px ; lien nu `.vx-dim a` (Journal → Hypothèses,
  16px) → même padding que `.vx-meta a` (règle séparée, gardien 293
  intact). Re-balayage : plus AUCUNE cible <32px, 0 erreur,
  0 débordement, 0 texte cassé — **18 vues profondes couvertes au
  total (lots 293/294/295)**. Gardien neuf
  test_ticker_links_touch_lot295 (2 tests). Capture envoyée. Bump
  SW v181 → v182 + 5 gardiens. Suite **2506 passed / 2 skipped
  (+2)**. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 294 — livré** : LOT PRODUIT — vues profondes : contrôles
  segmentés TAPPABLES. Sondeur du lot 293 réutilisé sur 6 vues
  ?view= à 390 (breadth, calendar, risk, track-record, positions,
  settings) : 5/6 SAINES ; défaut réel sur /system?view=settings —
  les 7 contrôles segmentés (densité, navigation latérale,
  animations) mesuraient 26px, `.vx-segmented button` échappant à la
  règle tactile mobile faute de classe vx-btn → min-height:40px en
  ≤640px, aligné sur la règle existante, desktop intact. Gardien
  neuf test_segmented_touch_lot294 (2 tests). Preuves : les 7
  boutons sortis de la liste <32px, 0 erreur, 0 débordement, les 5
  autres vues re-balayées saines, capture envoyée. Bump SW
  v180 → v181 + 5 gardiens. Suite **2504 passed / 2 skipped (+2)**.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 293 — livré** : LOT PRODUIT — fiche Analyse : liens
  d'approfondissement TAPPABLES. Calibrage du parcours profond le
  plus central (/analysis/AAPL, sondeur complet) : sain partout SAUF
  « Calendrier complet → », « Risque complet → », « Journal
  complet → » à **15px de haut** à 390 — quasi intappables au pouce
  (4 sites du motif `.vx-meta > a`). Correctif mobile ≤640px :
  `.vx-meta a{display:inline-block;padding:13px 0}` → cible 41px,
  ligne inline, desktop intact. Gardien neuf
  test_meta_links_touch_lot293 (2 tests). Preuves : les 3 liens
  sortis de la liste <32px, 0 erreur, 0 texte cassé, 0 débordement,
  capture envoyée. Bump SW v179 → v180 + 5 gardiens. Suite
  **2502 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 292 — livré** : AUDIT TACTILE du shell (390, navigateur
  réel) — après la complétion du parcours palette (288/289/291), les
  3 autres parcours tactiles calibrés avec l'intention d'y livrer
  une amélioration : « Plus » (tiroir 3 espaces, liens 357×40,
  navigation réelle /options vérifiée), « Connexions » (contenu
  honnête : IBKR Hors ligne, DÉMO étiquetée), « Notifications »
  (état vide honnête). Fermetures tactiles OK, 0 erreur,
  0 débordement. **Verdict : les 3 sont SAINS — aucun changement
  fait** (un changement gratuit est pire que pas de changement).
  Capture envoyée. Suite 2500/2. Docs seulement, pas de bump. É1 :
  GO acquis, toujours en attente de déblocage permissions.

- **Lot 291 — livré** : LOT PRODUIT — la palette se ferme d'un TAP
  SUR LE FOND. Les lots 288/289 avaient soigné l'entrée tactile ; le
  calibrage de la SORTIE a montré un piège : `.vx-palette` plein
  écran ne se fermait que par Échap (inexistant au tactile) ou en
  choisissant un item — le clic vx-overlay ferme aussi mais cet
  overlay n'est jamais affiché pour la palette. Correctif standard :
  `e.target===palette → close` dans vx-shell.js. Gardien neuf
  test_palette_backdrop_close_lot291 (2 tests). Preuves 390 tactile
  + 1440 : ouverture → tap fond → fermée → réouverture → tap item →
  fermée ; 0 erreur, 0 débordement, capture envoyée. Bump SW
  v178 → v179 + 5 gardiens. Suite **2500 passed / 2 skipped (+2)**.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 290 — livré** : ÉCHÉANCE PÉRIODIQUE — smoke-check complet
  SAIN (4e mesure, protocole lot 251) : 8 pages × HTTP 200, 0 erreur
  console/pageerror, client-log count:0, healthz ok. 7 tailles sur 8
  STRICTEMENT identiques aux mesures 251/270/280 ; /system 3897→4124
  (+227) EXPLIQUÉ : la vue par défaut de /system est `connections`,
  seule vue modifiée depuis (carte « Verrou d'accès », lot 283) —
  écart = fonctionnalité livrée, base saine. Nouvelle référence
  /system = 4124. Suite 2498/2. Prochaine échéance ~lot 300. Docs
  seulement, pas de bump. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 289 — livré** : LOT PRODUIT — cible TACTILE du champ de
  recherche. Suite directe du lot 288 : le champ est LE chemin
  tactile vers la palette, or il mesurait 33px de haut à 390px, sous
  la règle des cibles ≥40px que responsive.css impose déjà aux
  boutons → min-height:40px + icône loupe recentrée (calée en absolu
  pour 33px), bloc ≤640px seulement — topbar 62px inchangé, desktop
  intact. Gardien neuf test_search_touch_target_lot289 (2 tests).
  Preuves : 390 champ 40px + icône centrée (écart 0px) + palette au
  tap (12 items), 1440 inchangé (33px), 0 débordement, 0 erreur,
  capture envoyée. Bump SW v177 → v178 + 5 gardiens. Suite
  **2498 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 288 — livré** : LOT PRODUIT — palette de commandes au
  TACTILE. Le calibrage navigateur a montré que le chemin existe
  déjà (tap sur le champ de recherche → openPalette ; vérifié à
  390px : 12 items, 0 erreur) → aucun bouton ajouté, changement
  gratuit évité. Vrai défaut mesuré : à 390px le champ ne fait que
  93px et la pastille « ⌘K » s'affiche quand même — affordance
  CLAVIER mensongère au tactile (~30px mangés) → masquée en ≤640px
  (responsive.css), desktop intact. Gardien neuf
  test_palette_touch_lot288 (2 tests : tap câblé + ⌘K masqué en
  mobile). Preuves : 390 pastille masquée + palette au tap, 1440
  pastille visible + palette au clic, 0 débordement, 0 erreur,
  capture envoyée. Bump SW v176 → v177 + 5 gardiens. Suite
  **2496 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **MINI-BILAN 281-286 (lot 287, rattrapage)** : tranche « la boucle
  repart en développement ». 281-282 : veille ; 283 : carte Verrou
  d'accès (v174) ; 284 : carte Application (v175) ; 285 : **GO PURGE
  É1 reçu** — tests faits et poussés, retrait terminal.py bloqué par
  le classifieur de permissions (3 approches refusées, utilisateur
  informé) ; 286 : verdict de version (v176). Suite 2486→2494 (+8) ;
  3 cartes réelles = 3 bumps ; 0 défaut produit ; 1 bug de timing
  attrapé avant livraison. É1 : GO ACQUIS, travail PRÊT, blocage
  ENVIRONNEMENTAL — à la reprise : re-générer la table des spans,
  appliquer, prouver, une PR. Docs seulement, pas de bump.

- **Lot 286 — livré** : LOT PRODUIT — la carte Application porte
  désormais un VERDICT DE VERSION : version locale (caches de
  l'appareil) vs **version publiée lue de /sw.js servi à l'instant**
  (fetch no-store — donnée réelle, aucun endpoint nouveau) → badge
  « à jour » / « mise à jour disponible » (n/d honnête si une lecture
  manque). Preuves navigateur : « locale td-shell-v176 · publiée
  td-shell-v176 · à jour », 0 erreur console, 0 débordement, capture
  envoyée. Gardien neuf test_app_version_check_lot286 (2 tests).
  Bump SW v175 → v176 + 5 gardiens. Suite **2494 passed / 2 skipped
  (+2)**.

- **Lot 285 — PURGE É1 : GO reçu, moitié 1/2 faite, moitié 2/2
  BLOQUÉE (permissions)** : le « Go » utilisateur a lancé l'Étape 1.
  Tests adaptés (cat. B : 3 fichiers de caractérisation supprimés +
  épingles retirées ; cat. C : asserts d'alias supprimés retirés, les
  alias vivants gardent les leurs) — commit b8d3842 poussé sur
  `agent/skyler-v2-lot-285`, PAS de PR (une PR = l'étape complète).
  Le retrait des 82 défs / 5 236 lignes dans terminal.py (spans prêts,
  table de l'outil commité) a été refusé 3 fois par le classifieur de
  permissions du mode auto → utilisateur informé (déblocage : règle
  Bash, mode interactif, ou « réessaie »). LE GO RESTE ACQUIS — la
  purge s'exécute en priorité dès déblocage.

- **Lot 284 — livré** : LOT PRODUIT — carte **« Application »** dans
  Système → Réglages. Comble la douleur documentée à chaque rapport
  (« iPhone : vider le cache à la main pour recevoir SW vNNN ») :
  **version du shell RÉELLE** lue des caches du navigateur
  (caches.keys() → td-shell-vN, jamais un numéro codé en dur — le
  gardien interdit tout td-shell-vN en dur dans le JS de page) + état
  du service worker + **bouton « Forcer la mise à jour de l'app »**
  (désinscrit le SW, vide CacheStorage, recharge — NE TOUCHE JAMAIS
  localStorage : les données desk survivent, gardien le fige). Bug de
  timing trouvé au navigateur (première lecture « n/d » pendant que
  le SW installait encore son cache) → cause VÉRIFIÉE avant correctif
  (le cache s'appelait bien td-shell-v175) → re-render sur
  serviceWorker.ready. Preuves : « td-shell-v175 · actif (hors-ligne
  prêt) » affichés, clic RÉEL testé (reload, caches vidés puis SW
  réinstallé), 0 débordement 1440/390, 0 erreur console, capture
  envoyée. Gardien neuf test_app_update_card_lot284 (3 tests).
  **Bump SW v174 → v175** + 5 gardiens. Suite **2492 passed /
  2 skipped (+3)**.

- **Lot 283 — livré** : DIRECTIVE « Continue à développer encore » →
  sortie de veille, LOT PRODUIT. Carte **« Verrou d'accès »** dans
  Système → Connexions — la seule amélioration produit en attente
  (lot 259 : le bouton de verrouillage ne vivait que dans
  PAGE_SETTINGS, page héritée jamais routée). Rendu dynamique selon
  l'état RÉEL du verrou (AUTH_ON, lu à la requête) : actif → badge +
  faits vérifiés (session 30 j, anti-force-brute, temps constant) +
  bouton « 🔓 Se déconnecter & verrouiller cet appareil » → /logout ;
  inactif → état honnête SANS bouton (repli 127.0.0.1, marche à
  suivre VERTEX_CODE/.env). Classes existantes uniquement, 0 littéral
  couleur, HTML entités (pas d'apostrophe nue). Gardien neuf
  test_lock_card_lot283 (3 tests : les 2 états + domicile unique).
  Preuves navigateur (DEMO) : carte visible, badge « inactif »,
  bouton absent comme attendu, 0 débordement 1440/390, 0 erreur
  console, capture envoyée. **Bump SW v173 → v174** + 5 gardiens.
  Suite **2489 passed / 2 skipped (+3)**.

- **Lot 282 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 281 — livré** : VEILLE ACTIVE — état vérifié post-échéance
  (0 doublon trigger, integration à jour, 0 PR oubliée, arbre propre,
  suite 2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 280 — livré** : ÉCHÉANCE PÉRIODIQUE honorée — SMOKE-CHECK
  complet SAIN (protocole lot 251 : 8 pages × HTTP 200, 0 erreur
  console/pageerror, client-log count:0, healthz ok) avec des valeurs
  STRICTEMENT identiques au lot 270 — trois mesures périodiques
  (251, 270, 280), trois résultats identiques : la base intégrée est
  STABLE. + MINI-BILAN 276-280 : 4 cycles de veille (276-279,
  rapports minimaux, 0 travail fabriqué) + cette échéance ; défauts
  produit 0 (48 lots depuis le 232) ; code produit 0 ligne (35 lots,
  246-280) ; suite 2486/2 ; SW v173 ; 5 PR (#309→#313). Prochaine
  échéance périodique ~lot 290. Pas de bump.

- **Lot 279 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Prochain lot (280) :
  échéance périodique (smoke-check complet + mini-bilan 276-280).
  Pas de bump.

- **Lot 278 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Échéance périodique dans
  2 lots. Pas de bump.

- **Lot 277 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 276 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Échéance périodique
  ~lot 280. Pas de bump.

- **MINI-BILAN 271-275 (lot 275)** : tranche « la veille en régime de
  croisière » — première tranche entièrement en veille après
  l'échéance du lot 270. 4 cycles identiques (271-274 : état vérifié
  à chaque fois, rapports minimaux, 0 travail fabriqué) + ce bilan.
  Défauts produit : 0 (43 lots depuis le 232) ; code produit :
  0 ligne (30 lots, 246-275) ; suite 2486/2 vérifiée à chaque cycle ;
  SW v173 ; 5 PR (#304→#308). Prochaine échéance périodique :
  smoke-check complet ~lot 280. ATTENDENT L'HUMAIN (inchangé) :
  « GO purge étape 1 » (dossier exécutable), « Nettoie les branches
  de lots » (277), bouton verrouillage (sur demande), validation
  physique TWS/iPhone, merge main.

- **Lot 274 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Mini-bilan 271-275 au
  prochain lot. Pas de bump.

- **Lot 273 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 272 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 271 — livré** : VEILLE ACTIVE — état vérifié (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher (échéance périodique honorée au lot
  précédent), rapport minimal. Pas de bump.

- **Lot 270 — livré** : SMOKE-CHECK PÉRIODIQUE COMPLET (échéance
  annoncée depuis le lot 263, honorée) + MINI-BILAN 266-270. Protocole
  du lot 251 rejoué : **8 pages racines × HTTP 200, 0 erreur
  console/pageerror, /api/client-log count:0, healthz ok (8
  moteurs)** — résultat IDENTIQUE au lot 251 (±1 caractère
  d'horodatage) → 0 défaut, 0 changement de code. Bilan de tranche :
  cycles de veille 3-6 (266-269, rapports minimaux, 0 travail
  fabriqué) + cette échéance ; défauts produit 0 (38 lots depuis le
  232) ; code produit 0 ligne (25 lots, 246-270) ; suite 2486/2 et SW
  v173 inchangés ; 5 PR (#299→#303). Le régime de veille TIENT :
  cycles courts entre les échéances, échéance honorée avec une vraie
  mesure navigateur. Prochaine échéance périodique ~lot 280. Pas de
  bump.

- **Lot 269 — livré** : VEILLE ACTIVE, cycle 6 — état IDENTIQUE aux
  cycles 1-5 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Prochain lot (270) : smoke-check périodique COMPLET + mini-bilan
  266-270. Pas de bump.

- **Lot 268 — livré** : VEILLE ACTIVE, cycle 5 — état IDENTIQUE aux
  cycles 1-4 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Smoke-check complet dans 2 lots (~270). Pas de bump.

- **Lot 267 — livré** : VEILLE ACTIVE, cycle 4 — état IDENTIQUE aux
  cycles 1-3 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Pas de bump.

- **Lot 266 — livré** : VEILLE ACTIVE, cycle 3 — état IDENTIQUE aux
  cycles 1-2 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Smoke-check périodique prévu ~lot 270. Pas de bump.

- **MINI-BILAN 261-265 (lot 265)** : tranche « la boucle atterrit en
  veille ». 261 : CLAUDE_VERTEX_REBUILD.md neutralisé (dernier risque
  documentaire — un ordre de mission périmé pouvait détourner une
  future session ; les 6 .md racine sont sains) ; 262 : constat
  honnête d'épuisement des pistes → VEILLE ACTIVE + inventaire jamais
  fait (303 branches distantes dont 277 mortes, nettoyage proposé sur
  demande) ; 263-264 : deux cycles de veille prouvés — courts,
  honnêtes, zéro travail fabriqué ; 265 : ce bilan. Défauts produit :
  0 (33 lots depuis le 232) ; code produit : 0 ligne (20 lots,
  246-265) ; suite 2486/2 et SW v173 inchangés ; 5 PR (#294→#298).
  RÉCAP de ce qui attend l'humain : « GO purge étape 1 » (dossier
  complet exécutable avec baseline de gain) ; « Nettoie les branches
  de lots » (277, commande prête) ; bouton de verrouillage visible
  (sur demande) ; validation physique TWS/iPhone (SW v173) ; merge
  main (accord explicite).

- **Lot 264 — livré** : VEILLE ACTIVE, cycle 2 — état IDENTIQUE au
  cycle 1 (0 doublon trigger, integration à jour, 0 PR oubliée, arbre
  propre, suite 2486/2). Aucun code produit changé, aucun signal, rien
  à toucher. Rapport minimal conformément au régime de veille. Pas de
  bump.

- **Lot 263 — livré** : VEILLE ACTIVE, cycle 1. État vérifié : 1 seul
  trigger actif (0 doublon), integration à jour (lot 262 fusionné),
  0 PR oubliée, arbre propre, suite **2486 passed / 2 skipped**.
  Constat honnête : aucun code produit changé depuis v173 → aucune
  re-mesure due (prochain smoke-check périodique raisonnable ~lot
  270), aucun signal d'anomalie — RIEN À TOUCHER ce cycle (le toucher
  aurait été du travail fabriqué). Docs seulement, pas de bump.

- **Lot 262 — livré** : CONSTAT D'ÉTAT — les pistes autonomes sont
  ÉPUISÉES (produit mesuré correct depuis le lot 232, invariants tous
  audités, 6 .md racine sains, baseline perf posée, dossier de purge
  complet et exécutable) → la boucle passe en **VEILLE ACTIVE** :
  entretien espacé, constats courts, toute directive exécutée
  immédiatement. Mesure du lot (jamais faite) : **303 branches
  distantes**, dont 266 `agent/skyler-v2-lot-*` fusionnées squash +
  11 rc-periodique = **277 branches mortes sûres à supprimer** (leur
  contenu vit dans integration et les PR #1→#294) — nettoyage
  PROPOSÉ, PAS exécuté (action de masse sur l'infra partagée →
  déclenchable sur demande : « Nettoie les branches de lots »).
  Vérifications légères : 1 seul trigger actif (0 doublon),
  integration à jour, aucune PR ouverte oubliée. Docs seulement, pas
  de bump. Suite **2486 passed / 2 skipped**.

- **Lot 261 — livré** : CLAUDE_VERTEX_REBUILD.md NEUTRALISÉ. Le
  dernier .md racine non audité n'était pas une doc d'accueil mais un
  ORDRE DE MISSION pour Claude datant de l'ère Total Rebuild, resté
  actif à la racine : « travaille sur agent/vertex-total-rebuild » +
  livrables d'époque — en CONTRADICTION directe avec la gouvernance
  CLAUDE.md (skill vertex-skyler-v2, branche integration, anciennes
  branches = références historiques). Risque réel : une future session
  pouvait suivre l'ancien ordre. Calibrage avant de trancher : fichiers
  pointés existants, branche encore sur origin, document référencé par
  les audits d'époque → PAS de suppression — bannière d'obsolescence
  en tête qui neutralise l'ordre et redirige vers la gouvernance
  actuelle. **Les 6 .md racine sont désormais tous audités et sains.**
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 256-260 (lot 260)** : tranche « mesurer le neuf,
  aligner les portes d'entrée ». 256 : baseline perf serveur jamais
  chiffrée (import 11,68 s à froid / ~2 s à chaud ; TTFB 8 pages
  1,3-1,9 ms — le coût du mort est à l'IMPORT, métrique avant/après
  purge) ; 257-259 : audit systématique des docs d'ACCUEIL contre le
  code — **10 défauts corrigés (4 README + 3 DEMARRER_ICI + 3
  SECURITE), dont 2 touchant la sécurité** (« écoute 0.0.0.0 »
  prétendue ; bouton de déconnexion fantôme dans une page orpheline) ;
  .env.example audité EXACT. Défauts produit : 0 (28 lots depuis le
  232) ; 0 ligne de code produit touchée (15 lots, 246-260) ; suite
  2486/2 et SW v173 inchangés ; 5 PR (#289→#293) ; 1 redémarrage
  worker (256) repris sans perte. LEÇON : les docs d'accueil dérivent
  silencieusement jusqu'à contredire la sécurité réelle — l'audit
  « affirmation par affirmation, tracée vers la ligne de code » les a
  remis au vrai. ATTEND L'HUMAIN : « GO purge étape 1 » (dossier
  complet avec baseline de gain) ; bouton de verrouillage visible sur
  demande ; validation physique TWS/iPhone ; merge main sur accord.

- **Lot 259 — livré** : SECURITE.md ↔ RÉALITÉ (dernier .md racine
  d'accueil non audité). VRAI et vérifié dans la source : cookie 30 j
  httponly/SameSite=Lax (terminal.py L133-134), comparaison à temps
  constant (auth.py L127 hmac.compare_digest), anti-force-brute
  5 essais → verrou progressif min(300, 15×(n-4)) s (auth.py L133).
  **3 corrections** : le « bouton Se déconnecter & verrouiller dans
  Paramètres » est un BOUTON FANTÔME — il ne vit que dans
  PAGE_SETTINGS (terminal.py L7477), page héritée orpheline (0 routée,
  preuve lot 248) → doc corrigée vers la route /logout qui, elle,
  fonctionne ; « désactiver le verrou → l'app redevient ouverte »
  omettait le repli 127.0.0.1 sans code (lot 218) → précisé ; liste
  des pages publiques complétée sur la vraie PUBLIC_PATHS (auth.py
  L28-30 : + /logout, /api/healthz, webhook TradingView signé).
  CONSTAT à l'humain : le bouton de verrouillage n'a jamais été
  recâblé dans la nouvelle UI — /logout couvre le besoin ; bouton
  visible dans Système = petit lot produit SUR DEMANDE. Docs
  seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 258 — livré** : DEMARRER_ICI.md ↔ RÉALITÉ (suite de l'audit
  des portes d'entrée). **3 défauts corrigés** : nom de dossier périmé
  `IBKT-DASHBORD-` (×2) → `Vertex-` ; table des espaces PRÉ-REFONTE
  (Overview/Matinal/Comité/Recherche/Décisions/Santé/Fiche titre) →
  les 8 espaces canoniques réels ; « badge 🟢 LIVE IBKR en haut à
  droite » inexistant → l'état de source réel « Live/Différé/Hors
  ligne » du panneau d'état (vx-shell.js L205-209, vérifié AVANT de
  trancher). **`.env.example` audité ligne par ligne : EXACT, non
  touché** (sémantique VERTEX_CODE conforme au comportement gardé lot
  218 ; READONLY énoncé ; sections à jour). Lanceurs DEMO vérifiés
  existants — section conservée. Les 3 portes d'entrée du dépôt
  (README lot 257, DEMARRER_ICI, .env.example) sont désormais alignées
  sur la réalité. Docs seulement, pas de bump. Suite **2486 passed /
  2 skipped**.

- **Lot 257 — livré** : README ↔ RÉALITÉ — la vitrine du dépôt n'avait
  jamais été auditée contre les faits mesurés. **4 défauts corrigés,
  dont 1 de SÉCURITÉ** : le README affirmait « le serveur écoute déjà
  sur tout le réseau local (0.0.0.0) » alors que la réalité durcie et
  GARDÉE (test_network_binding_lot218) est l'écoute 127.0.0.1 par
  défaut, LAN seulement via VERTEX_CODE (verrou) ou VERTEX_LAN=1 →
  section réécrite avec la vraie procédure ; liste de pages
  pré-refonte (/titre, /entreprises, /watchlist) → les 8 espaces
  canoniques + note de redirection ; « 57 leaders US » → univers réel
  S&P 500 ∪ Nasdaq 100 ∪ Dow (~500 titres, healthz 517) ; structure
  périmée → routes/pages/moteurs actuels. Calibrage AVANT correction :
  ib_reader.py vérifié réel et branché (sa ligne était correcte —
  conservée), fichiers pointés tous existants, 0 test n'épingle le
  README. Docs seulement, pas de bump. Suite **2486 passed / 2
  skipped**.

- **Lot 256 — livré** : BASELINE de performance SERVEUR avant-purge
  (jamais chiffrée formellement — le lot 72 mesurait le client).
  Import de terminal.py : **11,68 s à froid, ~2 s à chaud** (3
  passes) ; TTFB des 8 pages racines : **1,3-1,9 ms** (3 mesures
  chacune, HTML 22-86 ko) ; healthz 3 ms. Lecture honnête : le
  SERVICE est instantané (pages = chaînes préconstruites — rien à
  corriger) ; le coût du code mort est à l'IMPORT, payé à chaque
  démarrage pour construire notamment des pages héritées jamais
  servies — c'est LA métrique que la purge devrait améliorer, à
  re-mesurer avec le même protocole après É1/É2. Reprise après
  redémarrage du worker en début de lot (état vérifié : lot 255
  fusionné, 0 trigger actif — rien perdu). 0 changement de code,
  docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 251-255 (lot 255)** : tranche « consolider sans
  fabriquer ». 251 : smoke-check santé post-merges SAIN (8 pages ×
  200, 0 erreur console, client-log 0) ; 252 : outil de chiffrage
  rendu rejouable de partout (1 défaut d'OUTILLAGE prouvé puis corrigé,
  chiffres identiques au lot 249) ; 253 : annexe É1 — liste exacte des
  82 défs triée A/B/C, le « GO » devient exécutable sans
  reconstruction ; 254 : audit invariant « fichiers runtime jamais
  commités » TENU (0 traqué, 0 incohérence, .gitignore 100 % des
  sites d'écriture) ; 255 : ce bilan. **10 lots consécutifs (246-255)
  sans toucher au code produit** — chaque lot une mesure ou un outil,
  jamais du remplissage. Suite 2486/2 et SW v173 inchangés ; 5 PR
  (#284→#288) ; défauts produit : 0 (23 lots consécutifs). État : la
  purge est PRÊTE (preuves + fourchette 31,4-48,7 % + outil robuste +
  liste triée) et bloquée PAR CONCEPTION sur « GO purge étape 1 » ;
  les pistes autonomes restantes sont de l'entretien périodique que la
  boucle ESPACE plutôt que d'en fabriquer.

- **Lot 254 — livré** : AUDIT de l'invariant « fichiers runtime jamais
  commités » (règle Git de CLAUDE.md — le seul invariant jamais audité
  formellement). 3 volets mesurés : `git ls-files` × motifs interdits
  → **0 fichier runtime traqué** (unique match : un fichier de TEST au
  nom similaire) ; `ls-files -ci` → **0 incohérence** traqué/ignoré ;
  croisement .gitignore ↔ sites d'écriture RÉELS de l'app →
  **couverture 100 %** (skyler_memory/sessions/decisions.json +
  alerts_fired.json listés nommément ; les 3 caches couverts par
  `*_cache.json` ; les jokers du rituel de nettoyage = ceinture-
  bretelles, aucun fichier réel ne correspond aux variantes).
  INVARIANT TENU → 0 correctif. Docs seulement, pas de bump. Suite
  **2486 passed / 2 skipped**.

- **Lot 253 — livré** : ANNEXE É1 — la liste EXACTE des retraits de
  l'Étape 1, générée et triée (`ANNEXE-E1-RETRAITS.md`, **0 purge**).
  Mode `--e1` ajouté à l'outil officiel : 82 défs du périmètre borne
  basse (spans de lignes, tailles) + fichiers de tests impactés,
  régénérable à volonté. Triage en 3 catégories d'action : A retrait
  sec ; B retrait avec les tests de caractérisation (lot183/184/185 +
  épingles — écrits POUR ce moment) ; **C re-cibler le test PUIS
  retirer l'alias** — découverte du lot : `_rsi`/`_atr`/`_adx`/
  `_demo_one`/`_vehicle_of`/`_swing_project` sont des alias de
  compatibilité vers des moteurs VIVANTS (vertex/engines/indicators,
  vertex/data/demo, strategy_fit, swing) — les tests fonctionnels qui
  les importent gardent leur valeur, seul l'import change. 2 faux
  positifs de grep (`home` : fonction locale d'un test + mot de
  commentaire) vérifiés dans la source et marqués à ignorer. Dossier
  de décision mis à jour (ligne É1 → annexe). Aucun code produit
  touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 252 — livré** : ROBUSTESSE de l'outil de décision
  `tools/purge_e2_sizing.py` (l'instrument officiel du chiffrage,
  rejoué à É1/É2). Défaut PROUVÉ avant de toucher : lancé depuis
  `docs/` → FileNotFoundError (open/grep/import relatifs au cwd).
  Correctif minimal : racine du dépôt ancrée sur `__file__` +
  `os.chdir`. Preuve : rejoué depuis docs/ ET depuis la racine —
  chiffres identiques entre eux et IDENTIQUES au lot 249 (5 236 l. /
  48,7 % ; 107 défs) → la mesure est STABLE et reproductible. Aucun
  code produit touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 251 — livré** : SMOKE-CHECK santé post-tranche en conditions
  réelles. Après les 5 merges docs-only (246-250), re-mesure en vrai
  navigateur (serveur DEMO, Playwright 1440×900, écoute console +
  pageerror) : **8 pages racines × HTTP 200, 0 erreur console,
  /api/client-log count:0, healthz ok** (8 moteurs, scan démo 20/517).
  Verdict SAIN → 0 changement de code. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 246-250 (lot 250)** : tranche « du prouver au préparer
  la décision ». 246 : 4e parcours métier (journalisation d'une
  décision d'un trait, écriture réelle prouvée) ; 247 : grande synthèse
  de la campagne 214-246 (produit MESURÉ correct) ; 248 : dossier de
  décision de purge (21 fonctions héritées / 0 routée / 21 orphelines) ;
  249 : chiffrage outillé É2 (fourchette 31,4-48,7 % de terminal.py
  mort, outil commité, 2 pièges gravés) ; 250 : ce bilan. **0 ligne de
  code produit touchée sur les 5 lots** — le produit est prouvé et la
  règle « jamais de changement gratuit » a tenu. Suite 2486/2 et SW
  v173 inchangés ; 5 PR (#279→#283) ; 3 faux positifs d'outils
  attrapés avant conclusion. État honnête : les pistes autonomes
  s'amincissent ; le seul gros chantier restant (purge chiffrée) est
  bloqué PAR CONCEPTION sur « GO purge étape 1 » — la boucle continue
  en entretien utile sans fabriquer du travail.

- **Lot 249 — livré** : CHIFFRAGE OUTILLÉ de l'Étape 2 de la purge —
  **AUCUNE purge**, l'estimation « 25-30 % » du dossier devient une
  FOURCHETTE MESURÉE. Outil commité (`docs/refactor/validation/tools/
  purge_e2_sizing.py`, mark-and-sweep AST : racines = 14 fonctions
  routées mesurées en runtime + 18 décorées + 26 module-level +
  externes ; 2 passes). Résultat sur terminal.py (10 743 l.) : borne
  BASSE certaine **3 370 lignes mortes (31,4 %) / 408 ko (33,4 %)**
  (82 défs) ; borne HAUTE **5 236 lignes (48,7 %) / 692 ko (56,6 %)**
  (107 défs) si les boucles d'injection partent avec. DEUX PIÈGES
  mesurés et gravés au dossier (§ 1d) : 12 constantes PAGE_*
  référencées par CHAÎNE via `globals()[_pg]` (l. ~6537-6588 — retrait
  sans adaptation = KeyError à l'import) ; dépendance croisée NOUVELLE
  `PAGE_ENTREPRISES` → `_OPP_BRIEF_JS` → injecté dans `PAGE_DAILY`
  (l. ~6088-6097) → Étape 3, pas avant. Doctrine tenue : 1er passage à
  49,2 % avec 4 faux positifs (fonctions décorées after_request/
  errorhandler) — vérifiés dans la source, script corrigé AVANT
  publication du chiffre. Décision inchangée : « GO purge étape 1 »
  attendue. Docs + outil seulement, pas de bump. Suite
  **2486 passed / 2 skipped**.

- **Lot 248 — livré** : DOSSIER DE DÉCISION DE PURGE de terminal.py
  (TERMINAL-PURGE-DECISION.md) — **0 code touché**, tout est preuve
  et plan. PREUVE DÉCISIVE mesurée ce lot : croisement runtime
  app.url_map × fonctions retournant PAGE_* → **21 fonctions de rendu
  héritées trouvées, 0 routée, 21 ORPHELINES** — aucun utilisateur ne
  peut les atteindre (cohérent avec les 43 « route migrée » et le
  constat du lot 246). Les 32 constantes PAGE_* ne sont référencées
  hors terminal.py QUE par les tests de caractérisation écrits POUR
  ce moment (lot 183 + épingles). Une exception cartographiée :
  PAGE_DAILY ↔ home_art.py/vault.py (hérités eux-mêmes) → étape
  dédiée. PLAN en 3 étapes sûres — É1 fonctions orphelines + PAGE_*
  + tests de caractérisation sans objet ; É2 blocs BODY/CSS/JS
  révélés non référencés (chiffrage outillé) ; É3 dépendances
  croisées — une PR par étape, rollback = revert, pytest 100 % +
  navigateur 8 pages à chaque étape. **DÉCISION DEMANDÉE À L'HUMAIN :
  « GO purge étape 1 » — rien ne sera purgé sans.** Docs seulement,
  pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 247 — livré** : GRANDE SYNTHÈSE DE LA CAMPAGNE DE PREUVE
  (lots 214 → 246, 33 lots, PR #247 → #279). Après la clôture de la
  tournée graphique TV (204), la boucle a basculé de « construire » à
  « PROUVER ». Chiffres : suite 2472 → **2486** (+14), SW v171 →
  **v173** (2 bumps, chacun porté par un correctif réel), **6
  gardiens neufs**, **3 correctifs produit** (tous
  mesurés-minimaux-vérifiés), ~30 protocoles navigateur. PROUVÉ :
  les 8 invariants CLAUDE.md (8/8 tenus, 3 lacunes de garde
  comblées) ; le rendu honnête (0 NaN affiché) ; la navigation
  (31 liens, 177 boutons) ; le responsive COMPLET (3 débordements
  réels corrigés, 0 faux correctif) ; le shell interactif entier ;
  l'infrastructure (SW réel — doctrine bump=déploiement prouvée,
  desk sync round-trip client) ; les 4 PARCOURS métier (analyse,
  contrat, GEX, journal-écriture). **0 défaut produit depuis le lot
  232 : le produit est MESURÉ correct, du pixel au blob de sync.**
  RESTE EN ATTENTE HUMAINE : (1) purge de terminal.py (~25-30 % mort
  cartographié, dont la page Journal héritée) — accord explicite
  requis ; (2) validation physique TWS réel + iPhone (vider le cache
  pour SW v173) ; (3) merge vers main — accord explicite requis.
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 246 — livré** : PARCOURS JOURNAL D'UN TRAIT — le dernier flux
  d'ÉCRITURE du produit prouvé de bout en bout. /journal?view=journal
  → bouton « Ajouter une entrée » → formulaire de décision →
  NVDA + Enregistrer → **1 entrée dans vxJournal local** → NVDA
  présent dans le blob /api/desk (push VXEntities) → rechargement :
  l'entrée **persiste et s'affiche** → nettoyage PAR LE PROTOCOLE
  (retirée du store, poussée, absente du serveur — desk_data.json
  jamais édité à la main). 0 erreur console. Calibrage honnête : deux
  fausses pistes écartées — le jTicker/jSave de vertex/ui/journal.py
  appartient à la page Journal HÉRITÉE (PAGE_JOURNAL de terminal.py,
  plus servie par /journal — candidate connue à la purge en attente
  d'accord) ; le VRAI produit passe par performance_page
  (j-ticker/j-confirm, store VXEntities) — c'est lui qui est prouvé.
  Les QUATRE parcours sont prouvés : les 3 lectures (analyse 241,
  contrat 242, GEX 243) ET l'écriture (journal 246). Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 245 — livré** : MINI-BILAN 241-245. Tranche de 5 lots
  (PR #274 → #278) : suite **2486 / 2 skipped stable**, SW **v173
  STABLE** (0 bump — 5 lots de preuve pure). Réalisations : les
  3 PARCOURS MÉTIER prouvés d'un trait — (1) plan d'analyse actions :
  clic ACN → /analysis/ACN, plan complet, 8 canvas LWC + 32 SVG
  (241) ; (2) contrat options : radar 50 → détail payoff/R:R/théta/IV
  avec « estimation modèle, pas une promesse », note de méthode
  canvas∉innerText gravée (242) ; (3) positionnement GEX : radar
  18/18 avec « n/d » honnête → détail cohérent (243) ; (4) vues
  Système internes 4/4 → couverture des vues EXHAUSTIVE (244). FAIT
  MARQUANT : **le produit ENTIER est mesuré correct** — après le
  shell (236-240), ce sont les chemins de VALEUR qui sont prouvés ;
  3 tranches de preuve sans un seul défaut produit depuis le lot
  232 : le socle est sain et DÉMONTRÉ tel. Doctrine : 5 lots, 0 ligne
  de code produit, 0 bump, chaque faux positif d'outil corrigé avant
  conclusion. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 244 — livré** : VUES SYSTÈME INTERNES — les deux dernières
  vues jamais balayées du produit (/system?view=connections et
  /system?view=archive), au protocole discriminant, à 390 px ET
  1440 px, en contexte navigation. RÉSULTAT : **4/4 propres** —
  0 overflowX, 0 dépassement droit, 0 marqueur malhonnête (texte DOM
  et SVG balayés), 0 erreur console. La couverture des VUES est
  désormais EXHAUSTIVE : 8 pages racines (390+768) + 6 secondaires +
  15 vues internes — auxquelles s'ajoutent états vides (219),
  liens/boutons (221), composants et flux du shell (229-236), SW
  (237), sync (239) et les 3 parcours métier (241-243). Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 243 — livré** : PARCOURS GEX D'UN TRAIT — le 3e parcours
  métier prouvé de bout en bout. /options?view=positioning → radar
  de positionnement rendu (**18/18 titres exploitables** : SPOT,
  NET GEX en M$, régime stabilisant/accélérateur, biais, bascule Ø-Γ
  avec **« n/d » honnête** quand inconnue — jamais un chiffre
  inventé —, murs call/put, max pain) → saisie ACN dans #vx-gx-sym →
  détail GEX rendu : murs call/put, gamma, flip, spot, 10 barres,
  chips de valeurs — cohérent avec la ligne ACN du radar
  (bascule 192,92 · mur call 198,2 · mur put 189,4). 0 marqueur
  malhonnête (texte DOM ET texte SVG balayés — leçon du lot 242),
  client-log 0, 0 erreur console. Capture envoyée. Les TROIS parcours
  métier sont prouvés d'un trait : plan d'analyse actions (241),
  contrat options (242), positionnement GEX (243). Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 242 — livré** : PARCOURS CONTRAT OPTIONS D'UN TRAIT — le 2e
  cœur métier prouvé de bout en bout. /opportunities?view=options →
  radar rendu (**50 contrats**) → clic sur un contrat → détail
  COMPLET : payoff canvas hachuré zones PERTE/GAIN avec **chip
  BE 136.98** et ligne spot (« Breakeven 136.98 · prime 3812 ») ;
  matrice R:R simulé 7 scénarios × J+0→J+28 avec la mention
  d'honnêteté « MODEL_ESTIMATE — estimation modèle, pas une
  promesse » ; décomposition temps hachurée + chip Min ; sensibilité
  IV avec dominante en chip. 0 vocabulaire d'ordre, client-log 0,
  0 erreur console. NOTE DE MÉTHODE honnête : le premier passage
  textuel déclarait « payoff absent » — FAUX POSITIF de l'outil (les
  libellés d'un canvas ne vivent pas dans innerText) ; la
  vérification VISUELLE a corrigé le classement avant toute
  conclusion (réflexe du lot 238 : jamais déclarer un défaut sur une
  heuristique). Capture envoyée. Les DEUX cœurs métier (analyse
  actions 241, contrat options 242) sont prouvés. Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 241 — livré** : PARCOURS D'ANALYSE COMPLET — le cœur métier
  de Vertex (voir un titre → ouvrir son analyse → lire le plan)
  prouvé d'UN SEUL trait en navigateur, alors que les pages n'avaient
  été validées qu'isolément. Parcours réel : clic sur le menu
  d'entité ACN depuis / → « Ouvrir l'analyse » → navigation vers
  /analysis/ACN → **plan complet rendu** : verdict, niveaux
  (entrée/stop/objectif), conviction, comité, scénario/cône —
  **8 canvas LWC** (le vendor chargé par cette seule page) +
  **32 graphiques SVG** hydratés, 0 marqueur malhonnête, 32 états
  honnêtes —/n/d, /api/client-log count 0, 0 erreur console. Capture
  du plan envoyée. Le chemin de valeur quotidien — délégué de clic →
  navigation → vendor → hydratation → plan lisible — est prouvé de
  bout en bout. Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 240 — livré** : MINI-BILAN 236-240. Tranche de 5 lots
  (PR #269 → #273) : suite **2486 / 2 skipped stable**, SW **v173
  STABLE** (0 bump — 5 lots de preuve pure, rien à déployer).
  Réalisations : (1) modal d'ajout 3 étapes prouvé, écriture réelle
  au store + READONLY affirmé dans l'UI même — « Vertex n'envoie
  JAMAIS un ordre » (236) ; (2) service worker v173 prouvé en vrai —
  actif, seul cache présent (nettoyage prouvé), 32/32 statiques
  servies du cache en 2e visite : la doctrine bump=déploiement est
  prouvée (237) ; (3) docs : 0 référence morte sur 94 fichiers, les
  17 signalements d'heuristique tous résolus individuellement (238) ;
  (4) desk sync round-trip côté client réel — push au ts exact, pull
  au boot qui restaure tout après localStorage.clear (239). FAIT
  MARQUANT : **la preuve du shell est TOTALE** — composants (229/231/
  234), flux (236), infrastructure (237/239), navigation et
  responsive (219-233) : chaque mécanisme de l'expérience quotidienne
  déroulé en conditions réelles, 0 défaut trouvé sur la tranche — le
  produit tient. Doctrine : 5 lots, 0 ligne de code produit, 0 bump,
  et chaque lot a produit du SAVOIR vérifié. Docs seulement, pas de
  bump. Suite **2486 passed / 2 skipped**.

- **Lot 239 — livré** : DESK SYNC ROUND-TRIP CÔTÉ CLIENT RÉEL —
  l'invariant n° 1 (17 clés / 4 listes) et la préférence utilisateur
  centrale (« tout synchronisé automatiquement au lancement ») sont
  gardés côté serveur depuis longtemps, mais le CHEMIN CLIENT n'avait
  jamais été prouvé en navigateur. Protocole (avec sauvegarde
  préalable de desk_data.json et nettoyage PAR LE PROTOCOLE — règle
  n° 6, jamais d'édition à la main) : (1) écriture locale
  toggleFavorite('TSLA') ; (2) push débouncé 1200 ms → **ts serveur =
  ts client à la milliseconde près** et TSLA dans myFavs du blob ;
  (3) localStorage.clear() + rechargement (« appareil neuf ») → le
  pull au boot **restaure TSLA, deskTs et 5 clés desk** ;
  (4) nettoyage : favori retiré → push → TSLA retiré du serveur.
  La chaîne écriture → débounce → POST /api/desk → persistance →
  pull → réhydratation fonctionne exactement comme conçue. 0 erreur
  console. Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 238 — livré** : LIENS .md DANS docs/ HORS VALIDATION — la
  piste proposée cinq fois, enfin prise. 94 fichiers .md balayés
  (validation/ exclu — déjà gardé au lot 228) : 1 lien markdown
  formel → valide ; 162 mentions backticks → 17 signalées par
  l'heuristique de chemin, puis CHAQUE signalement vérifié par
  recherche du nom dans tout le dépôt : 14 fichiers EXISTANTS
  ailleurs (docs/refactor/, docs/release/,
  .claude/skills/vertex-skyler-v2/references/, .claude/FRAMEWORK.md)
  et 3 gabarits/raccourcis de prose (placeholder SKYLER-LOT-XX,
  plage « 08A.md à 08E.md »). **0 référence réellement morte** — pas
  un seul « mort » déclaré sur la foi d'une heuristique de chemin.
  Gardien non pertinent ici (les mentions par nom seul sont un usage
  légitime ; la zone à risque est gardée depuis le 228). Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 237 — livré** : SERVICE WORKER v173 VÉRIFIÉ EN NAVIGATEUR
  RÉEL — le SW est bumpé et gardé depuis 173 versions mais son
  comportement n'avait JAMAIS été vérifié en vrai (littéraux de
  source seulement). Protocole : 1re visite / (enregistrement,
  activation, caches), 2e visite /markets (nouvelle page, même
  contexte). RÉSULTAT : SW enregistré + ACTIF (scope /) ;
  **td-shell-v173 est le SEUL cache présent** — le nettoyage des
  caches périmés à l'activation est prouvé ; precache 5 entrées
  (coquille : manifest, icône, fonts) ; 2e visite : page CONTRÔLÉE
  par le SW et **32/32 ressources statiques servies du cache**
  (transferSize=0) — le cache runtime fait exactement le travail
  conçu (hasShellJs=false au precache n'est PAS un défaut : les JS
  entrent au cache à la 1re requête). La doctrine « bump =
  déploiement » qui gouverne la boucle depuis 173 versions est
  désormais PROUVÉE, pas supposée. 0 erreur console. Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 236 — livré** : MODAL D'AJOUT D'ENTITÉ — le dernier flux
  interactif du shell jamais testé en navigateur, avec la vérif
  READONLY la plus sensible (c'est le SEUL endroit du produit où
  l'utilisateur saisit une « position »). Parcours réel : bouton + →
  modal « Ajouter » (barre d'étapes 1/0/0) → NVDA + Continuer → 6
  destinations (1/1/0) → Watchlist → formulaire priorité/zone/thèse/
  catalyseur (1/1/1) → Confirmer → modal fermé et **NVDA réellement
  écrit dans la watchlist du store** (VXEntities.watchlist() le
  contient). READONLY : texte des 3 étapes balayé, y compris le
  formulaire Position → **0 vocabulaire d'ordre** ET la mention
  « Registre déclaratif — Vertex n'envoie JAMAIS un ordre » est
  affirmée DANS l'interface, au seul endroit où la confusion serait
  possible. 0 erreur console. TOUS les flux interactifs du shell sont
  prouvés (drawer/modal 229, palette 231, menu 234, ajout 236).
  Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 235 — livré** : MINI-BILAN 231-235. Tranche de 5 lots
  (PR #264 → #268) : suite **2486 / 2 skipped stable**, SW v172 →
  **v173** (1 seul bump, porté par le seul correctif réel de la
  tranche). Réalisations : (1) palette de commande prouvée
  comportementalement — Ctrl+K, filtre, flèches, Entrée navigue,
  câblage VXEntities vivant (231) ; (2) vues internes 390 balayées,
  1 débordement réel soldé — .vx-update REPLIE, ellipse refusée sur
  une info d'honnêteté (232) ; (3) couverture responsive COMPLÈTE :
  8 racines (390+768) + 6 secondaires + 13 vues — campagne totale
  3 défauts réels corrigés, 2 bumps justifiés, 0 faux correctif
  (233) ; (4) menu contextuel prouvé + READONLY vérifié — 0 action
  d'ordre dans les libellés (234). FAIT MARQUANT : TOUS les
  composants interactifs du shell sont prouvés en conditions réelles
  (drawer/modal 229, palette 231, menu 234) — le shell n'est plus
  supposé correct, il est MESURÉ correct. Doctrine : 4 lots de
  constat sans code produit, 1 correctif mesuré-minimal-vérifié.
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 234 — livré** : MENU CONTEXTUEL D'ENTITÉ — le dernier
  composant interactif jamais testé en navigateur, avec vérif
  READONLY explicite. Calibrage instructif : les déclencheurs
  [data-entity-menu] vivent dans le DOM hydraté de / (3) et /markets
  (20) — pas sur /opportunities en démo. Parcours réel sur / (bouton
  ACN) : menu ouvert (11 actions, focus DANS le menu, entièrement
  dans le viewport) ; flèches ↓↓ suivies (data-active + focus sur
  l'item actif) ; clic-dehors ferme. **READONLY vérifié : 0 action
  d'ordre** — balayage des libellés contre {acheter, vendre, ordre,
  buy, sell, transmettre, passer} → vide ; « Ajouter une position »
  est un ENREGISTREMENT au journal personnel (localStorage/desk
  sync), pas un ordre — l'invariant tient jusque dans le vocabulaire.
  0 erreur console. TOUS les composants interactifs du shell sont
  désormais prouvés en conditions réelles (drawer/modal 229, palette
  231, menu 234). Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 233 — livré** : DERNIÈRES VUES À 390px — la couverture
  responsive navigateur est COMPLÈTE. Les 3 vues jamais balayées
  (/journal?view=journal, /journal?view=track-record,
  /intelligence?view=committee) au protocole discriminant, en
  contexte navigation : **3/3 propres** (0 overflowX, 0 dépassement
  droit, 0 marqueur malhonnête, 0 erreur console). CAMPAGNE SOLDÉE :
  8 pages racines (390 au lot 222 + 768 au lot 224) + 6 pages
  secondaires (223) + 13 vues internes (232 + 233) — tout le produit
  navigable balayé. Bilan de la campagne : **3 défauts réels trouvés
  et corrigés** (crumb /tracking 433px, bouton retour /portfolio
  403px intermittent, ligne de fraîcheur knowledge graph 591px),
  2 bumps SW justifiés (v172, v173), 0 faux correctif. Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 232 — livré** : VUES INTERNES À 390px — le protocole
  discriminant du 222 appliqué aux 10 vues à onglets JAMAIS balayées
  (opportunités options/anomalies/calendrier, options volatilité/
  positionnement, marchés secteurs/volatilité/breadth, portefeuille
  watchlist/risque), en contexte navigation. RÉSULTAT : 9/10 propres,
  **1 débordement RÉEL** trouvé — /portfolio?view=risk : la ligne de
  fraîcheur/source .vx-update du knowledge graph (nowrap, 562px)
  finissait à 591px, 201px coupés hors écran. Correctif MINIMAL scopé
  ≤768px : .vx-update REPLIE (white-space:normal + overflow-wrap) —
  l'ellipse REFUSÉE délibérément : c'est une info d'HONNÊTETÉ (la
  traçabilité de la source doit rester entièrement lisible). Vérifié :
  ligne repliée à 361px ≤ 390, les 10 vues rejouées → 0 défaut,
  0 erreur console. Captures avant/après envoyées. Bump SW
  **v172 → v173** + 5 gardiens (composant de toutes les cartes — le
  correctif doit se déployer). Suite **2486 passed / 2 skipped**.

- **Lot 231 — livré** : PALETTE DE COMMANDE — le constat
  comportemental complet d'un composant JAMAIS testé en navigateur
  (seuls des littéraux de source étaient gardés). Parcours réel en
  démo : **Ctrl+K** ouvre (input focusé, 11 items en 3 groupes
  Positions/Pages/Actions — la position réelle ACN du store y figure :
  le câblage VXEntities est vivant, pas décoratif) ; filtre « march »
  → 4 items ; **flèches** ↓↓↑ suivies par aria-selected (idx 0→2→1) ;
  **Échap** ferme ; le clic sur la barre de recherche ouvre aussi
  (blur→openPalette) ; « archive » + **Entrée** → navigation RÉELLE
  vers /system?view=archive, palette fermée. 0 erreur console.
  Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 230 — livré** : MINI-BILAN 226-230. Tranche de 5 lots
  (PR #259 → #263) : suite 2482 → **2486** / 2 skipped (+4), SW
  **v172 STABLE** (0 bump — 5 lots de constat/garde, rien à
  déployer). Réalisations : (1) budgets JS mesurés — chart-core.js
  57,2/64 kB (89 %, marge 6,8 kB, +18 kB coût légitime de la tournée
  TV), calibration du gardien recalibrée + consigne « discuter le
  budget AVANT de le crever » (226) ; (2) dette TODO : 0 marqueur
  dans tout le code produit + perf serveur : 16 routes, médianes
  1,2-2,9 ms (227) ; (3) mémoire de la boucle GARDÉE : 218 références
  d'index → 0 morte, périmètre 01-09 enfin écrit, gardien
  index↔rapports — le rituel est un invariant testé (228) ; (4) cycle
  drawer/modal au clavier prouvé comportementalement — focus revenu
  au déclencheur, closeAll referme les deux (229). Doctrine : tranche
  100 % « mesurer avant de toucher » — 0 ligne de code produit
  modifiée, 1 gardien neuf, 2 recalibrations de vérité, chaque
  constat chiffré. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 229 — livré** : CYCLE DRAWER/MODAL AU CLAVIER — le constat
  COMPORTEMENTAL qui manquait aux lots 209/210 (eux prouvaient les
  attributs, celui-ci déroule le vrai parcours). Protocole Playwright
  sur `/` : clic RÉEL sur Notifications → drawer ouvert (attributs
  levés, overlay, focus DANS le panneau) → Échap → fermé, attributs
  reposés, **focus revenu au déclencheur** (vx-notifs-btn) ; modal
  via le chemin produit VX.shell.openModal → même cycle impeccable ;
  les DEUX ouverts + UN SEUL Échap → les deux reposent
  aria-hidden/inert (focus → body : closeAll ne peut pas choisir un
  déclencheur — limitation connue, pas un défaut). Observation
  classée : le modal s'ouvre SANS l'overlay partagé — VOULU (son
  conteneur est plein écran fixed inset:0 ; l'overlay sert au
  drawer). 0 erreur console. Le retour de focus lastFocus posé au 209
  est prouvé en conditions réelles. Constat honnête, aucun code
  touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 228 — livré** : INTÉGRITÉ SKYLER-INDEX ↔ RAPPORTS — la
  mémoire de la boucle vérifiée puis GARDÉE. Mesure : 218 références
  citées dans l'index → **0 morte** (tous les rapports existent) ;
  231 rapports sur disque → 13 sans ligne d'index = les lots 01-09
  (batch correctness pré-Institutional+), hors champ PAR CONSTRUCTION
  (l'index commence au lot 10, STATUS retrace le début) — mais ce
  périmètre n'était écrit nulle part. Livré : (1) périmètre documenté
  dans l'en-tête de l'index ; (2) gardien
  test_skyler_index_integrity_lot228 (4 tests — références mortes
  cassent la suite, rapports orphelins cassent la suite (exemption
  01-09 bornée par regex), périmètre documenté, anti-vide ≥ 200
  références réellement vérifiées). Le rituel « rapport + ligne
  d'index à chaque lot » n'est plus une habitude : c'est un invariant
  TESTÉ. Docs/tests seulement, pas de bump. (Lot repris proprement
  après un redémarrage du worker en début d'exécution.)
  Suite **2486 passed / 2 skipped** (2482 + 4).

- **Lot 227 — livré** : DETTE TODO + PERF SERVEUR — double constat
  mesuré, 0 défaut. (1) Balayage TODO/FIXME/XXX/HACK (mot entier) sur
  TOUT le code produit (terminal.py + vertex/** py/js/css, vendor
  exclu) : **0 occurrence** — aucune dette auto-documentée éparpillée ;
  la dette CONNUE vit où elle doit (rapports de purge, en attente
  d'accord humain). (2) Chronométrage réel (urllib, 5 passes/route,
  DEMO chaud) des 8 routes HTML + 8 API critiques : **16/16 en 200,
  médianes 1,2 à 2,9 ms, pire cas 8 ms** (premier hit de /) — la
  génération serveur (HTML en chaînes Python) est négligeable devant
  le budget DCL < 300 ms du lot 72 ; le coût du chargement est côté
  navigateur, déjà budgété et gardé (72 + dérive mesurée au 226).
  Constat honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 226 — livré** : BUDGETS JS/CSS STATIQUES — la piste proposée
  trois fois, enfin prise. Mesure de vertex/static/** contre les
  gardiens du lot 72 (64 kB/fichier première partie, vendor isolé).
  VERDICT : gardien VERT, aucune violation — mais dérive réelle
  documentée : **chart-core.js 39 → 57,2 kB** (+18 kB, coût LÉGITIME
  de la tournée TV 189-213 : jauge, hachures, chips, extrêmes, radar
  dominant, levelLines) soit **89 % du budget**, marge restante
  6,8 kB ; options-intel 39,1 kB (61 %) ; neon-glass.css 47 kB
  (73 %) ; vendor 160 kB toujours chargé par /analysis seule (gardien
  d'isolement vert). CONTRE-VÉRITÉ corrigée : le commentaire de
  calibration du gardien affirmait encore « chart-core 39 kB » —
  recalibré aux valeurs mesurées, avec consigne explicite : au
  prochain palier, discuter le budget AVANT de le crever (pas de
  hausse en douce — c'est la dérive que le gardien ferme).
  Tests/docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 225 — livré** : MINI-BILAN 221-225. Tranche de 5 lots
  (PR #254 → #258) : suite **2482 / 2 skipped stable**, SW v171 →
  **v172** (1 seul bump, porté par le SEUL correctif réel de la
  tranche). Le balayage NAVIGATEUR systématique du produit est
  SOLDÉ — l'audit a porté là où pytest ne voit rien (DOM hydraté,
  contexte de navigation) et la méthode a payé : (1) liens/boutons —
  31 liens internes × HTTP 200, 177 boutons tous câblés (221) ;
  (2) 2 débordements RÉELS du topbar mobile trouvés et soldés — crumb
  /tracking 433px + bouton retour /portfolio 403px INTERMITTENT
  (reproduit en navigation) → ellipse scopée ≤768px, bump v172
  (222) ; (3) pages secondaires 390 en navigation : 6 pages 0 défaut
  (223) ; (4) tablette 768 au point de rupture exact du media query :
  8 pages 0 défaut (224). Couverture navigateur cumulée depuis 219 :
  états vides ✔, liens ✔, boutons ✔, 390 principal + secondaires ✔,
  768 ✔. Doctrine tenue : 4 lots sans code produit dits honnêtement ;
  le seul correctif mesuré, minimal, vérifié dans le contexte
  défaillant rejoué. Docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 224 — livré** : RESPONSIVE 768px (TABLETTE) — chasse aux
  cousins des défauts topbar du lot 222, au point de rupture EXACT du
  media query du correctif (max-width:768px — là où un défaut de bord
  serait le plus probable), protocole discriminant en contexte
  navigation sur les 8 espaces. RÉSULTAT : **0 défaut partout** —
  overflowX 0, 0 dépassement droit d'élément visible, 0 erreur
  console. Le correctif 222 s'applique bien à 768 inclus (fil
  d'Ariane et bouton retour tronquent aussi en tablette) et aucune
  autre famille de défauts n'apparaît à ce viewport. Constat honnête,
  aucun code touché, pas de bump. (Lot exécuté sur ordre « continue »,
  trigger réarmé.) Suite **2482 passed / 2 skipped**.

- **Lot 223 — livré** : PAGES SECONDAIRES À 390px — le protocole
  discriminant du lot 222 étendu aux pages JAMAIS balayées en
  responsive, et en CONTEXTE DE NAVIGATION (2 pages visitées avant →
  bouton retour visible — précisément le contexte qui piégeait
  /portfolio au 222). Balayage : /titre/AAPL, /company/AAPL,
  /analysis/ACN, /intelligence, /login, /design-system. RÉSULTAT :
  **0 défaut sur les 6 pages** — overflowX 0, 0 dépassement droit
  d'élément visible, 0 marqueur malhonnête (NaN/undefined/Infinity),
  0 erreur console. Le correctif du 222 (fil d'Ariane + bouton retour
  en ellipse, shell partagé) couvre bien ces pages. Constat honnête,
  aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 222 — livré** : RESPONSIVE 390px — 2 DÉBORDEMENTS RÉELS du
  topbar trouvés et SOLDÉS (le spot-check navigateur a enfin payé).
  Mesure : overflowX document = 0 partout (les gardes tiennent), MAIS
  en discriminant off-canvas voulu / dépassement droit réel :
  (1) /tracking — le crumb « Approfondissement du Portefeuille »
  (nowrap 213px) finissait à 433px, texte passant SOUS les boutons ;
  (2) /portfolio en NAVIGATION — le libellé du bouton retour (nowrap
  155px) poussait le cluster droit à 403px (refresh coupé de 13px) ;
  intermittent car le bouton retour n'apparaît qu'en navigation —
  reproduit en visitant 3 pages avant. Correctif MINIMAL scopé ≤768px
  (responsive.css) : .vx-breadcrumb flex:1/overflow hidden + enfants
  min-width:0/ellipsis ; .vx-back-btn span idem — fil et libellé
  TRONQUENT au lieu de passer dessous. Vérifié : contexte défaillant
  rejoué → cluster à 378px ≤ 390 ✔ ; balayage 8 pages → 0 dépassement,
  0 erreur console ; captures avant/après envoyées. Bump SW
  **v171 → v172** + 5 gardiens (CSS du shell — le correctif doit se
  déployer). Suite **2482 passed / 2 skipped**.

- **Lot 221 — livré** : LIENS INTERNES + BOUTONS — balayage
  NAVIGATEUR des 8 pages en démo (DOM hydraté — les gardiens
  existants ne voient que la source servie). Protocole : serveur DEMO
  (healthz ok/demo), Playwright 1440×900, extraction des a[href]
  internes dédupliqués + GET réel sur chaque cible, et inventaire des
  button avec détection de câblage (onclick, data-* des délégués
  globaux, submit, aria-controls). RÉSULTAT : **31 liens internes
  uniques → 31 × HTTP 200 (0 lien mort)** ; **177 boutons
  (18+55+39+12+10+20+13+10) → 0 sans câblage détectable**. Cohérent
  avec l'architecture des délégués clavier/clic posés aux lots
  précédents. Constat honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 220 — livré** : MINI-BILAN 216-220. Tranche de 5 lots
  (PR #249 → #253) : suite 2472 → **2482** / 2 skipped (+10 : 3+4+3),
  SW **v171 STABLE** — 5 lots sans bump (doctrine des constats : rien
  à déployer, dit honnêtement). Réalisations : (1) AUDIT D'INVARIANTS
  CLAUDE.md TERMINÉ — 8 invariants vérifiés par constat mesuré, 0
  violation ; (2) 3 gardiens NEUFS sur lacunes réelles (invariants
  documentés mais épinglés par aucun test) : RequestTimeout=45
  anti-blocage IBKR (216), scan_state jamais réassigné — scan AST des
  3 formes interdites (217), écoute réseau 127.0.0.1 sans code (218) ;
  (3) audit navigateur des états vides honnêtes (219, piste jamais
  réalisée) : 8 pages, 0 marqueur malhonnête, 0 erreur console ;
  (4) doctrine tenue — aucun code produit modifié sur toute la
  tranche, calibrage avant de toucher. Docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 219 — livré** : ÉTATS VIDES HONNÊTES EN DÉMO — l'audit
  NAVIGATEUR jamais réalisé (le DOM après hydratation JS est hors de
  portée du test_client — c'est là que NaN/undefined apparaîtraient).
  Protocole : serveur DEMO (healthz data_source:demo), Playwright
  1440×900 (domcontentloaded + 4500 ms) sur les 8 espaces ; par page :
  recherche des marqueurs malhonnêtes affichés (NaN, undefined, null,
  Infinity), comptage des états honnêtes (—/n/d), étiquette démo,
  erreurs console. RÉSULTAT : **0 marqueur malhonnête sur les 8
  pages**, états honnêtes présents partout (1 à 21 par page),
  étiquette démo confirmée serveur sur les 8, **0 erreur console**,
  /api/client-log count:0 après balayage complet. Invariant n° 4
  (« jamais de chiffre inventé affiché comme réel ») TENU — constat
  honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 218 — livré** : FIN DE L'AUDIT D'INVARIANTS CLAUDE.md (lots
  214/216/217/218). (1) Filet desk_data.json : TENU et déjà gardé par
  test_desk_backup_lot178 (8 tests — snapshot quotidien créé AVANT le
  premier écrasement du jour, jamais réécrit ensuite, rotation 7 j,
  validation stricte du restore) — rien à ajouter. (2) Écoute réseau
  (« sans code d'accès, le serveur n'écoute que 127.0.0.1 ») : règle
  TENUE dans _start_app (lan_ok = AUTH_ON ou VERTEX_LAN=1 ou $PORT →
  0.0.0.0 ; sinon 127.0.0.1) MAIS gardée par AUCUN test (grep lan_ok/
  0.0.0.0/VERTEX_LAN dans tests/ → 0) — on pouvait exposer le desk à
  tout le Wi-Fi sans casser la suite. Livré :
  test_network_binding_lot218 (3 tests — source épinglée, table de
  vérité sur la même expression avec VERTEX_LAN=0 ≠ opt-in, message
  config honnête). BILAN DE L'AUDIT : 8 invariants vérifiés par
  constat, 3 lacunes de garde réelles comblées (RequestTimeout=45,
  scan_state, écoute réseau), 0 violation. Tests seulement, pas de
  bump. Suite **2482 passed / 2 skipped** (2479 + 3).

- **Lot 217 — livré** : INVARIANT scan_state « muté en place — ne
  JAMAIS réassigner » (state.py / CLAUDE.md) — constat mesuré + gardien
  AST. Scan du code produit (terminal.py + vertex/**, trois formes
  interdites : réassignation module-level hors state.py, affectation
  d'attribut .scan_state, global scan_state) → **0 offenseur** ; les 5
  `scan_state = scan_state or {}` des moteurs sont des rebinds LOCAUX
  de paramètres (ils ne touchent pas l'objet partagé — légitimes).
  Lacune : AUCUN des ~30 fichiers de tests utilisant scan_state ne
  vérifiait CET invariant, alors que le casser est silencieux et grave
  (boucle de fond et routes garderaient des objets différents — pages
  figées sans erreur). Livré : test_scan_state_invariant_lot217
  (4 tests — scan AST, domicile unique documenté, gardien-du-gardien
  sur exemple synthétique qui prouve que le scanner détecte bien les 3
  formes, et non-faux-positif sur le rebind local). Tests seulement,
  pas de bump. Suite **2479 passed / 2 skipped** (2475 + 4).

- **Lot 216 — livré** : INVARIANTS n° 2 + IBKR (suite de l'audit du
  lot 214) — constat mesuré + UN gardien neuf sur lacune réelle.
  (1) Règle n° 2 (JS généré valide / apostrophes) : TENUE et déjà
  gardée en entier par test_js_syntax_sweep_lot182 (chaque bloc
  <script> inline de 16 routes au vrai parseur node --check + chaînes
  JS des modules + garde-fou de volume ≥12 blocs) — rien à ajouter.
  (2) IBKR : readonly=True TENU, codé en dur (READONLY = True +
  connect readonly=True) et gardé par 3 tests (test_no_orders balayage
  dépôt, strategy_os_final_guards, data_sources). MAIS lacune RÉELLE
  mesurée : grep RequestTimeout tests/ → 0 occurrence — l'invariant
  CLAUDE.md « RequestTimeout=45 (ne pas retirer — anti-blocage) »
  n'était épinglé par AUCUN test. Livré :
  test_ibkr_timeout_lot216 (3 tests) — valeur 45, les DEUX bornes
  appliquées dans la façade readonly (ib.RequestTimeout + timeout du
  connect), et scheduler DEFAULT_TIMEOUT_S aligné sur le gateway (si
  l'un bouge sans l'autre, le test casse). Tests seulement, pas de
  bump. Suite **2475 passed / 2 skipped** (2472 + 3).

- **Lot 215 — livré** : MINI-BILAN 211-215 + vérif cohérence SW.
  Tranche de 5 lots (PR #244 → #248) : suite 2466 → **2472** / 2
  skipped (+6), SW v168 → **v171** (bumps 211/212/213 ; 214/215 =
  constats sans bump). Réalisations : (1) chasse aux hex nus COMPLÈTE
  — 5 littéraux soldés sur 4 sites (movers Système, étiquettes RRG,
  bordure démo Opportunités, texte des tuiles treemap) ; (2) 2
  gardiens pérennes BORNÉS verrouillent la chaîne entière (pages
  Python lot 212 + builders JS lot 213) — plus aucun endroit où un
  hex nu peut se glisser sans casser la suite ; (3) invariants
  CLAUDE.md vérifiés par constat mesuré (desk sync 17 clés/4 listes,
  sanitize_news 6 sorties SANITIZED + faux positif écarté) ;
  (4) doctrine tenue — 2 lots de constat sans code produit, dits
  honnêtement. Entretien du lot : cohérence SW vérifiée —
  td-shell-v171 identique dans system.py L211 ET les 5 gardiens,
  aucune dérive de version. Docs seulement, pas de bump.
  Suite **2472 passed / 2 skipped**.

- **Lot 214 — livré** : AUDIT D'INVARIANTS CLAUDE.md par CONSTAT
  MESURÉ (pas sur parole). (1) Desk sync (règle n° 1) : gardien
  test_desk_sync_keys_single_source_of_truth relancé → 1 passed ;
  comptage direct : __DESK_KEYS (terminal.py) = 17 clés, DESK_KEYS
  (vx_kit.py) = 17 identiques, et journal.py porte les 17 inline dans
  le JS jvSyncPush — exactement ce que le gardien vérifie. TENU.
  (2) sanitize_news (règle n° 5) : cartographie exhaustive — les 6
  points de sortie de contenu news (content.py, api_skyler, api_events,
  skyler_sweep.py, terminal.py ×2) passent TOUS par sanitize_news ; le
  signalement system_status_ep écarté comme FAUX POSITIF après lecture
  du corps réel (le champ 'news' y est un seuil de fraîcheur interne —
  thresholds 3600 s, et build_system_status ne sert que age_s + enum
  _freshness : aucun texte externe ne transite). Gardien XSS lot 177
  relancé → 6 passed. TENU. Docs seulement, pas de bump (doctrine des
  lots de constat). Suite **2472 passed / 2 skipped**.

- **Lot 213 — livré** : GARDIEN HEX NU ÉTENDU AUX BUILDERS JS
  (charts/*.js + pages/*.js — test_no_bare_hex_static_js_lot213,
  3 tests), calibré AVANT d'écrire : 49 occurrences → 40 =
  DÉFINITIONS de palette (le bloc C.colors de chart-core + le thème
  obsidian-copper entier — la source des tokens doit bien porter les
  hex quelque part ; exemptions BORNÉES par leurs marqueurs exacts et
  testées : si les bornes bougent, le test casse au lieu de scanner à
  côté), 8 = lookups col(VC,'n','#hex') légitimes, et 1 littéral
  RÉELLEMENT nu soldé : le texte des tuiles du treemap
  (fill="#f3f1ed" → var(--vx-text-primary,#F8F5F3), SVG var() natif,
  repli d'inventaire sûr). Avec le lot 212, la chaîne COMPLÈTE est
  couverte (pages Python + builders JS) — plus aucun endroit où un
  hex nu peut se glisser sans casser la suite. Bump SW v170 → v171 +
  5 gardiens (le texte des tuiles change subtilement — déploiement).
  Capture treemap envoyée, 0 erreur console.
  Suite **2472 passed** / 2 skipped (2469 + 3).

- **Lot 212 — livré** : GARDIEN « AUCUN HEX NU DANS LES PAGES » —
  le balayage des lots 211-212 pérennisé en pytest
  (test_no_bare_hex_pages_lot212, 3 tests) : tout hex quoté dans
  vertex/ui/pages/*.py est REFUSÉ hors formes de repli légitimes
  (var(--…,#hex), cc/col/cssv('…','#hex'), lookup||'#hex'), avec
  exemption DOCUMENTÉE et testée de widget_lab.py (bibliothèque
  design FIGÉE, palette de mise en scène délibérée). CORRECTION
  HONNÊTE au passage : le « balayage complet » du lot 211 était
  incomplet — la calibration a trouvé 2 littéraux nus de plus,
  soldés : étiquettes RRG de Marchés ('#bab4ac' →
  VXCharts.colors.muted||'#8A8284', repli dans l'inventaire sûr) et
  bordure démo d'Opportunités ('#FFC857' → VXCharts.colors.warning).
  Calibré contre l'état réel avant commit : 10 occurrences → 2
  réelles (soldées) + 8 widget_lab (exemptées) → gardien vert à 0.
  Bump SW v169 → v170 + 5 gardiens (deux pages visibles changent
  subtilement — déploiement). Captures RRG + Opportunités envoyées,
  0 erreur console. Suite **2469 passed** / 2 skipped (2466 + 3).

- **Lot 211 — livré** : ENTRETIEN — deux choses. (1) Le constat
  « movers absents en démo » du lot 199 ré-examiné et CLOS : pas un
  trou silencieux — l'hôte n'est créé que si movers.length, et
  l'absence de cotations est déjà couverte par l'état honnête de la
  table (« Aucune cotation web pour l'instant… »). (2) Dette RÉELLE
  trouvée dans le même bloc et soldée : les barres movers coloraient
  en HEX NUS ('#36c889'/'#ed655c') — le DERNIER littéral couleur nu
  des pages (balayage complet : toutes les autres occurrences sont
  des lookups de tokens avec fallback, motif légitime) → remplacés
  par VXCharts.colors.positive/negative (VXCharts garanti présent
  par la garde de la branche). Bump SW v168 → v169 + 5 gardiens : le
  rendu peut changer subtilement (hex figé → vraie valeur du token)
  et le correctif doit atteindre les clients en cache. Note honnête :
  pas de capture possible (movers exigent des cotations web,
  absentes en démo) — preuve par code + balayage.
  Suite 2466 passed / 2 skipped.

- **Lot 210 — livré** : PREUVE NAVIGATEUR du cycle a11y du MODAL et
  du chemin closeAll (complément du 209 qui n'avait prouvé que le
  drawer) : modal fermé {aria-hidden:true, inert} → ouvert {retirés}
  → refermé {reposés} ; closeAll (Échap/overlay) avec modal + drawer
  ouverts ensemble → les DEUX reposent leurs attributs (délégation à
  panelClose par construction) ; 0 erreur console. AUCUN code à
  changer — ce lot prouve au lieu de supposer. Docs seulement, pas
  de bump. + MINI-BILAN 206-210 (ci-dessous).
  Suite 2466 passed / 2 skipped (inchangée).

### MINI-BILAN tranche 206-210

5 lots, PR #239 → #243, suite 2461 → 2466 (+5 gardiens a11y),
SW v167 → v168 (un seul bump — le vecteur de déploiement du correctif
a11y, pas un bump cosmétique). Tranche d'APRÈS-TOURNÉE, entièrement
dans la doctrine « mesurer avant de toucher » : tour responsive
complet MESURÉ (lots 206-207 — 9 espaces × 5 viewports = 45/45
cellules sans débordement ni erreur console, 0 correctif nécessaire),
cohérence de la grammaire TV vérifiée par INVENTAIRE mesuré (208 —
divergences toutes justifiées, 0 retouche gratuite), accessibilité
des panneaux hors-canvas CORRIGÉE et gardée (209 — aria-hidden +
inert + 5 gardiens ; 210 — cycle prouvé modal + closeAll). Trois lots
sur cinq n'ont pas touché une ligne de code produit : le produit
était déjà droit, et la boucle l'a prouvé au lieu de le décorer.
EN ATTENTE de directive : purge terminal.py (~25-30 % mort,
cartographié, accord humain requis) ; sinon entretien continu.

- **Lot 209 — livré** : ACCESSIBILITÉ des panneaux hors-canvas
  (l'observation du lot 206 corrigée) : le drawer d'entité et le
  modal FERMÉS portent désormais aria-hidden="true" + inert dans le
  markup servi par le shell, et vx-shell.js les bascule proprement
  (panelOpen retire les deux attributs, panelClose les repose — même
  chemin pour les deux panneaux, retour de focus préservé). Sidebar
  mobile laissée hors périmètre en connaissance de cause : visible
  sur desktop, repli piloté par media query CSS — un aria-hidden JS
  risquerait une régression desktop pour un gain nul (rapporté).
  Cycle PROUVÉ en navigateur : fermé {aria-hidden:true, inert} →
  ouvert {retirés} → refermé {reposés}, 0 erreur console. Gardien
  test_a11y_drawer_lot209.py (5 tests : HTML servi, source JS,
  identité dialogue, focus). Bump SW v167 → v168 + 5 gardiens —
  JUSTIFIÉ : le HTML du shell change, sans bump les clients en cache
  ne recevraient jamais le correctif (le bump est le vecteur de
  déploiement). Suite **2466 passed** / 2 skipped (2461 + 5).

- **Lot 208 — livré** : INVENTAIRE MESURÉ DE COHÉRENCE (option 2 de
  la proposition lot 205) : script d'analyse des builders charts +
  pages sur 4 axes — (1) police des chips : tvEdgeChip fontSize 9
  PARTOUT, chips canvas 700 9px uniformes, libellés de zones 8.5 sur
  viewBox denses ; (2) hachures : alphas IDENTIQUES SVG/canvas
  (.08/.38), tuiles 6 vs 8 et traits 1.6 vs 1.4 = équivalence
  visuelle voulue entre userSpace SVG et pixels canvas ; (3) rayons
  ≈ h/2 partout (coins pleinement arrondis cohérents) ; (4) pieds de
  cartes : 3 classes à 3 RÔLES distincts (vx-chart-foot = pied
  graphique avec fraîcheur, vx-meta = note, vx-muted = secondaire) —
  une sémantique, pas une divergence. Seul point suspect vérifié :
  fontSize 11 de candlestick-lwc = config d'AXES de Lightweight
  Charts (faux positif de grep). VERDICT : toutes les divergences
  sont JUSTIFIÉES → AUCUNE retouche (harmoniser serait un changement
  gratuit — risque sans gain). Option 2 SOLDÉE par constat. AUCUN
  code touché, AUCUN bump SW. Suite 2461 passed / 2 skipped.

- **Lot 207 — livré** : TOUR RESPONSIVE 2/2 (mesuré, même protocole
  que le 206) : /portfolio, /options, /journal, /system,
  /intelligence × 5 viewports — 0 px de débordement de page sur les
  25 cellules, 0 erreur console, seuls les panneaux hors-canvas
  voulus signalés (mécanisme translateX déjà vérifié).
  ★ VERDICT GLOBAL DU TOUR (lots 206-207) : 9 espaces × 5 viewports
  = **45/45 cellules propres** — aucune page de Vertex ne défile
  horizontalement entre 390 et 1920 px, aucune erreur console, tous
  les habits TV de la tournée tiennent à toutes les tailles.
  L'option 1 de la proposition du lot 205 est SOLDÉE en 2 lots sans
  un seul correctif nécessaire — la discipline responsive des
  refontes précédentes a tenu. AUCUN code touché, AUCUN bump SW.
  Captures de contrôle Portefeuille 1920 + Intelligence 390
  envoyées. Suite 2461 passed / 2 skipped.

- **Lot 206 — livré** : TOUR RESPONSIVE post-tournée 1/2 (mesuré,
  option par défaut de la proposition du lot 205) : 4 espaces
  (Aujourd'hui, Marchés, Opportunités, Analyse) × 5 viewports
  (390/768/1024/1440/1920), mesure Playwright de (a) débordement
  horizontal de page, (b) éléments hors viewport (hors défilement
  voulu et fixed), (c) erreurs console. VERDICT : 0 défaut réel —
  débordement de page 0 px sur les 20 cellules, 0 erreur console ;
  tous les éléments signalés sont des panneaux hors-canvas VOULUS
  (sidebar mobile repliée à gauche à 390, drawer d'entité fermé par
  translateX à 768+ — vérifiés au style calculé). Les habits TV de
  la tournée (chips, hachures, dégradés, dominantes) passent
  proprement du mobile au 1920. Observation rapportée sans agir :
  le drawer fermé n'a pas d'aria-hidden (piste accessibilité, pas un
  défaut de layout). AUCUN code touché, AUCUN bump SW. Captures de
  contrôle 1920 + 390 envoyées. Suite 2461 passed / 2 skipped.

- **Lot 205 — livré** : BILANS — mini-bilan 201-205 + BILAN DE
  CLÔTURE de la tournée graphique TV (ci-dessous) + proposition de
  suite chiffrée (décision humaine). Aucun code produit touché —
  vérification visuelle des dernières captures sans défaut évident,
  donc pas de changement gratuit ni de bump SW. Suite 2461 passed /
  2 skipped (inchangée).

### MINI-BILAN tournée 201-205

5 lots, PR #234 → #238, suite stable 2461 passed / 2 skipped,
SW v164 → v167 (stable depuis le 204 — deux lots de constats sans
changement visible, la règle de bump respectée dans les deux sens).
Réalisations : radar à sommet dominant (201), price-chart — canonique
LWC constaté TV natif + repli levelLines en chips au bord droit
(202), cône de mouvement σ hachuré + murs GEX en dominantes à chips
(203), dernier balayage en 3 constats honnêtes et INVENTAIRE 100 %
TRAITÉ (204), bilans et passation (205).

### ★ BILAN DE CLÔTURE — TOURNÉE GRAPHIQUE TV (lots 189 → 204)

Directive utilisateur (lot 188) : « que tout Vertex ressemble à ça —
fluide, beau, parfait » (langage visuel TradingView). Livré en
16 lots (189-204), PR #222 → #237, SW v153 → v167, suite verte
2461/2 à CHAQUE lot, 0 erreur console à chaque capture.

**Grammaire commune créée (chart-core & co)** :
- jauge TV : arc ENTIER en dégradé continu + pointeur blanc court
  (189) — héritée par 6+ jauges (santé, VIX, breadth, comité, risque,
  environnement options) ;
- `tvHatch` (SVG) + `hatchPattern` (canvas) : la texture « estimation,
  pas un réel » (189/197) — cône de projection, payoff, théta, cône σ ;
- `tvEdgeChip` + chips canvas : étiquettes pleine couleur à texte
  sombre (189) — bords du cône, treemap, niveaux du plan, extrêmes,
  barres dominantes, murs GEX, rails, radar, runway ;
- `tvExtremesPlugin` : chips Max/Min sur les extrêmes RÉELS (195) —
  équité, drawdown, série de référence ;
- `.vx-rail-chip` : chip de valeur sur pointeur de rail (198).

**Règles transverses appliquées partout** :
- DOMINANTE EN ÉVIDENCE (jamais sur singleton) : consensus, heatmap,
  staleness, barres, radar, GEX, stress tests (préexistant) ;
- ESTIMATION HACHURÉE : toute projection assume sa texture ;
- CHIPS DE VALEURS RÉELLES : les chiffres clés se lisent sur le
  graphique, pas à côté.

**Héritages gratuits constatés** (un builder aligné = ses pages
alignées) : scénarios Options (via heatmap), discipline Journal +
sensibilité IV + leadership + movers (via C.bars), jauges (via
C.gauge), équité/drawdown/série de référence (via C.area).

**Honnêteté tenue de bout en bout** : constats démo rapportés sans
agir (prime aberrante, tuiles sans P&L, movers/journal vides, env
options absent), « n/d » sur régime indéterminé, pas de sparkline
sans série, pas de dominante inventée. Un correctif structurel au
passage : __VXVOCAB injecté par le shell (191).

### Proposition de suite (décision humaine — rien n'est lancé)

1. **Tour responsive complet post-tournée** : 8 espaces × 5 viewports
   (390→1920), vérification visuelle des nouveaux chips/hachures aux
   petites tailles, corrections des débordements trouvés
   (~2-3 lots). ← choix par défaut de la boucle si rien n'est dit.
2. **Polish transverse de cohérence** : uniformiser les pieds de
   cartes, les tailles de chips et les densités de hachures entre
   pages (~2 lots).
3. **PURGE de terminal.py** : ~25-30 % du monolithe mort cartographié
   et figé par tests (lots 183-185) — EN ATTENTE D'ACCORD HUMAIN
   EXPLICITE, jamais lancée sans.
4. **Attente de directive** : la boucle continue sur des lots
   d'entretien (gardiens, honnêteté, petites dettes).

- **Lot 204 — livré** : TOURNÉE TV — DERNIER BALAYAGE de
  l'inventaire (lot de CONSTATS, aucun code produit modifié) :
  (1) « double probabilité » = la colonne P(doubler) du scanner
  d'options, une estimation DÉJÀ étiquetée « EST. » avec sa
  définition en pied — la doctrine de la tournée y était ; (2) barres
  S+/S/A/B et stress tests Portefeuille DÉJÀ conformes — vérifié
  navigateur : le pire scénario (TOP_SECTOR_MINUS_15, −15 %) porte
  la dominante (libellé rouge gras + halo) depuis le lot 131, la
  concentration sa mini-barre à repère (lot 138) ; (3) sparklines
  des tuiles KPI d'Aujourd'hui : AUCUN payload ne fournit de série
  par KPI → pas de sparkline inventée, constat honnête (reporté à
  une évolution moteur, jamais à une invention UI).
  → **TV-CHARTS-INVENTORY.md : 100 % des lignes traitées** (refaites,
  héritées ou constatées conformes/honnêtes). Décision fidèle aux
  règles : AUCUN bump SW (aucun changement de shell visible).
  Captures stress tests (dominante) + tuiles KPI + risque 1440
  envoyées, 0 erreur console. Suite 2461 passed / 2 skipped
  (inchangée — docs seulement).

- **Lot 203 — livré** : TOURNÉE TV — la volatilité et le
  positionnement Options. (1) CÔNE DE MOUVEMENT ATTENDU : les bandes
  1σ (brand) et 2σ (copper) sont une estimation lognormale
  (σ = spot·IV_ATM·√(DTE/365)) → remplissages HACHURÉS
  (C.hatchPattern lot 197 — la texture commune au cône de projection,
  au payoff et au théta), repli translucide propre si le helper est
  absent ; médiane, tooltips et légende inchangés. (2) GEX PAR
  STRIKE : les deux niveaux que le trader cherche — MUR CALL (max
  call GEX) et MUR PUT (max |put GEX|), calculés seulement s'il y a
  ≥ 2 strikes — deviennent les dominantes : barre pleine intensité
  (1 vs .55) + valeur RÉELLE en chip pleine couleur (texte sombre,
  borné au viewBox) au bout de la barre ; axe, strikes, spot
  pointillé et pied honnête inchangés. SW v166 → v167 + 5 gardiens.
  Captures cône hachuré (spot 180) + GEX ACN (chips « 15.59 M$ » /
  « −6.24 M$ ») + Volatilité 1440/390 envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : vol cone ✔, GEX ✔.

- **Lot 202 — livré** : TOURNÉE TV — le PRICE-CHART d'Analyse.
  CONSTAT sur le canonique : le graphique principal est rendu par
  TradingView Lightweight Charts et ses niveaux du plan sont DÉJÀ des
  étiquettes natives de l'échelle de prix (TP1 206.37 vert, Entrée
  198.00, Résistance, Stop 189.63 rouge, dernier prix, volume —
  vérifié navigateur sur /analysis/ACN) : le langage TV d'origine.
  REPLI Chart.js ALIGNÉ : C.levelLines (chart-core) passe du texte
  plat à gauche aux CHIPS pleine couleur au BORD DROIT (texte sombre
  gras, anti-collision verticale par empilement quand deux niveaux se
  chevauchent, bornage à la zone de tracé) — l'échelle de repli
  (bougies invalides → priceCard) parle désormais la même langue que
  le canonique. Lignes pointillées et couleurs par kind inchangées ;
  gardiens lot 52/54 (C.levelLines/multiLine) toujours verts. Note
  honnête : le repli n'est pas capturable en démo (le canonique
  fonctionne) — preuve par le code + suite. SW v165 → v166 +
  5 gardiens. Capture chandeliers ACN + Analyse 1440/390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  price-chart ✔.

- **Lot 201 — livré** : TOURNÉE TV — le RADAR de scores (C.radar,
  scorecard de la fiche Analyse) reçoit la règle « dominante en
  évidence » : le sommet à la valeur MAXIMALE réelle porte un anneau
  de focus (couleur, opacité .55) et sa valeur en CHIP pleine couleur
  (tvEdgeChip, texte sombre) posé VERS LE CENTRE le long du rayon —
  jamais sur les libellés d'axes. Grille dégressive, remplissage
  radial, points et libellés inchangés ; chip = valeur réelle
  arrondie (« 100 » sur l'axe Risque d'ACN en démo). JAUGE
  ENVIRONNEMENT OPTIONS : ✔ par héritage STRUCTUREL — mountEnvGauge
  appelle VXCharts.gauge directement (chemin unique vers la jauge TV
  lot 189) ; en démo l'hôte n'est pas rendu (données environnement
  absentes → état honnête), héritage prouvé par le code. SW v164 →
  v165 + 5 gardiens. Capture radar ACN + Analyse 1440/390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  radar ✔, jauge env. options ✔.

- **Lot 200 — livré** : TOURNÉE TV — la SÉRIE DE RÉFÉRENCE de
  Marchés (120 séances, SPY ou proxy honnête) reçoit les chips
  Max/Min : passthrough `extremes` de C.areaCard vers C.area (opt-in
  — aucun autre appelant modifié) + activation sur la carte de
  référence — les bornes RÉELLES de la période (Max 443,69 /
  Min 351,41 en démo) se lisent sur la courbe avec la pilule de
  dernière valeur, comme sur TV. DISCIPLINE Journal : ✔ par HÉRITAGE
  STRUCTUREL — les barres du Journal/Performance appellent
  VXCharts.bars directement (3 sites) → elles ont reçu le lot 199
  (dominante liserée + chip) sans modification ; journal démo vide →
  états vides honnêtes, héritage prouvé par le chemin de code
  unique. SW v163 → v164 + 5 gardiens. Captures série de référence +
  Marchés 1440/390 + Journal envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : aires de référence ✔,
  discipline ✔.

### MINI-BILAN tournée 196-200

5 lots, PR #229 → #233, suite stable 2461 passed / 2 skipped,
SW v159 → v164. La tranche a rendu TRANSVERSES les règles de la
grammaire TV : « dominante en évidence » appliquée à la staleness
Système (196 — tuile liserée + âge en chip du plus rassis), aux
barres partagées C.bars (199 — liseré + valeur en chip, hérité par
6 familles) ; texture « estimation » hachurée généralisée
(C.hatchPattern + option hatch de C.area, 197 — théta Options) ;
chips de valeur sur les pointeurs de rails (198 — VIX réel, « n/d »
honnête sur régime indéterminé) ; chips Max/Min sur les extrêmes
réels des aires (200 — série de référence Marchés). Deux ✔ par
HÉRITAGE constaté sans code : scénarios Options (197, via heatmap
194) et discipline Journal (200, via C.bars 199) — la grammaire
paye : chaque builder partagé aligné aligne ses pages gratuitement.
Honnêteté tenue partout (movers/journal vides rapportés, jamais de
dominante sur singleton). Reste à l'inventaire : price-chart
niveaux, radar, vol cone, GEX, double probabilité, sparklines KPI.

- **Lot 199 — livré** : TOURNÉE TV — les BARRES du builder partagé
  C.bars reçoivent la règle « dominante en évidence » : la barre au
  |valeur| max (calculée seulement s'il y a ≥ 2 barres — jamais une
  dominante sur singleton) porte un liseré appuyé (couleur pleine
  1.6 px vs alpha 80 / 1 px pour les autres) et sa VALEUR en chip
  pleine couleur (texte sombre — plugin canvas dans la grammaire
  tvEdgeChip, posé au bout de la barre, borné à la zone de tracé,
  vertical et horizontal gérés). Hérité par TOUS les appelants :
  sensibilité IV (Options), S+/S/A/B (Portefeuille), leadership
  (Marchés), discipline (Journal), movers (Système), recherche
  (Intelligence). Matière verre, survol, axes et formats inchangés ;
  la valeur du chip est la donnée RÉELLE formatée par le yFmt de
  l'appelant. Constat honnête : #vx-brain-movers ne se rend pas en
  démo (pas de mouvements) — rapporté sans agir. SW v162 → v163 +
  5 gardiens. Capture sensibilité IV GOOGL (chip rouge « −23.4 % »
  sur le choc −20 %, liseré appuyé) + Système 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  barres ✔ (sensibilité IV ✔ par héritage constaté).

- **Lot 198 — livré** : TOURNÉE TV — les RAILS de Marchés reçoivent
  le chip de valeur : nouvelle classe réutilisable
  .vx-rail-chipline/.vx-rail-chip (cockpit.css) — chip posé au-dessus
  du pointeur du rail, fond clair/texte sombre/gras 800/chiffres
  tabulaires (le même langage que le pointeur blanc des jauges lot
  189 et les chips de bord), positionné par --vx-rail-pos et BORNÉ
  aux extrémités (clamp) pour ne jamais déborder. Calme↔Stress : la
  valeur RÉELLE du VIX (12.7 en démo) à sa position sur l'échelle
  10→40 ; Défense↔Attaque : la confiance réelle du régime en %, et
  « n/d » HONNÊTE quand le régime est indéterminé — jamais un
  pourcentage inventé sur UNKNOWN. Dégradés des rails et flèches
  inchangés. SW v161 → v162 + 5 gardiens. Captures carte VIX (jauge +
  rail + chip 12.7) + rail positionnement (chip n/d) + 1440 + 390
  envoyées, 0 erreur console. Suite 2461 passed / 2 skipped.
  Inventaire TV : bandes linéaires ✔.

- **Lot 197 — livré** : TOURNÉE TV — le THÉTA Options assume sa
  texture de PROJECTION : nouveau C.hatchPattern (chart-core) =
  équivalent canvas du tvHatch (teinte .08 + rayures 45° .38),
  réutilisable par tous les builders Chart.js via la nouvelle option
  `hatch` de C.area (opt-in — défaut inchangé, aucun graphique
  modifié sans opt-in). option-theta : hatch + chip Min — la
  décroissance temps vient du scenario_pricer (un MODÈLE), l'aire est
  hachurée comme le payoff (192) et le cône (190), le chip Min marque
  le point le plus bas de la projection. SCÉNARIOS Options : ✔ par
  HÉRITAGE constaté (option-scenarios passe par C.heatmapCard → il a
  reçu le lot 194 sans modification — texte coloré par intensité,
  pire cellule −66 % en dominante, pied « estimation modèle, pas une
  promesse »). SW v160 → v161 + 5 gardiens. Captures théta hachuré
  (chip « Min 23,3 ») + matrice scénarios + 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  théta ✔, scénarios ✔. (Lot exécuté immédiatement sur ordre
  utilisateur — trigger annulé puis réarmé pour le 198.)

- **Lot 196 — livré** : TOURNÉE TV — FRAÎCHEUR PAR DOMAINE (Système,
  vue Données) : la règle « dominante en évidence » appliquée à la
  staleness — le domaine le PLUS RASSIS (âge max connu, calculé
  seulement s'il y a ≥ 2 âges connus, jamais un « pire » inventé sur
  un singleton) porte : tuile de la heatmap de fraîcheur au liseré
  appuyé (1.6 px) dans sa couleur d'état, et âge en CHIP pleine
  couleur (texte sombre, gras 800 — grammaire tvEdgeChip) à côté de
  sa barre dans la table. Les autres domaines restent adoucis ;
  domaine sans âge → ni barre ni chip (honnêteté du lot 142
  préservée). Âges/états strictement réels (/api/live/status), aucun
  seuil inventé. SW v159 → v160 + 5 gardiens. Capture : « companies »
  (20 952 min hors ligne) en chip rouge + tuile liserée, domaines à
  22 s adoucis — 1440 + 390 envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : staleness ✔.

- **Lot 195 — livré** : TOURNÉE TV — ÉQUITÉ & DRAWDOWN (Portefeuille)
  avec chips Max/Min sur les extrêmes RÉELS : nouveau
  C.tvExtremesPlugin (chart-core) — chips canvas dans la grammaire
  tvEdgeChip (fond plein, texte sombre), Max au-dessus du point, Min
  en dessous, bornés à la zone de tracé ; opt-in `extremes` de
  C.area (true | 'max' | 'min') — AUCUN autre graphique modifié sans
  opt-in. equity-chart : Max + Min (les deux chiffres du drawdown se
  lisent sur la courbe) ; drawdown-chart : Min seul = le PIRE creux
  réel. Pilule de dernière valeur, glow, crosshair, arithmétique et
  états vides honnêtes intacts. Preuve : série d'exemple semée
  LOCALEMENT dans le navigateur de test (add_init_script, jamais
  commitée) — la page reste honnêtement vide sans clôtures
  déclarées. SW v158 → v159 + 5 gardiens. Captures chips
  « Max 11510 »/« Min 10040 » et « Min −4 % » + 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  equity ✔, drawdown ✔.

### MINI-BILAN tournée 191-195

5 lots, PR #224 → #228, suite stable 2461 passed / 2 skipped,
SW v154 → v159. Tranche entièrement consacrée à la TOURNÉE GRAPHIQUE
TV (directive utilisateur du lot 188) : 9 signatures livrées —
barres de consensus du comité (191, style « Note des analystes »),
regimeAura aligné + payoff hachuré GAIN/PERTE (192), catalystRunway
en piste dégradée hachurée à chip J-x (193), heatmap à texte
d'intensité + cellule dominante et treemap à chips de part (194,
builders partagés → héritage large), équité/drawdown à chips
Max/Min sur extrêmes réels (195, opt-in). Un CORRECTIF STRUCTUREL
au passage : __VXVOCAB injecté par le shell de la refonte (191) —
libellés FR sur toutes les pages, gardien anti-XSS respecté.
Doctrine tenue : dégradés fondus, hachures = estimation, chips de
bord = chiffres clés, dominante en évidence ; données RÉELLES
uniquement (les constats démo — prime aberrante, tuiles sans P&L —
sont rendus honnêtement et RAPPORTÉS sans agir). Reste à l'inventaire :
sparklines KPI, aires indices, barres leadership, price-chart,
radar, vol cone, barres S+/S/A/B, GEX/scénarios/théta/IV options,
discipline Journal, staleness Système.

- **Lot 194 — livré** : TOURNÉE TV — la HEATMAP alignée (builder
  partagé C.heatmapCard — hérité par secteurs Marchés, P&L mensuel
  Portefeuille, scénarios/IV Options) : (1) le texte de chaque
  cellule porte la COULEUR de son intensité (alpha fondu .45 → 1 sur
  |t|, gras 700) — la grille se lit sans regarder les fonds, comme
  les cartes secteurs TV ; (2) la cellule DOMINANTE de TOUTE la
  grille (|t| max, une seule) en évidence — liseré appuyé 1.6 px +
  gras 800, les autres adoucies (même langage que la barre dominante
  du consensus lot 191). TREEMAP (chart-core) : la part « x % » des
  grandes tuiles passe du texte translucide au chip tvEdgeChip
  pleine couleur de la tuile (texte sombre) — grammaire des chips de
  bord. Tuiles verre, cellules nulles et navigation inchangées.
  Constat démo honnête : tuiles treemap neutres (P&L absent — la
  couleur ne s'invente pas). SW v157 → v158 + 5 gardiens. Captures
  heatmap secteurs (+1,28 % vert / −1,58 % rouge, dominante liserée)
  + treemap (chips 65 %/35 %) + 1440 + 390 envoyées, 0 erreur
  console. Suite 2461 passed / 2 skipped. Inventaire TV : heatmap ✔,
  treemap ✔.

- **Lot 193 — livré** : TOURNÉE TV — catalystRunway (Aujourd'hui)
  aligné sur la grammaire : (1) piste DTE en dégradé CONTINU
  (imminence rouge → jaune ancré à la frontière ≤ 5 j réelle →
  horizon éteint — le risque temporel est dans la matière de la
  piste) ; (2) zone ≤ 5 j HACHURÉE (tvHatch — la texture
  estimation/risque commune au cône lot 190 et au payoff lot 192) ;
  (3) le PROCHAIN catalyseur porte son échéance en chip tvEdgeChip
  pleine couleur d'impact (texte sombre), les suivants en texte.
  Anti-collision lot 61, anneau de focus, verdict tonal et état vide
  honnête STRICTEMENT inchangés ; helpers TV gardés par test
  d'existence. SW v156 → v157 + 5 gardiens. Capture piste (chip J-0
  rouge Emploi US, J-3/J-5/J-6/J-7) + 1440 + 390 envoyées, 0 erreur
  console. Suite 2461 passed / 2 skipped. Inventaire TV : runway ✔.

- **Lot 192 — livré** : TOURNÉE TV — deux graphiques alignés. (1)
  regimeAura (Aujourd'hui) rejoint la grammaire TV : l'arc de
  confiance ENTIER en dégradé continu de la tonalité du régime
  (fondu .18 → .95), POINTEUR blanc court posé sur l'arc à la
  position de la confiance (même langage que l'aiguille C.gauge du
  lot 189), « x % confiance » en évidence colorée gras 800 — halo,
  chips de grammaire et verdict inchangés, état honnête intact
  (sans régime → vide). (2) PAYOFF Options hachuré : _hatch(color) =
  équivalent CANVAS du tvHatch SVG (teinte .08 + rayures 45° .38),
  zones gain/perte du payoff en motifs hachurés (le payoff à
  l'échéance est une ESTIMATION) + libellés « GAIN »/« PERTE » de
  part et d'autre du breakeven selon C/P — arithmétique du contrat
  STRICTEMENT inchangée, contrat incomplet → vide honnête. Constat
  démo rapporté sans agir : prime GOOGL aberrante (3812) → P&L
  ≈ −100 % partout, rendu honnête des chiffres fournis. SW v155 →
  v156 + 5 gardiens. Captures Aujourd'hui 1440+390 + carte aura +
  carte payoff envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : aura ✔, payoff ✔.

- **Lot 191 — livré** : TOURNÉE TV — les BARRES DE CONSENSUS du
  comité (charts/consensus-bars.js, nouveau builder
  VXCharts.consensusBars) — le « Note des analystes » TradingView
  nourri par les comptes RÉELS des verdicts du comité : libellé à
  gauche, barre pleine à bout arrondi proportionnelle au max, compte
  à droite ; la barre DOMINANTE en pleine intensité et gras 800, les
  autres adoucies (.45) ; total honnête en pied (« N dossiers passés
  en revue — comptes réels ») ; vide → état vide honnête. CORRECTIF
  STRUCTUREL découvert par la 1re capture : __VXVOCAB n'était injecté
  que par l'ancien pipeline mort → désormais injecté par le SHELL de
  la refonte (`<script id="vx-vocab">` — l'id satisfait le gardien
  anti-XSS du lot 43), libellés FR (« Éviter », « Surveiller la
  cassure », « Attendre ») disponibles sur TOUTES les pages. Branché
  vue Comité d'Intelligence (remplace le tally ad hoc). SW v154 →
  v155 + 5 gardiens. Captures /intelligence?view=committee 1440+390
  + carte cadrée envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : consensus ✔.

- **Lot 190 — livré** : TOURNÉE TV — le CÔNE DE PROJECTION
  (charts/projection-cone.js, nouveau builder VXCharts.projectionCone)
  — la signature « prix cible » TradingView nourrie par les niveaux
  RÉELS du plan moteur : trait blanc des clôtures réelles → point
  actuel, éventail HAUSSIER hachuré (tvHatch) entre TP1 et TP3 avec
  médiane pointillée TP2, faisceau de RISQUE vers le stop, frontière
  « PROJECTION — plan moteur », chips de bord tvEdgeChip (TP3 +x %,
  TP2, TP1, Actuel, Stop −x % — pourcentages CALCULÉS). Sans plan
  complet → état vide honnête ; pied « une carte de risque, pas une
  prévision de marché ». Branché en tête de la carte « Plan &
  niveaux clés » de la fiche Analyse. Marge chips ajustée après la
  1re capture. SW v153 → v154 + gardiens. Captures /analysis/ACN
  1440+390 + carte cadrée envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : cône ✔.

### MINI-BILAN tournée 186-190

5 lots, PR #219 → #223, suite 2450 → 2461 passed, SW v152 → v154.
Bascule en cours de tranche : après les gardiens transverses (186 :
31 fichiers JS src= node --check + ≥40 assets 0 lien mort + 0
externe ; 188 : 54 endpoints d'API fetchés 0 mort) et un DÉFAUT RÉEL
corrigé (187 : le design-system affichait des hex périmés → hex
DÉRIVÉS de tokens.css, la double source a disparu), la DIRECTIVE
UTILISATEUR a ouvert la TOURNÉE GRAPHIQUE TV (« que tout Vertex
ressemble à ça — fluide, beau, parfait ») : fondation livrée (189 —
inventaire complet, grammaire tvHatch/tvEdgeChip, JAUGE TV à arc
dégradé continu et pointeur blanc héritée par 6 appelants) puis la
première grande signature (190 — le cône de projection du plan sur
la fiche Analyse). Doctrine tenue : données RÉELLES uniquement (pas
de plan → vide honnête, jamais un consensus inventé), tokens
uniquement (les gardiens couleur ont refusé 2 fallbacks — corrigés),
captures envoyées à chaque lot. Suite de l'inventaire : consensus
comité, regimeAura, payoff hachuré, treemap, equity/drawdown,
heatmap, GEX.

- **Lot 189 — livré** : TOURNÉE GRAPHIQUE TV — FONDATION (directive
  confirmée par l'utilisateur en cours de lot : « que tout Vertex
  ressemble à ça — fluide, beau, parfait »). Inventaire complet des
  graphiques vivants (TV-CHARTS-INVENTORY.md, statuts + plan des
  lots), grammaire TV dans chart-core (tvHatch « estimation »,
  tvEdgeChip d'étiquette de bord) et PREMIÈRE SIGNATURE refaite : la
  JAUGE passe au style TradingView — arc entier en dégradé CONTINU
  (couleurs des bandes fondues, rouge→jaune→vert), pointeur blanc
  court posé sur l'arc (ajusté après 1re capture pour ne jamais
  couvrir le texte), état coloré en évidence sous l'arc. API 100 %
  compatible : les 6 appelants (Marchés ×3, Portefeuille, Système,
  Intelligence, options-intel) héritent sans changement. Les
  gardiens couleur ont refusé 2 fallbacks hors inventaire →
  conformes (#121214). Captures Breadth/Volatilité 1440+390
  envoyées, 0 erreur console. SW v152 → v153 + gardiens.
  Suite 2461 passed / 2 skipped.
- **Lot 188 — livré** : gardien des LIENS D'API des pages vivantes
  (54 endpoints fetchés par les 11 pages servies — 0 mort, motifs
  paramétrés gérés) + invariants d'intelligence_page (662 l, la
  moins gardée) : 6 vues 200 avec UN SEUL onglet actif le bon, vue
  inconnue → défaut jamais cassée, 0 id dupliqué, ≥ 12 VX.states,
  page saine. 5 tests. Suite 2456 → 2461 passed / 2 skipped.

## ⚡ DIRECTIVE UTILISATEUR ACTIVE (reçue au lot 188) — TOURNÉE GRAPHIQUE TV

L'utilisateur (captures TradingView SKHY à l'appui) demande la
REFONTE DE TOUS LES GRAPHIQUES de Vertex, lot par lot, un par un,
dans le langage visuel TradingView : jauges semi-circulaires
DÉGRADÉES à aiguille (Strong sell → Strong buy), cône de projection
prix cible min/moy/max en éventail, barres de consensus analystes,
zones d'ESTIMATION hachurées sur les barres de prévision, doubles
axes annotés, tableaux réels vs estimations — « moderne, équilibré,
voyant, beau, structuré au mieux ». Chaque graphique, chaque widget.
Protocole par lot : grammaire commune d'abord (chart-core), puis 1-2
builders refaits par lot AVEC serveur DEMO + captures navigateur +
SendUserFile + SW bump + gardiens. Données RÉELLES uniquement
(absent → n/d), tokens seulement, aucun littéral couleur nouveau.

- **Lot 187 — livré** : DÉFAUT RÉEL CORRIGÉ sur la page de référence
  /design-system (254 l, zéro test dédié) — elle affichait des hex
  PÉRIMÉS recopiés à la main : 10+ étiquettes divergeaient de
  tokens.css (--vx-black affiché #020202, réel #060405 ; les tokens
  devenus alias var() montraient l'ancienne valeur). Correctif
  STRUCTUREL minimal : les hex sont désormais DÉRIVÉS de tokens.css
  à l'import (alias résolus) — la double source a disparu, la page
  LIT la vérité et ne peut plus mentir. 6 tests : preuve rouge/vert
  (≥ 30 swatches, 0 divergence), variables toutes existantes (un
  renommage CSS fait échouer la référence), alias montrés résolus,
  ids uniques + littéraux interdits absents + data-ds-copy ≥ 20 +
  état vide au libellé produit exact. SW v151 → v152 (changement
  visible) + 4 gardiens de version mis à jour. Moteurs intacts.
  Suite 2450 → 2456 passed / 2 skipped.
- **Lot 186 — livré** : GARDIEN DES JS STATIQUES et des liens
  d'assets (extension du lot 182 : le sweep couvrait l'inline, pas
  les fichiers src=). 5 tests figent : les 31 fichiers JS du
  produit (chart-core, regime-aura, catalyst-runway, vx-shell…)
  parsent TOUS par node --check (seul exclu documenté : la
  bibliothèque tierce minifiée vendor) ; les ≥ 40 assets référencés
  par les 13 routes servies résolvent TOUS en 200 — aucun lien
  mort ; AUCUN asset http(s) externe (l'autonomie hors-ligne des
  lots 81-85 est désormais gardée en continu) ; chaque builder
  charts s'enregistre sur VXCharts (exception documentée : le thème
  → VXChartTheme, miroir de palette.py déjà gardé). Constat : état
  présent sain — 0 invalide, 0 lien mort, 0 externe. Aucun code
  modifié, pas de bump SW. Suite 2445 → 2450 passed / 2 skipped.
- **Lot 185 — livré** : cartographie de mort, volet FONCTIONS
  (clôture 183-185, rien supprimé). Méthode PRUDENTE (un doute =
  vivant ; racines = décorées, référencées au module, vues actives,
  références externes) : 29 des 91 fonctions top-niveau de
  terminal.py sont mortes — 62 lignes seulement, QUE des stubs de
  vues legacy (≤ 4 lignes : return PAGE_* morte, redirection ou
  render migré) + _rail + _legacy_pages_redirect ; AUCUNE logique
  métier morte. Les 9 boucles de fond sont CLASSÉES VIVANTES (garde
  anti-faux-positif testée). 5 tests figent l'inventaire, la garde,
  la nature des stubs, le recoupement endpoints et le poids chiffré.
  Aucun code modifié, pas de bump SW.
  Suite 2440 → 2445 passed / 2 skipped.

### MINI-BILAN tournée 181-185 — « UI vivante + cartographie de mort »

5 lots, PR #214 → #218, suite 2416 → 2445 passed (+29 tests), SW
stable v151 (tournée tests pure). Deux fils : (1) les couches UI
VIVANTES gardées — home_art caractérisée (injection, progressive
enhancement, VIX narratif) et la règle critique n°2 SYSTÉMATISÉE
(chaque bloc <script> inline de chaque page servie passe au vrai
parseur node --check, garde anti-vide) ; (2) la CARTOGRAPHIE DE MORT
de terminal.py, prudente et prouvée (AST + introspection Flask +
recoupement empirique) : 25 pages (~2 265 l) + 35 couches JS/CSS +
29 fonctions stubs (62 l) + 2 helpers — morts, orphelins,
inventaires EXACTS figés par tests (ressusciter ou supprimer =
décision explicite), aucun vieux lien utilisateur ne tombe dans le
vide (39 redirections vérifiées). AUCUNE logique métier morte — le
poids mort est du HTML/JS d'anciennes pages. DÉCISION HUMAINE EN
ATTENTE : autoriser le lot de purge (≈ 25-30 % du monolithe) ?

- **Lot 184 — livré** : vie/mort des COUCHES JS/CSS du monolithe
  (extension du lot 183, rien supprimé). Par AST + recoupement
  empirique : les 35 chaînes _*_JS/_*_CSS de terminal.py ne
  nourrissent QUE les 25 pages mortes — chaque assignation qui les
  consomme vise une PAGE_* morte ou une autre couche ; _vpage (20
  appels module-niveau, tous vers des pages mortes) et _rail (défini
  mais appelé NULLE PART — helper mort) sont les seuls à les
  toucher ; les marqueurs signés (hmHost, artBoard) sont absents des
  11 pages réellement servies. 5 tests figent l'inventaire exact et
  ces preuves. Bilan cumulé du poids mort de terminal.py : 25 pages
  + 35 couches + 2 helpers (~2 265+ lignes) — purge = décision
  humaine (question ouverte depuis le lot 183). Aucun code modifié,
  pas de bump SW. Suite 2435 → 2440 passed / 2 skipped.
- **Lot 183 — livré** : VÉRIFICATION DE VIE des pages legacy de
  terminal.py — CONSTAT STRUCTUREL documenté, rien supprimé : par
  introspection des vues Flask ACTIVES, les 25 blobs PAGE_*
  (~2 265 lignes de HTML/JS) ne sont plus servis par AUCUNE route —
  la refonte (vertex/ui/pages + redesign) a tout repris, les 39
  anciennes URLs redirigent vers les 8 espaces canoniques, et aucun
  module n'importe terminal.PAGE_* (mortes ET orphelines). 5 tests
  figent : l'inventaire EXACT des 25 mortes (ressusciter ou
  supprimer = mise à jour explicite de l'inventaire) ; l'orphelinat
  prouvé ; les 39 redirections vers leur cible exacte ; les
  destinations = les 8 espaces canoniques, toutes 200 (aucun vieux
  lien ne tombe dans le vide) ; aucune chaîne de redirections.
  QUESTION OUVERTE à l'utilisateur : autoriser un futur lot de
  PURGE de ces ~2 265 lignes mortes ? Aucun code modifié, pas de
  bump SW. Suite 2430 → 2435 passed / 2 skipped.
- **Lot 182 — livré** : GARDIEN GLOBAL DE SYNTAXE JS — la règle
  critique n°2 (« tout JS généré depuis Python doit être valide —
  deux SyntaxError silencieuses ont déjà vécu ») SYSTÉMATISÉE
  (survey honnête : tracking_page/vault/sync_center ont leurs
  gardiens de contenu, la lacune était transverse). 6 tests : les
  16 routes HTML canoniques répondent toutes 200 et CHAQUE bloc
  <script> inline de chaque page est validé par node --check —
  0 erreur tolérée (une apostrophe française non échappée fait
  désormais échouer la suite) ; garde anti-vide (≥ 12 blocs
  réellement contrôlés — le gardien ne peut pas passer en tournant
  à vide) ; sync_center.JS et le _HEATMAP_JS du vault validés AVANT
  injection ; l'extracteur lui-même testé unitairement (src/json
  ignorés, inline gardé). Constat : tout l'état présent parse — le
  gardien empêche la régression. Aucun code modifié, pas de bump
  SW. Suite 2424 → 2430 passed / 2 skipped.
- **Lot 181 — livré** : caractérisation de la COUCHE ARTISTIQUE de
  l'accueil `vertex/ui/home_art.py` (171 lignes, ZÉRO test —
  VIVANTE : appliquée sur PAGE_DAILY et PAGE_STRATEGIE ; survey
  honnête : ibkr_scheduler/source_router couverts par 22 tests,
  quant_engine par 17, swing/events aussi). 8 tests figent :
  l'injection pure (apply() → <style>+<script> UNE fois avant
  </body>, sans </body> → no-op silencieux ; apply_desk() → CSS
  SEUL) ; la syntaxe JS RÉELLE validée par node --check (règle
  critique n°2 — deux SyntaxError silencieuses ont déjà vécu, un
  vrai parseur garde désormais cette couche) ; le progressive
  enhancement (catch → tout visible, arrêt propre sans #ovMarket,
  reduced-motion dans les deux CSS) ; le contrat de données
  (fetch /api/market/summary, rafraîchi 90 s SEULEMENT onglet
  visible, chiffres fr-FR, bandes narratives VIX ≤14/≥22 distinctes
  des bandes de données 16/22 du lot 153, VIX absent → tiret
  honnête) ; le câblage réel prouvé (artBoard dans PAGE_DAILY,
  DESK_CSS dans PAGE_STRATEGIE qui reste sans script). Aucun code
  modifié, pas de bump SW. Suite 2416 → 2424 passed / 2 skipped.
- **Lot 180 — livré** : caractérisation des DONNÉES ANALYSTES
  PROFONDES `vertex/data_sources/analyst_deep.py` (226 lignes, ZÉRO
  test, servi par la fiche titre — scheduler/live_stream déjà
  couverts lots 109/99, traces/logging dormants sans appelant :
  écartés à dessein). 10 tests HORS LIGNE (faux ticker pandas, faux
  yfinance injecté dans sys.modules, cache isolé) figent : le NaN
  écarté (jamais un chiffre fantôme) ; les révisions BPA (net30 +
  tendance, repli '0y' → '0q') ; les surprises (le trimestre À VENIR
  séparé en `next`, beats 2/3 + moyenne 5.6 exacte) ; les notes
  d'analystes (récentes d'abord, cap 6, firm bornée 40) ; les
  initiés (solde + biais, non classable → None) ; et la politique de
  cache — cache FRAIS servi sans AUCUN appel réseau (faux yfinance
  qui explose si touché : prouvé), yfinance mort → le cache PÉRIMÉ
  servi plutôt que rien, échec TOTAL jamais persisté. Aucun code
  modifié, pas de bump SW. Suite 2406 → 2416 passed / 2 skipped.

### MINI-BILAN tournée 176-180 — « surfaces de sécurité »

5 lots, PR #209 → #213, suite 2375 → 2416 passed (+41 tests), SW
stable v151 (tournée tests pure). Après la clôture des routes
(lot 176 : funnel fail-honest, copilot jamais une 500, live
parsing), la tranche a durci les surfaces de sécurité : le gardien
XSS DE BOUT EN BOUT (lot 177 — payload injecté dans les états,
neutralisé à CHAQUE sortie HTTP, + gardien statique ≥ 6 sites
sanitize_news) ; le filet du desk (lot 178 — snapshot quotidien
jamais réécrit, rotation 7, restore anti-traversal, ts neuf qui
gagne le LWW) ; l'observabilité bornée en mémoire (lot 179 —
percentiles exacts, anneau 200, timer qui propage) ; et les données
analystes (lot 180 — périmé plutôt que rien, échec jamais caché,
zéro réseau prouvé). Constats honnêtes en série : auth.py (15
tests), webhook TradingView (12), config (secrets jamais renvoyés,
lot 111), startup (lot 105), client-log (lot 94) étaient DÉJÀ
blindés — les surfaces de sécurité du produit sont désormais toutes
gardées par des tests. Prochaine direction au survey du lot 181.

- **Lot 179 — livré** : caractérisation de l'OBSERVABILITÉ du
  Strategy OS (§37) — `vertex/observability/metrics.py` (ZÉRO test
  direct) et les sections de `diagnostics.py` (le webhook TradingView,
  candidat prévu, s'est révélé complet avec 12 tests — constat
  honnête, repli sur la vraie lacune). 9 tests figent : les
  compteurs qui CUMULENT vs les jauges qui ÉCRASENT ; les
  percentiles EXACTS (100 mesures 1..100 → p50 51.0/p95 95.0/max
  100.0, échantillon unique → confondus) ; l'anneau de 200 mesures
  (250 envoyées → fenêtre 51..250, p50 151.0 — bornage mémoire) ;
  le timer contextuel qui mesure ET propage l'exception (jamais
  avalée, durée enregistrée quand même) ; le snapshot COPIE isolée ;
  les sections de system_diagnostics STRICTEMENT optionnelles (sans
  dépendance → {metrics} seul, rien d'inventé) ; data_quality_report
  qui compte TOUS les paquets mais borne les dégradés à 20 et les
  warnings à 3. Aucun code modifié, pas de bump SW.
  Suite 2397 → 2406 passed / 2 skipped.
- **Lot 178 — livré** : FILET DE SÉCURITÉ DU DESK — backup quotidien
  + /api/desk/restore de `desk.py` (règle critique n°6 ; le candidat
  auth.py s'est révélé déjà très couvert — 15 tests force-brute/
  open-redirect — constat honnête, repli sur la vraie lacune).
  8 tests figent : le snapshot quotidien créé au PREMIER écrasement
  du jour avec le contenu d'AVANT le push, jamais réécrit par les
  pushs suivants (le snapshot du matin protège la journée), rotation
  à 7 (les plus vieux purgés) ; le restore qui refuse TOUT nom hors
  motif strict (../../etc/passwd, date incomplète, suffixe — le
  path traversal est impossible), introuvable → 404, illisible →
  500 SANS toucher le desk courant, réussi → données du snapshot
  avec un ts DE MAINTENANT (gagne le last-writer-wins sur tous les
  appareils) ; la liste triée du plus récent au plus ancien. Aucun
  code modifié, pas de bump SW. Suite 2389 → 2397 passed /
  2 skipped.
- **Lot 177 — livré** : GARDIEN XSS DE BOUT EN BOUT (règle critique
  n°5 : « tout texte externe passe par sanitize_news avant d'être
  servi »). Le lot 102 figeait la FONCTION ; rien ne prouvait que
  chaque ROUTE applique l'assainissement. 6 tests injectent un
  payload malveillant (script, img onerror, lien javascript:) dans
  les états partagés et vérifient chaque point de sortie :
  /news-feed sert le titre SANS balise avec quotes échappées, la
  traduction vidée, le lien javascript: supprimé et le lien https
  %-encodé (sûr en href ET window.open) ; le filtre serveur ?sym=
  ne contourne PAS l'assainissement ; /api/events/<sym> et
  /api/skyler/<sym> ne servent JAMAIS le payload brut (le texte
  survit neutralisé à travers evidence/events) ; un gardien
  statique compte les sites d'appel sanitize_news( en production
  (≥ 6 — content, analysis_api ×2, skyler_sweep, terminal ×2) :
  retirer un assainissement fait échouer la suite. Aucun code
  modifié, pas de bump SW. Suite 2383 → 2389 passed / 2 skipped.
- **Lot 176 — livré** : CLÔTURE de la tournée « honnêteté des
  routes » — les trois lacunes minces restantes en un lot
  (opportunities_api, ai_api /api/copilot/ask POST, live_api).
  8 tests figent : les 7 étages EXACTS de l'entonnoir (universe →
  … → positions) et son chemin d'erreur fail-honest (moteur en
  panne → 500 avec structure VIDE + erreur nommée, jamais un
  entonnoir à moitié inventé) ; le copilote qui n'explose JAMAIS
  (body vide OU JSON corrompu → 200 ok False « question vide ») et
  son repli sans clé DOUBLEMENT étiqueté (le label ET l'étiquette
  dans la réponse elle-même — le contenu varie selon le scan,
  l'étiquette jamais) ; le contrat du rapport live {lines,
  requested, ts}, le parsing des domaines (espaces/vides purgés,
  ordre gardé), le domaine inconnu → rien relancé mais demande
  tracée ; aucun verbe d'ordre dans les 3 modules. Leçon encodée :
  figer les INVARIANTS stables (parsing, étiquettes), pas les états
  transitoires (kicked dépend de l'état du moteur). Aucun code
  modifié, pas de bump SW. Suite 2375 → 2383 passed / 2 skipped.
- **Lot 175 — livré** : honnêteté HTTP de la SESSION D'ANALYSE
  `vertex/app/routes/session_api.py` (la logique de RESTAURATION de
  /api/session/digest était la lacune — moteur digest et manifest
  déjà couverts). 8 tests figent : le démarrage à froid → 'analyzing'
  servi tel quel ; le digest prêt → servi, mémorisé ET persisté ;
  l'écriture disque THROTTLÉE (2 appels < 30 s → 1 écriture) ; le
  scan retombé « pas prêt » → instantané 'restored' avec l'as_of
  absolu conservé mais l'ÂGE EFFACÉ (jamais un âge faussement
  frais) ; la restauration sert une COPIE (le mémo reste 'ready') ;
  session_id_for refuse bool et chaîne ; la couverture plafonnée à
  100 % sur univers périmé (600/517 → 100, jamais 116) ; aucun
  verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2367 → 2375 passed / 2 skipped.

### MINI-BILAN tournée 171-175 — « honnêteté des routes »

5 lots, PR #204 → #208, suite 2338 → 2375 passed (+47 tests, dont
les 10 du lot 171 déjà comptés dans 2338 : tranche réelle 2328 →
2375), SW stable v151 (tournée tests pure). La NOUVELLE DIRECTION
ouverte au lot 171 a figé la couche HTTP des routes les plus
sensibles — les moteurs étaient couverts, le câblage ne l'était
pas : positions_api (desk vide/corrompu honnête, IBKR hors ligne ne
clôture JAMAIS, introuvable → 200 + erreur documenté) ·
decision_api (params corrompus avalés, seuils -20/-25 % intacts par
HTTP, pas de covered call sans actions) · tracking_api (DATA_REQUIRED
sans prix inventé, étiquette HYPOTHÉTIQUE imposée, stop gèle,
restart n'écrase pas) · planning_api (le ticket d'ordre COMMENCE
par le disclaimer READONLY, stop « non transmis », la concentration
bloque même à budget correct) · session_api (instantané restauré à
l'âge EFFACÉ, throttle disque). Fil rouge prouvé partout : état
vide → réponse honnête, entrée corrompue → jamais un crash, donnée
absente → jamais inventée, AUCUN verbe d'ordre dans aucun module de
routes. Reste mince : opportunities funnel, copilot/ask POST,
live report — à balayer ou clore au lot 176.

- **Lot 174 — livré** : honnêteté HTTP du TICKET DE PRÉPARATION
  D'ORDRE `vertex/app/routes/planning_api.py` (/api/planning/ticket
  — la route la plus sensible au READONLY : elle prépare un texte à
  COPIER dans IBKR sans jamais transmettre) et de la RECHERCHE
  /api/search de feeds.py. 10 tests figent : sans symbole → 400 ;
  le plan du scan repris tel quel avec dimensionnement EXACT
  (100 k × 1 % = 1 000, risque unitaire 5 → 200 actions, rr 3.0
  transmis) ; la CONCENTRATION qui bloque même avec un budget de
  risque correct (poids projeté 20 % > 15 % → blocked + blocker
  explicite) ; le body qui prime sur le plan du scan ; les refus
  honnêtes (sans compte → sizing None sans blocage, stop au-dessus
  de l'entrée → « risque non défini », option sans prime → « prime
  indisponible ») ; l'option dimensionnée sur la prime (250 par
  contrat → 4) ; l'INVARIANT PRODUIT : chaque copy_text COMMENCE
  par « PRÉPARATION UNIQUEMENT — Vertex est en lecture seule et ne
  transmet aucun ordre » et le stop y est « (référence, non
  transmis) » ; la recherche (vide → [], insensible à la casse,
  plafond dur 20). Aucun code modifié, pas de bump SW.
  Suite 2357 → 2367 passed / 2 skipped.
- **Lot 173 — livré** : honnêteté HTTP du moteur de SUIVI
  `vertex/app/routes/tracking_api.py` (le cycle de vie
  /api/tracking/<id>, /performance, /stop, /restart, /history était
  à ZÉRO test — seuls la liste et la création étaient couverts).
  10 tests figent : les refus explicites (404 « suivi introuvable »
  sur les 5 sous-routes, 400 « symbol requis ») ; la création
  honnête (action inconnue du scan → 201 mais DATA_REQUIRED avec
  reference_price None — JAMAIS un prix inventé ; action cotée →
  référence LAST/« scan » tracée, benchmark SPY, is_hypothetical
  True ; option → MID exact du body) ; la performance au prix
  courant RÉEL du scan avec l'étiquette IMPOSÉE « Suivi
  HYPOTHÉTIQUE : aucune position réelle… », l'option exigeant son
  mark en paramètre (sans mark → None, jamais un chiffre sans
  source) ; le stop qui GÈLE le résultat (final_price/return/MFE/MAE
  exacts) ; le restart à identifiant NEUF laissant l'ancien suivi
  gelé ; aucun verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2347 → 2357 passed / 2 skipped.
- **Lot 172 — livré** : honnêteté HTTP des DÉCISIONS DE POSITION
  `vertex/app/routes/decision_api.py` (deux endpoints à ZÉRO test :
  /api/position-decision/<sym> et /api/options-for/<sym> — les
  moteurs servis sont couverts par le lot 87, la lacune était le
  câblage HTTP). 9 tests figent : le symbole inconnu → HOLD avec
  sous-jacent étiqueté DATA_INSUFFICIENT (jamais inventé) ; le stop
  touché via query params → EXIT 78 ; les paramètres corrompus
  (entry=abc, dte=) avalés en None — JAMAIS un crash ; les seuils de
  discipline traversant la couche HTTP intacts (action -20 % EXIT,
  option -20 % HOLD, -25 % EXIT) ; le thêta qui commande à ≤14 j ;
  le board vide → note explicite sans contrat inventé ; les 5 rôles
  exacts pour une position action (CALL/PUT/LEAPS/COVERED_CALL/
  PROTECTIVE_PUT) réduits à 3 pour une option détenue (pas de call
  couvert sans actions) ; jamais un contrat d'un autre titre ; aucun
  verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2338 → 2347 passed / 2 skipped.
- **Lot 171 — livré** : NOUVELLE DIRECTION « honnêteté des routes » —
  caractérisation de la couche HTTP Position Intelligence
  `vertex/app/routes/positions_api.py` (249 lignes ; survey préalable :
  options/ et research/ déjà couverts, mais 4 endpoints à ZÉRO test —
  /api/positions/state, /report, /audit, /reconcile — alors que les
  moteurs sous-jacents ont 41 tests directs). 10 tests figent : le
  desk vide → live False DIT, P&L/delta/theta None (jamais un 0
  inventé) ; la position réelle recalculée au prix RÉEL du scan
  ((200−150)×10 = 500), cible dépassée → action DESCRIPTIVE
  « SÉCURISER » mais décision ATTENDRE (Vertex n'exécute jamais) ;
  IBKR hors ligne → « aucune clôture automatique », 0 réparation ;
  desk corrompu → 200 + vide honnête (state ET stress) ; introuvable
  → HTTP 200 + erreur explicite DOCUMENTÉ tel quel (pas 404) ; le
  diff « ce qui a changé » (baseline puis +5 % → MAJOR, snapshot
  persisté) ; aucun verbe d'ordre dans la source. Aucun code modifié,
  pas de bump SW. Suite 2328 → 2338 passed / 2 skipped.
- **Lot 170 — livré** : caractérisation de l'UNIVERS
  `data/universe.py` (324 lignes — données pures : l'univers scanné,
  la watchlist, les cartographies GICS/industrie ; DERNIER module de
  la file du périmètre ai/data/strategy/portfolio). 9 tests figent
  les INVARIANTS DE COHÉRENCE : univers dédupliqué ≥ 400 tickers,
  LIVE_SYMBOLS == UNIVERSE == INDEX_MEMBERS['union'] (une seule
  vérité), INDEX_SOURCE ∈ {live, cache, cache-stale, static} ;
  normalisation yfinance (AUCUN point dans l'univers US ni la
  watchlist — BRK-B ; les suffixes de place vivent exclusivement
  dans _EUROPE/_ASIA, toutes suffixées) ; _GICS exactement 11
  secteurs miroir des 11 ETF ; AUCUN ticker dans deux secteurs ni
  deux industries, aplatis couvrant exactement les déclarés ;
  watchlist 57 sans doublon ; TREND_SET == set(_TREND_EXTRA).
  Aucun code modifié, pas de bump SW.
  Suite 2319 → 2328 passed / 2 skipped.

### MINI-BILAN tournée 166-170

5 lots, PR #199 → #203, suite 2271 → 2328 passed (+57 tests), SW
stable v151 (tournée tests pure). Couverts : la couche IA optionnelle
(briefs — dégradation IA → Google → texte d'origine, jamais un texte
perdu, clé réelle exigée) ; le copilote d'analyse (chemin Claude
mocké, réponse étiquetée « estimation, pas une donnée broker »,
contexte mort → erreur honnête) ; la stratégie options personnalisée
legacy_adapter (VIVANTE — PUT imposé en régime dangereux, sorties
±50 %, portefeuille à arithmétique fermée) ; le profil d'entreprise
(segments curés sommant 100 %, schéma _v force le re-fetch, « jamais
de page vide ») ; et l'univers (une seule vérité par ticker, une
seule liste servie au live). La file du périmètre est ÉPUISÉE : tous
les modules de vertex/engines, market, quant, services, ai, data,
strategy et portfolio ont désormais des tests directs — plus aucun
moteur sans caractérisation. Prochaine direction à choisir au lot
171 (honnêteté des routes, sécurité, options/, research/).

- **Lot 169 — livré** : caractérisation du PROFIL D'ENTREPRISE
  `data/company.py` (340 lignes — cache hebdo + couche curée hors
  ligne + fetch yfinance côté utilisateur ; testé HORS LIGNE,
  _fetch_profile monkeypatché). 9 tests figent : l'INVARIANT des
  segments curés (les 20 répartitions somment toutes à 100 %) ; la
  démo qui sert la couche curée avec stale True SIGNALÉ ; le
  symbole inconnu → squelette honnête (None partout, jamais
  inventé) ; l'ordre cache/fetch/curé (fetch réussi → cache écrit,
  second appel sans réseau, schéma antérieur → re-fetch
  automatique, fetch mort → secours curé « jamais de page vide ») ;
  les pairs de la même industrie (soi-même exclu, cap 4) ; les
  médianes sectorielles (seuil 3 membres, PE < 250 strict,
  conversions en %, memo qui tient même vide — le cache 1.4 Mo
  n'est pas reparsé). Aucun code modifié, pas de bump SW.
  Suite 2310 → 2319 passed / 2 skipped.
- **Lot 168 — livré** : caractérisation de la STRATÉGIE OPTIONS
  PERSONNALISÉE `legacy_adapter.py` (272 lignes, 0 test — VIVANTE :
  servie par command et terminal ; échelle 1/2/3/6/9/12 mois,
  mark-to-market Black-Scholes en cours de route, constructeur de
  portefeuille). 21 tests figent : le régime (mots-clés + seuils
  exacts 60/40, {} → neutral) ; les briques (IV bornée [0.22,
  1.10], pas de strike 1/2.5/5/10, détention ~1/3 bornée 5-45 j) ;
  la jambe d'option (breakeven call = strike+prime / put =
  strike−prime, sorties EXACTES +50 %/−50 %, alerte théta clampée,
  scénarios ORDONNÉS pess < prob < except, cible technique du plan
  valorisée en route) ; le RÉGIME DANGEREUX qui impose le PUT même
  sur conviction haussière (défense d'abord) ; le portefeuille
  cœur×3/satellites×2 à arithmétique FERMÉE (cash = capital −
  déployé, maxloss = déployé, risque/position ~10 % borné) et le
  portefeuille vide honnête sans candidats. Aucun code modifié,
  pas de bump SW. Suite 2289 → 2310 passed / 2 skipped.
- **Lot 167 — livré** : caractérisation étendue du COPILOTE
  D'ANALYSE `ai/copilot.py` (159 lignes — répond en français ancré
  dans les nombres réels ; Anthropic entièrement mocké). 8 tests
  figent les LACUNES des 5 tests existants : les positions du desk
  (cap 20, filtre par symbole, stop repris du snapshot d'entrée,
  desk illisible → [] jamais inventé) ; le contexte sans symbole
  réduit à digest + positions ; le post-mortem chiffré inclus
  quand des trades clôturés existent ; le symbole normalisé
  (majuscules, 12 max) ; le chemin Claude mocké — succès étiqueté
  « estimation, pas une donnée broker » readonly True, texte vide
  ou exception API → repli déterministe étiqueté (jamais
  d'exception propagée) ; contexte indisponible → ok False avec
  erreur honnête et answer None. Aucun code modifié, pas de bump
  SW. Suite 2281 → 2289 passed / 2 skipped.
- **Lot 166 — livré** : caractérisation de la COUCHE IA OPTIONNELLE
  `ai/briefs.py` (178 lignes — traduction FR des news, mini-profils,
  descriptions ; dégradation IA → Google gratuit → texte d'origine).
  10 tests entièrement HORS LIGNE (_google_fr monkeypatché selon son
  contrat) : available exige une clé RÉELLE (absence, placeholder
  sk-ant-xxxx et mauvais préfixe rejetés) ; fr_news sans clé →
  repli Google avec CACHE (aucun second appel pour les mêmes
  titres), désalignement de lignes → titres anglais d'origine
  (fidélité > traduction), échec réseau → origine ; company_brief
  sans clé/résumé → {} (jamais un profil inventé) ; fr_label et
  fr_desc cachés avec repli sur l'origine (jamais un texte perdu).
  Aucun code modifié, pas de bump SW. Suite 2271 → 2281 passed /
  2 skipped.
- **Lot 165 — livré** : caractérisation du MOTEUR DE RISQUE du
  portefeuille RÉEL `risk_engine.py` (§26, servi par strategy_os —
  la chaîne du risque est désormais COMPLÈTE : correlation +
  stress_tests + basket_risk + risk_engine). 8 tests figent : la
  garde de provenance (snapshot 'SCANNER' → ValueError — le risque
  ne se calcule JAMAIS sur les candidats du scanner) ; les agrégats
  exacts (surpoids 66.67 % > 15 %, HHI 0.4623, secteur 80 % > 40 %
  averti, bêta pondéré 1.07 ; aucun bêta connu → None jamais un
  1.0 inventé) ; les règles de discipline aux bornes INCLUSES
  (drawdown -25 % pile → no_new_risk True « AUCUN nouveau risque » ;
  titre -23.1 % ≤ -20 % → revue obligatoire) ; le plafond d'options
  (4 > 3 → blocage) avec agrégat de greeks HONNÊTE (somme des seuls
  connus, gamma absent → None pas un 0, greeks_partial signalé) ;
  le contrat 14 clés. Aucun code modifié, pas de bump SW.
  Suite 2263 → 2271 passed / 2 skipped.

### MINI-BILAN tournée 161-165

5 lots, PR #194 → #198, suite 2239 → 2271 passed (+32 tests), SW
stable v151 (tournée tests pure). Couverts : les constituants
d'indices (« le démarrage n'est jamais bloqué » désormais PROUVÉ
par l'ordre de résolution cache → live → stale → static) ; le trio
audit/contexte/rôles (le journal IA borné, et les 4 RAPPELS
D'INVARIANTS READONLY injectés dans chaque analyse IA figés mot
pour mot) ; l'exposition factorielle et le moteur de remplacement
(« décision humaine requise » — jamais une exécution) ; la
vérification de vie des deux legacy (TOUS DEUX VIVANTS — aucun code
mort) ; le risque de panier (cap infaisable → somme n × cap,
concentration non détectée sur petit panier, FAIL-OPEN sur erreur
— trois limites documentées) ; et le moteur de risque réel (chaîne
du risque complète, bornes de discipline incluses, provenance
gardée). Le périmètre ai/data/strategy/portfolio n'a plus que
briefs/copilot/company/universe (couvertures partielles) et
legacy_adapter en file. Tout changement futur de ces sémantiques
fera échouer la suite.

- **Lot 164 — livré** : caractérisation du RISQUE DE PANIER
  `legacy_basket_risk.py` (99 lignes, 0 test — VIVANT malgré son
  nom : servi par analysis_api, command et risk_engine ; le
  « no-trade de concentration »). 8 tests figent : les gardes
  (panier < 2 séries → note honnête sans blocage, série < 40
  points exclue) ; le drapeau de corrélation (paire clonée 0.92 →
  no_new_risk True + top_pair expliquée ; panier diversifié →
  aucun drapeau) ; TROIS LIMITES documentées — cap infaisable
  (n × 15 % < 100 % → somme des poids = n × cap, pas de
  renormalisation), concentration sectorielle NON détectée sur
  petit panier (2 titres mono-secteur capés à 30 % restent sous le
  seuil 40 %), et FAIL-OPEN sur erreur (entrée illisible →
  no_new_risk False, l'analyse ne bloque pas quand elle ne peut
  pas conclure) ; la redistribution _cap_weights (somme 1 quand
  faisable). Aucun code modifié, pas de bump SW.
  Suite 2255 → 2263 passed / 2 skipped.
- **Lot 163 — livré** : caractérisation de l'EXPOSITION FACTORIELLE
  `factor_exposure.py` et du MOTEUR DE REMPLACEMENT
  `replacement_engine.py` (§25, zéro-test, dépendances research/
  monkeypatchées) + VÉRIFICATION DE VIE des deux legacy : TOUS
  DEUX VIVANTS (legacy_basket_risk → analysis_api + command +
  risk_engine ; legacy_adapter → command + terminal) — aucun code
  mort à signaler, candidats à caractérisation future. 8 tests
  figent : la pondération par les poids RÉELS (1.5 exact), la
  couverture partielle SIGNALÉE (« exposition indicative »),
  value None sans donnée (jamais un zéro inventé), les 10 facteurs
  toujours présents ; côté remplacement : place disponible → rien,
  bloqué → la plus faible du rôle avec « décision humaine
  requise » (jamais une exécution), candidat moins bon →
  « déconseillé », rôle sans membre → pool global documenté, sans
  scores → départage au défaut 50 mais score affiché None. Aucun
  code modifié, pas de bump SW. Suite 2247 → 2255 passed /
  2 skipped.
- **Lot 162 — livré** : caractérisation du TRIO zéro-test —
  `ai/audit.py` (journal des appels IA servi par strategy_os),
  `ai/strategy_context.py` (contexte injecté dans chaque analyse
  IA) et `portfolio/team_roles.py` (rôles §25). 8 tests figent :
  le journal BORNÉ à 200 entrées avec erreurs tronquées à 5 (pas
  de fuite verbeuse), les stats ok/fallbacks, le journal neuf
  honnêtement vide ; le contrat 10 clés du contexte avec bornes
  cohérentes ET les 4 RAPPELS D'INVARIANTS figés mot pour mot
  (« lecture seule absolue: aucun ordre », « moteur exécutif
  déterministe », « aucune promesse de performance », « jamais
  inventer » — les affaiblir cassera ce test) ; les 4 rôles dans
  l'ordre terrain, cohérents avec ROLE_TARGETS (une seule vérité
  d'effectifs), DEFENDER/GOALKEEPER sans horizon. Aucun code
  modifié, pas de bump SW. Suite 2239 → 2247 passed / 2 skipped.
- **Lot 161 — livré** : caractérisation des CONSTITUANTS D'INDICES
  `data/constituents.py` (112 lignes, 0 test — nourrit l'univers
  des titres au démarrage : Wikipedia + cache disque + snapshot
  statique). 9 tests SANS réseau (fetch monkeypatché, cache isolé) :
  normalisation yfinance (BRK.B → BRK-B), filtrage des tickers
  implausibles avec dédup ordonnée, intégrité du snapshot statique
  (≥ 400/80/25 ET déjà normalisé), et surtout l'ORDRE DE RÉSOLUTION
  complet — sans cache + réseau mort → static (démarrage JAMAIS
  bloqué), cache frais prioritaire (aucun appel réseau), force=True
  qui retente puis retombe sur cache-stale, liste vide dans le
  cache → repli statique PAR INDICE, fetch réussi → live + cache
  persisté ; garde-fou parsing (listes < 400/80/25 → ValueError
  explicite). Aucun code modifié, pas de bump SW.
  Suite 2230 → 2239 passed / 2 skipped.
- **Lot 160 — livré** : caractérisation de la famille RISQUE
  PORTEFEUILLE — `correlation.py` (consommé par risk_engine →
  drapeau du Command Center) et `stress_tests.py` (route
  strategy_os, §26), deux modules zéro-test. 11 tests figent :
  bornes ±1.0 exactes, gardes (< 30 points / variance nulle →
  None), paires triées, seuils high_pairs ≥ 0.8 et avertissement
  ≥ 0.7, matrice vide honnête ; côté stress : l'hypothèse
  DOCUMENTÉE bêta inconnu = 1.0 (SPY -5 % → -4.17 % exact), le
  secteur dominant, CORRELATIONS_TO_ONE qui ne choque QUE les
  actions (le cash protège), la sensibilité taux inconnue → None
  honnête, le REFUS des stress sans équité calculable, le
  worst_case et l'alerte drawdown, les 10 scénarios déclarés
  présents. Aucun code modifié, pas de bump SW.
  Suite 2219 → 2230 passed / 2 skipped.

### MINI-BILAN tournée 156-160

5 lots, PR #189 → #193, suite 2178 → 2230 passed (+52 tests), SW
stable v151 (tournée tests pure). Couverts : la structure par
pivots (les 5 signaux du plan, anti-chasse 1.2 ATR), les
indicateurs techniques purs (quatre philosophies de trous de
données DOCUMENTÉES : SMA se réinitialise, EMA traverse, ATR
recopie, VWAP resservi ; RSI golden Wilder 70.5), la règle de
fraîcheur du Live Engine (bornes STRICTES des 7 domaines — à la
borne on bascule déjà), l'horloge de marché (borne 4h00, limite
jours fériés documentée), et la famille risque portefeuille
(corrélations + stress tests : bêta inconnu = 1.0, le cash protège,
refus honnête sans équité). Le nouveau périmètre ai/data/strategy/
portfolio est inventorié : 11 modules zéro-test, file publiée au
lot 159. Tout changement futur de ces sémantiques fera échouer la
suite et devra être assumé explicitement.

- **Lot 159 — livré** : complément de l'HORLOGE DE MARCHÉ
  `market_clock.py` (5 tests : borne pré-marché 4h00 exacte,
  vendredi 20h00 → fermé jusqu'au lundi, format « 09:05 ET »
  zéro-paddé, et une LIMITE documentée — pas de calendrier de
  jours fériés : le 1er janvier en semaine est affiché « open »,
  ajouter un calendrier NYSE = décision explicite que ce test
  rendra visible) + INVENTAIRE du nouveau périmètre
  (vertex/ai/, data/, strategy/, portfolio/) : 11 modules à ZÉRO
  test découverts, dont la FAMILLE RISQUE PORTEFEUILLE
  (correlation 42 l, factor_exposure 29 l, replacement_engine
  36 l, stress_tests 85 l) priorisée pour le lot 160, puis
  data/constituents (112 l), ai/audit, ai/strategy_context, et
  deux legacy à vérifier (legacy_basket_risk, legacy_adapter).
  Aucun code modifié, pas de bump SW. Suite 2214 → 2219 passed /
  2 skipped.
- **Lot 158 — livré** : caractérisation de la RÈGLE DE FRAÎCHEUR du
  LIVE ENGINE `live_engine.py` (258 lignes — le moteur de
  synchronisation dont dépendent toutes les pages ; les 13 tests
  existants couvrent les flux, ce lot fige les BORNES de la partie
  pure). 19 tests : les bornes STRICTES des 7 domaines (à la borne
  exacte on bascule déjà — age == frais → stale, age == rassis →
  offline ; seuils figés : prices 5 min/30 min, options 1 h/6 h,
  companies 48 h/8 j, news 2 h/12 h, calendar 1 j/4 j, weekly
  8 j/15 j, ai 5 min/30 min) ; les défauts du domaine inconnu
  (600/3600) ; les bascules de libellés EXACTES (59s → « 59s »,
  60 → « 1 min », 3600 → « 1 h », 86400 → « 1 j ») ; l'âge None →
  « jamais synchronisé » honnête ; le forçage de cycle (wait_force
  réveillé → True et l'événement CONSOMMÉ ; force_event rend le
  même objet par domaine). Aucun code modifié, pas de bump SW.
  Suite 2195 → 2214 passed / 2 skipped.
- **Lot 157 — livré** : caractérisation des INDICATEURS TECHNIQUES
  purs `market/indicators.py` (155 lignes, §12 — SMA/EMA/RSI/ATR/
  Bollinger/VWAP sans pandas ; seules les LACUNES des 11 tests
  existants sont figées). 9 tests : robustesse (non-numérique →
  None traversant, fenêtre nulle → tout None) ; les ASYMÉTRIES de
  trous de données DOCUMENTÉES — SMA se réinitialise (honnêteté de
  fenêtre), EMA traverse (pas de fenêtre à invalider), ATR recopie
  la dernière valeur, VWAP resservi sur volume nul — deux
  philosophies assumées, les unifier = décision explicite ;
  longueurs H/L/C tronquées au minimum ; la valeur GOLDEN du RSI
  sur la série classique de Wilder (70.5 — prouve le lissage de
  Wilder, pas une SMA) ; le multiplicateur Bollinger à écart
  symétrique exact. Aucun code modifié, pas de bump SW.
  Suite 2186 → 2195 passed / 2 skipped.
- **Lot 156 — livré** : caractérisation de la STRUCTURE PAR PIVOTS
  `pivots.py` (124 lignes, ratio 0.65 — structure() appelée par
  analysis.py : sommets/creux fractals, tendance, logique d'entrée,
  stop STRUCTUREL du plan). 8 tests figent, chacun par un zigzag
  déterministe : les 5 signaux — EN_TENDANCE (milieu de mouvement →
  pas d'entrée), REFUS_DOWNTREND (rebond en baisse = piège, aucun
  niveau émis), RANGE (cassure confirmée exigée), BREAKOUT
  (franchissement RÉCENT ≤ 1.2 ATR anti-chasse → stop sous le
  dernier creux, cible = extension measured-move, rr cohérent),
  REPLI_REPRIS (repli ≤ 1.8 ATR sur le creux PUIS reprise → cible
  le sommet) ; les gardes (série courte / entrée invalide → None) ;
  le repli ATR à 1 % du cours (jamais de ÷0) ; le contrat 16 clés
  avec fenêtres swing bornées à 4. Aucun code modifié, pas de bump
  SW. Suite 2178 → 2186 passed / 2 skipped.
- **Lot 155 — livré** : caractérisation du BRIEF ÉDITORIAL
  `editorial.py` (202 lignes, ratio 0.34 — le narratif de séance
  §10 en tête d'Aujourd'hui ; scoring.py écarté car déjà couvert
  finement par le lot 97). 17 tests figent : les seuils EXACTS des
  phrases d'indices (±0.15), le leadership technologique à écart
  STRICT > 0.2 (0.2 pile ne déclenche pas) et la rotation
  cyclique ; les trois phrases VIX aux bornes 18/25 ; la frontière
  breadth 55 (saine/sélectivité) ; la PRIORITÉ des risques
  (RISK-OFF avant breadth étroite ; breadth < 45 strict, 45 pile →
  aucun risque déclaré) ; la branche calls IV chère ; le titre
  « À la une » borné à 180 caractères ; les sources triées et
  dédupliquées ; l'opportunité prioritaire qui saute les REFUSER.
  Aucun code modifié, pas de bump SW. Suite 2161 → 2178 passed /
  2 skipped.

### MINI-BILAN tournée 151-155

5 lots, PR #184 → #188, suite 2098 → 2178 passed (+80 tests), SW
stable v151 (tournée tests pure). Les modules minces HORS engines/
sont couverts : les SIX à zéro test (regime_features — le cerveau
physique qui modifie le score, sectors, ml_calibration, context,
news_impact, news_pipeline) plus editorial (0.34). Découvertes clés
désormais VERROUILLÉES par des tests : une droite pure n'a pas
d'exposant de Hurst (analyze(droite) = NEUTRE malgré efficience
1.0) ; les bornes humbles de la probabilité de gain [0.05, 0.85]
(jamais une promesse) ; le verdict météo « participation ?% »
honnête ; la limite de sous-chaîne du classement d'actualités
('ai' matche dans « mountain ») ; les bandes VIX 16/22 (données)
vs 18/25 (narratif) ; les bornes RORO ±8 ; la hiérarchie des
risques éditoriaux (régime indéterminé > RISK-OFF > breadth < 45).
Tout changement futur de ces sémantiques fera échouer la suite.

- **Lot 154 — livré** : caractérisation des ACTUALITÉS (§15) —
  `news_impact.py` (classement par mots-clés + importance +
  direction potentielle) et `news_pipeline.py` (validation/dédup/
  tri), deux modules zéro-test servis par daily_brief. 20 tests
  figent : la priorité du PREMIER match (MACRO gagne sur RESULTATS)
  et le défaut ENTREPRISE ; une LIMITE documentée — matching par
  SOUS-CHAÎNE, le mot-clé 'ai' matche dans « mountain »/« rain » →
  SECTEUR (passer aux frontières de mots = décision explicite) ;
  l'arithmétique d'importance EXACTE (base 30, corroborations
  plafonnées +30, portefeuille +25, bonus catégorie, plafond 100) ;
  les seuils de direction ±0.15 EXACTS avec confiance plafonnée
  0.7 (humble, jamais une causalité affirmée) ; les rejets du
  pipeline COMPTÉS jamais masqués ; le doublon fusionné en
  corroborations (2 → importance 80 recomposée) ; sym en
  majuscules, fr vide → None, tri décroissant, état vide honnête.
  L'assainissement XSS reste chez news_plus (déjà couvert). Aucun
  code modifié, pas de bump SW. Suite 2141 → 2161 passed /
  2 skipped.
- **Lot 153 — livré** : caractérisation du CONTEXTE MARCHÉ
  `context.py` (105 lignes, 0 test — la « météo » du jour servie
  par decision_api et terminal : régime du SPY lui-même, bandes
  VIX, Risk-On/Off cycliques vs défensifs, breadth des leaders,
  verdict du jour). 15 tests figent : la robustesse totale (5 ×
  None → contrat complet, verdict quand même émis avec
  « participation ?% » honnête — limite documentée) ; le régime
  SPY (rampe → TREND ADX 100, oscillation → CHOP) ; les bandes VIX
  à bornes EXACTES (15.9 calme / 16.0 normal / 21.9 normal / 22.0
  stress ; 1 seul point → None) ; la breadth réelle (nh pos52 ≥ 98,
  nl ≤ 5) ; les bornes RORO EXACTES ±8 (gap 8 RISK-ON, 7 NEUTRE,
  -8 RISK-OFF ; sans secteurs → 50/50 NEUTRE) ; le verdict complet
  composé. Aucun code modifié, pas de bump SW.
  Suite 2126 → 2141 passed / 2 skipped.
- **Lot 152 — livré** : caractérisation combinée de la ROTATION
  SECTORIELLE `sectors.py` (83 lignes, 0 test — servie par le
  comité et la fiche Analyse) et de la CALIBRATION ML
  `ml_calibration.py` (92 lignes, 0 test — probabilité de gain
  consommée par quant_engine). 13 tests figent : agrégats exacts
  (avg_score, pct_buy, breadth depuis les signaux), tri décroissant,
  symbole hors mapping exclu, bornes risk_band exactes (<3 Low,
  3-5 Med, >5 High), delta vs veille (scores None ignorés, sans
  baseline → None), défauts neutres sans détail moteur ; côté ML :
  point NEUTRE edge 54 → 0.500, calibration annoncée figée
  (86 → 0.736, 30 → 0.317), bornes HUMBLES [0.05, 0.85] (jamais
  une promesse), ajustement Monte-Carlo first-touch, et deux
  limites documentées — bloc None → proba neutre 0.468 mais edge
  NON NUMÉRIQUE → prédiction entière None (pas de repli partiel).
  Aucun code modifié, pas de bump SW. Suite 2113 → 2126 passed /
  2 skipped.
- **Lot 151 — livré** : NOUVELLE DIRECTION — modules minces HORS
  engines/. Inventaire par ratio : six modules à ZÉRO test direct
  (market/context, news_impact, news_pipeline, regime_features,
  sectors, quant/ml_calibration). Choisi : `regime_features.py`
  (179 lignes) — le CERVEAU PHYSIQUE importé par analysis.py, dont
  la rétroaction score_adjust MODIFIE le score Vertex. 15 tests
  figent : Hurst persistant > 0.56 / anti-persistant < 0.2 + LIMITE
  documentée (une droite PURE n'a pas d'exposant — différences
  décalées constantes → None, d'où analyze(droite) = NEUTRE malgré
  efficience 1.0) ; entropie (constants → 0.0, concentré < dispersé,
  garde 30 points) ; efficience de Kaufman (monotone → 1.0 exact,
  aller-retour → 0.0, plat → None) ; demi-vie OU (rappel fort →
  courte, tendance → None honnête) ; états TENDANCE
  FRACTALE/RETOUR MOYENNE avec notes ; rétroaction EXACTE (+4/+7,
  -7, -3/-6, -2 entropie extrême — extrêmes réels +7/-9, marge
  sous les bornes [-10,+8]) ; physique absente → (0, ''). Séries
  déterministes à graines fixes (PCG64 stable). Aucun code modifié,
  pas de bump SW. Suite 2098 → 2113 passed / 2 skipped.
- **Lot 150 — livré** : caractérisation du DIGEST DE SESSION
  `session_digest.py` (116 lignes, ratio 0.80 — dernier de la file
  des moteurs minces ; servi par /api/session/digest, affiché en
  tête d'Aujourd'hui). 8 tests figent : la garde RISK-ON + S&P en
  CHOP → NEUTRE (un risk-on dans un marché haché n'est pas un feu
  vert) ; RISK-OFF prioritaire même seul ; le score /100 branché
  sur l'unique source market_lens.climate (93 — jamais réinventé) ;
  les dte booléens/texte ignorés sans masquer les catalyseurs
  valides (tri croissant) ; scan_ts booléen → âge None (même garde
  que le lot 142 côté UI) ; build(None, None) honnêtement
  'analyzing' ; top borné à 3 avec compte complet ; contrat de
  sortie exact. Aucun code modifié, pas de bump SW.
  Suite 2090 → 2098 passed / 2 skipped.

### MINI-BILAN tournée 146-150

5 lots, PR #179 → #183, suite 2033 → 2098 passed (+65 tests), SW
stable v151 (aucun changement de shell — tournée moteur pure). La
file des moteurs par couverture croissante est ÉPUISÉE : analysis
(ratio 0.19), strategy_fit (0.35), postmortem (0.61), market_lens
(0.66), stats (0.77), session_digest (0.80) — tous caractérisés
sur leurs branches, gardes, bornes exactes et comportements
limites. Découvertes clés désormais VERROUILLÉES par des tests :
divergence des seuils FAVORABLE (62 au climat market_lens vs 65 au
tilt strategy_fit — même formule) ; Spearman à rangs ordinaux (une
série constante « corrèle » à 1.0) ; break-even classé perte ;
profit factor None jamais infini ; booléens rejetés par toutes les
gardes numériques ; Socle défensif exige un ext_atr explicite ;
l'inconnu n'est jamais investissable (plancher scorecard 18/40 <
seuil B). Tout changement futur de sémantique sur ces points fera
échouer la suite et devra être assumé explicitement.

- **Lot 149 — livré** : caractérisation du PRISME MARCHÉ
  `market_lens.py` (77 lignes — source unique du score marché /100,
  servie par feeds/decision_api/command) + `stats.py` (Spearman de
  l'edge, médianes secteur). 13 tests figent : les bornes EXACTES
  des bandes du climat (FAVORABLE ≥62, DANGEREUX <40) avec une
  DIVERGENCE réelle documentée (même formule que le tilt
  strategy_fit mais seuil 62 ici contre 65 là-bas) ; climat sur
  None ET {} → None (pas de climat inventé) ; le tiers supérieur
  porteur (n=2 → seul le rang 1) ; le score de secteur non
  numérique classé dernier avec avg_score None honnête ; la
  frontière titre fort à 70 STRICTE ; « 2 verts dont le titre » →
  partiellement aligné (pas contre-courant) ; la frontière Spearman
  8 points ; une LIMITE documentée — rangs ordinaux sans rangs
  fractionnaires : une série constante « corrèle » à 1.0
  (pathologique en réel, la changer = décision explicite) ; les
  bornes strictes 0 < PE < 250 et l'exclusion des secteurs sans
  valorisation. Aucun code modifié, pas de bump SW.
  Suite 2077 → 2090 passed / 2 skipped.
- **Lot 148 — livré** : caractérisation étendue du POST-MORTEM du
  Journal `postmortem.py` (151 lignes, ratio 0.61 — fonction pure
  servie par /api/journal/postmortem, affichée dans
  Journal/Discipline). 10 tests figent : la coercition numérique
  (cost=True REJETÉ — bool est un int, un flag ne devient jamais
  un coût ; chaînes numériques OK ; inf/0/négatif inexploitables) ;
  deux limites DOCUMENTÉES — break-even classé PERTE (win_rate 0,
  PF None sans ÷0) et échantillon 100 % gagnant → PF None (indéfini
  honnête, PAS infini) avec narrative sans phrase PF ; le drapeau
  « win rate élevé mais P&L négatif » ; les récidives triées par
  nombre de pertes décroissant ; les dates inversées (abs) et non
  parsables (None exclu de la moyenne — pas de 0 inventé) ; les 8
  dernières erreurs du journal tronquées à 140 ; le contrat de
  sortie identique plein/vide avec generator déterministe. Aucun
  code modifié, pas de bump SW. Suite 2067 → 2077 passed / 2
  skipped.
- **Lot 147 — livré** : caractérisation étendue de la COUCHE
  STRATÉGIE `strategy_fit.py` (161 lignes, ratio 0.35 — source
  unique : terminal.py délègue vehicle_of / attach_vehicle /
  strat_score ; c'est elle qui choisit ACTION vs OPTION et oriente
  les playbooks). 17 tests figent : la branche AU CHOIX et le
  message « IV chère » ; les défauts EXACTS du strat_score (score
  seul → 50, ligne vide → 22, clamp 0) ; la PRIORITÉ des 6
  playbooks (Momentum avant Qualité) + limite documentée (Socle
  défensif exige un ext_atr explicite — le calme non prouvé n'est
  pas calme) ; attach_vehicle (meilleur CALL par qualité, PUT
  ignoré, board vide → ACTION) ; le seuil rr_ok ≥ 2 STRICT (1.99
  échoue) avec repli plan → vx_rr et R:R inconnu honnête ; les 3
  bandes du tilt à l'arithmétique exacte (93 FAVORABLE / 50 NEUTRE
  avec round bancaire / DANGEREUX). Aucun code modifié, pas de
  bump SW. Suite 2050 → 2067 passed / 2 skipped.
- **Lot 146 — livré** : caractérisation étendue du CŒUR analytique
  `analysis.py` (333 lignes — la couverture la plus mince de
  vertex/engines/, ratio tests/moteur 0.19 : le golden figeait UN
  scénario, aucune branche de détection couverte). 17 tests
  figent : robustesse aux flux sans Volume (indices/ETF) et à
  l'historique court (repli SMA→EWM, JSON sans NaN) ; profils
  DÉFENSIF et ÉQUILIBRÉ ; radar d'anomalies (gap, pic de volume)
  avec FORMULE du score figée (min(100, Σ sév × 16)) et niveaux
  cohérents ; cassure confirmée (volume ≥1.5× exigé) ; régime
  CHOP ; invariants du plan (stop sous l'entrée, échelle exacte
  1R/2R/3R, setup_quality borné) ; transparence du score
  (score == clamp(base + struct_adj [-12,+10])) ; checklist des
  9 signaux + sigcount. Aucun code modifié, pas de bump SW.
  Suite 2033 → 2050 passed / 2 skipped.
- **Lot 145 — livré** : caractérisation du moteur `scorecard.py`
  (254 lignes) — vérifié VIVANT : importé par terminal.py (alias
  `ibkr`), `verdict()` appelé pendant le scan ; produit le score
  /40, les niveaux S+/S/A/B + allocations, l'entry timing, le
  no-chase et le verdict affichés dans Opportunités ; c'était le
  DERNIER moteur à zéro référence dans tests/. 36 tests figent :
  grille des niveaux à bornes exactes (36/32/28/22 + allocations),
  les 4 raisons no-chase isolées, les 6 états d'entry timing, le
  plancher neutre 18/40 → rejeté (l'inconnu n'est jamais
  investissable), la fenêtre catalyseur earnings (7-45 j idéale),
  verdict({}) → None (falsy — pas de données, pas de verdict),
  somme des composantes == score40 (une seule vérité), robustesse
  aux valeurs pourries. Aucun code modifié, pas de bump SW.
  Suite 1997 → 2033 passed / 2 skipped.

### MINI-BILAN tournée 141-145

5 lots, PR #174 → #178, SW stable v150 → v151 : fourchette
analystes en rail à repères (141) · staleness par domaine en barre
relative + garde Number(null) (142) · tournée de vérification
transversale : AUCUN défaut restant, l'esthétique 124-143 est
déclarée COMPLÈTE sur preuves (143) · pivot vers les
caractérisations moteur : timeframes.py figé en 13 tests (144) ·
scorecard.py — le dernier moteur à zéro test — figé en 36 tests
(145). Suite 1984 → 2033 passed / 2 skipped : plus AUCUN moteur de
vertex/engines/ sans test direct ; les deux contributeurs au score
(confluence ±5, scorecard /40) ont désormais leurs contrats,
gardes et planchers neutres verrouillés par des tests qui rendent
tout changement de sémantique explicite.

- **Lot 144 — livré** : retour aux caractérisations moteur —
  `timeframes.py` (confluence journalier × hebdo, contribue ±5 au
  score Vertex, drapeau `mtf` du scan) n'avait AUCUN test direct.
  13 tests figent : les 5 états et leurs contributions exactes
  (ALIGNÉ HAUSSIER +5 · REPLI DANS TENDANCE +3 · REBOND
  CONTRE-TENDANCE -4 · ALIGNÉ BAISSIER -5 · NEUTRE 0, cette
  dernière branche construite empiriquement : prix > EMA30 hebdo
  mais EMA10 qui se retourne) ; gardes < 32 semaines → None et
  entrée non ré-échantillonnable → None ; contrat de sortie 9 clés
  typées ; comportement limite série plate DOCUMENTÉ (ALIGNÉ
  BAISSIER, RSI 100 — pathologique, le changer = décision
  explicite). Aucun code moteur/UI modifié, pas de bump SW.
  Suite 1984 → 1997 passed / 2 skipped.
- **Lot 143 — livré** : tournée de VÉRIFICATION transversale des
  8 espaces (clôture de la directive esthétique maximale) : 8
  captures desktop 1440 fraîches (une par espace, 0 erreur console
  chacune) inspectées à la recherche des derniers défauts — chiffres
  nus, chevauchements, barres plates, badges débordants, étiquettes
  coupées. Constat honnête : AUCUN défaut restant ; les fixes des
  lots 125/129/133/142 tiennent tous ; le treemap Portefeuille
  neutre est l'honnêteté (marques IBKR indisponibles), pas un
  défaut. Lot documentaire — aucun code modifié, PAS de bump SW
  (v151 courante). La tournée esthétique 124 → 143 est COMPLÈTE.
  Suite 1984/2, RC GO, parcours 14/14, responsive 0 défaut.
- **Lot 142 — livré** : passe graphique n°17 — Système/Données :
  l'ÂGE de la fraîcheur par domaine n'est plus un texte nu —
  mini-barre de verre de STALENESS relative (échelle = âge max
  connu) : les domaines frais restent discrets, le plus rassis
  (companies, 20 481 min) saute aux yeux en pleine barre negative.
  Couleur par état ; sans âge connu → pas de barre (garde
  d.age_s == null AVANT Number(), car Number(null) = 0).
  Automatisations vérifiée (badges + honnêteté déjà corrects).
  SW v150 → v151 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 141 — livré** : passe graphique n°16 — fiche Analyse,
  section Sentiment : la FOURCHETTE des objectifs analystes n'est
  plus du texte nu — RAIL de verre low → high avec deux repères
  halotés : le COURS en cyan et l'OBJECTIF MOYEN en warning. On
  voit d'un coup d'œil où le prix vit dans la fourchette (cours 198
  AU-DESSUS de l'objectif 179 → potentiel négatif expliqué).
  Repères clampés aux bords, bornes affichées, title au survol.
  SW v149 → v150 + 4 gardiens. Captures + zoom envoyés.
  Suite 1984/2, RC GO.
- **Lot 140 — livré** : passe graphique n°15 — Top/Flop 10 de la Vue
  d'ensemble Marchés : chaque variation gagne sa mini-barre SIGNÉE
  de verre (positive → verte depuis la gauche, négative → rouge
  alignée à droite ; échelle relative au max de la liste) — la
  hiérarchie des mouvements se lit sans les pourcentages (ABT -6,3 %
  pèse visiblement 3× ALGN -1,3 %). SW v148 → v149 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 136-140

5 lots, suite constante **1984 passed / 2 skipped**, PR #169 → #173,
SW v144 → v149 : comparaison des candidats en verre + score Skyler
/40 en barre graduée (136) · poids de position avec repère du
plafond de tier (137) · concentration avec repère prudent ~15 %
(138) · leadership sectoriel avec halo du meneur (139) · Top/Flop
10 en barres signées (140). Le patron « mini-barre de verre
color-mix sur tokens » est GÉNÉRALISÉ — plus un seul chiffre nu
structurant sur les 8 espaces ; chaque barre porte désormais soit
une graduation (seuils moteur), soit un signe (axe zéro), soit un
repère (plafond/seuil prudent), soit un halo (meilleur/pire/meneur).

- **Lot 139 — livré** : passe graphique n°14 — Vue d'ensemble
  Marchés : le Leadership sectoriel passe en VERRE — chaque barre
  est un dégradé de sa propre couleur (color-mix) et le secteur
  MENEUR garde l'ember avec un halo doux (le leadership se voit
  avant de lire le score). Hiérarchie par intensité conservée.
  Aujourd'hui vérifiée : Aura, Runway, listes et tuiles KPI déjà
  au niveau (tuiles gardées — non touchées). SW v147 → v148 +
  4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 138 — livré** : passe graphique n°13 — Synthèse
  Portefeuille : la tuile KPI CONCENTRATION n'est plus un chiffre
  nu — mini-barre de verre avec le REPÈRE prudent (~15 % par titre,
  celui cité par le Risque dominant) au tick : < 15 % positive,
  15-25 warning, > 25 negative + halo. Le 65 % d'ACN vire au rouge,
  la donnée et son seuil se parlent enfin. n/d honnête conservé.
  SW v146 → v147 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 137 — livré** : passe graphique n°12 — Positions
  Portefeuille : le POIDS de chaque position devient une mini-barre
  de verre avec REPÈRE DU PLAFOND du tier (tick à 60 % du rail =
  plafond, ex. 15 % Constitution ; sous 80 % → positive, proche →
  warning, au-dessus → negative + halo). Sans tier connu : échelle
  simple, aucun plafond inventé. Le chiffre éducatif d'un poids,
  c'est sa distance au plafond. SW v145 → v146 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 136 — livré** : passe graphique n°11 — Radar Opportunités :
  (a) la Comparaison des meilleurs candidats passe en VERRE — chaque
  barre est un dégradé de sa propre couleur et le MEILLEUR du
  critère gagne un halo doux ember (le gagnant se voit sans lire
  les nombres) ; (b) le score canonique /40 du Classement Skyler
  gagne sa mini-barre graduée (≥ 28 positive, 16-27 warning, < 16
  negative). Watchlist vérifiée : états vides honnêtes en démo.
  SW v144 → v145 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 135 — livré** : passe graphique n°10 — scan Actions
  (Opportunités) : le SCORE n'est plus un chiffre nu — mini-barre de
  verre GRADUÉE 0-100 (≥ 70 positive = actionnable, 40-69 warning =
  à surveiller, < 40 negative = rejeté — les seuils réels du
  moteur), dégradé color-mix sur tokens, valeur tabulaire conservée.
  La hiérarchie de la liste de travail quotidienne se lit d'un coup
  d'œil. SW v143 → v144 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 131-135

5 lots (passes noyau → widgets faits main), suite constante
**1984 passed / 2 skipped**, PR #164 → #168, SW v139 → v144 :
stress tests verre + pire scénario mis en avant (131) · anomalies
en mini-barres + calendrier avec imminence ≤ 7 j (132) · payoff de
structure Options — 2 bugs préexistants tués, spot/BE enfin tracés
(133) · net GEX en barre signée depuis l'axe zéro (134) · score du
scan en barre graduée (135). Le patron « mini-barre de verre
color-mix sur tokens » est devenu la réponse standard aux chiffres
nus ; 3 bugs visuels réels tués sur la tournée (stats collées,
rails invisibles, plugins payoff jamais exécutés).

- **Lot 134 — livré** : passe graphique n°9 — radar de positionnement
  du desk Options : le net GEX n'est plus un nombre nu — mini-barre
  SIGNÉE de verre depuis l'axe zéro (positif → droite en positive =
  stabilisant ; négatif → gauche en negative = accélérateur ;
  dégradé color-mix sur tokens, échelle relative au max du radar,
  valeur M$ conservée à côté). L'œil voit qui pousse où et avec
  quelle force. Vue LEAPS vérifiée (rien de plat). SW v142 → v143
  + 4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 133 — livré** : passe graphique n°8 — payoff de structure du
  desk Options : **2 bugs préexistants tués** — (a) le 3e argument
  `[refPlugin]` passé à `C.mount` (qui n'en prend que 2) était
  silencieusement ignoré : les repères spot/breakeven ne
  s'affichaient JAMAIS ; (b) `getPixelForValue(prix)` sur un axe
  catégorie attend un index → mapping prix→index ajouté. Repères
  désormais sur tokens (spot info, BE warning — grammaire lot 124,
  les rgba orphelins morts), zones gain/perte teintées, trait 1.6 +
  halo. SW v141 → v142 + 4 gardiens. Captures avant/après + zoom
  envoyées (BE 153.23 et spot 180 enfin visibles). Suite 1984/2,
  RC GO.
- **Lot 132 — livré** : passe graphique n°7 — Opportunités : (a) la
  table des ANOMALIES perd ses chiffres nus — l'intensité devient
  une mini-barre de verre (dégradé warning via color-mix, échelle
  relative au max du scan) + valeur tabulaire ; (b) le CALENDRIER
  gagne l'IMMINENCE visuelle — tout événement à ≤ 7 jours porte un
  liseré warning et sa date en warning gras (dte réel earnings,
  écart de dates macro ; option `urgent` ajoutée au builder
  timelineCard). SW v140 → v141 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.
- **Lot 131 — livré** : passe graphique n°6 — Portefeuille/Risque :
  les barres des STRESS TESTS passent en matière VERRE (dégradé de
  leur propre couleur via color-mix sur tokens, doux au zéro → dense
  à l'impact) et le PIRE scénario est mis en avant (libellé négatif
  gras + halo + aria « pire scenario ») — le chiffre éducatif d'un
  stress test. Vue Performance vérifiée : états vides honnêtes en
  démo, jauge HHI et donut sectoriel héritent déjà du noyau.
  SW v139 → v140 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 130 — livré** : passe graphique n°5 — fiche Analyse : le bloc
  « Performance multi-horizons » (1 sem./1 mois/1 trim./1 an) passe
  en matière VERRE — chaque barre est un dégradé de sa propre
  couleur, doux au centre (zéro) → dense à l'extrémité de la valeur,
  construit par color-mix sur les tokens (aucun littéral nouveau).
  Reste de la fiche vérifié : radar, chandeliers+plan, runway,
  price-chart, timeline déjà au niveau. SW v138 → v139 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 126-130

5 lots (fin de 1re tournée + 4 passes noyau), suite constante
**1984 passed / 2 skipped**, PR #159 → #163, SW v134 → v139 :
jauge verre + libellés kv protégés + badge adaptatif (126) ·
heatmaps verre sur tokens — derniers rgba hors palette éliminés
(127) · donut à chiffre central éducatif (128) · rails sémantiques
rétablis + courbe des taux cyan + anti-collision endDots (129) ·
multi-horizons verre de la fiche Analyse (130). Deux BUGS visuels
réels tués : stats collées « Trades3 » (125) et rails invisibles
sous override noir !important (129). Le noyau graphique (barres,
jauges, heatmaps, donuts, lignes, aires, radar, treemap, entonnoir,
payoff) est désormais ENTIÈREMENT en grammaire verre sur tokens.

- **Lot 129 — livré** : passe graphique n°4 — **bug visuel réel
  corrigé** : les rails CALME↔STRESS et DÉFENSE↔ATTAQUE de Marchés
  étaient INVISIBLES (une règle neon-glass `background:rgba(0,0,0,.28)
  !important` écrasait le dégradé sémantique — vérifié au navigateur,
  backgroundImage:none) → override supprimé, dégradés rétablis.
  Courbe des taux US : « Actuelle » passe en cyan (elle se détache
  enfin de l'ombre grise de la veille). C.endDotsPlugin : anti-
  collision des noms de série (≥ 11 px d'écart — toutes les
  multiLine héritent). SW v137 → v138 + 4 gardiens. Captures
  avant/après envoyées (Volatilité + Macro). Suite 1984/2, RC GO.
- **Lot 128 — livré** : passe graphique n°3 — le donut gagne SON
  chiffre éducatif : la catégorie dominante et sa part (« 55 % /
  AVOID ») s'affichent au CENTRE de l'anneau, dans la couleur de son
  arc (plugin vxDonutCenter ; rien si total nul — aucune donnée
  inventée ; signature lot 53 intacte). Tous les donuts héritent.
  Tour des autres builders : anomaly-scan, équité/drawdown,
  sparkline déjà au niveau. SW v136 → v137 + 4 gardiens. Captures
  avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 127 — livré** : passe graphique n°2 — heatmaps matière VERRE
  (`C.heatmapCard`) : les DERNIERS rgba verts/rouges hors palette du
  système graphique remplacés par les tokens (convertis en rgb à
  l'exécution), chaque cellule devient une tuile de verre (dégradé
  diagonal de sa propre couleur, liseré inset, coins arrondis),
  grille aérée (border-spacing 3px). Héritent : matrice scénarios
  options (Stop/Flat/TP × temps), heatmap secteurs Marchés, P&L
  mensuel Portefeuille. Theta et sensibilité IV vérifiés — ils
  héritaient déjà des lots 120/125. SW v135 → v136 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 126 — livré** : amélioration graphique n°8 (Système) — **1re
  tournée esthétique TERMINÉE (8 pages / 8)**. Jauge `C.gauge` en
  matière VERRE (arc de valeur = dégradé de sa propre couleur, doux →
  dense, posé sur un halo large ; point de lecture avec halo — toutes
  les jauges héritent : Santé moteurs, Participation Marchés…) ;
  libellés clé/valeur protégés dans utilities.css (une valeur longue
  n'écrase plus le libellé en « Ét at » — gardien lot 57 respecté) ;
  badge des canaux en colonne adaptative (CONFIGURATION_MISSING
  s'affiche entier). Aucun littéral couleur nouveau. SW v134 → v135
  + 4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 121-125

5 lots graphiques (directive esthétique maximale), suite stable
**1984 passed / 2 skipped**, PR #154 → #158, SW v129 → v134 :
entonnoir monochrome + scatter teinté (Opportunités) · radar radial
(Analyse) · treemap verre (Portefeuille) · payoff breakeven/spot
(Options) · barres verre + stats stylées (Journal). Grammaire
commune installée : dégradé dense → doux de la propre couleur de
l'objet, liseré fin, UN chiffre éducatif par graphique, tokens
uniquement. Reste : Système (lot 126), puis nouvelles passes
(scénarios options, vol cone, heatmaps, gauges…).

### MINI-BILAN tournée 91-95

5 lots, 36 tests, suite 1771 → 1807, **1 défaut réel de moteur corrigé**
(committee : fenêtre « DANS LA ZONE D'ACHAT » = code mort → s'ouvre
enfin), skyler_core jamais touché : decide figé (9) · committee défaut
réel + 9 · pivots figé (8) · contrat POST figé (4) · filtres durs
options figés (6).

### MINI-BILAN tournée 86-90 — « moteurs blindés » COMPLET

5 lots, 46 caractérisations nées vertes, suite 1725 → 1771, 0 ligne de
logique modifiée, fichiers runtime jamais touchés. Toute la chaîne
« données → preuves (evidence) → décision (stack) → affichage
(recommendation/__VXVOCAB) → auto-notation (track_record) → persistance
(persist) → états (connections) » est figée par la suite : tout
changement futur de sémantique cassera les tests.

### MINI-BILAN tournée 81-85

Polices auto-hébergées (0 requête externe prouvé) · offline RÉEL
corrigé (défaut MAJEUR : le shell canonique n'enregistrait jamais le
service worker) · 26 contrôles interactifs 0 inerte · cycle desk 6/6
sans perte possible · alertes+SSE 4/4 sains. Suite 1714 → 1725,
SW v125 → v127, 4 outils d'audit rejouables versionnés dans tools/.

## Index des lots

Voir `docs/refactor/validation/SKYLER-INDEX.md` — tableau complet 10 → 23.

## Programme Institutional+ — TERMINÉ (RC sur intégration)

Les 12 lots + audit sont livrés sur `integration/vertex-skyler-v2`.
Verdict RC : **GO AVEC RÉSERVES** — voir `SKYLER-LOT-12.md` §11.

## Prochaine action unique

Validation humaine de la RC sur appareil physique (TWS réel, pages, iPhone).
Ensuite, avec accord explicite UNIQUEMENT, merge `integration/vertex-skyler-v2`
→ `main`.

**Arrêt — validation humaine requise.**

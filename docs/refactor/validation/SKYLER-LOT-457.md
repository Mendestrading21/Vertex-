# SKYLER LOT 457 — « Actions 10 / 10 — complet, remplacement obligatoire » : le portefeuille affiche la limite de la Constitution **V1** alors que le produit tourne sur la **V2**, qui en autorise 15 — et la bonne borne est affichée trois cartes plus bas

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-457` (base : lot 456 fusionné,
52baeb8)

Trente-huitième lot de la veine, septième de la tranche 450-459. Le 456 avait
ouvert la famille des **fractions affichées** et laissé **7 sur 12 non tracées**,
nommées et exclues de tout total. Ce lot **solde la dette** — modèle 449/455.

**Aucun code, aucun gardien, aucun test.**

## Les 7 dernières, tranchées

```text
fraction affichée                         producteur                       verdict
sm.beats / sm.total        /analysis      analyst_deep.py:110              SAINE (nuance nommée)
diag.ai.ok / diag.ai.total vx-shell.js    ai/audit.py:29-34                SAINE
b.points / b.max           /analysis      skyler_core.py:232 + profil      SAINE
p.v / p.max                options-struct options-structure.js:337-343     SAINE (barème)
rating_mean / 5            /analysis      company.py:236 recommendationMean SAINE (échelle 1-5)
favorable / pts.length     options-struct options-structure.js:213         SAINE (même tableau)
CALLS·PUTS / 1 max         /portfolio     portfolio_page.py:265-271        ► voir ci-dessous
```

**Six sur sept sont saines**, et elles le sont pour la même raison : numérateur
et dénominateur sont posés **dans le même objet** ou dérivés de **la même liste**.
`b.points/b.max` mérite sa preuve : `mx = cfg.get(name, 0)` avec
`cfg = profil.skyler_score.blocks` — mesuré, le profil porte bien les 8 blocs et
**leur somme fait exactement 40**, le dénominateur du score affiché.

**La nuance, nommée et NON classée** : dans `analyst_deep`, `total` s'incrémente
pour chaque trimestre publié, mais `beats` exige `surp is not None`. Un trimestre
dont la surprise est inconnue **compte au dénominateur sans jamais pouvoir
compter au numérateur**. C'est la forme du 455 — mais ici elle est **honnête** :
un trimestre non mesurable n'est pas un trimestre battu. Je le nomme et **je ne
le classe pas**.

## La trouvaille : trois dénominateurs sur une carte, deux exacts, un périmé

`portfolio_page.py:265-271` affiche trois limites en dur :

```javascript
cell('Actions', stocks.length + ' / 10',
     stocks.length >= 10 ? 'complet — remplacement obligatoire' : 'places disponibles', …)
cell('Options tactiques', opts.length + ' / 3',
     `CALLS ${…} · PUTS ${…} / 1 max`, …)
```

Confrontées à la Constitution réellement chargée (`load_profile()` → `strategy_id
= vertex_strategy_v2`) :

```text
affiché         Constitution V2 (celle que le produit charge)          verdict
« / 3 »         max_simultaneous_options            = 3                EXACT
« 1 max »       max_simultaneous_bearish_positions  = 1                EXACT
« / 10 »        portfolio_target_positions {min 8, max 15}             FAUX — c'est 15
```

**Deux dénominateurs sur trois sont exactement ceux de la Constitution.** C'est le
témoin positif le plus serré possible : il est **sur la même carte**, écrit par le
même auteur, dans le même geste. L'instrument n'accuse pas la carte en bloc — il
désigne **une** valeur.

### D'où vient le 10 : c'est la limite de la V1

```text
tests/test_constitution_v2.py:24   load_profile(version=1) → max_positions == 10
tests/test_constitution_v2.py:69   load_profile()          → max_positions == 15
C.list_versions() = [1, 2] · load_profile() par défaut = vertex_strategy_v2
```

**Le « / 10 » n'est pas une invention : c'est la borne de la Constitution V1,
restée figée dans l'interface quand les moteurs sont passés en V2.**

### Le banc : les deux cartes se contredisent sur la même page

`portfolio_context.build()`, moteur réel, positions fabriquées :

```text
 n  | moteur : in_bounds · places libres | carte « Lignes »      | carte KPI « Actions »
  7 | False  ·  8                        | sous la cible         | 7 / 10 · places disponibles
  8 | True   ·  7                        | dans les bornes       | 8 / 10 · places disponibles
  9 | True   ·  6                        | dans les bornes       | 9 / 10 · places disponibles
 10 | True   ·  5                        | dans les bornes       | 10 / 10 · COMPLET        ← CONTRADICTION
 12 | True   ·  3                        | dans les bornes       | 12 / 10 · COMPLET        ← CONTRADICTION
 15 | True   ·  0                        | dans les bornes       | 15 / 10 · COMPLET        ← CONTRADICTION
 16 | False  ·  0                        | au-dessus de la cible | 16 / 10 · COMPLET
```

**Les deux cas sains tombent juste** : à 7 les deux cartes disent « il reste de la
place », à 16 les deux disent « au-dessus ». La contradiction n'apparaît que dans
la **fenêtre 10-15** — exactement l'écart entre les deux Constitutions.

### Et la bonne borne est déjà à l'écran

`portfolio_page.py:966` rend, dans la carte voisine :

```javascript
<span class="vx-chart-question">${b.min}-${b.max} lignes cibles · plafond 15 % par titre …</span>
```

avec `b = d.bounds`, servi par le moteur : **`{min: 8, max: 15}`**. La page
**affiche donc « 8-15 lignes cibles » trois cartes sous un KPI qui déclare le
book complet à 10.**

C'est la famille 433 aggravée : l'information honnête n'est pas seulement *déjà
calculée*, elle est **déjà affichée**.

## Classement — rang 1

Ce n'est pas une étiquette approximative : c'est une **consigne d'action fausse**.
À 10 lignes, le terminal dit « **complet — remplacement obligatoire** », c'est-à-dire
*pour acheter, il faut d'abord vendre*, alors que la stratégie que l'utilisateur
suit autorise **cinq lignes de plus**. Le défaut **change une décision**, il est
**affiché en KPI de tête**, et il est **contredit par la même page**.

Correction pressentie : lire `d.bounds.max` — **déjà reçu par la page** — au lieu
du littéral. **Aucun GO, rien n'est engagé.**

**Le gardien existe et il est vert** : `tests/test_constitution_v2.py:69` vérifie
`portfolio_max_positions == 15` **côté profil**. **Aucun test ne compare le
littéral de la page au profil chargé** — périmètre qui s'arrête avant l'interface,
motif 381/385/414/415.

### Une réserve que je pose franchement

Le KPI compte `stocks = rich.filter(t => t.type === 'STK')`, tandis que le moteur
compte **tous** les symboles ouverts. Les deux numérateurs ne portent donc pas
exactement sur le même ensemble si le book contient des options. **Cela ne sauve
pas le dénominateur** : 10 n'est la borne d'aucune des deux lectures sous la V2,
et la page affiche elle-même 8-15. Je le dis pour que le résultat ne soit pas
sur-lu.

## L'état de la veine

```text
fractions affichées relevées dans les 42 objets servis      12
   tranchées au 456                                          5   (2 plafonnées, 3 saines)
   tranchées ici                                             7   (1 défaut, 6 saines)
   ────────────────────────────────────────────────────────────
   12 / 12 — VEINE DES FRACTIONS AFFICHÉES REFERMÉE
```

Bilan de la veine : **1 rang 1** (la borne V1 figée), **1 rang 2** (le plafond de
200 du 456), **1 rang 3** (le camembert constant), **1 rang 4 par lecture**
(`symbols_usable` plafonné à 30), **8 fractions saines**. Deux lots, quatre
défauts, et un taux de saines qui montre que l'instrument ne crie pas au loup.

## Portée

- La dette du 456 sur `gex_scan` **reste ouverte** : je n'ai pas tenté un
  troisième banc, le lot ayant trouvé ailleurs. Elle reste **rang 4 par lecture**.
- Le banc appelle le **moteur réel** sur des positions **fabriquées** : il
  établit le comportement du **code**, pas la taille réelle du book de
  l'utilisateur. Ce qu'il établit sans ambiguïté, c'est que **la contradiction
  occupe toute la fenêtre 10-15**.
- Les deux limites options sont vérifiées **par lecture du profil chargé**, pas
  par un banc — il n'y a rien à exécuter, la valeur est une constante du JSON.
- **Aucun navigateur ouvert.** La co-visibilité des deux cartes est établie sur
  la source servie (`portfolio_page.py:266` et `:966`), pas observée au rendu.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `portfolio_context.build()` et `constitution.load_profile()`
  appelés en mémoire ; `persist` redirigé ; **`/options/<sym>`, `/api/analyst/` et
  `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixantième lot court, septième de la tranche.

Le 455 avait montré qu'une veine se solde parfois sur son défaut le plus grave ;
**le 457 le confirme une seconde fois** — sept lignes à trancher, six saines, et
la dernière portait le premier rang 1 depuis le 452.

Le fait de méthode le plus utile est ailleurs : le témoin positif était **dans la
carte elle-même**. Trois dénominateurs, deux exacts, un faux. Sans les deux
exacts, j'aurais mesuré « la page invente ses limites » ; avec eux, la mesure
désigne **une valeur, une ligne, une version périmée** — et rend la correction
évidente.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **25** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**

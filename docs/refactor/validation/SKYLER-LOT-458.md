# SKYLER LOT 458 — Les littéraux de l'interface contre la Constitution : l'échelle de conviction est copiée à la valeur près, mais le classeur de catégories d'options est **aveugle au type** et ne connaît que 3 des 5 catégories

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-458` (base : lot 457 fusionné,
bff3d92)

Trente-neuvième lot de la veine, huitième de la tranche 450-459. Le 457 a trouvé
une **limite de configuration périmée figée dans l'interface**. Ce lot applique la
règle 455 → 456 : **désigner la famille suivante par la forme du défaut trouvé**
— *un littéral de l'interface qui duplique une valeur du profil de stratégie*.

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, décidé AVANT de mesurer

Le profil V2 contient **126 valeurs numériques**, **49 distinctes**. Chercher
chacune en dur dans les 42 objets servis produirait un total massivement
contaminé : `2`, `3`, `5`, `15`, `50`, `100` apparaissent partout par
coïncidence.

**Règle posée avant la première mesure : ne retenir que les valeurs à CHEMIN
UNIQUE dans le profil** — celles dont le sens n'est pas ambigu.

```text
valeurs numériques du profil V2                    126
valeurs distinctes                                  49
   à chemin UNIQUE, retenues                        21
   à chemins MULTIPLES, EXCLUES et nommées          28
      0.3 · 1 · 2 · 3 · 4 · 5 · 6 · 8 · 10 · 12 · 15 · 20 · 24 · 25 · 28 · 30
      35 · 40 · 50 · 60 · 70 · 75 · 80 · 90 · 100 · 180 · 210 · 540
```

Les 28 exclues **ne sont comptées dans aucun total** (règle 448) : leur sens
n'est pas décidable par le nombre seul.

Sur les 21 retenues, **19 apparaissent** dans les octets servis, **2 non**
(`-25` = `portfolio_max_drawdown_pct`, `0.9` = `LEAPS.delta_max`).

### Les coïncidences, écartées après lecture du contexte

Sur les 19 présentes, **8 sont des homonymes purs** — vérifié en lisant chaque
occurrence : `7` (134 occurrences : largeurs, indices), `120`/`240` (pixels de
graphique), `150`/`200`/`365`/`500` (hauteurs, bornes de buckets), `-20`
(bornes d'histogramme du journal), `31` (coordonnée SVG). **Nommées, écartées,
non comptées.**

Restent **11 valeurs décidables** : six deltas et cinq seuils de conviction.

## Témoin positif n°1 — l'échelle de conviction est copiée à la valeur près

`portfolio_page.py:185-189` :

```javascript
const n = sc <= 40 ? sc : Math.round(sc / 2.5);
if (n >= 36) return {tier:'S+', max:15};
if (n >= 32) return {tier:'S',  max:10};
if (n >= 28) return {tier:'A',  max:5};
return              {tier:'B',  max:2};
```

Contre `conviction_levels` du profil chargé :

```text
palier   score_min profil   seuil affiché    allocation_pct profil   plafond affiché
S_PLUS         36               36                [10, 15]                15      EXACT
S              32               32                [ 7, 10]                10      EXACT
A              28               28                [ 3,  5]                 5      EXACT
B              24 (refus <24)    —                [ 1,  2]                 2      EXACT
                                        8 valeurs sur 8 : CONCORDANTES
```

**Huit valeurs de la Constitution, recopiées exactement — sur la page même où le
457 a trouvé une borne périmée.** C'est le témoin qui rend le lot lisible :
l'interface duplique la Constitution **correctement la plupart du temps**.

## Témoin positif n°2 — trois bornes de delta sur cinq sont verbatim

`opportunities_page.py:475-477`, rendu dans la colonne **« Catégorie »** du
tableau options :

```javascript
function catOf(c){ const d = Math.abs(c.delta || 0);
  if (d >= 0.40 && d <= 0.60) return 'BALANCED';
  if (d >= 0.28 && d <  0.45) return 'DYNAMIC';
  if (d >= 0.18 && d <  0.30) return 'ULTRA_CONVEX';
  return 'AUTRE'; }
```

`0.40/0.60`, `0.28/0.45`, `0.18/0.30` sont **exactement** les
`delta_min`/`delta_max` de BALANCED, DYNAMIC et ULTRA_CONVEX. Rien n'est inventé.

## La trouvaille : le classeur ignore le TYPE et ne connaît que 3 catégories sur 5

**Reproduction du prédicat servi** (trois comparaisons recopiées — **une
reproduction, pas une exécution de la page**, règle 443), appliquée aux bornes de
la Constitution elle-même :

```text
catégorie du profil   delta du profil   étiquette rendue par la page
BALANCED                0.40–0.60       BALANCED                       CONCORDE
DYNAMIC                 0.28–0.45       BALANCED / DYNAMIC             ← DIVERGE
ULTRA_CONVEX            0.18–0.30       DYNAMIC / ULTRA_CONVEX         ← DIVERGE
LEAPS                   0.70–0.90       AUTRE                          ← DIVERGE
BEARISH_TACTICAL        0.30–0.55       BALANCED / DYNAMIC             ← DIVERGE
```

Trois faits, mesurés :

**1. Les catégories de la Constitution SE CHEVAUCHENT** (BALANCED 0.40-0.60,
DYNAMIC 0.28-0.45, BEARISH_TACTICAL 0.30-0.55). Un classeur **fondé sur le seul
delta ne peut donc pas** reproduire la taxonomie : aux bords, c'est l'ordre des
`if` qui décide. Ce n'est pas un bug d'implémentation, c'est une **grandeur
insuffisante**.

**2. Le prédicat ignore le type du contrat.** `Math.abs(c.delta)` — et pourtant
`c.type` **est dans le même objet** : `legacy_engine.py:291` écrit
`'type': direction.upper()`. Conséquence mesurée :

```text
put  delta −0.45  →  « BALANCED »
call delta  0.45  →  « BALANCED »        même étiquette, direction opposée
put  delta −0.25  →  « ULTRA_CONVEX »
```

Or la Constitution pose `primary_direction: LONG_CALL`,
`target_call_share_pct: 90`, et une catégorie **BEARISH_TACTICAL** distincte,
`frequency: RARE`, `max_simultaneous_bearish_positions: 1`. **Étiqueter un put
« BALANCED » range une position baissière rare dans la catégorie haussière par
défaut.**

**3. Le board CONTIENT des puts.** `legacy_engine.build_board()` sélectionne
`sells = [r for r in rows if r['verdict'] == 'AVOID']` puis
`best_for_symbol(..., 'put', ...)`. La branche est donc **atteignable** dès qu'un
titre du scan est en AVOID.

### Classement — rang 2

C'est une **étiquette fausse affichée** dans une colonne de tableau, sur une page
servie, alors que **l'information qui la corrigerait est dans le même objet**.
Ce n'est pas un chiffre faux, et rien n'est inventé : les trois bornes recopiées
sont exactes. C'est une **taxonomie amputée et aveugle à la direction**.

Correction pressentie : ajouter le type au prédicat et les deux catégories
manquantes — ou renommer la colonne pour ce qu'elle mesure vraiment, une **bande
de delta**. **Aucun GO, rien n'est engagé.** Aucun test ne compare le classeur de
la page aux catégories du profil : **aucun gardien.**

### Ce que je n'ai PAS établi

**Qu'un delta ≥ 0.70 atteigne réellement ce board.** `best_for_symbol` filtre par
**moneyness du strike** — calls entre 0,98× et 1,18× le spot — ce qui **exclut le
deep-ITM**, donc probablement les deltas LEAPS. La branche « AUTRE » pourrait
être rare ou inatteignable pour les calls. **Je ne le tranche pas** (règle
442/445 : une étiquette fausse sur une branche inatteignable n'est pas un
mensonge à l'écran). **Le cas du put, lui, est atteignable** — établi par lecture
du producteur, le board étant vide au démarrage.

## La réponse à la question du réveil

**Le 457 n'était pas isolé en GENRE, mais il l'est en GRAVITÉ.**

```text
valeurs de la Constitution dupliquées dans l'interface et VÉRIFIÉES
   concordantes    14   (8 de l'échelle de conviction + 3 bornes de delta ×2)
   divergentes      1   la borne de positions du 457 (10 au lieu de 15)
   taxonomie incomplète, non chiffrée   1   le classeur de catégories (458)
```

**L'interface recopie la Constitution correctement dans 14 cas mesurés sur 15.**
Le rang 1 du 457 reste donc un **relief isolé**, pas la pointe d'un massif — et
c'est un résultat qui **borne** le dossier plutôt qu'il ne l'élargit.

## Portée

- **28 valeurs sur 49 sont exclues d'emblée** et nommées : leur sens n'est pas
  décidable par le nombre. **Aucun total ne les inclut.**
- **8 coïncidences écartées après lecture** du contexte, nommées une par une.
- Le classeur est **reproduit**, pas exécuté : les trois comparaisons sont
  recopiées à l'identique des octets servis, et je le dis.
- L'atteignabilité de la branche « AUTRE » n'est **pas établie** ; celle du
  mauvais étiquetage des puts l'est **par lecture du producteur**, pas par
  exécution.
- **Aucun navigateur ouvert.** La colonne « Catégorie » est établie sur les
  octets servis (`opportunities_page.py:489`, `${catOf(c)}` dans un `vx-badge`).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `constitution.load_profile()` appelé en mémoire ; routes
  en **GET** ; `persist` redirigé ; **`/options/<sym>`, `/api/analyst/` et
  `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante et unième lot court, huitième de la tranche.

Le lot fait deux choses, et la seconde compte davantage. Il trouve un **rang 2** —
une colonne qui range un put baissier dans une catégorie haussière alors que le
type est dans le même objet. Et il **borne le rang 1 du 457** : sur quinze
valeurs de Constitution dupliquées dans l'interface et vérifiées, **quatorze
concordent**. La divergence d'hier était un accident de version, pas une pratique.

Le fait de méthode : **le calibrage a été posé avant la première mesure**, et
c'est lui qui rend le lot publiable. Sans la règle « chemin unique seulement »,
les 49 valeurs auraient rendu des centaines de coïncidences et un total
contaminé — exactement ce que le 437 interdit.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **25** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**

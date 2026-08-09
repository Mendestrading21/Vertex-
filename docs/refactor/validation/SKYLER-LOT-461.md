# SKYLER LOT 461 — La carte « Risque dominant » de `/portfolio` déclare « Aucun risque critique détecté » entre 15 % et 25 % de concentration — alors qu'elle cite elle-même le repère de 15 % et que deux cartes voisines sont déjà en alerte

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-461` (base : lot 460 fusionné,
cd38953)

Quarante et unième lot de la veine, premier de la tranche 460-469. Le bilan n°15
a recommandé **(a)** : continuer les lots de mesure en désignant la famille
suivante par la forme du dernier défaut trouvé. Le 458/459 avait nommé une
**taxonomie amputée et aveugle à une dimension** ; ce lot attaque **la classe
entière des CLASSEURS SERVIS**.

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure (règle 458)

**CLASSEUR SERVI** = un fragment de code servi qui, à partir d'au moins **une
comparaison numérique contre un littéral**, rend **au moins deux étiquettes
textuelles distinctes** destinées à l'affichage.

**Quatre formes reconnues** (leçon 454 : un détecteur à une seule forme ment) :
déclaration `function`, affectation `= function`, flèche à corps `=> {…}`,
flèche à expression `=> cond ? 'X' : 'Y'`.

**Exclus d'emblée, nommés, comptés dans AUCUN total** : ce qui rend une couleur,
un token ou une classe CSS (habillage, pas taxonomie) · ce qui rend un nombre ·
les tables de correspondance sans comparaison numérique · les classeurs sur une
**chaîne** (`=== 'BUY'`), qui ne sont pas des seuils.

## Trois corrections d'instrument — et la première était un ZÉRO FAUX

Le calibrage ne suffit pas : l'instrument a menti trois fois avant de dire vrai.
**Le contrôle qui les a toutes révélées : exiger que le détecteur retrouve le cas
CONNU du 458 (`catOf`).** Il ne le retrouvait pas.

```text
#   défaut de l'instrument                          effet mesuré
1   `return\s+` exigeait un ESPACE après return     les octets servis écrivent
                                                    `return'BALANCED'` → le cas du
                                                    458 était INTROUVABLE, zéro faux
2   les `return` des fonctions IMBRIQUÉES étaient   50 candidats dont ~30 faux
    attribués à la fonction PARENTE                 (piège 453, la fenêtre qui
                                                    avale un autre receveur)
3   plafond de 44 puis 60 caractères par étiquette  `winnerRule` (étiquettes de
                                                    ~78 caractères) SILENCIEUSEMENT
                                                    absent de la population
```

Le n°3 est le plus instructif et c'est la **leçon du 459 qui se répète** : une
**borne d'instrument** — ici la longueur maximale d'une étiquette — décidait de
la population mesurée, et rien ne le signalait. Il a fallu chercher `winnerRule`
**nommément** pour découvrir qu'il manquait.

**Trois faux arrêtés avant publication. Total : 26 → 29.**

## La population, après correction

```text
corpus : 42 objets servis · 841 916 caractères
détecteur final                                    28 candidats
   RETENUS comme classeurs                          13
   EXCLUS, nommés, dans aucun total                 15
```

Les 15 exclus, nommés : `confl` (classeur sur chaîne), `brCls`, `cellStyle`
(classes CSS), `fmtDelta`, `pct`, `sessAge` (formatage), `monotonePath`,
`sparkArea`, `rrLadder` (chemins SVG), `macroCard`, `rowHtml` (gabarits HTML),
`C.donut`, `C.sparkline` (configuration de graphique), `loadSkyler` (chargeur),
`tickerMatches` (recherche).

## Le verdict, classeur par classeur — et il BORNE le 458

```text
classeur              objet servi        grandeurs lues                      verdict
bucketOf              /opportunities     verdict + rr_ok + score             SAIN
tierOf                /opportunities     bucketOf + score                    SAIN
tierOf                /portfolio         score  (8/8 conforme, cf. 458)      SAIN
roleOf                /portfolio         type + score + verdict + liste      SAIN
thesisState           /portfolio         mark + stop + pl + confirmation     SAIN
nextAction            /portfolio         thesisState + pl + confirmation     SAIN
liqState              options-structure  oi + spread                         SAIN
computeVerdict        options-structure  liq + asym + prime + dte            SAIN
optNextAction         options-structure  pl + confirmation                   SAIN
────────────────────────────────────────────────────────────────────────────────
catOf                 /opportunities     |delta| SEUL — `c.type` ignoré      aveugle (458)
catOf2                /opportunities     idem, SECOND site non signalé       aveugle (458)
winnerRule            /portfolio         pl SEUL — le type est perdu à       rang 3
                                         l'appel `winnerRule(t.pl)`
dominantRisk          /portfolio         multi-dimensions, mais SEUIL CITÉ   RANG 2
                                         ≠ SEUIL APPLIQUÉ
```

**Neuf classeurs servis sur treize sont sains.** L'aveuglement au type trouvé au
458 touche **deux sites** — le même prédicat, dupliqué — et non une pratique
générale. **C'est un bornage**, du même type que celui que le 458 avait posé sur
le 457.

**Fait neuf, petit mais net** : le prédicat du 458 existe en **deux exemplaires**
dans les octets servis de `/opportunities` — `catOf` (colonne « Catégorie ») et
`catOf2`, recopié à l'identique dans `window.__opCompare`. Le 458 n'en signalait
qu'un.

## La trouvaille : un classeur qui CITE un seuil et en APPLIQUE un autre

`portfolio_page.py:216-226`, rendu en **KPI de tête** (`:324-326`, encart
« **Risque dominant** ») :

```javascript
if(m.top1 && m.top1.w > 25)
  return {label:`Concentration élevée : ${m.top1.sym} = … % du portefeuille`,
          detail:'au-delà d’un repère prudent (~15 % pour un titre)', tone:'warn'};
…
return {label:'Aucun risque critique détecté',
        detail:'concentration et invalidations dans les repères', tone:'muted'};
```

**Le prédicat se déclenche à 25. Le repère que sa propre phrase invoque est 15.**
La Constitution réellement chargée (`load_profile()` → `vertex_strategy_v2`) pose
`max_stock_weight_pct = 15.0`.

### Reproduction des trois prédicats servis (règle 443 — recopiés, pas exécutés)

```text
poids Top 1 |  KPI « Concentration »  |  carte « Discipline V2 »  |  carte « RISQUE DOMINANT »
     14,9 % |  POSITIVE               |  sous le plafond          |  Aucun risque critique détecté
     15,0 % |  WARNING                |  sous le plafond          |  Aucun risque critique     ← CONTRADICTION
     16,0 % |  WARNING                |  > plafond 15 % (rouge)   |  Aucun risque critique     ← CONTRADICTION
     20,0 % |  WARNING                |  > plafond 15 % (rouge)   |  Aucun risque critique     ← CONTRADICTION
     25,0 % |  WARNING                |  > plafond 15 % (rouge)   |  Aucun risque critique     ← CONTRADICTION
     25,1 % |  NEGATIVE (halo)        |  > plafond 15 % (rouge)   |  Concentration élevée : 25 %
     45,0 % |  NEGATIVE (halo)        |  > plafond 15 % (rouge)   |  Concentration élevée : 45 %
```

**Fenêtre exacte de la contradiction, au pas de 0,1 point : 15,0 % → 25,0 %.**
Les deux cas sains encadrent juste : à 14,9 % les trois éléments s'accordent, à
25,1 % aussi.

### Ce qui rend le résultat serré : la contradiction porte sur UNE MÊME valeur

Le KPI « Concentration » (`:349`) et la carte « Risque dominant » (`:222`) lisent
**la même expression, `m.top1.w`**, calculée une seule fois par `computeMetrics`.
Dans la fenêtre 15-25, l'une passe en **WARNING** avec la légende « repère
~15 % » pendant que l'autre écrit « **Aucun risque critique détecté** —
concentration … **dans les repères** ». Il n'y a ici **aucune question de
dénominateur** : c'est le même nombre, lu au même instant, par deux prédicats de
la même page.

La troisième carte (« Discipline du portefeuille (Constitution V2) », `:964-969`,
`topOver = top_weight_pct > 15` → « **> plafond 15 %** » en rouge) **corrobore**,
mais elle lit une grandeur **serveur** distincte (`portfolio_context`). Je la cite
comme corroboration et **pas** comme preuve — leçon 458 : *un même nombre n'est
pas une même grandeur.*

### Classement — rang 2, et je dis pourquoi pas rang 1

Ce qui plaide pour le **rang 1** : c'est un **KPI de tête**, il énonce une
**absence de risque** qui est fausse dans toute la fenêtre, et il contredit le
plafond que la Constitution impose et que la page affiche elle-même.

Ce qui l'en empêche, et je le retiens : **l'utilisateur n'est pas laissé sans
signal** — le KPI voisin est déjà jaune et la carte Discipline déjà rouge dans la
même fenêtre. Le défaut est une **fausse quiétude en tête d'écran**, pas une
consigne d'action fausse comme celle du 457. **Rang 2.**

Correction pressentie : comparer à `max_stock_weight_pct` — déjà calculé par
`portfolio_context.py:64` — ou, à défaut, au littéral 15 déjà employé deux fois
sur la même page. **Aucun GO, rien n'est engagé.**

**Aucun gardien** : `dominantRisk` n'apparaît dans **aucun test**.
`max_stock_weight_pct` est vérifié côté profil (`test_constitution.py`) et côté
moteur (`test_risk_engine_lot165.py`, qui **avertit dès 15 %**), jamais contre le
littéral de la page — périmètre qui s'arrête avant l'interface, motif
381/385/414/415/457.

## Le rang 3 : la même échelle de gains, deux formulations, le type perdu à l'appel

`/portfolio` applique `nextAction(t)` à **toutes** les lignes, options comprises,
et délègue à `winnerRule(t.pl)` — qui ne reçoit **qu'un nombre**. Le type est
dans l'objet de l'appelant et n'est pas transmis. `/options` a un frère
**conscient du type**, `optNextAction`.

```text
P&L    /portfolio (winnerRule)                          /options (optNextAction)
 +60 % « relever le STOP SOUS LE PRIX, réévaluer »      « conserver tant que thèse et
                                                          catalyseur tiennent »
 +35 % « verrouiller le risque (STOP au-dessus du       « réévaluer invalidation et
         prix moyen) »                                    risque de temps »
```

**Les cinq paliers sont identiques** (20/30/50/75/100) : rien n'est faux, et je ne
gonfle pas. Ce qui diffère, c'est que la ligne d'une **option** reçoit sur
`/portfolio` une consigne rédigée pour une **action** — un stop sous le prix —
alors qu'une version adaptée existe ailleurs dans le produit. **Rang 3.**

## Ce que le lot ne prétend pas

- Les prédicats sont **reproduits, pas exécutés** : les comparaisons sont
  recopiées à l'identique des octets servis, la page n'est pas rendue.
- La carte « Risque dominant » teste **d'abord** les invalidations : la fenêtre
  15-25 ne s'observe que **si aucune position n'est cassée**. Je le dis, la
  branche concentration est la **deuxième**.
- Le rapprochement avec la Constitution porte sur une grandeur **client**
  (`m.top1.w`, poids sur la valeur brute des positions, cash exclu) et une règle
  **serveur** exprimée en pourcentage de portefeuille. **La contradiction que je
  publie comme prouvée est INTRA-PAGE, sur une valeur identique** ; le
  rapprochement à la Constitution est une corroboration.
- La population de 13 classeurs vaut **pour les quatre formes détectées**. Un
  classeur bâti par un helper ou par une table de seuils **échapperait** —
  **non quantifié**.
- `roleOf` porte une **liste de six tickers défensifs en dur** (`XLU`, `XLP`,
  `BIL`, `SGOV`, `SHV`, `GLD`) sans source de configuration : **mesuré, il n'en
  existe aucune** dans `vertex/strategy`. Je le **nomme** — ce n'est pas une
  contradiction prouvée, je ne le classe pas.
- **Aucun navigateur ouvert.**

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

Soixante-quatrième lot court, premier de la tranche 460-469.

La famille désignée par le bilan a payé **au premier lot** : un **rang 2**, un
**rang 3**, un **site supplémentaire** du défaut du 458 — et surtout un **bornage
franc**, neuf classeurs sains sur treize. La chaîne de relais tient une cinquième
fois ; je rappelle la réserve du bilan n°15 : **la famille m'a été proposée dans
l'orientation de réveil, je ne l'ai pas trouvée seule.**

Le fait de méthode est le même qu'au 459, et il commence à être une **règle** :
**une borne d'instrument décide de la population mesurée.** Trois fois de suite
mon détecteur a rendu une population fausse — un espace manquant, une fenêtre
trop large, un plafond de caractères — et **c'est le contrôle par un cas CONNU
(`catOf`) qui l'a révélé à chaque fois**. Un détecteur qui ne retrouve pas le
défaut d'hier ne mesure rien aujourd'hui.

Genre neuf pour la nomenclature : **UN CLASSEUR QUI CITE UN SEUIL ET EN APPLIQUE
UN AUTRE.**

Comptes séparés : résultats faux **arrêtés avant publication** **29** (+3) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**

# SKYLER LOT 468 — Les seuils décisionnels contre la Constitution : dix-neuf valeurs concordent, aucune divergence NEUVE — et la vraie trouvaille est que la moitié des seuils des classeurs n'a AUCUNE source de configuration

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-468` (base : lot 467 fusionné,
579d6b9)

Quarante-huitième lot de la veine, huitième de la tranche 460-469 — et **dernier
lot d'ouverture** avant le solde du 469 et le bilan n°16 du 470. La veine des
routes est refermée sans dette ; ce lot ouvre **la seule piste de la liste jamais
ouverte** : les **seuils en dur des 13 classeurs du 461**, confrontés à leur
source de configuration.

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Le 462 a tranché les **phrases** qui citent un seuil (26/28 concordent). Ici ce
sont **les seuils eux-mêmes**, y compris ceux qu'aucune phrase ne cite.

**Critère décisif** — sans lui tout littéral entre et le total est contaminé
(leçon 458) :

```text
SEUIL DE STRATÉGIE     décide un VERDICT PRODUIT (limite de lignes, bande de
                       delta, score de conviction, plafond de poids, palier de
                       gain)  → DEVRAIT venir de la Constitution
SEUIL DE PRÉSENTATION  décide seulement COMMENT on montre (largeur, plafond
                       d'affichage, arrondi)  → aucune source attendue
                       → EXCLU, NOMMÉ, compté dans aucun total
```

**Deux passes**, parce qu'une seule ne voit qu'un côté : **A** config → code
(la limite du profil est-elle codée en dur, et concorde-t-elle ?) · **B** code →
config (le littéral du classeur a-t-il une clé ?).

**Verdicts** : SOURCÉ CONCORDANT · SOURCÉ DIVERGENT (défaut) · **NON SOURCÉ**
(le littéral **est** la source — le nommer est le résultat, pas un défaut en
soi) · PRÉSENTATION (exclu).

## Les deux contrôles obligatoires, sur des cas dont je connais la réponse (leçon 467)

```text
CONTRÔLE 1 — le cas du 457
   servi   cell('Actions', stocks.length + ' / 10', stocks.length >= 10 ? …)
   profil  portfolio_target_positions.maximum = 15
   →  SOURCÉ DIVERGENT retrouvé                                    OK

CONTRÔLE 2 — le cas du 458
   profil  S_PLUS 36 [10,15] · S 32 [7,10] · A 28 [3,5] · B 24 [1,2]
   servi   n>=36 → {tier:'S+',max:15} ; n>=32 → S,10 ; n>=28 → A,5 ; B,2
   →  SOURCÉ CONCORDANT retrouvé                                   OK
```

## Une correction d'instrument, attrapée par la passe A elle-même

La passe A a d'abord déclaré `max_simultaneous_bearish_positions` et
`target_call_share_pct` **« CLÉ ABSENTE »** — alors que le 457 les avait mesurées
à 1 et 90. **Mon chemin de lecture du profil était plat** ; les deux vivent sous
`.options_profile.` :

```text
.options_profile.max_simultaneous_bearish_positions = 1
.options_profile.target_call_share_pct              = 90
```

Un « absent » qui n'est qu'un chemin trop court. **Un faux arrêté avant
publication. Total : 39 → 40.**

## Ce que la mesure donne — dix-neuf concordances, deux divergences déjà connues

```text
SOURCÉ CONCORDANT                                              19 valeurs
   échelle de conviction (36/32/28 + 15/10/5/2)      8    tierOf /portfolio
   bandes de delta BALANCED/DYNAMIC/ULTRA_CONVEX     6    catOf, catOf2
   paliers de gain 30/50/75/100                      4    winnerRule, optNextAction
        ← .position_rules.winner_management.review_thresholds_gain_pct
   plancher d'open interest 500                      1    liqState
        ← .options_profile.categories.LEAPS.open_interest_min

SOURCÉ DIVERGENT                                                2 — TOUS DÉJÀ CONNUS
   « Actions n / 10 » vs maximum 15                       le 457
   dominantRisk > 25 vs max_stock_weight_pct 15           le 461
```

**Aucune divergence NEUVE.** Les deux seules sont celles que la boucle avait déjà
publiées, et elles ressortent **par le contrôle**, pas par surprise. **Dixième
bornage consécutif.**

Fait neuf, petit et net : sur les **cinq** paliers de gain servis, **quatre
concordent exactement** avec `review_thresholds_gain_pct = [30, 50, 75, 100]` —
**le palier « Gain ≥ +20 % » n'a aucune source.** Il a été ajouté à l'échelle
sans passer par la Constitution.

## La vraie trouvaille : la moitié des seuils n'est gouvernée par rien

```text
NON SOURCÉ — aucune clé n'existe pour ce concept dans TOUT le profil
   roleOf     liste de 6 tickers défensifs   XLU · XLP · BIL · SGOV · SHV · GLD
   computeVerdict  prime « > 12 % du notionnel »
   thesisState     proximité du stop  × 1,04  (bande de 4 %)
   computeVerdict  asymétrie  3 / 1,8 / 1,2
   liqState        gradations de spread  3 / 6 / 10 %
   winnerRule      le palier +20 %
```

**Pour ces six concepts, le littéral EST la Constitution.** Ils décident des
verdicts affichés — « Défense / gardien », « Structure intéressante mais chère »,
« Fragilisée — proche invalidation », « Asymétrie excellente », « Liquidité
acceptable » — et **aucun n'est versionné avec le profil, aucun n'est comparé à
lui par un test.**

Ce n'est **pas un mensonge à l'écran** : ces valeurs ne contredisent rien, elles
n'ont simplement pas d'autorité au-dessus d'elles. C'est une **surface de
décision hors Constitution**. **Rang 4**, et la valeur du lot est la mesure.

Le contraste est ce qui rend le résultat lisible : **là où une clé existe, le code
la respecte dix-neuf fois sur vingt et une.** Le problème n'est pas la
désobéissance, c'est **l'absence de loi** sur la moitié du terrain.

## Deux candidats que je ne classe PAS — et pourquoi

**`liqState` tolère un spread de 6 % là où la Constitution plafonne LEAPS à 5 %.**
`.options_profile.categories.LEAPS.spread_pct_max = 5.0` ; la page range à
« Acceptable » tout `spread ≤ 6`. **Mais les portées diffèrent** : la clé est
*par catégorie*, le classeur est *générique*. Leçon 458 — un même nombre n'est
pas une même grandeur. **Nommé, non classé.**

**`computeVerdict` ne signale une échéance courte qu'en dessous de 20 jours,
quand la Constitution pose un minimum ABSOLU de 60.** Sur le papier, une fenêtre
de quarante jours sans avertissement. **Sauf que `chain_loader.py:24` et
`contract_filter.py:18` filtrent déjà sur `[absolute_minimum, absolute_maximum]`
= [60, 540]** : un contrat à moins de 60 jours n'atteint probablement jamais le
board. **Je n'ai pas établi la chaîne de bout en bout** — la charge utile vient
de `multileg_lab`, qui ne refuse qu'un DTE négatif, alimenté par
`scan_state['options_board']` dont je n'ai pas prouvé le filtrage. **Règle
442/445 et modèle 456 : je le dis et je ne le classe pas.**

**Troisième fois dans cette tranche qu'un candidat sérieux meurt sur
l'atteignabilité** — après « cible 1 » (462) et l'alerte de démo (465). C'est
devenu le filtre dominant.

## Ce que le lot ne prétend pas

- La liste des **limites de stratégie** de la passe A est **fermée** (six clés).
  Une limite que je n'ai pas nommée échapperait. **Non quantifié.**
- La passe B part des **13 classeurs du 461** — elle hérite de leur périmètre :
  quatre formes de déclaration, aucun classeur bâti par un helper.
- `bucketOf` (72/66/56) et `tierOf` /opportunities (80) travaillent sur une
  échelle **/100** quand la Constitution est en **/40**. La conversion existe
  ailleurs (`sc<=40?sc:round(sc/2.5)`) mais **je n'ai pas prouvé que c'est la
  même grandeur** : **non tranché, non compté**.
- « Aucune clé n'existe » est établi par **balayage de tous les chemins du
  profil** sur une liste de mots-clés par concept. Une clé au nom inattendu
  échapperait.
- **Aucun banc, aucun moteur appelé** hors `load_profile()`. **Aucun navigateur.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `constitution.load_profile()` en mémoire ; pages en
  **GET** ; `persist` redirigé ; **aucun écrivain appelé** ; **`/options/<sym>`,
  `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante et onzième lot court, huitième et **dernier lot d'ouverture** de la
tranche.

Il ferme la dernière piste de la liste, et il la ferme **en négatif** : là où la
Constitution parle, le code l'écoute — **dix-neuf valeurs sur vingt et une** — et
les deux exceptions sont **déjà à l'ordre du jour depuis le 457 et le 461**.
**Dixième bornage consécutif.**

Ce que la mesure ajoute est d'une autre nature, et c'est ce que je retiens :
**six concepts décisionnels n'ont aucune autorité au-dessus d'eux.** Une liste de
six tickers décide de l'étiquette « Défense / gardien » ; un `1,04` décide qu'une
thèse est « fragilisée » ; un `12 %` décide qu'une structure est « chère ». Ces
valeurs sont peut-être excellentes — **je n'en juge pas** — mais elles ne sont ni
versionnées, ni testées, ni discutables au même endroit que le reste.

Genre neuf pour la nomenclature : **UN SEUIL QUI DÉCIDE SANS LOI** — un littéral
qui produit un verdict affiché alors qu'aucune configuration ne le gouverne.

Comptes séparés : résultats faux **arrêtés avant publication** **40** (+1) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**

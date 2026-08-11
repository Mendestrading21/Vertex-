# SKYLER LOT 459 — Les deux dettes de la tranche soldées PAR EXÉCUTION : le plafond du radar GEX monte au rang 2, la branche « AUTRE » est bel et bien atteignable — et ma borne d'atteignabilité a bougé trois fois avant que je la publie

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-459` (base : lot 458 fusionné,
e657e72)

Quarantième lot de la veine, **dernier lot de mesure de la tranche 450-459**. Un
dernier lot de tranche solde une dette au lieu d'ouvrir un front (modèle 449).
Deux dettes étaient ouvertes, toutes deux « **établies par lecture** » ; les deux
sont **soldées par exécution**, et elles vont **en sens opposés**.

**Aucun code, aucun gardien, aucun test.**

## Dette (i) — `gex_scan` du 456 : le banc tourne, et le verdict monte

Le 456 avait échoué **deux fois** à exécuter `gex_scan.scan()`. La cause, trouvée
en lisant le moteur — deux minutes, comme au 457 :

```text
gex_scan.py:29    la clé du board est `sym`            (j'écrivais `symbol`)
gex.py:142        l'open interest se lit `oi`          (j'écrivais `open_interest`)
```

**Banc, moteur réel, `top=30` — la valeur que la route passe** (`options_intel_api.py:133`) :

```text
board |  sans cap (top=None)   |  AVEC top=30
   10 |   10/ 10 exploitables  |   10/ 10      concordent
   29 |   29/ 29 exploitables  |   29/ 29      concordent
   30 |   30/ 30 exploitables  |   30/ 30      concordent
   31 |   31/ 31 exploitables  |   30/ 31   ← le plafond mord EXACTEMENT à 31
   45 |   45/ 45 exploitables  |   30/ 45
  120 |  120/120 exploitables  |   30/120
```

**La bascule tombe exactement au seuil annoncé** (règle 448), et les trois cas
sains tombent juste.

**Le plafond est-il atteignable ?** Oui, et c'est même le cas nominal :
`_publish_board()` (`terminal.py:1033-1044`) publie **FOCUS ∪ ROTATION**, et le
commentaire du cycle annonce couvrir « **tout l'univers optionable (~700 titres
US) … en quelques heures** ». Un board de plus de 30 sous-jacents est la
situation normale.

**Requalification : rang 4 « par lecture » → RANG 2, établi par exécution.** La
phrase servie « `X`/`Y` **titres exploitables** » présente, au-delà de 30, un
**plafond d'affichage** comme une mesure d'exploitabilité — même genre qu'au 456.

## Dette (ii) — la branche « AUTRE » du 458 : atteignable, et ma borne a bougé trois fois

Question : un delta ≥ 0,70 (bande LEAPS de la Constitution) peut-il figurer au
board, alors que `best_for_symbol` filtre par **moneyness** (calls 0,98–1,18 ×
spot) ?

Le seul sélecteur qui alimente le board est bien `best_for_symbol` — **focus**
(`terminal.py:1073`) **et rotation** (`:1586`). Delta calculé par le moteur réel
`legacy_engine._greeks` (Black-Scholes du dépôt).

### Trois grilles, trois réponses — et je publie les trois

```text
grille                                          delta call maximal   verdict
A. K/S ∈ {0.98…1.18}, dte ≤ 540, iv ≥ 0.20            0.684          « inatteignable »
B. pas de 0.004 sur K/S, iv ≥ 0.15                    0.715          atteignable, marginal
C. pas de 0.001 sur K/S, iv ≥ 0.10  (2 000 points)    0.781          ATTEIGNABLE
```

**La grille A m'aurait fait publier « inatteignable ».** C'était faux : il suffit
d'abaisser le plancher d'IV pour qu'un call **au money et à longue échéance**
franchisse 0,70. Sur la grille C, **40,3 % de la bande LEAPS (0,700-0,781) est
atteignable**.

**Leçon, et elle est neuve** : *une borne d'atteignabilité mesurée sur une grille
est une propriété de la GRILLE tant qu'on n'a pas borné les entrées réelles.* Je
n'ai **pas** borné la distribution réelle d'IV du dépôt — je publie donc la
grille la plus large et je dis laquelle.

**Verdict : la branche « AUTRE » EST atteignable. Le 458 tient sur ce point.**

## Ce que « AUTRE » recouvre vraiment — la mesure que le 458 n'avait pas

Étiquetage de **tout l'espace de delta atteignable** par le prédicat servi
(reproduction des trois lignes, pas exécution de la page — règle 443) :

```text
CALL   moneyness 0,98–1,18 · |delta| 0,005 à 0,715 · 1 530 points
   BALANCED       49,8 %
   AUTRE          24,8 %      ← surtout deep-OTM (<0,18) et la bande 0,60-0,715
   DYNAMIC        16,8 %
   ULTRA_CONVEX    8,6 %

PUT    moneyness 0,82–1,02 · |delta| 0,000 à 0,569 · 1 530 points
   DYNAMIC        34,2 %      ← catégorie HAUSSIÈRE
   ULTRA_CONVEX   28,6 %      ← catégorie HAUSSIÈRE
   AUTRE          26,7 %
   BALANCED       10,5 %      ← catégorie HAUSSIÈRE
```

Deux conclusions, et elles **resserrent** le 458 :

**1. « AUTRE » est largement HONNÊTE.** Il couvre surtout des deltas que **la
Constitution elle-même ne catégorise pas** : rien en dessous de 0,18, et **aucune
catégorie entre 0,60 (plafond BALANCED) et 0,70 (plancher LEAPS)**. Un call à
K/S 0,98 et dte 540 sort à delta 0,684 — « AUTRE » est alors la seule réponse
honnête. **Je retire donc l'insinuation que « AUTRE » serait en soi un défaut.**

**2. Ce qui tient, entièrement, c'est l'aveuglement au TYPE.** **73,3 % de
l'espace de put atteignable reçoit un badge de catégorie HAUSSIÈRE** — DYNAMIC
34,2 %, ULTRA_CONVEX 28,6 %, BALANCED 10,5 % — alors que la Constitution pose
`primary_direction: LONG_CALL` et réserve aux positions baissières une catégorie
distincte, `BEARISH_TACTICAL`, `frequency: RARE`, plafonnée à **1**. Le champ qui
corrigerait cela, `c.type`, est dans le **même objet**.

**Le rang 2 du 458 est confirmé — sur UN front, pas deux, et désormais chiffré.**

## L'état des deux dettes

```text
dette                          avant ce lot            après ce lot
gex_scan `symbols_usable`      rang 4, par lecture     RANG 2, par exécution     ↑
« LEAPS → AUTRE » (458)        non établi              atteignable, mais         ↓
                                                       « AUTRE » est honnête
aveuglement au type (458)      rang 2, par lecture     RANG 2 confirmé, 73,3 %   =
                                                       de l'espace put mesuré
```

**Les deux dettes de la tranche sont closes.** Le bilan n°15 héritera de comptes
nets : plus aucun « établi par lecture » en suspens dans la tranche 450-459.

## Portée

- Le prédicat `catOf` est **reproduit**, pas exécuté — trois comparaisons
  recopiées à l'identique des octets servis.
- Les pourcentages d'étiquetage portent sur une **grille de moneyness × dte × iv**,
  pas sur des contrats réels : ils décrivent **l'espace que le sélecteur peut
  produire**, pas la fréquence des cas en usage. `scan_state['options_board']`
  est vide au démarrage.
- **Je n'ai pas borné la distribution réelle d'IV**, et c'est ce qui a fait bouger
  ma borne trois fois. Le chiffre publié (0,781) est celui de la grille la plus
  large que j'aie essayée — **pas une borne du produit**.
- Le banc `gex_scan` fabrique un board **synthétique** : il établit que le
  plafond mord à 31, pas la taille réelle du board en usage. L'argument
  d'atteignabilité repose sur la **lecture** de `_publish_board` et de son
  commentaire, et je le dis.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `gex_scan.scan()`, `gex.compute()` et
  `legacy_engine._greeks()` appelés en mémoire ; routes en **GET** ; `persist`
  redirigé ; **`/options/<sym>`, `/api/analyst/` et `/api/correlations/` NON
  appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-deuxième lot court, **dernier de la tranche 450-459**.

Il fait ce qu'un dernier lot doit faire : il **solde**, et il solde dans les deux
sens. Une dette monte d'un rang parce que le banc tourne enfin ; une autre est
confirmée mais **resserrée de moitié**, et l'insinuation de trop y est retirée.

Le fait de méthode est le plus utile de la tranche, et il est inconfortable :
**ma borne d'atteignabilité a bougé trois fois — 0,684 puis 0,715 puis 0,781 —
et seule la dernière grille était assez large.** La première m'aurait fait
publier « branche inatteignable », c'est-à-dire enterrer un défaut réel. Ce
n'est pas un faux arrêté avant publication au sens habituel : c'est un **faux qui
aurait été produit par un instrument trop étroit**, et la parade est de **faire
varier la grille jusqu'à ce que la réponse cesse de bouger** — ce qu'elle n'a pas
encore fait ici, et je l'écris.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **25** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**

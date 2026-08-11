# SKYLER LOT 494 — La dette du 493 soldée aux deux bouts : le SECOND score /40 monte à 40/40 et atteint S+ — mais il n'est affiché NULLE PART, tandis que le /40 qu'on VOIT plafonne à 29 et n'atteint jamais S ni S+

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-494` (base : lot 493 fusionné,
`392a8ec3`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 493 avait nommé sa dette en deux morceaux : « le plafond du second /40 reste
à établir » et « ni s'il atteint une surface servie ». **Huitième dette nommée
payée d'affilée — et cette fois les deux morceaux sont payés.**

## L'ordre des questions, et pourquoi il est le bon

Le réveil imposait de vérifier **d'abord** si l'objet atteint une surface servie
(règle 491 : *vérifier que l'objet mesuré est l'objet affiché, AVANT de mesurer*).
J'ai suivi cet ordre, et il a changé la nature du lot : la réponse à (1) est
**non**, ce qui interdit tout classement — mais elle rend la réponse à (2)
beaucoup plus parlante qu'elle ne l'aurait été seule.

## (1) La surface servie — mesuré : NON

Instrument : recherche dans les **42 objets servis** (8 pages + `/analysis/AAPL`
+ 33 JS non-vendor), **841 916 caractères** — le corpus de référence, retrouvé au
caractère près.

**Calibration écrite dans le détecteur**, sortie programmée : témoin **positif**
`.detail` (l'`analysis_page` fait `const d=(t&&t.detail)||{}` sur la réponse de
`/api/ticker`) → **4 objets**, trouvé ; témoin **négatif** `zzz_inexistant` →
**0**. Instrument valide.

```text
acces  .pack  /  ['pack']            0    ← /analysis fetche /api/ticker mais ne lit JAMAIS `pack`
score40                              0
no_chase                             0
optfit                               0
api/cockpit                          0    ← le SEUL endpoint qui expose `recommendations`
```

**Les deux chemins de production sont morts côté client :**

- **Chemin A** — `terminal.py:591` → `recs` → `scan_state['recommendations']` →
  `/api/cockpit`. **Cet endpoint n'a aucun consommateur** dans tout le dépôt.
  Les **sept** lecteurs de `d.recommendations` qui lisent `r.score40`
  (`terminal.py:3513, 3553, 3581, 3619, 3630, 3793, 4155`) vivent dans
  **`PAGE_DAILY` (2353-3838) et `PAGE_WATCHLIST` (3956-4288)** — deux constantes
  qu'**aucune route ne retourne** (vérifié : pas un seul `return PAGE_*`).
- **Chemin B** — `terminal.py:1597` → `out['ibkr']` → `options_pack` →
  `/api/ticker/<sym>` (clé `pack`) et `/options/<sym>`. La page `/analysis`
  **fetche bien** `/api/ticker`, et ne lit que `t.detail` et `t.company`.

**Le second /40 est calculé pour chaque titre à chaque scan, et jeté.**

## (2) Le plafond — 40/40, et S+ EST atteignable

Le banc du 493 rendait « 25/40 » et je l'avais refusé parce que `Fondamentaux
5/8` et `Option Fit 4/6` trahissaient les branches **neutres**. Cette fois la
validité du banc est **vérifiée avant toute conclusion** (leçon 492/493), par
deux calibrations avec sortie programmée :

```text
(A) ENTRÉE VIDE  d={'score':0}, sans opt ni fund
    attendu, calculé à la main sur le code :
    fond 5 · tech 1 · cata 3 · inst 2 · optfit 4 · asym 3  → total 18
    MESURÉ : identique.                                        OK

(B) VALIDITÉ  sur l'entrée « parfaite », AUCUNE composante ne doit rester
    sur sa valeur neutre — en particulier fond != 5 et optfit != 4.
    MESURÉ : composantes restées neutres = AUCUNE.               OK
```

C'est exactement le contrôle qui manquait hier. Une fois passé :

```text
entrée parfaite  fond 8 · tech 8 · cata 6 · inst 6 · optfit 6 · asym 6
                 TOTAL 40/40 · niveau S+

balayage 2 099 520 combinaisons   MIN 8 · MAX 40
  S+      3 597   (0,17 %)
  S      89 947
  A     464 438
  B   1 107 676
  rejeté 433 862
```

**Les six composantes atteignent leur maximum, le total atteint 40, et les cinq
niveaux sont atteints.**

## Le contraste, et c'est le résultat du lot

```text                         skyler_core.score40      scorecard.score40 (alias ibkr)
plafond                        29 / 40   (485)          40 / 40
niveaux S et S+                INATTEIGNABLES (484-A)   atteignables (S+ 0,17 %)
affiché ?                      OUI — /analysis          NON — nulle part
```

**Le « /40 » que l'utilisateur voit ne peut pas atteindre ses deux niveaux
hauts ; le « /40 » qui les atteint n'est affiché nulle part.** Deux moteurs, deux
échelles /40, deux échelles S+/S/A/B — et ils sont exactement à l'envers l'un de
l'autre.

Je le **nomme** et je ne le **classe pas** : un chiffre non affiché ne trompe
personne (règles 486, 491, 492). Ce que ce lot apporte n'est pas un dossier, c'est
**la fin d'une incertitude** — la question du 493 a maintenant une réponse
mesurée aux deux bouts.

## Le second contrôle — deux cas que mes instruments EXCLUAIENT

### (I) Le banc fabrique un `opt` complet — que passe le SITE D'APPEL ?

```text
terminal.py:591   (le scan, tous les titres)   MAX 38/40   cata plafonné à 4/6
terminal.py:1597  (options_pack, un titre)     MAX 40/40   aucun bloc plafonné
```

`terminal.py:588-590` construit `opt = {'valuation': …}` plus éventuellement
`'best_pick'` — et **jamais** de clé `earnings_dte`. Or `ibkr_score` lit
`ed = opt.get('earnings_dte')` : au site du scan, `ed` est **toujours None**,
donc `cata` vaut 3, +1 en régime TREND → **4 sur 6, par construction du site
d'appel, pas du moteur**.

**C'est le motif du 485 reproduit sur l'autre moteur** : un bloc plafonné sous
**son propre** maximum. Ici il ne bloque rien (38 dépasse le seuil S+ de 36) —
mais il n'est visible que si l'on refuse de mesurer le moteur **hors** de son
site d'appel.

### (II) Conclure par ABSENCE — les clés SŒURS sont-elles lues ?

Sur les **34 clés** qu'`options_pack` pose dans `out`, **18 voient leur nom
apparaître** dans les octets servis (`error`, `regime`, `spot`, `sector`,
`name`… et **`ibkr`, 2 fois**). Lues une à une : les deux occurrences de `.ibkr`
sont **`data_sources.ibkr`**, l'état de connexion du courtier sur `/system`.

**Enseignement chiffré sur mon propre instrument : l'ABSENCE d'un nom est une
preuve forte, sa PRÉSENCE ne prouve rien — 18 faux positifs sur 34.** C'est la
règle 488 (*le tri se fait à la lecture, pas au grep*) avec, pour la première
fois, **son taux d'erreur mesuré**.

## Trois faux résultats arrêtés avant publication

1. **Le motif `ibkr` nu rendait 19 occurrences** dans les octets servis. J'aurais
   pu écrire « c'est lu ». Motif resserré puis **lecture** : les 19 sont
   `/api/ibkr/positions`, `data_sources.ibkr`, `source==='ibkr'` — **le
   courtier**, jamais le verdict. **Vingt-et-unième homonyme.**
2. **`d.recommendations` sur `/journal`** : j'allais compter un consommateur.
   Tracé — il vient de `/api/skyler/memory`, c'est-à-dire de
   `decision_memory.recommendations()`. **Vingt-deuxième homonyme.**
3. **J'allais écrire que le vocabulaire servi est orphelin.** Les 9 pages portent
   `BUY_PULLBACK`, `WATCH_BREAKOUT`, `TOO_LATE`, `ACCEPTÉ SUR REPLI` dans
   `__VXVOCAB` ; comme `scorecard` est leur producteur et qu'il n'atteint pas le
   client, j'ai cru tenir un vocabulaire sans producteur. **Faux** :
   `decision_stack.py:110` produit `BUY_PULLBACK`, et `decision_api.py:144-145`
   s'en sert. **Le vocabulaire est légitime.**

**Arrêtés avant publication : 62 → 65.**

## Une erreur à moi, publiée hier, que je corrige

La **ligne d'index du 493** déclare « snapshot runtime 21 fichiers, écart
**AUCUN** ». C'est faux, et le rapport du 493 dit le contraire au même moment :
un fichier **est apparu** (`desk_backup_20260810.json`) et le compte est passé de
**21 à 22**. La ligne d'index est corrigée par la présente mention ; je ne
réécris pas la ligne publiée, je la contredis ici, à sa date.

**Publiés puis corrigés : 10 → 11.**

## Portée

- Le plafond 40/40 est établi **par balayage** de 2 099 520 combinaisons
  d'entrées **fabriquées** : c'est ce que le moteur **peut** rendre, pas la
  distribution en usage réel (règle 459 — une borne mesurée sur une grille est
  une propriété de la grille). Le point à 40 est atteint, donc la borne haute est
  **exacte**, pas seulement une borne inférieure.
- La non-présence sur surface servie est établie sur les **octets servis** et sur
  le tracé des deux chemins de production. **Aucun navigateur ouvert** : je n'ai
  pas besoin du rendu pour établir qu'un champ n'est jamais lu par le code servi.
- `PAGE_DAILY` et `PAGE_WATCHLIST` sont déclarées **non servies** parce
  qu'aucune route ne les retourne. Je n'ai **pas** audité l'ensemble des
  constantes `PAGE_*` de `terminal.py` — seulement ces deux-là.
- Le second `/40` **n'est pas classé**. Il rejoint la famille du 486 et du 491 :
  exact, produit, jamais peint.
- Le coût de calcul (un `verdict()` par titre à chaque scan, jeté) est **constaté,
  non chiffré** : je n'ai pas mesuré de temps.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** (`cache_path` suit la redirection) ;
  `scorecard` **sans écriture**, vérifié au 493 ; **aucune route réseau
  sortante** — `/options/<sym>` et `/api/analyst/<sym>` jamais appelés.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, aucun apparu, aucun
  disparu, écart final **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Quatrième lot consécutif sans nouveau dossier classé**, et je ne vais pas
l'habiller : la feuille reste à 24. Mais ce lot ne ressemble pas aux trois
précédents. Le 491 a nettoyé une liste, le 492 a mesuré deux barèmes, le 493 a
clos une famille — **le 494 ferme une question qu'il avait lui-même ouverte
la veille, aux deux bouts, avec le contrôle de validité qui manquait.**

Et il pose sur la table la phrase la plus courte de la tranche : **il y a deux
scores /40 dans Vertex, et c'est le mauvais qui est branché.**

Comptes séparés : résultats faux **arrêtés avant publication 65 (+3)** ; publiés
puis corrigés **11 (+1)** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**

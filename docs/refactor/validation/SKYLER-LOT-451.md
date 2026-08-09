# SKYLER LOT 451 — Les quatre phrases `source` ne sont jamais produites : `build_surface` n'a aucun appelant, et la liste blanche d'outils de l'IA non plus

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-451` (base : lot 450 fusionné,
5e682aa)

Trente-deuxième lot de la veine, premier de la tranche 450-459. Le bilan n°14
venait de trancher que **vérifier l'affichage avant de mesurer** est la règle la
plus rentable. Ce lot l'applique au champ composé suivant sur la carte du 444 :
**`source`**, 4 phrases, annoncé « lu par 4 écrans ».

**Aucun code, aucun gardien, aucun test.**

## D'abord une erreur de plan, que je publie

L'orientation de ce lot disait : *« un champ nommé `source` qui se tromperait sur
la provenance serait un défaut d'honnêteté direct »*. **C'était faux avant même la
première mesure.** Dans `vol_surface.py`, `source` n'est **pas** une étiquette de
provenance :

```python
Anomaly(code='STRIKE_IV_DISLOCATION', …, source=f'{symbol} {exp} {k}', …)
Anomaly(code='SMILE_DISCONTINUITY',   …, source=f'{symbol} {exp} {k1}->{k2}', …)
Anomaly(code='EXPIRY_IV_DISLOCATION', …, source=f'{symbol} dte={dte}', …)
Anomaly(code='SKEW_OUTLIER',          …, source=f'{symbol} {exp}', …)
```

C'est un **localisateur d'anomalie** : il dit **où** l'anomalie se trouve, pas
**d'où vient la donnée**. Le « 4 écrans » de la carte du 444 concerne un **autre**
`source` — celui des cartes de graphique (`source: 'scan'`, `scan.source`…).

**Cinquième récidive du piège « un nom, plusieurs payloads »** (438 `scan`, 441
`.decision`, 444 `invalidation`, 446 `return_pct`, ici `source`) — et **la
première fois qu'il égare le PLAN, avant toute mesure**. Le péage du 446 a fait
son travail : il a mordu à l'étape 1.

## Étape 1 — l'affichage : ces phrases n'atteignent aucun écran, parce qu'elles ne sont jamais produites

```text
fonction                              appelants HORS de son module
vol_surface.build_surface()                      0
vol_surface.relative_value_zones()               0
```

Les quatre `Anomaly(...)` sont **toutes** construites à l'intérieur de
`build_surface()`. Sans appelant, **aucune des quatre phrases n'est jamais
construite**. Ce n'est pas « non affiché » — c'est **jamais produit**, la
distinction posée au 449.

Les deux seules mentions de `vol_surface` hors du module sont :

```text
vertex/ai/tool_registry.py:16        'get_vol_surface'  — une CHAÎNE dans une liste blanche
opportunities_page.py:607            « … moteurs option_anomalies / vol_surface / portefeuille »
                                       — le mot dans une PHRASE FRANÇAISE, pas un appel
```

## Et la liste blanche qui le nomme n'a, elle non plus, aucun appelant

```text
vertex/ai/tool_registry.py           appelants dans vertex/ : 0
```

`ALLOWED_TOOLS` — qui contient `'get_vol_surface'` — et `FORBIDDEN_TOOLS`, et la
classe `ToolRegistry` avec sa validation `register()`, ne sont **importés par
aucun module de production**. Deux modules, **269 lignes** au total
(`vol_surface.py` 210, `tool_registry.py` 59), qu'aucun chemin servi n'atteint.

### Ce que cela ne veut PAS dire — et je le dis avant qu'on le lise de travers

`FORBIDDEN_TOOLS` contient `place_order`, `submit_order`, `transmit_order`… On
pourrait croire qu'un garde-fou de sécurité est hors circuit. **Ce n'est pas le
cas, et l'invariant READONLY ne dépend pas de cette liste.** Mesuré : dans tout
`vertex/`, hors `tool_registry.py`, la recherche de `place_order`,
`submit_order`, `transmit` rend **une seule ligne** :

```python
vertex/planning/order_ticket.py:175    'transmitted': False,   # invariant : jamais transmis
```

**Il n'existe aucun chemin d'ordre à garder.** La liste blanche ne protège rien
parce qu'il n'y a rien à protéger par elle — pas parce qu'une protection aurait
sauté.

## Les gardiens, eux, sont bien là — sur du code que le produit n'appelle pas

```text
tests/test_ai_runtime.py:26-40                 instancie ToolRegistry, vérifie ALLOWED ∩ FORBIDDEN = ∅
tests/test_production_guards_canonical.py:48-53 même vérification, nommée « gardien canonique »
tests/test_vol_surface_lot108.py                exerce build_surface()
```

C'est exactement le motif du **436** : *un gardien dont le périmètre s'étend
AU-DELÀ du produit*. Ces tests passent, ils vérifient ce qu'ils disent — et ils
défendent **269 lignes que le produit n'appelle jamais**. Ils rendraient toute
suppression coûteuse et donnent l'impression que ces modules comptent.

## Classement

- **Les 4 phrases `source` : jamais produites** → **rang 4**, même famille que
  `tradingview_signal_store` au 449. Rien à l'écran, donc aucun mensonge.
- **269 lignes de moteur et de registre sans appelant, mais testées** →
  **rang 3** : poids mort, et trois fichiers de tests qui le figent.

**Ce n'est pas un défaut de sécurité** — je viens de le mesurer et je le répète
ici pour que le classement ne soit pas sur-lu.

Correction pressentie — et c'est une **décision de produit**, pas une correction
de deux lignes : soit `build_surface` a un consommateur prévu et il manque (la
page `/options` a une vue volatilité), soit il n'en a pas et les deux modules
doivent partir avec leurs tests. **Aucun GO, rien n'est engagé.**

## Portée

Je mesure les appelants **dans `vertex/`** ; un appel depuis `terminal.py` a été
cherché dans le même balayage et n'existe pas non plus. Un appel construit
dynamiquement (`getattr`, table de dispatch) échapperait à cette recherche —
**je ne l'ai pas quantifié**, mais `ToolRegistry.register()` étant lui-même sans
appelant, la table de dispatch qui l'utiliserait n'existe pas.

`realized_vol()` et `_median()` du **même fichier** ont, eux, des appelants (2 et
8) : le fichier n'est donc pas entièrement mort — **seule la partie qui produit
les anomalies l'est**. C'est le témoin positif de la mesure : l'instrument
distingue, dans le même module, ce qui est appelé de ce qui ne l'est pas.

**Aucun navigateur ouvert.** Sur les 110 phrases concluantes du 444, **89 restent
fermées** après ce lot.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Aucun moteur exécuté : ce lot est un parcours d'appelants
  sur le code source, pas un banc.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-quatrième lot court, premier de la tranche.

Le lot ne trouve **aucun défaut affiché** — et c'est le péage du 446 qui l'a
décidé en trois mesures, avant d'ouvrir un banc. Le bilan n°14 disait que la
règle vaut **parce qu'une carte existait** ; ici elle vaut aussi **parce qu'elle
arrête tôt** : le plan était fondé sur un contresens de nom, et l'étape 1 l'a
révélé avant que la mesure ne soit dépensée.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **20** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**

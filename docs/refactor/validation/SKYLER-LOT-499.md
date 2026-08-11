# SKYLER LOT 499 — La famille du 495 bornée par un ESPION D'EXÉCUTION à zéro faux positif : SEPT clés manquent sur le DÉTAIL, et ZÉRO sur tous les autres objets de `scan_state` — la symétrie inverse que le 498 avait nommée n'existe pas

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-499` (base : lot 498 fusionné,
`5afafe29`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

## Le choix

**(a)**, comme recommandé : c'est la veine qui a produit le dernier rang 1
(495-A), et la question posée — « la symétrie inverse existe-t-elle ? » — est
**décidable par la mesure**. **(b)**, le coût de démarrage en millisecondes,
**reste une dette nommée**. **(c)**, le bilan n°18, est le lot 500.

## Le changement d'instrument, et c'est le point du lot

Le 495 cherchait les lectures par **expression régulière** : 33 sorties, **29
faux positifs** (le `d` de `decision_memory` n'est pas le détail du scan). Ici
l'instrument est un **espion d'exécution** : chaque objet de `scan_state` est
remplacé par une sous-classe de `dict` qui enregistre les clés **demandées et
absentes**.

**Une absence enregistrée est réelle par construction — zéro faux positif.**

**Calibration — charge d'abord (497), témoin du même genre (498) :**

```text
(0) CHARGE   scan DEMO : 20 titres · 20 lignes                        OK
(A) POSITIF  detail.st_fund enregistré absent 132 fois (trouvaille du 495)  OK
(B) NÉGATIF  detail.score jamais enregistré absent : 0 fois           OK
```

Exercices : **32, toutes réponses 200** — `/scan`, `/api/cockpit`,
`/api/watchlist`, `/api/market/summary`, `/api/market/regime`, `/api/brief`,
`/api/committee-review`, `/api/opportunities/funnel`, `/api/data-quality`,
`/api/strategie`, `/api/comite`, `/api/weekly`, `/cal-feed`, `/news-feed`,
`/healthz`, `/api/live/status`, `/api/session/manifest`,
`/api/portfolio/context`, plus `/api/decision/<sym>` et
`/api/strategy/decision/<sym>` sur six titres, plus `recalculate_all` avec et
sans thèse. **Aucune route réseau sortante.**

## Le résultat : la famille tient sur UN SEUL objet

```text
-- DÉTAIL : 7 clés demandées et ABSENTES --
   earnings_dte     212 ×      st_fund      132 ×      fund_score  132 ×
   rr                92 ×      st_timing     92 ×      atr          80 ×
   rvol              80 ×

-- ROW              0 clé absente
-- portfolio        0        daily        0        market_ctx   0
-- committee        0        strategy     0        recommendations 0
```

**La symétrie inverse que le 498 avait nommée comme dette N'EXISTE PAS** : aucune
clé n'est lue sur la ROW sans y vivre. Les cinq autres objets de `scan_state`
sont propres eux aussi. **Le défaut est confiné au DÉTAIL**, et c'est un
bornage, pas une extension.

Témoin de vie, pour que « zéro » veuille dire quelque chose : sur les mêmes
exercices, le détail a servi `sector` **3 616 fois**, `score` 1 892, `rs` 1 632 ;
la ROW `score` 254, `symbol` 96 ; `market_ctx` `spy_regime` 36. **Les objets ont
bien été lus.**

## Les trois clés au-delà des quatre du 495 — et le tri qui compte

```text
rr    92 ×  strategy_os_api.py:59 · recalculator.py:102
            → `detail.get('rr') or plan.get('rr')` — LE REPLI FONCTIONNE
            → SANS CONSÉQUENCE. (Et `plan['rr']` vaut 3.0 : dossier 442.)
atr   80 ×  calculator.py:35  `(detail or {}).get('atr')` — AUCUN repli
            → `stop_distance_atr = None`. La valeur existe : `plan['atr']`.
rvol  80 ×  calculator.py:46  `d.get('rvol')` — AUCUN repli
            → `rel_volume = None`. La valeur existe : `volx` sur le détail,
              `rvol` sur la ROW. **Exactement le motif du `st_fund`.**
```

**`rel_volume` et `stop_distance_atr` : 0 occurrence dans les octets servis.**
Et le 497 a établi que `/portfolio` ne lit du `/api/positions/state` que
`state.portfolio`, jamais le tableau des positions. **Doublement non affichés →
nommés, non classés** (règles 486, 491, 492, 494).

**J'allais compter `rr` comme un cinquième défaut.** Le repli
`or plan.get('rr')` le rend inoffensif. **Une clé morte suivie d'un repli qui
marche n'est pas un défaut** — c'est une redondance.

**Arrêtés avant publication : 75 → 76.**

## Le second contrôle — ce que l'espion EXCLUT, chiffré contre l'ancien instrument

L'espion ne voit que les **chemins exécutés**. Comparaison directe avec la regex
du 495 sur la même question :

```text
clés vues par la regex du 495                        89 distinctes
clés vues par l'espion                                7
  dont INVISIBLES à la regex du 495                   1 : `atr`
      → `(detail or {}).get('atr')`, forme PARENTHÉSÉE que la regex
        (« un NOM nu suivi de .get( ») ne peut pas voir, par construction
  signalées par la regex, jamais vues par l'espion    83
      → chemins non exécutés OU faux positifs (le 495 en avait mesuré 29 sur 33)
```

Autres formes parenthésées relevées au passage, invisibles à l'ancien
instrument : `plan` (3 sites), `price` (5), `series`, `verdict` (2) — toutes
présentes sur leur objet, donc sans conséquence, **mais elles montrent que la
regex du 495 avait un angle mort structurel**.

**Les deux instruments ne se remplacent pas** : l'espion est exact mais borné
par la couverture ; la regex est large mais bruitée. Ce lot les fait se
contrôler l'un l'autre, et **chacun trouve ce que l'autre ne peut pas voir**.

## Portée

- **32 exercices** sur des routes vérifiées sûres. Les chemins non exécutés
  échappent : le chiffre « 83 clés signalées par la regex jamais vues » **borne
  ce que je n'ai pas couvert**, sans le trier.
- Les comptes (212 ×, 132 ×…) dépendent du **nombre d'exercices**, pas d'une
  fréquence de production. Ils indiquent l'intensité relative, rien de plus.
- Le scan DEMO fait **20 titres** ; un détail réel plus riche pourrait porter des
  clés que la démo n'a pas. **La conclusion sur les sept est cohérente avec le
  495**, qui l'avait établie par AST sur le code, indépendamment de la démo.
- Je n'ai espionné que les objets **de premier niveau** de `scan_state` ; les
  sous-objets (`detail[sym]['plan']`, `['sub']`, `['series']`) **ne sont pas
  espionnés**.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** ; positions **fabriquées en mémoire**,
  `desk_data.json` jamais ouvert en écriture ; **aucune route réseau sortante**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle — dernier lot de la tranche 490-499

Ce lot ferme la tranche sur une note qui la résume : **il ne trouve pas un
défaut, il borne une famille** — et il le fait en **changeant d'instrument**
plutôt qu'en refaisant la même mesure.

Le fait le plus durable est méthodologique et il est mesuré, pas affirmé :
**un espion d'exécution a zéro faux positif et un angle mort de couverture ; une
regex a une couverture totale et 29 faux positifs sur 33.** Les faire tourner
l'un contre l'autre a produit exactement une clé neuve (`atr`) et une borne
honnête sur ce qui reste invisible.

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
Dette nommée qui reste : **le coût de démarrage en millisecondes** (498).

Comptes séparés : résultats faux **arrêtés avant publication 76 (+1)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse. Le lot 500 sera le
bilan n°18.**

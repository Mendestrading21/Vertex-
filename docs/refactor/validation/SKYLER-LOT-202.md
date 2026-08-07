# SKYLER LOT 202 — Tournée TV : price-chart — niveaux du plan en chips (repli aligné)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-202` (base : lot 201 fusionné)

## Livré

### Price-chart (Analyse) — l'échelle des niveaux au langage TV partout

1. **Constat sur le CANONIQUE** : le graphique principal d'Analyse est
   rendu par TradingView Lightweight Charts (lwCandlestickCard) — les
   niveaux du plan y sont DÉJÀ des étiquettes natives de l'échelle de
   prix (TP1 206.37 vert, Entrée 198.00, Résistance 199.70, Stop
   189.63 rouge, dernier prix, volume) : c'est le langage TV d'origine.
   Vérifié en navigateur sur /analysis/ACN.
2. **REPLI Chart.js aligné** (`C.levelLines`, chart-core) : les niveaux
   du plan passaient en texte plat à gauche — ils portent désormais
   leur étiquette en **CHIP pleine couleur au BORD DROIT** (texte
   sombre, gras, comme l'échelle TV), avec **anti-collision verticale**
   (empilement quand deux niveaux se chevauchent) et bornage à la zone
   de tracé. Lignes pointillées et couleurs par kind inchangées.
   Le repli (bougies invalides → priceCard) parle maintenant la même
   langue que le canonique.

## Accros

Aucun. Note honnête : le repli n'est pas capturable en démo (le
canonique LWC fonctionne — c'est le comportement voulu de l'échelle de
repli) ; l'alignement est prouvé par le code (node --check + suite) et
la capture montre le canonique déjà conforme.

## Preuves

- `node --check` OK (chart-core.js) ; gardiens lot 52/54 (`C.levelLines`
  présent, découpage multiLine) toujours verts.
- Serveur DEMO port 5002 : `lot202-pricechart-card.png` — chandeliers
  ACN avec chips de niveaux natifs au bord droit ; pages Analyse
  1440 + 390 — envoyées, **0 erreur console**.
- SW `td-shell-v165` → `v166` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 203 : suivant de TV-CHARTS-INVENTORY.md — vol cone / IV term
structure, GEX / double probabilité, sparklines KPI. Mini-bilan au
lot 205.

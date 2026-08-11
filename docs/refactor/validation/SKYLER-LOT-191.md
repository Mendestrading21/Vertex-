# SKYLER V2 — LOT 191 : TOURNÉE TV — barres de consensus du comité

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-191`
(base : `integration/vertex-skyler-v2` @ `46c7903`, lot 190 fusionné).
Lot UI (tournée graphique TV). Moteurs INTACTS, READONLY intact.

## 1. Livré

```text
NOUVEAU BUILDER charts/consensus-bars.js — VXCharts.consensusBars :
  le « Note des analystes » TradingView sur des comptes RÉELS —
  libellé à gauche, barre pleine à bout arrondi (longueur ∝ max),
  compte à droite, la barre DOMINANTE en pleine intensité et les
  autres adoucies (opacité .45), total rappelé en pied honnête.
  items vide → VX.states.empty (le consensus n'est jamais inventé).
BRANCHÉ vue Comité (intelligence_page.py) : remplace le tally
  ad hoc par le builder, tons par famille de verdict (positif /
  négatif / breakout / attente), libellés FRANÇAIS via __VXVOCAB.
BONUS STRUCTUREL : __VXVOCAB (source unique
  recommendation.vocab_js) n'était injecté QUE dans l'ancien
  pipeline mort — il est désormais injecté par le SHELL de la
  refonte (toutes les pages en profitent : « Éviter », « Surveiller
  la cassure », « Attendre » au lieu des clés brutes).
SW v154 → v155 + 5 gardiens de version.
```

## 2. Accros rencontrés (dits)

Le gardien anti-XSS fuzz (lot 43) refuse toute balise <script> NUE
dans les pages — l'inline du vocabulaire en était une → balise
attribuée (<script id="vx-vocab">), l'esprit du gardien est
préservé (un payload réfléchi injecte un <script> nu). Première
capture : libellés en clés brutes (__VXVOCAB absent des pages de la
refonte) → correctif shell ci-dessus, secondes captures en FR.

## 3. Preuves

```text
node --check consensus-bars.js → OK (+ sweep lot 186 en suite)
Serveur DEMO 5002 · captures /intelligence?view=committee 1440+390 +
  carte cadrée (« Éviter » 11 dominant rouge, « Surveiller la
  cassure » 8, « Attendre » 1 — 20 dossiers) — 0 erreur console —
  ENVOYÉES à l'utilisateur
python -m pytest tests/ -q → 2461 passed, 2 skipped
TV-CHARTS-INVENTORY.md : consensus ✔
```

## 4. Suite

LOT 192 : regimeAura aligné (Aujourd'hui) + payoff hachuré (Options)
OU zones d'estimation sur les aires. MINI-BILAN au lot 195.

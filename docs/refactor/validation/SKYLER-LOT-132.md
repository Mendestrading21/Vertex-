# SKYLER V2 — LOT 132 : passe n°7 — anomalies lisibles + calendrier avec imminence (Opportunités)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-132`
(base : `integration/vertex-skyler-v2` @ `3f1e3a1`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
opportunities_page.py + timeline-chart.js + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /opportunities?view=anomalies & calendar)

Deux widgets « chiffres sur chiffres » : (a) la table des ANOMALIES —
l'intensité était un nombre nu à côté du score, impossible de classer
d'un coup d'œil ; (b) le CALENDRIER des catalyseurs — 30 lignes
monotones identiques, l'imminence (résultats dans 3 j vs dans 43 j)
ne se voyait pas.

## 2. Améliorations

```text
anomalies (opportunities_page.py) : l'intensité devient une
  MINI-BARRE de verre (dégradé warning doux → dense via color-mix,
  échelle relative au max du scan) + la valeur tabulaire à côté —
  l'œil classe sans lire chaque nombre
calendrier (timeline-chart.js + opportunities_page.py) : IMMINENCE
  visuelle — tout événement à ≤ 7 jours porte un liseré warning et
  sa date en warning gras (dte réel pour les earnings, écart de
  dates pour la macro) ; le builder timelineCard gagne l'option
  `urgent` (toutes les timelines peuvent en hériter)
aucun littéral couleur nouveau · états vides honnêtes inchangés
```

SW `td-shell-v140` → `td-shell-v141` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v141)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (anomalies + calendrier)
```

## 4. Suite

LOT 133 : passe n°8 (candidats : desk Options /options sous-vues,
vue Radar Opportunités, dernières tuiles KPI).

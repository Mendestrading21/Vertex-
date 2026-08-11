# SKYLER V2 — LOT 141 : passe n°16 — fourchette des analystes en rail de verre (fiche Analyse)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-141`
(base : `integration/vertex-skyler-v2` @ `ac6f74b`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
analysis_page.py + SW + gardiens + docs.

## 1. Diagnostic (fiche /analysis/ACN, section 4 — Sentiment)

La FOURCHETTE des objectifs analystes était du texte nu
(« 130,00 – 275,00 ») à côté d'un « Objectif moyen 179,29 (-9.4%) » —
trois nombres sans géométrie : impossible de voir OÙ le cours vit
dans la fourchette, ni pourquoi le potentiel est négatif.

## 2. Amélioration (consensus, analysis_page.py)

```text
la fourchette devient un RAIL de verre low → high (dégradé brand
  léger) avec deux repères HALOTÉS : le COURS en cyan et
  l'OBJECTIF MOYEN en warning — on voit d'un coup d'œil que le
  cours (198) est AU-DESSUS de l'objectif moyen (179), d'où le
  potentiel négatif
bornes low/high affichées aux extrémités · title au survol de
  chaque repère · repères clampés aux bords (jamais inventés)
color-mix sur tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v149` → `td-shell-v150` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v150)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 + zoom Sentiment envoyées
```

## 4. Suite

LOT 142 : passe n°17 (candidats : Système sous-vues
Données/Automatisations, dernières poches).

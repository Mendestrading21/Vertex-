# SKYLER V2 — LOT 138 : passe n°13 — concentration en barre de verre avec repère prudent (Synthèse)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-138`
(base : `integration/vertex-skyler-v2` @ `25a0fdd`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
portfolio_page.py + SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /portfolio Synthèse)

Le treemap d'allocation est déjà en verre (lot 123) et le hero
éditorial est riche. La tuile KPI **CONCENTRATION** affichait « 65 % »
en chiffre nu — alors que le Risque dominant juste au-dessus cite le
repère prudent (~15 % par titre) : la donnée et son seuil vivaient
côte à côte sans se parler.

## 2. Amélioration (kpi Concentration, portfolio_page.py)

```text
la concentration devient une MINI-BARRE de verre avec le REPÈRE
  prudent au tick (~15 %, celui du Risque dominant) : < 15 %
  positive, 15-25 warning, > 25 negative + halo — le 65 % d'ACN
  vire au rouge, la distance au repère se VOIT
sous-titre enrichi : « Top 1 ACN · Top 3 100 % · repère ~15 % »
n/d honnête conservé quand les poids sont indisponibles
color-mix sur tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v146` → `td-shell-v147` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v147)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Synthèse)
```

## 4. Suite

LOT 139 : passe n°14 (candidats : tuiles KPI d'Aujourd'hui, vue
Vue d'ensemble Marchés, design system) ; lot 140 = mini-bilan 136-140.

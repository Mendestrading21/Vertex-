# SKYLER V2 — LOT 128 : passe n°3 — le donut gagne son chiffre éducatif

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-128`
(base : `integration/vertex-skyler-v2` @ `e40454b`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
chart-core.js + SW + gardiens + docs.

## 1. Diagnostic

Tour des builders restants : anomaly-scan (halos pulsants + dégradé),
équité/drawdown (wrappers de C.area — verre du lot 120), sparkline
(dégradé lot 53) déjà au niveau. Le manque : `C.donut` — l'anneau
central restait VIDE ; pour connaître la catégorie dominante il
fallait lire la légende et additionner de tête (la page Breadth
l'écrivait en texte au-dessus, à côté du graphique).

## 2. Amélioration (C.donut, chart-core.js — tous les donuts héritent)

```text
LE chiffre éducatif du donut : la catégorie DOMINANTE et sa part
  (« 55 % / AVOID ») s'affichent AU CENTRE de l'anneau, dans la
  couleur de son arc — l'œil lit la conclusion sans additionner
plugin vxDonutCenter (afterDatasetsDraw), centré sur le vrai centre
  de l'arc (meta.data[0].x/y) — robuste au redimensionnement
rien n'est affiché si le total est nul (aucune donnée inventée)
libellé tronqué à 14 caractères en muted sous le pourcentage
signature lot 53 intacte (arcs arrondis, spacing, hoverOffset) ·
  aucun littéral couleur nouveau
```

SW `td-shell-v136` → `td-shell-v137` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v137)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Marchés/Breadth —
  « Répartition des verdicts du scan »)
```

## 4. Suite

LOT 129 : passe suivante (candidats : timeline-chart, price-chart,
mise en scène des vues Volatilité/Macro).

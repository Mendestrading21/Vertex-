# SKYLER V2 — LOT 125 : amélioration graphique n°7 — Journal (barres verre + stats enfin stylées)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-125`
(base : `integration/vertex-skyler-v2` @ `41c7f4f`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
chart-core.js + cockpit.css + performance_page.py + SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /journal)

Trois défauts : (a) le bloc Post-mortem affichait des stats BRUTES
COLLÉES (« Trades3 », « Réussite33 % », « P&L cumulé-700 ») — les classes
`vx-stats-row`/`vx-stat` utilisées par **5 pages** n'avaient AUCUN CSS ;
(b) `C.bars` (distribution, erreurs/mois, track record… tous les
graphiques à barres de Vertex) : aplats translucides sans matière ;
(c) `loadTrack` : 3 hex codés en dur (`#9d978e`, `#36c889`, `#ed655c`).

## 2. Améliorations

```text
C.bars matière VERRE (chart-core.js — toutes les barres héritent) :
  chaque barre est un dégradé de sa PROPRE couleur, dense à
  l'extrémité de la valeur → doux vers la base (même grammaire que
  treemap/aire), liseré fin de la couleur, PLEINE au survol —
  l'alpha n'est appliqué qu'aux hex 6 digits, jamais corrompu
famille .vx-stat (cockpit.css) : tuiles de verre sobres — libellé
  uppercase discret, chiffre mono tabulaire 19px, positif/négatif
  avec halo (--vx-glow-pos/neg) — répare 5 pages d'un coup
track record : hex en dur → VXCharts.colors.muted/positive/negative
  (plus aucun littéral orphelin)
uniquement des tokens — AUCUN littéral couleur nouveau
```

SW `td-shell-v133` → `td-shell-v134` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v134)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (+ preuve barres verre
  sur Marchés/Breadth)
```

## 4. Suite

LOT 126 : amélioration graphique n°8 (Système /system).

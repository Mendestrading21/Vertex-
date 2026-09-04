# Vertex — Moteur options (Vertex Dynamic Options)

Voir `VERTEX_CALCULATION_REFERENCE.md` pour les formules. Piliers :
- `scenario_pricer.py` : BS avec dividende, grille spot (BEAR/STOP/FLAT/
  BASE/TP1-3) × temps (0-28 j) × IV (±20/±10/0), R:R = gains/pertes
  simulés (jamais le payoff max), taux par échéance.
- `call_selector.py` : catégories BALANCED (Δ .40-.60) / DYNAMIC (Δ .28-.45,
  principale) / ULTRA_CONVEX (Δ .18-.30, rare) — 1 par catégorie + 1
  principal ; DTE 60-270, préf. 90-210.
- `bearish_tactical.py` : PUT rare (≥3 preuves convergentes, max 1) —
  jamais « parce que le marché baisse ».
- `contract_scorer.py` : `MIN_REWARD_RISK = 2.0` (constitution), score
  multiplicatif liquidité × R:R × coût du temps.
- Comparateur (§22) : défensif / PRINCIPAL / explosif, dominance Pareto
  expliquée dimension par dimension (UI Opportunités → Options).

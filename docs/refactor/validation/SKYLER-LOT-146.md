# SKYLER V2 — LOT 146 : caractérisation étendue du cœur analytique

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-146`
(base : `integration/vertex-skyler-v2` @ `f2fc91c`, lot 145 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié.

## 1. Cible et méthode de choix

Constat d'inventaire : contrairement au décompte du canevas, TOUS les
moteurs candidats ont déjà un fichier de tests dédié. Le critère
pertinent est donc la MINCEUR de la couverture : ratio lignes de
tests / lignes de moteur. Le plus mince de vertex/engines/ :

```text
ratio 0.19  analysis.py — 333 lignes de moteur, 4 tests (63 lignes)
(suivants : strategy_fit 0.35, postmortem 0.61, market_lens 0.66…)
```

`analysis.py` est LE cœur : `analyse()` transforme l'OHLCV en fiche
technique complète (régime, détections, anomalies, plan, score) pour
chaque titre du scan. Le golden existant fige UN scénario — aucune
branche de détection n'était couverte.

## 2. Ce qui est figé (`tests/test_analysis_lot146.py`, 17 tests)

```text
Robustesse d'entrée : flux SANS colonne Volume (indices/ETF Stooq)
  → volx 1.0, series.volume None, jamais de KeyError ; historique
  court (60 barres) → repli SMA→EWM, fiche complète, JSON sans NaN
Profils : DÉFENSIF (titre calme + beta 0.5 + dividende + Utilities)
  et ÉQUILIBRÉ (sans fondamentaux) — le golden figeait déjà OFFENSIF
Radar d'anomalies : gap haussier +6 % détecté (clé, libellé, sévérité
  1-3) ; pic de volume 6× (volspike) ; FORMULE du score figée
  (min(100, Σ sévérités × 16)) + niveaux CALME <25 / ACTIF <55 /
  ALERTE ≥55 cohérents sur tout résultat
Détections : cassure confirmée = nouveau plus-haut 20 j ET volume
  ≥1.5× (sans volume → False) ; régime CHOP sur oscillation plate
  (choppiness ≥60)
Plan (3 fixtures) : stop toujours SOUS l'entrée, échelle de TP
  exacte 1R/2R/3R, rr 3.0, stop_dist_atr > 0, setup_quality borné
  0-100, stop_type ∈ {structure, ATR plafond, ATR structure proche}
Transparence du score (3 fixtures) : struct_adj borné [-12, +10] et
  score affiché == clamp(base_score + struct_adj, 0, 100) — une
  seule arithmétique, pas de deuxième vérité
Checklist signaux : 9 clés exactes + sigcount == somme des 7
  signaux comptés
```

## 3. Preuves

```text
python -m pytest tests/test_analysis_lot146.py -q → 17 passed
python -m pytest tests/ -q → 2050 passed, 2 skipped (2033 + 17)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 147 : caractérisation suivante par ratio croissant —
`strategy_fit.py` (0.35 — couche stratégie source unique :
vehicle_of / strat_score, servie par le scan) puis postmortem (0.61)
/ market_lens (0.66).

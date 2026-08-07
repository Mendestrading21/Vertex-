# SKYLER V2 — LOT 180 : caractérisation des données analystes profondes

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-180`
(base : `integration/vertex-skyler-v2` @ `18a6606`, lot 179 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey honnête : scheduler registry (lot 109), live_stream (lot 99)
et traces/logging (dormants — AUCUN appelant production, non
caractérisés à dessein) écartés. La vraie lacune :
`vertex/data_sources/analyst_deep.py` (226 lignes, ZÉRO test,
1 appelant production — la fiche titre de terminal.py). Testé HORS
LIGNE : faux ticker pandas, faux module yfinance injecté dans
sys.modules, cache isolé.

## 2. Ce qui est figé (`tests/test_analyst_deep_lot180.py`, 10 tests)

```text
Lecture robuste — NaN écarté (jamais un chiffre fantôme) ;
  révisions BPA : net30 exact + tendance up/down, repli '0y' → '0q' ;
  surprises : le trimestre À VENIR (Reported EPS NaN) séparé en
  `next`, fenêtre N publiés, beats 2/3 + moyenne 5.6 exacte ;
  notes d'analystes : les plus récentes d'abord, cap 6, firm
  bornée 40 ; initiés : solde 1200 + biais buy, transaction
  non classable (Gift) → None jamais un flux inventé
Politique de cache — symbole vide → None ; cache FRAIS servi sans
  AUCUN appel réseau (faux yfinance qui explose si touché —
  prouvé) ; yfinance mort + TTL dépassé → le cache PÉRIMÉ est servi
  plutôt que rien ; échec TOTAL (aucun bloc) → jamais persisté
  (on ne cache pas un échec) et rien écrit sur disque
```

## 3. Preuves

```text
python -m pytest tests/test_analyst_deep_lot180.py -q → 10 passed
python -m pytest tests/ -q → 2416 passed, 2 skipped (2406 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

Tranche 176-180 TERMINÉE (mini-bilan dans STATUS.md). LOT 181 :
survey pour la direction suivante — data_sources restants minces
(source_router prod=0, ibkr_scheduler tests=2), pages UI, ou
correctifs utilisateur.

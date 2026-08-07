# SKYLER V2 — LOT 149 : caractérisation prisme marché + statistiques

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-149`
(base : `integration/vertex-skyler-v2` @ `87b8642`, lot 148 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié. Deux moteurs minces combinés (comme prévu au canevas).

## 1. Cibles

`vertex/engines/market_lens.py` (77 lignes, ratio 0.66) — SOURCE
UNIQUE du score marché /100, servie par 3 routes (feeds.py:31,
decision_api.py:92, command.py:30) : climat, rang du secteur,
alignement aux trois niveaux. `vertex/engines/stats.py` (48 lignes,
ratio 0.77) — Spearman de l'edge + médianes de valorisation par
secteur.

## 2. Ce qui est figé (`tests/test_market_lens_stats_lot149.py`, 13 tests)

```text
climate — arithmétique exacte (93 porteur) ; bornes EXACTES des
  bandes : FAVORABLE ≥62 (62 oui, 61 non), DANGEREUX <40 (40
  NEUTRE, 39 DANGEREUX) ; DIVERGENCE réelle DOCUMENTÉE : même
  formule que le tilt strategy_fit mais FAVORABLE à 62 ici contre
  65 là-bas ; None ET {} (falsy) → None (pas de climat inventé)
sector_standing — tiers supérieur porteur (n=6 → 2 rangs ; n=2 →
  seul le rang 1) ; score non numérique → classé DERNIER avec
  avg_score None (honnête, jamais un chiffre inventé) ; secteur
  hors scan → None
build — frontière titre fort à 70 STRICTE (69.9 non, 70 oui) ;
  2 feux verts dont le titre → « partiellement aligné » (PAS
  « à contre-courant », réservé au titre fort SEUL)
spearman — frontière 8 points exacte (7 → None, 8 → valeur) ;
  LIMITE DOCUMENTÉE : rangs ordinaux (double argsort, pas de rangs
  fractionnaires pour les égalités) → une série CONSTANTE
  « corrèle » à 1.0 avec une série croissante au lieu d'un
  indéfini — pathologique en réel, le changer = décision explicite
sector_medians — bornes strictes 0 < pe < 250 (250 et -5 exclus),
  n compte TOUS les membres ; secteur sans pe NI fwd_pe
  entièrement absent (pas de fiche valorisation sans valorisation)
```

## 3. Preuves

```text
python -m pytest tests/test_market_lens_stats_lot149.py -q → 13 passed
python -m pytest tests/ -q → 2090 passed, 2 skipped (2077 + 13)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 150 : `session_digest.py` (0.80) + MINI-BILAN 146-150
obligatoire.

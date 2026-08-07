# SKYLER V2 — LOT 179 : caractérisation de l'observabilité (§37)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-179`
(base : `integration/vertex-skyler-v2` @ `e5961ec`, lot 178 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey honnête : le webhook TradingView (candidat prévu) est COMPLET
(12 tests — secret, replay/dédup, validation, jamais d'achat direct,
purge sous charge) ; client-log, config (lot 111, secrets jamais
renvoyés) et startup (lot 105) aussi. La vraie lacune :
`vertex/observability/metrics.py` (58 l, ZÉRO test direct —
l'instrumentation du Strategy OS servie par /api/diagnostics) et les
sections de `diagnostics.py`.

## 2. Ce qui est figé (`tests/test_observability_lot179.py`, 9 tests)

```text
Metrics (instance fraîche, jamais le singleton) — compteurs qui
  CUMULENT (défaut +1, valeur libre) vs jauges qui ÉCRASENT ;
  percentiles EXACTS (100 échantillons 1..100 → p50 51.0, p95 95.0,
  max 100.0 ; échantillon unique → les trois confondus) ; anneau de
  200 mesures (250 envoyées → n 200, fenêtre 51..250, p50 151.0 —
  bornage mémoire) ; timer contextuel qui mesure ET propage
  l'exception (__exit__ False — jamais avalée, durée enregistrée
  quand même) ; snapshot = COPIE isolée (muter le snapshot ne
  touche pas le registre)
system_diagnostics — sections STRICTEMENT optionnelles (sans
  dépendance → {metrics} seul, rien d'inventé) ; avec dépendances
  (contrats status()/stats()) → scan/ibkr_scheduler/alerts/ai/
  tradingview présents tels quels
data_quality_report — tous les paquets COMPTÉS (by_quality 30) mais
  liste des dégradés bornée à 20 et warnings à 3 (réponse bornée)
```

## 3. Preuves

```text
python -m pytest tests/test_observability_lot179.py -q → 9 passed
python -m pytest tests/ -q → 2406 passed, 2 skipped (2397 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 180 : dernier lot de la tranche + MINI-BILAN 176-180 obligatoire
(176 clôture routes, 177 XSS bout en bout, 178 backup desk, 179
observabilité, 180 à livrer — PR #209-#213). Candidats : scheduler
registry (lot 109 à vérifier), vertex/observability/traces-logging,
ou survey général.

# SKYLER V2 — LOT 168 : caractérisation de la stratégie options personnalisée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-168`
(base : `integration/vertex-skyler-v2` @ `ece4854`, lot 167 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/strategy/legacy_adapter.py` (272 lignes, 0 test — VIVANT :
servi par command et terminal). La stratégie options personnalisée :
échelle 1/2/3/6/9/12 mois à delta MIX, mark-to-market Black-Scholes
en cours de route (cœur de la spéculation : on ne garde pas jusqu'à
l'échéance), constructeur de portefeuille cœur/satellites. Pur (BS
interne) — aucun réseau, testé directement.

## 2. Ce qui est figé (`tests/test_legacy_adapter_lot168.py`, 21 tests)

```text
_bias — mots-clés (RISK-ON → favorable, stress → dangerous) et
  seuils EXACTS du score : ≥60 favorable, <40 dangerous, entre →
  neutral ; {} et None → neutral
Briques — proxy IV borné [0.22, 1.10] (défaut ATR 2 % → 0.317) ;
  pas de strike 1/2.5/5/10 selon le cours (<50/<100/<250/≥250) ;
  durée de détention ~1/3 de l'échéance bornée 5-45 j
_leg — breakeven call = strike + prime, put = strike − prime ;
  règles de sortie EXACTES (+50 % → 1.5×prime, stop −50 % →
  0.5×prime) ; alerte théta = dte − 45 (1 mois → 0 clampé) ;
  scénarios ORDONNÉS pess < prob < except ; cible technique du
  plan valorisée en cours de route
build — RÉGIME DANGEREUX impose le PUT même sur conviction
  haussière (défense d'abord) ; favorable + haussier → CALL avec
  les 6 horizons
build_portfolio — rôles CŒUR×3 puis SATELLITE×2, cash = capital −
  déployé (arithmétique fermée), maxloss = déployé (achat sec),
  risque par position borné ~10 % du capital ; sans candidats →
  portefeuille vide honnête (cash = capital)
```

## 3. Preuves

```text
python -m pytest tests/test_legacy_adapter_lot168.py -q → 21 passed
python -m pytest tests/ -q → 2310 passed, 2 skipped (2289 + 21)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 169 : data/company.py (340 l, 0.39 — yfinance à mocker) OU
data/universe.py (324 l, 0.56). Mini-bilan 166-170 au lot 170.

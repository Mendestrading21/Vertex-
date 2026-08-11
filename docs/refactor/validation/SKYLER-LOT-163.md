# SKYLER V2 — LOT 163 : exposition factorielle + remplacements + vérif legacy

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-163`
(base : `integration/vertex-skyler-v2` @ `c1fee90`, lot 162 fusionné).
Lot TESTS + VÉRIFICATION, aucun code moteur ni UI modifié.

## 1. Vérification de VIE des deux legacy (exigée par le canevas)

**Les deux sont VIVANTS** — pas de code mort :

```text
portfolio/legacy_basket_risk.py (99 l) → importé par
  routes/analysis_api.py, routes/command.py ET
  portfolio/risk_engine.py
strategy/legacy_adapter.py (272 l) → importé par
  routes/command.py ET terminal.py
```

Ils restent candidats à une caractérisation future (file), mais
aucun signalement de code mort n'est justifié.

## 2. Ce qui est figé (`tests/test_factor_replacement_lot163.py`, 8 tests)

`vertex/portfolio/factor_exposure.py` (29 l) et
`vertex/portfolio/replacement_engine.py` (36 l) — dépendances
research/ monkeypatchées (déterministe, léger).

```text
factor_exposure — pondération par les POIDS RÉELS (0.5×2.0 +
  0.5×1.0 = 1.5, couverture 100 % → pas de note) ; couverture
  partielle SIGNALÉE (50 % → « exposition indicative ») ; aucune
  donnée → value None (jamais un zéro inventé) ; les 10 facteurs
  toujours présents dans le contrat
replacement_engine — place disponible → pas de remplacement ;
  bloqué → la plus FAIBLE du rôle proposée avec « décision humaine
  requise » (jamais une exécution) ; candidat moins bon que la
  plus faible → « déconseillé » ; rôle sans membre → pool GLOBAL
  (comportement documenté) ; sans scores → départage au défaut 50
  mais score AFFICHÉ None (pas un 50 inventé à l'écran)
```

## 3. Preuves

```text
python -m pytest tests/test_factor_replacement_lot163.py -q → 8 passed
python -m pytest tests/ -q → 2255 passed, 2 skipped (2247 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 164 : caractériser un des deux legacy VIVANTS
(legacy_basket_risk 99 l — servi par 3 appelants — en priorité) ;
puis ai/briefs (0.33) / ai/copilot (0.37) / data/company (0.39) /
portfolio/risk_engine (0.52). Mini-bilan 161-165 au lot 165.

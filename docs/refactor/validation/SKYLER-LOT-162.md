# SKYLER V2 — LOT 162 : caractérisation du trio audit IA + contexte + rôles

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-162`
(base : `integration/vertex-skyler-v2` @ `bb8c565`, lot 161 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié. Trois petits
modules zéro-test combinés (~81 lignes).

## 1. Cibles

`vertex/ai/audit.py` (37 l — journal des appels IA, servi par
strategy_os_api), `vertex/ai/strategy_context.py` (25 l — le
contexte injecté dans CHAQUE analyse IA, porteur des rappels
d'invariants) et `vertex/portfolio/team_roles.py` (19 l — rôles de
l'équipe §25).

## 2. Ce qui est figé (`tests/test_ai_portfolio_trio_lot162.py`, 8 tests)

```text
audit — journal BORNÉ à 200 entrées (deque : 250 enregistrées →
  les 200 plus récentes seulement) ; stats ok/fallbacks comptées ;
  erreurs TRONQUÉES à 5 par entrée (pas de fuite verbeuse) ;
  journal neuf honnêtement vide
strategy_context — contrat 10 clés exact ; bornes cohérentes
  (positions min ≤ max, DTE min ≤ max, décisions jamais vides) ;
  les 4 RAPPELS D'INVARIANTS injectés dans chaque analyse IA
  figés mot pour mot : « lecture seule absolue: aucun ordre »,
  « moteur exécutif déterministe », « aucune promesse de
  performance », « jamais inventer » — les affaiblir = décision
  explicite qui cassera ce test
team_roles — les 4 rôles dans l'ordre terrain (ATTACKER,
  MIDFIELDER, DEFENDER, GOALKEEPER) ; descriptions cohérentes avec
  ROLE_TARGETS du modèle (une seule vérité d'effectifs) ; profils
  non vides ; DEFENDER/GOALKEEPER sans horizon (positions de fond)
```

## 3. Preuves

```text
python -m pytest tests/test_ai_portfolio_trio_lot162.py -q → 8 passed
python -m pytest tests/ -q → 2247 passed, 2 skipped (2239 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 163 : factor_exposure (29 l) + replacement_engine (36 l)
— fixtures team_engine à évaluer ; vérifier VIVANTS les deux legacy
(legacy_basket_risk 99 l, legacy_adapter 272 l) — si morts :
constat + signalement code mort, pas de suppression sans accord.
Mini-bilan 161-165 au lot 165.

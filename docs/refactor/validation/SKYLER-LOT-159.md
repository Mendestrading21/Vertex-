# SKYLER V2 — LOT 159 : horloge de marché + inventaire du nouveau périmètre

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-159`
(base : `integration/vertex-skyler-v2` @ `f26cf1c`, lot 158 fusionné).
Lot TESTS + INVENTAIRE, aucun code moteur ni UI modifié.

## 1. (a) Complément market_clock (`tests/test_market_clock_lot159.py`, 5 tests)

`vertex/services/market_clock.py` (41 lignes) — les 4 tests
existants couvrent 9h30/16h/20h et le week-end. Figé en plus :

```text
Borne pré-marché 4h00 EXACTE (3h59 fermé, 4h00 pre)
Vendredi soir : 19h59 after, 20h00 fermé — et samedi fermé même
  en pleine « séance »
Format du champ et : « 09:05 ET » (HH:MM zéro-paddé)
LIMITE DOCUMENTÉE : PAS de calendrier de jours fériés — le
  1er janvier 2026 (un jeudi) est affiché « open » à midi.
  L'horloge ne connaît que l'heure et le jour de semaine ;
  ajouter un calendrier NYSE = décision explicite future, ce
  test rendra le changement visible
Contrat market_status : {open, session, et}
```

## 2. (b) INVENTAIRE du nouveau périmètre (file des prochains lots)

Ratio lignes-tests/lignes-module sur vertex/ai/, vertex/data/,
vertex/strategy/, vertex/portfolio/ — 11 modules à ZÉRO test :

```text
0.00  portfolio/correlation.py         42 l   ← candidats prioritaires :
0.00  portfolio/factor_exposure.py     29 l     la FAMILLE RISQUE
0.00  portfolio/replacement_engine.py  36 l     PORTEFEUILLE (4 modules,
0.00  portfolio/stress_tests.py        85 l     ~192 l, à combiner)
0.00  portfolio/team_roles.py          19 l
0.00  data/constituents.py            112 l   ← univers des titres
0.00  data/_constituents_static.py     59 l
0.00  ai/audit.py                      37 l
0.00  ai/strategy_context.py           25 l
0.00  portfolio/legacy_basket_risk.py  99 l   (legacy — vérifier vivant)
0.00  strategy/legacy_adapter.py      272 l   (legacy — vérifier vivant)
Puis : ai/briefs.py (0.33), ai/copilot.py (0.37),
data/company.py (0.39), portfolio/risk_engine.py (0.52),
data/universe.py (0.56)
```

## 3. Preuves

```text
python -m pytest tests/test_market_clock_lot159.py -q → 5 passed
python -m pytest tests/ -q → 2219 passed, 2 skipped (2214 + 5)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 160 : la FAMILLE RISQUE PORTEFEUILLE (correlation +
factor_exposure + stress_tests + replacement_engine — vérifier les
appelants) + MINI-BILAN 156-160 obligatoire.

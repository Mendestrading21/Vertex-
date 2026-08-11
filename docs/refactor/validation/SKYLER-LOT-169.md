# SKYLER V2 — LOT 169 : caractérisation du profil d'entreprise

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-169`
(base : `integration/vertex-skyler-v2` @ `01e5f10`, lot 168 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/data/company.py` (340 lignes, ratio 0.39) — le profil
d'entreprise « lent » (cache hebdo + couche curée hors ligne + fetch
yfinance côté utilisateur). Testé HORS LIGNE : cache isolé,
`_fetch_profile` monkeypatché — aucun appel yfinance réel.

## 2. Ce qui est figé (`tests/test_company_lot169.py`, 9 tests)

```text
Données curées — INVARIANT : les 20 répartitions de segments de CA
  somment TOUTES exactement à 100 % ; démo → couche curée servie
  (Jensen Huang, fondée 1993, Data Center 78 %, drapeau 🇺🇸) avec
  stale True SIGNALÉ à l'UI ; symbole inconnu → squelette honnête
  (None partout, l'UI affichera « — », jamais inventé)
Ordre cache/fetch/curé — fetch réussi → cache écrit + stale
  False ; second appel servi du cache SANS réseau ; entrée d'un
  SCHÉMA antérieur (_v < 3) → re-fetch automatique ; fetch mort →
  secours curé (« jamais de page vide »)
peers — pairs de la même industrie, soi-même exclu, cap 4
sector_medians — seuil 3 membres (secteur solo absent), borne
  PE < 250 stricte, marge/croissance/ROE convertis en % ; le memo
  tient MÊME VIDE (memo sur le timestamp — le cache 1.4 Mo n'est
  pas reparsé à chaque appel)
```

## 3. Preuves

```text
python -m pytest tests/test_company_lot169.py -q → 9 passed
python -m pytest tests/ -q → 2319 passed, 2 skipped (2310 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 170 : `data/universe.py` (324 l, 0.56 — dernier de la file) +
MINI-BILAN 166-170 obligatoire.

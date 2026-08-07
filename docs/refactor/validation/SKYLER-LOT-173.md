# SKYLER V2 — LOT 173 : honnêteté HTTP du moteur de suivi

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-173`
(base : `integration/vertex-skyler-v2` @ `0fe8eb2`, lot 172 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey : la mémoire Skyler d'analysis_api est très couverte (17
fichiers de tests sur /api/skyler/memory). La vraie lacune :
`vertex/app/routes/tracking_api.py` (175 lignes) — **le cycle de vie
/api/tracking/<id> (GET/PATCH), /performance, /stop, /restart,
/history était à ZÉRO test** ; seuls la liste GET et le POST de
création étaient couverts (full_system_integration, post_routes).

## 2. Ce qui est figé (`tests/test_tracking_api_lot173.py`, 10 tests)

```text
Refus explicites — id inconnu → 404 « suivi introuvable » sur les
  5 sous-routes ; création sans symbole → 400 « symbol requis »
Création honnête — action inconnue du scan → 201 mais statut
  DATA_REQUIRED avec reference_price None (JAMAIS un prix inventé) ;
  action cotée → ACTIVE, référence LAST/« scan » (provenance tracée),
  benchmark SPY, is_hypothetical True ; option → quote du body,
  référence MID exacte ((3.0+3.4)/2 = 3.2)
Performance — action au prix courant RÉEL du scan (+10 % exact,
  high/drawdown), étiquette imposée « Suivi HYPOTHÉTIQUE : aucune
  position réelle… » dans limitations ; option : le mark est EXIGÉ
  en paramètre (?mark=4.08 → +27.5 %), sans mark → current/return
  None — jamais un chiffre sans source
Stop — gel du résultat au prix réel du scan (final_price, return,
  MFE/MAE exacts, raison conservée, STOPPED horodaté)
Restart — identifiant NEUF (201), repart du prix courant, l'ancien
  suivi reste GELÉ (history : final + stopped_at intacts)
Invariant — aucun verbe d'ordre dans la source du module
```

## 3. Preuves

```text
python -m pytest tests/test_tracking_api_lot173.py -q → 10 passed
python -m pytest tests/ -q → 2357 passed, 2 skipped (2347 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 174 : poursuivre la tournée des routes — sonder feeds.py
(/api/options, /api/comite, /api/weekly), ai_api (/api/copilot/ask
POST), session_api, opportunities_api. MINI-BILAN 171-175 au lot 175.

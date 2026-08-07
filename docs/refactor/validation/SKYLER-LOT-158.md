# SKYLER V2 — LOT 158 : caractérisation de la règle de fraîcheur du Live Engine

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-158`
(base : `integration/vertex-skyler-v2` @ `e84fc8a`, lot 157 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/services/live_engine.py` (258 lignes, ratio 0.64) — LE
moteur de synchronisation dont dépendent toutes les pages ; le Sync
Center et la vue Système affichent ses états. Les 13 tests existants
couvrent les flux (status/refresh/forçage/routes) — ce lot fige les
BORNES de sa partie pure : `calculate_freshness` (la règle unique),
les libellés et le cycle de forçage.

## 2. Ce qui est figé (`tests/test_live_engine_lot158.py`, 19 tests)

```text
Bornes STRICTES par domaine (7 domaines paramétrés) : à la borne
  exacte on bascule DÉJÀ — age == frais → stale, age == rassis →
  offline. Seuils publiés figés : prices 5 min/30 min · options
  1 h/6 h · companies 48 h/8 j · news 2 h/12 h · calendar 1 j/4 j ·
  weekly 8 j/15 j · ai 5 min/30 min
Domaine inconnu → défauts (600 s, 3600 s)
Libellés humains — bascules d'unités EXACTES : 59 s « il y a
  59s » / 60 s « 1 min » / 3600 « 1 h » / 86400 « 1 j »
Âge None → ('offline', 'jamais synchronisé') — honnête
Forçage — wait_force réveillé → True et l'événement est CONSOMMÉ
  (la même attente redevient timeout False) ; force_event rend
  toujours LE même objet Event par domaine (boucles et Sync Center
  partagent l'objet)
```

## 3. Preuves

```text
python -m pytest tests/test_live_engine_lot158.py -q → 19 passed
python -m pytest tests/ -q → 2214 passed, 2 skipped (2195 + 19)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 159 : `market_clock.py` (41 l) + inventaire d'un NOUVEAU
périmètre (vertex/ai/, vertex/data/, vertex/strategy/,
vertex/portfolio/ par ratio) pour construire la file suivante.
Mini-bilan 156-160 au lot 160.

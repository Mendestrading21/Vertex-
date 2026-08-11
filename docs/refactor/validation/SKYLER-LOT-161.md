# SKYLER V2 — LOT 161 : caractérisation des constituants d'indices

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-161`
(base : `integration/vertex-skyler-v2` @ `36f013e`, lot 160 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/data/constituents.py` (112 lignes, 0 test direct) — nourrit
`data/universe.py` : les constituants S&P 500 + Nasdaq 100 + Dow au
DÉMARRAGE (Wikipedia + cache disque + snapshot statique embarqué —
« le démarrage n'est JAMAIS bloqué »). Testé SANS aucun accès
réseau : fetch monkeypatché, cache isolé en tmp_path.

## 2. Ce qui est figé (`tests/test_constituents_lot161.py`, 9 tests)

```text
Normalisation — yfinance : majuscules, trim, points → tirets
  (BRK.B → BRK-B)
Filtrage — tickers implausibles rejetés (nombres, > 6 lettres,
  vides), doublons éliminés en conservant l'ordre
Snapshot statique — intégrité du filet de sécurité : ≥ 400/80/25
  titres ET déjà normalisé (_clean idempotent dessus)
ORDRE DE RÉSOLUTION (le cœur) :
  · sans cache + réseau mort → 'static' (démarrage jamais bloqué),
    union dédupliquée
  · cache frais (< 12 h) → 'cache', AUCUN appel réseau
  · force=True → fetch tenté même sur cache frais ; s'il échoue →
    'cache-stale' (les données périmées valent mieux que rien)
  · liste VIDE dans le cache → repli statique PAR INDICE (les
    autres listes du cache restent servies)
  · fetch réussi → 'live' ET cache persisté sur disque
Garde-fou parsing — listes anormalement courtes (< 400/80/25) =
  parsing Wikipedia cassé → ValueError explicite (le fallback
  prend le relais en amont) ; get_index_members ne lève JAMAIS
```

## 3. Preuves

```text
python -m pytest tests/test_constituents_lot161.py -q → 9 passed
python -m pytest tests/ -q → 2239 passed, 2 skipped (2230 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 162 : file du périmètre — trio ai/audit (37 l) +
ai/strategy_context (25 l) + portfolio/team_roles (19 l) à
combiner ; puis factor_exposure + replacement_engine ; legacy à
vérifier. Mini-bilan 161-165 au lot 165.

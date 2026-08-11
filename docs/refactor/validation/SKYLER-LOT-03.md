# SKYLER V2 — LOT 03 — MARKET INTELLIGENCE (MarketContext canonique)

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-03-market-context`
> Base : `agent/skyler-v2-lot-02-constitution-v2`
> Périmètre : nouveau moteur pur + 1 route additive — aucun moteur existant modifié

## 1. Constat (inventaire des sources réelles)

L'état marché vivait éclaté et non typé : `scan_state['market']` (regime/breadth/vix/risk,
lens du scan), `scan_state['market_ctx']` (spy_regime/vix/vix_band/roro/breadth),
`/api/market/summary` (agrégat plat sans provenance), `/api/market/regime`
(classification §24 sans fraîcheur). Aucune dimension ne portait source/unité/statut ;
un VIX divergent entre les deux états n'était visible nulle part ; « ce qui a changé
depuis la dernière session » n'existait pas.

## 2. Décision

Créer `vertex/engines/market_context.py` — fonction PURE `build(scan_state, prev,
now, demo)` (horloge injectée, déterministe, JSON-sérialisable) :

- **12 dimensions typées** au contrat FactValue `{value, unit, source, as_of, status}` :
  5 réellement alimentées (spy_trend, breadth_ma200_pct, vix+bande, leadership, roro)
  et 7 déclarées **MISSING honnêtes** (rates_curve, dollar, credit_spreads,
  vol_term_structure, dispersion, liquidity, cross_asset) — jamais d'approximation
  non étiquetée ;
- statuts : LIVE / STALE (> 2100 s, aligné constants) / DEMO / MISSING / **CONFLICTED**
  (VIX présent dans les deux sources avec écart > 1 pt → statut + entrée `conflicts`
  avec les deux valeurs, jamais moyenné en douce) ;
- `freshness_floor` = as_of du scan (un contexte n'est jamais plus frais que sa donnée) ;
- **régime** : moteur déterministe §24 réutilisé (`classify_regime`) + **transition**
  `{from, to, changed}` contre le contexte précédent (None honnête sans précédent) ;
- **`changes_since_prev`** : régime, VIX (≥ 2 pts), bande VIX, breadth (≥ 5 pts),
  leadership — liste vide si rien n'a changé (pas de bruit inventé) ;
- route additive `GET /api/market/context` (feeds.py) : lit le contexte précédent via
  `persist` (`market_context_last.json`, gitignoré) et ne persiste que lorsqu'un
  nouveau scan republie (`as_of` différent) — base du « depuis la dernière session ».

## 3. Fichiers modifiés

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/market_context.py` | nouveau moteur pur | faible |
| `vertex/app/routes/feeds.py` | +1 route additive `/api/market/context` | faible |
| `tests/test_market_context.py` | nouveau — 11 tests | faible |
| `.gitignore` | + `market_context_last.json` (runtime) | nul |

## 4. Tests rouges avant

```text
python -m pytest tests/test_market_context.py -q → collection error (module inexistant)
```

## 5. Tests après

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_market_context.py -q → 11 passed
python -m pytest tests/ -q → 1200 passed, 2 skipped
```

Couverture exigée par le runbook : provenance complète (LIVE), MISSING ≠ 0,
STALE (> 2100 s), DEMO étiqueté, état vide honnête (UNKNOWN, as_of None),
**CONFLICTED** avec les deux valeurs, régime + confiance, transition avec/sans
précédent, diff listé/vide, déterminisme JSON strict, route de bout en bout.

## 6. Validation runtime (DEMO=1 NO_IBKR=1)

`GET /api/market/context` → `schema_version: 1`, `demo: true`, `vix 12.7 DEMO`
(bande « calme »), régime **UNKNOWN à confiance 0.0** car le mode démo n'alimente
que 2 dimensions (< 3 → dégradation honnête du moteur §24, note explicite),
7+2 dimensions MISSING listées, `changes_since_prev` vide au premier passage.
`/api/client-log` = 0.

## 7. Invariants vérifiés

- [x] aucune dimension inventée ; absent = MISSING ; conflit visible non résolu ;
- [x] verdict jamais plus frais que la donnée (`freshness_floor`) ;
- [x] moteur de régime EXISTANT réutilisé (aucun calcul financier nouveau) ;
- [x] fonction pure, horloge injectée, déterminisme prouvé par test ;
- [x] READONLY ; fichier runtime gitignoré ; aucun secret.

## 8. Risques restants

1. 7 dimensions du schéma cible attendent leurs sources réelles (taux, dollar,
   crédit, terme de vol, dispersion, liquidité, cross-asset) — elles resteront
   MISSING tant qu'une source honnête n'est pas branchée (lots futurs).
2. En mode démo, spy_trend/leadership sont MISSING (le lens démo ne les produit
   pas) → régime UNKNOWN ; en mode réel les 5 dimensions s'alimentent.
3. Le SkylerPacket (lot 5) consommera ce contexte — pas encore branché.

## 9. Verdict

**GO** — moteur pur prouvé (11 tests), route servie en runtime, honnêteté
missing/stale/demo/conflit démontrée, suite 1200 verte.

## 10. Prochaine étape autorisée

`/vertex-skyler-v2 lot-4` (news, catalyseurs et anomalies — série OHLCV canonique).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**

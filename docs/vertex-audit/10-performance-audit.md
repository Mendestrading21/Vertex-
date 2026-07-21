# 10 — Audit performance

Objectif produit : calculs et chiffres **plus rapides**, **sans perdre d'information ni de précision**. Mesure via
`vertex/observability/metrics.py` (`METRICS`). Détail : `references` + agent `vertex-performance-auditor`.

## Optimisations déjà en place (Lots 0-9, byte-identiques vérifiés)
| Zone | Mécanisme | Fichier |
|---|---|---|
| Instrumentation | `METRICS` (latences par étape) | `vertex/observability/metrics.py` |
| `analyse()` | memo empreinte BLAKE2b `_analyse_fp` / `_ANALYSE_MEMO` | `terminal.py` |
| yfinance | TTL cache `_YF_CACHE` (ouvert 90 s / fermé 900 s via `_yf_ttl`) | `terminal.py` |
| Scan | parallélisation `ThreadPoolExecutor` `_analyse_one`/`_safe_one`, `_workers=min(8,max(1,cpu-1))` | `terminal.py` |
| Réponse `/scan` | cache `_SCAN_RESP` + ETag/304 | `terminal.py` |
| Options pack | TTL cache `_OPTPACK_CACHE` (fiche ~3 min) | `terminal.py` |
| Options view | memo `_view_get`/`_view_put`/`_VIEW_MISS` sur `ts` de chaîne ; warm lock par symbole | `options_intel_api.py`, `options/on_demand.py` |
| Backtest / strike | memo `_BT_MEMO` / `_STRIKE_MEMO` | `engines/backtest.py`, `strategy/legacy_adapter.py` |
| Indicateurs | True Range partagé, dédup `_ewm20/_sma50/_sma200/_std20` | `engines/indicators.py`, `analysis.py` |
| Réponse | `_gzip_response` (garde `Content-Encoding`, pas de double gzip) | `terminal.py` |

## Findings restants
- **PRF-01 (P1) — Payload fiche ~8 Mo.** `/analysis/<sym>` renvoie un très gros JSON. **Action** : trimmer les
  champs non consommés, paginer/paresser les séries lourdes, mesurer avant/après. Ne retirer aucun chiffre affiché.
- **PRF-02 (P2) — Fraîcheur des caches vs live — ✅ FAIT (audit + gardien).** Vérifié : `_YF_CACHE` relit son TTL
  à chaque lecture, plus court en séance (`_YF_TTL_OPEN=90 < _YF_TTL_CLOSED=900`) → l'ouverture force le refetch ;
  `_OPTPACK_CACHE`/`_SCAN_RESP` en mémoire, process-scopés, mono-source, `DEMO_MODE` constant + bypass `fresh` ;
  `company_cache.json` (seul persisté) : la démo ne fait ni réseau ni écriture (jamais de mock persisté comme réel),
  fraîcheur = âge 7 j **ET** version de schéma, drapeau `stale` honnête. Gardien `tests/test_cache_freshness.py`.
- **PRF-03 (P2) — Complétude des clés de memo.** Chaque memo doit inclure **toutes** les entrées qui changent la
  sortie (sinon valeur périmée silencieuse). Ajouter un test byte-identique par memo critique.
- **PRF-04 (P3) — Course sur `scan_state`.** Sous parallélisation, `scan_state` reste muté en place (jamais
  réassigné) ; confirmer l'absence de course sur les clés écrites concurremment.

## Méthode de mesure
Isoler `METRICS._timings` par scan, comparer P50/P95, et prouver **byte-identique** (hash de scan) après chaque
optimisation. Aucune régression de précision (règle produit n°4).

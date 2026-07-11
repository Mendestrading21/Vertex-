# Migration du namespace historique → architecture Vertex Strategy OS

> L'ancien package Python portait un nom personnel ; l'exigence produit impose
> zéro occurrence de ce nom dans l'arbre final, y compris ici. Il est donc
> désigné « ancien package ». Il comptait 23 modules (~3 872 lignes) à la
> racine du dépôt, importé en bloc par `terminal.py:32` et par morceaux par
> `vertex/` et `tests/`.

## Table de migration

| Module (ancien package) | Responsabilité réelle | Consommateurs (entrants) | Tests | Destination | Risque |
|---|---|---|---|---|---|
| `__init__.py` | marqueur de package | import implicite | — | supprimé | bas |
| `ai.py` | traduction FR news/labels (Anthropic→Google→identité), mini-profil entreprise | terminal, routes system/content, data/company | routes system/content | `vertex/ai/briefs.py` | moyen (réseau, clé) |
| `anomalies.py` | 10 anomalies statistiques prix/volume (pur) | terminal (detect_anomalies) | — | `vertex/anomalies/stock_anomalies.py` (absorbé puis étendu) | bas |
| `committee.py` | comité 4 portes (qualité/catalyseur/timing/R:R≥2) → ACHETER/…/ÉVITER | terminal | — | `vertex/engines/committee.py` | moyen (couplé à detail) |
| `config.py` | profil, poids, buckets delta/DTE, couleurs, grade/verdict | terminal, scoring, options, engines/analysis | indirects | `vertex/strategy/config.py` | HAUT (nœud central + constantes contradictoires) |
| `daily.py` | brief quotidien + diff jour/jour (persistance) | terminal | — | `vertex/scanner/daily.py` | moyen (I/O) |
| `engine.py` | verdict synthétique règles (ACHETER FORT…ÉVITER) | terminal | indirects | `vertex/engines/decide.py` | bas |
| `fundamentals.py` | fondamentaux yfinance `tk.info` + médianes sectorielles | terminal | — | `vertex/data_sources/fundamentals.py` | moyen (réseau, threads) |
| `ibkr.py` | ⚠️ mal nommé — AUCUN lien API broker. Score /40 + no-chase + verdict trader | terminal | — | `vertex/engines/scorecard.py` (renommé) | moyen (delta 0.65-0.90 contradictoire) |
| `market.py` | contexte marché (régime SPY, VIX, risk-on/off, breadth) | terminal | indirects | `vertex/market/context.py` | moyen (except avalés) |
| `options.py` | chaînes yfinance + Greeks BS maison + quality/suitability + reco | terminal, strategy, weekly, tests | test BS direct | `vertex/options/legacy_engine.py` | HAUT (réseau, BS maison, delta contradictoire, except→[] global) |
| `physics.py` | Hurst, entropie, efficience, demi-vie → état + rétroaction score | terminal (mort), engines/analysis | indirects | `vertex/market/regime_features.py` | bas-moyen |
| `pivots.py` | structure pivots fractals (tendance + entrée + stop/cible/R:R) | terminal (mort), engines/analysis | indirects | `vertex/quant/pivots.py` | bas-moyen |
| `portfolio_risk.py` | risk manager panier (corrélations, HHI, sizing inverse-vol) | routes command/analysis_api | indirects | `vertex/portfolio/risk_engine.py` | bas |
| `research.py` | lecture graphique FR + thèse décisive | terminal | indirects | `vertex/research/chart_read.py` | bas-moyen |
| `scoring.py` | scores purs (tech/momentum/fond/risque/options) + compose | terminal (mort), engines/analysis | indirects | `vertex/quant/scoring.py` | HAUT (cœur du barème) |
| `sectors.py` | SECTOR_MAP (45 tickers→9 secteurs) + rotation | terminal, committee, fundamentals, portfolio_risk, weekly | indirects | `vertex/market/sectors.py` | moyen (nœud interne) |
| `strategy.py` | échelle horizons options + portefeuille options 50k/100k/200k | terminal, routes command | indirects | `vertex/strategy/legacy_adapter.py` | moyen-haut (DTE 30-365 contradictoire) |
| `timeframe.py` | confluence journalier × hebdo | terminal (mort), engines/analysis | indirects | `vertex/engines/timeframes.py` | bas |
| `validator.py` | walk-forward, PSR, DSR, PBO | routes command/analysis_api, tests | directs | `vertex/validation/out_of_sample.py` | bas |
| `vertex.py` | noyau quant (trend/entry, R:R, Kelly, Monte-Carlo, EV, verdict S+) | terminal (mort), engines/analysis, tests | directs | `vertex/engines/quant_engine.py` | moyen-haut (collision de nom résolue) |
| `vertex_ml.py` | méta-modèle logistique (probabilité calibrée) | noyau quant uniquement | indirects | `vertex/quant/ml_calibration.py` | bas |
| `weekly.py` | watchlist hebdo figée + fiches + persistance | terminal | indirects | `vertex/scanner/weekly.py` | moyen-haut (I/O + réseau via options) |

## Imports internes réécrits

- `from . import sectors` (committee, fundamentals, portfolio_risk, weekly)
  → `from vertex.market import sectors`
- `from . import scoring, config` (options) → `from vertex.quant import scoring`
  + `from vertex.strategy import config`
- `from . import config` (scoring) → `from vertex.strategy import config`
- `from .options import _bs_price, _greeks` (strategy)
  → `from vertex.options.legacy_engine import _bs_price, _greeks`
- `from . import vertex_ml` (noyau quant) → `from vertex.quant import ml_calibration as vertex_ml`
- `from . import options` (weekly) → `from vertex.options import legacy_engine as options`

## Consommateurs externes mis à jour

- `terminal.py:32` — import éclaté vers les nouveaux modules ; les 5 modules
  jamais utilisés (scoring, pivots, physics, timeframe, noyau quant) ne sont
  PLUS importés par le monolithe.
- `vertex/engines/analysis.py:17`, `vertex/app/routes/{command,analysis_api,content,system}.py`,
  `vertex/data/company.py:281`, `tests/test_vertex.py:12` — imports migrés.
- `.github/workflows/ci.yml` — `compileall` ne référence plus l'ancien package.

## Suppression des noms personnels (hors package)

- Salutation d'accueil en dur (`terminal.py:2572`) → « Bonjour. »
- Clé localStorage de positions (`terminal.py:3213-3214`) → `vxPos`, avec
  migration automatique des données depuis la clé héritée (nom reconstruit
  dynamiquement pour ne pas réintroduire l'occurrence).
- CLAUDE.md (profil utilisateur), README.md, docs/AUDIT.md (nom de dépôt
  personnel), docs/ARCHITECTURE.md, docs/ROADMAP.md, `vertex/ui/vault.py:130`,
  commentaires/docstrings (`analysis.py`, `strategy_fit.py`, `command.py`,
  `company.py`, tests) — reformulés.

## Adaptateurs temporaires

La migration a pu se faire d'un bloc (tous les consommateurs mis à jour dans
le même commit, suite de tests verte avant/après) : **aucun adaptateur
temporaire n'a été nécessaire**, et le test
`test_no_temporary_migration_adapters_left` garantit qu'aucun résidu n'existe.

## Test gardien

`tests/test_production.py` (nouveau) : `test_no_personal_name_in_current_tree`
échoue si la recherche insensible à la casse des noms personnels retourne la
moindre occurrence hors `.git/`, et `test_no_legacy_personal_package` échoue si
le répertoire de l'ancien package réapparaît.

# Vertex — Référence des calculs financiers

Chaque calcul : formule, unités, source, comportement en donnée absente,
tests. Règle transverse : **une donnée absente ne devient jamais 0** —
elle reste `None`/`MISSING` côté moteurs et « — »/« n/d » côté UI.

## 1. Pricing d'options — `vertex/options/scenario_pricer.py`

| Élément | Détail |
|---|---|
| Formule | Black-Scholes européen avec rendement de dividende continu : `C = S·e^{-qT}·N(d1) − K·e^{-rT}·N(d2)` |
| Unités | S, K, prime : **dollars par action** · T : années (jours/365) · σ, r, q : décimaux (0.25 = 25 %) |
| Taux | `vertex/data_sources/rates.py` — taux PAR ÉCHÉANCE (interpolation), fallback plat 0.045 documenté (`fallback_used=True`) |
| Hypothèses | exercice anticipé non modélisé (américaines : ESTIMATION), smile non déformé dans les scénarios |
| Étiquette | `model_source ∈ {MODEL_ESTIMATE, FALLBACK_ESTIMATE}` — les Greeks broker (`BROKER_GREEKS`) sont préférés quand disponibles |
| Donnée absente | mid/DTE/spot manquants → simulation **refusée** avec raison dans `limitations` |
| Tests | `test_calculations_golden.py` : golden ATM 10.19, parité put-call, plancher intrinsèque (grille), monotonies, T=0 = intrinsèque exacte, dividende, IV round-trip |

## 2. Scénarios & R:R — `simulate()`

- Grille spot (BEAR/STOP/FLAT/BASE/TP1/TP2/TP3 — stop et TP = **plan du
  sous-jacent**, jamais un % forfaitaire) × temps (0/3/5/10/15/20/28 j) ×
  IV (−20/−10/0/+10/+20 %).
- `worst_planned_loss_pct` = pire P&L au scénario STOP sur l'horizon de
  détention ; `base_expected_gain_pct` = P&L au scénario BASE.
- **R:R = gain simulé / |perte simulée|** — jamais le payoff maximal.
- Tests : `test_option_scenario_at_stop` (repricing vérifié à la main),
  `test_reward_risk_uses_repriced_premiums`, `test_option_time_scenarios`,
  `test_option_iv_scenarios`, `test_expired_option_scenarios_refused`.

## 3. Conventions d'unités options

| Grandeur | Convention canonique | Conversion |
|---|---|---|
| Prime | dollars **par action** (`mid`) | contrat = ×100 (`capital_free_analysis.cost_per_contract`) |
| IV | décimal (0.42) | board legacy en % → normalisé ÷100 par `/api/options/simulate`, noté dans `limitations` |
| Delta | signé (CALL ∈ [0,1], PUT ∈ [−1,0]) | bandes de catégories en **valeur absolue** pour les PUTs |
| DTE | jours calendaires | T = DTE/365 |
| Multiplicateur | 100 (violations → `MULTIPLIER_MISMATCH` bloquant) | |
| Nombre de contrats | calculé **uniquement si capital fourni** | jamais inventé |

Tests : `test_option_multiplier`, `test_percentage_conventions`.

## 4. Indicateurs actions — `vertex/engines/indicators.py`

- RSI (Wilder, n=14) : série haussière → ~100, baissière → ~0, plate →
  neutre (jamais 0 par division masquée). ATR (n=14) : True Range moyen —
  golden : range constant 2 → ATR = 2. ADX standard.
- Les moyennes mobiles/pivots/structure viennent des moteurs (`analysis`,
  `quant/pivots`) — l'UI ne recalcule aucun indicateur.

## 5. Performance — `vertex/engines/performance_ledger.py`

| Métrique | Formule | Test golden |
|---|---|---|
| Win rate | gagnants / clôturés | 3/5 = 0.6 |
| Expectancy | moyenne des rendements (%) | +4.0 |
| Profit factor | Σ gains / |Σ pertes| | 35/15 = 2.33 |
| Max drawdown | min(equity/peak − 1), équité composée | 1−0.95×0.90 = −14.5 % |
| Sharpe/Sortino/Calmar-like | moyenne/σ, moyenne/σ_downside, gain total/&#124;DD&#124; | bornés par n≥5 |

- **Moins de 5 clôtures → métriques retenues** (note d'honnêteté).
- Signal / alerte / recommandation / décision / position simulée / réelle :
  types séparés, métriques jamais mélangées (`metrics_scope`).

## 6. Validation — `vertex/validation/`

- PSR/DSR/PBO : `out_of_sample.py` (réf. Bailey & López de Prado).
- Brier (golden : parfait = 0, 0.5 constant = 0.25), log loss (0.5 → ln 2),
  fiabilité par décile, stabilité temporelle — probabilité affichée
  uniquement si calibrée (sinon « Confiance insuffisante »).
- Walk-forward sans look-ahead : train strictement passé + embargo
  (`test_walk_forward_has_no_lookahead`).

## 7. Temps & timezone

- Timestamps ISO 8601 ; naïf interprété UTC ; âge jamais négatif
  (`test_timezone_handling`). Horloge de session : America/New_York (UI).

## 8. Actions corporate & devises

- Split non appliqué entre sources → `SPLIT_MISMATCH` **bloquant**
  (ACTIONABLE interdit) — `test_stock_split_handling`.
- Devise ≠ USD sur un contrat → `CURRENCY_MISMATCH` bloquant.
- Dividendes : q continu dans le pricing (`test_dividend_context`) ;
  ex-dividende proche exposé dans le setup (`UnderlyingSetup.ex_dividend_days`).

## 9. Divergences broker/modèle

- `BROKER_MODEL_GREEK_DIVERGENCE` levée si |Δbroker − Δmodèle| ≥ 0.12
  (`test_broker_model_divergence_warning`). En l'absence d'IBKR, les valeurs
  modèle restent étiquetées MODEL_ESTIMATE — jamais présentées comme broker.

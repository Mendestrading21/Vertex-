# SKYLER V2 — SCHÉMA CANONIQUE DE DÉCISION

## 1. Objectif

`SkylerPacket` est le contrat unique entre les données, les moteurs analytiques, le moteur de décision, l’interface et la couche de rédaction Claude.

Aucune page ne doit recomposer un verdict à partir de champs dispersés. Aucun prompt ne doit recevoir des données brutes non normalisées.

## 2. Principes

- schéma versionné ;
- validation stricte ;
- sérialisable JSON ;
- aucune valeur NaN/Infinity ;
- unités explicites ;
- timestamps UTC ;
- provenance par valeur critique ;
- distinction fait/estimation/interprétation ;
- champs absents conservés comme absents ;
- compatibilité ascendante documentée ;
- packet immuable après décision.

## 3. Enveloppe

```json
{
  "schema_version": "2.0.0",
  "decision_engine_version": "skyler-decision-1.0.0",
  "packet_id": "uuid",
  "symbol": "NVDA",
  "asset_type": "STOCK",
  "created_at": "2026-08-05T08:00:00Z",
  "analysis_horizon": "90D",
  "mode": "REAL",
  "contexts": {},
  "evidence": [],
  "contradictions": [],
  "scenarios": {},
  "instrument_candidates": [],
  "portfolio_impact": {},
  "decision": {},
  "audit": {}
}
```

## 4. Valeur traçable

```json
{
  "value": 42.5,
  "unit": "percent",
  "source": "IBKR",
  "source_field": "impliedVolatility",
  "as_of": "2026-08-05T07:59:40Z",
  "freshness": "LIVE",
  "status": "AVAILABLE",
  "estimated": false,
  "method": null,
  "confidence": 0.99
}
```

Enums minimum :

### `freshness`

- `LIVE`
- `DELAYED`
- `RECENT`
- `STALE`
- `EXPIRED`
- `UNKNOWN`

### `status`

- `AVAILABLE`
- `MISSING`
- `INSUFFICIENT`
- `ERROR`
- `DEMO`
- `OFFLINE`
- `NOT_APPLICABLE`

### `mode`

- `REAL`
- `DEMO`
- `SIMULATED`
- `BACKTEST`

## 5. Contextes

### MarketContext

- régime principal et secondaires ;
- confiance ;
- indices ;
- breadth ;
- volatilité ;
- taux ;
- crédit ;
- dollar ;
- liquidité ;
- cross-asset ;
- changements depuis session précédente ;
- nouveau risque autorisé ;
- limites de données.

### CompanyContext

- activité ;
- croissance ;
- marges ;
- cash-flow ;
- bilan ;
- valorisation ;
- révisions ;
- qualité ;
- comparaison secteur/historique ;
- inconnues.

### CatalystContext

- événements ;
- dates ;
- horizon ;
- nouveauté ;
- direction ;
- magnitude ;
- confiance ;
- sources ;
- dépendances ;
- scénarios événementiels.

### TechnicalContext

- tendance ;
- momentum ;
- volatilité ;
- niveaux ;
- entrée ;
- invalidation ;
- extension ;
- confirmation ;
- volume ;
- multi-timeframe.

### InstitutionalContext

- relative strength ;
- anomalies ;
- volume ;
- flux ;
- short interest ;
- options positioning ;
- confirmations ;
- limites/proxies.

### OptionsContext

- chaîne et timestamp ;
- liquidité ;
- IV ;
- Greeks ;
- skew ;
- term structure ;
- expected move ;
- GEX ;
- walls ;
- scénarios ;
- earnings risk ;
- candidats TACTICAL/SWING/LEAPS.

### PortfolioContext

- positions ;
- poids ;
- P&L ;
- thèse ;
- concentration ;
- corrélations ;
- budget de risque ;
- drawdown ;
- exposition options ;
- capacité d’ajout ;
- candidat au remplacement.

### DataQualityContext

- complétude ;
- fraîcheur ;
- cohérence ;
- contradictions de sources ;
- champs critiques absents ;
- actionnable autorisé ;
- confidence cap ;
- veto.

## 6. EvidenceClaim

```json
{
  "claim_id": "tech-trend-001",
  "domain": "TECHNICAL",
  "statement": "tendance journalière haussière",
  "polarity": "POSITIVE",
  "strength": 0.81,
  "confidence": 0.90,
  "evidence_level": "F2",
  "source_ids": ["price-daily-001", "ma200-001"],
  "freshness": "RECENT",
  "independent_group": "PRICE_DAILY",
  "estimated": false
}
```

`independent_group` empêche de compter plusieurs métriques dérivées du même fait comme preuves indépendantes.

## 7. Contradiction

```json
{
  "contradiction_id": "conf-001",
  "code": "PRICE_OPTIONS_DIVERGENCE",
  "severity": "MAJOR",
  "claim_ids": ["tech-001", "options-014"],
  "description": "prix haussier mais skew et GEX se dégradent",
  "resolution": "CONFIRMATION_REQUIRED",
  "confidence_cap": 0.60,
  "blocking": false
}
```

## 8. Scénarios

```json
{
  "model_version": "scenario-1.0.0",
  "probabilities_sum": 1.0,
  "pessimistic": {
    "probability": 0.25,
    "target_price": 170.0,
    "return_pct": -12.0,
    "trigger": "guidance réduite",
    "invalidation_effect": "THESIS_BROKEN",
    "assumptions": [],
    "unknowns": []
  },
  "probable": {},
  "exceptional": {},
  "expected_return_pct": 21.4,
  "expected_pnl": null,
  "tail_risk": null,
  "calibration_status": "CALIBRATED"
}
```

## 9. InstrumentCandidate

```json
{
  "instrument_id": "NVDA-20270115-C-150",
  "instrument_type": "LONG_CALL",
  "mandate": "LEAPS",
  "eligible": true,
  "blocking_reasons": [],
  "spot": {},
  "strike": {},
  "expiration": "2027-01-15",
  "dte": 528,
  "premium_executable": {},
  "delta": {},
  "gamma": {},
  "theta": {},
  "vega": {},
  "vanna": {},
  "vomma": {},
  "charm": {},
  "open_interest": {},
  "spread_pct": {},
  "iv_rank": {},
  "iv_percentile": {},
  "probability_of_profit": {},
  "probability_of_double": {},
  "max_loss": {},
  "max_loss_unbounded": false,
  "scenario_matrix_id": "matrix-001",
  "quality_score": 5.2
}
```

## 10. Décision

```json
{
  "final_decision": "ATTENDRE",
  "operational_state": "DECLENCHEMENT_CONDITIONNEL",
  "score_40": 34,
  "grade": "S",
  "confidence": 0.73,
  "confidence_factors": {
    "data_quality": 0.92,
    "agreement": 0.78,
    "robustness": 0.71,
    "calibration": 0.80
  },
  "thesis": "...",
  "why_now": "...",
  "trigger": "...",
  "invalidation": "...",
  "preferred_instrument_id": null,
  "risk_max": "...",
  "devils_advocate": "...",
  "minority_opinion": "...",
  "unknowns": [],
  "recheck_conditions": []
}
```

## 11. Audit

- hash des entrées ;
- versions moteurs ;
- règles appliquées ;
- hard gates ;
- erreurs/refus ;
- analystes exécutés ;
- durée ;
- sources ;
- seed simulations ;
- prompt version Claude ;
- texte généré séparé des champs canoniques.

## 12. Validation

Le packet est refusé si :

- `schema_version` inconnue ;
- timestamp invalide ;
- unité absente sur valeur critique ;
- NaN/infini ;
- probabilités incohérentes ;
- décision hors enum ;
- grade incompatible avec score ;
- instrument interdit marqué éligible ;
- `max_loss_unbounded` absent lorsque pertinent ;
- final decision produite par un autre composant que le Président ;
- mode démo non étiqueté ;
- source critique absente.

## 13. Tests obligatoires

- round-trip JSON ;
- validation des enums ;
- migration de version ;
- refus unités ambiguës ;
- refus probabilités invalides ;
- refus NaN/infini ;
- immutabilité après décision ;
- hash d’entrée stable ;
- Claude ne peut modifier les champs canoniques ;
- champs sensibles filtrés avant sérialisation externe.

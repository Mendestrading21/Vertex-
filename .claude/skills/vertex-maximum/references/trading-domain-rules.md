# Règles du domaine trading & moteur de décision

## Invariant absolu
**Lecture seule.** Aucun ordre transmis, jamais (live ni paper). Vertex prépare/simule/vérifie ; l'humain
transmet dans TWS. Voir `.claude/rules/vertex-safe-editing-rules.md` et `docs/READONLY_SAFETY.md`.

## Séparation des couches (ne jamais mélanger)
`Raw → Normalized → Derived → Signals → Scores → Scenarios → Recommendations → Decisions → Orders(préparés) →
Executions(observées) → Outcomes → Learnings`.

## Moteurs déterministes (source de vérité — `vertex/engines/`, `vertex/market/`, `vertex/quant/`)
- **Verdict exécutif** : `executive_engine.decide()` (constitution : ACHETER/RENFORCER/ATTENDRE/REDUIRE/REFUSER) +
  `decision_stack.evaluate()` (vue comité) + `evidence.gather()` (~10 analystes pondérés par régime, contradictions
  exposées) + `reasoning.build()` (3 scénarios, invalidations, points de bascule). **Même entrée → même verdict.**
- **Physique du prix** (`market/regime_features.py`) : Hurst (variance des différences), entropie de Shannon,
  efficience de Kaufman, demi-vie d'Ornstein-Uhlenbeck.
- **Quant** (`engines/quant_engine.py`) : Monte-Carlo GBM 1200 chemins (seed dérivé du prix → déterministe),
  block-bootstrap 1500, calibration ML. **Plafonds à ne jamais casser : Kelly demi-Kelly capé 12 %,
  p_win ≤ 0,85** (`quant/ml_calibration.py`).
- **Options** : greeks Black-Scholes + IV par bissection + PoP lognormale sur chaînes réelles ; en live, greeks
  **courtier IBKR** (`modelGreeks`) — jamais estimés. Étiqueter broker vs `MODEL_ESTIMATE`.
- **Portefeuille / risque** (`vertex/portfolio/`) : `risk_engine` (HHI, bêta, drawdown, greeks nets),
  `portfolio_guard` (garde-fous), `stress_tests`, `team_engine`.

## Reproductibilité & explicabilité (§9)
Toute décision expose/stocke : version moteur, version règles, données utilisées, timestamp, hypothèses, scores,
seuils, exceptions, résultat, **raison**. Explicabilité : facteurs pour / contre, donnée qui changerait la
décision, limites appliquées, scénario défavorable. Une recommandation porte création + **expiration** + statut +
version.

## Risque & construction de position (prep only — mission §10)
Calculer selon les données RÉELLEMENT disponibles (sinon `—`/estimation honnête) : taille, % portefeuille, perte
max, risque au stop, impact marge, greeks (Δ/Γ/Θ/V), concentration, corrélation, bêta, expo secteur/devise/
événement, liquidité, spread, slippage estimé, risque gap/expiration/assignation. **Limites configurables** (taille
max/position/stratégie, expo max/actif/secteur/devise, perte max/opération/jour, drawdown max, marge max, nb max
positions, expo options/événement max). **Toute violation visible AVANT** la préparation de l'ordre.

## L'IA n'décide jamais
Claude (`vertex/ai/`) **interprète** le paquet des moteurs (thèse, avocat du diable, contradictions) ; le verdict
appartient au moteur exécutif déterministe. Registre d'outils : 17 outils d'ordre **interdits** (rejetés à
l'enregistrement, `vertex/ai/tool_registry.py`). Sans clé API → repli déterministe honnête, jamais de texte inventé.

## Honnêteté de la donnée (règle 4)
Jamais de chiffre inventé présenté comme réel. Donnée absente → `—`/`n/d`. « démo » ne s'affiche que si le serveur
le confirme. Vertex doit pouvoir dire : « je ne dispose pas d'assez de données fiables pour cette analyse » —
préférable à une recommandation incorrecte.

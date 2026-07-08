# VERTEX — Plan directeur (feuille de route institutionnelle)

Terminal d'intelligence décisionnelle. **Analyse uniquement · lecture seule · aucun ordre.**

Méthode : livraison par **phases**, chacune découpée en **pull requests** petites, testées,
sans régression (strangler pattern). Aucune PR ne redessine tout. Chaque étape est validée
avant la suivante.

---

## Phases

| # | Phase | Objectif | État |
|---|---|---|---|
| 0 | **Fondation** | Extraire univers/constantes/config, statut système, tests sûreté, CI, docs | ✅ **fait** (branche `foundation/vertex-institutional-refactor`) |
| 1 | **Architecture** | Package `vertex/`, factory Flask, routes découpées, ré-export des moteurs `elio` | **en cours** — 8 Blueprints extraits (decision, analysis, feeds, system, content, auth, desk, command) |
| 2 | **Backend/Services** | `services/` (scanner, market_data, ibkr, options, cache, universe, news, status) | **en cours** — status, market_clock, persist |
| 3 | **Decision Stack** | Moteur unifié 14 couches → décision explicable + audit trail | **en cours** — `vertex/engines/decision_stack.py` + comité |
| 4 | **Scoring** | Sous-scores nommés/bornés/documentés/tracés dans l'UI | à venir |
| 5 | **Risk Manager** | Chaleur portefeuille, corrélation, NO_NEW_RISK, sizing | à venir |
| 6 | **Options Desk** | Table institutionnelle, IV rank, liquidité, danger, décision véhicule | à venir |
| 7 | **Portfolio** | Exposition, allocation, concentration sectorielle | à venir |
| 8 | **Validator** | Preuve d'edge (walk-forward), calibration, honnêteté sur l'incertitude | à venir |
| 9 | **Backtest** | Forward-test discipliné, courbe d'équité, drawdown | à venir |
| 10 | **Design System** | Tokens, typographie (Inter/IBM Plex/JetBrains Mono), composants | à venir |
| 11 | **Dashboard/UI** | Pages premium, tables redessinées, charts institutionnels | à venir |
| 12 | **Performance** | Latence, caches, taille des réponses, mobile | à venir |
| 13 | **Security** | Consolidation verrou d'accès, secrets, chiffrement au repos (option) | à venir |
| 14 | **Tests** | Couverture par moteur (scoring, decision, options, risk, api) | en cours |
| 15 | **CI/CD** | Lint, matrice, artefacts, déploiement Render | fondation posée |
| 16 | **Documentation** | Docs moteurs, API, contribution | en cours |
| 17 | **Refactoring final** | `terminal.py` mince → suppression | à venir |

---

## Critères de validation (à chaque PR)

- ✅ `pytest tests/ -q` vert (dont `test_no_orders`).
- ✅ `compileall` sans erreur.
- ✅ Aucune régression fonctionnelle (smoke : pages 200, API JSON valide).
- ✅ Aucun NaN dans les réponses API ; scores bornés [0, 100].
- ✅ Invariant lecture seule préservé.
- ✅ Un module = une responsabilité ; aucune logique dupliquée introduite.

---

## Prompts de travail (1 → 19)

> Chaque prompt : **but · fichiers · objectifs · critères de qualité · risques · tests · résultat attendu.**

### Prompt 1 — Audit complet
- **But** : cartographier modules, dépendances, doublons, code fragile, dette.
- **Fichiers** : tout le dépôt (lecture seule).
- **Objectifs** : inventaire LOC/responsabilités, graphe de dépendances, liste des doublons et des risques.
- **Qualité** : audit factuel, priorisé par sévérité, avec fichier:ligne.
- **Risques** : sous-estimer le couplage de `terminal.py`.
- **Tests** : n/a (analyse).
- **Résultat** : `docs/ARCHITECTURE.md` + backlog priorisé. *(fait)*

### Prompt 2 — Architecture
- **But** : poser le package `vertex/` (factory, config, extensions, routes).
- **Fichiers** : `vertex/app/*`, `vertex/__init__.py`.
- **Objectifs** : `create_app()`, blueprints par domaine, `terminal.py` importe la factory.
- **Qualité** : séparation routes/logique ; zéro import circulaire.
- **Risques** : casser l'ordre d'initialisation (scan de fond, caches).
- **Tests** : smoke (toutes routes 200), démarrage app.
- **Résultat** : app modulaire, `terminal.py` allégé.

### Prompt 3 — Backend/Services
- **But** : extraire la logique de données en services testables.
- **Fichiers** : `vertex/services/{scanner,market_data,ibkr,option_chain,cache,universe,fundamentals,news,status,logging}.py`.
- **Objectifs** : chaque service = une responsabilité, sans Flask, injectable.
- **Qualité** : pas d'accès réseau caché ; erreurs remontées, jamais avalées en silence.
- **Risques** : régressions du scan de fond.
- **Tests** : `test_services`, mocks.
- **Résultat** : cœur métier découplé de l'UI.

### Prompt 4 — Frontend
- **But** : sortir le HTML/CSS/JS des chaînes Python vers `vertex/ui/`.
- **Fichiers** : `vertex/ui/templates/*`, `vertex/ui/static/*`.
- **Objectifs** : templates Jinja, JS en modules, fin des f-strings HTML géantes.
- **Qualité** : aucun texte qui déborde, responsive, thèmes cohérents.
- **Risques** : très gros volume de markup à migrer → par page.
- **Tests** : smoke rendu + captures visuelles.
- **Résultat** : UI maintenable.

### Prompt 5 — Design System
- **But** : tokens + typographie + composants réutilisables.
- **Fichiers** : `vertex/ui/static/css/tokens.css`, composants.
- **Objectifs** : palette (fond #05070B…), Inter/IBM Plex/JetBrains Mono, échelles d'espacement.
- **Qualité** : Bloomberg/Linear/Palantir ; zéro néon crypto, zéro surcharge.
- **Risques** : incohérence pendant la transition.
- **Tests** : revue visuelle, contraste AA.
- **Résultat** : identité premium unifiée.

### Prompt 6 — Dashboard
- **But** : cockpit décisionnel (régime, permission marché, top setups).
- **Fichiers** : route dashboard + composants.
- **Objectifs** : répondre instantanément « marché favorable ? setup propre ? trop tard ? ».
- **Qualité** : chaque élément a une valeur de décision.
- **Risques** : surcharge d'information.
- **Tests** : smoke + revue.
- **Résultat** : page d'accueil institutionnelle.

### Prompt 7 — Decision Stack
- **But** : unifier les 14 couches en un moteur unique explicable.
- **Fichiers** : `vertex/engines/decision_stack.py`, `models/decision.py`.
- **Objectifs** : sortie normalisée (final_decision, conviction, confidence, vehicle, timing, entry/stop/targets, pros/cons/blockers, risk_flags, data_quality, explanation, audit_trail).
- **Qualité** : décisions autorisées seulement dans l'énumération ; règles de dégradation appliquées (données rassies → DATA_INSUFFICIENT, marché risk-off → pas de STRONG_BUY, etc.).
- **Risques** : incohérence avec les scores existants.
- **Tests** : `test_decision_stack` (chaque règle).
- **Résultat** : une décision, traçable, par titre.

### Prompt 8 — Scoring
- **But** : sous-scores propres, bornés, décomposés, tracés.
- **Fichiers** : `vertex/engines/scoring_engine.py`.
- **Objectifs** : MarketScore, TechnicalScore, MomentumScore, FundamentalScore, EntryQuality, OptionScore, RiskScore, VertexEdge, DataQualityScore, ConfidenceScore.
- **Qualité** : chaque score répond « quoi/pourquoi/quelles données/ce qui le fausse/fraîcheur/confiance ».
- **Risques** : fausse précision.
- **Tests** : `test_scoring` (bornes, robustesse aux données manquantes).
- **Résultat** : scoring transparent et défendable.

### Prompt 9 — Risk Manager
- **But** : rendre le risque visible et strict.
- **Fichiers** : `vertex/engines/risk_engine.py`.
- **Objectifs** : chaleur portefeuille (déjà posée), corrélation, NO_NEW_RISK, sizing par volatilité/conviction.
- **Qualité** : règle pro ≤ 6 % de capital exposé ; alertes claires.
- **Risques** : faux positifs de concentration.
- **Tests** : `test_risk`.
- **Résultat** : discipline de risque intégrée.

### Prompt 10 — Options Desk
- **But** : table d'options institutionnelle + décision véhicule.
- **Fichiers** : `vertex/engines/options_engine.py`, UI options.
- **Objectifs** : IV rank, liquidité (spread/OI), théta/jour, danger, breakeven, proba, décision.
- **Qualité** : IV chère → ACTION/WAIT ; illiquide → ACTION.
- **Risques** : greeks maison à valider.
- **Tests** : `test_options`.
- **Résultat** : desk options clair et sûr.

### Prompt 11 — Portfolio
- **But** : exposition, allocation, concentration.
- **Fichiers** : `vertex/engines/*`, UI portfolio.
- **Objectifs** : donut allocation, exposition/levier, heat, corrélation sectorielle.
- **Qualité** : lisible en un coup d'œil.
- **Tests** : `test_portfolio`.
- **Résultat** : vue portefeuille pro.

### Prompt 12 — Validator
- **But** : prouver (ou nuancer) l'edge.
- **Fichiers** : `vertex/engines/validator_engine.py`.
- **Objectifs** : walk-forward sans look-ahead, calibration, honnêteté sur l'incertitude.
- **Tests** : `test_validator` (bornes, edge > bruit).
- **Résultat** : crédibilité statistique.

### Prompt 13 — Backtest
- **But** : forward-test discipliné.
- **Objectifs** : courbe d'équité, drawdown, Sharpe/Sortino gardés.
- **Tests** : `test_backtest`.
- **Résultat** : preuve de comportement dans le temps.

### Prompt 14 — Performance
- **But** : latence, caches, taille des réponses, mobile.
- **Objectifs** : `/scan` allégé/paginé, gzip, budgets de rendu.
- **Tests** : mesures de latence.
- **Résultat** : rapide sur mobile et bureau.

### Prompt 15 — Security
- **But** : consolider verrou d'accès + secrets.
- **Fichiers** : `vertex/app/config.py`, middleware auth.
- **Objectifs** : source unique du verrou, secrets hors dépôt, chiffrement au repos (option).
- **Tests** : `test_no_orders`, auth.
- **Résultat** : sûr par conception.

### Prompt 16 — Documentation
- **But** : docs moteurs + API + contribution.
- **Résultat** : compréhensible par un senior en quelques minutes.

### Prompt 17 — Tests
- **But** : couverture par moteur.
- **Fichiers** : `tests/test_{scoring,decision_stack,options,risk,validator,api}.py`.
- **Résultat** : filet de sécurité complet.

### Prompt 18 — CI/CD
- **But** : lint + matrice + artefacts + déploiement.
- **Résultat** : intégration continue fiable, sûreté bloquante.

### Prompt 19 — Refactoring final
- **But** : `terminal.py` mince puis supprimé.
- **Résultat** : architecture propre, modulaire, testée, documentée.

---

## Standard « fini »

VERTEX est fini quand : architecture propre · UI premium · tables belles · charts utiles ·
Decision Stack unifié · risque visible · qualité des données explicite · tests verts · docs
claires · **aucun ordre possible** · chaque décision explicable · chaque score traçable.

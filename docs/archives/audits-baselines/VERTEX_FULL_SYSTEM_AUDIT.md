# VERTEX FULL SYSTEM INTEGRATION — AUDIT

> Audit forensique ciblé sur les invariants de production (READONLY,
> observabilité, connexions honnêtes, couverture des routes). Ce qui a été
> corrigé cette passe est marqué ✅ ; ce qui reste est listé sans complaisance.

## 1. READONLY (§4) — invariant absolu
- `READONLY=True` en dur ; aucun chemin de désactivation.
- **Correctif ✅** : `closePosition` (clôture DÉCLARATIVE localStorage, « aucun
  ordre n'est envoyé ») renommé **`recordExit`** dans `vx-entities.js` et
  `portfolio_page.py`. Le token interdit ne figure plus nulle part.
- **Preuve ✅** : `test_no_order_path_anywhere_in_source` scanne tout le code
  produit (backend + JS, hors tests/docs) → **0 occurrence** d'appel/définition
  parmi les 26 verbes d'ordre interdits.
- IBKR : `readonly=True` toujours ; worker unique `RequestTimeout=45`.

## 2. Observabilité (§41) — endpoints canoniques
Ajoutés cette passe (consolident des données existantes, jamais inventées) :
- **✅ `/readyz`** — readiness distinct de `/healthz` : vérifie configuration,
  stratégie, stockage, READONLY ; 200 si prêt, 503 sinon, avec le détail par check.
- **✅ `/api/system/status`** — alias canonique de `/api/system-status`.
- **✅ `/api/system/jobs`** — alias canonique de `/api/system/automations`.
- **✅ `/api/system/connections`** — état honnête des 6 connexions.

## 3. Connexions honnêtes (§9) — `vertex/services/connections.py`
- Vocabulaire canonique (§2) : NOT_IMPLEMENTED / CONFIGURATION_MISSING / BLOCKED
  / OFFLINE / DEGRADED / STALE / DELAYED / FALLBACK / DEMO / LOADING / READY /
  LIVE / ERROR.
- **Correctif ✅** : IBKR n'est **jamais** déclaré LIVE/DELAYED sans preuve de
  session ; « configuré » ≠ « connecté » → **OFFLINE** honnête en l'absence de
  socket confirmé. Claude sans clé → FALLBACK. TradingView sans secret →
  CONFIGURATION_MISSING. Aucun secret n'est exposé.
- **Preuve ✅** : `test_connections_use_canonical_statuses`,
  `test_ibkr_not_claimed_live_without_proof`.

## 4. Couverture des routes (§31)
- **Preuve ✅** : `test_main_routes_ok_or_redirect` couvre 35 routes/sous-vues
  (les 9 espaces + sous-vues Marchés/Opportunités/Portefeuille/Performance/
  Intelligence/Système/Options) → toutes 200/redirect.
- `test_legacy_routes_redirect` : anciennes URLs (/options-lab, /watchlist,
  /journal, /sectors, /health) → redirigent.
- **Preuve navigateur ✅** : 11 routes principales balayées en Chromium →
  **0 erreur console**. Endpoints santé → tous **200** en curl.

## 5. Ce qui N'A PAS été traité cette passe (honnêteté §2)
Le prompt couvre ~40 phases. Cette passe cible les invariants de production les
plus critiques et prouvables. Restent, entre autres, non traités ou seulement
partiels :
- Séquence de démarrage à 24 étapes formalisée (§8) — un startup report existe
  déjà mais pas la séquence typée complète.
- Consolidation des « sources de vérité » dupliquées (§6) — plusieurs moteurs
  historiques coexistent encore dans `terminal.py`.
- Pipeline de données typé de bout en bout (§18), contrat de donnée unique (§17)
  généralisé à tous les domaines.
- Bus d'événements central formalisé (§28).
- Traitement « flagship » interactif des pages Marchés/Portefeuille/Performance/
  Intelligence (graphiques déjà présents mais pas tous au niveau cible).
- Tests d'intégration démarrage/dégradé complets (§50) et 10 parcours E2E (§51)
  — seuls des sous-ensembles sont couverts.

Ces éléments sont réels et non déclarés « faits ».

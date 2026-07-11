# VERTEX FULL PRODUCTION OS — Implémentation

Passe finale de consolidation (2026-07-11), troisième et dernière mission
après Strategy OS (moteurs) et Master Redesign OS (interface). Règle de
vérité appliquée : chaque affirmation ci-dessous est adossée à un test, une
capture ou une vérification navigateur reproduite dans cette passe.

## 1. Livré dans cette passe

### Vérité numérique
- `tests/test_calculations_golden.py` (31 tests) : valeurs de référence
  calculées à la main (BS ATM 10.19, parité put-call, plancher
  intrinsèque, drawdown −14.5 %, profit factor 2.33, Brier/log loss…),
  propriétés par grilles déterministes (monotonies spot/vol/temps,
  T=0 = intrinsèque, IV round-trip, scénarios relatifs).
- Conventions d'unités écrites et testées
  (`docs/VERTEX_CALCULATION_REFERENCE.md`) : prime par action vs par
  contrat (×100), IV décimale canonique (normalisation % tracée à la
  frontière `/api/options/simulate`), delta signé (bandes en valeur
  absolue pour les PUTs), DTE en jours calendaires, T=DTE/365.
- **DTE à l'heure de New York** : `datetime.now()` naïf remplacé par
  l'horloge America/New_York dans les deux calculs d'échéance
  (`options_lab._timeline`, `legacy_engine._ny_now`) — plus de
  surestimation d'un jour en soirée sur serveur UTC.

### Tests canoniques (§37)
- `tests/test_production_guards_canonical.py` (37 tests) porte les noms
  exigés : `test_no_fake_data_displayed`, `test_missing_data_becomes_none`,
  `test_all_routes_respond`, `test_every_button_has_handler`,
  `test_readonly_forever`, `test_no_order_code_paths`,
  `test_decision_engine_is_single_source`, `test_desk_sync_not_broken`,
  `test_all_sync_keys_are_canonical`, `test_walk_forward_has_no_lookahead`,
  `test_option_multiplier`, `test_percentage_conventions`,
  `test_timezone_handling`, `test_stock_split_handling`, etc.

### Corrections de bogues (trouvés par l'audit indépendant)
- **Contrat `/api/pos-quotes`** : le client (Portefeuille + Briefing)
  envoyait `{items:…}` et indexait par id alors que le serveur attend
  `{positions:…}` et renvoie des clés composites `SYM|exp|strike|RIGHT` —
  le P&L live ne se peuplait jamais. Corrigé et vérifié en navigateur
  (positions réelles cotées, parcours D).
- **Télémétrie 0-erreur** : la nouvelle UI n'émettait rien vers
  `/api/client-log`. `vx-core.js` remonte désormais `window error` +
  `unhandledrejection` (borné, tronqué) ; testé de bout en bout (erreur
  injectée → visible dans le journal serveur).
- **États dégradés silencieux en console** : `/api/ibkr/positions` (503)
  et `/api/strategy/decision/<sym>` (404) généraient des erreurs console
  à chaque visite. Passés en HTTP 200 avec `ok:false` /
  `available:false` — le corps porte l'état honnête, la console reste à 0.
- Service worker bump `td-shell-v7` (shell modifié).

### Documentation de production (8 documents)
`VERTEX_BASELINE_REPORT.md` · `VERTEX_FULL_AUDIT.md` ·
`VERTEX_BUTTON_MATRIX.md` · `VERTEX_ROUTE_MATRIX.md` ·
`VERTEX_DATA_SOURCE_MATRIX.md` · `VERTEX_CALCULATION_REFERENCE.md` ·
`VERTEX_KNOWN_LIMITATIONS.md` · ce document.

## 2. Preuves de vérification (reproduites dans cette passe)

- **Tests** : `python -m pytest tests/ -q` → **516 passed, 0 failed**.
- **Parcours A-I (§38)** : 9/9 PASS en Chromium réel (script
  `journeys_ai.py`) — A favori aller-retour Briefing, B options
  Dynamic→scénarios→alerte→notifications, C watchlist aller-retour avec
  contexte restauré, D position→clôture→journal auto, E secteurs→
  opportunités filtrées→analyse, F palette ⌘K→AAPL, G repli Claude
  déterministe, H TradingView non configuré affiché honnêtement,
  I IBKR hors ligne (ok:false, marques « indisponibles », qualité de
  données dégradée).
- **Console navigateur** : 0 erreur sur les 8 espaces + vue positions avec
  données réelles seedées ; `GET /api/client-log` → `{"count":0}`.
- **Responsive** : aucun débordement horizontal à 768 (tablette) ni
  390 px (mobile) sur Briefing et Portefeuille.
- **Noms personnels** : recherche insensible à la casse du motif interdit
  sur tout l'arbre de travail → 0 occurrence (gardien
  `test_no_personal_names_anywhere`).
- **Chemins d'ordre** : 0 (gardiens `test_no_order_code_paths`,
  `test_readonly_forever` ; `readonly=True` codé en dur).

## 3. Décisions d'architecture actées

- Les « faux zéros » du scoring legacy (`quant_engine`, `decide.py`) sont
  **documentés, pas réécrits** : ce chemin produit les verdicts
  historiques du track record ; le chemin canonique (scenario_pricer,
  ExecutiveEngine, provenance) refuse la donnée absente. Détail :
  `VERTEX_FULL_AUDIT.md §2`.
- 30 routes « API seules » (sans consommateur UI) **conservées** — règle
  « aucune suppression sans redirection » ; deux décisions produit
  remontées à l'utilisateur (`/news-feed`, `/api/options-lab`).
- Branche de travail : `claude/vertex-strategy-os-h17dso` (contrainte
  d'environnement, documentée dans le baseline).

## 4. Limitations restantes

Voir `VERTEX_KNOWN_LIMITATIONS.md` (18 entrées, toutes déclarées, aucune
masquée par une donnée inventée). Blocages externes avec procédure :
IBKR (brancher TWS local, retirer `NO_IBKR=1`), TradingView
(`TRADINGVIEW_SECRET` + script Pine), Claude (`ANTHROPIC_API_KEY`).

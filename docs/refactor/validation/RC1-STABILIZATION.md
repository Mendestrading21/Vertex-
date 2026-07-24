# Validation — RC1 : Stabilisation finale

> Branche `agent/vertex-total-rebuild`. Phase de **gel fonctionnel** : aucune nouvelle
> fonctionnalité — stabiliser, nettoyer, prouver. Base `origin/main` (`2b4fa70`)
> **intouchée**. Conforme à `VERTEX_CONSTITUTION.md`, `VERTEX_PRODUCT_BIBLE.md`,
> `PRODUCT_EXPERIENCE_REVIEW.md`, `SKILL.md` et aux 8 rapports de validation PR 1→7.

## RC1-A — Gel fonctionnel
Toutes les modifications RC1 entrent dans : bug · cohérence · accessibilité · dette
technique · suppression de code mort · documentation. **0 nouvelle fonctionnalité,
0 nouveau moteur, 0 nouvel espace, 0 nouvelle visualisation.**

## RC1-B — Audit du code mort (avec preuve) → 6 fichiers supprimés
Audit par recherche exhaustive (include + invocation) sur `vertex/`, `terminal.py`,
`tests/`, JS/CSS.

| Fichier supprimé | Symbole | Preuve | Risque |
|---|---|---|---|
| `js/charts/correlation-matrix.js` | `correlationCard` | 0 include, 0 invocation | bas |
| `js/charts/factor-chart.js` | `factorCard` | 0 include, 0 invocation | bas |
| `js/charts/geographic-exposure.js` | `geoCard` | 0 include, 0 invocation | bas |
| `js/charts/vol-surface.js` | `volSurfaceCard` | 0 include, 0 invocation | bas |
| `js/charts/breadth-chart.js` | `breadthCard` | chargé (Marchés) mais **0 appel** (refs = prose/test négatif) | bas-moyen |
| `js/charts/sector-chart.js` | `sectorCard` | 0 appel | bas-moyen |

Balises `<script>` de breadth/sector retirées de `markets_page.py:195-196`. Gardiens
`test_chart_modules_exist` / `test_no_fake_data_in_charts` mis à jour. Commit isolé
réversible `6cfcb18`. **Non supprimé (preuve = vivant/test-gardé)** : vues Options
legacy (défaut/liens/tests), `option-scenarios.js` (appelé), tous les modules page-JS,
tous les CSS (15/15 liés), `intelligence_page.py` (route hors-nav active).

## RC1-C — Cartographie de terminal.py (extraction différée, par prudence)
`terminal.py` = **10 734 lignes** (inchangé en RC1). Cartographie :
- **Routes HTML legacy actives** : `/scan`, `/desc/<sym>`, `/options/<sym>`, `/quotes`,
  `/ibkr`, `/weekly-regen` (~40 autres routes déjà commentées `# [redesign] migrée`).
- **Endpoints API** : `/api/ticker/<sym>`, `/api/company/<sym>`, `/api/analyst/<sym>`,
  `/api/names`, `/api/track-record`, `/api/rescan`, `/api/alerts/status`,
  `/api/correlations/<sym>`…
- **Rendu legacy** : blocs HTML/JS concaténés (`_DECJ_JS`, `loadHealth`…).
- **Adaptateurs IBKR** : connexions `readonly=True` (lignes 714, 975, 2098).
Décision RC1 : **aucune extraction** — la règle interdit « déplacement non testé /
migration big-bang / changement simultané logique+architecture ». L'extraction
incrémentale (helpers purs, formatters, registres) est planifiée **post-RC1**, chaque
bloc déplacé accompagné de son test. Rien n'est déplacé sans preuve.

## RC1-D — Consolidation des composants (audit + convergence partielle)
Inventaire (source canonique confirmée) : Card/KPI/Verdict/Scenario/Freshness/Tabs/
Segmented/Button/Drawer/Modal/Skeleton/Empty/Error/Insufficient/Demo/Live-dot →
`components.css` + `states.css` + `chart-core.js` (Chart Shell unique). **Divergences
relevées** (corrigées post-RC1, aucun bug de rendu) : `.vx-stat*` dupliqué
(options_intel + tracking), badges démo fragmentés (`.vx-badge-demo` / `.vx-demo-tag` /
`.vx-hypo`), override local `.vx-verdict-card`, `.vx-chip` sur 3 CSS. **Styles inline :
335** (pics system/design-system/analysis 49/49/48) — migration progressive planifiée.
Aucune régression : la consolidation lourde est différée pour respecter le gel.

## RC1-E — Audit routes & API + gardien READONLY
- **8 espaces canoniques** (redesign.py) + **37 redirections legacy** (toutes 301,
  query préservée) + routes hors-nav (`/intelligence`, `/tracking`, `/design-system`).
- **Endpoints API** inventoriés par domaine (briefing/décision, marchés/analyse,
  options, portefeuille, tracking, IA, live, système).
- **Endpoints non consommés** (legacy, aucun ordre) : `/api/strategie`, `/api/comite`,
  `/api/weekly`, `/api/correlations/<sym>`, `/api/risk`, `/api/portefeuille`,
  `/api/company/twin/<sym>` → listés dans KNOWN_ISSUES, non retirés (revue de contrat
  requise).
- **AUCUN endpoint d'ordre** — voir RC1-I.

## RC1-F — Performance (mesures)
| Métrique | Valeur |
|---|---|
| Import `terminal` (froid) | ~1,8 s |
| Poids JS total (`static/vertex/js`) | ~360 Ko → **~343 Ko** après retrait des 6 graphes |
| Poids CSS total | ~67 Ko |
| Lignes Python `vertex/` | 31 889 |
| `terminal.py` | 10 734 lignes |
Optimisation appliquée : **retrait de 6 modules de graphes** (≈17 Ko JS + 2 `<script>`
en moins sur Marchés). Pas de goulot bloquant identifié ; les pages re-fetchent
proprement (pas de skeleton infini). Optimisations plus poussées (bundling ciblé par
vue) planifiées post-RC1.

## RC1-G — Accessibilité (audit)
- **Landmarks / aria** : `aria-label` sur sections, `role="tablist"`/`role="tab"` sur
  les onglets, `role="note"` sur les insights, `role="img"` + `aria-label` sur les
  barres/heatmaps décoratives.
- **Titres** : chaque espace a un `<h1>` unique ; H2/H3 hiérarchisés.
- **Graphiques** : Chart Shell fournit un **résumé accessible** (`summary`) — présent
  sur les payoffs/distribution ; couverture à compléter post-RC1.
- **Sans couleur** : P&L et verdicts portent un **libellé texte** en plus de la couleur
  (badges nommés, mots « WIN/LOSS », « Cassée », « Renforcement interdit »…).
- **Formulaires/dialogs** : `<label for>` sur les champs, drawers/modales via
  `VX.shell` (focus géré). **Limites restantes** (KNOWN_ISSUES) : audit clavier complet
  + `prefers-reduced-motion` exhaustif + contrastes AA mesurés = finition post-RC1.

## RC1-H — Responsive (mesuré, 5 viewports)
Sweep Playwright sur **15 vues** (8 espaces + sous-vues clés) × **5 viewports**
(390×844, 768×1024, 1024×768, 1440×900, 1920×1080) = **75 combinaisons**.

| Viewport | Débordement réel (max) | Erreurs console applicatives |
|---|---|---|
| 390 | **0 px** | 0 |
| 768 | **0 px** | 0 |
| 1024 | **0 px** | 0 |
| 1440 | **0 px** | 0 |
| 1920 | **0 px** | 0 |

**0 débordement réel sur les 75 combinaisons.** (Un premier passage avait relevé des
404 transitoires sur `/markets` — les 2 graphes supprimés encore référencés ; corrigé
en retirant les balises `<script>`, re-sweep propre.) Tableaux larges = scroll
horizontal intentionnel (desktop) / cartes (mobile). Aucun contenu critique masqué,
aucune interaction hover-only critique.

## RC1-I — Sécurité & intégrité
- **READONLY prouvé** : `readonly=True` codé en dur à chaque connexion IBKR
  (`ib_reader.py:53/63`, `terminal.py:714/975/2098`, `ibkr_gateway.py:43`) ;
  `config.py READONLY=True / ANALYSIS_ONLY=True` non désactivables.
- **0 endpoint / fonction d'ordre** : recherche `def (place|submit|transmit|modify|
  cancel)_order | placeOrder | exercise_option | close_position` → **0 définition,
  0 appel**. Toutes les occurrences des verbes d'ordre sont des **listes d'interdiction**
  (`tool_registry.py FORBIDDEN_TOOLS`), des **libellés de statut**
  (`order_execution: disabled-by-design`) ou des **tests gardiens**. `/api/planning/
  ticket` produit un ticket de dimensionnement `transmitted:false, readonly:true`.
- **~20 tests gardiens READONLY** : `test_no_orders`, `_ORDER_WORDS` (multiples),
  `test_ibkr_readonly`, `test_readonly_is_effective`, `test_ibkr_offline_does_not_close_positions`…
- **Secrets** : `.env` / `.vertex_secret` **gitignorés** (aucun secret committé).
- **XSS** : données externes échappées côté client (`esc()`), news via
  `news_plus.sanitize_news()`.
- **Démo / offline / stale / missing / insufficient** : états honnêtes vérifiés
  (badges DEMO/OFFLINE, `n/d`, jamais un zéro inventé).

## RC1-J — Tests
- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **954 passed, 2 skipped** (**956 collectés**).
- Couverture des gardiens : routes 200, sous-vues, READONLY (×~20), démo, sans-IBKR,
  stale/missing/insufficient, options (IV/payoff/greeks/garde-fou), portefeuille
  (état-de-thèse/garde-fou), journal (discipline/hero honnête), système (readonly/hero),
  service worker (vN présent, v(N-1) absent). **Aucun gardien utile supprimé.**

## RC1-K — Cohérence éditoriale
- **8 labels canoniques** présents et cohérents (Aujourd'hui/Marchés/Opportunités/
  Analyse/Portefeuille/Options/Journal/Système) ; aucun label parasite visible.
- **Tutoiement** = registre dominant ; **`performance_page.py` normalisé** (mélange
  tu/vous supprimé, commit `f201528`). Reste (post-RC1) : `intelligence_page.py`
  (hors-nav) en vouvoiement.
- Vocabulaire d'états (LIVE/DELAYED/STALE/DEMO/OFFLINE/n/d) et niveaux S+/S/A/B
  cohérents. Un seul terme anglais visible : « Watchlist » (financier standard).

## RC1-L — Service worker & cache
- Version **`td-shell-v51`** (bump RC1 v50→v51 : purge du cache runtime pré-suppression) ; `install` (skipWaiting + précache manifest/icône),
  `activate` (suppression des caches ≠ version + `clients.claim`). **Pas de nouveau
  bump en RC1** (stabilisation, pas de changement de shell visible).
- Gardiens : `vN` présent + `v(N-1)` absent (`test_ui_v3`, `test_redesign_ui`,
  `test_production_guards_canonical`).

## RC1-M — Documentation release
Créés : `docs/refactor/validation/RC1-STABILIZATION.md` (ce fichier),
`docs/release/RC1_CHECKLIST.md`, `docs/release/RC1_KNOWN_ISSUES.md`,
`docs/release/RC1_CHANGELOG.md`, `docs/release/RC1_ROLLBACK.md`.

## Verdict : **GO (RC1 interne)**
Tous les critères GO/NO-GO sont satisfaits (voir `RC1_CHECKLIST.md`). RC1 est propre,
mesurée, documentée et réversible. **Aucun merge dans `main`, aucun tag final, aucune
release publique** — en attente de validation humaine.

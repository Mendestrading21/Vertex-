# VERTEX — Inventaire des fichiers (Phase 1)

> Branche `agent/vertex-total-rebuild` @ `362c7d4` · **617 fichiers suivis** ·
> `terminal.py` = **10 734 lignes** (monolithe). Audit 100 % lecture seule
> (`git ls-files`, `grep`, `wc`, `ls`) — aucun fichier de données/secret ouvert
> au-delà de la confirmation d'existence.

> **Constat transversal** : le dépôt est en **migration strangler**. Deux UI
> coexistent — l'ancienne (monolithe `terminal.py` + `vertex/ui/*.py` à plat) et
> la nouvelle (`routes/redesign.py` + `vertex/ui/shell/` + `vertex/ui/pages/*`).
> Beaucoup de « doublons » sont les deux moitiés de cette bascule, **pas** du code
> mort. Ne rien supprimer sans confirmer quelle route sert quoi (règle SKILL).

## 1. Racine

| Path | Rôle | Statut | Risque | Note |
|---|---|---|---|---|
| `terminal.py` | Monolithe Flask + blueprints + IBKR | ACTIF | **élevé** | 10 734 lignes ; toute page ancienne y vit |
| `ib_reader.py` | Connecteur IBKR `readonly=True` | ACTIF | **élevé** | Importé `terminal.py:2091` ; invariant lecture seule |
| `company_cache.json` | **Cache société 1,38 Mo COMMITÉ** | hygiène | moyen | voir §11 |
| `position_inventory.json` | **Inventaire positions COMMITÉ (103 o)** | hygiène | moyen | voir §11 |
| `render.yaml`, `requirements.txt`, `pytest.ini`, `.env.example` | Déploiement/test | ACTIF | faible | `.env` réel gitignoré |
| Lanceurs `Lancer_VERTEX*.{bat,command}`, `Installer_Demarrage_Auto.bat` | Démarrage Win/macOS | ACTIF | faible | variantes normales |
| `README.md`, `CLAUDE.md`, `CLAUDE_VERTEX_REBUILD.md`, `DEMARRER_ICI.md`, `SECURITE.md` | Docs | ACTIF | faible | |

## 2. `vertex/app` — noyau Flask

`config.py`/`config_validation.py` (invariant `READONLY`, **élevé**),
`state.py` (`scan_state` muté en place, **élevé**), `routes/redesign.py` (routes
des 9 espaces, **élevé**), `routes/*_api.py` (blueprints JSON par domaine),
`routes/{auth,command,content,desk,feeds,live_events,system}.py` — `system.py`
porte le versioning service-worker `td-shell-vN`.

## 3. `vertex/ui` — DEUX générations d'UI (point chaud)

**3a. Redesign (strangler, servi par `routes/redesign.py`)** :
`ui/shell/__init__.py` (**registre nav `PRIMARY_NAV`**, `SHELL_VERSION='vx-shell-1'`
— 2ᵉ registre ; commentaire « huit espaces » mais **9 entrées**, incohérence),
`ui/pages/{briefing, markets_page, opportunities_page, portfolio_page,
analysis_page, options_intel_page, performance_page, intelligence_page,
system_page, tracking_page}.py`, `design_system_page.py`, `design_system_demo.py`.

**3b. Monolithe historique (importé UNIQUEMENT par `terminal.py`)** :
`ui/nav.py` (**1er registre nav**, LEGACY?), `ui/{signals, vault, options_lab,
journal, sync_center, strategy_os, design_system, vx_kit, home_art}.py`.
⚠️ `journal.py` et `vx_kit.py` portent des listes `DESK_KEYS` critiques
(gardien `test_production.py::test_desk_sync_keys_single_source_of_truth`) —
ne pas toucher sans ce test.

## 4-8. Métier (aucun marqueur TODO/FIXME/deprecated — code Python propre)

- **`vertex/engines/` (22 modules)** : `decision_stack` (vérité, élevé),
  `recommendation` (façade unique, élevé), + analysis/decide/committee/context/
  evidence/reasoning/scorecard/quant_engine/market_lens/track_record/…
- **`vertex/options/` (19)** : ⚠️ **`legacy_engine.py` = nom trompeur mais module
  le plus importé du dépôt** (Black-Scholes/greeks/IV ; `terminal.py:36`,
  `scanner/weekly.py:34`, `strategy/legacy_adapter.py:22`, tests golden) — **ACTIF**,
  à renommer, pas supprimer.
- **`vertex/strategy/`** : `legacy_adapter.py` **ACTIF** (`terminal.py:47`,
  `command.py:17`), `executive_engine`, `constitution`, `memory/*`, `profiles/`.
- **`vertex/services/`** : `news_plus.py` (`sanitize_news()` anti-XSS, **élevé**,
  règle 5), live_engine/live_stream/connections/market_clock/persist/startup.
- **Packages secondaires** : `ai/*` (17), `data_sources/*` (19, dont `ibkr_*`×6 +
  `fallback_market_data.py`), `data/*` (`demo.py`, `_constituents_static.py`),
  `research/*`+`research/institutional/*`, `positions/*` (12),
  `portfolio/*` (`legacy_basket_risk.py` **ACTIF**, nom trompeur), `market/*`,
  `tracking/*`, `scanner/*`, `visualization/*` (`palette.py`), `quant/`,
  `companies/` vs `company/` (homonymes à vérifier).

## 9. `vertex/static` — CSS / JS

**9a. CSS (15 fichiers, ~1 100 l)** : tokenisé et modulaire. **Aucun fichier CSS
legacy nommé** (`black-glass.css`/`signal-green.css` n'existent pas). `tokens.css`
(168 l, source canonique), `components.css` (192), layout/cockpit/buttons/base/
states/control-surface/responsive/tables/polish/animations/charts/utilities/forms.
→ Pas de couche de migration CSS morte. **Le poids inline est côté Python.**

**9b. Densité `style=` inline (à réduire)** : `terminal.py` **1 682**,
`ui/options_lab.py` 62, `ui/journal.py` 58, `ui/pages/analysis_page.py` 52,
`design_system_page.py` 49, `system_page.py` 43, briefing 38, opportunities 35…

**9c. JS** : `charts/` (24), `pages/` (2), `vendor/` (2), core (`vx-core`,
`vx-entities`, `vx-shell`, `live-updates`).
- ⚠️ **Deux moteurs de chandeliers chargés ensemble** : `candlestick-chart.js`
  (Canvas) **et** `candlestick-lwc.js` (TradingView LWC), tous deux inclus par
  `analysis_page.py:204` et `:206` + `price-chart.js` → redondance probable, à
  trancher par test navigateur.
- `chart-theme-obsidian-copper.js` : palette JS à réconcilier avec `palette.py`
  (Python) et `tokens.css` (CSS) — **3 sources de couleurs**.
- `static/chart.umd.min.js` (racine, hors `vertex/static/`) : à vérifier s'il est
  encore référencé, sinon MORT?.

## 10. `tests` (75) & `docs` (66)

- **Tests gardiens** : `test_no_orders.py` (READONLY), `test_production.py`,
  `test_nav.py`, `test_redesign_ui.py`, `test_obsidian_theme.py`, `test_ui_v3.py`,
  `test_visual_intelligence.py`. Doivent rester à 100 % (893/895 actuellement).
- **Docs** : nombreux audits/baselines redondants (`VERTEX_FULL_AUDIT`,
  `VERTEX_ULTIMATE_AUDIT`, `VERTEX_MASTER_REDESIGN_AUDIT`, `VERTEX_REPO_AUDIT`…) —
  candidats à consolidation. `docs/redesign/` = **121 PNG** de baseline.

## 11. Hygiène — données/secrets suivis par git ⚠️

`.gitignore` couvre `.env`, `desk_data.json`, `desk_backup_*.json`,
`tracking_backup_*.json`, `ai_enrichment_backup_*.json`, `.vertex_secret` — bon.

**Mais deux fichiers de données sont COMMITÉS** (existence confirmée, contenu non
ouvert) :

| Fichier | Taille | Problème |
|---|---|---|
| `company_cache.json` | **1,38 Mo** | Cache société versionné, non gitignoré ; gonfle le dépôt, conflits de merge. À sortir du suivi git — sauf seed volontaire (`vault.py:130`). **Décision utilisateur requise.** |
| `position_inventory.json` | 103 o | **Inventaire de positions** (données potentiellement liées à un compte réel). La règle sécurité Vertex interdit de committer inventaires de positions / identifiants. **À retirer du suivi git — décision utilisateur requise.** |

> Aucun `.env` réel, `.vertex_secret` ni `desk_data.json` n'est suivi (conforme).
> **Aucune suppression effectuée dans ce lot d'audit** : ces deux fichiers sont
> signalés pour arbitrage, pas retirés.

## 12. Marqueurs de code

`grep TODO|FIXME|XXX|HACK|deprecated` sur `vertex/`, `terminal.py`, `ib_reader.py`
= **0 occurrence**. Aucun `*_old*`/`*.bak`/`*-v2*`/`*_backup*` suivi. Les seuls
« legacy » sont **3 modules au nom hérité mais ACTIFS** + des docs `*_V3_*`.

## Legacy/morts potentiels — à VÉRIFIER avant toute suppression (priorisé)

**P0 — Doublons actifs coûteux**
1. **2 moteurs chandeliers** chargés ensemble (`candlestick-chart.js` vs
   `candlestick-lwc.js`, `analysis_page.py:204/206`) → tester lequel rend, retirer l'autre.
2. **2 registres de navigation** (`ui/nav.py` vs `shell/PRIMARY_NAV`) + « 8 vs 9
   espaces » → lever l'incohérence (`tests/test_nav.py`).
3. **3 sources de couleurs** (`palette.py` / `chart-theme-obsidian-copper.js` /
   `tokens.css`) → unifier en une source canonique.

**P1 — UI monolithe historique** (retirer quand routes migrées)
4. `ui/{signals,vault,options_lab,journal,sync_center,strategy_os,design_system,
   vx_kit,home_art}.py` — importés uniquement par `terminal.py`. Vérifier la
   couverture redesign équivalente ; **ne pas toucher `journal.py`/`vx_kit.py`**
   sans le gardien desk-keys.
5. `ui/pages/design_system_demo.py` (vitrine) — besoin prod ou retirable.

**P2 — Nommage trompeur : NE PAS supprimer, renommer**
6. `options/legacy_engine.py` (ACTIF, très importé) → renommer `options_engine`.
7. `strategy/legacy_adapter.py` (ACTIF). 8. `portfolio/legacy_basket_risk.py` (ACTIF).

**P3 — Recouvrements à vérifier**
9. `vertex/company/` vs `vertex/companies/`. 10. `positions/calculator.py` vs
`recalculator.py` ; `data/_constituents_static.py` vs `constituents.py`.
11. `static/chart.umd.min.js` (référencé ?).

**P4 — Hygiène**
12. `company_cache.json`, `position_inventory.json` → gitignore (décision user).
13. `docs/redesign/*` (121 PNG) + docs d'audit multiples → consolidation.

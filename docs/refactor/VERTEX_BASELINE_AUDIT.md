# VERTEX — Baseline Audit (Phase 0)

> Audit réel exécuté le 2026-07-23. Aucune modification du runtime.
> Branche : `agent/vertex-total-rebuild` — commit `362c7d417d8993c5f38343f35490e81b62fa52fa`.
> Environnement : conteneur Linux, Python 3.11.15, mode `DEMO=1 NO_IBKR=1 PORT=5002`.

## 1. Constat

Point de départ exigé par `CLAUDE_VERTEX_REBUILD.md` : établir un état initial
mesuré (tests, démarrage, routes, erreurs, captures, états dégradés) **sans rien
modifier**, comme socle de comparaison pour toute la refonte.

## 2. Commandes exécutées et résultats exacts

| Étape | Commande | Résultat |
|---|---|---|
| Branche | `git branch --show-current` | `agent/vertex-total-rebuild` |
| Commit | `git rev-parse HEAD` | `362c7d417d8993c5f38343f35490e81b62fa52fa` |
| Fichiers suivis | `git ls-files \| wc -l` | **617** |
| Compilation | `python -m compileall -q terminal.py vertex` | **exit 0** (aucune erreur de syntaxe) |
| Tests | `python -m pytest tests/ -q` | **893 passed, 2 skipped en 14.48 s** |
| Démarrage démo | `DEMO=1 NO_IBKR=1 python terminal.py` | serveur prêt, `/healthz` **200 en ~1 s** après démarrage |

### 2.1 `/healthz` (démo)

```json
{"build":"VERTEX-1.0","data_source":"demo","engines":["scoring","pivots",
"committee","strategy","portfolio_risk","vertex","vertex_ml","validator"],
"ibkr_enabled":false,"last_scan":"20:11:15","scan_age":32,"scan_error":null,
"scanned":20,"status":"ok","universe":517,"vertex_ready":20}
```

- 8 moteurs déclarés sains ; univers 517 titres ; 20 scannés en démo ; IBKR désactivé (honnête).

## 3. Cartographie brute des routes

- **163 règles** dans `app.url_map` (détail complet : `ROUTE_ENDPOINT_MAP.md`).
- **9 espaces** dans `PRIMARY_NAV` (`vertex/ui/shell/__init__.py:13`) :
  Briefing `/`, Marchés `/markets`, Opportunités `/opportunities`,
  Portefeuille `/portfolio`, Analyse `/analysis`, Options `/options`,
  Performance `/performance`, Intelligence `/intelligence`, Système `/system`.
- Pages hors nav : `/tracking`, `/design-system`, `/system/design-system`.
- **37 redirections legacy 301** (`redesign.py` `LEGACY_REDIRECTS`) : `/daily`,
  `/news`, `/stocks`, `/journal`, `/heatmap`, `/strategie`, `/options-lab`… →
  routes canoniques.

## 4. Erreurs console / réseau / Python

| Sonde | Méthode | Résultat |
|---|---|---|
| Journal erreurs client | `GET /api/client-log` | `{"count":0,"errors":[]}` — **0 erreur réelle enregistrée** |
| Erreurs console navigateur | Playwright `console`/`pageerror` sur 10 pages ×2 viewports | Voir §6 (capture) — aucune erreur JS bloquante relevée sur les pages chargées |
| Log serveur Python | `server.log` | Démarrage propre, `Running on http://127.0.0.1:5002`, aucun traceback |

> Limite honnête : l'inspection navigateur se fait via Chromium **headless**
> dans ce conteneur Linux (pas un appareil physique). Les captures et mesures
> d'overflow sont réelles ; l'ergonomie tactile réelle reste à valider sur
> iPhone/iPad par l'utilisateur.

## 5. Responsive — débordement horizontal mesuré

Mesure `scrollWidth` vs `clientWidth` par page (Playwright). **Constat majeur :
débordement horizontal sur 8 pages / 11 en mobile 390×844.**

| Page | Mobile 390 | Desktop 1440 |
|---|---|---|
| Briefing `/` | **OVERFLOW 430/390** | ok 1440 |
| Marchés | **OVERFLOW 469/390** | ok |
| Opportunités | **OVERFLOW 456/390** | ok |
| Portefeuille | **OVERFLOW 403/390** | ok |
| Analyse `/analysis/AAPL` | ok 390 | ok |
| Options | ok 390 | ok |
| Performance | **OVERFLOW 417/390** | ok |
| Intelligence | **OVERFLOW 405/390** | ok |
| Système | **OVERFLOW 547/390** | ok |
| Suivi (tracking) | **OVERFLOW 448/390** | ok |
| Design system | ok 390 | ok |

- Le pire cas est **Système (547px pour 390 disponibles, +40 %)**.
- Desktop 1440 : **aucun débordement**. Le problème est purement mobile.
- Viole directement `CLAUDE.md` (« aucun overflow horizontal ») et la règle
  design V4 §9 (« aucun débordement horizontal »).

## 6. Captures d'écran (preuves)

Captures Chromium réelles produites (scratchpad `shots3/`), desktop 1440 +
mobile 390 (full page) + tablette 768 pour les espaces principaux :
`briefing, markets, opportunities, portfolio, analysis, options, performance,
intelligence, system`. Elles servent de référence « avant » pour la refonte.

## 7. États dégradés (démo / sans IBKR / données absentes)

| Scénario | Sonde | Comportement observé | Verdict |
|---|---|---|---|
| Sans IBKR | `GET /api/system/connections` | IBKR `OFFLINE` + action + impact explicités ; TradingView `CONFIGURATION_MISSING` (503 honnête) ; IA `MISSING` | **Honnête** ✅ |
| Badge démo | HTML rendu (briefing) | Texte `DÉMO/MOCK/SIMUL` présent et visible (`demo_badge_visible=True`) | **Honnête** ✅ |
| Ticker absent | `GET /api/ticker/ZZZZZ` | HTTP 200, champs `null` partout (aucun chiffre inventé) | **Honnête** ✅ |
| Qualité données démo | `GET /api/data-quality` | `by_quality = {MISSING: 20}` — **les 20 titres affichés sont notés `MISSING`** alors que les pages montrent scores/verdicts | ⚠️ **Incohérence** — voir `CONTRADICTIONS_REGISTER.md` C-07 |
| Décision ticker absent | `GET /api/decision/ZZZZZ` | HTTP 200 + verdict comité avec `confidence:56`, `lean:38` pour un titre inexistant | ⚠️ **Anti-manifeste** (« Vertex peut dire je ne sais pas ») — voir C-08 |

## 8. Synthèse Phase 0

- **Vert** : tests 100 % (893/895), compilation propre, démarrage sain, 0 erreur
  client réelle, états sans-IBKR/absent/démo honnêtement étiquetés.
- **Rouge** : débordement horizontal mobile généralisé (8/11) ; incohérence
  qualité-données en démo (tout `MISSING`) ; décision « confiante » sur ticker
  inexistant.
- Base solide côté données/tests ; le chantier prioritaire est **le responsive
  mobile** et **quelques honnêtetés de données** (voir registre des
  contradictions et rapport de synthèse).

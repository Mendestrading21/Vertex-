# VERTEX — Rapport de synthèse Phases 0–2

> **Audit réel, aucune modification du runtime.** Seuls des documents ont été
> créés sous `docs/refactor/`. IBKR READONLY, moteurs, tests et données intacts.

## 0. Contexte

Exécution des phases 0 (baseline), 1 (inventaire) et 2 (cartographie &
contradictions) du programme `vertex-total-rebuild`, **sans** commencer la refonte
des pages. Objectif : comprendre l'existant avec preuves avant toute
transformation.

## 1. Branche & commit

- Branche : **`agent/vertex-total-rebuild`**
- Commit de départ : **`362c7d417d8993c5f38343f35490e81b62fa52fa`**
- Environnement : conteneur Linux, Python 3.11.15, `DEMO=1 NO_IBKR=1 PORT=5002`.

## 2. Commandes exécutées — résultats exacts

| Commande | Résultat |
|---|---|
| `git branch --show-current` | `agent/vertex-total-rebuild` |
| `git ls-files \| wc -l` | **617 fichiers** |
| `python -m compileall -q terminal.py vertex` | **exit 0** |
| `python -m pytest tests/ -q` | **893 passed, 2 skipped — 14.48 s** |
| `DEMO=1 NO_IBKR=1 python terminal.py` + `/healthz` | **200**, `data_source:demo`, 8 moteurs, univers 517, scanned 20, IBKR off |
| `GET /api/client-log` | `{"count":0,"errors":[]}` — 0 erreur client |
| Sonde Playwright (Chromium) sur 11 routes × 2-4 viewports | captures + overflow réels |

## 3. Décompte du produit

| Élément | Nombre |
|---|---|
| Fichiers suivis | 617 |
| `terminal.py` | 10 734 lignes (monolithe) |
| Règles de routage (`url_map`) | **163** |
| Redirections legacy 301 | 37 |
| Espaces principaux (`PRIMARY_NAV`) | **9** (+ tracking + design-system) |
| Endpoints `/api` | ~90 sur 20 blueprints |
| Moteurs `engines`/`options`/`strategy` | 22 + 19 + ~8 |
| Graphiques instanciés dans les pages | ~55 (voir `CHART_INVENTORY.md`) |
| Tests | 895 (893 pass, 2 skip) |

## 4. État honnête des données (démo / sans IBKR / absent)

✅ **Bon** : badge démo visible ; `/api/system/connections` étiquette IBKR
`OFFLINE` / TV `CONFIGURATION_MISSING` / IA `MISSING` avec action+impact ; ticker
absent → champs `null` (aucun chiffre inventé) ; 0 erreur client.

⚠️ **À corriger** :
- **C-07** : en démo `/api/data-quality` renvoie **tout `MISSING`** (20/20) alors
  que les pages montrent scores/verdicts → message contradictoire.
- **C-08** : `/api/decision/ZZZZZ` (ticker inexistant) renvoie un verdict comité
  **confidence 56** au lieu de « données insuffisantes » → anti-manifeste.

## 5. Responsive — défaut le plus visible

**Débordement horizontal mobile (390 px) sur 8 pages / 11** :
Système 547, Marchés 469, Opportunités 456, Tracking 448, Briefing 430,
Performance 417, Intelligence 405, Portefeuille 403. Propres : Analyse, Options,
Design-system. **Desktop 1440 : aucun débordement.** Viole `CLAUDE.md` /
design-v4 §9.

## 6. Les 10 problèmes prioritaires

| # | Problème | Sévérité | Réf. |
|---|---|---|---|
| 1 | Débordement horizontal mobile sur 8/11 pages (pire : Système 547px) | 🔴 | Baseline §5 |
| 2 | Décision « confiante » sur ticker inexistant (`/api/decision/ZZZZZ` conf 56) | 🔴 | C-08 |
| 3 | Qualité données démo = tout `MISSING` malgré scores affichés | 🔴 | C-07 |
| 4 | Identité ambiguë : « Obsidian Prism / General Sans » (CLAUDE.md) vs « Obsidian Copper / Inter » (code) | 🔴 | C-04 |
| 5 | Graphiques doublons massifs (secteurs ×4, jauges régime/breadth ×3, funnel & radar dupliqués) | 🟠 | C-09 |
| 6 | 3 sources de couleurs divergentes non gardées (palette.py/JS/CSS, séries 2&5) | 🟠 | C-02/C-11 |
| 7 | 2 moteurs de chandeliers chargés ensemble sur Analyse | 🟠 | C-05 |
| 8 | 2 registres de navigation + incohérence « 8 vs 9 espaces » | 🟠 | C-01/C-06 |
| 9 | Monolithe `terminal.py` 10 734 l + 1 682 `style=` inline + pages `PAGE_*` mortes construites au boot | 🟠 | FILE_INVENTORY §1/9 |
| 10 | Hygiène : `position_inventory.json` (positions réelles) et `company_cache.json` (1,38 Mo) **commités** | 🟠 | FILE_INVENTORY §11 |

## 7. Contradictions critiques (rappel)

🔴 C-04 (identité), C-07 (qualité démo), C-08 (décision sans données). Détails et
sources dans `CONTRADICTIONS_REGISTER.md`. Chaque item cite **ses deux sources** et
propose une source canonique.

## 8. Graphiques — décisions provisoires

- **GARDER** : `an-chart` (chandeliers+MM+plan), suite options (payoff, scénarios,
  theta, iv-sensitivity), performance (equity/drawdown/monthly/dist/track-bar),
  `vx-trk-chart`, courbe des taux, waterfall santé, breadth-trend, un seul funnel.
- **FUSIONNER** : jauges VIX/Breadth/Régime (1 par page), suite secteurs Marchés
  (4→2), breadth 1-barre + rings, funnel & radar dupliqués.
- **MODIFIER** : `op-radar`→renommer (scatter) ; couleurs sans sens
  (`pf-opt-tree`, `vx-opp-rr`, `vx-brain-movers`) ; heatmaps/scatter en conteneur
  scrollable (overflow mobile).
- **SUPPRIMER / brancher** : galerie `dsc-*` (données factices) hors prod ;
  factories mortes (`correlationCard`, `factorCard`, `geoCard`, `volSurfaceCard`,
  `sparkbars`).

## 9. Fichiers legacy/morts potentiels (à VÉRIFIER, non supprimés)

- **P0** : 2 moteurs chandeliers ; 2 registres nav ; 3 sources de couleurs.
- **P1** : UI monolithe `ui/{signals,vault,options_lab,journal,sync_center,
  strategy_os,design_system,vx_kit,home_art}.py` (importés seulement par
  `terminal.py`) — **ne pas toucher `journal.py`/`vx_kit.py`** (clés sync desk).
- **P2 (renommer, pas supprimer)** : `options/legacy_engine.py`,
  `strategy/legacy_adapter.py`, `portfolio/legacy_basket_risk.py` — tous **ACTIFS**.
- **P4 (hygiène)** : `company_cache.json`, `position_inventory.json` → décision
  utilisateur (gitignore) ; `docs/redesign/*` 121 PNG à consolider.

## 10. Risques identifiés

- **Régression moteur** : toute correction de C-07/C-08 touche `decision_stack` /
  producteurs de qualité → exige un **test rouge** d'abord (règle SKILL/gardien
  moteurs).
- **Suppression prématurée** : les « doublons » sont souvent les deux moitiés de
  la migration strangler ; supprimer sans preuve d'imports/routes/tests casse.
- **Service worker** : tout changement de shell impose un bump `td-shell-vN`
  (`system.py`) + tests.
- **Clés sync desk** : nouvelle clé localStorage → 4 registres à mettre à jour.
- **Validation mobile** : mesures faites en Chromium headless, pas sur appareil
  physique — à confirmer côté utilisateur (iPhone/iPad).

## 11. Plan exact de la PR suivante (PR n°1 — Fondations honnêtes & responsive)

> Périmètre restreint, testable, réversible. **Ne touche pas** les 8 pages en
> profondeur ; corrige les défauts transverses les plus critiques + prépare la
> couche design.

1. **Responsive mobile (défaut n°1)** — auditer et corriger la cause du
   débordement (conteneurs `overflow-x` sur heatmaps/tables/scatter, largeurs
   fixes, treemaps `clientWidth`). Cible : `scrollWidth ≤ clientWidth` sur les
   8 pages en 390 px. Ajouter un **test gardien** de non-débordement (sonde
   Playwright ou assert layout).
2. **Honnêteté données** —
   - C-08 : `decision_stack` renvoie un état « données insuffisantes » pour un
     symbole hors univers (test rouge → correction → non-régression).
   - C-07 : `/api/data-quality` en démo étiquette `DEMO/SIMULATED` au lieu de
     `MISSING` (test dédié).
3. **Palette : source unique** — désigner `palette.py` canonique, dériver JS/CSS,
   **durcir** `test_js_theme_matches_python_palette` pour comparer `SERIES` entière
   (corrige C-02/C-11) ; purger commentaires « cuivre/orange » (C-03).
4. **Nettoyage sûr, non destructif** — confirmer par test navigateur lequel des
   2 moteurs chandeliers rend (C-05) et retirer le redondant ; documenter la
   décision « 8 vs 9 espaces » sans changer le comportement (C-01).
5. **Décision d'identité (bloquant design)** — trancher C-04 avec l'utilisateur
   (« Obsidian Copper / Inter » vs « Obsidian Prism / General Sans ») **avant** la
   PR n°2 (design system).
6. **Hygiène dépôt** — proposer le retrait du suivi git de `position_inventory.json`
   et `company_cache.json` (décision utilisateur ; **aucune suppression sans accord**).

**Validation PR n°1** : `compileall` OK ; `pytest` 100 % ; `/healthz` + 9 espaces
200 ; 0 débordement mobile ; `/api/client-log` 0 ; captures avant/après ;
`docs/refactor/validation/PR-01.md` (commit, commandes, résultats, captures,
anomalies, risques, verdict GO/GO-avec-réserves/NO-GO).

**PR ultérieures** (séquence SKILL) : n°2 design system & chart system · n°3
navigation & architecture (décision 8 vs 9) · n°4 Aujourd'hui & Marchés · n°5
Opportunités & Analyse · n°6 Portefeuille · n°7 Options · n°8 Journal & Système ·
n°9 nettoyage/perf/accessibilité/doc.

## 12. Livrables produits (ce lot)

`docs/refactor/` : `VERTEX_BASELINE_AUDIT.md`, `FILE_INVENTORY.md`,
`ROUTE_ENDPOINT_MAP.md`, `PAGE_DATA_GRAPH_MATRIX.md`, `CHART_INVENTORY.md`,
`CONTRADICTIONS_REGISTER.md`, `VISUAL_REFERENCE_MAP.md`, `PHASE_0_2_REPORT.md`
(ce document). Captures de baseline dans le scratchpad de session (desktop /
mobile / tablette, 9 espaces).

## Format de compte rendu (rappel SKILL)
- **Constat** : produit en migration strangler, données globalement honnêtes,
  tests verts.
- **Problème** : responsive mobile généralisé, 2-3 honnêtetés de données,
  doublons graphiques, identité ambiguë, monolithe.
- **Décision** : audit documenté, aucune modification runtime ; PR n°1 ciblée.
- **Implémentation** : 8 documents d'audit sourcés.
- **Validation** : voir §2 (tests/healthz/overflow réels).
- **Reste à faire** : exécuter PR n°1 après arbitrage de l'identité (C-04) et de
  l'hygiène (positions/cache) avec l'utilisateur.

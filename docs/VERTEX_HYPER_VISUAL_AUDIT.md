# VERTEX — HYPER VISUAL INTELLIGENCE : AUDIT & FEUILLE DE ROUTE

> Branche `feature/vertex-hyper-visual-intelligence` · baseline **896 tests verts, 1 skipped**.
> Invariants respectés : aucune donnée inventée · READONLY inviolable · aucune décision/stratégie/source/connexion modifiée · aucun chemin d'exécution d'ordre.

Ce document est l'audit préalable exigé (§40) et le plan d'exécution par phases.
Il est **honnête sur le périmètre** : la refonte complète (§12–28) est un chantier
multi-phases. Chaque phase est livrée testée, vérifiée en navigateur, et commitée.

---

## 0. État réel du socle (déjà fait dans les passes précédentes)

Le terminal a déjà reçu, sur `vertex-connection-setup`, une refonte lourde :

- **Dashboard** (`briefing.py`) : 9 sections hiérarchisées (Situation → Brief →
  Actus → Marchés → Pouls → Mouvements → Opportunités → Secteurs → Portefeuille),
  graphique héros interactif, jauges, waterfall santé, treemap secteurs, brief
  repliable, badges séance/scan, rafraîchissement live 2 min.
- **Opportunités** (`opportunities_page.py`) : SCREENER 5 vues (screener / options /
  portfolio / anomalies / calendar) avec barre de filtres collante, 4 préréglages,
  ~15 filtres, nuage avantage×proba (zones élite, Kelly, no-trade), heat secteur×
  statut cliquable, distribution live, table triable 15 colonnes, plan de trade,
  espérance, grade, ruban de momentum, synchro URL partageable.
- **Système de couleurs** : déjà sémantiquement séparé — `--vx-signal-*` (marque
  olive #84aa31) ≠ `--vx-positive` (#36c889) ≠ `--vx-negative` (#ed655c) ≠
  `--vx-warning` (#dda23b) ≠ `--vx-option`/`--vx-violet` (#9c79d0). **Le problème
  D « trop de vert » est donc déjà largement traité** au niveau des tokens ;
  ce qui manquait : un token macro/cross-asset dédié et des séries neutres riches.
- **Contrat graphique** : chaque carte (`VXCharts.card`) porte déjà titre +
  question + conclusion + source + fraîcheur + bouton « Comprendre ce graphique ».
- **Fuite Chart.js** : corrigée à la racine (destruction avant re-paint).
- **Service worker** : `td-shell-v60`.

## 1. Inventaire des pages & routes (réel)

| Route | Module | État | Hero ? | Priorité refonte |
|---|---|---|---|---|
| `/` Dashboard | `briefing.py` | refondu | oui (graphique marché) | affiner (§12) |
| `/opportunities` | `opportunities_page.py` (5 vues) | refondu | oui (nuage) | affiner (§13-15) |
| `/portfolio` | `portfolio_page.py` | refondu partiel | non net | **cockpit (§23)** |
| `/analysis/<sym>` | `analysis_page.py` | riche | oui (candlestick) | onglets (§24) |
| `/options`, `/options/<sym>` | `options_intel_page.py`, `options_symbol_page.py` | fonctionnel | partiel | **section majeure (§16-22)** |
| `/performance` | `performance_page.py` | vide sans trades | non | Progress Center (§25) |
| `/intelligence` | `intelligence_page.py` | fonctionnel | partiel | §26 |
| `/system` | `system_page.py` | fonctionnel | partiel | Operations Center (§27) |

## 2. Données réellement disponibles (vérifié via /scan, /api/command)

- **rows** (par titre) : `score verdict sector industry price change perf_w/m/q/y rs
  rvol pos52 rsi grade zscore gap_pct trend squeeze breakout pullback accumulation
  distribution anomalies anomaly_score anomaly_lvl mtf{state,note} vehicle{reco,why}
  vx_edge vx_pwin vx_kelly vx_rr vx_ev vx_asym vx_notrade vx_flags st_tech/mom/fund/
  risk/conf playbook profile setup_quality rr rr_ok strat_score sigcount ext_atr rsi_div`
- **detail[sym]** : `plan{entry,stop,tp1-3,rr} series{close,dates,ema20,sma50,sma200,
  rsi,volume} thesis chart_read`. ⚠ `earnings_dte` non peuplé côté detail.
- **options_board** : `type bucket exp dte strike pop p_itm p_tgt danger bid ask mid
  cost be iv delta gamma theta theta_burn vega oi vol spread quality quality_parts
  em_pct swing_ret swing_ok tgt stale grade`.
- **APIs** : `/api/command` (top_stocks, top_options, counts, alerts, risk{avg_corr,
  max_corr, diversification, hhi, no_new_risk, sectors, limits}), `/api/market/summary`,
  `/api/market/regime`, `/api/opportunities/funnel`, `/cal-feed`, `/news-feed`,
  `/api/options/simulate`, `/api/options/vol-charts/<sym>`, `/api/options/scenarios/<sym>`.

**Données absentes (à afficher en état vide honnête, jamais inventé)** : historique
d'IV réalisée, surface d'IV complète, equity curve (tant que < N trades clôturés),
earnings_dte fiable, rho.

## 3. Problèmes visibles restants (diagnostic §2 du brief)

| # | Problème | Où | Correctif prévu |
|---|---|---|---|
| A | Tables 100 lignes brutes | opportunités univers, chaînes | pagination/virtualisation, scroll interne borné |
| B | Poids visuel uniforme | portfolio, system | hiérarchie 4 niveaux, KPI strip |
| C | Textes trop petits par endroits | jauges, tables denses | échelle typo tokens |
| D | Trop de vert | **déjà traité** (tokens séparés) | + token teal macro, séries neutres |
| E | Graphiques silencieux | options, système | contrat lecture déjà en place → l'étendre |
| F | Options sous-développées | /options | labs dédiés (chain, vol, greeks, scenarios) |
| G | Espaces mal utilisés | portfolio, performance | grille 12 col explicite, hauteurs adaptées |

## 4. Plan par phases (chaque phase = commit testé + vérifié navigateur)

- **Phase F1 — Fondation (en cours)** : audit + tokens manquants (teal macro,
  stone/plum, échelle typo hero/table/kpi-lg) + grille 12 col explicite
  (`.vx-span-*`) + skeletons partagés. Zéro régression (add-only).
- **Phase F2 — Système graphique** : `chart-theme.js` (palette séries incluant
  teal macro), lecture descriptive généralisée, bouton plein écran + vue tableau
  sur les graphiques majeurs, cycle de vie (lazy render via IntersectionObserver).
- **Phase F3 — Inspecteur & Data Grid** : `inspector-drawer.js` réutilisable,
  `data-grid.js` (header sticky, tri, pagination/virtualisation, densité).
- **Phase P1 — Portefeuille cockpit** (§23) : KPI strip, treemap + allocations
  compactes, distance aux stops, corrélation, exposition options.
- **Phase P2 — Options labs** (§16-22) : overview command center, chaîne pro,
  volatility lab, greeks lab, scenarios lab, position detail.
- **Phase P3 — Performance / Intelligence / Système** (§25-27).
- **Phase R — Responsive & accessibilité** (§36, §38) : test 11 résolutions,
  focus visible, reduced-motion, tableaux alternatifs.

## 5. Critères de validation (par phase)

- `python -m pytest tests/ -q` reste vert (896+).
- `/api/client-log` = 0 erreur ; console navigateur = 0 erreur.
- Aucun débordement horizontal à 375/768/1440.
- Chaque graphique majeur : source + fraîcheur + lecture visibles.
- Aucune valeur inventée ; états vides honnêtes documentés.
- SW bumpé à chaque changement de shell.

---

*Ce document sera enrichi à chaque phase (état après / preuves / captures).*

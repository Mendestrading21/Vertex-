# VERTEX — Inventaire des graphiques (Phase 2)

> Branche `agent/vertex-total-rebuild` @ `362c7d4`. Audit lecture seule.
> Moteur de rendu **unique** : Chart.js via `VXCharts.mount` (seul `new Chart(...)`
> du code — `chart-core.js:47`) + primitives SVG maison + TradingView Lightweight
> Charts (chandeliers pro, auto-hébergé). Toute carte passe par le contrat
> `C.card` (titre / question / conclusion / pied source-date-mode).

## A. API `VXCharts` (`vertex/static/vertex/js/charts/chart-core.js`)

**Primitives Chart.js** : `mount`, `axes`, `card`, `sparkline`, `area`, `bars`,
`donut`, `multiLine`, `levelLines` (plan entrée/stop/TP), `eventMarkers`.
**Primitives SVG maison** : `gauge`, `treemap`, `waterfall`, `radar`, `flow`,
`rings`, `funnel`, `sparkbars`.
**Cartes haut niveau** (wrappers) : `barCard`, `breadthCard`, `correlationCard`,
`donutCard`, `drawdownCard`, `equityCard`, `factorCard`, `geoCard`,
`heatmapCard` (HTML/CSS, pas canvas), `areaCard`, `sectorCard`, `sparklineInto`,
`timelineCard` (HTML), `priceCard`, `candlestickCard`, `lwCandlestickCard`
(TradingView), `volSurfaceCard`, `payoffCard`, `scenarioMatrix`, `thetaCard`,
`ivSensitivityCard`, `alertFromLevel`.

**Factories jamais instanciées dans les pages (mortes à l'inventaire)** :
`correlationCard`, `factorCard`, `geoCard`, `volSurfaceCard`, `sparkbars` (hors
démo). → à brancher pendant la refonte ou retirer.

## B. Palette / thème — 3 sources qui doivent s'accorder

`vertex/visualization/palette.py` (autorité Python) ·
`chart-theme-obsidian-copper.js` (thème JS) · `tokens.css` (variables CSS).

| Rôle | Python `palette.py` | JS `chart-theme` | Accord ? |
|---|---|---|---|
| brand / série 0 | `#84aa31` | `#84aa31` | OUI |
| neutral / série 2 | `#9d978e` (CSS `--vx-neutral-chart`) | `#8f8a83` (`series[2]`) | **NON** |
| copper / série 5 | `#747d75` | `#48631b` (`series[5]`) | **NON** |
| copper_light | `#a3ca42` | `#84aa31` | **NON** |
| option / série 3 | `#9c79d0` | `#9c79d0` | OUI |
| positive / negative / warning | `#36c889` / `#ed655c` / `#dda23b` | idem | OUI |

- **Le tableau `SERIES` diverge sur 2 des 6 couleurs (indices 2 et 5).** Le test
  `tests/test_visual_intelligence.py::test_js_theme_matches_python_palette:37` ne
  vérifie QUE la présence de brand/beige/option + absence de bleu — il **ne
  détecte pas** ces divergences. Divergence réelle, non gardée. (Voir C-02.)
- **Commentaires périmés** : `palette.py` et `chart-theme-obsidian-copper.js`
  décrivent la marque comme « cuivre/orange » alors que `#84aa31` est un **vert
  olive**. Le nom de fichier `obsidian-copper` est trompeur. (Voir C-03.)
- **3ᵉ copie codée en dur** de la palette dans `chart-core.js:13-19` (repli si
  `VXChartTheme` absent) qui suit les valeurs JS, pas Python.
- Garde-fou zéro-bleu : alias `blue`/`cyan`/`info` remappés sur vert/beige —
  **aucun bleu réel**, conforme.

## C. Inventaire des graphiques par page

> `Concl.` = conclusion textuelle présente · `Dbl` = doublon suspecté.

### Briefing (`briefing.py`)
| id | ligne | titre | type | endpoint | Concl. | Dbl |
|---|---|---|---|---|---|---|
| data-spark | 301 | strip indices | sparkline | `/scan` series | non | non |
| vx-regime-gauge | 357 | Confiance régime | gauge | `/api/market/regime` | oui | **oui** (=vx-gauge-trend) |
| vx-gauge-vix | 417 | VIX | gauge | `/api/market/summary` | oui | **oui** (=markets vix) |
| vx-gauge-breadth | 425 | Breadth | gauge | summary | oui | **oui** (=breadth-chart) |
| vx-gauge-trend | 434 | Régime | gauge | regime | oui | **oui** (redondant même page) |
| vx-market-chart | 376 | Marché US SPY | areaCard | `/scan` SPY | oui | **oui** (=markets spy) |
| vx-breadth-chart | 394 | Breadth/participation | breadthCard (1 barre) | summary | oui | **oui** (redondant gauge) |
| vx-opp-rr | 498 | Priorité R:R | bars horiz | `/api/command` | non | non |
| vx-opp-posture | 518 | Posture comité | donutCard | `/api/command` | oui | non |
| vx-rotation | 538 | Rotation sectorielle | sectorCard | `/scan` sectors | oui | **oui** (=markets sectors) |
| vx-calendar | 618 | Calendrier | timelineCard | `/cal-feed` | non | **oui** (=markets cal) |

### Marchés (`markets_page.py`)
Contient **4 vues des mêmes `scan.sectors`** : `vx-mk-sectors-chart` (bar, 489),
`vx-mk-sectors-heat` (heatmap HTML, 498), `vx-mk-rotation` (RRG scatter, 539),
`vx-mk-sectors-tree` (treemap, 528). Plus **3 jauges régime** et **3 jauges
breadth** répétées (regime-gauge 246, breadth-gauge 573, vix-gauge 738,
vol-breadth 746, vol-regime 754…). Autres : `vx-mk-multi` (indices rebasés, 356),
`vx-mk-spy` (382), `vx-mk-yield` (courbe des taux, 420), `vx-mk-macro-cal` (461),
`vx-mk-breadth-trend` (615), `vx-mk-verdicts` (donut, 631), `vx-mk-funnel`
(entonnoir, 641 — **doublon** de opportunités), `vx-mk-rings` (659),
`vx-mk-health-wf` (waterfall, 674), `vx-mk-dist` (**barres HTML maison, hors
VXCharts**, ~690).

### Opportunités (`opportunities_page.py`)
`op-radar` (**scatter mal nommé « radar »**, 165), `op-funnel-viz` (144 —
**doublon** markets funnel), `op-ranking` (**scoreBar HTML maison**, 103),
`op-payoff` (370), `op-scenarios` (scenarioMatrix, 383), `op-theta` (387),
`op-iv` (391), timeline (450).

### Analyse (`analysis_page.py`)
`an-scorecard-radar` (radar 5 scores, 298 — **doublon** intelligence radar),
`an-chart` (**lwCandlestick + MM20/50/200 + plan + événements**, 327) — **pièce
maîtresse**.

### Portefeuille (`portfolio_page.py`)
`pf-contrib-cv` (P&L par position, bars, 161), `pf-alloc-tree` (treemap, 182 —
recouvre contrib+roles), `pf-roles-donut` (193), `pf-opt-tree` (treemap options,
**couleur = PUT/CALL = peu de sens financier**, 349), `pf-comb-pf` (payoff
combiné, 408), `od-payoff` (drawer, 456), `pf-risk-gauge` (HHI, 544),
`pf-sector-donut` (564).

### Performance (`performance_page.py`)
`vx-pf-equity` (215), `vx-pf-drawdown` (225), `vx-pf-monthly` (heatmap HTML,
257), `vx-pf-dist` (272), `vx-pf-track-bar` (394). Données **localStorage
journal** (mode delayed, honnête).

### Intelligence (`intelligence_page.py`)
`vx-analyst-radar` (313 — **doublon** analysis scorecard), `vx-committee-gauge`
(339), `vx-research-chart` (Sharpe walk-forward, 536), `vx-imp-flow` (chaîne
d'impact, 605).

### Système (`system_page.py`)
`vx-brain-movers` (barCard, 407), `vx-sys-gauge` (moteurs OK, 404),
`vx-data-quality-chart` (donut FRESH/RECENT/STALE/EXPIRED/MISSING, 579).

### Suivi / Options-intel / Design-system
`vx-trk-chart` (bars idée vs SPY, `tracking.js:63`) · `vx-opt-gauge-radial`
(`options-intel.js:137`), `strat-pf-*` (payoffs par stratégie, 498) · galerie
`dsc-*` (`design_system_demo.py:134-155`, **données factices**, vitrine).

## D. Décisions préliminaires (À VALIDER)

**Transverse palette**
- **MODIFIER** — réconcilier les 3 palettes (série neutre `#9d978e`↔`#8f8a83`,
  copper `#747d75`↔`#48631b`) et **renforcer** `test_js_theme_matches_python_palette`
  pour comparer `SERIES` entière.
- **MODIFIER** — purger les commentaires « cuivre/orange » et renommer
  `chart-theme-obsidian-copper.js` (identité réelle = vert Signal).

**FUSIONNER (doublons)**
- Jauges VIX / Breadth / Régime répétées 2-3×/page → **une seule instance/page**.
- Suite secteurs de Marchés (bar + heatmap + RRG scatter + treemap = 4 vues des
  mêmes données) → **garder 2 au maximum** (ex. RRG décisionnel + heatmap détail).
- Breadth : `breadthCard` **à une seule barre** = chart dégénéré ; les `rings`
  répètent des chiffres déjà en KV → garder gauge + tendance multi-séances.
- Funnel dupliqué Marchés↔Opportunités ; radar scorecard dupliqué
  Analyse↔Intelligence → source unique.

**MODIFIER (couleur/nommage/mobile)**
- `op-radar` → renommer (c'est un **scatter**).
- Couleur sans sens financier : `pf-opt-tree` (PUT/CALL), `vx-opp-rr`,
  `vx-brain-movers` (couleur figée) → porter la couleur par une métrique
  décisionnelle ou passer en neutre.
- Heatmaps HTML larges (`sectors-heat`, `pf-monthly`, `scenarioMatrix`) →
  conteneur `overflow-x`; RRG scatter illisible < 380px ; treemaps recalcul
  `clientWidth` au resize à vérifier. **(lié à l'overflow mobile — Phase 0 §5.)**

**GARDER (haute valeur)**
- `an-chart` (chandeliers + MM + plan), suite options (`payoffCard`,
  `scenarioMatrix`, `thetaCard`, `ivSensitivityCard`), performance
  (`equity/drawdown/monthly/dist/track-bar`), `vx-trk-chart`, `vx-mk-yield`,
  `vx-mk-health-wf`, `vx-mk-breadth-trend`, un seul `funnel`.

**SUPPRIMER / déplacer**
- Galerie `dsc-*` (données factices) hors production si non destinée à
  l'utilisateur final.
- Factories mortes (`correlationCard`, `factorCard`, `geoCard`, `volSurfaceCard`,
  `sparkbars`) — à brancher ou retirer.

> Toutes ces décisions sont **provisoires** : elles reposent sur la lecture du
> code, pas encore sur un test navigateur graphique par graphique. Elles seront
> tranchées page par page dans les PR de refonte.

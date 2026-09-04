# Page : Portefeuille (`/portfolio` + `/tracking` → `portfolio_page.py`)

> Fiche **amorcée** (audit). À compléter avant le lot de refonte Portefeuille. Gabarit :
> `.claude/skills/vertex-maximum/templates/page-audit-template.md`.

## Mission de la page
Donner l'exposition réelle et le risque du portefeuille IBKR (lecture seule) : équipe/positions, options,
risque, watchlist. Répond à « quelle est mon exposition ? quel risque ? que surveiller ? ».

## Questions auxquelles elle doit répondre
Quelles positions et quel P&L (réel, provenance) ? Quelle exposition par secteur/facteur ? Quel risque agrégé
(greeks nets, drawdown, corrélations) ? Quelles valeurs surveillées et pourquoi ?

## Données utilisées / source
Positions & P&L : IBKR read-only (`positions/`, `portfolio/`, `_live_meta`/`_live_quotes`) ; greeks : broker vs
`MODEL_ESTIMATE` ; watchlist : localStorage synchronisé (`desk_data.json`, clés desk-sync). Statut live via
`_sync_ibkr_state` (fraîcheur 75 s).

## Composants / graphiques présents
Onglets `?view=team|positions|options|risk|watchlist`. Tables de positions, tuiles KPI (P&L, exposition), greeks
nets, `VXCharts` (donut/secteur, correlation-matrix, factor, geographic-exposure, drawdown).

## Problèmes identifiés (reliés à l'audit)
- **DAT-01 (P0)** — une position/valeur absente ou un flux coupé ne doit pas afficher `0` → `—`/`unavailable`.
- **DAT-03 (P1)** — chaque chiffre affiché (P&L, prix, greeks) doit porter **source + fraîcheur + réel/estimé**
  (footer `VX.updateIndicator`). C'est la page la plus sensible à la provenance.
- **IBK-01/02** — badge live = socket réel ; exposer delayed/stale/partial explicitement.
- **CMP-02** — 4 systèmes de tuiles à unifier (MetricCard). **A11Y-01** — P&L/risque ne dépendent pas que du rouge/vert.

## Plan d'implémentation (lot dédié)
1. Provenance visible sur chaque valeur (enveloppe `ProvenancedValue`, DAT-02). 2. Absence ≠ 0. 3. États
delayed/stale/partial rendus. 4. Tuiles → MetricCard. 5. A11y (signe/icône sur risque). 6. Watchlist : vérifier
que les clés sync sont dans les 4 listes (gardien).

## Tests / critères de validation
`pytest` 100 % (dont `test_desk_sync_keys_single_source_of_truth`) ; `/api/client-log`=0 ; navigateur réel sur les
5 onglets ; provenance présente partout ; démo étiquetée. DoD : `../../.claude/skills/vertex-maximum/references/page-definition-of-done.md`.

## Statut
**À FAIRE** (fiche amorcée ; aucune modif de code cette session).

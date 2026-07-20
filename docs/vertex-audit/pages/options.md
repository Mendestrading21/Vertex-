# Page : Options (`/options` + `/options/<sym>` → `options_intel_page.py` · `options_symbol_page.py`)

> Fiche **amorcée** (audit). À compléter avant le lot de refonte Options. Gabarit :
> `.claude/skills/vertex-maximum/templates/page-audit-template.md`.

## Mission de la page
Comprendre la volatilité et construire des scénarios d'options : chaîne, IV/skew, greeks, scénarios de prix,
événements. Espace où le **violet** est la couleur sémantique autorisée (options).

## Questions auxquelles elle doit répondre
Quelle est la structure de vol (IV, skew, surface) ? Quels greeks (broker vs modèle) ? Quels scénarios de P&L
selon spot/IV/temps ? Quels événements (earnings) impactent le pari ? Quelle stratégie multi-jambes convient ?

## Données utilisées / source
Chaîne & greeks : IBKR (`data_sources/ibkr_option_chain.py`, `greeks_source` = `GREEKS_BROKER` sinon
`MODEL_ESTIMATE`) ; scénarios : `options/scenario_pricer.py` (`MODEL_ESTIMATE`) ; IV/surface : `options/`.
Fraîcheur via caches `_OPTPACK_CACHE` / `_VIEW_MISS` (voir `../10-performance-audit.md`).

## Composants / graphiques présents
Onglets `?view=overview|volatility|radar|scenarios|events`. Graphes `VXCharts` : `option-chain(-grid)`,
`option-payoff`, `option-scenarios`, `option-theta`, `option-iv-sensitivity`, `vol-surface`, greeks radar.

## Problèmes identifiés (reliés à l'audit)
- **RT-01 (P1) — ✅ RÉSOLU** : collision `/options/<sym>` (JSON vs page). JSON déplacé sous `/api/options/pack/<sym>`,
  2 consommateurs corrigés, page réservée. Vérifié DEMO (`/api/options/pack/AAPL`→JSON, `/options/AAPL`→HTML) + 919 tests.
- **DAT-01 (révisé P2)** — chaîne vide déjà honnête (`available:false`, cellules `None`) — vérifié DEMO ; résidu
  étroit OI/vol au producteur live (voir `../06-data-provenance.md`).
- **DAT / honnêteté greeks** — bien étiquetés `MODEL_ESTIMATE` vs broker ; vérifier le rendu du badge sur chaque tuile.
- **CMP-02** — tuiles KPI à migrer vers MetricCard. **CHT-02** — contrat de graphe (source/ts/question/conclusion).

## Plan d'implémentation (lot dédié)
1. Déplacer le JSON vers `/api/options/<sym>` ; réserver `/options/<sym>` à la page ; mettre à jour les appelants JS.
2. Durcir l'absence de chaîne → `unavailable`. 3. Migrer tuiles → MetricCard. 4. Contrat de graphe sur payoff/
scénarios/IV/greeks. 5. Vérifier violet=options exclusif.

## Tests / critères de validation
`pytest` 100 % (dont gardiens options) ; `/api/client-log`=0 ; navigateur réel sur les 5 onglets + dossier titre ;
badges provenance/greeks corrects ; byte-identique là où déterministe. DoD : `../../.claude/skills/vertex-maximum/references/page-definition-of-done.md`.

## Statut
**À FAIRE** (fiche amorcée pour cadrer le lot ; aucune modif de code cette session).

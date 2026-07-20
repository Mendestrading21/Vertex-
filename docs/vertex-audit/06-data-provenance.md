# 06 — Provenance, fraîcheur & intégrité des données

Règle produit n°4 : **jamais de chiffre inventé présenté comme réel** ; donnée absente → `—`/`n/d` ; distinguer
`0` (vrai zéro) · absent · `N/A` · `Indisponible` · `Estimation` · `Retardée` · `Périmée`.

## Ce qui est déjà bien fait
- **Greeks étiquetés** : `GREEKS_MODEL = 'MODEL_ESTIMATE'` (`vertex/options/models.py:16`,
  `vertex/data_sources/models.py:30`) ; `greeks_source = GREEKS_BROKER if broker else 'MODEL_ESTIMATE'`
  (`data_sources/ibkr_option_chain.py:77`). Scénarios : `scenario_pricer` porte `MODEL_ESTIMATE`
  (`options/scenario_pricer.py:7`), rendu jusqu'en UI (`options-symbol.js:195`, `analysis_page.py:613`).
- **Schéma de provenance** documenté (`vertex/visualization/schemas.py:17` : `source` = IBKR / MODEL_ESTIMATE / DESK…).
- **Mode dégradé honnête** : `services/startup.py:48` → `'OFFLINE', 'NO_IBKR=1 — marques desk/EOD, Greeks MODEL_ESTIMATE'`.
- **Fraîcheur socket** : garde-fou 75 s (`_sync_ibkr_state`, voir `09`).

## Findings
- **DAT-01 (P2 — révisé après vérification, ex-P0).** Le producteur IBKR **brut** `chain()` (`terminal.py:900-908`)
  émet `0`/`0.0` pour IV/OI/volume/bid/ask/last absents. **MAIS** vérifié en lisant + en testant en DEMO : la
  couche de normalisation `_persist_chain_full` (`terminal.py:1178` `_q` `>0 else None` ; `:1180` `iv if iv else
  None`) reconvertit ces `0` en **`None` honnête** avant tout affichage, et l'endpoint `/api/options/chain-grid`
  renvoie un **état vide honnête** (`available:false` + note) quand la chaîne manque — confirmé empiriquement
  (chain-grid & surface AAPL/bogus → `available:false`, aucun faux `0`). ⇒ **pas de masquerade user-visible.**
  Résidu réel étroit : (a) OI/volume où `0` légitime et « absent » restent confondus au producteur brut
  (`terminal.py:904-905`) ; (b) le chemin DataFrame `_IbkrChainSide` (`terminal.py:1215`) → moteurs
  (`legacy_engine`, `on_demand`) porte les `0` bruts, mais les consomme en calcul (`quoted = bid>0 and ask>0`),
  pas en affichage. **Action** (P2, chemin IBKR live — non testable en cloud) : au producteur, distinguer NaN→`None`
  de vrai `0` pour OI/volume ; à ne faire qu'avec vérification locale IBKR. **Ne pas** dégrader la couche
  d'affichage déjà honnête.
- **DAT-02 (P2) — Enveloppe de provenance éclatée.** L'info existe (`_live_meta`, `_live_quotes`,
  `marketDataType`, `greeks_source`, caches TTL) mais **pas de type unique**. **Action (Phase 2/6)** : introduire
  une enveloppe `ProvenancedValue` : `value · source · timestamp · quality · latency · environment · accountId ·
  currency · isEstimated · isDelayed · isStale · error`, portée du moteur jusqu'au footer `VX.updateIndicator`.
- **DAT-03 (P2) — Uniformité du footer de provenance.** Vérifier que **chaque** carte affichant un chiffre porte
  source + timestamp + état (live/delayed/stale/estimated). Pages à repasser : Portefeuille, Options, Dashboard.
- **DAT-04 (P1) — Anti-mock silencieux.** Toute donnée synthétique → badge `DÉMO/MOCK/SIMULATED` ; « démo »
  seulement si `DEMO_MODE`. Chercher les fallbacks qui remplacent une source réelle sans étiquette.

## Chaîne de sources
IBKR (live/delayed) → yfinance → stooq → demo (`DEMO_MODE`/`NO_IBKR`). Chaque valeur dit d'où elle vient.
News/textes externes : **toujours** via `news_plus.sanitize_news()` avant rendu (XSS). Détail contrat :
`references/ibkr-data-contract.md` + `.claude/rules/vertex-data-integrity-rules.md`.

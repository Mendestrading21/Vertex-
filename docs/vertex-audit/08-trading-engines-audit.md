# 08 — Audit des moteurs de décision (trading)

Pipeline déterministe : **raw → signaux → scores → scénarios → recommandations** (jamais → ordre). Modules
(`vertex/engines/`) : `decision_stack` (vérité des verdicts), `recommendation` (façade unique + vocabulaire
`__VXVOCAB`), `decide`/`context`, `evidence`, `reasoning`, `scorecard`, `committee`, `quant_engine`, `backtest`,
`analysis`, `indicators`, `track_record`, `stats`, `strategy_fit`, `swing`, `timeframes`, `market_lens`,
`multileg_lab`, `options_lab`, `performance_ledger`. Physique du marché : `regime_features.py` (Hurst / entropie /
Kaufman / OU). Simulation : Monte-Carlo GBM (~1200 chemins), block-bootstrap (~1500).

## Ce qui est bien fait
- **Déterminisme mesuré** : memoization par empreinte BLAKE2b (`_analyse_fp`/`_ANALYSE_MEMO`), memo backtest
  (`_BT_MEMO`), memo strike (`_STRIKE_MEMO`) — vérifiés **byte-identiques** memo vs calcul frais (voir `10`).
- **Estimations étiquetées** : greeks `MODEL_ESTIMATE` vs `GREEKS_BROKER`, scénarios `MODEL_ESTIMATE` (voir `06`).
- **Façade unique** `recommendation` + vocabulaire canonique `__VXVOCAB` (cohérence sémantique).

## Findings à vérifier (via `vertex-trading-auditor`)
- **ENG-01 (P1) — Plafonds explicites & testés.** Confirmer par test que Kelly est plafonné (~12 %) et `p_win`
  plafonné (~0.85) **dans le code servi** (pas seulement en doc). Ajouter/relier un gardien si absent.
- **ENG-02 (P2) — Explicabilité de bout en bout.** Chaque recommandation affichée doit exposer ses facteurs
  (`evidence`/`reasoning`) : vérifier qu'aucune reco n'arrive « nue » en UI. Relier verdict `decision_stack` →
  facteurs → rendu.
- **ENG-03 (P2) — Validité statistique visible.** MC/bootstrap doivent afficher n (chemins/rééch.) et l'horizon ;
  refuser d'afficher un intervalle si l'échantillon est insuffisant (« pas assez de données fiables », règle §6).
- **ENG-04 (P1) — Sémantique unique des verdicts.** Un même verdict = même mot + même couleur sur toutes les
  pages et graphes. Auditer `__VXVOCAB` vs libellés réels des pages (Analyse, Opportunités, Intelligence).
- **ENG-05 (P1) — Zéro chemin d'ordre.** Reconfirmer que les 17 outils d'ordre restent interdits
  (`vertex/ai/tool_registry.py`) et qu'aucun moteur n'expose de méthode d'exécution (gardiens `test_ai_api.py`).

## Cible
Moteurs = source déterministe et **explicable** de recommandations et de **préparation** de tickets (sizing,
perte max, marge/risque, greeks) ; jamais d'exécution. Détail : `references/trading-domain-rules.md`.

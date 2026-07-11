# Vertex Strategy — Audit forensique (avant refonte Strategy OS)

Date : 2026-07-11 · Branche : `claude/vertex-strategy-os-h17dso` · Baseline : 250 tests verts.

> Note de rédaction : l'exigence produit impose ZÉRO occurrence de nom personnel
> dans l'arbre final, y compris dans les documents d'audit. L'ancien package
> Python à nom personnel est donc désigné ici « **ancien package** » (23 modules,
> ~3 872 lignes, à la racine du dépôt avant migration).

## 1. Moteurs de décision concurrents (défaut le plus grave)

Six producteurs de verdicts coexistent, avec trois vocabulaires incompatibles :

| # | Moteur | Emplacement (avant migration) | Vocabulaire | Seuils propres |
|---|--------|------------------------------|-------------|----------------|
| A | `config.verdict()` | ancien package, config | BUY / WATCH / WAIT / AVOID | `min_score_buy=75` |
| B | `analysis.analyse()` | `vertex/engines/analysis.py:208` | recopie A dans `detail['verdict']` | délègue à A |
| C | `decision_stack.evaluate()` | `vertex/engines/decision_stack.py:66-263` | STRONG_BUY / BUY / BUY_PULLBACK / WATCH_BREAKOUT / WAIT / TOO_LATE / AVOID / NO_NEW_RISK / DATA_INSUFFICIENT | 80/66/56 |
| D | `committee._evaluate_one()` | ancien package, committee:82-114 | ACHETER / RENFORCER / ATTENDRE / ÉVITER | gate 62, ACHETER 74, RR_MIN 2.0 |
| E | `recommendation.position_decision()` | `vertex/engines/recommendation.py:94` | ADD/HOLD/WATCH/RAISE_STOP/TRIM/TAKE_PROFIT/EXIT | positions détenues |
| F | `options_lab._research()` | `vertex/engines/options_lab.py:149-157` | ACHETER / ATTENDRE / ÉVITER | quality≥62 & pop≥30 |

- `decision_stack` se déclare « vérité unique » mais **dépend en entrée** du
  verdict A (`decision_stack.py:68`), et le Command Center (`/api/command`)
  consomme le comité D, pas C.
- `recommendation._ALIAS` (`recommendation.py:36-53`) mappe 9 vocabulaires vers
  l'affichage : la divergence est masquée à l'UI, pas résolue.
- Verdict /40 supplémentaire : module « scorecard » (ancien nom trompeur
  évoquant le broker) — ACCEPTÉ / ACCEPTÉ SUR REPLI / ATTENTE / REFUSÉ.

**Correction prévue** : un `executive_engine` unique au-dessus de la
DecisionStack, seule couche autorisée à produire la décision finale
(ACHETER / RENFORCER / ATTENDRE / REDUIRE / REFUSER).

## 2. Constantes contradictoires

- **R:R** : 1.5 dans `decision_stack.py:126,209` ; 2.0 dans le comité
  (`RR_MIN=2.0`), `strategy_fit.py:125`, `evidence.py:109-112`. Un titre à
  R:R 1.7 est accepté sur une page, refusé sur une autre.
- **Delta options — contradiction interne** :
  - `config.OPTION_BUCKETS` cible des deltas 0.35–0.70 (bas) ;
  - `options.option_quality` récompense 0.70–0.88 (`qd=20`) ;
  - le scorecard /40 récompense 0.65–0.90 (`+2`) ;
  - le comparateur d'options du desk cite 0.45–0.70.
  → Le MÊME contrat reçoit une « suitability » et une « quality » avec des
  cibles opposées. (Défaut §6.2 confirmé.)
- **DTE** : `config` bucket long 150–400 ; ancienne stratégie 30–365 avec
  satellites courts ; options_lab LEAPS ≥300 ; swing ≥90. La nouvelle
  préférence 90–210 (60–270 absolu) n'existe nulle part. (Défaut §6.3 confirmé.)
- **Drawdowns** : `recommendation.py:123` code -25 en dur ; le -20 par titre
  n'est appliqué nulle part.
- **Grilles d'achat** : 4 grilles (75 / 80-66-56 / 62-74 / 72) sans constante partagée.

## 3. Provenance des données (défaut §6.1 confirmé)

- **yfinance** en direct : chaînes d'options + IV (ancien module options),
  fondamentaux (`tk.info`), profil entreprise (`vertex/data/company.py`),
  scan quotidien (avec repli Stooq). Données différées ~15 min non
  horodatées individuellement.
- **IBKR** : lecture seule partout (`readonly=True` : `ib_reader.py:53,63`,
  `terminal.py:683,1963,2063`). Adaptateur qui imite yfinance
  (`terminal.py:995`) et bascule `options.yf` (l.1012/1060) — le mélange de
  sources est **implicite**, non tracé valeur par valeur.
- **Aucun champ standard** {value, source, source_mode, timestamp,
  age_seconds, quality, fallback_used} : impossible de savoir si un prix
  affiché est IBKR live ou yfinance différé.
- **Greeks** : TROIS Black-Scholes maison concurrents (ancien module options
  `_greeks` ; `options_lab.py:30 _bs` ; `swing.py:30` approximation ATM),
  taux sans risque codé en dur et divergent (0.045 à deux endroits distincts),
  **jamais** les `modelGreeks` IBKR. Aucune étiquette
  BROKER_GREEKS / MODEL_ESTIMATE / FALLBACK_ESTIMATE. (Défauts §6.6, §6.8.)
- **Dividendes** : ignorés par tous les pricings. (Défaut §6.7.)
- **Démo** : `vertex/data/demo.py` génère OHLCV et board d'options
  synthétiques ; garde-fous corrects (`source:'demo-synthetic'`, badge UI),
  MAIS `options_lab._comparator` (l.636-672) mêle primes théoriques BS et
  vraies lignes de board dans la même vue, et `swing._annotate_swing` annote
  démo et réel sans distinction.

## 4. Scénarios options trop simplifiés (défaut §6.5 confirmé)

- `_viz` : payoff/cône/thêta sur LA seule échéance de la star (une horizon).
- `swing` : fenêtre unique 21 jours, mouvement 1.25σ.
- `_comparator` : horizons codés en dur 0.5 an / 1.2 an, indépendants du
  contrat réel.
- Aucun scénario d'IV (±10/±20 %), aucun scénario multi-temps
  (0/3/5/10/15/20/28 j), pas de valeur au stop / TP1 / TP2 / TP3.

## 5. CALLS et PUTS mélangés (défaut §6.4 confirmé)

- `recommendation.py:188-197` propose covered calls (delta 0.15–0.40,
  DTE 20–90) et protective puts (delta -0.45..-0.12, DTE 25–180) — stratégies
  de VENTE d'options ou de couverture, interdites par le nouveau profil
  (long CALL 90 %, PUT tactique rare, jamais de vente).
- La page stratégie documente Bull Call Spread, Protective Put, Covered
  Call, Bear Put Spread (`terminal.py:4546-4550`) — contenus pédagogiques à
  remplacer par le profil Vertex.
- Aucun moteur PUT isolé ; aucun lien régime→convergence de preuves.

## 6. Risque portefeuille (défaut §6.9 confirmé)

- `/api/command` : `portfolio_risk.build()` sur les candidats ACHETER/RENFORCER
  du scan (`command.py:102-106`), `/api/risk` sur le top 10 du scan
  (`analysis_api.py:44-51`). Les positions réelles (desk `desk_data.json`,
  `/api/ibkr/positions`) ne sont **jamais** injectées.
- Le « Risk Manager » affiché mesure donc un panier hypothétique. Correction :
  moteur de risque sur positions réelles ou simulées explicites.

## 7. Track record (défaut §6.10 confirmé)

- `track_record.record()` journalise le verdict A (BUY/WATCH…), pas la
  décision canonique ; `evaluate()` mesure des rendements de SIGNAL à
  +1/+5/+20 séances sur clôtures uniquement (`_hit_tp1` rate les mèches →
  biais optimiste).
- Aucune séparation signal / opportunité présentée / acceptée / position
  ouverte / clôturée.

## 8. Robustesse & dette

- **Exceptions avalées** : ~62 `except Exception` silencieux dans l'ancien
  package (16 dans le noyau quant), plus `persist.py:35,45`,
  `analysis.py:183-279`, `command.py:107,116`, `decision_api.py:109`,
  `live_engine.py:110,129`, `desk.py:48`. Un score sans « physique » est
  indiscernable d'un score complet.
- **Threading** : `scan_state` muté en place sans lock, lu par toutes les
  routes → lectures transitoirement incohérentes (rows d'un cycle, detail du
  précédent). Verrous existants localisés (persist, desk) seulement.
- **Le plus dangereux** : `best_for_symbol` enveloppe réseau+calcul dans un
  seul try/except → `return []` : un bug de parsing masque TOUS les contrats.
- **Routes sans test** : `/api/options-lab` (route Flask), `live_api.py`.
- **Monolithe** : `terminal.py` 10 429 lignes, 85 fonctions top-level,
  HTML/JS en chaînes ; import de l'ancien package dont 5 modules jamais
  utilisés (import surdimensionné) ; le module « vertex » de l'ancien package
  importé puis immédiatement masqué par le package `vertex/` (import mort).

## 9. Biais méthodologiques (validation)

- Pas de walk-forward systématique : le validateur PSR/DSR/PBO existe (bon
  point, réf. Bailey & López de Prado) mais n'est appliqué qu'à l'équité du
  backtest simple (poids 0.55 trend + 0.45 momentum re-calculés sur les mêmes
  ~120 séances → **risque de look-ahead** sur la sélection des poids).
- Survivorship : univers = constituants ACTUELS du S&P/Nasdaq — les
  disparus n'y sont pas (biais reconnu, à documenter dans la Research Factory).
- `_hit_tp1` sur clôtures → biais optimiste (stops intrajournaliers ignorés).
- Probabilités (POP, prob. ITM) lognormales affichées **sans calibration
  mesurée** (ni Brier, ni courbe de fiabilité). (→ §30 de la refonte.)

## 10. Sûreté d'exécution — CONFIRMÉE

- Recherche exhaustive `placeOrder | place_order | submitOrder | transmit |
  cancel_order | whatIf | MarketOrder | LimitOrder` : **zéro chemin
  d'exécution**. IBKR `readonly=True` partout, `READONLY=True`
  (`vertex/app/config.py:40`), `order_execution:'disabled-by-design'`,
  CI bloquante `tests/test_no_orders.py`.

## 11. Anomalies & scanner actuels — limites

- Détecteur actions : 10 anomalies statiques (volume spike, cassure 52s,
  divergences…), zéro anomalie de DONNÉES (stale/crossed/split), zéro anomalie
  d'OPTIONS (zero bid, parité put-call, IV outlier), zéro surface de vol.
- Sélection de contrat « star » : tri qualité puis POP puis OI — pas de
  catégories (BALANCED/DYNAMIC/ULTRA_CONVEX), pas de score contextuel, prime
  faible non pénalisée en soi.
- Pas de régimes de marché multidimensionnels (le contexte marché existe :
  régime SPY ADX + VIX + risk-on/off + breadth 45 leaders — base saine à
  étendre).

## 12. Occurrences de noms personnels (état initial)

55 occurrences (insensible casse) dans 39 fichiers : import du package legacy
(8 sites), salutation d'accueil en dur (`terminal.py:2572`), clé localStorage
de positions (`terminal.py:3213-3214`), profil utilisateur dans CLAUDE.md,
nom de dépôt personnel dans docs/AUDIT.md, références d'architecture dans
README/docs/CI. Traitées en Phase 2 (voir NAMESPACE_MIGRATION_AUDIT.md).

# VERTEX — Audit système complet & corrections

> Audit forensique du système et de la stratégie (3 sweeps parallèles :
> calculs, décision/stratégie, honnêteté des données/routes) suivi de
> corrections **réelles et testées**. Chaque correction est prouvée par un test.

## Méthode
Trois audits indépendants ont balayé le dépôt en parallèle :
1. **Calculs** (positions, options, indicateurs, portefeuille).
2. **Décision & stratégie** (cohérence des seuils, autorité unique).
3. **Honnêteté des données & routes** (données inventées, endpoints morts, LIVE abusif).

Le cœur numérique est jugé **sain** (pas de double ×100, pas d'erreur de signe
P&L, breakeven/annualisation corrects). Les défauts confirmés ci-dessous ont été
corrigés.

## Corrections appliquées (prouvées)

### Stratégie — seuil R:R unifié à 2,0 (contradiction critique)
La règle canonique est **R:R ≥ 2,0** (hard gate ExecutiveEngine). Trois moteurs
utilisaient encore **1,5**, produisant des verdicts contradictoires (un titre à
R:R 1,7 pouvait ressortir « Achat » dans DecisionStack puis être bloqué par
l'ExecutiveEngine).
- ✅ `engines/decision_stack.py:126` — gate d'achat `< 1.5` → `< 2.0`.
- ✅ `engines/decision_stack.py:209` — texte « ratio ≥ 1.5 » → « ≥ 2.0 ».
- ✅ `engines/evidence.py:111` — preuve négative sous `< 1.5` → `< 2.0` (fin de
  la zone 1,5–2,0 « silencieusement acceptable »).
- ✅ `scanner/stages.py:85` — pénalité `rr < 1.5` → `rr < 2` (même zone).
- Test : `tests/test_strategy_consistency.py` (R:R 1,7 n'est jamais un achat ;
  aucun seuil 1,5 résiduel dans les moteurs).

### Stratégie — stop de discipline action à −20 % (et non −25 %)
- ✅ `engines/recommendation.py:122` — la limite **portefeuille** (−25 %) était
  appliquée à une **action isolée**, contredisant le drawdown titre −20 % de la
  constitution. Corrigé : action −20 %, option −25 % (convexité).

### Honnêteté des données — badge « LIVE IBKR » abusif
- ✅ `terminal.py` (badge d'en-tête, 7 occurrences) — affichait « 🟢 LIVE IBKR »
  sur le simple flag de configuration `ibkr_enabled` (vrai par défaut), sans
  preuve de session. Corrigé : le badge n'affiche LIVE que sur une **donnée
  IBKR réelle** (`data_source==='ibkr'`) — sinon « 🟡 DIFFÉRÉ ». Règle de vérité.
- Test : `test_header_badge_never_claims_live_ibkr_from_config_flag`.

### Honnêteté des données — endpoint mort du morning brief
- ✅ `terminal.py` `mbLoad()` — interrogeait `/news` (redirection HTML → `r.json()`
  échoue → news vides silencieuses, toutes les 60 s). Repointé vers `/news-feed`
  (JSON réel, schéma `items` compatible).
- Test : `test_morning_brief_uses_live_news_endpoint`.

### Calculs — provenance & Greeks honnêtes (§21)
- ✅ `positions/recalculator.py` — les positions options live recevaient
  `greeks_source='BROKER_GREEKS'` **sans aucune valeur de Greek** (label de
  provenance faux). Corrigé : BROKER_GREEKS n'est réclamé que si delta/gamma/
  theta/vega réels sont présents ; sinon `UNAVAILABLE`.
- ✅ `positions/calculator.py:108` — `qty=None` produisait un Greek positionnel
  **0** au lieu de `None` (zéro fabriqué). Corrigé (valeur unitaire conservée).
- ✅ `portfolio/risk_engine.py` — l'agrégat Greeks faisait `g.get('delta') or 0`,
  transformant un Greek absent en 0 et **sous-estimant** l'exposition. Corrigé :
  somme des seules valeurs connues, `None` si aucune, drapeau `greeks_partial`.
- Tests : `tests/test_calc_honesty.py`.

## Points signalés, NON corrigés (honnêteté §2)
- **Autorité de décision multiple** : `decide.py`, `committee.py`, `scorecard.py`
  publient encore des verdicts d'achat en parallèle de l'ExecutiveEngine,
  réconciliés par la façade `recommendation.py` (`__VXVOCAB`). Router tout via
  l'ExecutiveEngine est un refactor lourd et risqué — **non entrepris** ici.
- **Committee `g_rr` contournable** : `committee.py:65` permet de passer le gate
  R:R via un breakout/uptrend. L'ExecutiveEngine reste l'autorité finale (2,0),
  mais le comité (avis consultatif) peut afficher un R:R sous-minimum. Non modifié.
- **vol_surface.py** : convention IV fraction vs pourcentage divergente du board
  (piège latent, non déclenché dans le flux actuel). Non modifié.
- **quant_engine.py** : `except: return 0` sur des sous-scores internes — un 0 de
  secours au lieu d'un None marqué. Non modifié (score interne, non affiché brut).

## Preuve
- **740 tests OK** (+6 sur la base 734), 0 échec.
- Navigateur Chromium : 6 pages clés (Briefing, Portefeuille, Risque, Analyse,
  Volatilité, Options) → **0 erreur console**.
- READONLY, zéro nom personnel, pas de modification de `main`.

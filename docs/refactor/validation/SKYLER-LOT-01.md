# SKYLER V2 — LOT 01 — CORRECTNESS OPTIONS

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-01-options-correctness`
> Base : `agent/skyler-v2-lot-00-baseline` (empilée sur `integration/vertex-skyler-v2`)
> SHA avant : lot-0 · SHA après : voir commit du lot
> Périmètre exclusif : mathématiques, unités, validation, garde-fous (aucune refonte page, aucun thème, aucun scoring global)

## 1. Constat

`vertex/engines/multileg_lab.py` (moteur multi-jambes servi par `/api/options/strategies/<sym>`
et `POST /api/options/analyze`) présentait quatre défauts de correctness :

1. **Perte illimitée masquée** (`multileg_lab.py:150-151` avant lot) : seule la borne
   *profit* était testée (`right_slope > 0`). Une exposition NETTE VENDEUSE de calls
   (short call nu, ratio 1×2) affichait un `max_loss` numérique issu de la grille finie
   (0 → 3× spot), avec le commentaire faux « perte : toujours bornée ». Un short call
   à 100 $ affichait ≈ −19 500 $ alors que la perte théorique est infinie.
2. **Heuristique d'unité d'IV silencieuse** (`> 1.5 → /100`) dans le cœur métier
   (`strategies_for_symbol`), interdite par OPTIONS_CORRECTNESS.md.
3. **Taux figé, dividende absent, modèle non traçable** : `r=0.045` sans provenance
   dans la sortie, aucun rendement de dividende.
4. **Entrées invalides non refusées** (spot négatif, strike ≤ 0, prime négative,
   NaN/inf, DTE négatif → calculs silencieusement faux) et **exécution ambiguë**
   (primes déclarées présentées sans avertissement de spread/slippage).

Le profil actif V1 (`vertex/strategy/profiles/vertex_strategy_v1.json`) interdit
`short_options` et `credit_spreads`, mais `rank_strategies` pouvait marquer
`recommended` un iron condor (jambes vendues, crédit).

## 2. Problème

Impact financier direct : un utilisateur voyait une perte max « bornée » sur une
structure à risque infini ; une stratégie interdite par sa propre constitution
pouvait être présentée comme recommandée ; une IV pourcentage atteignant le cœur
produisait PoP ≈ 100 % (absurde). Sévérité : élevée (décision financière faussée).

## 3. Périmètre

### Inclus
`vertex/engines/multileg_lab.py`, `vertex/options/iv_units.py` (nouveau),
`tests/test_options_correctness_lot1.py` (nouveau, 21 tests).

### Hors périmètre
Refonte de page, thème, nouvelles sources marché, Constitution V2 (lot 2),
séparation TACTICAL/SWING/LEAPS des scanners (lot 6), probabilité de doublement (lot 6).

## 4. Décision

Corriger au point de jonction le plus étroit, comportements existants préservés :

- pente terminale nette calls+actions → `max_loss_unbounded` ; le flag **prime** sur
  la grille (`max_loss: null` si illimité) — convention identique à `max_profit` ;
- frontière de normalisation IV typée `vertex/options/iv_units.py` :
  `normalize_iv(value, unit)` (PERCENT/DECIMAL, ValueError si unité inconnue) +
  `from_legacy_board(value)` — UNIQUE porte tolérée pour le board au contrat mixte
  (producteurs réels en %, fixtures en décimal), détection ÉTIQUETÉE (unité détectée +
  avertissement propagés dans la réponse API) ; le cœur refuse toute IV > 300 % ;
- `analyze_strategy(..., r=0.045, q=0.0)` : taux ET dividende configurables, formules
  Black-Scholes avec facteur `e^{-qT}` (q=0 → résultats bit-à-bit identiques), bloc
  `model` traçable dans chaque sortie (type/r/q/iv_unit/premium_basis) ;
- refus structurés `refusals: [{field, value, why}]` (spot, strike, premium, qty,
  days_to_exp, iv — NaN/inf compris), textes historiques conservés ;
- bloc `execution` : `spread_slippage_included` explicite ; si bid/ask fournis sur
  toutes les jambes option → `net_premium_adverse` (achat à l'ask, vente au bid) ;
- filtrage par le PROFIL ACTIF : `_options_mandate()` lit la constitution V1 ;
  jambe vendue / crédit / perte illimitée → `hors_mandat: true` + `mandate_reasons`,
  JAMAIS `recommended` (le labo reste consultable — conforme « laboratoire uniquement ») ;
  mandat DTE signalé au niveau résultat (`mandate.dte_ok`, bornes, note honnête).

Alternative rejetée : normaliser l'unité d'IV chez le producteur du board (contrat
mixte réel %/décimal) — trop large pour ce lot, prévu avec la série OHLCV canonique.

## 5. Fichiers modifiés

| Fichier | Rôle | Modification | Risque |
|---|---|---|---|
| `vertex/options/iv_units.py` | frontière d'unités IV | nouveau (typée + legacy étiquetée) | faible |
| `vertex/engines/multileg_lab.py` | moteur multi-jambes | validation, max_loss_unbounded, q, model, execution, mandat | moyen |
| `tests/test_options_correctness_lot1.py` | preuves | nouveau — 21 tests (rouges d'abord) | faible |

Contrats et unités : IV décimale dans le cœur (0.404 = 40,4 %) ; prime PAR ACTION ;
multiplicateur 100 explicite ; r/q annuels continus ; montants en dollars ; sorties
`iv_unit`/`iv_detected_from`/`model`/`execution` nouvelles, aucune clé existante retirée.

Compatibilité : API additive (les clés existantes gardent leur sémantique ; seul
`max_loss` devient `null` pour les expositions nettes vendeuses de calls — cas
qu'AUCUNE surface UI ne produit aujourd'hui : les 7 presets du labo sont bornés et
le POST reçoit les positions longues du desk ; l'UI est de plus null-safe
`Math.abs(s.max_loss || 0)`). Démo/sans IBKR inchangés.

## 6. Tests rouges avant correction

```text
python -m pytest tests/test_options_correctness_lot1.py -q
16 failed, 5 passed          # 5 verts = module iv_units surface + comportement historique conservé
```

Échecs prouvant chaque défaut : `test_naked_short_call_loss_unbounded` (KeyError
`max_loss_unbounded`), `test_core_refuses_percent_iv` (PoP calculée sur IV=30),
`test_refusal_negative_spot_structured` (pas de `refusals`), `test_model_provenance_traced`,
`test_dividend_yield_lowers_call_delta` (paramètre `q` inexistant),
`test_execution_adverse_fill_with_bid_ask`, `test_short_leg_strategies_hors_mandat_never_recommended`, etc.

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex                    → exit 0
python -m pytest tests/test_options_correctness_lot1.py \
       tests/test_multileg_lab.py tests/test_multileg_iv_units_06.py \
       tests/test_options_lab.py -q                           → 51 passed
python -m pytest tests/ -q                                    → 1175 passed, 2 skipped
python -m pytest tests/test_no_orders.py -q                   → inclus (3 passed dans la suite)
```

Cas manuels vérifiés dans les tests : short call nu (crédit 500 $ = gain max, perte
illimitée), ratio 1×2, covered call (−9 800 $ à cours 0, borné), short put (−9 500 $),
delta = N(d1) exact calculé indépendamment, rempli défavorable 370 $ vs 300 $ déclaré.

## 8. Validation manuelle et navigateur

Serveur `DEMO=1 NO_IBKR=1` :

- `GET /api/options/strategies/GOOGL` → `iv: 0.468`, `iv_unit: DECIMAL`,
  `iv_detected_from: PERCENT` + avertissement de frontière dans `warnings`,
  `mandate.profile_version: 1`, `mandate.dte_ok: false` (échéance labo hors bornes
  60–270 signalée honnêtement), recommandée = jambes longues uniquement ;
- navigateur Chromium réel : `/options`, `/options?view=structure`,
  `/options?view=positioning`, `/analysis/GOOGL` → rendu normal, **0 erreur console** ;
- `/api/client-log` → 0.

Pas de changement de shell visible → pas de bump service worker.

## 9. Invariants vérifiés

- [x] READONLY — aucun chemin d'ordre (gardien `test_no_order_paths_in_module` vert) ;
- [x] aucune donnée inventée — refus structurés, primes jamais devinées ;
- [x] unités explicites (IV typée, prime/action, multiplicateur 100, r/q tracés) ;
- [x] flag illimité PRIME sur toute valeur de grille finie ;
- [x] stratégie interdite par le profil actif jamais `recommended` ;
- [x] démo/sans IBKR inchangés ; aucun secret ni fichier runtime dans le diff.

## 10. Comparaison avant/après

| Mesure | Avant | Après |
|---|---|---|
| Short call nu → `max_loss` | ≈ −19 500 $ (faux, grille) | `null` + `max_loss_unbounded: true` |
| IV « 30 » atteignant le cœur | PoP ≈ 100 % (absurde) | refus structuré champ `iv` |
| Iron condor (profil V1) | pouvait être `recommended` | `hors_mandat` + jamais recommandé |
| Provenance modèle | absente | bloc `model` (r/q/unités/base de prime) |
| Suite de tests | 1154 | **1175 passed / 2 skipped** |

## 11. Risques et limites restants

1. Le labo sélectionne toujours l'échéance ~35 DTE (signalée hors mandat) — la
   séparation TACTICAL/SWING/LEAPS est le périmètre du **lot 6**.
2. La frontière legacy `from_legacy_board` reste une détection (étiquetée) tant que
   le producteur du board n'est pas normalisé (**lot 4/6**).
3. Les moteurs mono-jambe (`options_lab.py`, `legacy_engine.py`) gardent leurs
   conversions `/100` locales cohérentes avec leur contrat — à migrer vers
   `iv_units` au **lot 6**.
4. Probabilité de doublement (≠ PoP) non implémentée — **lot 6**.

## 12. Rollback

`git revert` du commit du lot. Aucune donnée persistée affectée.

## 13. Verdict

**GO** — défauts reproduits par tests rouges, corrigés au point le plus étroit,
1175 tests verts, preuve runtime + navigateur, aucune régression.

## 14. Prochaine étape autorisée

`/vertex-skyler-v2 lot-2` (Constitution stratégique V2).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**

# SKYLER V2 — LOT 0 — BASELINE

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-00-baseline` (issue de `agent/skyler-v2-audit-convergence`, elle-même issue de `integration/vertex-skyler-v2`)
> SHA avant : `b696e12` (audit) · base runtime : Neon Glass `a802155`
> Périmètre : mesure de l'état exact + récupération de l'actif RC1 (§7.1 de l'audit). **Aucun moteur ni calcul modifié.**

## 1. Constat — mesures exactes de la base

| Mesure | Valeur | Commande |
|---|---:|---|
| Fichiers Python suivis | 393 | `git ls-files '*.py'` |
| Fichiers JavaScript suivis | 32 | `git ls-files '*.js'` |
| `terminal.py` | 10 738 lignes | `wc -l` |
| Moteurs (`vertex/engines/`) | 27 modules | hors `__init__` |
| Modules options (`vertex/options/`) | 24 modules | hors `__init__` |
| Builders graphiques (`js/charts/`) | 21 fichiers | `ls` |
| Fichiers de routes (`vertex/app/routes/`) | 20 | hors `__init__` |
| Endpoints déclarés (`@bp.route`/`@app.route`) | 174 | `grep -rhoE` |
| Fichiers de tests | 104 (105 avec le gardien récupéré) | `ls tests/test_*.py` |
| Service worker | `td-shell-v87` | `vertex/app/routes/system.py` |
| READONLY | `True` (`vertex/app/config.py:40`) + `readonly=True` services | grep |

## 2. Validations exécutées (résultats exacts)

```text
python -m compileall -q terminal.py vertex        → exit 0
python -m pytest tests/ -q                        → 1150 passed, 2 skipped (avant lot)
python -m pytest tests/test_no_orders.py -q       → 3 passed
python -m pytest tests/ -q                        → 1154 passed, 2 skipped (après récupération RC1)
```

Serveur `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1` :

- `/healthz` → 200, `status:ok`, source `demo`, 20 titres scannés, `scan_error:null` ;
- `/readyz` → 200, `ready:true`, 4 checks verts dont `readonly: lecture seule effective` ;
- `/api/client-log` → `{"count":0}` (0 erreur JS applicative).

Tour navigateur Playwright (Chromium réel) — **22 routes / 8 espaces, 0 erreur console** :
briefing, markets (+breadth), opps (+stocks/cal/opt), analysis, portfolio (+pos/perf/risk),
options (+leaps/pos/struct), journal, system (+data/auto), intelligence, performance.
Débordement horizontal **page** : 0 px à 1440 et à 390 (les compteurs « ovf » du tour sont
des scrollers internes voulus — tables/rails). Captures : `docs/skyler/baseline/*.png`
(briefing 1440 + 390, portfolio 1440, options-positionnement 1440).

## 3. Récupération de l'actif RC1 (seul changement de ce lot)

Conformément au §7.1 de `BRANCH_CONVERGENCE_AUDIT.md` (validation utilisateur : « continue,
on corrigera étape par étape ») :

| Fichier | Action | Nature |
|---|---|---|
| `docs/release/RC1_HUMAN_ACCEPTANCE.md` | restauré tel quel depuis `28d1e4e` | doc historique |
| `docs/release/RC1_CHECKLIST.md` | remis à son état final RC1 (v51/954 tests — record historique) | doc historique |
| `tests/test_sw_cache_safety_rc1.py` | réintroduit **adapté** : assertion de version dynamique (1 seule constante `td-shell-vN`, N ≥ 51 — jamais de régression sous la RC1) ; invariants structurels inchangés (précache = manifest+icône seulement, network-first, purge des vieux caches, aucun graphe supprimé référencé) | test gardien |

Le cherry-pick brut de `28d1e4e` a été refusé (il aurait rétrogradé le SW v87 → v51).
Résultat : 4 tests récupérés passent ; suite complète **1154 passed / 2 skipped**.

## 4. Invariants vérifiés

- [x] READONLY intact (`/readyz` le prouve en runtime ; `test_no_orders` 3/3).
- [x] Aucun moteur, calcul, endpoint ou visuel modifié (diff = 2 docs + 1 test + captures).
- [x] Aucun secret ni fichier runtime dans le diff.
- [x] Aucune donnée inventée ; mode démo étiqueté par le serveur.
- [x] Service worker non modifié (aucun bump nécessaire — pas de changement de shell).

## 5. Risques et limites restants (hérités, pour les lots suivants)

1. Pertes théoriquement illimitées des expositions nettes vendeuses de calls non flaguées (`max_loss_unbounded` absent) — **lot 1**.
2. Unités d'IV aux frontières (heuristique %/décimal) — **lot 1**.
3. Profil stratégique V1 non aligné mandat LEAPS (180–540 DTE, delta 0,70–0,90) — **lot 2**.
4. OHLCV artificiel possible dans certains chemins d'anomalies — **lot 4**.
5. Dette `terminal.py` (10 738 lignes) et endpoints legacy — hors périmètre Skyler immédiat.

## 6. Rollback

`git revert` du commit de ce lot ; aucune donnée runtime affectée. Les fichiers restaurés
sont additifs (leur suppression ramène à l'état Neon exact).

## 7. Verdict

**GO** — baseline mesurée, prouvée en runtime et en navigateur ; seul l'actif RC1 récupéré
s'ajoute, sans toucher au runtime.

## 8. Prochaine étape autorisée

`/vertex-skyler-v2 lot-1` (correctness options).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**

# SKYLER V2 — AUDIT DE CONVERGENCE DES BRANCHES

> Date : 2026-08-04
> Branche de travail : `agent/skyler-v2-audit-convergence` (issue de `integration/vertex-skyler-v2`)
> Lot : `AUDIT` (`/vertex-skyler-v2 audit`)
> Périmètre : **lecture seule** — aucun moteur, calcul, endpoint ou visuel modifié.
> Commandes utilisées : `git rev-parse`, `git merge-base`, `git rev-list --left-right --count`,
> `git log --oneline A..B`, `git diff --stat|--name-status A...B`, `git ls-tree`.

---

## 1. Constat — état exact des branches auditées

| Branche | SHA | Dernier commit | SW shell | Fichiers tests | Moteurs (`vertex/engines`) | Options (`vertex/options`) |
|---|---|---|---|---:|---:|---:|
| `main` | `2b4fa70` | 2026-07-15 · greeks vanna/vomma | `td-shell-v42` | 75 | 22 | 20 |
| `agent/vertex-total-rebuild` (RC1) | `28d1e4e` | 2026-07-24 · SW v51 + dossier d'acceptation | `td-shell-v51` | 83 | 22 | 20 |
| `agent/vertex-neon-glass-graphs` (Neon Glass) | `a802155` | 2026-08-04 · scanner d'anomalies | `td-shell-v87` | 105 | 28 | 25 |
| `integration/vertex-skyler-v2` | `5b5e0b3` | 2026-08-04 · gouvernance Skyler (docs) | `td-shell-v87` | 105 | 28 | 25 |

Branches V4/Prism (références historiques, gouvernance §3.8) :

| Branche | Position vs `main` | Dernier commit |
|---|---|---|
| `claude/v4-01-foundations` … `claude/v4-qa-conformance` (7 branches) | histoire massivement divergente (494 commits de `main` absents ; 54–58 commits propres) | 2026-07-22 |
| `integration/vertex-v4-clean` | idem (494 absents / 67 propres) | 2026-07-23 |
| `redesign/vertex-v4-master` | `main` + 5 commits | 2026-07-22 |

Ces branches ne partagent pas une base saine avec `main` (racine ancienne/orpheline). Elles
sont **gelées comme références** et ne doivent jamais servir de base de développement.
Aucune suppression n'est proposée ici (action destructive → accord humain requis).

## 2. Topologie réelle (ancêtres communs)

```text
main (2b4fa70) ────────────────────────────────► [canonique, figée 15-07]
   └─► agent/vertex-total-rebuild : +37 commits
            │
            ├─ 84fbdc5 (24-07, dossier RC1) = point de bifurcation
            │      └─► 28d1e4e : +1 commit propre à RC1 (SW v51 + acceptation)  ⚠ absent de Neon
            │
            └─► agent/vertex-neon-glass-graphs : +56 commits depuis 84fbdc5
                     └─► integration/vertex-skyler-v2 : +9 commits (docs/skill uniquement)
```

Vérifications :

- `merge-base main ↔ rebuild` = `merge-base main ↔ neon` = `2b4fa70` → **les deux branches
  contiennent 100 % de `main`** (0 commit de `main` absent de l'une ou l'autre).
- `merge-base rebuild ↔ neon` = `84fbdc5` → **Neon Glass est une continuation directe de la RC1**
  (bifurcation au dernier commit de doc RC1, avant le bump SW v51).
- `merge-base neon ↔ skyler-v2` = `a802155` (= tip Neon) → **`integration/vertex-skyler-v2`
  est un fast-forward de Neon Glass + 9 commits de gouvernance ; diff strictement limité à
  `.claude/skills/vertex-skyler-v2/*`, `docs/skyler/STATUS.md` et `CLAUDE.md` (section Skyler).
  Aucun fichier runtime touché.**

## 3. Inventaire des commits uniques

### 3.1 RC1 → 1 commit absent de Neon Glass (risque n°2 du STATUS — CONFIRMÉ)

`28d1e4e` — `fix(rc1-sw): bump service worker v50 -> v51 (purge cache runtime pré-suppression) + dossier d'acceptation humaine`

| Fichier | Nature | Présent dans Neon/skyler-v2 ? |
|---|---|---|
| `docs/archives/release/RC1_HUMAN_ACCEPTANCE.md` (+143 l.) | dossier d'acceptation humaine RC1 | **NON — perdu** |
| `tests/test_sw_cache_safety_rc1.py` (+55 l.) | gardien de sécurité du cache SW | **NON — perdu** |
| `vertex/app/routes/system.py` (v50→v51) | bump SW | **Superseded** (Neon est à v87, lignée propre) |
| `tests/test_redesign_ui.py`, `tests/test_ui_v3.py`, `tests/test_production_guards_canonical.py` | gardiens alignés v51 | **Superseded** (alignés v87 côté Neon) |
| `docs/archives/release/RC1_CHECKLIST.md` (8 l.) | mise à jour checklist | **NON** (Neon garde la version pré-v51) |

Conclusion : la seule vraie perte fonctionnelle est **le test gardien
`test_sw_cache_safety_rc1.py` et le dossier d'acceptation** ; les bumps de version sont
obsolètes (v87 > v51 sur la même lignée de service worker).

### 3.2 Neon Glass → 56 commits absents de RC1 (par thème)

1. **Identité visuelle Neon Glass** (11 c.) : Graph System V2, refonte Marchés/Opportunités,
   identité bleu→verre blanc/gris neutre, thème sombre, zéro orange.
2. **Widget Lab** (7 c.) : `/widget-lab`, 60+ widgets, curation 15 officiels, galerie musée.
3. **Reconstruction pages** (2 c.) : Aujourd'hui avec widgets validés (Regime Aura, Catalyst Runway).
4. **CONTINUITY** (13 c.) : shell persistant, store global, cache client persistant,
   stale-while-revalidate, VX.prices, VX.freshness, mode offline, observabilité, session atomique.
5. **Session 30 min** (3 c.) : cadence 1800 s, cache de session figé, fix cache froid.
6. **Positions** (1 c.) : gérer/modifier/clôturer/supprimer une position (localStorage, jamais d'ordre).
7. **OPTIONS-IA / dealer positioning** (6 c.) : moteur GEX, flow, synthèse-thèse, vue
   Positionnement, Vanna/Charm, max pain + skew IV, pin-risk, radar multi-titres.
8. **Assistant** (5 c.) : copilote Claude, post-mortem journal, surveillance gamma,
   stress-scénarios portefeuille, GEX quotidien.
9. **Pré-trade + anomalies** (2 c.) : ticket pré-trade 7 vérifications, scanner d'anomalies.
10. **Durcissement** (6 c.) : audit-fix JS/Python/sécurité, verifier_vertex, tour complet.

### 3.3 `integration/vertex-skyler-v2` → 9 commits (gouvernance documentaire pure)

`5c592f3`→`5b5e0b3` : skill maître, architecture, constitution trading V2, contrat options,
runbook, checklist, template de rapport, STATUS initial, routage `CLAUDE.md`.
**Aucun changement runtime** — vérifié par `git diff --name-status` (9 fichiers, tous docs/skill).

## 4. Divergences par domaine (RC1 `28d1e4e` ↔ Neon `a802155`)

Total : **137 fichiers, +14 148 / −633** (côté Neon depuis la bifurcation).

### 4.1 Moteurs — 11 nouveaux, 0 conflit

Tous **ajoutés** côté Neon (aucun moteur existant de RC1 modifié de façon concurrente) :
`engines/anomaly.py`, `engines/portfolio_stress.py`, `engines/postmortem.py`,
`engines/pretrade.py`, `engines/session_digest.py`, `engines/session_snapshot.py`,
`options/gex.py`, `options/gex_history.py`, `options/gex_scan.py`, `options/flow.py`,
`options/dealer_synthesis.py`.

### 4.2 Pages & routes — modifications unilatérales (côté Neon uniquement)

Toutes les pages (`vertex/ui/pages/*` : briefing, markets, opportunities, analysis,
portfolio, options_intel, performance, system, + `widget_lab` nouveau), le shell, et
8 routes (`analysis_api`, `options_intel_api`, `positions_api`, `desk`, `ai_api`,
`redesign`, `system`, + `session_api` nouveau) ont évolué côté Neon. RC1 n'a modifié que
`system.py` (bump v51) → **un seul fichier en intersection : `vertex/app/routes/system.py`**.

### 4.3 Tests — 30 fichiers divergents

- Côté Neon : +22 nouveaux (gex, flow, dealer_synthesis, gex_scan, gex_history, copilot,
  postmortem, gamma_surveillance, portfolio_stress, pretrade, anomaly_engine, continuity×7,
  session_digest, widget_lab, neon_glass, reconstruction_today, launch_readiness,
  options_flow) + 8 gardiens modifiés.
- Côté RC1 : +1 nouveau (`test_sw_cache_safety_rc1.py`) + 3 gardiens alignés v51.
- Intersection conflictuelle : les 3 gardiens de version SW (`test_redesign_ui`,
  `test_ui_v3`, `test_production_guards_canonical`) — résolue de fait par v87.

### 4.4 Constitution / profil stratégique

`main`, RC1 et Neon partagent le même profil V1 (`vertex/strategy/`) — non modifié par
Neon. La Constitution V2 (S+/S/A/B, LEAPS 180–540 DTE, delta 0,70–0,90) **n'existe encore
dans aucune branche de code** ; elle n'existe que comme référence du skill (lot-2).

## 5. Risques de conflit et risques de perte

| # | Risque | Sévérité | État |
|---|---|---|---|
| 1 | Divergence RC1 ↔ Neon | — | **Résolue par la topologie** : Neon est un fast-forward de RC1 sauf 1 commit ; pas de fusion croisée nécessaire. |
| 2 | Commit RC1 `28d1e4e` absent de Neon | Moyenne | **Confirmé.** Perte réelle : `test_sw_cache_safety_rc1.py` + `RC1_HUMAN_ACCEPTANCE.md` + 8 l. de checklist. Récupérable proprement (cherry-pick partiel adapté v87) — voir plan §7. |
| 3 | Conflit `system.py` (v51 vs v87) si cherry-pick brut de `28d1e4e` | Faible | Ne PAS cherry-pick le bump : reprendre uniquement doc + test, en adaptant l'assertion de version à la lignée v87+. |
| 4 | Branches V4/Prism reprises par erreur comme base | Élevée si violée | Gouvernance §3.8 : références gelées. Racine incompatible (494 commits de `main` absents) — toute fusion serait destructrice. |
| 5 | `main` divergerait pendant les lots | Faible | `main` figée au 15-07 et 100 % contenue dans Neon ; aucun commit unique côté `main`. À re-vérifier au préflight de chaque lot (`git fetch --prune`). |
| 6 | Risques de calcul hérités (short call illimité, unités IV, OHLCV artificiel, profil V1 ≠ mandat LEAPS) | Élevée (financière) | **Hors périmètre de cet audit** (aucun changement runtime autorisé). Présents à l'identique dans les 3 branches de code → à traiter aux lots 1, 2 et 4 selon le runbook, tests rouges d'abord. |

## 6. Décision — source canonique par domaine

| Domaine | Source canonique | Justification |
|---|---|---|
| Moteurs déterministes (`vertex/engines`, `vertex/options`) | **Neon Glass** (`a802155`) | Sur-ensemble strict de RC1 et `main` ; 11 moteurs de plus, 1150 tests verts. |
| Pages & UI (8 espaces, widget-lab) | **Neon Glass** | Seule lignée portant Neon Glass + CONTINUITY + session 30 min. |
| Routes & API | **Neon Glass** | Sur-ensemble strict (aucune route RC1 perdue). |
| Service worker & gardiens de version | **Neon Glass** (v87) | v51 de RC1 est un ancêtre logique dépassé sur la même lignée. |
| Tests | **Neon Glass** + récupération de `test_sw_cache_safety_rc1.py` (adapté) | Seul actif RC1 non couvert. |
| Dossier release RC1 (`docs/archives/release/*`) | **RC1** pour `RC1_HUMAN_ACCEPTANCE.md` + delta checklist | Documents d'acceptation humaine à préserver dans l'historique produit. |
| Gouvernance Skyler (`.claude/skills`, `docs/skyler`) | **`integration/vertex-skyler-v2`** | Seule branche porteuse ; docs-only vérifié. |
| `main` | Version canonique de release — **ne bouge pas** sans accord humain explicite | CLAUDE.md + gouvernance §3.1–3.2. |
| Branches V4/Prism | Références historiques gelées | Racine divergente ; jamais une base. |

**Recommandation de branche canonique de développement : `integration/vertex-skyler-v2`**
(= Neon Glass `a802155` + gouvernance), base fonctionnelle `agent/vertex-neon-glass-graphs`,
conformément au skill. Aucune fusion vers `main` proposée.

## 7. Plan de récupération (aucune fusion automatique — validation humaine requise avant exécution)

1. **Récupérer l'actif RC1 perdu** (petite PR dédiée, au plus tôt en lot-0) :
   - reprendre `docs/archives/release/RC1_HUMAN_ACCEPTANCE.md` et le delta `RC1_CHECKLIST.md`
     depuis `28d1e4e` (copie de fichiers, pas de cherry-pick du bump SW) ;
   - réintroduire `tests/test_sw_cache_safety_rc1.py` en adaptant l'assertion de version
     à la lignée courante (v87+), et vérifier qu'il passe.
2. **Ne rien fusionner** entre RC1 et Neon : la topologie rend toute fusion inutile ;
   RC1 reste consultable en l'état.
3. **Ne pas toucher** aux branches V4/Prism ni à `main` (suppression = action destructive
   → interdite sans preuve d'inutilisation et accord explicite).
4. Continuer tous les lots depuis `integration/vertex-skyler-v2` via des branches
   `agent/skyler-v2-lot-XX-…`, PR brouillon vers l'intégration, un lot par invocation.

## 8. Invariants vérifiés pendant l'audit

- [x] Aucun moteur, calcul, endpoint ou visuel modifié (diff du lot = 2 fichiers docs).
- [x] Aucun fichier runtime/secret touché.
- [x] Branche ≠ `main` ; branche de travail issue de `integration/vertex-skyler-v2`.
- [x] Aucune fusion, aucun push forcé, aucune suppression de branche.
- [x] READONLY intact (aucun fichier de code touché).

## 9. Verdict

**GO** — la convergence est plus simple que redouté : Neon Glass est une continuation
directe de la RC1 (pas une branche sœur), `main` est entièrement contenue, et
`integration/vertex-skyler-v2` est un fast-forward documentaire de Neon Glass.
Un seul actif à récupérer (test gardien SW + dossier d'acceptation RC1), sans conflit.

## 10. Prochaine étape autorisée

Une seule : `/vertex-skyler-v2 lot-0` (baseline), après validation humaine de cet audit —
en y intégrant la récupération de l'actif RC1 décrite au §7.1 si l'humain la valide.

**Arrêt après ce lot — validation humaine requise.**

# SKYLER V2 — LOT 50 : profilage des routes chaudes (mesurer avant d'optimiser)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-50-profiling`
(base : `integration/vertex-skyler-v2` @ `d6ce3ec`, fraîchement fetchée) ·
Mode : développement, axe OPTIMISATION (demande utilisateur) — ZÉRO
changement produit dans ce lot, mesures publiées.

## 1. Objectif et méthode

L'utilisateur a demandé « d'autres choses à faire pour optimiser ? » —
règle appliquée : MESURER d'abord, corriger ensuite, jamais l'inverse.
Outil versionné `tools/profile_hot_routes.py` (reproductible) :

- p50/p95/max (`time.perf_counter`, N=20 requêtes après 2 de chauffe)
  sur 5 routes chaudes + les 8 pages HTML, serveur DEMO=1 NO_IBKR=1 ;
- micro-bench in-process des étages du cœur décisionnel (fixtures FIXES,
  moyenne sur 200 appels) pour vérifier l'hypothèse « double
  build_packet + score40 recalculé dans /api/skyler/<sym> ».

## 2. Mesures (serveur démo local)

| Cible | p50 ms | p95 ms | max ms | Verdict |
|---|---|---|---|---|
| `/api/skyler/AAPL` (cœur) | 13.8 | 14.4 | 14.5 | RAS |
| `/api/skyler/memory` | 1.5 | 1.7 | 1.7 | RAS |
| `/api/skyler/memory/export` | 1.6 | 1.8 | 1.8 | RAS |
| `/api/command` | 2.4 | 2.8 | 2.9 | RAS |
| `/api/market/summary` | 1.4 | 1.7 | 2.4 | RAS |
| 8 pages HTML (`/` … `/system`) | 1.1–1.5 | 1.3–1.7 | ≤ 5.1 | RAS |

**Toutes les cibles sont sous 15 ms p95** — très loin du seuil de
100 ms fixé d'avance comme « RAS dit ».

## 3. Hypothèse du double calcul — VÉRIFIÉE puis relativisée

Micro-bench des étages (fixtures fixes, moyenne sur 200 appels) :

| Étage | ms/appel |
|---|---|
| `build_packet` | 0.327 |
| `score40` | 0.340 |
| `red_team.review` | 0.368 |
| `decide` (complet, perturbations incluses) | 9.018 |
| **Surcoût du double connu** (build_packet + score40 dupliqués) | **0.667** |
| Part du surcoût dans `decide` | **7.4 %** |

L'hypothèse est CONFIRMÉE factuellement (le double calcul existe et
coûte ~0.7 ms) mais RELATIVISÉE : le gros de `decide` est l'analyse de
perturbation (11 recalculs par CONSTRUCTION — c'est la robustesse
mesurée du lot 21, pas du gaspillage), et la route entière répond en
~14 ms. Supprimer le doublon gagnerait ~1 ms sur 14 (~5-7 %) —
**imperceptible pour l'utilisateur**.

## 4. Décision documentée pour le lot 51 : **NO-GO**

Critère fixé d'avance : GO seulement si gain attendu MESURABLE. À ~1 ms
de gain sur une route à 14 ms, le rapport bénéfice/risque est défavorable
(toucher le cœur décisionnel pour un gain invisible). **NO-GO dit.**
L'axe optimisation est épuisé en valeur réelle : les performances sont
excellentes partout. Si un jour la latence réelle dégrade (TWS réel,
watchlist plus large), ce rapport et l'outil versionné donnent la
baseline chiffrée pour re-mesurer avant d'agir.

## 5. Preuves complémentaires

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1627 passed, 2 skipped (inchangé — outil
                                                     de mesure seulement)
```

Moteur 0.9.0 et SW v107 inchangés ; aucune écriture produit (l'outil
lit et mesure). Un correctif d'outil pendant le lot : sys.path depuis
tools/ pour le micro-bench (dit).

## 6. Suite

Retour aux RC périodiques espacées (~30 min) — chaque RC re-prouvant
suite complète + 8 pages + parcours mémoire + cycle souverain. La
validation humaine physique reste l'étape décisive.

**Arrêt après ce lot — validation humaine requise.**

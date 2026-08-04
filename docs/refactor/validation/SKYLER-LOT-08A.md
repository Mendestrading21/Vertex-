# SKYLER V2 — LOT 08a — NEON GLASS · ANALYSE (carte décision Skyler)

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-08a-analysis-skyler`
> Base : `agent/skyler-v2-lot-07-portfolio-intelligence`
> Périmètre : UNE page (Analyse), une carte — aucun moteur ni calcul modifié
> (discipline lot 8 : une sous-PR par espace validé)

## 1. Constat

Les 8 espaces ont déjà leur expérience Neon Glass (campagne pré-Skyler). Ce qui
manque au lot 8 : EXPOSER les nouvelles sorties Skyler. `/api/skyler/<sym>`
(décision canonique, score /40, hard gates, scénarios) n'était visible nulle part.

## 2. Décision

Carte « **Skyler — décision canonique** » sur la fiche Analyse, sous le scanner
d'anomalies :

- badge décision (ton sémantique) + **total /40** + niveau + `plafonnée par <gate>` ;
- 8 puces de blocs (points/max, `basis` complet au survol, INSUFFISANT grisé) ;
- portes déclenchées listées en rouge (id + raison) ; portes non évaluables comptées ;
- scénarios pessimiste/probable/exceptionnel : cible + rendement exact +
  « **probabilité : non calibrée** » (jamais un chiffre inventé) ;
- pied : catalyseur daté, invalidation (stop réel), risque max %, objection la
  plus forte.

Chargement `loadSkyler()` via `VX.fetch` (TTL 120 s, cache session),
`VX.refresh.register(...,300000)`. États honnêtes : indisponible / injoignable.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/ui/pages/analysis_page.py` | +1 carte HTML + `loadSkyler()` (additif) | faible |
| `vertex/app/routes/system.py` | SW `td-shell-v87` → **v88** (shell visible modifié) | faible |
| `tests/test_redesign_ui.py`, `test_ui_v3.py`, `test_production_guards_canonical.py`, `test_reconstruction_today.py` | gardiens alignés v88 (v87 absent) | nul |
| `tests/test_skyler_core.py` | + gardien `an-skyler`/`loadSkyler` dans la page | faible |
| `docs/skyler/baseline/lot08a_skyler_card_1440.png` | capture | nul |

## 4. Tests

```text
python -m compileall -q terminal.py vertex → exit 0
gardiens affectés (6 fichiers) → 128 passed
suite complète → 1266 passed, 2 skipped
```

## 5. Validation navigateur (DEMO=1 NO_IBKR=1, Chromium réel)

| Vue | Taille | Résultat |
|---|---:|---|
| /analysis/GOOGL | 1440×900 | carte rendue : `REFUSER · 18/40 · REFUS_WATCH`, 8 blocs (Asymétrie 6/6, Données 4/4, Fondamentaux 0/5 grisé…), scénarios avec « probabilité : non calibrée », 0 débordement page |
| /analysis/GOOGL | 390×844 | même contenu, 0 débordement page |

Console : **0 erreur** (les deux tailles). `/api/client-log` = 0. `sw.js` sert
bien `td-shell-v88`. Capture : `docs/skyler/baseline/lot08a_skyler_card_1440.png`.

## 6. Invariants vérifiés

- [x] une page = une mission ; réponse d'abord (badge + /40), preuve ensuite (blocs), expertise au survol (`basis`) ;
- [x] aucun chiffre inventé à l'écran (probabilités « non calibrée » affichées telles quelles) ;
- [x] bump SW + 4 gardiens (v87 interdit) ; apostrophes : aucune apostrophe brute dans les chaînes JS ajoutées ;
- [x] aucun moteur/calcul modifié ; READONLY.

## 7. Risques restants

1. Pages suivantes du lot 8 (Aujourd'hui/Marchés/…) : exposer MarketContext
   (`changes_since_prev`) et les scanners par univers — sous-PR par espace.
2. La carte affiche le score honnêtement bas tant que fondamentaux/flux ne sont
   pas branchés — c'est voulu (le `basis` l'explique au survol).

## 8. Verdict

**GO** — carte prouvée en navigateur (2 tailles, 0 erreur), gardiens SW alignés,
suite 1266 verte.

## 9. Prochaine étape autorisée

Lot 8 espace suivant (Aujourd'hui : diff de session MarketContext) — ou lot 9 selon priorité humaine.

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**

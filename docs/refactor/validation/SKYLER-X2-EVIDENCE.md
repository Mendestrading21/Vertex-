# SKYLER V2 — X2 — LABORATOIRE D'ÉVIDENCE (forward/MFE/MAE réels)

> Date : 2026-08-05 · Branche : `agent/skyler-v2-x2-evidence` (empilée sur X1)

## Décision

`vertex/engines/evidence_lab.py` (pur) : pour chaque spike historique |z|≥2 de
la série RÉELLE (détecté par le moteur anomalies existant), mesure EXACTE des
rendements forward à 1/5/10 barres et du MFE/MAE sur 10 barres, agrégés en
MÉDIANES par direction (haussier/baissier). Honnêteté structurelle :
**IN-SAMPLE et DESCRIPTIF — la mise en garde « PAS un backtest » est dans la
sortie** ; événement trop récent (< 10 barres d'avenir) compté NON MESURABLE,
jamais extrapolé ; série courte → indisponible ; aucun événement → dit.
C'est la première brique MAE/MFE du lot 9 RC, calculée sur vraies barres.

Route `GET /api/evidence/<sym>` (série canonique, `series_source` exposée).
Carte « Que s'est-il passé après ? » sur la fiche Analyse, entre le scanner
d'anomalies et la décision Skyler. SW v93 → **v94** + gardiens.

## Preuves

```text
tests : 8 passed — cas à la main exacts (+1 %/barre → fwd_5 = +5.10 %,
        MFE = +10.46 %), buckets séparés, non-mesurable compté, série courte,
        zéro événement, étiquette in-sample/backtest, route, page
suite : 1300 passed, 2 skipped · compileall exit 0
```

Navigateur (démo GOOGL, 1440 + 390, 0 erreur, 0 débordement) — résultat RÉEL
parlant : après les 2 spikes haussiers mesurables, médiane **−3,73 %** à
+5 barres ; après le spike baissier, **+10,55 %** — le retour à la moyenne est
visible dans les données, pas affirmé. 1 spike trop récent compté non mesurable.
Capture `docs/skyler/baseline/x2_evidence_1440.png`.

## Verdict

**GO** — l'assistant ne se contente plus de détecter les anomalies : il montre
ce qu'elles ont réellement donné ensuite, médianes exactes, limites affichées.
**Arrêt de lot — validation groupée.**

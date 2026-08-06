# SKYLER V2 — LOT 117 : boucle continue — Research Factory figée

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-117`
(base : `integration/vertex-skyler-v2` @ `1493ee6`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/research/factory.py` (§29 — le cycle de vie IDEA → APPROVED des
signaux de recherche) n'avait que 2 tests nominaux (définition +
walk-forward requis, anti look-ahead). Les transitions INTERDITES
exactes, les erreurs NOMMÉES, l'embargo réel des splits et le seuil
« passed » n'étaient figés nulle part.

## 2. Les 8 comportements figés (nés verts, dits)

```text
transitions interdites REFUSÉES : IDEA ne saute jamais DEFINED ·
  APPROVED ne redevient jamais une idée · RETIRED est TERMINAL         OK
une idée REJECTED peut renaître en IDEA (jamais en APPROVED direct)    OK
état inconnu → LifecycleError qui NOMME l'état                         OK
DEFINED exige les 11 champs — les manquants sont NOMMÉS                OK
APPROVED : les 12 contrôles de biais manquants NOMMÉS · complets
  mais sans walk-forward → « un beau backtest ne suffit jamais »       OK
chaque transition est HISTORISÉE (from/to/evidence)                    OK
splits : échantillon < (folds+1)·20 → refus « trop court » ·
  l'embargo sépare TOUJOURS train et test (bornes exactes figées :
  120 éch. → (0,20)/(25,45) … (0,100)/(105,120))                       OK
passed exige ≥ max(2, n−1) folds positifs : 5/5 → True, 0/5 → False
  — jamais un pass de complaisance                                     OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1976 passed, 2 skipped   (1968 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 118 : angle suivant ; lot 120 = mini-bilan 116-120.

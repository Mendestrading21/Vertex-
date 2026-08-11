# SKYLER V2 — LOT 98 : boucle continue — earnings + barème stratégie figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-98-anomalies`
(base : `integration/vertex-skyler-v2` @ `5dd55ef`, fraîchement fetchée).
**Moteurs INTACTS — diff = tests + docs uniquement.**

## 1. Repérage honnête

option_anomalies : déjà couvert en profondeur (21 tests ciblés — zero
bid, crossed, spread, valeur temps négative, signe des Greeks, rassis).
Trous réels : les MODES post-earnings d'`earnings_engine`, la date
inconnue, le run-up lointain, la désinfection multi-phrases ; et les
BORNES EXACTES du barème `vertex/strategy/config.py` (source unique des
seuils que toute l'app consomme).

## 2. Les 8 comportements figés (nés verts, dits)

```text
date de résultats inconnue → aucune décision, note honnête             OK
jours négatifs → RÉACTION (≤ 2 j) vs DRIFT (> 2 j) exacts              OK
résultats lointains (> 10 j) → RUN-UP avec sortie AVANT l'annonce
  (défaut constitution)                                                OK
≤ 10 j sans dossier → refus avec CHAQUE exigence manquante NOMMÉE
  (les 9 : date confirmée, expected move, IV crush, gap défavorable,
  perte max…) — jamais un refus muet                                   OK
langage interdit (garanti / sans risque / 99 % sûr) neutralisé,
  insensible à la casse, multi-occurrences                             OK
grade : bornes EXACTES 90/80/72/60/45 (S+ → D)                         OK
verdict : BUY exige score ≥ 75 ET trend ≥ 66 · CHOP rétrograde
  TOUJOURS en WATCH · WAIT/AVOID exacts                                OK
poids du score = 100 pile · buckets d'échéance cohérents
  (min < cible < max, deltas croissants dans ]0,1[)                    OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1830 passed, 2 skipped   (1822 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 99 : angle suivant ; LOT 100 = BILAN CONSOLIDÉ n°7 (76-100) +
récapitulatif complet à l'utilisateur.

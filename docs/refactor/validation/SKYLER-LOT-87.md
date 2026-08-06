# SKYLER V2 — LOT 87 : boucle continue — façade recommendation + __VXVOCAB figées

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-87-vocab`
(base : `integration/vertex-skyler-v2` @ `f690615`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Constat de couverture

`vertex/engines/recommendation.py` (212 lignes — la façade UNIQUE :
vocabulaire client __VXVOCAB, normalize des verdicts historiques,
gestion de position détenue, options sur position) n'avait **AUCUN test
dédié** — le `recommendation` testé ailleurs est un HOMONYME
(`vertex.options.recommendation`). Façade entière figée.

## 2. Les 10 comportements figés (nés verts, dits)

```text
__VXVOCAB couvre les 9 décisions du stack + 7 verdicts de gestion,
  chacun avec label FR + tone + classe pill valide — AUCUN TROU     OK
normalize(None/'')  → '—' gris · inconnu → passthrough gris
  (jamais inventé)                                                  OK
alias historiques insensibles à la casse (acheter fort, REFUSÉ,
  renforcer)                                                        OK
position vide       → HOLD (Conserver) par défaut                  OK
stop touché         → EXIT confiance 78                            OK
discipline exacte   → action -20 % coupe · option -20 % NE COUPE
  PAS (limite -25 %, convexité)                                    OK
option ≤ 14 j       → gain TAKE_PROFIT · sans marge EXIT (thêta)   OK
cible à ≤ 4 %       → TAKE_PROFIT · +100 % TRIM · +40 % RAISE_STOP OK
sous-jacent AVOID   → TRIM · STRONG_BUY en gain → ADD              OK
board vide          → suggestions [] + note honnête                OK
```

**Aucun résultat malhonnête — la façade traite chaque cas proprement.
Tout changement futur de sémantique cassera ces 10 tests.**

## 3. Preuves

```text
python -m pytest tests/ -q → 1745 passed, 2 skipped   (1735 + 10)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 88 : angle suivant ; au lot 90, mini-bilan 86-90.

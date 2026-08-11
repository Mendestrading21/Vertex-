# SKYLER V2 — LOT 91 : boucle continue — decide.py figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-91`
(base : `integration/vertex-skyler-v2` @ `e534046`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Constat de couverture

`vertex/engines/decide.py` (128 lignes — le verdict de scan ACHETER
FORT → ÉVITER avec hard gates stratégie) n'avait qu'UN test dédié (le
gate R:R de test_strategy_consistency). 9 caractérisations nées vertes
le figent — dont UNE hypothèse de MA sonde corrigée en cours de lot :
`decide({})` rend `None` (refus honnête, jamais un verdict sans
données) et non ÉVITER — figé tel quel, dit.

## 2. Les 9 comportements figés

```text
None / {} → None (jamais un verdict sans données)                    OK
détail faible → ÉVITER + conviction bornée + action honnête          OK
dossier complet → ACHETER FORT avec plan chiffré dans l'action       OK
hard gate stop absent → SURVEILLER + « invalidation absente »        OK
hard gate régime inconnu → SURVEILLER + « pas de nouveau risque »    OK
borne R:R exacte → 2.0 passe · 1.9 dégradé avec message chiffré      OK
CHOP → jamais un achat (SURVEILLER)                                  OK
sur-étendu → l'action dit « attendre un repli »                      OK
résultats ≤ 14 j → risque IV-crush cité · 60 j → silence             OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1780 passed, 2 skipped   (1771 + 9)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 92 : angle suivant — la tournée continue (committee.py, routes POST
restantes, ou balisage HTML).

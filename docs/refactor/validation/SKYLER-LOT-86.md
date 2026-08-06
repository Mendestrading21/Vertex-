# SKYLER V2 — LOT 86 : boucle continue — cas limites du decision stack figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-86-caracterisation`
(base : `integration/vertex-skyler-v2` @ `a8dc701`, fraîchement fetchée).
**Moteur 0.9.0 INTACT — aucune ligne de logique modifiée.**

## 1. Méthode

Lecture complète de `vertex/engines/decision_stack.py` (349 lignes) +
inventaire croisé avec `tests/test_decision_stack.py` (21 tests
existants) → 10 branches limites réellement NON couvertes identifiées.

## 2. Les 10 branches figées par caractérisation (nées vertes, dites)

```text
evaluate(None)            → DATA_INSUFFICIENT, conviction/confiance 0,
                            entry/stop None (honnête)                 OK
score='n/a'               → conviction 0 — JAMAIS un chiffre inventé  OK
bornes exactes            → 80→STRONG_BUY · 79.9→BUY · 66→BUY ·
                            65.9→WATCH · 56 WATCH→WATCH · 55.9→WAIT   OK
verdict inconnu '???'     → WAIT (repli sûr)                          OK
frontière rassis          → 900 s frais (A) · 901 s rassis (B, -15)   OK
cassure en CHOP           → surveiller, ne pas poursuivre (règle 4)   OK
distribution cachée       → surveiller (règle 7)                      OK
demo=True                 → source demo-synthetic + flag « données
                            synthétiques (démo) » TOUJOURS affiché    OK
R:R absent                → ne dégrade PAS (inconnu ≠ mauvais)        OK
décision non acheteuse    → véhicule ACTION toujours                  OK
```

**Aucun résultat malhonnête trouvé — le moteur traite chaque cas limite
proprement. Son comportement est désormais FIGÉ par la suite : tout
changement futur de sémantique cassera ces 10 tests.**

## 3. Preuves

```text
python -m pytest tests/ -q → 1735 passed, 2 skipped   (1725 + 10)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Moteur 0.9.0 : diff = tests + docs uniquement
```

## 4. Suite

Lot 87 : angle suivant le plus porteur de la tournée perpétuelle.

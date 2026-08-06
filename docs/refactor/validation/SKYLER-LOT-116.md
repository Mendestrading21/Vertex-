# SKYLER V2 — LOT 116 : boucle continue — catalyseurs non-earnings figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-116`
(base : `integration/vertex-skyler-v2` @ `91f1a46`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/catalysts/event_engine.py` (§21/§23 — classement des catalyseurs
event-driven : guidance, régulateur, investor day…) n'avait AUCUN test.
Sa règle de sûreté — un événement NON CONFIRMÉ ne justifie jamais un
mode earnings ni un hold-through — n'était figée nulle part.

## 2. Les 8 comportements figés (nés verts, dits)

```text
non confirmé → JAMAIS dans l'horizon actionnable, même à 5 jours       OK
type inconnu → reclassé OTHER ET dénoncé dans unknown_types (jamais
  avalé en silence) · type absent = OTHER sans dénonciation            OK
horizon 0-30 j : bornes INCLUSES, passé/31 j/date inconnue exclus,
  trié par proximité · has_near_catalyst ⇔ horizon non vide            OK
events vides ou None → structure vide honnête                          OK
fenêtre earnings du résumé : 45 j INCLUS, 46 exclu, 0 inclus,
  passé (-2) exclu, None = pas de catalyseur                           OK
next_events plafonné à 3 (les plus proches)                            OK
non confirmés → avertissement NOMMÉ avec le compte exact et la règle
  (« jamais utilisés pour tenir une position à travers un événement ») OK
tout confirmé → zéro avertissement, catalyseur reconnu                 OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1968 passed, 2 skipped   (1960 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 117 : angle suivant ; lot 120 = mini-bilan 116-120.

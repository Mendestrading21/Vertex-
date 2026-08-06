# SKYLER V2 — LOT 89 : boucle continue — track_record figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-89-track`
(base : `integration/vertex-skyler-v2` @ `9569a87`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Constat de couverture

`vertex/engines/track_record.py` (181 lignes — le moteur qui NOTE Vertex
lui-même : ledger append-only des verdicts + jointure aux prix réels +
stats de fiabilité) n'avait **AUCUN test dédié**. Figé par 6
caractérisations nées vertes (dites), ledger simulé par monkeypatch —
les fichiers runtime (edge_ledger, track_meta) n'ont jamais été touchés.

## 2. Les 6 comportements figés

```text
record() sans lignes      → 0, aucun fichier touché                  OK
_fwd bords                → date inconnue (None,None) · bord de
  série None · clôture 0 → None · nominal exact +4,0 %               OK
_hit_tp1                  → TP1 d'abord True · stop d'abord False ·
  non résolu None (honnête) · plan incomplet None                    OK
ledger vide               → entries 0, groupes vides, méthode
  approximative TOUJOURS dite dans note                              OK
seuil d'échantillon       → n<5 JAMAIS publié · win_1j calculé sans
  division par zéro · TP1 sans plan → None (dénominateur 0)          OK
mémoïsation 30 min        → le ledger n'est pas relu à chaque appel  OK
```

**Aucune stat inventée possible : historique vide → zéros honnêtes,
petit échantillon → tu, plan absent → None.**

## 3. Preuves

```text
python -m pytest tests/ -q → 1761 passed, 2 skipped   (1755 + 6)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 90 : services critiques (persist/connections) + MINI-BILAN 86-90.

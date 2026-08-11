# SKYLER V2 — LOT 99 : boucle continue — broker SSE + états système figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-99`
(base : `integration/vertex-skyler-v2` @ `cb1cd0d`, fraîchement fetchée).
**Moteurs INTACTS — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/services/live_stream.py` (le broker pub/sub des Server-Sent
Events — tout le temps réel de l'app y passe) n'avait AUCUN test direct :
seule mention = son nom dans une liste de workers (test_obsidian_theme).
Et `status_service` n'était figé que sur les 4 états IBKR + la forme
nominale — pas les transitions ok/warming/degraded ni la fraîcheur.

## 2. Les 9 comportements figés (nés verts, dits)

```text
canal inconnu → reclassé « system » (jamais perdu, jamais inventé) ·
  ids strictement croissants depuis 1                                  OK
replay_since (Last-Event-ID) → seulement les événements PLUS récents,
  client à jour → []                                                   OK
tampon circulaire borné : au-delà de la capacité les plus anciens
  sortent, les ids restent vrais, stats exactes                        OK
client lent (file pleine à 501 événements) → le diffuseur n'attend
  JAMAIS (surplus ignoré, last_id avance)                              OK
unsubscribe idempotent : double départ silencieux, plus rien livré     OK
sse_format : framing NOMMÉ exact « id:/event:/data: » + double saut
  final, accents intacts (leçon lot 85 : onmessage muet sur un
  event: nommé — addEventListener est le contrat)                      OK
app : {} → warming (« aucun titre ») · error → degraded (prime sur
  tout) · rows + scan frais → ok, 0 avertissement                      OK
fraîcheur : scan vieux → stale + « rassis » (avertissement, pas
  panne) · pas de timestamp → unknown honnête, jamais fresh par
  défaut · timestamp pourri → None                                     OK
mode : demo PRIME sur ibkr, sinon ibkr, sinon cloud                    OK
```

Brokers NEUFS à chaque test — le BROKER global partagé jamais touché.

## 3. Preuves

```text
python -m pytest tests/ -q → 1839 passed, 2 skipped   (1830 + 9)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 100 = BILAN CONSOLIDÉ n°7 (76-100) + récapitulatif complet à
l'utilisateur.

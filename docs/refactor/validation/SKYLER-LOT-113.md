# SKYLER V2 — LOT 113 : boucle continue — types de provenance figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-113`
(base : `integration/vertex-skyler-v2` @ `b2912dc`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

engines/backtest : déjà couvert (golden 136863.1, forme sans NaN,
< 3 titres → None honnête — dit). Trou réel :
`vertex/data_sources/models.py` — les TYPES porteurs de provenance
(ProvenancedValue.usable, missing(), AnalyticsPacket) sur lesquels
repose toute la couche données. Les constantes sont importées partout
mais les comportements n'avaient AUCUN test direct.

## 2. Les 8 comportements figés (nés verts, dits)

```text
missing() honnête par défaut : UNAVAILABLE/NONE/MISSING, non
  utilisable, fallback False · avertissement nommé si fourni          OK
usable exige valeur ET qualité vivante : FRESH/RECENT/STALE → True
  (STALE = dégradé, pas mort) · EXPIRED/MISSING → False · valeur
  None jamais utilisable même « fraîche »                              OK
0.0 et False sont des VALEURS réelles (seul None = pas de donnée —
  le piège falsy est évité)                                            OK
contrat to_dict complet (8 clés), warnings inclus                      OK
listes de warnings JAMAIS partagées entre instances                    OK
AnalyticsPacket : 5 familles de sources initialisées vides, qualité
  MISSING + warnings [], as_of ISO UTC auto                            OK
set_source stocke un DICT figé (snapshot to_dict, pas l'objet) ·
  contrat to_dict du paquet (4 clés)                                   OK
deux paquets ne partagent JAMAIS leurs sources (default_factory)       OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1944 passed, 2 skipped   (1936 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 114 : angle suivant ; lot 115 = mini-bilan 111-115.

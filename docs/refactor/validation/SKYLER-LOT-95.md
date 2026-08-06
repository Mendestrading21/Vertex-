# SKYLER V2 — LOT 95 : boucle continue — filtres durs options figés + bilan 91-95

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-95-indicators`
(base : `integration/vertex-skyler-v2` @ `6320090`, fraîchement fetchée).
**Moteurs INTACTS — diff = tests + docs uniquement.**

## 1. Repérage honnête

- indicators.py : déjà couvert (38 tests dont goldens) — pas d'angle ;
- anomaly.py (10 tests) / events.py (14 tests) : couverts — pas d'angle ;
- call_selector : couvert par test_options_engine (import combiné que ma
  détection avait manqué — dit) ;
- **contract_filter.py : couvert seulement INDIRECTEMENT** — les filtres
  DURS (un contrat écarté ici n'est jamais scoré ni proposé) méritaient
  des caractérisations directes. C'est l'angle du lot.

## 2. Les 6 comportements figés (nés verts, dits)

```text
bornes DTE constitution INCLUSIVES (min et max passent, ±1 refusé) ·
  DTE None → jamais accepté par défaut                                 OK
bande de delta existe pour CHAQUE catégorie CALL · catégorie
  inconnue → None                                                      OK
delta inconnu → jamais classé (absent ≠ conforme)                      OK
hard_filter : refus DOCUMENTÉS (« hors bornes constitution »,
  « liquidité intraitable ») · PUT ni gardé ni rejeté (hors périmètre
  du moteur CALL)                                                      OK
contrats gardés annotés _liquidity (tradeable) + _anomalies            OK
bucket_by_category répartit par bande de delta exacte                  OK
```

## 3. MINI-BILAN 91-95

5 lots, 36 tests, suite 1771 → **1807**, **1 défaut réel de moteur
corrigé** (committee : la fenêtre « DANS LA ZONE D'ACHAT » était du code
mort — elle s'ouvre enfin), skyler_core jamais touché :

- 91 · decide.py figé (9) — hard gates stop/régime/R:R 2.0 exact ;
- 92 · committee.py — DÉFAUT RÉEL corrigé + 9 caractérisations ;
- 93 · pivots/structure figé (8) — measured move exact, piège refusé ;
- 94 · contrat POST figé (4) — 0×5xx, télémétrie bornée ;
- 95 · filtres durs options figés (6).

## 4. Preuves

```text
python -m pytest tests/ -q → 1807 passed, 2 skipped   (1801 + 6)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 5. Suite

Lot 96 : angle suivant — la tournée continue.

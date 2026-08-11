# SKYLER V2 — LOT 145 : caractérisation du moteur scorecard (score /40)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-145`
(base : `integration/vertex-skyler-v2` @ `eb489e8`, lot 144 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié.

## 1. Cible

`vertex/engines/scorecard.py` (254 lignes). Vérification préalable
exigée par le canevas : le module est-il encore servi ? **OUI — bien
vivant** : `terminal.py:46` l'importe (alias `ibkr`) et
`terminal.py:617` appelle `verdict()` pendant le scan. Il produit le
SCORE /40, les niveaux S+/S/A/B/rejeté + allocations, l'entry timing,
le filtre no-chase et le verdict final affichés dans Opportunités.
C'était le DERNIER moteur à zéro référence dans tests/.

## 2. Ce qui est figé (`tests/test_scorecard_lot145.py`, 36 tests)

```text
Grille des niveaux — bornes EXACTES : ≥36 S+ (10-15 %) · ≥32 S
  (7-10 %) · ≥28 A (3-5 %) · ≥22 B (1-2 %) · <22 rejeté (0 %)
No-chase — les 4 raisons de surchauffe isolées une à une (RSI ≥72,
  extension ≥2.5x ATR, bougie ≥2x ATR, sommet 52s sans volume)
  + titre propre → liste vide
Entry timing — les 6 chemins d'état : BUY_NOW · AVOID (<50) ·
  TOO_LATE (RSI ≥76) · BUY_PULLBACK (no-chase) · WATCH_BREAKOUT
  (60-69) · BUY_PULLBACK par défaut (50-59) ; niveaux repris du
  plan (resistance prioritaire sur tp1)
Score /40 — plancher neutre EXACT du dict vide : 18/40
  (5+1+3+2+4+3) → rejeté : L'INCONNU N'EST JAMAIS INVESTISSABLE
  (18 < seuil B 22) ; fenêtre catalyseur earnings (7-45 j idéale
  → 6, <7 j risque binaire → 3, 46-90 j → 4, au-delà → 3, bonus
  TREND plafonné à 6)
Verdict — None ET dict vide (falsy) → None (pas de données, pas
  de verdict) ; ACCEPTÉ sur idée propre ; REFUSÉ → taille 0 % ;
  composantes : 6 clés, maxima 8/8/6/6/6/6, SOMME == score40
  affiché (une seule vérité) ; robustesse aux valeurs pourries
  (strings/None → défauts, jamais d'exception, plancher 18)
```

## 3. Preuves

```text
python -m pytest tests/test_scorecard_lot145.py -q → 36 passed
python -m pytest tests/ -q → 2033 passed, 2 skipped (1997 + 36)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 146 : caractérisation suivante parmi les moteurs à 1 seule
référence (analysis, events, postmortem, pretrade, stats,
strategy_fit) — priorité à ceux servis par une route.

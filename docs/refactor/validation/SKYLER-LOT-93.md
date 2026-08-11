# SKYLER V2 — LOT 93 : boucle continue — pivots/structure figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-93-structure`
(base : `integration/vertex-skyler-v2` @ `54c7fdc`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Pourquoi cet angle

`vertex/quant/pivots.py` (124 lignes — la structure de marché par pivots
fractals : tendance, cassure, repli repris, refus) NOURRIT committee.py
et la zone d'achat réparée au lot 92 — il venait de gagner en importance.
**Aucun test dédié n'existait.**

## 2. Les 8 comportements figés (nés verts, dits — séries synthétiques déterministes)

```text
entrées invalides (None, colonnes manquantes, série courte) → None      OK
zigzag haussier en milieu de mouvement → EN_TENDANCE, non confirmé,
  « attendre la cassure »                                               OK
miroir baissier → REFUS_DOWNTREND, « piège », jamais confirmé           OK
cassure FRAÎCHE (≤ 1,2 ATR au-dessus du sommet, franchi récemment) →
  BREAKOUT confirmé · stop SOUS le dernier creux · cible = measured
  move exact · R:R = (cible−entrée)/(entrée−stop) exact                 OK
cassure ÉTENDUE (> 1,2 ATR) → jamais poursuivie (non confirmé)          OK
repli sur le dernier creux PUIS reprise → REPLI_REPRIS confirmé,
  cible = dernier sommet                                                OK
range plat → RANGE, « cassure confirmée » exigée                        OK
ATR None/0 → repli 1 % du prix, jamais de division par zéro             OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1797 passed, 2 skipped   (1789 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 94 : angle suivant ; lot 95 = MINI-BILAN 91-95.

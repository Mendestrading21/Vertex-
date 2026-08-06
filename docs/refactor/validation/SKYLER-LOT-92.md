# SKYLER V2 — LOT 92 : boucle continue — committee.py : branche morte réparée

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-92-committee`
(base : `integration/vertex-skyler-v2` @ `d233cc0`, fraîchement fetchée).
**skyler_core 0.9.0 NON touché** — le moteur corrigé est le comité de
SCAN (`vertex/engines/committee.py`, sans version figée au ledger).

## 1. Défaut RÉEL découvert par la caractérisation

`committee.py` (les 4 portes, anti-impatience) n'avait AUCUN test dédié.
En figeant la « zone d'achat », mon test rouge a prouvé que la branche
**« ✅ DANS LA ZONE D'ACHAT — fenêtre d'entrée ouverte »** était du
**code mort mathématique** : le garde `ez < price` exigeait le cours
AU-DESSUS de la zone pour la calculer, alors que `in_zone` exigeait le
cours DEDANS — contradiction. Conséquence : la note promettait « 🎯 on
guette le repli », mais quand le repli ARRIVAIT, la zone disparaissait
et le trader voyait un « attendre » générique. La fenêtre promise ne
s'ouvrait jamais.

## 2. Correction minimale (le nominal ne change pas)

La zone est TOUJOURS calculée quand résistance > stop : au-dessus, on
guette (affichage strictement identique à avant) ; dès que
`prix ≤ (résistance + 2·stop)/3` — c'est-à-dire R:R(prix) ≥ 2:1 — la
fenêtre s'ouvre comme la note l'a toujours promis. Preuve : prix 110 →
ATTENDRE avec « Zone d'achat : sous $101.33 » (inchangé) · prix 100 →
**ACHETER « DANS LA ZONE »** (avant : ATTENDRE générique sans zone).

## 3. Tests (le rouge d'abord + 8 caractérisations)

`tests/test_committee_lot92.py` (9) : univers vide honnête · symbole
sans détail sauté · qualité insuffisante ÉVITER · rebond en tendance
baissière = PIÈGE refusé · sur-étendu/CHOP ATTENDRE · formule de zone
exacte + fenêtre in_zone (LE test rouge) · élite vs RENFORCER · tri
ACHETER→ÉVITER + seuils du verdict global.

## 4. Preuves

```text
python -m pytest tests/ -q → 1789 passed, 2 skipped   (1780 + 9)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

Pas de bump SW (aucun changement de shell — la sortie moteur alimente
les mêmes gabarits).

## 5. Suite

Lot 93 : angle suivant — la tournée continue.

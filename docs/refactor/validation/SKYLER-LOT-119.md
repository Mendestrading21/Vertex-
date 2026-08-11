# SKYLER V2 — LOT 119 : amélioration graphique n°1 — Catalyst Runway développé (Aujourd'hui)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-119`
(base : `integration/vertex-skyler-v2` @ `c078421`, fraîchement fetchée).
**NOUVELLE DIRECTIVE utilisateur : « améliorer chaque page, des
graphiques encore plus propres, plus beaux, plus développés ».**
Moteurs INTACTS — diff = builder JS + bump SW + 4 gardiens + docs.

## 1. Diagnostic (capture AVANT, page /)

Le graphique le plus faible d'Aujourd'hui : « Catalyseurs imminents »
(Catalyst Runway) — ligne fine, petits points uniformes, étiquettes
chevauchées à J-7, aucune hiérarchie d'impact, aucune notion visuelle
d'urgence.

## 2. Améliorations (vertex/static/vertex/js/charts/catalyst-runway.js)

```text
zone d'imminence ≤ 5 j : bande teintée var(--vx-negative) à 8 % +
  libellé « zone ≤ 5 j » — l'urgence se VOIT avant de se lire
points dimensionnés par impact : high r=5 + halo doux · med r=4 ·
  low r=3 — la hiérarchie remplace l'uniformité
prochain catalyseur : anneau de focalisation — l'œil sait où regarder
graduations hebdomadaires (7j/14j/21j…) discrètes sous la piste
bornes nommées : « aujourd'hui » à gauche, « horizon J-N » à droite
étiquettes : 14 caractères (au lieu de 12), viewBox 132 (respiration)
anti-collision 2 rangées conservé · aucun littéral couleur nouveau
  (tokens var(--vx-*) uniquement) · état vide honnête inchangé
```

SW `td-shell-v127` → `td-shell-v128` + 4 gardiens (v127 absent).

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped   (gardiens SW ajustés)
tools/rc_short_audit.js → GO — 0 défaut (SW v128)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées à l'utilisateur
```

## 4. Suite

LOT 120 : amélioration graphique n°2 (page Marchés) + MINI-BILAN
116-120.

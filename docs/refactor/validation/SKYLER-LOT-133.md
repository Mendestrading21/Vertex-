# SKYLER V2 — LOT 133 : passe n°8 — payoff de structure Options (2 bugs préexistants tués)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-133`
(base : `integration/vertex-skyler-v2` @ `312ffc9`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
options-structure.js + SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /options — Structure)

Le payoff du desk Options (multileg, DIFFÉRENT du payoffCard corrigé
au lot 124) : trait nu sans zones ni halo, et surtout **les repères
spot/breakeven n'apparaissaient JAMAIS** — deux bugs préexistants :
(a) `C.mount(canvas, config)` ne prend que 2 arguments — le 3e
argument `[refPlugin]` était silencieusement ignoré, le plugin ne
tournait pas ; (b) même exécuté, `getPixelForValue(prix)` sur un axe
CATÉGORIE attend un index — le repère tombait hors de l'axe. Les
couleurs des repères étaient en plus des rgba hors palette
(`rgba(200,173,141)`, `rgba(221,162,59)`).

## 2. Corrections + verre (options-structure.js)

```text
plugins déplacés AU BON ENDROIT : clé racine `plugins:[…]` de la
  config Chart.js (comme multiLine) — refPlugin s'exécute enfin
mapping prix → index (idxOf, plus proche point) — spot et BE
  tombent au bon pixel sur l'axe catégorie
repères sur TOKENS (grammaire lot 124) : spot en info (cyan),
  breakeven en warning — plus aucun rgba orphelin
zones gain/perte teintées (positive+'24' / negative+'20') —
  on VOIT où la structure gagne · trait 1.6 + softGlowPlugin
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v142)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS + zoom du payoff envoyées —
  BE (153.23) et spot (180) enfin visibles
```

SW `td-shell-v141` → `td-shell-v142` + 4 gardiens.

## 4. Suite

LOT 134 : passe n°9 (candidats : sous-vues Options restantes —
Positionnement/LEAPS/Volatilité —, Radar Opportunités).

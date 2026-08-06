# SKYLER V2 — LOT 104 : boucle continue — environnement options figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-104`
(base : `integration/vertex-skyler-v2` @ `14367f6`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/options/environment.py` (score « LONG OPTION ENVIRONMENT » §14 —
l'agrégat 5 dimensions affiché par l'espace Options) n'avait que 3 tests
de SURFACE (bornes, IV basse favorable, tableau vide inconnu). Les
formules exactes par dimension, les frontières 66/45 et l'exclusion
honnête des dimensions inconnues n'étaient figées nulle part.

## 2. Les 8 comportements figés (7 nés verts + 1 sonde corrigée, dits)

```text
volatilité : IV médiane 20 % → 100 pts · 60 %+ → 0 · 40 % → 50 pile     OK
IV textuelle ou nulle = indisponible (jamais convertie en silence)      OK
IV rank inversé (0 → 100, 100 → 0) et borné (120 → 0, jamais négatif)   OK
liquidité : spread 1 % → 100 · 8 % → 0 · 0.5 % borné à 100 · 4.5 → 50   OK
event risk : fraction ≤7 j exacte (1/2 → 50) · aucune date connue →
  INCONNU (pas 100) · valeur non parsable = CONNUE mais jamais
  imminente (ma sonde attendait l'exclusion — réalité figée, dite)      OK
verdict : 66 → PORTEUR · 65.9 → MITIGE · 45 → MITIGE · 44.9 → HOSTILE   OK
dimension inconnue EXCLUE de la moyenne (1 seule mesurable → sa note,
  jamais diluée par des zéros) + chaque absente NOMMÉE en incertitude   OK
interprétation : PORTEUR → FAVORABLE · HOSTILE → DÉFAVORABLE ·
  confiance = dims connues / 5 (0.6 exact à 3/5)                        OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1872 passed, 2 skipped   (1864 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 105 : lot de travail + MINI-BILAN tournée 101-105.

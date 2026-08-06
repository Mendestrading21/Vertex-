# SKYLER V2 — LOT 114 : boucle continue — frontière d'unités IV figée

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-114`
(base : `integration/vertex-skyler-v2` @ `3c5d7db`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/options/iv_units.py` — la FRONTIÈRE de normalisation née du
grand défaut « IV % vs décimal » (contrat OPTIONS_CORRECTNESS : plus
jamais d'heuristique silencieuse dans le cœur). Seules 4 assertions
existaient : la porte legacy `from_legacy_board` (détection ÉTIQUETÉE,
jamais muette), la frontière EXACTE du seuil 1.5 et les rejets NaN/inf
n'étaient figés nulle part. app/state = simple porteur de données (dit).

## 2. Les 8 comportements figés (nés verts, dits)

```text
unité inconnue → ValueError (une unité devinée est un BUG, pas une
  donnée) — y compris 'percent' minuscule et None                      OK
NaN/inf/≤0/texte non numérique → None dans LES DEUX unités             OK
conversions exactes : 40.4 % → 0.404 · décimal inchangé · texte
  numérique accepté                                                    OK
legacy board : pourcentage DÉTECTÉ et ÉTIQUETÉ (avertissement citant
  la frontière) — jamais une conversion muette                         OK
legacy board : décimal passe SANS avertissement                        OK
seuil 1.5 EXACT : 1.5 pile = décimal (150 % de vol, rare mais réel)
  · 1.51 → pourcentage averti                                          OK
legacy board : ordure → triple None (valeur, unité, avertissement)     OK
la frontière n'exporte QUE ses deux portes (pas d'heuristique cachée)  OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1952 passed, 2 skipped   (1944 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 115 : lot de travail + MINI-BILAN tournée 111-115.

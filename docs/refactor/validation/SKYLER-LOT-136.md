# SKYLER V2 — LOT 136 : passe n°11 — Radar Opportunités (comparaison en verre + score /40 en barre)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-136`
(base : `integration/vertex-skyler-v2` @ `a4d7ef9`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
neon-glass.css + opportunities_page.py + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /opportunities & /portfolio?view=watchlist)

Watchlist : états vides honnêtes en démo (corrects). Radar : deux
widgets encore plats — (a) la **Comparaison des meilleurs candidats**
(7 critères × 4 candidats) : barres grises uniformes, le « meilleur
du critère » à peine distinguable ; (b) le **Classement Skyler** :
score canonique « 22/40 » en chiffre nu sur 20 lignes.

## 2. Améliorations

```text
comparaison (neon-glass.css) : chaque barre devient un dégradé de
  sa propre couleur (doux → dense, patron 130-135) et le MEILLEUR
  du critère gagne un halo doux ember — le gagnant se voit sans
  lire les nombres (ACN score, AOS asymétrie/R:R/edge, MMM
  momentum ressortent instantanément)
classement Skyler (opportunities_page.py) : le score /40 gagne sa
  mini-barre de verre graduée — ≥ 28 positive, 16-27 warning,
  < 16 negative — valeur /40 conservée
color-mix sur tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v144` → `td-shell-v145` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v145)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Radar)
```

## 4. Suite

LOT 137 : passe n°12 (candidats : Positions Portefeuille, vues
Aujourd'hui restantes, design system page).

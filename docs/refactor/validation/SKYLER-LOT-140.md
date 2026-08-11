# SKYLER V2 — LOT 140 : passe n°15 — Top/Flop 10 en barres signées + mini-bilan

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-140`
(base : `integration/vertex-skyler-v2` @ `efc99d5`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
markets_page.py + SW + gardiens + docs.

## 1. Diagnostic (Vue d'ensemble Marchés)

Les listes TOP 10 / FLOP 10 affichaient la variation en pourcentage
NU (coloré mais sans ampleur visuelle) — impossible de voir d'un coup
d'œil que ABT (-6,3 %) pèse trois fois ALGN (-1,3 %).

## 2. Amélioration (moversRows, markets_page.py)

```text
chaque variation gagne sa MINI-BARRE de verre SIGNÉE : positive →
  barre verte depuis la gauche, négative → barre rouge alignée à
  droite ; dégradé doux → dense via color-mix ; échelle RELATIVE au
  max de la liste — la hiérarchie des mouvements se lit sans les
  pourcentages
le pourcentage, le secteur, le prix, le score et le menu ⋯ restent
  inchangés · état vide honnête inchangé
color-mix sur tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v148` → `td-shell-v149` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v149)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Vue d'ensemble)
```

## 4. Mini-bilan 136-140 (chiffres vérifiés dans les rapports)

5 lots, suite constante 1984/2, PR #169 → #173, SW v144 → v149 :
comparaison des candidats en verre + score Skyler /40 (136) · poids
de position avec repère du plafond de tier (137) · concentration
avec repère prudent ~15 % (138) · leadership sectoriel avec halo du
meneur (139) · Top/Flop 10 en barres signées (140). Le patron
« mini-barre de verre color-mix sur tokens » est GÉNÉRALISÉ — plus
un seul chiffre nu structurant sur les 8 espaces.

## 5. Suite

LOT 141 : passe n°16 (candidats : fiche Analyse sections 1/4 —
Pairs et Sentiment —, page Système vues Données/Automatisations).

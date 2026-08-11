# SKYLER V2 — LOT 127 : passe n°2 — heatmaps matière verre (scénarios options, secteurs, P&L mensuel)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-127`
(base : `integration/vertex-skyler-v2` @ `69f7328`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE — nouvelle passe après la 1re tournée.**
Moteurs INTACTS — diff = heatmap.js + SW + gardiens + docs.

## 1. Diagnostic

Tour des widgets options avancés : theta (C.area) et sensibilité IV
(C.barCard) héritent déjà des acquis 120/125. Le graphique encore PLAT :
`C.heatmapCard` — le builder de la **matrice scénarios options**
(Stop/Flat/TP × temps), de la heatmap **secteurs** (Marchés) et du
**P&L mensuel** (Portefeuille) — avec les DERNIERS rgba verts/rouges
hors palette (`rgba(34,199,122,…)`, `rgba(239,83,80,…)`) et des aplats
pleine largeur collés.

## 2. Améliorations (heatmap.js — les 3 consommateurs héritent)

```text
couleurs dérivées des TOKENS : C.colors.positive/negative convertis
  en rgb à l'exécution (helper rgbOf) — les derniers littéraux
  hors palette du système graphique sont morts
chaque cellule est une TUILE de verre : dégradé diagonal 135° de sa
  propre couleur (dense haut-gauche → doux bas-droit, même grammaire
  que treemap lot 123 et barres lot 125), liseré fin en inset,
  coins arrondis 5
grille AÉRÉE : border-spacing 3px — fini le bloc d'aplats collés
état absent inchangé (surface neutre honnête) · aria/titres inchangés
```

SW `td-shell-v135` → `td-shell-v136` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v136)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Marchés/Secteurs — la
  matrice scénarios options n'apparaît qu'après simulation d'un
  contrat, même builder)
```

## 4. Suite

LOT 128 : passe suivante — vol cone / sparklines / ce qui reste de
plus plat.

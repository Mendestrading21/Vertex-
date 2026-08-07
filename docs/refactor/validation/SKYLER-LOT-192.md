# SKYLER LOT 192 — Tournée TV : regimeAura aligné + payoff hachuré

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-192` (base : lot 191 fusionné)

## Livré

### 1. Regime Aura aligné sur la grammaire TV (Aujourd'hui)

`vertex/static/vertex/js/charts/regime-aura.js` — l'arc de confiance
rejoint le langage de la jauge TV du lot 189 :

- l'arc ENTIER (152° → 388°) est désormais rendu en **dégradé continu**
  de la tonalité du régime (fondu .18 → .95 gauche→droite), au lieu du
  couple piste grise + arc blanc partiel ;
- **pointeur blanc court posé sur l'arc** à la position de la confiance
  (r 50 → 60 + halo de tonalité r 62), même grammaire que l'aiguille de
  `C.gauge` — jamais sur le texte central ;
- le texte « x % confiance » passe en évidence **coloré tonalité, gras
  800** quand la confiance est connue (muté sinon — état honnête
  conservé : sans régime → `VX.states.empty`, l'aura ne s'invente pas).

Halo atmosphérique, chips de grammaire (Marché/Breadth/VIX) et verdict
« risque neuf autorisé/bloqué » inchangés. Tonalité toujours dérivée
UNIQUEMENT de `newRisk` moteur.

### 2. Payoff Options — zones GAIN/PERTE hachurées (tournée TV)

`vertex/static/vertex/js/charts/option-payoff.js` :

- helper `_hatch(color)` : équivalent **canvas** du `tvHatch` SVG
  (teinte faible .08 + rayures 45° .38) — le payoff à l'échéance est
  une ESTIMATION, la texture le dit ;
- le remplissage au-dessus/en-dessous de zéro passe des aplats
  translucides aux **motifs hachurés** positif/négatif
  (`fill.above/below` = CanvasPattern, Chart.js natif) ;
- **libellés de zones** « GAIN » / « PERTE » de part et d'autre du
  breakeven (côté profitable selon C/P), masqués si la zone est trop
  étroite (< 34 px).

Arithmétique du contrat STRICTEMENT inchangée (mêmes xs/ys, mêmes
marqueurs spot/BE). Contrat incomplet → état vide honnête inchangé.

## Accros

Aucun accro de code. Constat de DONNÉES DÉMO (rendu honnête, pas un
défaut du builder) : le contrat démo GOOGL porte une prime aberrante
(3812) et un breakeven fourni (136.98) incohérent avec le strike
(175.1) → le P&L affiché est ≈ −100 % partout et le BE tracé là où la
donnée le dit. Le builder trace les chiffres FOURNIS sans les corriger
— comportement voulu (données réelles uniquement).

## Preuves

- `node --check` OK sur les 2 fichiers modifiés.
- Serveur DEMO port 5002 : captures `lot192-today-1440.png`,
  `lot192-today-390.png`, `lot192-aura-card.png` (arc dégradé rouge +
  pointeur à 0 %, UNKNOWN — 0 % confiance en rouge gras),
  `lot192-payoff-card.png` (hachures pleines zone, BE/spot/PERTE/GAIN)
  — envoyées, **0 erreur console**.
- SW `td-shell-v155` → `v156` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 193 : suivant de TV-CHARTS-INVENTORY.md — sparklines KPI +
catalystRunway (Aujourd'hui) OU aires indices avec zone d'estimation
(Marchés). Mini-bilan 191-195 au lot 195.

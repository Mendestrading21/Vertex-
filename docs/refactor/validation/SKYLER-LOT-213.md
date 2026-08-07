# SKYLER LOT 213 — Gardien hex nu étendu aux builders JS + 1 littéral soldé

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-213` (base : lot 212 fusionné)

## Livré

### 1. Calibration sur les builders JS statiques (avant d'écrire)

Balayage de `charts/*.js` + `pages/*.js` : **49 occurrences** de hex
quotés →

- 40 = **définitions de palette** (bloc `C.colors = Object.assign({…})`
  de chart-core + `chart-theme-obsidian-copper.js` entier) — la SOURCE
  des tokens doit bien porter les hex quelque part : légitimes ;
- 8 = lookups `col(VC, 'name', '#hex')` (repli après token) :
  légitimes ;
- **1 littéral réellement nu** : le texte des tuiles du treemap
  (`fill="#f3f1ed"`, chart-core) → soldé :
  `var(--vx-text-primary,#F8F5F3)` (SVG, var() natif, repli dans
  l'inventaire sûr).

### 2. Gardien `tests/test_no_bare_hex_static_js_lot213.py` (3 tests)

- refus des hex nus dans les builders, formes de repli légitimes
  élargies (`fn('n','#hex')`, `fn(obj,'n','#hex')`, `var()`, `||`) ;
- exemptions BORNÉES et testées : le thème entier + le bloc palette de
  chart-core découpé par ses bornes exactes
  (`C.colors = Object.assign(` → `}, THEME.colors);`) — si les bornes
  bougent, le test casse au lieu de scanner à côté ;
- épinglage du correctif treemap (le hex ne revient pas).

Avec le lot 212, la chaîne complète est couverte : pages Python +
builders JS — plus aucun endroit où un hex nu peut se glisser sans
casser la suite.

## Décision SW

Bump `td-shell-v170` → `v171` + 5 gardiens : le texte des tuiles
treemap change subtilement (#f3f1ed → valeur réelle du token) — le
correctif doit se déployer.

## Preuves

- `node --check` OK ; nouveau gardien 3/3 ; suite complète
  **2472 passed / 2 skipped** (2469 + 3).
- Navigateur : /portfolio (treemap) — 0 erreur console, capture
  envoyée.

## Suite

LOT 214 : entretien suivant ou directive. Mini-bilan 211-215 au
lot 215. Purge terminal.py toujours EN ATTENTE d'accord humain.

# SKYLER LOT 212 — Gardien « aucun hex nu dans les pages » + 2 littéraux soldés

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-212` (base : lot 211 fusionné)

## Livré

### 1. Correction honnête du lot 211

Le « balayage complet » du lot 211 était INCOMPLET : la calibration du
gardien de ce lot a trouvé 2 littéraux nus de plus, soldés ici :

- `markets_page.py` (étiquettes du RRG, canvas) : `'#bab4ac'` →
  `(window.VXCharts&&VXCharts.colors&&VXCharts.colors.muted)||'#8A8284'`
  (token d'abord, repli dans l'inventaire sûr des gardiens) ;
- `opportunities_page.py` (bordure des points en mode démo) :
  `'#FFC857'` → `VXCharts.colors.warning` (VXCharts garanti — la même
  expression référence déjà VXCharts.colors.brand).

### 2. Gardien pérenne `tests/test_no_bare_hex_pages_lot212.py` (3 tests)

Balayage de `vertex/ui/pages/*.py` : tout hex quoté `'#xxxxxx'` est
REFUSÉ sauf dans les formes de repli légitimes — `var(--…, #hex)`,
`cc('n','#hex')`, `col('n','#hex')`, `cssv('--v','#hex')`, et
`lookup || '#hex'` (repli canvas). Exemption DOCUMENTÉE et testée :
`widget_lab.py` (bibliothèque design FIGÉE, palette de mise en scène
délibérée — hors périmètre produit). + test d'épinglage des 2 sites
corrigés (les hex ne reviennent pas) + test que l'exemption reste
intentionnelle.

Calibré contre l'état réel AVANT commit : 10 occurrences trouvées →
2 réelles (soldées), 8 = widget_lab (exemptées) → gardien vert à 0.

## Décision SW

Bump `td-shell-v169` → `v170` + 5 gardiens : deux pages visibles
changent subtilement (gris des étiquettes RRG, ambre de la bordure
démo → vraies valeurs des tokens) — le correctif doit se déployer.

## Preuves

- Nouveau gardien : 3/3 verts ; suite complète **2469 passed /
  2 skipped** (2466 + 3).
- Navigateur : /markets?view=sectors + /opportunities — 0 erreur
  console, captures envoyées.

## Suite

LOT 213 : entretien suivant ou directive. Mini-bilan 211-215 au
lot 215. Purge terminal.py toujours EN ATTENTE d'accord humain.

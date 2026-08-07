# SKYLER LOT 291 — La palette se ferme d'un tap sur le fond

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-291` (base : lot 290 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — la sortie tactile qui manquait

Les lots 288/289 ont soigné l'ENTRÉE tactile de la palette (tap sur la
recherche). Le calibrage de ce lot a regardé la SORTIE : `.vx-palette`
est un fond plein écran (`position:fixed;inset:0`) et ses seules
fermetures étaient **Échap** (câblé sur `document`, inexistant au
tactile) et **choisir un item** — le clic sur `vx-overlay` ferme aussi,
mais `openPalette` n'affiche jamais cet overlay. Sur iPhone,
l'utilisateur qui ouvrait la palette par curiosité était **piégé** :
aucun tap ne la refermait.

## Livré

`vx-shell.js` : le tap/clic sur le fond (hors boîte) ferme la palette —
comportement standard de tout dialogue :
`if (e.target === palette) palette.dataset.open = '0'`.

## Gardien neuf — `tests/test_palette_backdrop_close_lot291.py` (2 tests)

Fermeture par le fond câblée + la sortie existante (item) intacte.

## Preuves (navigateur réel, DEMO, 390 tactile + 1440)

Séquence complète aux deux viewports : ouverture au tap → **tap sur le
fond → fermée** → réouverture → **tap sur un item → fermée**. 0 erreur
console, 0 débordement. Capture envoyée.
Suite complète : **2500 passed / 2 skipped** (+2).

## Décision SW

**Bump v178 → v179** (JS du shell change) + les 5 gardiens.

## Suite

LOT 292 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.

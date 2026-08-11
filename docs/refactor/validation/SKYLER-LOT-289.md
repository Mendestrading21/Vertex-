# SKYLER LOT 289 — Cible tactile du champ de recherche (≥40px en mobile)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-289` (base : lot 288 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée

Suite directe du calibrage du lot 288 : le champ de recherche du topbar
est **LE chemin tactile vers la palette de commandes** — or il mesurait
**33px de haut** à 390px, sous la règle des cibles tactiles ≥40px que
`responsive.css` impose déjà aux boutons (`.vx-btn,.vx-tab,.vx-chip
{min-height:40px}`). Le topbar fait 62px (`--vx-topbar-h`) : un champ
de 40px y tient sans rien changer d'autre. Seule contrainte trouvée au
calibrage : l'icône loupe est calée en absolu (`top:9px`) pour un champ
de 33px → à recentrer.

## Livré

- `responsive.css` (bloc ≤640px) :
  `.vx-topbar-search input{min-height:40px}` +
  `.vx-topbar-search svg{top:50%;transform:translateY(-50%)}`.
- Gardien `tests/test_search_touch_target_lot289.py` (2 tests) :
  cible ≥40px + icône recentrée, dans le bloc mobile.

## Preuves (navigateur réel, DEMO)

- 390px : champ **40px de haut** (33 avant), icône centrée (écart
  mesuré : 0px), tap → palette ouverte (12 items), 0 erreur console,
  0 débordement — capture envoyée.
- 1440px : rien ne change (33px, icône comme avant) — desktop intact.
- Suite complète : **2498 passed / 2 skipped** (+2).

## Décision SW

**Bump v177 → v178** (CSS du shell visible change) + les 5 gardiens.

## Suite

LOT 290 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
(Échéance périodique : smoke-check complet prévu vers le lot 290.)

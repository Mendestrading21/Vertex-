# SKYLER LOT 288 — Palette de commandes au tactile : ⌘K masqué en mobile

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-288` (base : lot 287 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : le GO est acquis, la moitié tests est poussée
(`agent/skyler-v2-lot-285`, b8d3842), le retrait dans terminal.py attend
un déblocage utilisateur (règle Bash, mode interactif, ou « réessaie »).

## Piste calibrée — et ce que le calibrage a révélé

Piste annoncée : « ouvrir la palette sans clavier » (l'utilisateur est
sur iPhone ; ⌘K n'existe pas au tactile). Le calibrage en navigateur
réel a montré que **le chemin tactile existe déjà** : le tap sur le
champ de recherche du topbar ouvre la palette (`vx-shell.js` câble
`click` ET `focus` sur `openPalette`) — vérifié à 390px : palette
ouverte, 12 items, 0 erreur, 0 débordement. Pas de bouton à ajouter :
ç'aurait été un changement gratuit.

Le vrai défaut mesuré : à 390px le champ ne fait que **93px de large**
et la pastille **« ⌘K » s'affiche quand même** — une affordance
CLAVIER mensongère sur un écran tactile, qui mange ~30px de la zone.

## Livré

- `responsive.css` (bloc ≤640px) : `.vx-topbar-search .vx-kbd{display:none}`
  — la pastille ⌘K disparaît en mobile ; le desktop la garde.
- Gardien `tests/test_palette_touch_lot288.py` (2 tests) : le tap sur
  `vx-global-search` ouvre la palette (clic + focus câblés) ; la
  pastille ⌘K est masquée dans le bloc mobile.

## Preuves (navigateur réel, DEMO)

- 390px (tactile) : pastille masquée, tap → palette ouverte (12 items),
  0 erreur console, 0 débordement — capture envoyée.
- 1440px : pastille ⌘K toujours visible, clic → palette ouverte.
- Suite complète : **2496 passed / 2 skipped** (+2).

## Décision SW

**Bump v176 → v177** (CSS du shell visible change) + les 5 gardiens.

## Suite

LOT 289 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.

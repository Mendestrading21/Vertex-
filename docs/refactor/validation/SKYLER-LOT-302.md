# SKYLER LOT 302 — Clavier : le Tab traverse le topbar (la palette s'ouvrait de force)

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-302` (base : lot 301 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — parcours clavier desktop (jamais balayé)

Sondeur : 25 tabulations sur `/`, focus visible mesuré à chaque arrêt.
Bonnes nouvelles : skip-link premier arrêt et fonctionnel, **focus
visible sur 100 % des arrêts**, ordre logique sidebar → topbar.

**Défaut réel** : au Tab sur le champ de recherche, le gestionnaire
`focus` faisait `blur + openPalette()` — la palette s'ouvrait DE FORCE,
capturait le focus, et le cycle repartait du début : **les 4 boutons du
topbar (Ajouter, Connexions, Notifications, Actualiser) étaient
inatteignables au clavier** (mesuré : jamais dans les 25 arrêts).

## Livré

`vx-shell.js` : plus d'ouverture au focus. Ouvertures :
- **clic/tap** (inchangé — le chemin tactile du lot 288 est préservé) ;
- **frappe dans le champ** : `keydown` (caractère, Entrée, ↓) ouvre la
  palette et AMORCE la recherche avec le caractère saisi (Tab et
  modificateurs traversent librement).

Gardien du lot 288 mis à jour en conséquence (évolution documentée) +
gardien neuf `tests/test_keyboard_topbar_lot302.py` (2 tests).

## Preuves (navigateur réel, DEMO)

- Desktop : 24 tabulations — palette JAMAIS ouverte, **les 4 boutons du
  topbar atteints**, champ de recherche traversable ; frappe « a » →
  palette ouverte, amorcée « a », focus dans son champ. Capture envoyée.
- Tactile 390 : tap → palette ouverte (non-régression lot 288).
- 0 erreur console. Suite complète : **2516 passed / 2 skipped** (+2).

## Décision SW

**Bump v185 → v186** (JS du shell change) + les 5 gardiens.

## Suite

LOT 303 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.

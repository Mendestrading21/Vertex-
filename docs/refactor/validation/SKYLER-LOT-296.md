# SKYLER LOT 296 — Honnêteté : l'étiquette « board réel » suivait le mode

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-296` (base : lot 295 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — audit d'honnêteté des lignes source/fraîcheur

Le balayage tactile étant terminé (293/294/295), angle neuf : les
8 pages racines sondées en DEMO pour l'étiquetage démo et les lignes
`.vx-update` (source + fraîcheur). Résultat : DEMO visible sur les 8,
toutes les lignes renseignées, 0 placeholder vide — SAUF un mensonge :
**/options affichait « À l'instant · multileg_lab (board réel) » en
plein mode DEMO**. L'étiquette était codée EN DUR
(`options-structure.js`), alors que `mode: d.demo ? 'demo' : 'delayed'`
juste à côté connaissait la vérité. Violation de la règle produit
« données RÉELLES uniquement — jamais un chiffre inventé affiché comme
réel ».

## Livré (4 sites)

- `options-structure.js` : source de la carte payoff →
  `d.demo ? 'multileg_lab (board démo)' : 'multileg_lab (board réel)'` ;
  pied de la Carte-Verdict → `board ' + (d.demo ? 'démo' : 'réel')`.
- `options_intel_page.py` (2 textes statiques servis identiques dans
  les deux modes) : « depuis le board réel » → « depuis le board
  d'options » — un texte statique ne peut pas revendiquer « réel ».

## Gardien neuf — `tests/test_options_board_label_lot296.py` (2 tests)

Les deux ternaires présents + une seule occurrence « board réel »
restante (branche non-démo) + plus aucune revendication « réel » dans
les textes statiques. (1er run rouge sur mon propre décompte — corrigé
et re-prouvé.)

## Preuves (navigateur réel, DEMO)

- /options : « À l'instant · multileg_lab **(board démo)** » ;
  « board réel » absent de toute la page ; 0 erreur console. Capture
  envoyée.
- Suite complète : **2508 passed / 2 skipped** (+2).

## Décision SW

**Bump v182 → v183** (JS + HTML servis changent) + les 5 gardiens.

## Suite

LOT 297 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.

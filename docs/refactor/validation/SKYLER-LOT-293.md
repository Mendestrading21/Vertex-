# SKYLER LOT 293 — Fiche Analyse : liens d'approfondissement tappables

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-293` (base : lot 292 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — la fiche /analysis/TICKER à 390

Le shell tactile étant épuisé (288/289/291/292), calibrage du parcours
profond le plus central : la fiche d'analyse (destination de presque
tous les taps — palette, opportunités, portefeuille). Sondeur complet :
erreurs console, débordements par élément, textes cassés
(NaN/undefined), boutons non câblés, cibles < 32px.

Résultat sain partout SAUF un défaut réel : **les liens
d'approfondissement — « Calendrier complet → », « Risque complet
(positions réelles) → », « Journal complet → » — mesuraient 15px de
haut** à 390. Quasi intappables au pouce, alors qu'ils mènent aux vues
complètes. 4 sites du motif `.vx-meta > a` (3 fiche Analyse,
1 Portefeuille).

## Livré

`responsive.css` (bloc ≤640px) :
`.vx-meta a{display:inline-block;padding:13px 0}` → cible 15 + 2×13 =
**41px**, la ligne reste inline, desktop intact.

## Gardien neuf — `tests/test_meta_links_touch_lot293.py` (2 tests)

Règle mobile présente + les 3 liens d'approfondissement existent
toujours dans la fiche.

## Preuves (navigateur réel, DEMO)

- 390 : les 3 liens ont quitté la liste des cibles < 32px (mesure
  avant : h=15 ×3 ; après : plus aucun) ; 0 erreur console, 0 texte
  cassé, 0 bouton non câblé, 0 débordement réel. Capture envoyée.
- 1440 : inchangé (les éléments « hors écran » du sondeur = le tiroir
  fermé hors-canvas, faux positif).
- Suite complète : **2502 passed / 2 skipped** (+2).

## Décision SW

**Bump v179 → v180** (CSS du shell visible change) + les 5 gardiens.

## Suite

LOT 294 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.

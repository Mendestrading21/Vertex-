# SKYLER LOT 294 — Vues profondes : contrôles segmentés tappables

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-294` (base : lot 293 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — le sondeur du lot 293 sur 6 vues profondes (390)

Balayage : /markets?view=breadth, /opportunities?view=calendar,
/portfolio?view=risk, /journal?view=track-record,
/options?view=positions, /system?view=settings — erreurs console,
débordement, textes cassés, cibles < 32px (topbar exclu).

**5 vues sur 6 SAINES.** Défaut réel sur /system?view=settings : les
**7 contrôles segmentés** (densité Compact/Confort/Dense, navigation
Déployée/Réduite, animations Activées/Coupées) mesuraient **26px** —
`.vx-segmented button` (padding 5px, aucune min-height) échappe à la
règle tactile mobile `.vx-btn,.vx-tab,.vx-chip{min-height:40px}` faute
de classe vx-btn.

## Livré

`responsive.css` (bloc ≤640px) : `.vx-segmented button{min-height:40px}`
— aligné sur la règle existante, posé juste sous elle. Desktop intact
(composant aussi présent sur /design-system, même bénéfice mobile).

## Gardien neuf — `tests/test_segmented_touch_lot294.py` (2 tests)

Règle segmentée présente + la règle générale `.vx-btn,.vx-tab,.vx-chip`
toujours en place.

## Preuves (navigateur réel, DEMO)

- 390 : les 7 boutons ont quitté la liste < 32px (40px mesurés) ;
  0 erreur, 0 débordement ; les 5 autres vues restent saines au
  re-balayage. Capture envoyée.
- Suite complète : **2504 passed / 2 skipped** (+2).

## Décision SW

**Bump v180 → v181** (CSS du shell visible change) + les 5 gardiens.

## Suite

LOT 295 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
